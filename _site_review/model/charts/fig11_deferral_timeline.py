"""Figure 11: how many times the gross-versus-net income question was deferred.

Built ONLY from data/deferrals-gross-vs-net.json, itself built by grepping the primary texts in
data/extracted/*.flow.txt (the 2025 Guidelines with embedded 2017/2018/2021/2023/2025 commentary,
the Brattle Economic Review, the Task Force report) for "gross", "net income", "next quadrennial",
"next task force", "at this time", "again in this review", "prior task forces". A cycle is marked
DEFERRED only where the corpus holds a verbatim quote deferring the gross-vs-net question specifically;
otherwise NO RECORD IN CORPUS. Never inferred from silence, and never from a later cycle's own claim
about "prior task forces" without that prior cycle's own text in the corpus."""
import json
import os
import matplotlib.pyplot as plt
from _common import ROOT, write_csv, out, theme, facts

theme.apply("light"); P = theme.P
DATA = os.path.join(ROOT, "data", "deferrals-gross-vs-net.json")


def main():
    d = json.load(open(DATA))
    cycles = sorted(d["cycles"], key=lambda r: r["year"])
    n_deferred = sum(1 for r in cycles if r["status"] == "DEFERRED")
    n_total = len(cycles)

    fig, ax = theme.figure(9.5, 4.6)
    fig.subplots_adjust(bottom=0.05, top=0.78)
    xs = [r["year"] for r in cycles]
    ax.axhline(0, color=P["axis"], lw=1.2, zorder=1)

    for i, (x, r) in enumerate(zip(xs, cycles)):
        up = 1 if i % 2 == 0 else -1
        deferred = r["status"] == "DEFERRED"
        color = P["series"][1] if deferred else P["text_mute"]
        ax.plot([x, x], [0, up], color=color, lw=1.2, zorder=2)
        ax.plot([x], [up], marker="o", ms=11, mfc=(color if deferred else "none"), mec=color, mew=1.8, zorder=3)
        va = "bottom" if up > 0 else "top"
        ax.annotate(f"{r['label']}\n{r['status']}", (x, up), xytext=(0, 8 if up > 0 else -8),
                    textcoords="offset points", ha="center", va=va, fontsize=8.7,
                    color=(P["text"] if deferred else P["text_mute"]),
                    fontweight="bold" if deferred else "normal")

    ax.set_xlim(2016, 2027)
    ax.set_ylim(-2.1, 2.1)
    ax.set_xticks(xs)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.get_yaxis().set_visible(False)
    for spine in ("left", "top", "right"):
        ax.spines[spine].set_visible(False)
    ax.grid(False)

    theme.finish(ax, title=f"Gross versus net was deferred in {n_deferred} of {n_total} documented guidelines cycles, 2017–2025",
                 subtitle="Each Massachusetts guidelines edition or amendment; filled = deferred on the record, hollow = no record in the corpus.",
                 comma=False, legend=False,
                 pairs=[("Question", "Gross vs. net income basis (not the separate alimony/tax question)"),
                        ("Corpus", "2025 Guidelines + embedded commentary, Brattle Econ. Review, Task Force report"),
                        ("Cycles", f"{n_total}, 2017–2025")],
                 notes="Only 2025 has a verbatim deferral; 2025's own text says prior task forces did the same, but their primary text is not "
                       "in this corpus, so 2017/2018/2021/2023 are marked no record, not deferred. Econreview also states the next review is expected 2029.",
                 source="data/deferrals-gross-vs-net.json (data/extracted/*.flow.txt)")
    theme.save(fig, out("fig11_deferral_timeline.png"))
    write_csv("fig11_deferral_timeline.csv", ["year", "label", "kind", "status", "document", "quote"],
              [(r["year"], r["label"], r["kind"], r["status"], r.get("document") or "", (r.get("quote") or "").replace("\n", " ")) for r in cycles])
    print("fig11 written:", f"{n_deferred} of {n_total} deferred")


if __name__ == "__main__":
    main()
