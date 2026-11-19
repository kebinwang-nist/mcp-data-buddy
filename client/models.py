"""Typed data contracts passed between the client's layers.

The parsing layer turns the backend's raw answer into a :class:`QueryResult`;
the UI layer renders it. No I/O happens here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

# A single grid cell. Markdown tables yield strings; JSON keeps scalar types.
CellValue = str | int | float | bool | None


class GridData(BaseModel):
    """One tabular result set to show as a grid.

    Attributes:
        title: Heading shown above the grid.
        columns: Column header names, in display order.
        rows: Row values; each row has exactly ``len(columns)`` cells.
    """

    model_config = ConfigDict(frozen=True)

    title: str
    columns: list[str] = Field(min_length=1)
    rows: list[list[CellValue]]

    @model_validator(mode="after")
    def _check_row_lengths(self) -> GridData:
        """Reject rows whose cell count differs from the column count."""
        width = len(self.columns)
        for index, row in enumerate(self.rows):
            if len(row) != width:
                raise ValueError(f"row {index} has {len(row)} cells, expected {width}")
        return self


class QueryResult(BaseModel):
    """A parsed backend answer: prose text plus zero or more grids.

    Attributes:
        text: Markdown prose left after removing tabular blocks.
        grids: Tabular result sets, in the order they appeared.
    """

    model_config = ConfigDict(frozen=True)

    text: str
    grids: list[GridData] = Field(default_factory=list)
