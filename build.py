"""Build the milestone report, slides, evidence index and blank review sheets."""

import csv
from itertools import combinations
from pathlib import Path
import re
from xml.sax.saxutils import escape

from pilot import ROOT, SEED, digest, load
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.graphics.shapes import Drawing, Rect, String, Line
import fitz

OUT = ROOT / "results"
NAVY = "#142D4E"
TEAL = "#087E8B"
GRAY = "#536174"
REFS = [
    ('Anil R. Doshi and Oliver P. Hauser. 2024. Generative AI enhances individual creativity but reduces the collective diversity of novel content. Science Advances 10, 28, eadn5290.', 'https://doi.org/10.1126/sciadv.adn5290'),
    ('GH Archive. n.d. GH Archive: public GitHub timeline and hourly archives. Retrieved October 24, 2026.', 'https://www.gharchive.org/'),
    ('GitHub. n.d. REST API endpoints for commits. Retrieved October 24, 2026.', 'https://docs.github.com/en/rest/commits/commits#list-commits'),
    ('Sentence Transformers. n.d. all-MiniLM-L6-v2 model card. Retrieved October 24, 2026.', 'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2'),
    ('James Lopez Bernal, Steven Cummins, and Antonio Gasparrini. 2017. Interrupted time series regression for the evaluation of public health interventions: a tutorial. International Journal of Epidemiology 46, 1, 348-355.', 'https://doi.org/10.1093/ije/dyw098'),
    ('OpenAI. 2022. Introducing ChatGPT. November 30, 2022.', 'https://openai.com/index/chatgpt/'),
    ('Prime Intellect. n.d. Prime Inference; live model catalog and pricing. Retrieved October 24, 2026.', 'https://docs.primeintellect.ai/inference/overview'),
    ('Whitney K. Newey and Kenneth D. West. 1987. A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix. Econometrica 55, 3, 703-708.', 'https://doi.org/10.2307/1913610'),
]


def write_csv(name, fields, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def worksheets(data):
    records = data["records"]
    rows = [{"id": f"R{i+1:02}", "summary": r["idea"], "historical_source": r["source"],
             "reviewer": "", "pass_fail_uncertain": "", "reason": ""}
            for i, r in enumerate(records)]
    write_csv("summary_review.csv", list(rows[0]), rows)
    pairs = sorted(combinations(range(len(records)), 2), key=lambda ij: digest(f"{SEED}:pair:{ij}".encode()))[:50]
    rows = [{"pair_id": f"P{k+1:02}", "a_id": f"R{i+1:02}", "b_id": f"R{j+1:02}",
             "idea_a": records[i]["idea"], "idea_b": records[j]["idea"],
             "reviewer": "", "rating_1_to_5": "", "rationale": ""}
            for k, (i, j) in enumerate(pairs)]
    write_csv("pair_review.csv", list(rows[0]), rows)


def chart(data):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5), layout="constrained")
    months = data["months"]
    labels = [m["month"] for m in months]
    counts = [sum(d["month"] == m["month"] for d in data["decisions"]) for m in months]
    axes[0].bar(labels, counts, color=NAVY, label="Candidates attempted")
    axes[0].bar(labels, [m["kept"] for m in months], color=TEAL, label="Projects retained")
    for i, m in enumerate(months):
        axes[0].text(i, counts[i] + max(counts)*0.03, f"{m['kept']}/{counts[i]}", ha="center")
    axes[0].set_ylim(0, max(counts)*1.22)
    axes[0].set_title("Retrieval and filtering workload", loc="left", weight="bold")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].set_ylabel("Repositories")
    x = np.arange(len(months))
    axes[1].bar(x - .18, [m["diversity"] for m in months], width=.36, color=TEAL, label="Idea statements")
    axes[1].bar(x + .18, [m["readme_diversity"] for m in months], width=.36, color="#ABC0D5", label="Cleaned README prefix")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylim(0, 1.15)
    axes[1].set_ylabel("Mean cosine distance")
    axes[1].set_title("Selected-set diversity only", loc="left", weight="bold")
    axes[1].legend(frameon=False, fontsize=8)
    for i, m in enumerate(months):
        axes[1].text(i-.18, m["diversity"]+.025, f"{m['diversity']:.3f}", ha="center", fontsize=9)
    fig.suptitle("Feasibility samples: one UTC hour per month; no population or causal inference", fontsize=11, color=NAVY)
    fig.savefig(OUT / "pilot.png", dpi=180)
    plt.close(fig)


