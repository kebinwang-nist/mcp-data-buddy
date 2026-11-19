"""Gateway rules applied to every tool call that passes through ``server.py``.

Rules live in the project-root ``gateway_config.json``. Each enabled rule
becomes a FastMCP middleware on the gateway, so it covers the tools of every
mounted server. Supported rule types:

- ``pii``: detects personal data (SSNs, emails, phone numbers, card numbers,
  IP addresses, plus any ``custom_patterns``) in tool arguments and results,
  and blocks, redacts or logs it. With ``ai_check`` enabled, a separate model
  (the ``GATEWAY_AI_*`` settings) also finds names, addresses and dates of
  birth. See :class:`gateway.middleware.PIIMiddleware`.
"""

import json
from pathlib import Path

from fastmcp.server.middleware import Middleware

from gateway.ai_check import AIDetector
from gateway.middleware import PIIMiddleware
from gateway.pii import PIIScanner

_GATEWAY_CONFIG = Path(__file__).resolve().parent.parent / "gateway_config.json"


def _build_pii(rule: dict) -> Middleware:
    scanner = PIIScanner.from_config(
        detectors=rule.get("detectors"),
        custom_patterns=rule.get("custom_patterns"),
    )
    ai = rule.get("ai_check") or {}
    ai_detector = (
        AIDetector.from_settings(
            kinds=ai.get("kinds"),
            max_chars=ai.get("max_chars", 20_000),
            timeout_seconds=ai.get("timeout_seconds", 30.0),
        )
        if ai.get("enabled", False)
        else None
    )
    return PIIMiddleware(
        scanner,
        on_request=rule.get("on_request", "log"),
        on_response=rule.get("on_response", "redact"),
        tools=rule.get("tools"),
        exclude_tools=rule.get("exclude_tools"),
        ai_detector=ai_detector,
        ai_on_error=ai.get("on_error", "block"),
    )


_RULE_TYPES = {"pii": _build_pii}


def load_rules(path: Path = _GATEWAY_CONFIG) -> list[Middleware]:
    """Build a middleware for every enabled rule in ``gateway_config.json``.

    A missing config file means no rules.

    Raises:
        ValueError: If a rule has an unknown ``type`` or invalid settings.
    """
    if not path.exists():
        return []
    middleware: list[Middleware] = []
    for rule in json.loads(path.read_text(encoding="utf-8")).get("rules", []):
        if not rule.get("enabled", True):
            continue
        build = _RULE_TYPES.get(rule.get("type"))
        if build is None:
            raise ValueError(
                f"Rule {rule.get('name')!r} has unknown type {rule.get('type')!r}; "
                f"choose from {list(_RULE_TYPES)}"
            )
        middleware.append(build(rule))
    return middleware
