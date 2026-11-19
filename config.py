"""Application configuration.

Loads and validates settings from the environment (and a local ``.env`` file)
at import time using pydantic-settings, failing fast on missing required values.

Side effects: reads environment variables and, if present, ``.env``.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    """OpenAI-compatible chat model configuration.

    Attributes:
        ai_api_key: API key for the OpenAI-compatible endpoint.
        ai_api_base: Base URL of the OpenAI-compatible API.
        ai_model: Model identifier to request from the endpoint.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ai_api_key: str
    ai_api_base: str
    ai_model: str = "gpt-4o-mini"


class GatewayAISettings(BaseSettings):
    """Model the gateway's ``pii`` rule asks to find PII the regexes miss.

    Each unset field falls back to the matching ``AI_*`` value, so the gateway
    uses the chat model unless you pick another one.

    Attributes:
        gateway_ai_api_key: API key for the OpenAI-compatible endpoint.
        gateway_ai_api_base: Base URL of the OpenAI-compatible API.
        gateway_ai_model: Model identifier to request from the endpoint.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gateway_ai_api_key: str | None = None
    gateway_ai_api_base: str | None = None
    gateway_ai_model: str | None = None


class OpenFDASettings(BaseSettings):
    """Optional openFDA API key used by ``servers/fda``.

    Without a key openFDA allows 1,000 requests per day per IP; with one, 120,000 per
    day. The key is sent as the HTTP Basic-auth username, never in the URL.

    Attributes:
        openfda_api_key: The openFDA API key, or ``None`` (a blank value counts as unset).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openfda_api_key: SecretStr | None = None


@lru_cache(maxsize=1)
def get_ai_settings() -> AISettings:
    """Return the validated AI settings, loaded once and cached.

    Returns:
        The populated :class:`AISettings`.

    Raises:
        pydantic.ValidationError: If any required value is missing or invalid.
    """
    return AISettings()


@lru_cache(maxsize=1)
def get_openfda_settings() -> OpenFDASettings:
    """Return the openFDA settings, loaded once and cached.

    Returns:
        The populated :class:`OpenFDASettings`; ``openfda_api_key`` may be ``None``.
    """
    return OpenFDASettings()


@lru_cache(maxsize=1)
def get_gateway_ai_settings() -> GatewayAISettings:
    """Return the gateway model settings with every field filled in.

    Returns:
        :class:`GatewayAISettings` with unset values taken from :class:`AISettings`.

    Raises:
        pydantic.ValidationError: If a value is unset in both places.
    """
    settings = GatewayAISettings()
    if (
        settings.gateway_ai_api_key
        and settings.gateway_ai_api_base
        and settings.gateway_ai_model
    ):
        return settings
    ai = get_ai_settings()
    return settings.model_copy(
        update={
            "gateway_ai_api_key": settings.gateway_ai_api_key or ai.ai_api_key,
            "gateway_ai_api_base": settings.gateway_ai_api_base or ai.ai_api_base,
            "gateway_ai_model": settings.gateway_ai_model or ai.ai_model,
        }
    )
