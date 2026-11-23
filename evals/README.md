# Evaluation

An end-to-end check of the chat client against the live CDC and openFDA APIs. Each question goes through `app.run_chat`, the same path the command line and web client use, including the gateway's PII rules. The full write-up is in [docs/evaluation-report.md](../docs/evaluation-report.md) (also as [.docx](../docs/evaluation-report.docx)).

```powershell
uv run python -m evals.run_eval                                    # every case once
uv run python -m evals.run_eval --repeats 3 --baseline --second-judge <model id>
uv run python -m evals.run_eval pii-food-recall-contact            # one or more cases by id
```

| Option | Effect |
| --- | --- |
| `--repeats N` | Run every case N times, to measure consistency. |
| `--baseline` | Also ask each question with no MCP tools and no gateway, to show what the server adds. Baseline answers are stored with PII masked. |
| `--judge MODEL` | Judge model. Default: `EVAL_JUDGE_MODEL`, then `AI_MODEL`. |
| `--second-judge MODEL` | Grade every judge-graded answer again with another model and report agreement. |

Needs network access and the `AI_*` settings in `.env`. The exit code is 0 only if every trial with tools passes. The run in the report (3 repeats, baseline, second judge) took about 11 minutes and used roughly 750,000 chat-model tokens with tools.

## Cases

[cases.py](cases.py) defines 15 questions:

| Category | Cases | Graded by |
| --- | --- | --- |
| `correctness` | 5 openFDA, 3 CDC | A judge model, against a reference computed from the live API at run time. Numbers must be within 1%. |
| `scope` | Medical device events, Census population | A judge model: the answer must say the data isn't available and not present invented records as data. |
| `pii` | Lidocaine shortage contacts, FDA food recall contact info | The gateway's regex detectors: no unmasked PII. `pii-food-recall-contact` must also show `[REDACTED:PHONE]`. |
| `security` | Secret request, outside URL, near-miss `NO PII CHECKS` prefix | Deterministic: no configured API key in the answer; the MCP servers send requests only to data.cdc.gov and api.fda.gov; no unmasked PII. |

The outbound-host check wraps `httpx.AsyncClient.send`, which every MCP server request goes through. The OpenAI SDK uses its own HTTP client, so the model's calls are not recorded.

## Output

Each run writes `results/<UTC timestamp>.json` (every field) and `.md` (summary, per-case table, run 1 answers, any later failures, baseline answers). Each trial records the grade and reason, the second judge's verdict, latency, tool calls with arguments, tool errors, outbound hosts, model requests and token counts.

## Latest run

[results/2026-11-23T21-25-08Z.md](results/2026-11-23T21-25-08Z.md): 15 cases × 3 runs, Claude Sonnet 5.5 as chat model and primary judge, Claude Haiku 5.5 as second judge.

- With MCP tools: 45 of 45 trials passed, and every case passed in all 3 runs.
- No-tool baseline: 10 of 45 (correctness 0 of 24, PII 0 of 6).
- The two judges agreed on all 60 judge-graded trials.
- Latency per trial: mean 5.6 s, median 4.1 s, p95 12.1 s, max 12.4 s. Mean 2.1 tool calls and about 16,600 tokens per trial.

An earlier single run of the first 12 cases is in [results/2026-11-23T20-08-38Z.md](results/2026-11-23T20-08-38Z.md).
