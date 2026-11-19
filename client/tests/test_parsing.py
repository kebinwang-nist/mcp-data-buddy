"""Unit tests for :mod:`client.parsing`."""

from __future__ import annotations

import pytest

from client.models import GridData
from client.parsing import parse_response, to_aggrid_options


def test_plain_prose_has_no_grids() -> None:
    result = parse_response("  Hello there.\n\nNo tables here.  ")
    assert result.grids == []
    assert result.text == "Hello there.\n\nNo tables here."


def test_markdown_table_under_heading() -> None:
    raw = "Intro text.\n\n## Pay plans\n| Code | Name |\n|---|---|\n| GS | General |\n| ZP | Pay |\n\nOutro."
    result = parse_response(raw)
    assert len(result.grids) == 1
    grid = result.grids[0]
    assert grid.title == "Pay plans"
    assert grid.columns == ["Code", "Name"]
    assert grid.rows == [["GS", "General"], ["ZP", "Pay"]]
    assert "|" not in result.text
    assert "Intro text." in result.text and "Outro." in result.text
    assert "## Pay plans" in result.text


def test_two_tables_titles_and_order() -> None:
    raw = "| a |\n|---|\n| 1 |\n\nTables:\n| b |\n|---|\n| 2 |"
    result = parse_response(raw)
    assert [g.title for g in result.grids] == ["Result 1", "Tables"]
    assert [g.columns for g in result.grids] == [["a"], ["b"]]


def test_back_to_back_tables_do_not_share_heading() -> None:
    raw = "## Heading\n| a |\n|---|\n| 1 |\n\n| b |\n|---|\n| 2 |"
    result = parse_response(raw)
    assert [g.title for g in result.grids] == ["Heading", "Result 2"]


def test_json_fence_records() -> None:
    raw = 'Here:\n```json\n[{"a": 1, "b": {"x": 1}}, {"a": 2, "c": true}]\n```\nDone.'
    result = parse_response(raw)
    assert len(result.grids) == 1
    grid = result.grids[0]
    assert grid.title == "Here"
    assert grid.columns == ["a", "b", "c"]
    assert grid.rows == [[1, '{"x": 1}', None], [2, None, True]]
    assert "```" not in result.text


def test_whole_response_json_list() -> None:
    result = parse_response('[{"id": 1}, {"id": 2}]')
    assert result.text == ""
    assert result.grids[0].rows == [[1], [2]]
    assert result.grids[0].title == "Result 1"


def test_dict_with_records_titled_by_key() -> None:
    result = parse_response('{"people": [{"name": "A"}], "count": 1}')
    assert [g.title for g in result.grids] == ["people"]


def test_flat_scalar_dict_is_field_value_grid() -> None:
    result = parse_response('{"name": "A", "age": 3}')
    assert result.grids[0].columns == ["Field", "Value"]
    assert result.grids[0].rows == [["name", "A"], ["age", 3]]


def test_invalid_json_fence_left_in_text() -> None:
    raw = "```json\n{not json\n```"
    result = parse_response(raw)
    assert result.grids == []
    assert result.text == raw


def test_table_inside_text_fence_not_parsed() -> None:
    raw = "```text\n| a |\n|---|\n| 1 |\n```"
    result = parse_response(raw)
    assert result.grids == []
    assert result.text == raw


def test_ragged_rows_and_escaped_pipes() -> None:
    raw = "| a | b |\n|---|---|\n| 1 |\n| x \\| y | 2 | extra |"
    grid = parse_response(raw).grids[0]
    assert grid.rows == [["1", ""], ["x | y", "2"]]


def test_blank_and_duplicate_headers() -> None:
    raw = "| a |  | a |\n|---|---|---|\n| 1 | 2 | 3 |"
    assert parse_response(raw).grids[0].columns == ["a", "Column 2", "a (2)"]


def test_aggrid_options_use_synthetic_fields() -> None:
    options = to_aggrid_options(GridData(title="t", columns=["a.b"], rows=[["v"]]))
    assert options["columnDefs"][0]["field"] == "c0"
    assert options["columnDefs"][0]["headerName"] == "a.b"
    assert options["rowData"] == [{"c0": "v"}]


@pytest.mark.parametrize(
    "raw", ["", "|", "```", "| a |\n|---|", "{", "[1, 2]", "[]", "{}", "~~~\n|", "[{}]"]
)
def test_never_raises(raw: str) -> None:
    parse_response(raw)
