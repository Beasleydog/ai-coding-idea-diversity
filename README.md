# Are AI coding assistants homogenizing what developers build?

EECS 448 · Group 4 · Samuel Schneider, Spencer Caldwell, Hezeki Webb.

We study whether the diversity of new public GitHub repository ideas changed
around ChatGPT's release. **The current result is an end-to-end feasibility pilot,
not evidence of an AI effect.** Independent human validation is pending.

## Start here

- [Milestone writeup (PDF)](results/Group4_Milestone_Writeup.pdf)
- [Ten-minute presentation (PDF)](results/Group4_Milestone_Presentation.pdf)
- [Readable report source](milestone.md)
- [Historical repository evidence](results/EVIDENCE.md)
- [Machine-readable observations, vectors, decisions and spend](results/pilot.json)
- [Review protocol](REVIEW.md) and [AI-use disclosure](AI_USE.md)

The PDFs are drafts for team review. Each PDF also embeds `AI_USE.md` as a file
attachment; the readable disclosure is linked above. The report and slides are generated from the
saved observations; no measured value is hand-entered into a PDF. Submission is
**October 27, 2026, before 8:59 AM America/New_York**. Each member must speak in the
presentation. Slide footers give a suggested speaker and time allocation.

## What works

`pilot.py` downloads real [GH Archive](https://www.gharchive.org/) creation events,
deduplicates repository IDs, orders them by a saved seed, and walks that order
until enough eligible projects are found. It retrieves a commit dated within
30 days of repository creation, its README and file tree through the GitHub API.
It never executes the retrieved projects.

Rule filters exclude private repositories, forks/mirrors, profile pages, missing source files,
absent/short/non-English READMEs, duplicate retained READMEs, oversized READMEs and
truncated trees. GLM 5.3 Flash classifies the remaining candidates and extracts
purpose-focused ideas of at most 80 words with exact supporting README quotes.
The final model input is the historical README alone: diagnostic runs with file
paths inferred unsupported features, so paths are now used only for rule checks.
Malformed responses and non-verbatim quotes fail closed.

Pinned all-MiniLM-L6-v2 embeddings produce a mean pairwise cosine-distance score.
We also compute a cleaned README-prefix comparison, leave-one-out ranges,
AI-topic exclusion and within-month owner deduplication. Source links, commit IDs,
hashes, model settings, token use, all candidate IDs and attempted rejection
reasons are saved. Offline verification recomputes the scores from published
vectors. Review forms contain no fabricated human ratings.

<!-- RESULTS -->

### Recorded pilot results

| Hourly frame | Candidates attempted | Retained | Idea diversity | README-prefix diversity |
|---|---:|---:|---:|---:|
| 2021-01 | 226 | 5 | 0.8328 | 0.8513 |
| 2023-01 | 60 | 5 | 0.7969 | 0.9472 |
| 2025-01 | 127 | 5 | 0.7509 | 0.7947 |

**15 retained projects; 413 attempted candidates.** 192 attempts were unavailable (HTTP 404); 4 failed model-output checks. All exploratory and final paid calls total approximately **$0.0301** by returned token usage. Conservative reservations, including uncertain calls, total **$0.4012**.

These numbers describe the selected sets only. An AI source audit inspected 15 final summaries; its notes and flagged concerns appear in the evidence index. This is not independent human validation. Smaller later scores in these three frames do not establish a population trend or an AI effect.

Recorded run: `2026-10-25T01:08:40.583500Z` (UTC). Exact vectors, candidate order, rejections, sensitivity results, prompts and token use are in [pilot.json](results/pilot.json).

<!-- /RESULTS -->

## What the pilot does not establish

The frames are January 15, **12:00–12:59 UTC** in 2021, 2023 and 2025. Ordering is
deterministic within those frames. These are not random samples of entire months,
and three sets do not support a before/after trend test. Candidate stopping at a
retained-project target also makes attempted counts unequal.

The source is an ancestor of the **currently observed default branch**, selected
using GitHub's `until` parameter and checked against committer timestamps. That
does not establish which branch was default at day 30 or whether a commit was
publicly available then. Imports, backdating, deletion, renames and rewritten
history complicate historical recovery. The current filter conservatively rejects
commits timestamped before repository creation. HTTP 404 means unavailable, not
necessarily deleted.

Identity/date redaction is best effort. Quote matching does not prove the whole
summary is correct, and model training could include these repositories.
The hosted GLM model ID is an alias, not an immutable weights revision; cached
responses preserve this run. Fresh API calls can differ even at temperature 0.
Documentation/language/extension rules select a subset of software. MiniLM limits
inputs to 256 word pieces, so the README comparison is a prefix baseline.
Stored bootstrap intervals describe resampling the selected set, not uncertainty
for monthly GitHub populations. Human filter precision/recall, summary fidelity,
pair agreement, the full 60-month trend and causal attribution are not established.

## Reproduce

Python 3.11 or 3.12. These are PowerShell commands run from this folder.
On Linux/macOS, replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --cache-dir .cache/pip .
.\.venv\Scripts\python.exe -m unittest -v
.\.venv\Scripts\python.exe pilot.py verify
.\.venv\Scripts\python.exe build.py
```

Tests and `verify` need no key or network. `build.py` rebuilds the PDFs, chart,
evidence index and **blank** review sheets from saved results. Keep filled reviewer
copies under `.cache/`; rebuilding intentionally leaves the published templates
blank. `build.py` also regenerates `milestone.md`; edit its report text in the
builder when revising the report. Installing dependencies requires network access.

To recollect the pilot, put **only** `PRIME_API_KEY=your_key` in the ignored `.env`
file or use a local copy you already have. Set `GITHUB_TOKEN` or `GH_TOKEN` in your
environment for public-repository read access; on Windows the runner can reuse an
existing WSL `gh` login. GitHub tokens are never copied into `.env` or results.

```powershell
.\.venv\Scripts\python.exe pilot.py collect --months 2021-01 2023-01 2025-01 --n 5 --max-candidates 600 --budget 1
.\.venv\Scripts\python.exe pilot.py analyze
.\.venv\Scripts\python.exe pilot.py advise
.\.venv\Scripts\python.exe pilot.py verify
.\.venv\Scripts\python.exe build.py
```

`collect` replaces the public run manifest; `analyze` must follow it. `advise` asks
GLM 5.3 Flash for study-improvement ideas and saves the exact prompt/response.
The model name is fixed to `z-ai/glm-5.3-flash`; it is never silently substituted.
`analyze` downloads the pinned MiniLM revision into `.cache/` on first use and
requires cached extraction inputs for the README baseline. Published vectors
let `verify` work without downloading a model. Use one collection/advice process
at a time; the local spend ledger is not a multiprocess billing service.

### Cost and secrets

Only LLM requests incur paid API usage. No GPU rental or billed BigQuery job was
started. Prime's live catalog provides the input/output rates. Before every POST,
the runner reserves a conservative input-byte/output-token cost, writes the
reservation to `.cache/spend.json`, and refuses requests exceeding the cumulative
cap. The default cap is **$1**, and the CLI refuses anything above **$5**. Failed
or uncertain calls keep their reservation; paid POSTs are not automatically retried.
Reported actual usage is a token-based estimate, not a downloaded billing invoice.

`.env`, `.cache/`, `.venv/` and Python build/cache files are ignored. Inputs,
raw model responses and the model cache stay local under `.cache/`. Do not delete
the spend ledger and continue paid runs under the assumption the old allowance
was restored. Do not add credentials to tracked files. Public results contain
concise source excerpts, provenance and vectors, not full third-party repositories.

## Next work

1. Independently review the pilot summaries and 50 pairs using [REVIEW.md](REVIEW.md).
2. Use [sample.sql](sample.sql) to prepare whole-month candidate frames. It has
   **not** been executed. Dry-run it and set a BigQuery byte limit before any job.
   The hourly collector does not yet ingest this SQL export.
3. Audit filtering on 100 candidates, including rejects, split across periods.
   Fix measurement errors, assess historical-branch recovery, choose monthly n,
   and freeze prompts before the full run.
4. Collect all 60 months, complete the human checks, then implement and fit the
   interrupted time series with confidence intervals and full-study robustness.

The pipeline intentionally has no causal or regression result to report yet.
The inherited course instructions and earlier design draft are preserved locally
in `.cache/original/`; they are not dependencies or generated study results.

## Files

`pilot.py` is the collection/measurement runner; `test_pilot.py` checks its critical
invariants; `build.py` generates deliverables. `results/pilot.json` is the source of
truth for measurements. `REVIEW.md`, `AI_USE.md`, `sample.sql` and `pyproject.toml`
hold the review protocol, AI record, next-stage query and dependencies. There is no
web app, database server or notebook layer.
