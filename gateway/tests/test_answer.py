"""Tests for the pii rule's on_answer handling (gateway.answer and load_answer_filters)."""

from __future__ import annotations

import asyncio
import json

import pytest

from gateway import load_answer_filters
from gateway.answer import AnswerFilter
from gateway.pii import PIIScanner

ANSWER = "For questions, call FDA at 1-888-463-6332 or email info@example.org."


def _apply(answer_filter: AnswerFilter, text: str) -> str:
    return asyncio.run(answer_filter.apply(text))


def test_redact_replaces_each_match() -> None:
    result = _apply(AnswerFilter(PIIScanner.from_config(), action="redact"), ANSWER)
    assert result == (
        "For questions, call FDA at [REDACTED:PHONE] or email [REDACTED:EMAIL]."
    )


def test_block_withholds_the_whole_answer() -> None:
    result = _apply(AnswerFilter(PIIScanner.from_config(), action="block"), ANSWER)
    assert "463-6332" not in result
    assert result.startswith("[Answer withheld by gateway rule 'pii'")
    assert "1 email, 1 phone" in result


@pytest.mark.parametrize("action", ["log", "off"])
def test_log_and_off_leave_the_answer_unchanged(action: str) -> None:
    assert _apply(AnswerFilter(PIIScanner.from_config(), action=action), ANSWER) == ANSWER


def test_answer_without_pii_is_unchanged() -> None:
    text = "| state | rate |\n|---|---|\n| Maryland | 12.5 |"
    assert _apply(AnswerFilter(PIIScanner.from_config(), action="redact"), text) == text


def test_detectors_setting_limits_what_is_redacted() -> None:
    scanner = PIIScanner.from_config(detectors=["email"])
    result = _apply(AnswerFilter(scanner, action="redact"), ANSWER)
    assert "1-888-463-6332" in result
    assert "[REDACTED:EMAIL]" in result


class _FailingDetector:
    async def find(self, text: str) -> list[tuple[str, str]]:
        raise RuntimeError("model down")


class _NameDetector:
    async def find(self, text: str) -> list[tuple[str, str]]:
        return [("person_name", "Jane Doe")]


def test_ai_failure_blocks_by_default() -> None:
    answer_filter = AnswerFilter(
        PIIScanner.from_config(), action="redact", ai_detector=_FailingDetector()
    )
    assert "can't be checked" in _apply(answer_filter, ANSWER)


def test_ai_failure_falls_back_to_regex_only() -> None:
    answer_filter = AnswerFilter(
        PIIScanner.from_config(),
        action="redact",
        ai_detector=_FailingDetector(),
        ai_on_error="regex_only",
    )
    assert "[REDACTED:PHONE]" in _apply(answer_filter, ANSWER)


def test_ai_findings_are_redacted() -> None:
    answer_filter = AnswerFilter(
        PIIScanner.from_config(), action="redact", ai_detector=_NameDetector()
    )
    assert _apply(answer_filter, "Recalled by Jane Doe.") == (
        "Recalled by [REDACTED:PERSON_NAME]."
    )


def test_invalid_action_is_rejected() -> None:
    with pytest.raises(ValueError, match="on_answer"):
        AnswerFilter(PIIScanner.from_config(), action="hide")  # type: ignore[arg-type]


def _write_config(tmp_path, rule: dict):
    path = tmp_path / "gateway_config.json"
    path.write_text(json.dumps({"rules": [rule]}), encoding="utf-8")
    return path


def test_load_defaults_to_redact(tmp_path) -> None:
    filters = load_answer_filters(_write_config(tmp_path, {"name": "pii", "type": "pii"}))
    assert [f.action for f in filters] == ["redact"]


def test_load_skips_off_and_disabled_rules(tmp_path) -> None:
    off = _write_config(tmp_path, {"name": "pii", "type": "pii", "on_answer": "off"})
    assert load_answer_filters(off) == []
    disabled = _write_config(tmp_path, {"name": "pii", "type": "pii", "enabled": False})
    assert load_answer_filters(disabled) == []


def test_load_missing_config_means_no_filters(tmp_path) -> None:
    assert load_answer_filters(tmp_path / "missing.json") == []
