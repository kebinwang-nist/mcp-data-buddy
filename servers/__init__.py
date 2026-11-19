"""Registry of the MCP servers in this project.

Each subfolder of this package is one standalone FastMCP server: its
``server.py`` defines ``mcp`` and its tools, and reads its endpoints from its
entry in the project-root ``server_config.json``. That file lists every server;
:data:`SERVERS` holds the enabled ones, which the gateway (``server.py`` at the
project root) mounts. Each entry's ``namespace`` becomes the prefix on that
server's tool names, e.g. ``cdc_get_dataset``.

To add a server: copy one of the subfolders to ``servers/<name>/``, edit its
``server.py``, then add an entry to ``server_config.json``. Optionally add
``servers/<name>/skills/SKILL.md``; servers that call :func:`servers.skills.load_skill`
expose it as an MCP resource, a ``skill`` prompt and the server instructions.
"""

import importlib
import json
from pathlib import Path

from fastmcp import FastMCP

_SERVER_CONFIG = Path(__file__).resolve().parent.parent / "server_config.json"


def _load_servers() -> dict[str, FastMCP]:
    """Import every enabled server in ``server_config.json``, keyed by namespace."""
    servers: dict[str, FastMCP] = {}
    for entry in json.loads(_SERVER_CONFIG.read_text(encoding="utf-8")):
        if not entry.get("enabled", True):
            continue
        module = importlib.import_module(f"servers.{entry['name']}.server")
        servers[entry.get("namespace", entry["name"])] = module.mcp
    return servers


SERVERS: dict[str, FastMCP] = _load_servers()
