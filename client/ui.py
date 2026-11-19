"""NiceGUI page: a question box, a text answer and one grid per table."""

from __future__ import annotations

from nicegui import ui

from client import backend
from client.backend import BackendError
from client.config import get_client_settings
from client.models import QueryResult
from client.parsing import parse_response, to_aggrid_options


def render_result(container: ui.element, result: QueryResult) -> None:
    """Replace ``container``'s content with the answer text and its grids.

    Args:
        container: The element to render into; it is cleared first.
        result: The parsed answer.
    """
    container.clear()
    with container:
        if result.text:
            ui.markdown(result.text)
        elif result.grids:
            ui.label("No text answer; see the tables below.")
        else:
            ui.label("The model returned an empty answer.")
        for grid in result.grids:
            ui.label(grid.title).classes("text-lg font-semibold")
            ui.aggrid(to_aggrid_options(grid), theme="quartz").classes("w-full").style(
                "height: auto"
            )


async def build_page() -> None:
    """Build the single page of the client (passed to ``ui.run(root=...)``)."""
    settings = get_client_settings()

    async def submit() -> None:
        prompt = (prompt_input.value or "").strip()
        if not prompt:
            ui.notify("Please enter a question.", type="warning")
            return
        if not ask_button.enabled:
            return  # A query is already running.

        prompt_input.disable()
        ask_button.disable()
        loading_row.set_visibility(True)
        results.clear()
        try:
            raw = await backend.ask(prompt)
        except BackendError as exc:
            ui.notify(f"Query failed: {exc}", type="negative", multi_line=True, close_button=True)
            return
        finally:
            prompt_input.enable()
            ask_button.enable()
            loading_row.set_visibility(False)
        render_result(results, parse_response(raw))

    with ui.column().classes("w-full max-w-5xl mx-auto p-4 gap-4"):
        ui.label(settings.title).classes("text-2xl font-bold")

        with ui.row().classes("w-full items-center no-wrap"):
            prompt_input = (
                ui.input(
                    label="Your question",
                    placeholder="e.g. Which CDC datasets cover adult smoking rates?",
                )
                .classes("flex-grow")
                .props('clearable aria-label="Your question"')
            )
            ask_button = ui.button("Ask", on_click=submit)
        prompt_input.on("keydown.enter", submit)

        with ui.row().classes("items-center gap-2") as loading_row:
            ui.spinner(size="lg").props('aria-label="Loading"')
            ui.label("Working on your question...")
        loading_row.set_visibility(False)

        results = ui.column().classes("w-full gap-4").props('aria-live="polite"')