def flow(width=490):
    d = Drawing(width, 115)
    scale = width / 490
    steps = [("GH Archive", "creation events"), ("Day-30 source", "README + paths"),
             ("GLM 5.3 Flash", "filter + idea"), ("MiniLM", "384-D vectors"),
             ("Diversity", "one score/set")]
    w = (width - 32) / 5
    for i, (title, subtitle) in enumerate(steps):
        x = i * (w + 8)
        d.add(Rect(x, 58, w, 46, rx=5, fillColor=colors.HexColor("#E5F4F4"), strokeColor=colors.HexColor(TEAL)))
        d.add(String(x+w/2, 87, title, textAnchor="middle", fontName="Helvetica-Bold", fontSize=9*scale))
        d.add(String(x+w/2, 67, subtitle, textAnchor="middle", fontSize=8*scale))
        if i < 4:
            d.add(Line(x+w, 81, x+w+8, 81, strokeColor=colors.HexColor(TEAL)))
    d.add(Rect(0, 5, width, 38, rx=5, fillColor=colors.HexColor("#F1F3F6"), strokeColor=colors.HexColor("#BCC6D0")))
    d.add(String(12, 29, "PLANNED: whole-month samples -> human validation -> 60-month trend + robustness", fontSize=9*scale))
    d.add(String(12, 12, "Teal = implemented pilot stages. Gray = full-study work; not claimed complete.", fontSize=8*scale, fillColor=colors.HexColor(GRAY)))
    return d


def text_plain(value):
    return re.sub(r"<[^>]+>", "", value).replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")


