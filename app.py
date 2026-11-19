"""Chat entry point: an OpenAI-compatible model driving the MCP server tools.

Connects to the local gateway MCP server (``server.py``), which mounts every
server registered in :mod:`servers`, exposes all their tools to an
OpenAI-compatible chat model hosted at the configured ``AI_API_BASE``,
and runs a tool-calling loop so the
model can answer questions using those tools.

Configuration (API key, base URL, model) is resolved from the environment /
``.env`` via :mod:`config`; nothing sensitive is hardcoded.

Run with: ``python app.py "your question"`` (or no argument for a default).
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys

from fastmcp import Client
from openai import AsyncOpenAI

from config import get_ai_settings
from server import mcp

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("app")

# Bound the tool-calling loop so a misbehaving model can't spin forever.
_MAX_TOOL_ITERATIONS = 25
# Tool results are resent with every request; cap each so a few wide table
# pages can't push the request past the gateway's size limit (HTTP 413).
_MAX_TOOL_RESULT_CHARS = 20_000


def _mcp_tools_to_openai_schema(tools: list) -> list[dict]:
    """Convert MCP tool definitions to OpenAI ``tools`` function schemas.

    Args:
        tools: Tool definitions returned by the FastMCP client.

    Returns:
        A list of OpenAI-compatible tool/function specifications.
    """
    openai_tools: list[dict] = []
    for tool in tools:
        openai_tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.input_schema or {"type": "object", "properties": {}},
                },
            }
        )
    return openai_tools


def _extract_tool_result_text(result) -> str:
    """Flatten a FastMCP tool-call result into a plain string for the model.

    Args:
        result: The ``CallToolResult`` returned by the FastMCP client.

    Returns:
        The textual content of the tool result.
    """
    # Prefer structured content when present, otherwise concatenate text blocks.
    if getattr(result, "data", None) is not None:
        data = result.data
        return data if isinstance(data, str) else json.dumps(data)

    parts: list[str] = []
    for block in getattr(result, "content", []) or []:
        text = getattr(block, "text", None)
        if text is not None:
            parts.append(text)
    return "\n".join(parts) if parts else ""


async def run_chat(user_prompt: str) -> str:
    """Answer ``user_prompt`` using the MCP tools and the chat model.

    Args:
        user_prompt: The user's question.

    Returns:
        The model's final natural-language answer.
    """
    settings = get_ai_settings()

    # OpenAI-compatible client pointed at the configured endpoint.
    client = AsyncOpenAI(
        api_key=settings.ai_api_key,
        base_url=settings.ai_api_base,
    )

    # Connect to the MCP server in-process and discover its tools.
    async with Client(mcp) as mcp_client:
        tools = await mcp_client.list_tools()
        openai_tools = _mcp_tools_to_openai_schema(tools)
        logger.info("Discovered %d MCP tool(s): %s", len(tools), [t.name for t in tools])

        messages: list[dict] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Use the provided tools when they "
                    "help answer the user's question, then summarize the result."
                ),
            },
            {"role": "user", "content": user_prompt},
        ]

        for _ in range(_MAX_TOOL_ITERATIONS):
            response = await client.chat.completions.create(
                model=settings.ai_model,
                messages=messages,
                tools=openai_tools or None,
                # No temperature override: Claude 5 models only
                # accept the default, and other endpoints work fine with it.
            )
            choice = response.choices[0].message

            # No tool calls: the model produced its final answer.
            if not choice.tool_calls:
                return choice.content or ""

            # Record the assistant's tool-call request, then execute each call.
            messages.append(
                {
                    "role": "assistant",
                    "content": choice.content,
                    "tool_calls": [tc.model_dump() for tc in choice.tool_calls],
                }
            )

            for tool_call in choice.tool_calls:
                name = tool_call.function.name
                try:
                    arguments = json.loads(tool_call.function.arguments or "{}")
                except json.JSONDecodeError:
                    arguments = {}
                logger.info("-> Calling tool %s with %s", name, arguments)

                # Hand tool errors back to the model instead of crashing, so it
                # can read the message (e.g. "Did you mean ...") and retry.
                result = await mcp_client.call_tool(name, arguments, raise_on_error=False)
                content = _extract_tool_result_text(result)
                if result.is_error:
                    logger.warning("Tool %s returned an error: %s", name, content)
                    content = f"Error: {content}"
                elif len(content) > _MAX_TOOL_RESULT_CHARS:
                    logger.warning(
                        "Truncated %s result from %d to %d chars",
                        name, len(content), _MAX_TOOL_RESULT_CHARS,
                    )
                    content = (
                        content[:_MAX_TOOL_RESULT_CHARS]
                        + f"\n[TRUNCATED: result was {len(content)} chars. "
                        "Request fewer rows (smaller limit) and page with offset.]"
                    )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": content,
                    }
                )

        logger.warning("Reached max tool iterations without a final answer.")
        return "Stopped after too many tool calls without a final answer."


async def main() -> None:
    """Parse the prompt from argv and print the model's answer."""
    user_prompt = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "Which CDC datasets cover adult smoking rates?"
    )
    print(f"User: {user_prompt}\n")

    answer = await run_chat(user_prompt)
    print(f"AI: {answer}")


if __name__ == "__main__":
    asyncio.run(main())
