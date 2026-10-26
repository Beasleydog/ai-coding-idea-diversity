# GitHub idea diversity

EECS 448, Group 4. Current milestone: set up repository-ID collection.
Filtering, historical file retrieval, summaries and diversity analysis are next steps.

## Current collection

**12,000 unique repository IDs: 200 for each month, January 2021 through December 2025.**
These are unfiltered candidates, not verified eligible projects. Selection ignores
all preliminary filtering decisions. There is no minimum commit count, language,
README, popularity or project-type requirement at this stage.

- `data/repositories.csv`: month, repository ID, name and URL.
- `data/months.csv`: selected count and target for every month.
- `data/collection.sqlite`: resumable candidate records and preserved earlier cost ledger.
- `presentation/`: editable PowerPoint with speaker notes and submission PDF.
- `milestone.md`, `requirements.txt`, `figures/`: original study design and course materials.
- `AI_USE.md`: assistance disclosure and decisions.

## Run

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install .
.venv/Scripts/python.exe collect.py collect --target 200 --workers 4
.venv/Scripts/python.exe collect.py export --target 200
.venv/Scripts/python.exe -m unittest -q
```

Set `GITHUB_TOKEN` in the environment or local `.env`, or use an existing `gh`
login (through WSL on Windows). `requirements.txt` is the course rubric, not a
Python dependency file. Never commit credentials or delete the local ledger.

The collector uses seeded time windows and stable ID ordering. Independent
requests run in parallel; SQLite writes and exports stay in one process. Completed
windows are saved so interrupted runs can resume. Rate-limit or incomplete-response
errors stop collection rather than silently changing the sample. CSVs are replaced
only after a complete export.

No repositories are cloned, no source code is executed, and no LLM calls are made.
This ID-only continuation added no model cost. The earlier ledger still accounts
for $0.069554 in usage plus a $0.401161 prior reserve, below the $5 limit.

The current collection establishes pipeline inputs. It is not a validated sample
for inference. The original writeup's final equal-size eligible sample remains
planned; filtering may require collecting additional candidates.
