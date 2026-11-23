"""Tests for the "NO PII CHECK" opt-out in app.py and the unchecked gateway in server.py."""

from __future__ import annotations

import asyncio

import pytest
from fastmcp import Client, FastMCP

import app
from gateway.middleware import PIIMiddleware
from gateway.pii import PIIScanner
from server import mcp, mcp_unchecked


@pytest.mark.parametrize(
    ("prompt", "question"),
    [
        ("NO PII CHECK What is FDA's phone?", "What is FDA's phone?"),
        ("NO PII CHECK: What is FDA's phone?", "What is FDA's phone?"),
        ("NO PII CHECK - What is FDA's phone?", "What is FDA's phone?"),
        ("NO PII CHECK\nWhat is FDA's phone?", "What is FDA's phone?"),
        (
            "NO PII CHECK. what's the FDA contact for food recall",
            "what's the FDA contact for food recall",
        ),
        ("NO PII CHECK, what is FDA's phone?", "what is FDA's phone?"),
        ("NO PII CHECK! What is FDA's phone?", "What is FDA's phone?"),
        ('NO PII CHECK: "FDA" phone?', '"FDA" phone?'),
        ("NO PII CHECK", ""),
        ("NO PII CHECK.", ""),
    ],
)
def test_prefix_opts_out_and_is_removed(prompt: str, question: str) -> None:
    assert app._split_pii_opt_out(prompt) == (True, question)


@pytest.mark.parametrize(
    "prompt",
    [
        "What is FDA's phone?",
        "no pii check What is FDA's phone?",  # case-sensitive
        " NO PII CHECK What is FDA's phone?",  # must be at the very start
        "Please, NO PII CHECK: What is FDA's phone?",
        "NO PII CHECKS please",  # not a whole word
        "NO PII CHECKER",
        "NO PII CHECK2 what is FDA's phone?",
        "NO PII CHECK_ what is FDA's phone?",
    ],
)
def test_other_prompts_keep_the_check(prompt: str) -> None:
    assert app._split_pii_opt_out(prompt) == (False, prompt)


def test_only_the_checked_gateway_has_the_pii_middleware() -> None:
    assert any(isinstance(m, PIIMiddleware) for m in mcp.middleware)
    assert not any(isinstance(m, PIIMiddleware) for m in mcp_unchecked.middleware)


def test_both_gateways_expose_the_same_tools() -> None:
    async def names(server: FastMCP) -> list[str]:
        async with Client(server) as client:
            return sorted(t.name for t in await client.list_tools())

    assert asyncio.run(names(mcp)) == asyncio.run(names(mcp_unchecked))


def test_middleware_redacts_only_when_present() -> None:
    """Same tool, with and without the PII middleware."""

    def build(checked: bool) -> FastMCP:
        server = FastMCP("t")

        @server.tool()
        def contact() -> str:
            return "Call 1-888-463-6332."

        if checked:
            server.add_middleware(PIIMiddleware(PIIScanner.from_config()))
        return server

    async def call(server: FastMCP) -> str:
        async with Client(server) as client:
            return (await client.call_tool("contact", {})).content[0].text

    assert asyncio.run(call(build(True))) == "Call [REDACTED:PHONE]."
    assert asyncio.run(call(build(False))) == "Call 1-888-463-6332."
