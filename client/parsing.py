"""Split a raw model answer into prose text and grid-ready tables.

Pure functions only: no I/O and no NiceGUI import, so this module is easy to
unit test. :func:`parse_response` never raises; anything it cannot turn into a
grid stays in the text.
"""

from __future__ import annotations

import json
import re
from typing import Any

from client.models import CellValue, GridData, QueryResult

# A markdown table separator row, e.g. ``|---|:---:|``.
_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
# Pipes that are not escaped as ``\|``.
_CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")
# Opening line of a fenced code block; group 2 is the info string.
_FENCE_RE = re.compile(r"^\s*(```|~~~)(.*)$")
_MAX_TITLE_CHARS = 120

# A grid found in the answer before titles are resolved: (title or None, columns, rows).
_RawGrid = tuple[str | None, list[str], list[list[CellValue]]]


def parse_response(raw: str) -> QueryResult:
    """Extract markdown tables and JSON record sets from ``raw`` as grids.

    Args:
        raw: The model's answer, usually markdown.

    Returns:
        The remaining prose as ``text`` plus one :class:`GridData` per table.
    """
    stripped = raw.strip()
    if stripped[:1] in ("[", "{"):
        whole = _json_to_grids(_load_json(stripped))
        if whole:
            return QueryResult(
                text="",
                grids=[
                    _make_grid(title or f"Result {n}", columns, rows)
                    for n, (title, columns, rows) in enumerate(whole, start=1)
                ],
            )

    lines = raw.splitlines()
    out: list[str] = []
    grids: list[GridData] = []
    used_title_lines: set[int] = set()

    def add(found: list[_RawGrid]) -> None:
        for title, columns, rows in found:
            if title is None:
                title = _preceding_title(out, used_title_lines)
            grids.append(_make_grid(title or f"Result {len(grids) + 1}", columns, rows))

    i = 0
    while i < len(lines):
        line = lines[i]

        fence = _FENCE_RE.match(line)
        if fence:
            end = _find_fence_end(lines, i, fence.group(1))
            if end is None:
                out.extend(lines[i:])
                break
            info = fence.group(2).strip().lower()
            body = "\n".join(lines[i + 1 : end]).strip()
            if info == "json" or (info == "" and body[:1] in ("[", "{")):
                found = _json_to_grids(_load_json(body))
                if found:
                    add(found)
                    i = end + 1
                    continue
            out.extend(lines[i : end + 1])
            i = end + 1
            continue

        if "|" in line and i + 1 < len(lines) and _SEPARATOR_RE.match(lines[i + 1]):
            header = _split_cells(line)
            if header and len(header) == len(_split_cells(lines[i + 1])):
                j = i + 2
                while j < len(lines) and lines[j].strip() and "|" in lines[j]:
                    j += 1
                width = len(header)
                rows: list[list[CellValue]] = []
                for body_line in lines[i + 2 : j]:
                    cells: list[CellValue] = list(_split_cells(body_line)[:width])
                    rows.append(cells + [""] * (width - len(cells)))
                add([(None, _clean_headers(header), rows)])
                i = j
                continue

        out.append(line)
        i += 1

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    return QueryResult(text=text, grids=grids)


def to_aggrid_options(grid: GridData) -> dict[str, Any]:
    """Build ``ui.aggrid`` options for ``grid``.

    Column fields are synthetic (``c0``, ``c1``, ...) because AG Grid reads dots
    in ``field`` as nested paths; the real name is the ``headerName``.

    Args:
        grid: The table to show.

    Returns:
        An AG Grid options dict.
    """
    return {
        "columnDefs": [
            {
                "headerName": name,
                "field": f"c{i}",
                "sortable": True,
                "filter": True,
                "resizable": True,
                "minWidth": 100,
            }
            for i, name in enumerate(grid.columns)
        ],
        "rowData": [{f"c{i}": value for i, value in enumerate(row)} for row in grid.rows],
        "domLayout": "autoHeight",
        "pagination": True,
        "paginationPageSize": 20,
        "paginationPageSizeSelector": [20, 50, 100],
    }


