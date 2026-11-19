"""Pure openFDA helpers shared by the FDA server and the skill generator (no I/O).

openFDA (``https://api.fda.gov/<category>/<endpoint>.json``) is an Elasticsearch-backed REST
API with the query parameters ``search``, ``count``, ``limit``, ``skip`` and ``sort``. This
module holds the rules both :mod:`servers.fda.server` and :mod:`servers.fda.build_skills`
apply: dataset id normalization and scope, how an HTTP status maps to ok / empty / retry /
error, the retry delay, Basic-auth for the optional API key, and the field-name checks and
client-side projection used by ``get_dataset``.
"""

from __future__ import annotations

import difflib
import re
from collections.abc import Collection, Iterable, Sequence
from dataclasses import dataclass
from typing import Any, Literal

import httpx

MAX_LIMIT = 1000
MAX_SKIP = 25000
DEFAULT_LIMIT = 10
DEFAULT_COUNT_LIMIT = 100
MAX_ATTEMPTS = 4  # waits of 1 s, 2 s and 4 s between attempts
RETRY_STATUSES = frozenset({429, 502, 503, 504})
MAX_RETRY_AFTER = 30.0
CATEGORIES = ("drug", "food")

_HOST_PREFIX = re.compile(r"^(?:https?://)?api\.fda\.gov(?=/|$)", re.IGNORECASE)
_IN_SCOPE = re.compile(r"^(?:drug|food)/[a-z0-9]+$")
_QUOTED = re.compile(r'"(?:[^"\\]|\\.)*"')
_FIELD_TERM = re.compile(r"([A-Za-z_][A-Za-z0-9_.]*)\s*:\s*([A-Za-z_][A-Za-z0-9_.]*)?")
_EXISTENCE = ("_exists_", "_missing_")
_NUMBER = re.compile(r"\d+(?:\.\d+)?")
_KEY_HINT = "Set OPENFDA_API_KEY in .env (count limit 1000 needs a key; use 999 or less)"
_MISSING = object()


def normalize_dataset_id(text: str) -> str:
    """Return the openFDA dataset id in ``text``, e.g. ``"drug/event"``.

    Accepts ``drug/event``, ``/drug/event.json`` and full URLs such as
    ``https://api.fda.gov/drug/event.json?limit=1``. Whitespace and backticks are stripped
    and the result is lowercased.
    """
    value = text.strip().strip("`").strip()
    value = _HOST_PREFIX.sub("", value)
    value = value.split("?", 1)[0].split("#", 1)[0]
    value = value.strip("/").removesuffix(".json")
    return value.lower()


def in_scope(dataset_id: str) -> bool:
    """Return whether ``dataset_id`` is a drug or food endpoint id (``drug/<x>``, ``food/<x>``)."""
    return bool(_IN_SCOPE.match(dataset_id))


@dataclass(frozen=True, slots=True)
class Outcome:
    """How a response is handled: ``ok``, ``empty`` (no matches), ``retry`` or ``error``."""

    kind: Literal["ok", "empty", "retry", "error"]
    message: str


def _error_body(payload: object) -> dict[str, Any]:
    """Return ``payload["error"]`` if it is a dict, else an empty dict."""
    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict):
            return error
    return {}


def classify(status: int, payload: object) -> Outcome:
    """Map an openFDA HTTP status and parsed JSON body (or ``None``) to an :class:`Outcome`.

    - 200: ``ok``.
    - 404 with ``error.code == "NOT_FOUND"`` ("No matches found!", "Nothing to count"):
      ``empty``.
    - 429, 502, 503, 504, and a 500 without ``error.details``: ``retry``.
    - 500 with ``error.details`` (query syntax error, count on a text field): ``error``.
    - Anything else: ``error`` with the API code and message; for a missing or invalid API
      key, a hint to set ``OPENFDA_API_KEY``.
    """
    error = _error_body(payload)
    code = str(error.get("code") or "")
    message = str(error.get("message") or "")
    if status == 200:
        return Outcome("ok", "")
    if status == 404 and code == "NOT_FOUND":
        return Outcome("empty", message or "No matches found!")
    if status in RETRY_STATUSES:
        return Outcome("retry", f"HTTP {status} {code}".rstrip())
    if status == 500:
        details = error.get("details")
        if details:
            return Outcome("error", f"{message or 'Server error'}: {str(details)[:500]}")
        return Outcome("retry", f"HTTP 500 {code}".rstrip())
    text = " ".join(part for part in (f"HTTP {status}", code) if part)
    if message:
        text = f"{text}: {message}"
    if code in ("API_KEY_MISSING", "API_KEY_INVALID"):
        text = f"{text.rstrip('.')}. {_KEY_HINT}."
    return Outcome("error", text)


