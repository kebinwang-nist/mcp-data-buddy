"""Gateway MCP server that mounts the servers registered in :mod:`servers`.

Each server's tools are exposed under its namespace, e.g.
``cdc_get_dataset``.

Every tool call also passes through the rules in ``gateway_config.json``
(see :mod:`gateway`), e.g. PII detection and redaction.

Run with: ``python server.py`` (stdio). Individual servers can also run on
their own, e.g. ``python -m servers.cdc.server``; the gateway rules don't
apply then.
"""

from fastmcp import FastMCP

from gateway import load_rules
from servers import SERVERS

mcp = FastMCP("Gateway")

for namespace, server in SERVERS.items():
    mcp.mount(server, namespace=namespace)

for rule in load_rules():
    mcp.add_middleware(rule)

if __name__ == "__main__":
    mcp.run()
