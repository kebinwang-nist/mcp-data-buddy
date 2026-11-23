# MCP Data Buddy: 5-minute video narrative

GSA MCP Server and SI Agent Government Hackathon, **Dataset Access Server** track.

This is the narration for the 7-slide video deck in [deck.html](deck.html). The 19-slide submission deck, which follows GSA's sample deliverable deck, is [mcp-data-buddy-deliverable.pptx](mcp-data-buddy-deliverable.pptx). Each segment below matches one slide. The narration is 369 words, which takes about 2.5 minutes at a normal speaking pace. That leaves roughly half of each segment for the visuals to play without narration, so speak slowly and pause on each slide. To record, open the deck in a browser, press **Present**, and move to the next slide at each segment's start time. Turn on **Narration** in the deck's toolbar to read the script under each slide.

## Timeline

| Time | Segment | Slide shows |
| --- | --- | --- |
| 0:00–0:30 | Hook | A plain question next to the portals and query syntax it takes today |
| 0:30–1:15 | The problem | A CDC dataset page, a raw CDC row and a raw openFDA record |
| 1:15–2:00 | What it is | MCP in one line, then AI client → gateway → CDC and FDA servers → official data |
| 2:00–3:00 | What it can do | Split screen: 6 CDC topics and 9 FDA endpoints, with example questions |
| 3:00–3:50 | Built-in privacy protection | A tool result before and after the gateway, with detectors and actions |
| 3:50–4:30 | Demo | One query with masked PII data and two complicated queries, in a chat window |
| 4:30–5:00 | Wrap-up | Three recap points, then how to try it |

## Segments

### 0:00–0:30 · Hook

**Visual:** A search box with "Has lidocaine been recalled?", next to three portal cards: an openFDA query URL in Elasticsearch syntax, a data.cdc.gov SoQL URL, and the openFDA field reference (535 fields across 9 endpoints). The left side shows the project name and a one-line promise.

**Narration:** "What if you could ask an AI, in plain English, whether a drug has been recalled, or which CDC datasets track RSV? And what if it answered using real, official data, without exposing anyone's personal information? That's what mcp-data-buddy does."

### 0:30–1:15 · The problem

**Visual:** The data.cdc.gov page for `vjzj-u7u8` (NSSP Emergency Department Respiratory Daily, 311,584 rows), a real raw CDC row whose address is JSON packed inside a string, and a real openFDA adverse-event record with fields like `reactionmeddrapt`. Four labels underneath: many portals, own query syntax, cryptic fields, needs skill.

**Narration:** "The CDC and FDA publish a huge amount of open data. But it's spread across many portals. Each has its own query syntax, and the field names are cryptic. Even simple questions take time and technical skill. AI assistants could help, but they need a safe, reliable way to reach this data."

### 1:15–2:00 · What it is

**Visual:** A one-line definition of MCP, then the architecture: Claude Desktop, VS Code or the project chat client → the gateway (6 tools, every call checked for personal data) → the CDC and FDA servers (list, describe and get datasets) → data.cdc.gov and api.fda.gov.

**Narration:** "mcp-data-buddy is a set of small servers built on the Model Context Protocol, or MCP. MCP is a standard way for AI assistants to use outside tools. Here, one server handles CDC data and another handles FDA data. A gateway sits in front and combines them. It connects to tools like Claude Desktop or VS Code, or to the project's own chat client."

### 2:00–3:00 · What it can do

**Visual:** CDC on the left: 305 assets in the six topics this project covers, from the National Center for Health Statistics (207) to public health infrastructure (2). FDA on the right: nine endpoints with record counts, from 21,054,159 drug adverse events to 1,585 drug shortage records. Example questions on both sides, and a note on the optional openFDA key.

**Narration:** "On the CDC side, the assistant can discover datasets by topic, such as vaccination coverage or smoking rates, and then query them. On the FDA side, it can look up drug adverse events, labeling, the NDC directory, the Orange Book, recalls and shortages. It also covers food recalls and food adverse events. Both sources are free, and an API key is only needed for higher FDA rate limits."

### 3:00–3:50 · Built-in privacy protection

**Visual:** A drug shortage record before the gateway, with a phone number and email highlighted, and after it, with both replaced by `[REDACTED:PHONE]` and `[REDACTED:EMAIL]`. The values are made up for the illustration. Underneath: the five detectors, the block/redact/log actions and the optional AI check. A footnote gives a real figure: in a recorded run, one result had 86 phone numbers and 1 email redacted.