def report(data):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Body448", fontSize=10.2, leading=14.2, spaceAfter=8, textColor=colors.HexColor(NAVY)))
    styles.add(ParagraphStyle(name="Small448", fontSize=8.2, leading=11, spaceAfter=6))
    styles["Title"].fontSize, styles["Title"].leading = 23, 28
    styles["Heading1"].textColor = colors.HexColor(TEAL)
    story, md = [], ["# Are AI Coding Assistants Homogenizing What Developers Build?\n",
                     "Group 4: Samuel Schneider, Spencer Caldwell, Hezeki Webb\n\nOctober 27, 2026 milestone; draft for team review.\n"]

    def p(value, small=False):
        story.append(Paragraph(value, styles["Small448" if small else "Body448"]))
        md.append(text_plain(value) + "\n")

    def h(value):
        story.append(Paragraph(value, styles["Heading1"]))
        md.append("## " + value + "\n")

    def table(rows, widths):
        rendered = [[Paragraph(escape(str(x)), styles["Small448"]) for x in row] for row in rows]
        t = Table(rendered, colWidths=widths, repeatRows=1, hAlign="LEFT")
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5F4F4")),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("LINEBELOW", (0, 0), (-1, 0), .7, colors.HexColor(TEAL)),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                               ("TOPPADDING", (0, 0), (-1, -1), 6)]))
        story.extend([t, Spacer(1, 10)])
        md.extend(["| " + " | ".join(map(str, row)) + " |" for row in rows[:1]])
        md.append("|" + "---|"*len(rows[0]))
        md.extend("| " + " | ".join(map(str, row)) + " |" for row in rows[1:])
        md.append("")

    def page():
        story.append(PageBreak())
        md.append("\n")

    months = data["months"]
    n = len(data["records"])
    attempted = len(data["decisions"])
    spend = sum(x.get("estimated_usd", 0) for x in data["spend"])
    reserve = sum(x["reserved_usd"] for x in data["spend"])
    invalid = sum(d["reason"] == "invalid_model_output" for d in data["decisions"])
    unavailable = sum(d["reason"] == "github_http_404" for d in data["decisions"])
    story.append(Paragraph("Are AI Coding Assistants Homogenizing What Developers Build?", styles["Title"]))
    p("Group 4 | Samuel Schneider, Spencer Caldwell, Hezeki Webb<br/>October 27, 2026 milestone | Draft for team review", small=True)
    h("Executive summary")
    p("AI coding assistants may affect which software ideas people pursue. Easier implementation could broaden the range of projects, while shared suggestions could make projects more alike. Doshi and Hauser [1] found greater similarity among AI-assisted stories; whether software project choices follow that pattern remains an open question.")
    p("<b>We will measure whether the diversity of ideas in newly created public GitHub repositories changed around ChatGPT's release.</b>")
    p("The proposed study samples 60 months, January 2021 through December 2025, and describes each repository using source material from its first 30 days. Short idea statements become embeddings; mean pairwise cosine distance measures the diversity of each selected set. The eventual analysis estimates level and slope changes from December 2022, the first full month after the November 30 release [6].")
    p(f"We have implemented an end-to-end feasibility pilot with <b>{n} projects across {len(months)} selected months</b>, exceeding the original five-project target. We attempted {attempted} candidates, retained historical commit links and source hashes, generated evidence-linked statements with GLM 5.3 Flash, and computed MiniLM embeddings and diversity scores. Estimated API cost is ${spend:.4f}; conservative reservations total ${reserve:.4f}, below the $5 limit. The most useful initial result is a measured account of retrieval and filtering failures.")
    p("This is a pipeline demonstration, not evidence that AI changed software diversity. The pilot uses one UTC hour per month rather than whole-month samples. Independent human review, full-month sampling and the 60-month regression remain pending.")
    story.append(flow())
    md.append("![Pilot measurements](results/pilot.png)\n\nImplemented: archive -> historical source -> GLM filter/idea -> MiniLM -> diversity. Planned: full-month samples, human validation, 60-month regression.\n")
    page()

    h("Proposed solution and implementation")
    p("<b>Inputs and sampling.</b> GH Archive supplies public CreateEvents [2]. The pilot downloads January 15, 12:00-12:59 UTC in 2021, 2023 and 2025. We keep repository-creation events, deduplicate IDs, and order candidates by SHA256(seed:repository_id), with seed <b>448-pilot-v1</b>. Rejections are replaced in that saved order. This is reproducible ordering within each hourly frame, not a random sample of a month. The prepared BigQuery query in sample.sql covers an entire month; it has not been run or billed.")
    p("<b>Historical retrieval.</b> Repository IDs resolve current metadata. We query ancestors of the currently observed default branch with GitHub's until parameter [3], select the returned commit, and require its committer timestamp to fall between creation and creation + 30 days. We recover its tree and README blob, saving the commit, tree and content hashes. This does not recover the historical default-branch name, prove public availability at the cutoff, or detect backdated commits and rewritten history. Imported histories with earlier timestamps are excluded.")
    p("<b>Filtering.</b> Reject forks/mirrors, profile repositories, missing source extensions, truncated trees, absent/short/non-English READMEs, and within-month duplicate retained READMEs. The extension allowlist includes HTML, CSS, SQL and notebooks. READMEs over 200 KB are excluded. English detection is seeded. GLM assigns project, tutorial, coursework, template, not software or unclear; only project passes. Schema failures and non-verbatim evidence quotes are recorded as model failures, never as accepted projects.")
    p("<b>Representation.</b> Every final extraction request uses the same prompt, temperature 0, low reasoning and 3,072 output-token cap. Input is bounded to 12,000 historical README characters; the file tree supports eligibility checks. We removed paths from model input after diagnostic runs inferred unsupported features from filenames. Identity/URL/date redaction is best effort. The model outputs an idea of at most 80 words and evidence quotes. Full inputs/responses are cached locally; the public index publishes concise quotes, source links and request hashes. Dependency-file retrieval is deferred.")
    p("<b>Measurement and outputs.</b> all-MiniLM-L6-v2 [4], pinned to one model revision, produces normalized 384-dimensional vectors. For n vectors, diversity = n/(n-1) * (1 - squared norm of their mean). Offline tests check this formula against explicit pairwise distances. We also compute leave-one-out ranges, a cleaned README-prefix baseline, AI-topic exclusion and within-month owner deduplication. MiniLM truncates long inputs at its 256 word-piece limit; the README baseline is therefore a prefix check. No repository code is executed.")
    page()

    h("Pilot results and interpretation")
    rows = [["Hourly frame", "Attempted", "Retained", "Idea distance", "README distance"]]
    for m in months:
        rows.append([m["month"], sum(d["month"] == m["month"] for d in data["decisions"]), m["kept"], f"{m['diversity']:.4f}", f"{m['readme_diversity']:.4f}"])
    table(rows, [100, 77, 70, 121, 122])
    story.append(Image(str(OUT / "pilot.png"), width=490, height=171.5))
    p(f"Across these frames, {unavailable}/{attempted} attempts returned HTTP 404 (unavailable; deletion and privacy cannot be distinguished). There were {invalid} invalid model outputs. Per-candidate reasons and complete candidate order are in results/pilot.json. Frame-specific stopping at the target means that attempted counts are workload measures, not equally sized surveys of each frame.")
    p("Higher distance means greater spread among these retained ideas. The values are descriptive; three sparse hourly samples cannot support a temporal trend, a before/after significance test or causal attribution. README and idea scores measure different representations and are not interchangeable. Stored bootstrap intervals condition on the selected projects; they are not confidence intervals for monthly populations.")
    first = data["records"][0]
    p(f"<b>Example, R01.</b> {escape(first['idea'])}<br/><b>Evidence:</b> {escape(first['idea_quotes'][0])}<br/><link href=\"{escape(first['source'])}\" color=\"#087E8B\">Inspect the historical README at the recorded commit</link>.", small=True)
    p("<b>Main threats.</b> Accessibility and documentation select the sample; language and extension rules exclude some software; model errors can differ over time; summaries may preserve implementation style or hallucinate purpose. Current-branch ancestry is an imperfect historical reconstruction. Future models may know these repositories, so redaction does not guarantee blindness. Broader changes in GitHub users and projects can explain any eventual trend.")
    page()

    h("Milestones and validation")
    table([["Deliverable / proposal plan", "Current status", "Lead"],
           ["1. Data pipeline / 200-repository pilot", f"Working historical pipeline; {attempted} attempted, {n} retained across three frames. Whole-month sampling pending.", "Samuel"],
           ["2. Representation and analysis / ideas, scores, plots", "Implemented for pilot: summaries, embeddings, scores, baseline and sensitivities. Full trend pending.", "Spencer"],
           ["3. Summary validation / two reviewers, 50 summaries", "Rubric and pilot worksheets prepared; automated evidence checks run. Independent human review pending.", "Hezeki"],
           ["4. Similarity validation / two reviewers, 50 pairs", "1-5 anchors and 50 blinded pair rows prepared. Human ratings and correlation pending.", "Hezeki"]], [188, 235, 67])
    p("<b>Goal 1.</b> The initial October 27 target was five projects from one month. The pilot now connects archive collection, historical retrieval, filtering and representation across three frames. Saved decisions expose failures. The proposal's representative monthly sample is still a separate task.")
    p("<b>Goal 2.</b> Public records contain ideas, quotes, hashes, historical links, normalized vectors and descriptive sensitivity results. Re-running verification needs no key or paid call. A single-command builder regenerates this five-page report, PDF slides, the result figure and blank reviewer sheets.")
    p("<b>Goals 3 and 4.</b> REVIEW.md defines categories, summary checks and 1-5 similarity anchors. Blank sheets cover all pilot summaries and 50 pairs. An AI source audit inspected all 15 summaries, flagging two platform inferences and two filter ambiguities (configuration versus software; possible upstream copy). These notes are in the evidence index. Two people must independently review before adjudication. The full-study summary target is 45/50 passing; filter precision/recall must include rejects. No human accuracy or agreement is claimed.")
    h("Way forward and schedule")
    table([["When", "Next concrete outcome", "Lead"],
           ["Oct 25-27", "Team checks evidence/AI disclosure, independently reviews pilot summaries and pairs, rehearses 10-minute talk.", "All; Hezeki coordinates reviews"],
           ["Oct 28-Nov 8", "Whole-month candidate frames, period-stratified filter audit, historical-branch sensitivity; expand several months and choose n/prompt.", "Samuel + Spencer"],
           ["Nov 9-20", "Run 60 months; finish 100-candidate, 50-summary and 50-pair checks; report monthly retrieval losses.", "Spencer + Hezeki"],
           ["Nov 21-final", "Fit segmented regression; robustness, interpretation, final paper and talk.", "All; Hezeki coordinates"]], [85, 310, 95])
    page()

    h("Full-study analysis and references")
    p("After representative monthly collection and human checks, fit a segmented time-series model [5] to 60 monthly scores: linear time, post-December-2022 indicator, time since that breakpoint, and annual sine/cosine terms. Report level and slope changes with Newey-West [8] 95% intervals and diagnose autocorrelation. Repeat without AI-topic projects, with one repository per owner across the study, and using cleaned README embeddings. These full-study checks have not been completed. The pilot owner check is within each month only.")
    for i, (ref, url) in enumerate(REFS, 1):
        p(f"[{i}] {escape(ref)} <link href=\"{escape(url)}\" color=\"#087E8B\">{escape(url)}</link>", small=True)
    h("Generative AI use and submission checks")
    p("GPT-6 through Codex implemented the pipeline, tests, draft prose and PDF materials. GLM 5.3 Flash generated project idea statements/classifications and study-improvement suggestions. Inputs were this repository's plan, the user's instructions and historical README/path evidence. The complete extraction prompt is stored in results/pilot.json and pilot.py. The attached AI_USE.md records user/extraction prompts, settings, reasoning, errors and the advice prompt/response location. An online copy is linked from the repository README. Review the attachment with this submission.", small=True)
    p("Observed model errors include missing required fields and quotes drawn from file paths rather than the README; those outputs were rejected. Passing automatic checks establishes only format and quote fidelity, not factual completeness. The reason to retain the method is reproducible, source-linked measurement with explicit rejection logs, not unverified trust in generated prose. Team members must record their own acceptance/rejection decisions and corrections in AI_USE.md before submission. The drafts do not claim that any named teammate has performed this review.", small=True)
    p("Submit Group4_Milestone_Writeup.pdf and Group4_Milestone_Presentation.pdf by October 27, 2026, 8:59 AM America/New_York, with the AI-use record as required by the course. The report is five pages; the talk is planned for ten minutes with each member speaking. Source-linked pilot details and blank review sheets remain in the repository.", small=True)

    def footer(c, doc):
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor(GRAY))
        c.drawString(54, 28, "Group 4 | EECS 448 | Feasibility pilot | Draft for team review")
        c.drawRightString(558, 28, str(doc.page))

    doc = SimpleDocTemplate(str(OUT / "Group4_Milestone_Writeup.pdf"), pagesize=(612, 792),
                            leftMargin=54, rightMargin=54, topMargin=36, bottomMargin=45,
                            title="Group 4 Milestone Writeup", author="Group 4 (AI-assisted draft)")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    attach_disclosure(OUT / "Group4_Milestone_Writeup.pdf")
    (ROOT / "milestone.md").write_text("\n".join(md), encoding="utf-8")


