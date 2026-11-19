"""Adapter between the web client and the chat backend in :mod:`app`.

This is the only client module that imports :mod:`app`. Importing it loads the
MCP gateway (``server`` -> ``servers``) in-process.
"""

from __future__ import annotations

import logging

from app import run_chat

logger = logging.getLogger(__name__)

# Appended to every prompt so tabular answers arrive as markdown tables, which
# the client turns into grids. app.run_chat's system prompt only says "summarize".
_TABLE_FORMAT_HINT = (
    "\n\nFormatting: when the answer includes tabular data, present each result set as a "
    "separate GitHub-flavoured markdown table with a header row, preceded by a short "
    "heading line."
)


class BackendError(Exception):
    """``run_chat`` failed; the message is safe to show in the UI."""


async def ask(prompt: str) -> str:
    """Answer ``prompt`` with :func:`app.run_chat`.

    Args:
        prompt: The user's question.

    Returns:
        The model's raw answer, usually markdown.

    Raises:
        BackendError: If the model call or any tool call fails.
    """
    logger.info("Submitting query (%d chars)", len(prompt))
    try:
        answer = await run_chat(prompt + _TABLE_FORMAT_HINT)
    except Exception as exc:
        logger.exception("run_chat failed")
        raise BackendError(f"{type(exc).__name__}: {exc}") from exc
    logger.info("Received answer (%d chars)", len(answer))
    return answer
