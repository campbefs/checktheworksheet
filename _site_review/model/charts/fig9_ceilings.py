"""Figure 9: where each state's presumptive schedule stops. Massachusetts applies its formula to
$450,000 of combined available income; most combined-income schedules stop lower. States with no
combined-income ceiling (percentage-of-obligor, Melson, open formula) are listed, not ranked.
Data: data/fifty-state/ceilings-2026-09-06.json (hand-completed from the verified run's profiles
and the local primary documents)."""
import json
import os
import matplotlib.pyplot as plt
from _common import ROOT, write_csv, out, theme

theme.apply("light"); P = theme.P
DATA = os.path.join(ROOT, "data", "fifty-state", "ceilings-2026-09-06.json")


def main():
    rows = json.load(open(DATA))
    ranked = sorted([r for r in rows if r["category"] == "combined-ceiling" and r["annual_ceiling"]],
                    key=lambda r: r["annual_ceiling"])
    others = [r for r in rows if r["category"] != "combined-ceiling" or not r["annual_ceiling"]]
    n_gross = sum(r["basis"] == "gross" for r in ranked)
    n_net = sum(r["basis"] == "net" for r in ranked)
    fig, ax = theme.figure(9, 0.24 * len(ranked) + 1.5)
    fig.subplots_adjust(left=0.24, right=0.97, bottom=0.06, top=0.92)
    y = range(len(ranked))
    colors = [P["series"][1] if r["state"] == "Massachusetts" else (P["series"][0] if r["basis"] == "gross" else P["series"][2])
              for r in ranked]
    ax.barh(list(y), [r["annual_ceiling"] for r in ranked], color=colors, height=0.62)
    ax.set_yticks(list(y)); ax.set_yticklabels([r["state"] for r in ranked], fontsize=8.5)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v / 1000:,.0f}k"))
    ax.set_ylim(-0.6, len(ranked) - 0.4)
    ax.grid(axis="y", visible=False)
    ma = next(r for r in ranked if r["state"] == "Massachusetts")
    ax.text(ma["annual_ceiling"] + 6000, ranked.index(ma), f"${ma['annual_ceiling']:,.0f}", va="center", fontsize=8.5, color=P["text_2"])
    # legend proxies for the basis colours
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=P["series"][0], label="Gross-income schedule"), Patch(color=P["series"][2], label="Net-income schedule"),
                       Patch(color=P["series"][1], label="Massachusetts (gross)")],
              loc="lower right", frameon=False, fontsize=9)
    rank = len(ranked) - ranked.index(ma)
    above = [r["state"] for r in ranked if r["annual_ceiling"] > ma["annual_ceiling"]]
    import statistics
    med = statistics.median([r["annual_ceiling"] for r in ranked])
    at480 = sum(r["annual_ceiling"] == 480_000 for r in ranked)
    theme.finish(ax, title=f"Massachusetts's presumptive formula runs to \\$450,000; {len(above)} schedules run higher, {len(ranked) - len(above) - 1} stop lower",
                 subtitle="Combined income at which each state's presumptive schedule ends; above it, support is discretionary.",
                 comma=False, legend=False,
                 pairs=[("Ranked", f"{len(ranked)} combined-income schedules ({n_gross} gross, {n_net} net)"),
                        ("Not ranked", f"{len(others)}: percentage-of-obligor, Melson or open formula"),
                        ("Basis", "Annual; monthly ×12, weekly ×52")],
                 notes=f"Median of the {len(ranked)}: \\${med:,.0f}; {at480} stop at exactly \\$40,000 a month. Net-income ceilings are not dollar-for-dollar "
                       "comparable with gross ones. Not ranked: " + ", ".join(sorted(r["state"] for r in others)) + ".",
                 source="data/fifty-state/ceilings-2026-09-06.json (verified-run profiles completed from local primary documents)")
    theme.save(fig, out("fig9_schedule_ceilings.png"))
    write_csv("fig9_schedule_ceilings.csv", ["state", "category", "annual_ceiling", "basis", "confidence", "brattle_fig34"],
              [(r["state"], r["category"], r["annual_ceiling"], r["basis"], r.get("confidence"), r.get("brattle_fig34")) for r in rows])
    print("fig9 written", len(ranked), "ranked;", len(above), "above MA:", above)


if __name__ == "__main__":
    main()
