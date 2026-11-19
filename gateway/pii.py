"""Regex-based PII detectors used by the gateway's ``pii`` rule.

Each detector is a compiled pattern plus an optional validator that weeds out
false positives (e.g. the Luhn check for card numbers). Patterns require the
usual separators (``123-45-6789``, ``(301) 555-0100``) so bare numeric IDs in
table data aren't flagged.
"""

from __future__ import annotations

import ipaddress
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass


def _luhn_ok(match: str) -> bool:
    """Return whether the digits in ``match`` pass the Luhn checksum."""
    digits = [int(c) for c in match if c.isdigit()]
    if not 13 <= len(digits) <= 19:
        return False
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def _ipv4_ok(match: str) -> bool:
    """Return whether ``match`` is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(match)
    except ValueError:
        return False
    return True


@dataclass(frozen=True)
class Detector:
    """One kind of PII: its label, pattern and optional validator."""

    name: str
    pattern: re.Pattern[str]
    validate: Callable[[str], bool] | None = None

    def finditer(self, text: str):
        """Yield the matches in ``text`` that pass the validator."""
        for m in self.pattern.finditer(text):
            if self.validate is None or self.validate(m.group()):
                yield m


BUILTIN_DETECTORS: dict[str, Detector] = {
    d.name: d
    for d in (
        Detector(
            "ssn",
            re.compile(r"\b(?!000|666|9\d\d)\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b"),
        ),
        Detector(
            "email",
            re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        ),
        Detector(
            "phone",
            re.compile(
                r"(?<![\w-])(?:\+?1[-.\s]?)?(?:\(\d{3}\)\s?|\d{3}[-.\s])\d{3}[-.\s]\d{4}\b"
            ),
        ),
        Detector(
            "credit_card",
            re.compile(r"\b\d(?:[ -]?\d){12,18}\b"),
            _luhn_ok,
        ),
        Detector(
            "ip_address",
            re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"),
            _ipv4_ok,
        ),
    )
}


class PIIScanner:
    """Finds and redacts PII in strings and nested JSON-like values."""

    def __init__(self, detectors: list[Detector]) -> None:
        self.detectors = detectors

    @classmethod
    def from_config(
        cls,
        detectors: list[str] | None = None,
        custom_patterns: dict[str, str] | None = None,
    ) -> PIIScanner:
        """Build a scanner from builtin detector names plus extra regexes.

        Args:
            detectors: Names from :data:`BUILTIN_DETECTORS`; ``None`` means all.
            custom_patterns: Extra ``{name: regex}`` detectors.

        Raises:
            ValueError: If a detector name is unknown.
        """
        names = list(BUILTIN_DETECTORS) if detectors is None else detectors
        unknown = [n for n in names if n not in BUILTIN_DETECTORS]
        if unknown:
            raise ValueError(
                f"Unknown PII detector(s) {unknown}; choose from {list(BUILTIN_DETECTORS)}"
            )
        found = [BUILTIN_DETECTORS[n] for n in names]
        for name, regex in (custom_patterns or {}).items():
            found.append(Detector(name, re.compile(regex)))
        return cls(found)

    def with_values(self, values: list[tuple[str, str]]) -> PIIScanner:
        """Return a scanner that also matches each ``(kind, value)`` literally.

        The literal detectors run first, longest value first, so a value is
        redacted whole before a regex can match part of it.
        """
        ordered = sorted(values, key=lambda kv: len(kv[1]), reverse=True)
        literal = [Detector(kind, re.compile(re.escape(value))) for kind, value in ordered]
        return PIIScanner(literal + self.detectors)

    def scan(self, value: object) -> Counter[str]:
        """Count PII matches by detector name anywhere inside ``value``."""
        counts: Counter[str] = Counter()
        for text in iter_strings(value):
            for detector in self.detectors:
                counts[detector.name] += sum(1 for _ in detector.finditer(text))
        return +counts

    def redact_text(self, text: str) -> str:
        """Replace every match in ``text`` with ``[REDACTED:<NAME>]``."""
        for detector in self.detectors:
            label = f"[REDACTED:{detector.name.upper()}]"
            text = detector.pattern.sub(
                lambda m: label
                if detector.validate is None or detector.validate(m.group())
                else m.group(),
                text,
            )
        return text

    def redact(self, value: object) -> object:
        """Return a copy of ``value`` with every string redacted."""
        if isinstance(value, str):
            return self.redact_text(value)
        if isinstance(value, dict):
            return {k: self.redact(v) for k, v in value.items()}
        if isinstance(value, list | tuple):
            return [self.redact(v) for v in value]
        return value


def iter_strings(value: object):
    """Yield every string nested inside ``value``."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from iter_strings(v)
    elif isinstance(value, list | tuple):
        for v in value:
            yield from iter_strings(v)
