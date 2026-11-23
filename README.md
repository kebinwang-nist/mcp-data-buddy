# MCP Data Buddy

A set of small [FastMCP](https://gofastmcp.com) servers, a gateway server that combines them, and a chat client that lets an
OpenAI-compatible model answer questions by calling their tools. Ask from the command line (`app.py`) or from a local web
page (`client/`) that shows each table in the answer as a sortable, filterable grid.

## What's in here

```
mcp-data-buddy/
├── servers/
│   ├── __init__.py            # SERVERS registry: namespace -> FastMCP server
│   ├── skills.py              # Optional SKILL.md loader shared by all servers
│   ├── cdc/
│   │   ├── server.py          # CdcServer (data.cdc.gov Socrata API)
│   │   ├── catalog.py         # Parses the dataset index out of the topic skills
│   │   ├── build_skills.py    # Regenerates the topic skills (public datasets only) from the Socrata catalog
│   │   └── skills/
│   │       └── <topic>/SKILL.md  # nchs, ncird, public_health_infrastructure, respiratory_viruses, smoking_tobacco, vaccinations
│   └── fda/
│       ├── server.py          # FdaServer (openFDA api.fda.gov drug and food endpoints)
│       ├── api.py             # Pure openFDA helpers: id scope, retry/empty rules, field hints, projection
│       ├── catalog.py         # Parses the endpoint index and field tables out of the endpoint skills
│       ├── build_skills.py    # Regenerates the endpoint skills from the field definitions and the live API
│       └── skills/
│           └── <endpoint>/SKILL.md  # drug_adverse_events, drug_labeling, drug_ndc, drug_orange_book, drug_recalls, drug_shortages, drugs_fda, food_adverse_events, food_recalls
├── gateway/
│   ├── __init__.py            # load_rules(): builds middleware from gateway_config.json
│   ├── ai_check.py            # Optional PII check by a separate model (GATEWAY_AI_*)
│   ├── answer.py              # AnswerFilter: applies the pii rule to the final answer (on_answer)
│   ├── middleware.py          # PIIMiddleware: block/redact/log PII in tool calls
│   └── pii.py                 # PII detectors (SSN, email, phone, card, IP) and redaction
├── client/                    # NiceGUI web client for app.py (see client/README.md)
│   ├── main.py                # Entry point: uv run python -m client.main
│   ├── ui.py                  # Page layout and submit handler
│   ├── backend.py             # Calls app.run_chat
│   ├── parsing.py             # Splits the answer into text and grids
│   ├── models.py              # GridData, QueryResult
│   ├── config.py              # CLIENT_* settings
│   └── tests/                 # Tests for parsing.py
├── server_config.json         # List of MCP servers: namespace, enabled flag, endpoint URLs
├── gateway_config.json        # Gateway rules applied to every tool call (e.g. PII)
├── server.py                  # Gateway: mounts every enabled server and applies the rules
├── app.py                     # Chat client: gateway tools + OpenAI-compatible model
└── config.py                  # App-level settings (AI_*, OPENFDA_API_KEY) from env/.env
```

### Architecture

Each folder in `servers/` holds one FastMCP server. Its `server.py` defines `mcp` and the tools, and any data files it needs sit next to it. The servers aren't run on their own. `server.py` at the project root is a **gateway**: it uses `FastMCP.mount()` to combine every server marked `enabled` in `server_config.json`, and adds that server's `namespace` to the front of each tool name. That keeps names unique when two servers have tools with the same name. `app.py` connects to the gateway, so it sees every tool from every registered server. The web client in `client/` is a page on top of `app.py`: it calls `app.run_chat` and shows the answer.

```
client/ (web page) ─┐
                    ├─► app.py ──► server.py (Gateway) ── rules (gateway_config.json) ─┬─ cdc ─► servers/cdc/
command line ───────┘                                                                └─ fda ─► servers/fda/
```

### Gateway rules: `gateway_config.json`

The gateway runs every tool call through the rules in [gateway_config.json](gateway_config.json). Each rule is a FastMCP middleware, so it covers the tools of every mounted server. The rules don't apply when you run a server on its own.

The `pii` rule finds personal data in tool **arguments** (what the model sends) and tool **results** (what the backend returns):

```json
{
  "rules": [
    {
      "name": "pii",
      "type": "pii",
      "enabled": true,
      "detectors": ["ssn", "email", "phone", "credit_card", "ip_address"],
      "custom_patterns": {},
      "on_request": "log",
      "on_response": "redact",
      "on_answer": "redact",
      "tools": null,
      "exclude_tools": []
    }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `detectors` | Built-in detectors to use. Leave it out to use all of them. |
| `custom_patterns` | Extra `{"name": "regex"}` detectors, e.g. `{"employee_id": "\\bE\\d{6}\\b"}`. |
| `on_request` / `on_response` | What to do when PII is found: `block` (the call fails with an error the model can read), `redact` (each match becomes `[REDACTED:<KIND>]`), `log` (a warning and nothing else), or `off`. |
| `on_answer` | What to do when PII is in the model's **final answer** in `app.py` and the web client. Default `redact`. `block` replaces the whole answer with a notice naming the PII kinds. `log` and `off` work as above. |
| `tools` / `exclude_tools` | Gateway tool names (e.g. `cdc_get_dataset`) to limit the rule to or skip. `null` means all tools. These don't affect `on_answer`. |

The answer needs its own check because the model can write PII that never went through a tool call. It might copy a value from a tool result before redaction applied, or write one it already knows. A well-known public number, such as an agency's information line, is redacted too, because the regex can't tell personal numbers from organizational ones. Use `"on_answer": "log"` if that's a problem. The answer filter runs in `app.py`, so it doesn't apply when another MCP client, such as Claude Desktop, uses the gateway.

**Skipping the check for one question.** In `app.py` and the web client, a question that starts with `NO PII CHECK` skips the `pii` rule entirely: tool arguments, tool results, the answer and the AI check. The prefix is case-sensitive and must be at the very start. It must be followed by a space, punctuation (`.`, `:`, `-`, `,` …) or nothing, so `NO PII CHECKS` doesn't count. It's removed, along with any spaces and punctuation right after it, before the question goes to the model:

```powershell
uv run python app.py "NO PII CHECK: What is the FDA's information phone number?"
```

The log records each skipped check as a warning. The opt-out works because `server.py` also builds `mcp_unchecked`, a gateway without the rules that only `app.py` uses. `uv run python server.py` always serves the checked gateway, so other MCP clients can't skip the rule. Anyone who can type a question can use the prefix, so don't rely on the rule as a control against the person asking.

The log lists only the kinds and counts of PII found, never the values. Detection uses regular expressions: card numbers must pass the Luhn check, and SSNs and phone numbers must have separators (`123-45-6789`), so plain numeric IDs aren't flagged. Only strings are scanned, so a number in a JSON result isn't redacted. Restart the gateway after you edit the file.

#### AI check with a separate model

Regular expressions can't find names, street addresses or dates of birth. To catch those, turn on `ai_check` in the `pii` rule. The gateway then sends each tool's arguments and results, and the final answer, to a model, which lists the PII it finds. The rule handles those values the same way as regex matches.

```json
"ai_check": {
  "enabled": true,
  "kinds": ["person_name", "street_address", "date_of_birth"],
  "on_error": "block",
  "max_chars": 20000,
  "timeout_seconds": 30
}
```

| Field | Meaning |
| --- | --- |
| `kinds` | The kinds of PII the model looks for. Each becomes a `[REDACTED:<KIND>]` label. |
| `on_error` | What happens if the model call fails or its answer isn't valid JSON. `block` fails the tool call, so nothing goes through unchecked. `regex_only` uses only the regex detectors for that call. |
| `max_chars` | Longer texts are split into chunks of this size and checked in parallel. |
| `timeout_seconds` | Timeout for each model call. |

The check model is set apart from the chat model in `.env`. Any value you leave out uses the matching `AI_*` value:

```dotenv
GATEWAY_AI_API_KEY=your-api-key
GATEWAY_AI_API_BASE=https://api.openai.com/v1
GATEWAY_AI_MODEL=gpt-4o-mini
```

The gateway keeps only values that appear word for word in the text. A value the model makes up or rewords, or a kind not listed in `kinds`, is ignored.

Each checked call adds one model request for the arguments and one for the result, which adds time and cost. Use `tools` / `exclude_tools` to limit which tools are checked. The text goes to the check model, so use an endpoint that is approved for this data.

### MCP tools

| Server | Tool (as exposed by the gateway) | Description |
| --- | --- | --- |
| cdc | `cdc_get_dataset(dataset_id, select=None, where=None, order=None, group=None, having=None, q=None, limit=100, offset=0)` | Queries a CDC open dataset (data.cdc.gov) with SoQL and returns the rows as JSON. Rejects unknown ids, and maps/charts with the dataset to query instead. |
| cdc | `cdc_list_datasets(search=None, category=None)` | Lists the public datasets, maps and charts in the CDC topic skills, optionally filtered (the search also matches tags). |
| cdc | `cdc_describe_dataset(id_or_name)` | One dataset's endpoint, row count, freshness, topics, tags and columns from its skill. |
| fda | `fda_get_dataset(dataset_id, search=None, count=None, sort=None, fields=None, limit=None, skip=0)` | Queries an openFDA drug or food endpoint (e.g. `drug/event`, `food/enforcement`) and returns records, or term counts with `count`, as JSON. `fields` keeps only the given dotted paths. No matches returns an empty result, not an error. Rejects unknown and non-drug/food ids; unknown field names come back as hints. |
| fda | `fda_list_datasets(search=None, category=None)` | Lists the openFDA endpoints in the skills, optionally filtered by words or by category (`drug`, `food`). |
| fda | `fda_describe_dataset(id_or_name, field_search=None)` | One endpoint's URL, record count, freshness, example queries and field table from its skill; `field_search` keeps only matching field rows. |

### Skills

A server can ship a `skills/SKILL.md` (YAML front matter with `name` and `description`, then markdown). Servers load it at startup through `servers/skills.py`. When it exists, the server exposes it as the resource `skill://<namespace>/<name>` and the prompt `<namespace>_skill` (as mounted by the gateway), and uses the description as its instructions when run on its own. Without a SKILL.md, a server behaves as it did before. Edits to a SKILL.md need a server restart.

cdc ships one skill per CDC topic at `skills/<topic>/SKILL.md` (`nchs`, `ncird`, `public_health_infrastructure`, `respiratory_viruses`, `smoking_tobacco`, `vaccinations`), exposed as `skill://cdc/cdc-<...>` and the prompt `cdc_skill-<topic>`. The discovery tools and `get_dataset` validation cover all of them. It lists public datasets only: `href` links, stories and restricted-public assets are skipped and counted in each skill's Overview. Each dataset section records its endpoint, the Topics and Tags from its intro page and the field names of one sample row (no values). Regenerate them with `uv run python -m servers.cdc.build_skills [folder ...]` (needs network access to data.cdc.gov; a full run takes a few minutes).

fda has one skill per openFDA endpoint at `skills/<endpoint>/SKILL.md` (`drug_adverse_events`, `drug_labeling`, `drug_ndc`, `drug_orange_book`, `drug_recalls`, `drug_shortages`, `drugs_fda`, `food_adverse_events`, `food_recalls`), exposed as `skill://fda/fda-<...>` and the prompt `fda_skill-<endpoint>`. Each skill's section lists the field definitions (type, `.exact` flag, description, possible values), the field names of one sample record (no values) and example queries that were run when the skill was built. Regenerate them with `uv run python -m servers.fda.build_skills [folder ...]` (needs network access to api.fda.gov and open.fda.gov; about 45 requests).

cdc and fda read an optional `"load_skills"` flag from their `server_config.json` entry (default `true`). With `"load_skills": false` the server exposes only its data tool, unvalidated, with no skill resources, prompts or instructions; the skill files stay in place.

### Server configuration: `server_config.json`

[server_config.json](server_config.json) at the project root lists every MCP server. It's the one place to change URLs or turn servers on and off:

```json
[
  {
    "name": "cdc",
    "namespace": "cdc",
    "enabled": true,
    "description": "Dataset reads from CDC open data (data.cdc.gov, Socrata SODA API).",
    "endpoints": {
      "base_url": "https://data.cdc.gov"
    }
  },
  {
    "name": "fda",
    "namespace": "fda",
    "enabled": true,
    "description": "Drug and food data from openFDA (api.fda.gov, Elasticsearch-based REST API).",
    "endpoints": {
      "base_url": "https://api.fda.gov"
    }
  }
]
```

| Field | Meaning |
| --- | --- |
| `name` | Folder name under `servers/`. Each server finds its own entry by this name. |
| `namespace` | Prefix the gateway adds to the server's tool names, e.g. `cdc_get_dataset`. |
| `enabled` | Whether the gateway mounts the server. |
| `load_skills` | Optional, default `true`: whether the server loads its `skills/` files (cdc, fda). |
| `endpoints` | The URLs the server calls. |

Current endpoints:

| Server | Endpoint key | URL |
| --- | --- | --- |
| cdc | `base_url` | `https://data.cdc.gov` |
| fda | `base_url` | `https://api.fda.gov` |

Settings that aren't URLs (timeouts, page limits) are constants at the top of each `server.py`.

### Adding a server for another agency

Every server follows the same shape: a folder under `servers/`, an entry in `server_config.json`, and optionally skills that tell the model what data exists. The gateway mounts it automatically and applies the PII rules, so you don't need to change `server.py`, `app.py` or the web client.

Choose a starting point based on how the agency publishes its data:

| The agency publishes… | Start from | Examples |
| --- | --- | --- |
| On a **Socrata** portal (dataset pages at `/d/<4x4-id>`, data at `/resource/<id>.json`) | `servers/cdc/` | `healthdata.gov`, many state and city open-data portals |
| Through its **own REST API** with documented endpoints and fields | `servers/fda/` | Any agency API with a field reference |
| A few endpoints, and you'd rather write the guidance by hand | One hand-written `SKILL.md` ([option C](#c-one-hand-written-skill)) | A small internal or partner API |

Below, `<agency>` is the new folder name, e.g. `hhs`.

#### A. A Socrata portal (copy `cdc`)

1. **Copy the server:**

   ```powershell
   Copy-Item -Recurse servers\cdc servers\<agency>
   Remove-Item -Recurse servers\<agency>\skills\*
   ```

   `catalog.py` works with any Socrata portal (it takes a `label`), so you can delete your copy and import from `servers.cdc.catalog` instead.

2. **Edit `servers/<agency>/build_skills.py`:**
   - Set `_HOST` to the portal's host name, e.g. `"healthdata.gov"`.
   - Replace `_CATEGORIES`. Each key is a skill folder name. Each `Category` holds:
     - `title`: the portal's category name, exactly as on its browse page (the builder uses it to query the Socrata catalog);
     - `skill_name`: e.g. `<agency>-<topic>`;
     - `description`: one paragraph on when to use the topic, which becomes the skill's front matter and the server's instructions;
     - `overview` and `tips`: markdown with known quirks and example `GET` queries.
   - Change the `# CDC open data: …` heading in `_render` and the CDC wording in the module docstring.

3. **Edit `servers/<agency>/server.py`:**
   - `_load_entry("cdc")` → `_load_entry("<agency>")`
   - `_LABEL = "CDC"` → your label
   - `FastMCP("CdcServer", …)` → a new server name
   - the CDC wording in `_instructions`, the tool docstrings and the error messages
   - the `servers.cdc.catalog` import, if you kept your own copy of `catalog.py`

4. **Register the server.** Add an entry to [server_config.json](server_config.json). The namespace becomes the tool prefix, e.g. `hhs_get_dataset`:

   ```json
   {
     "name": "<agency>",
     "namespace": "<agency>",
     "enabled": true,
     "description": "Dataset reads from <Agency> open data (<host>, Socrata SODA API).",
     "endpoints": { "base_url": "https://<host>" }
   }
   ```

5. **Generate the skills** (needs network access to the portal):

   ```powershell
   uv run python -m servers.<agency>.build_skills            # every topic in _CATEGORIES
   uv run python -m servers.<agency>.build_skills <topic>    # just one
   ```

   This writes `servers/<agency>/skills/<topic>/SKILL.md`. Like the CDC builder, it keeps only public assets, and it stores field names but never data values.

#### B. An agency REST API (copy `fda`)

openFDA has its own query syntax, so the `fda` files are more specific than the `cdc` ones. Copy the folder as in option A, then adapt each file:

| File | What to change |
| --- | --- |
| `api.py` | Pure helpers for the API: which endpoint ids are allowed (`_IN_SCOPE`), how to normalize an id, which HTTP statuses to retry, and what "no results" looks like. |
| `build_skills.py` | `_API` and the field-definition URLs. Replace `_ENDPOINTS`: one entry per endpoint with its description, overview, tips and example queries. The builder runs every example and refuses to write a skill if one returns nothing. |
| `catalog.py` | The id pattern in `_INDEX_ROW` and `_SECTION_HEADING` (`(?:drug\|food)/…` for openFDA), so the server can find your endpoints in the skills. |
| `server.py` | `_load_entry("fda")`, the server name, the parameters of `get_dataset` (map them to the API's query parameters), and the FDA wording in the docstrings, instructions and errors. |

If the API needs a key, add an optional setting next to `OPENFDA_API_KEY` in [config.py](config.py) and [.env.example](.env.example). Send the key in a header or Basic auth rather than in the URL, so it never appears in logs. Then register the server and generate the skills as in steps 4–5 of option A.

#### C. One hand-written skill

For a small API, write the guidance yourself. Create `servers/<agency>/server.py`:

```python
import json
from pathlib import Path

import httpx
from fastmcp import FastMCP

from servers.skills import load_skill, register_skill, skill_instructions

_SERVER_DIR = Path(__file__).resolve().parent
_SERVER_CONFIG = _SERVER_DIR.parents[1] / "server_config.json"


def _load_endpoints(name: str) -> dict[str, str]:
    for server in json.loads(_SERVER_CONFIG.read_text(encoding="utf-8")):
        if server["name"] == name:
            return server.get("endpoints", {})
    raise KeyError(f"No '{name}' entry in {_SERVER_CONFIG}")


_ENDPOINTS = _load_endpoints("<agency>")
_SKILL = load_skill(_SERVER_DIR)  # servers/<agency>/skills/SKILL.md, or None

mcp = FastMCP("AgencyServer", instructions=skill_instructions(_SKILL))
register_skill(mcp, _SKILL)  # exposes it as a resource and a "skill" prompt


@mcp.tool()
async def get_records(resource: str, limit: int = 10) -> str:
    """Return up to `limit` records from one <Agency> API resource as JSON."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{_ENDPOINTS['base_url']}/{resource}", params={"limit": limit}
        )
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    mcp.run()
```

Then write `servers/<agency>/skills/SKILL.md`:

```markdown
---
name: <agency>-data
description: Query <Agency> open data (<host>). Use it for <the kinds of questions this data answers>.
---

# <Agency> open data

## Overview
- Base URL, authentication, rate limits, how fresh the data is.

## Endpoints
| Resource | What it holds | Key fields |
|---|---|---|

## Usage tips
- Which resource to use for which question, data quirks, and example queries.
```

The `description` matters most: the model sees it in the server instructions and uses it to decide when to call this server's tools. Register the server as in step 4 of option A.

#### Check the new server

```powershell
uv run python -m servers.<agency>.server     # the server starts on its own
uv run fastmcp list server.py                # its tools appear with the <agency>_ prefix
uv run python app.py "Which <Agency> datasets cover <topic>?"
```

Then update this README: add the server to [What's in here](#whats-in-here), [MCP tools](#mcp-tools), [Skills](#skills) and the endpoint table under [Server configuration](#server-configuration-server_configjson).

Some things to keep in mind:
- Only use public data, and keep data values out of the skill files.
- The gateway's PII rule covers the new tools automatically. If results can contain contact details, as openFDA recall records do, leave `on_response` set to `redact`.
- Settings that aren't URLs, such as timeouts and page limits, go as constants at the top of `server.py`. URLs go in `server_config.json`.
- Set `"load_skills": false` in the server's entry to run without its skills, if your `server.py` reads that flag as `cdc` and `fda` do.

### CDC

The `cdc` server (namespace `cdc`) reads public data from `https://data.cdc.gov` with no API key. Run it on its own with `uv run python -m servers.cdc.server`.

### openFDA

The `fda` server (namespace `fda`) reads the openFDA drug and food endpoints at `https://api.fda.gov`; device, animal and veterinary, tobacco and the other openFDA categories are out of scope and rejected. An API key is optional: set `OPENFDA_API_KEY` in `.env` to raise the daily limit from 1,000 to 120,000 requests. The key is sent as the HTTP Basic-auth username, so it never appears in request URLs or logs. Run the server on its own with `uv run python -m servers.fda.server`. Drug shortage and drug recall records can contain firm phone numbers and emails; the gateway's PII rule redacts them in results.

## Prerequisites

- Python **3.13** or newer (see [.python-version](.python-version))
- [uv](https://docs.astral.sh/uv/) (recommended), or `pip`
- The base URL and an API key for an OpenAI-compatible endpoint. You only need these for `app.py` and the web client.

## Setup

1. **Install dependencies** (this creates `.venv` from `uv.lock`):

   ```powershell
   uv sync
   ```

   Without uv:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -e .
   ```

2. **Configure the environment.** Copy the example file and fill in your values:

   ```powershell
   Copy-Item .env.example .env
   ```

   | Variable | Required | Default | Description |
   | --- | --- | --- | --- |
   | `AI_API_KEY` | yes (for `app.py` and the web client) | — | API key for the OpenAI-compatible endpoint. |
   | `AI_API_BASE` | yes (for `app.py` and the web client) | — | Base URL of the endpoint, e.g. `https://api.openai.com/v1`. |
   | `AI_MODEL` | no | `gpt-4o-mini` | Model ID to request, e.g. `gemma-4-31B-it`. |
   | `GATEWAY_AI_API_KEY` / `GATEWAY_AI_API_BASE` / `GATEWAY_AI_MODEL` | no | the `AI_*` value | The separate model for the gateway's PII check (`ai_check`). |
   | `OPENFDA_API_KEY` | no | — | Optional openFDA API key; raises the daily limit from 1,000 to 120,000 requests. |
   | `CLIENT_HOST` / `CLIENT_PORT` / `CLIENT_TITLE` / `CLIENT_SHOW_BROWSER` | no | `127.0.0.1` / `8080` / `MCP Data Buddy` / `true` | Web client settings. See [client/README.md](client/README.md#settings). |

   Do not commit `.env`.

## How to run

Run these commands from the project root.

### 1. Ask a question through the chat client

```powershell
uv run python app.py "Which CDC datasets track RSV hospitalizations?"
```

With no argument, it asks a default question: *"Which CDC datasets cover adult smoking rates?"*

More examples:

```powershell
uv run python app.py "List the CDC vaccination coverage datasets for adults"
uv run python app.py "What does the CDC dataset aetd-68ew contain?"
```

The log shows each tool the model calls (`-> Calling tool ...`), then prints the final answer after `AI:`.

### 2. Use the web client

```powershell
uv run python -m client.main
```

Then open <http://127.0.0.1:8080> (a browser tab opens automatically by default). Type a question and press **Ask** or Enter. The answer appears as text, followed by one sortable, filterable grid for each table in it.

Run it as a module from the project root, as shown. `python client/main.py` doesn't work, because the client imports the root-level `app` and `config` modules.

> The web client has no authentication, and every question uses your API key. Keep it on `127.0.0.1`.

For settings, how answers are split into grids, and the module layout, see [client/README.md](client/README.md).

### 3. Run the gateway for other MCP clients

You can also expose the tools to any MCP client, such as Claude Desktop, Claude Code, or VS Code. The gateway uses the **stdio** transport:

```powershell
uv run python server.py
```

To try the tools interactively in the MCP Inspector, or list them from the command line:

```powershell
uv run fastmcp dev inspector server.py
uv run fastmcp list server.py
```

To register the gateway with an MCP client:

```json
{
  "mcpServers": {
    "mcp-data-buddy": {
      "command": "uv",
      "args": ["run", "--directory", "PATH\\mcp-data-buddy", "python", "server.py"]
    }
  }
}
```

## Tests

```powershell
uv run --with pytest==8.4.2 python -m pytest -q
```

