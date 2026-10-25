"""Export pilot evidence, a diagnostic chart and blank validation worksheets."""

import csv
from itertools import combinations

from pilot import ROOT, SEED, digest, load
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = ROOT / "results"
NAVY = "#142D4E"
TEAL = "#087E8B"


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


def main():
    data = load(OUT / "pilot.json")
    if any("diversity" not in m for m in data["months"]):
        raise SystemExit("Run pilot.py analyze after collection first")
    worksheets(data)
    chart(data)
    evidence(data)
    print("Exported pilot chart, evidence index and blank review sheets.")


if __name__ == "__main__":
    main()
