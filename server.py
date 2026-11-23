"""Gateway MCP server that mounts the servers registered in :mod:`servers`.

Each server's tools are exposed under its namespace, e.g.
``cdc_get_dataset``.

Every tool call also passes through the rules in ``gateway_config.json``
(see :mod:`gateway`), e.g. PII detection and redaction.

Run with: ``python server.py`` (stdio). Individual servers can also run on
their own, e.g. ``python -m servers.cdc.server``; the gateway rules don't
apply then.

``mcp_unchecked`` mounts the same servers without the rules. Only ``app.py``
uses it, for questions that start with ``NO PII CHECK``; running this file
always serves ``mcp``, with the rules.
"""

from fastmcp import FastMCP

from gateway import load_rules
from servers import SERVERS


def create_gateway(*, apply_rules: bool = True) -> FastMCP:
    """Mount every enabled server, adding the ``gateway_config.json`` rules if ``apply_rules``."""
    gateway = FastMCP("Gateway")
    for namespace, server in SERVERS.items():
        gateway.mount(server, namespace=namespace)
    if apply_rules:
        for rule in load_rules():
            gateway.add_middleware(rule)
    return gateway


mcp = create_gateway()
mcp_unchecked = create_gateway(apply_rules=False)

if __name__ == "__main__":
    mcp.run()