def _make_grid(title: str, columns: list[str], rows: list[list[CellValue]]) -> GridData:
    """Build a :class:`GridData` with the title trimmed to a sane length."""
    return GridData(title=title[:_MAX_TITLE_CHARS], columns=columns, rows=rows)


def _find_fence_end(lines: list[str], start: int, marker: str) -> int | None:
    """Return the index of the line closing the fence opened at ``start``, if any."""
    for j in range(start + 1, len(lines)):
        closing = lines[j].strip()
        if closing.startswith(marker) and closing.strip("`~") == "":
            return j
    return None


def _split_cells(line: str) -> list[str]:
    """Split a markdown table row into stripped cells, unescaping ``\\|``."""
    stripped = line.strip()
    parts = _CELL_SPLIT_RE.split(stripped)
    if stripped.startswith("|"):
        parts = parts[1:]
    if stripped.endswith("|") and not stripped.endswith("\\|") and parts:
        parts = parts[:-1]
    return [part.strip().replace("\\|", "|") for part in parts]


def _clean_headers(header: list[str]) -> list[str]:
    """Name blank headers ``Column N`` and suffix duplicates with `` (2)``, `` (3)``..."""
    seen: dict[str, int] = {}
    columns: list[str] = []
    for n, name in enumerate(header, start=1):
        name = name or f"Column {n}"
        seen[name] = seen.get(name, 0) + 1
        columns.append(name if seen[name] == 1 else f"{name} ({seen[name]})")
    return columns


def _preceding_title(out: list[str], used: set[int]) -> str | None:
    """Derive a grid title from the last non-blank text line, if it looks like one.

    Each line is used as a title at most once, so back-to-back tables don't
    share a heading.
    """
    for index in range(len(out) - 1, -1, -1):
        line = out[index].strip()
        if not line:
            continue
        if index in used:
            return None
        if line.startswith("#"):
            title = line.lstrip("#")
        elif line.endswith(":"):
            title = line.rstrip(":")
        elif line.startswith("**") and line.endswith("**"):
            title = line
        else:
            return None
        title = title.strip(" *_")
        if not title:
            return None
        used.add(index)
        return title
    return None


_NO_JSON = object()


def _load_json(text: str) -> Any:
    """Parse ``text`` as JSON, or return a sentinel that yields no grids."""
    try:
        return json.loads(text)
    except ValueError:
        return _NO_JSON


def _to_cell(value: Any) -> CellValue:
    """Keep JSON scalars as-is; serialise nested values to a JSON string."""
    if value is None or isinstance(value, str | int | float | bool):
        return value
    return json.dumps(value, ensure_ascii=False)


def _records_to_grid(title: str | None, records: list[dict[str, Any]]) -> _RawGrid | None:
    """Turn a list of JSON objects into one grid; columns are the union of keys."""
    keys: list[str] = []
    for record in records:
        for key in record:
            if key not in keys:
                keys.append(key)
    if not keys:
        return None
    rows = [[_to_cell(record.get(key)) for key in keys] for record in records]
    return (title, [str(key) for key in keys], rows)


def _is_records(value: Any) -> bool:
    """Whether ``value`` is a non-empty list made only of JSON objects."""
    return isinstance(value, list) and bool(value) and all(isinstance(v, dict) for v in value)


def _json_to_grids(value: Any) -> list[_RawGrid]:
    """Find grids in a parsed JSON value.

    A list of objects is one grid. A dict yields one grid per key holding a
    list of objects (titled with the key); a dict of only scalars becomes a
    ``Field``/``Value`` grid. Anything else yields nothing.
    """
    if _is_records(value):
        grid = _records_to_grid(None, value)
        return [grid] if grid else []
    if isinstance(value, dict) and value:
        found = [
            grid
            for key, item in value.items()
            if _is_records(item) and (grid := _records_to_grid(str(key), item))
        ]
        if found:
            return found
        if all(not isinstance(item, dict | list) for item in value.values()):
            return [(None, ["Field", "Value"], [[str(k), _to_cell(v)] for k, v in value.items()])]
    return []
