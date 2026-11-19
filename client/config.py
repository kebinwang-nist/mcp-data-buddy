"""Web client configuration.

Loads and validates the NiceGUI client settings from the environment (and a
local ``.env`` file) using pydantic-settings. All keys use the ``CLIENT_``
prefix, e.g. ``CLIENT_PORT``.

Side effects: reads environment variables and, if present, ``.env``.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ClientSettings(BaseSettings):
    """NiceGUI web client configuration.

    Attributes:
        host: Interface the web server binds to.
        port: TCP port the web server listens on.
        title: Page title and heading text.
        show_browser: Whether to open a browser tab on startup.
    """

    model_config = SettingsConfigDict(
        env_prefix="CLIENT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "127.0.0.1"
    port: int = Field(default=8080, ge=1, le=65535)
    title: str = "MCP Data Buddy"
    show_browser: bool = True


@lru_cache(maxsize=1)
def get_client_settings() -> ClientSettings:
    """Return the validated client settings, loaded once and cached.

    Returns:
        The populated :class:`ClientSettings`.

    Raises:
        pydantic.ValidationError: If any value is invalid.
    """
    return ClientSettings()
