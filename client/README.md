# MCP Data Buddy web client

A [NiceGUI](https://nicegui.io) web page for the chat backend. Type a question, press **Ask** (or Enter), and the
answer appears as text, followed by one sortable, filterable grid for each table in the answer.

## Prerequisites

- `uv sync` has been run at the project root.
- `.env` has the `AI_*` settings described in the [root README](../README.md).
- Network access to the CDC open data API at the `base_url` in [server_config.json](../server_config.json) (`https://data.cdc.gov`).

## Run

From the **project root**:

```powershell
uv run python -m client.main
```

Then open <http://127.0.0.1:8080> (a browser tab opens automatically by default).

Run it as a module. `python client/main.py` fails, because `app.py` imports the root-level modules `config` and
`server`, and those only resolve when the project root is on `sys.path`.

## Settings

All optional. Set them in `.env` or as environment variables.

| Variable | Default | Description |
| --- | --- | --- |
| `CLIENT_HOST` | `127.0.0.1` | Interface to bind to. |
| `CLIENT_PORT` | `8080` | Port to listen on. |
| `CLIENT_TITLE` | `MCP Data Buddy` | Page title and heading. |
| `CLIENT_SHOW_BROWSER` | `true` | Open a browser tab on startup. |

> The client has no authentication, and every question spends your API key. Keep it on `127.0.0.1`.

## How the output is built

1. `backend.ask` appends a formatting hint to the question, asking the model to put each result set in its own
   markdown table. It then awaits `app.run_chat`.
2. `parsing.parse_response` splits the answer:
   - Markdown tables, ```` ```json ```` record lists, and a whole-JSON answer each become a grid.
   - Each grid is titled from the heading or `Label:` line just above it, or `Result N` if there is none.
   - Everything else stays as text.
3. `ui.render_result` shows the text as markdown and each grid as an AG Grid (`ui.aggrid`), with 20 rows per page.

## Modules

| Module | Role |
| --- | --- |
| `config.py` | `ClientSettings` (`CLIENT_*`) |
| `models.py` | `GridData`, `QueryResult` data contracts |
| `parsing.py` | Pure: answer text -> text + grids; grid -> AG Grid options |
| `backend.py` | The only module that imports `app`; wraps errors in `BackendError` |
| `ui.py` | The page layout and submit handler |
| `main.py` | Entry point: `ui.run(...)` |

## Tests

```powershell
uv run --with pytest==8.4.2 python -m pytest client/tests -q
```