def slides(data):
    c = canvas.Canvas(str(OUT / "Group4_Milestone_Presentation.pdf"), pagesize=(960, 540))
    c.setTitle("Group 4 Milestone Presentation")
    c.setAuthor("Group 4 (AI-assisted draft)")
    slide_no = 0

    def slide(title, lines, speaker, timebox, picture=False, diagram=False):
        nonlocal slide_no
        slide_no += 1
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.rect(0, 0, 960, 540, fill=1, stroke=0)
        c.setFillColor(colors.HexColor(TEAL))
        c.rect(0, 524, 960, 16, fill=1, stroke=0)
        title_style = ParagraphStyle("slideTitle", fontName="Helvetica-Bold", fontSize=31, leading=36, textColor=colors.HexColor(NAVY))
        para = Paragraph(title, title_style)
        _, height = para.wrap(850, 120)
        para.drawOn(c, 50, 485-height)
        y = 465-height
        style = ParagraphStyle("slideBody", fontSize=21 if not picture else 17, leading=29 if not picture else 23, textColor=colors.HexColor(NAVY))
        for line in lines:
            para = Paragraph(line, style)
            _, height = para.wrap(850, 430)
            para.drawOn(c, 54, y-height)
            y -= height + 19
        if picture:
            c.drawImage(str(OUT / "pilot.png"), 55, 110, width=850, height=297.5, preserveAspectRatio=True, mask="auto")
        if diagram:
            from reportlab.graphics import renderPDF
            renderPDF.draw(flow(840), c, 55, 95)
        c.setStrokeColor(colors.HexColor("#CBD5E1"))
        c.line(50, 48, 910, 48)
        c.setFillColor(colors.HexColor(GRAY))
        c.setFont("Helvetica", 10)
        c.drawString(50, 29, f"Group 4 | {speaker} | {timebox} | Feasibility pilot; draft for team review")
        c.drawRightString(910, 29, str(slide_no))
        c.showPage()

    n, attempts = len(data["records"]), len(data["decisions"])
    spend = sum(s.get("estimated_usd", 0) for s in data["spend"])
    slide("Are AI coding assistants homogenizing what developers build?", [
        "Samuel Schneider · Spencer Caldwell · Hezeki Webb<br/>EECS 448 · October 27, 2026",
        f"<b>Milestone:</b> a working historical pipeline and {n} inspected-source project records across three hourly frames.",
        "Our question is open. This pilot tests the measurement process."], "Samuel", "0:50")
    slide("Why measure software ideas?", [
        "AI suggestions may steer people toward similar projects; easier implementation may also broaden what people build.",
        "AI-assisted stories became more similar in Doshi &amp; Hauser [1]. Software project choices may behave differently.",
        "<b>Objective:</b> measure changes in new-repository idea diversity around ChatGPT's release [6]."], "Samuel", "0:55")
    slide("One pipeline, source evidence at every stage", [
        "Public creation events → historical source at a fixed repository age → README-grounded idea → embedding → selected-set diversity.",
        "Implemented pilot stages appear in teal. Full-month sampling, human checks and the time-series study remain planned."], "Samuel", "1:05", diagram=True)
    slide("What did we actually sample?", [
        "January 15, 12:00–12:59 UTC, in 2021, 2023 and 2025 [2]. Seeded order; repository IDs deduplicated.",
        f"{attempts} candidates attempted → {n} eligible projects. Every exclusion is logged.",
        "Commits are dated within creation + 30 days, on current-default-branch ancestry [3]. Historical branch identity is not recovered.",
        "These are hourly feasibility samples. Whole-month BigQuery sampling is prepared, not run."], "Samuel", "1:10")
    slide("From a README to an idea vector", [
        "GLM 5.3 Flash: six project labels, an idea ≤80 words, and exact supporting README quotes [7].",
        "Same prompt and settings; bounded historical README input; identity/date redaction is best effort. Reject schema and quotation failures.",
        "MiniLM: 384 dimensions, unit normalization, pinned revision [4]. Mean pairwise cosine distance measures spread.",
        f"Estimated API use: ${spend:.4f}. A cumulative reservation ledger guards the $5 ceiling."], "Spencer", "1:05")
    slide("First descriptive measurements", [], "Spencer", "1:10", picture=True)
    slide("Checks that already run", [
        "Historical commit-window checks; exact quote checks; unit-vector checks; fast score agrees with explicit pairwise distances.",
        "Cleaned README-prefix baseline, leave-one-out ranges, AI-topic exclusion and within-month owner deduplication.",
        "Missing repositories and invalid model outputs are visible results. Passing these checks does not certify summary accuracy."], "Spencer", "1:00")
    slide("Human validation is prepared, still pending", [
        f"{n} summary-review rows, 50 pair-rating rows, and a shared rubric in REVIEW.md.",
        "Two independent reviewers: summary purpose/function supported, no invented claims; pair similarity rated from 1 (unrelated) to 5 (same idea).",
        "Then report agreement and similarity correlation. Full study: audit 100 candidate labels, including rejected projects.",
        "No human accuracy or agreement percentage is claimed today."], "Hezeki", "1:00")
    slide("What we can and cannot conclude", [
        "We can run the pipeline, preserve historical links, quantify attrition, and measure selected-set diversity.",
        "We cannot infer an AI effect, population monthly diversity, or a reliable temporal trend from three sparse hourly frames.",
        "Main risks: survival/documentation bias, changed branches/history, model errors, and unobserved changes in who uses GitHub.",
        "Next: whole-month frames, independent review, broader pilot, frozen prompt/sample size, then 60-month analysis [5,8]."], "Hezeki", "1:00")
    slide("Milestone status and next steps", [
        "<b>Samuel:</b> working data pipeline; next, full-month frames and historical retrieval checks.",
        "<b>Spencer:</b> ideas, embeddings and descriptive scores; next, several-month pilot and full trend after validation.",
        "<b>Hezeki + all:</b> prepared review guides; next, independent ratings and evidence review before submission.",
        "Oct 28–Nov 8: sampling/measurement pilot. Nov 9–20: collection and validation. Nov 21–final: analysis and report."], "Hezeki", "0:45")
    slide("References and AI disclosure", [
        "[1] Doshi &amp; Hauser, Science Advances (2024). [2] GH Archive. [3] GitHub commit API. [4] MiniLM model card.",
        "[5] Lopez Bernal et al., IJE (2017). [6] OpenAI, Introducing ChatGPT (2022). [7] Prime Inference. [8] Newey &amp; West (1987).",
        "Full linked references are in the writeup. AI_USE.md records prompts, settings and errors. Codex drafted code/materials; GLM produced classifications, ideas and design advice.",
        "Team review and acceptance decisions remain pending. Questions?"], "All", "reference slide; Q&A")
    c.save()
    attach_disclosure(OUT / "Group4_Milestone_Presentation.pdf")


