"""Entry point for the NiceGUI web client.

Run from the project root with: ``uv run python -m client.main``. Running it as
a module puts the project root on ``sys.path``, which :mod:`app` needs for its
top-level ``config``/``server`` imports.
"""

from __future__ import annotations

from nicegui import ui

from client.config import get_client_settings
from client.ui import build_page


def main() -> None:
    """Start the web server with the configured host, port and title."""
    settings = get_client_settings()
    ui.run(
        root=build_page,
        host=settings.host,
        port=settings.port,
        title=settings.title,
        show=settings.show_browser,
        # Reloading re-imports the heavy backend (MCP gateway, skills) on every change.
        reload=False,
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