**Narration:** "Health data raises privacy concerns, so the gateway scans every request and response. It looks for Social Security numbers, emails, phone numbers, credit cards and IP addresses. It can block, redact or log what it finds. An optional second AI check also catches names, street addresses and birth dates. Privacy is part of the design, not an afterthought."

### 3:50–4:30 · Demo

**Visual:** A line stating that the demo shows one query with masked PII data and two complicated queries, then a chat window with the three recorded questions, the tool calls behind each, and a shortened answer.

- **Masked PII:** "What is the FDA contact info for food recall?" took 1 tool call and 8 seconds. The model noted that the recall data has no FDA contacts and wrote four phone numbers from its own knowledge. The answer filter masked all four as `[REDACTED:PHONE]`. These are FDA's public hotlines, not personal data: a regex can't tell a personal line from an agency's, so the default masks both, and `"on_answer": "log"` keeps them.
- **Complicated query:** "Are there any current shortages for lidocaine?" took 5 tool calls and 18 seconds. The answer: yes, 87 entries, all marked "Current", from 10 manufacturers, led by Fresenius Kabi (32) and Hospira/Pfizer (26), with supply reasons and recovery dates.
- **Complicated query across both agencies:** "Is nirsevimab (Beyfortus) in shortage according to FDA, and which CDC datasets track RSV immunization of infants?" took 5 tool calls (3 FDA, 2 CDC) and 12 seconds. The answer: no shortage entry, plus three CDC infant immunization datasets, with which one is current.

**Narration:** "Let's see it in action. The demo shows one query with masked personal data and two complicated queries. First I ask, 'What is the FDA contact info for food recall?' The phone numbers in the answer come back masked. Next I ask, 'Are there any current shortages for lidocaine?' The assistant picks the FDA shortages endpoint, runs several queries and summarizes 87 listings. Finally, one question spans both agencies: is nirsevimab in shortage, and which CDC datasets track RSV immunization of infants? It checks FDA and CDC and answers both parts."

### 4:30–5:00 · Wrap-up

**Visual:** Three recap points (trusted data through conversation, privacy built in, easy to extend), then the commands to try it.

**Narration:** "To recap: trusted public health data through conversation, privacy protection built in, and a design that makes adding new data sources easy. Check out the project on GitHub, and try it with your own questions. Thanks for watching."

## Recording a live demo instead

The demo slide shows runs recorded on 23 November 2026 with Claude Sonnet 5.5 through an OpenAI-compatible endpoint. To record the chat live, start the web client from the project root and ask the same three questions:

```powershell
uv run python -m client.main     # opens http://127.0.0.1:8080
```

Model behavior varies between runs, so a live run may make different tool calls and word the answer differently. Each question takes about 15–20 seconds, so trim the wait in editing.

## Likely questions

**Why does each server have only three tools?** The tools follow what a user wants to do: find a dataset, understand it, and read it. Skill files built from each agency's live catalog let the server reject a wrong dataset id or field name before any API call and suggest the right one.

**Can the model see personal data?** Tool results are redacted before they reach the model, and the final answer is checked again. The optional AI check fails closed by default: if it can't run, the call is blocked.

**Why would company phone numbers be redacted?** A regular expression can't tell a personal phone number from an organizational one, so the default redacts both. Setting `"on_answer": "log"` in `gateway_config.json` keeps them in the answer and still logs the finding.

**How hard is it to add another agency?** Copy `servers/cdc` for a Socrata portal or `servers/fda` for a REST API, add an entry to `server_config.json`, and generate the skills. The gateway, chat loop and web client don't change.

**How was it tested?** 57 automated tests pass. For openFDA, every usage tip in the skills was checked against the live API, 28 example queries ran while the skills were built, and openFDA retry behavior was tested with a stubbed transport: a persistent 503 makes four attempts, waiting 1, 2 and 4 seconds. The CDC server doesn't retry yet. A 15-question evaluation against the live APIs, run 3 times, passed 45 of 45 trials with the tools; the same model without tools passed 10 of 45, and a second judge model agreed with every verdict. See [docs/evaluation-report.md](../evaluation-report.md).