def attach_disclosure(path):
    doc = fitz.open(path)
    doc.embfile_add("AI_USE.md", (ROOT / "AI_USE.md").read_bytes(), filename="AI_USE.md",
                    desc="Generative AI prompts, model settings, reasoning and observed errors")
    tmp = path.with_suffix(".tmp")
    doc.save(tmp)
    doc.close()
    tmp.replace(path)


def evidence(data):
    lines = ["# Pilot evidence", "", "Feasibility samples only. Human validation is pending.", "",
             "Each source link resolves a README at a recorded commit. IDs match the blank review sheets.", ""]
    for i, r in enumerate(data["records"], 1):
        lines.extend([f"## R{i:02}: {r['name']} ({r['month']})", "", r["idea"], "",
                      f"[Historical README]({r['source']}) · commit `{r['commit']}`", "",
                      f"Created: {r['created_at']}; cutoff: {r['cutoff']}; commit timestamp: {r['committed_at']}.", "",
                      "Supporting model-input quotes:", ""])
        lines.extend("> " + q.replace("\n", "\n> ") + "\n" for q in r["idea_quotes"])
        lines.extend([f"Request SHA256: `{r['request_sha256']}`. README SHA256: `{r['readme_sha256']}`.", ""])
        if "assistant_audit" in data:
            audit = data["assistant_audit"]["records"][i-1]
            lines.extend([f"**AI source-audit note (not human validation): {audit['summary_assessment']}.** {audit['note']}", ""])
    (OUT / "EVIDENCE.md").write_text("\n".join(lines), encoding="utf-8")


