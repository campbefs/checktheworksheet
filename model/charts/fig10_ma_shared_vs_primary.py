"""Figure 10: Massachusetts's EQUAL-TIME order (Box 1, S1) against every other jurisdiction's
PRIMARY-CUSTODY order (S2), one fact pattern. The question: how does an equal-time order in Massachusetts compare with primary-custody orders elsewhere? Data: tier-50 rows (Georgia held out)."""
import json
import os
import matplotlib.pyplot as plt
from _common import ROOT, write_csv, out, theme

theme.apply("light"); P = theme.P
DATA = os.path.join(ROOT, "data", "fifty-state", "tier-50-2026-09-05.json")


def main():
    tier = json.load(open(DATA))
    ma = next(r for r in tier if r["state"] == "Massachusetts")
    rows = [dict(state=r["state"], value=r["s2"], custody="primary") for r in tier if r["state"] != "Massachusetts"]
    rows.append(dict(state="Massachusetts", value=ma["s1"], custody="equal"))
    rows.sort(key=lambda r: r["value"])
    others = [r for r in rows if r["custody"] == "primary"]
    below = sum(r["value"] < ma["s1"] for r in others)
    above = [r["state"] for r in others if r["value"] > ma["s1"]]
    rank = len(rows) - rows.index(next(r for r in rows if r["custody"] == "equal"))

    fig, ax = theme.figure(9, 10)
    fig.subplots_adjust(bottom=0.05, top=0.90)
    y = list(range(len(rows)))
    colors = [P["series"][1] if r["custody"] == "equal" else P["series"][0] for r in rows]
    ax.barh(y, [r["value"] for r in rows], color=colors, height=0.62)
    ax.set_yticks(y)
    ax.set_yticklabels([("Massachusetts, EQUAL time" if r["custody"] == "equal" else r["state"]) for r in rows], fontsize=8.5)
    for lbl, r in zip(ax.get_yticklabels(), rows):
        if r["custody"] == "equal":
            lbl.set_fontweight("bold"); lbl.set_color(P["series"][1])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_ylim(-0.6, len(rows) - 0.4)
    # Same formula as fig5_states.py's pair_xmax (E12): the lead pair E12/E17 shares one x-axis
    # range. Do not change one without the other.
    ax.set_xlim(0, max(max(r["value"] for r in rows), ma["s1"]) * 1.08)
    ax.grid(axis="y", visible=False)
    # one annotation: MA's own primary-custody order, for scale
    yi = rows.index(next(r for r in rows if r["custody"] == "equal"))
    ax.plot([ma["s2"]], [yi], marker="|", markersize=14, color=P["text"], lw=0)
    ax.annotate(f"MA primary: ${ma['s2']:,.0f}", xy=(ma["s2"], yi), xytext=(ma["s2"] + 120, yi - 2.2),
                fontsize=8.5, color=P["text_2"], arrowprops=dict(arrowstyle="-", color=P["text_2"], lw=0.6))
    theme.finish(ax, title=f"Massachusetts's equal-time order exceeds the primary-custody order of {below} of the {len(others)} others",
                 subtitle="Second of a pair with E12: same states, same axis, Massachusetts's Box 1 equal-time order takes the place of its own primary-custody bar.",
                 comma=False,
                 pairs=[("Custody", "MA equal time (Box 1) vs others primary"), ("Children", "3"),
                        ("Child care", "None (base support)"), ("Incomes", "\\$201,000 / \\$29,640")],
                 notes=f"One fact pattern. Georgia held out. Above Massachusetts: {', '.join(above) or 'none'}. Each row profiled from primary sources, "
                       "computed twice blind, reconciled, attacked. Own premiums \\$43/\\$33 as each state treats them.",
                 source="data/fifty-state/tier-50-2026-09-05.json")
    theme.save(fig, out("fig10_ma_shared_vs_primary.png"))
    write_csv("fig10_ma_shared_vs_primary.csv", ["state", "custody", "monthly_order"],
              [(r["state"], r["custody"], r["value"]) for r in rows] + [("Massachusetts", "primary (reference)", ma["s2"])])
    print(f"fig10 written: MA S1 ${ma['s1']:,.2f} rank {rank} of {len(rows)}; above MA: {above}; MA S2 ${ma['s2']:,.2f}")


if __name__ == "__main__":
    main()