def retry_delay(attempt: int, retry_after: str | None) -> float:
    """Return the wait in seconds before retrying after attempt number ``attempt`` (1-based).

    Exponential (1, 2, 4, ... seconds), raised to a numeric ``Retry-After`` header value when
    that is larger, and capped at :data:`MAX_RETRY_AFTER`.
    """
    delay = float(2 ** (attempt - 1))
    value = (retry_after or "").strip()
    if _NUMBER.fullmatch(value):  # an HTTP-date Retry-After is ignored
        delay = max(delay, float(value))
    return min(delay, MAX_RETRY_AFTER)


def basic_auth(api_key: str | None) -> httpx.BasicAuth | None:
    """Return Basic auth with ``api_key`` as username, or ``None`` when the key is blank.

    openFDA accepts the key as the Basic-auth username, which keeps it out of request URLs
    (and so out of httpx's INFO request logs).
    """
    key = (api_key or "").strip()
    return httpx.BasicAuth(key, "") if key else None


def strip_exact(path: str) -> str:
    """Return ``path`` without a trailing ``.exact`` suffix."""
    return path.removesuffix(".exact")


def search_fields(search: str) -> list[str]:
    """Return the field names used in an openFDA ``search`` expression, de-duplicated.

    Quoted phrases are ignored, a trailing ``.exact`` is dropped, and for ``_exists_:f`` /
    ``_missing_:f`` the field ``f`` is returned.
    """
    unquoted = _QUOTED.sub(" ", search)
    found: list[str] = []
    for match in _FIELD_TERM.finditer(unquoted):
        name, after = match.group(1), match.group(2)
        if name in _EXISTENCE:
            if not after:
                continue
            name = after
        found.append(strip_exact(name))
    return list(dict.fromkeys(found))


def _is_known(path: str, known: Collection[str]) -> bool:
    """Return whether ``path`` is a known field or a parent object of one."""
    if path in known:
        return True
    prefix = f"{path}."
    return any(name.startswith(prefix) for name in known)


def field_hints(paths: Iterable[str], known: Collection[str]) -> list[str]:
    """Return one hint per unknown field in ``paths``, with up to 3 close matches.

    A path is known if it is in ``known`` or is a parent object of a known field (e.g.
    ``openfda`` or ``patient.drug``). A trailing ``.exact`` is ignored.
    """
    hints: list[str] = []
    for path in dict.fromkeys(strip_exact(p) for p in paths if p):
        if _is_known(path, known):
            continue
        close = difflib.get_close_matches(path, list(known), n=3, cutoff=0.6)
        suggestion = " or ".join(f"'{c}'" for c in close)
        tail = f"; did you mean {suggestion}?" if close else "."
        hints.append(f"Unknown field '{path}'{tail}")
    return hints


def _tree(paths: Sequence[str]) -> dict[str, Any]:
    """Build a nested dict of path parts from dotted ``paths``."""
    tree: dict[str, Any] = {}
    for path in paths:
        node = tree
        for part in path.split("."):
            node = node.setdefault(part, {})
    return tree


def _apply(value: Any, tree: dict[str, Any]) -> Any:
    """Keep only the parts of ``value`` named in ``tree``; ``_MISSING`` if none exist."""
    if not tree:
        return value
    if isinstance(value, list):
        items = [_apply(item, tree) for item in value]
        kept = [item for item in items if item is not _MISSING]
        return kept if kept else _MISSING
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, sub in tree.items():
            if key in value:
                picked = _apply(value[key], sub)
                if picked is not _MISSING:
                    out[key] = picked
        return out if out else _MISSING
    return _MISSING


def project(record: dict[str, Any], paths: Sequence[str]) -> dict[str, Any]:
    """Return ``record`` with only the dotted ``paths`` kept.

    Lists are traversed (each element projected), and keys missing from the record are
    omitted, e.g. ``project({"a": {"b": 1, "c": 2}}, ["a.b"]) == {"a": {"b": 1}}``.
    """
    picked = _apply(record, _tree([p for p in paths if p]))
    return picked if isinstance(picked, dict) else {}
