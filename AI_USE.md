# AI use for the retained milestone materials

## Models and scope

- **GPT-6 through Codex** drafted and revised slide wording, diagrams, speaker
  notes, LaTeX equation layouts, the illustrative Gum summary, collection code,
  tests and this documentation. The inherited `milestone.md` also discloses GPT-6
  assistance. Its original writing prompts were not available in this workspace.
- **GLM 5.3** (`z-ai/glm-5.3`, through Prime Inference) was used in the
  preliminary repository-purpose filtering run, which is not used to select
  the current ID-only collection. It produced no diversity results or idea
  summaries. Settings were temperature 0, low reasoning, and at most 1,536
  output tokens. The exact prompt, responses and usage remain in the local
  SQLite ledger. The current collector makes no model calls.
- The earlier exploratory implementation and its outputs were removed at the
  user's request. Its conservative $0.401161 budget reservation remains in the
  new accounting. The presentation does not reuse its empirical results.

## Presentation and implementation requests

The user supplied `milestone.md`, the course requirements and these instructions
(verbatim; spelling preserved):

> Make a slideshow presentation for the milestone. Consider the requirements file. We should convey the content from milestone.md, i dont awnt to talk about any of the work results we've done yet. IF U HAEV QUESTIONS HERE ASK ME RATHER TAHN ASSUMING
>
> I really want this to be text light presentation, without benig ambigious. every singel piece of text must earn its place, do'nt have eyebrow designs or text or nothing. but, make sure we go into enough detail to fully explain

> 1. I think im gonna try to collect + filter all of the repos we're gonna analyze by presentation time. so can we frame it as our current progress is setting up the github scraping + filtering pipeline
> 2. have speaker notes, they don't need to be assigned to people we can do that ourselves

> the equations are bad, need to be rendered latex not unicode. they need arrows pointing to chunks of each equation with labels to explain the role of each part, right now the math slides are way too heavy need to be broken down into multiple slides and explain the key equations we're using.
>
> also, in thsi repo, we have a bunch of explorateory work. it stated with requirements.txt and milestone.md and then i had you do some exploratoy work to get stuf we can presesnt. this work didnt turn out great. can you delete aell that stuff leaving only the requirements milestone.md and this presentation (and otehr stuff i would reasonably wnana keep i may be forgetting about) but like none of the prior work you did and then just setup an ultra clean pipeline to scrape github and then it passes repos into glm 5.3 to do the filtering step, try to collect the data we need but spend MAX 5 dollars. also i dont wanna be storing massive repos locally so lets just collect the ids or smthn. then ideally we can say we found N repos for all the month sblah blah we filtered in thsi way and exlcuded Y bad ones blah blah and have slides to talk about thsi stuff. keep the code and implementation and file structure and foler AS CLEANA S POSSIBLE, ULTRA MINIMAL AND CLEAN AND READABLE AND PRECISE, NO JUNK.
>
> also, go through all the slides and remove any un-needed eybrow text. try to make each statement as clear a spossible. i literally want you to go chunk by chunk, sentence by sentence, etc and think "is thsi needed" then "is it phrased as cleanly as possible" etc

The user approved historical sampling rather than present-day GitHub search:

> Use sampled hours across all 60 months

The user later reduced the collection size to finish sooner:

> Use one hour per month to finish sooner

After discussing an optional adoption-period exclusion, the user chose:

> Keep the current design for now

The user also requested:

> also when we talk about the llm summary can we have a slide that shows a screenshot of a repo and then next to it has an llm summary to show how we're gonna summarize repos

## Example summary

The illustrative summary was drafted from Gum's historical README at commit
`be4027ce28f812f905bfd1b5575e198729a6c4cc`:
https://github.com/charmbracelet/gum/blob/be4027ce28f812f905bfd1b5575e198729a6c4cc/README.md

The README describes shell-script utilities and documents input, fuzzy filtering,
progress indicators, styling and layout. These support the summary's claims.
Gum was deliberately chosen for explanation; it is not represented as a randomly
sampled observation or a GLM filtering result. The screenshot shows the real
GitHub interface with that commit selected; remotely hosted badges and the
interface itself can reflect the present day.

## Checks, corrections and student review

The assistant checked equation rendering, slide layout, source-to-summary claims,
package integrity, and collection budget behavior. These are implementation
checks, not independent scientific validation. Collection counts come from the
new ledger. Missing archives, unavailable repositories, exclusions and model
errors must remain distinct.

Observed assistant errors corrected during this revision: the first collector
used padded hour filenames that GH Archive does not use; its executor initially
waited on queued downloads after a failure. Native SVG equation images rendered
blank in the slide preview, so the actual LaTeX output was rendered to high
resolution transparent images. A first candidate for the summary example was a
starter template and was discarded. Interrupted archive downloads required
bounded retries. Earlier dense Unicode math slides were replaced. The exported
PowerPoint passed schema validation but failed normal opening in Microsoft
PowerPoint. PowerPoint's repair mode regenerated the package; normal reopening,
slide renders, content comparisons and all speaker notes were then checked.
The November and December 2025 sampled archives contained no repository-creation
events; the slides report those as coverage gaps without changing the study window.

**Independent team review remains pending.** Before submission, the team should
record which suggestions it accepts or rejects, why, and any additional errors
it finds. In particular, review the sampled-hour population, early-snapshot
limitations, filter accuracy and the representation of current progress. Do not
present this assistant-authored record as a student's endorsement. The inherited
writeup's original prompt log should be supplied by the team if available.

## ID-only milestone revision

The user changed the immediate deliverable to 200 unfiltered repository IDs for
each of the 60 months, with filtering presented as future work. The current CSV
therefore ignores all preliminary eligibility decisions. The presentation no
longer reports preliminary acceptance or rejection counts. No commit-count
threshold was adopted, and this continuation made no additional paid model calls.
The old response and cost ledger is preserved for accounting, not used as a
validated labeling dataset. Independent human validation remains future work.

The assistant checked 26 historical examples while investigating the preliminary
filter and found inconsistent judgments based on boilerplate READMEs. It also
found that event delivery timestamps could lag repository creation by a second.
Those exploratory decisions are not used in the ID-only deliverable; the current
collector performs neither historical-commit eligibility checks nor LLM filtering.
The ID export was checked for 12,000 unique IDs and exactly 200 per month.
