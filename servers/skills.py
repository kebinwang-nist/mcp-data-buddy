"""Load an optional SKILL.md for an MCP server and expose it to MCP clients.

A server package may ship a skill file at ``skills/SKILL.md`` (or ``skill/SKILL.md``, or
``skills/<name>/SKILL.md``). :func:`load_skill` finds and parses it into a :class:`Skill`;
:func:`load_nested_skills` parses every ``skills/<name>/SKILL.md`` for servers that ship
several; :func:`register_skill` publishes a skill as an MCP resource and prompt. A missing or unreadable
skill yields ``None`` and the server behaves as if skills did not exist.

Side effects: :func:`load_skill` reads the skill file; :func:`register_skill` mutates the
given FastMCP server. Problems are logged via :mod:`logging`, never printed.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

SKILL_FILENAME = "SKILL.md"

_FRONT_MATTER = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
_URI_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")


@dataclass(frozen=True, slots=True)
class Skill:
    """A parsed SKILL.md: front-matter fields plus the markdown body."""

    name: str
    description: str
    body: str
    text: str
    path: Path
    metadata: Mapping[str, object] = field(default_factory=dict, hash=False)

    @property
    def resource_uri(self) -> str:
        """Return the MCP resource URI for this skill, e.g. ``skill://cdc-vaccinations``."""
        slug = _URI_UNSAFE.sub("-", self.name).strip("-") or "skill"
        return f"skill://{slug}"


def find_skill_file(server_dir: Path) -> Path | None:
    """Return the first SKILL.md under ``server_dir``, or ``None`` if there is none.

    Checks ``skills/SKILL.md``, then ``skill/SKILL.md``, then ``skills/*/SKILL.md`` (sorted).
    """
    for candidate in (
        server_dir / "skills" / SKILL_FILENAME,
        server_dir / "skill" / SKILL_FILENAME,
    ):
        if candidate.is_file():
            return candidate
    nested = sorted(p for p in server_dir.glob(f"skills/*/{SKILL_FILENAME}") if p.is_file())
    return nested[0] if nested else None


def _field(metadata: Mapping[str, object], key: str, default: str) -> str:
    """Return ``metadata[key]`` as a stripped string, or ``default`` if missing or empty."""
    value = metadata.get(key)
    text = "" if value is None else str(value).strip()
    return text or default


def parse_skill(text: str, path: Path, default_name: str) -> Skill:
    """Parse SKILL.md ``text`` into a :class:`Skill` (pure, no I/O).

    Args:
        text: Full file contents.
        path: Path the text came from (stored on the result, used in log messages).
        default_name: Name to use when the front matter has no ``name``.

    Returns:
        The parsed skill. Missing or malformed front matter logs a warning and the body is
        still served.
    """
    text = text.removeprefix("\ufeff")
    match = _FRONT_MATTER.match(text)
    if match is None:
        logger.warning("Skill %s has no YAML front matter; serving it without metadata", path)
        return Skill(name=default_name, description="", body=text, text=text, path=path)

    body = text[match.end() :]
    metadata: Mapping[str, object] = {}
    try:
        loaded = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        logger.warning("Skill %s has malformed front matter (%s); ignoring it", path, exc)
    else:
        if isinstance(loaded, Mapping):
            metadata = {str(key): value for key, value in loaded.items()}
        else:
            logger.warning("Skill %s front matter is not a mapping; ignoring it", path)

    return Skill(
        name=_field(metadata, "name", default_name),
        description=_field(metadata, "description", ""),
        body=body,
        text=text,
        path=path,
        metadata=metadata,
    )


def load_skill(server_dir: Path) -> Skill | None:
    """Find and parse the SKILL.md of the server package at ``server_dir``.

    Returns:
        The skill, or ``None`` if no skill file exists or it cannot be read. Never raises
        for skill problems.
    """
    path = find_skill_file(server_dir)
    if path is None:
        logger.debug("No %s under %s", SKILL_FILENAME, server_dir)
        return None
    return _read_skill(path, default_name=server_dir.name)


def load_nested_skills(server_dir: Path) -> list[Skill]:
    """Parse every ``skills/<name>/SKILL.md`` under ``server_dir``, sorted by ``<name>``.

    Unreadable files are logged and skipped. Never raises for skill problems.
    """
    skills: list[Skill] = []
    for path in sorted(server_dir.glob(f"skills/*/{SKILL_FILENAME}")):
        skill = _read_skill(path, default_name=path.parent.name) if path.is_file() else None
        if skill is not None:
            skills.append(skill)
    return skills


def _read_skill(path: Path, default_name: str) -> Skill | None:
    """Read and parse the skill at ``path``; ``None`` (logged) if it cannot be read."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        logger.warning("Could not read skill %s (%s); continuing without it", path, exc)
        return None
    skill = parse_skill(text, path.resolve(), default_name=default_name)
    logger.info("Loaded skill %s from %s", skill.name, skill.path)
    return skill


def skill_instructions(skill: Skill | None, extra: str | None = None) -> str | None:
    """Build FastMCP server instructions from ``skill``, or ``None`` without a skill.

    Args:
        skill: The loaded skill, if any.
        extra: Optional server-specific guidance appended after the description.
    """
    if skill is None:
        return None
    parts = [skill.description] if skill.description else []
    if extra:
        parts.append(extra)
    parts.append(f"Full reference: MCP resource {skill.resource_uri}.")
    return "\n\n".join(parts)


def register_skill(mcp: FastMCP, skill: Skill | None, prompt_name: str = "skill") -> None:
    """Expose ``skill`` on ``mcp`` as a markdown resource and a prompt named ``prompt_name``.

    No-op when ``skill`` is ``None``. Pass a distinct ``prompt_name`` for each skill when a
    server registers several.
    """
    if skill is None:
        return

    def read_skill() -> str:
        return skill.text

    def skill_prompt() -> str:
        return skill.body

    mcp.resource(
        skill.resource_uri,
        name=skill.name,
        description=skill.description or None,
        mime_type="text/markdown",
    )(read_skill)
    mcp.prompt(
        name=prompt_name,
        description=f"Load the {skill.name} skill: {skill.description}".rstrip(": "),
    )(skill_prompt)