def readme_results(data):
    lines = ["<!-- RESULTS -->", "", "### Recorded pilot results", "",
             "| Hourly frame | Candidates attempted | Retained | Idea diversity | README-prefix diversity |",
             "|---|---:|---:|---:|---:|"]
    for m in data["months"]:
        attempted = sum(d["month"] == m["month"] for d in data["decisions"])
        lines.append(f"| {m['month']} | {attempted} | {m['kept']} | {m['diversity']:.4f} | {m['readme_diversity']:.4f} |")
    cost = sum(x.get("estimated_usd", 0) for x in data["spend"])
    bound = sum(x["reserved_usd"] for x in data["spend"])
    unavailable = sum(d["reason"] == "github_http_404" for d in data["decisions"])
    invalid = sum(d["reason"] == "invalid_model_output" for d in data["decisions"])
    lines.extend(["", f"**{len(data['records'])} retained projects; {len(data['decisions'])} attempted candidates.** "
                  f"{unavailable} attempts were unavailable (HTTP 404); {invalid} failed model-output checks. "
                  f"All exploratory and final paid calls total approximately **${cost:.4f}** by returned token usage. "
                  f"Conservative reservations, including uncertain calls, total **${bound:.4f}**.", "",
                  "These numbers describe the selected sets only. An AI source audit inspected all 15 final "
                  "summaries and flagged two platform inferences and two filtering ambiguities; notes appear "
                  "in the evidence index. This is not independent human validation. Smaller later scores "
                  "in these three frames do not establish a population trend or an AI effect.", "",
                  f"Recorded run: `{data['run_at']}` (UTC). Exact vectors, candidate order, rejections, "
                  "sensitivity results, prompts and token use are in [pilot.json](results/pilot.json).", "",
                  "<!-- /RESULTS -->"])
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!-- RESULTS -->.*?<!-- /RESULTS -->", "\n".join(lines), text, flags=re.S)
    path.write_text(text, encoding="utf-8")


def main():
    data = load(OUT / "pilot.json")
    if any("diversity" not in m for m in data["months"]):
        raise SystemExit("Run pilot.py analyze after completing collection first")
    worksheets(data)
    chart(data)
    report(data)
    slides(data)
    evidence(data)
    readme_results(data)
    print("Built report, slides, chart, evidence index and blank review sheets in results/.")


if __name__ == "__main__":
    main()
