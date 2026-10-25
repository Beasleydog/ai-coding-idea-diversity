# Review protocol (prepared; independent human review pending)

The pilot is a feasibility exercise. Automated evidence checks and an assistant's
audit do **not** satisfy the planned two independent human reviews. Do not put a
reviewer's name or a pass in a blank cell on their behalf.

## Project filter

Two people independently read historical READMEs and paths, without the model's
labels, period labels or present-day descriptions. Assign one category:

| Label | Decision rule |
|---|---|
| project | Software with a supported, concrete purpose; includes small tools and libraries. |
| tutorial | Follows an explicitly identified tutorial, course or video. |
| coursework | Explicit assignment, class exercise or lab. |
| template | Unmodified starter; installation scaffolding alone is not evidence of a project. |
| not software | Notes, bookmarks, dotfiles or configuration without a software purpose. |
| unclear | Evidence does not distinguish the above. |

Quote a passage and explain borderline decisions. Treat clones, portfolios and
modified starters consistently. A working clone can be an independent project;
do not assume that every clone is coursework. Resolve disagreements only after
both original labels have been recorded. Retain the original labels.

For the full study, review 100 candidates (50 before and 50 after December 2022),
including rejected candidates. Report raw agreement, Cohen's kappa, and project
precision/recall against adjudicated labels; report confusion matrices separately
by period. This pilot alone cannot establish those error rates.

## Summary fidelity

Use `results/summary_review.csv`: make a separate copy per reviewer **under
`.cache/`** so blank originals remain reproducible. Open the linked historical
README. Check the historical file tree if a feature is only supported by a path.
The summary must:

1. State the software's actual purpose and main function.
2. Identify users only when supported; an unnamed audience is acceptable.
3. Contain no invented feature, scope, platform, implementation or deployment claim.
4. Use at most 80 words and avoid treating installation boilerplate as purpose.

Mark `pass` only if all four hold. Otherwise mark `fail`, quote the unsupported or
omitted claim, and suggest a correction. Mark `uncertain` when inaccessible evidence
prevents a decision. Quotes matching the input are a necessary check, not proof
that every sentence is accurate. Full-study target: at least 45/50 passing
summaries, with both reviewers' decisions and disagreements reported. Pilot
inspection is diagnostic; it is not a certified accuracy percentage.

## Idea similarity (1–5)

Use `results/pair_review.csv`. Model scores, repository names and dates are omitted.
Rate the intended software idea rather than wording or programming language.

| Score | Anchor |
|---|---|
| 1 | Unrelated purpose and users (for example, a budget tool and a music synthesizer). |
| 2 | A broad theme overlaps, but the functions differ. |
| 3 | Related problem or audience, with substantially different main functions. |
| 4 | Same main purpose, with a meaningful difference in use or function. |
| 5 | Essentially the same software idea; implementation differences alone do not count. |

Each reviewer rates independently. Record uncertainty and a short rationale. The
worksheet deterministically samples up to 50 pairs across **all** pilot projects;
it is not restricted to pairs within a month. After review, report the proportion
of ratings within one point and Spearman correlation of mean human ratings with
cosine similarity. Inspect disagreements before freezing the extraction prompt.
Do not use model-generated ratings as human validation.

## What this pilot can settle

Check that the historical source is recoverable; distinguish raw retrieval errors,
rule exclusions and model failures; confirm the metric by direct pairwise distance;
find model mistakes to fix before scaling. It cannot establish an effect of AI,
monthly population diversity, a validated classifier, or a reliable sample size.
