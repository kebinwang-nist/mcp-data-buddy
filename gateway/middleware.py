"""Gateway middleware that applies the ``pii`` rule to tool calls."""

from __future__ import annotations

import logging
from typing import Literal

import mcp_types as mt
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.tools.base import ToolResult
from mcp_types import TextContent

from gateway.ai_check import AIDetector
from gateway.pii import PIIScanner, iter_strings

logger = logging.getLogger("gateway.pii")

Action = Literal["block", "redact", "log", "off"]
_ACTIONS = ("block", "redact", "log", "off")
AIErrorAction = Literal["block", "regex_only"]
_AI_ERROR_ACTIONS = ("block", "regex_only")


class PIIMiddleware(Middleware):
    """Detects PII in tool arguments and tool results.

    ``on_request`` and ``on_response`` pick what happens when PII is found:

    - ``block``: fail the call with a :class:`ToolError` naming the PII kinds.
    - ``redact``: replace each match with ``[REDACTED:<KIND>]`` and continue.
    - ``log``: log a warning and pass the data through unchanged.
    - ``off``: skip scanning.

    With an ``ai_detector``, a separate model also checks the text for PII the
    regexes miss (names, addresses, ...). If that model call fails,
    ``ai_on_error`` either blocks the call (``block``) or falls back to the
    regexes (``regex_only``).

    Matched values are never logged, only their kinds and counts.
    """

    def __init__(
        self,
        scanner: PIIScanner,
        *,
        on_request: Action = "log",
        on_response: Action = "redact",
        tools: list[str] | None = None,
        exclude_tools: list[str] | None = None,
        ai_detector: AIDetector | None = None,
        ai_on_error: AIErrorAction = "block",
    ) -> None:
        for label, action in (("on_request", on_request), ("on_response", on_response)):
            if action not in _ACTIONS:
                raise ValueError(f"{label} must be one of {_ACTIONS}, got {action!r}")
        if ai_on_error not in _AI_ERROR_ACTIONS:
            raise ValueError(
                f"ai_on_error must be one of {_AI_ERROR_ACTIONS}, got {ai_on_error!r}"
            )
        self.scanner = scanner
        self.ai_detector = ai_detector
        self.ai_on_error = ai_on_error
        self.request_action = on_request
        self.response_action = on_response
        self.tools = set(tools) if tools is not None else None
        self.exclude_tools = set(exclude_tools or [])

    def _applies_to(self, tool: str) -> bool:
        if tool in self.exclude_tools:
            return False
        return self.tools is None or tool in self.tools

    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        tool = context.message.name
        if not self._applies_to(tool):
            return await call_next(context)

        if self.request_action != "off" and context.message.arguments:
            scanner = await self._scanner_for(
                tool, "arguments", context.message.arguments
            )
            found = scanner.scan(context.message.arguments)
            if found:
                context = self._handle_request(scanner, context, found)

        result = await call_next(context)

        # Only plain results carry content; pass task/input-required results through.
        if self.response_action == "off" or type(result) is not ToolResult:
            return result
        texts = [b.text for b in result.content if isinstance(b, TextContent)]
        scanner = await self._scanner_for(
            tool, "result", [texts, result.structured_content]
        )
        # The text blocks usually repeat the structured content, so take the
        # larger count per kind rather than the sum.
        found = scanner.scan(texts) | scanner.scan(result.structured_content)
        if not found:
            return result
        return self._handle_response(scanner, tool, result, found)

    async def _scanner_for(self, tool: str, where: str, value: object) -> PIIScanner:
        """Return the regex scanner plus whatever the check model finds in ``value``."""
        if self.ai_detector is None:
            return self.scanner
        # Dedupe: text blocks often repeat the structured content verbatim.
        text = "\n".join(dict.fromkeys(iter_strings(value)))
        if not text.strip():
            return self.scanner
        try:
            found = await self.ai_detector.find(text)
        except Exception as e:
            logger.warning(
                "PII check model failed on %s of %s (%s): %s",
                where, tool, self.ai_on_error, type(e).__name__,
            )
            if self.ai_on_error == "block":
                raise ToolError(
                    f"Blocked by gateway rule 'pii': the PII check model failed on the "
                    f"{where} of {tool}, so the call can't be checked. Try again later."
                ) from e
            return self.scanner
        return self.scanner.with_values(found) if found else self.scanner

    def _handle_request(self, scanner, context, found) -> MiddlewareContext:
        tool = context.message.name
        logger.warning(
            "PII in arguments to %s (%s): %s", tool, self.request_action, _summary(found)
        )
        if self.request_action == "block":
            raise ToolError(
                f"Blocked by gateway rule 'pii': the arguments to {tool} contain "
                f"{_summary(found)}. Remove personal data from the request and retry."
            )
        if self.request_action == "redact":
            message = context.message.model_copy(
                update={"arguments": scanner.redact(context.message.arguments)}
            )
            return context.copy(message=message)
        return context

    def _handle_response(
        self, scanner: PIIScanner, tool: str, result: ToolResult, found
    ) -> ToolResult:
        logger.warning(
            "PII in result of %s (%s): %s", tool, self.response_action, _summary(found)
        )
        if self.response_action == "block":
            raise ToolError(
                f"Blocked by gateway rule 'pii': the result of {tool} contains "
                f"{_summary(found)}."
            )
        if self.response_action == "redact":
            content = [
                b.model_copy(update={"text": scanner.redact_text(b.text)})
                if isinstance(b, TextContent)
                else b
                for b in result.content
            ]
            return ToolResult(
                content=content,
                structured_content=scanner.redact(result.structured_content),
                meta=result.meta,
                is_error=result.is_error,
            )
        return result


def _summary(found) -> str:
    """Format detector counts, e.g. ``2 email, 1 ssn``."""
    return ", ".join(f"{n} {name}" for name, n in sorted(found.items()))
