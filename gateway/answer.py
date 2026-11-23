"""Apply the ``pii`` rule to the chat model's final answer.

The gateway middleware only sees tool calls. The model can still write PII into
its answer, either copied from a tool result or from what it already knows, so
:func:`app.run_chat` passes the answer through :class:`AnswerFilter` before
returning it. The filter uses the same detectors, custom patterns and optional
AI check as the rule's tool-call checks; ``on_answer`` picks the action.
"""

from __future__ import annotations

import logging
from typing import Literal

from gateway.ai_check import AIDetector
from gateway.pii import PIIScanner

logger = logging.getLogger("gateway.pii")

AnswerAction = Literal["block", "redact", "log", "off"]
_ACTIONS = ("block", "redact", "log", "off")
_AI_ERROR_ACTIONS = ("block", "regex_only")


class AnswerFilter:
    """Detects PII in a final answer and blocks, redacts or logs it.

    - ``block``: replace the whole answer with a short notice naming the PII kinds.
    - ``redact``: replace each match with ``[REDACTED:<KIND>]``.
    - ``log``: log a warning and return the answer unchanged.
    - ``off``: return the answer unchanged without scanning.

    Matched values are never logged, only their kinds and counts.
    """

    def __init__(
        self,
        scanner: PIIScanner,
        *,
        action: AnswerAction = "redact",
        ai_detector: AIDetector | None = None,
        ai_on_error: Literal["block", "regex_only"] = "block",
        rule_name: str = "pii",
    ) -> None:
        if action not in _ACTIONS:
            raise ValueError(f"on_answer must be one of {_ACTIONS}, got {action!r}")
        if ai_on_error not in _AI_ERROR_ACTIONS:
            raise ValueError(
                f"ai_on_error must be one of {_AI_ERROR_ACTIONS}, got {ai_on_error!r}"
            )
        self.scanner = scanner
        self.action = action
        self.ai_detector = ai_detector
        self.ai_on_error = ai_on_error
        self.rule_name = rule_name

    async def apply(self, answer: str) -> str:
        """Return ``answer`` after applying the rule's ``on_answer`` action."""
        if self.action == "off" or not answer.strip():
            return answer
        scanner = self.scanner
        if self.ai_detector is not None:
            try:
                found_values = await self.ai_detector.find(answer)
            except Exception as e:  # noqa: BLE001 - any failure is handled by ai_on_error
                logger.warning(
                    "PII check model failed on the answer (%s): %s",
                    self.ai_on_error, type(e).__name__,
                )
                if self.ai_on_error == "block":
                    return (
                        f"[Answer withheld by gateway rule '{self.rule_name}': the PII "
                        "check model failed, so the answer can't be checked. Try again later.]"
                    )
            else:
                if found_values:
                    scanner = scanner.with_values(found_values)

        found = scanner.scan(answer)
        if not found:
            return answer
        summary = ", ".join(f"{n} {name}" for name, n in sorted(found.items()))
        logger.warning("PII in the answer (%s): %s", self.action, summary)
        if self.action == "block":
            return f"[Answer withheld by gateway rule '{self.rule_name}': it contains {summary}.]"
        if self.action == "redact":
            return scanner.redact_text(answer)
        return answer
