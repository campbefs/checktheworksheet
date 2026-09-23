"""Figure 13: the cost-of-living defence (2026-09-23). Two single-axes exhibits:

  E32  Massachusetts and the six places that cost more to live in: the order at equal time and at
       primary custody, side by side, costliest first.
  E33  Every jurisdiction: cost of living against the equal-time order, Massachusetts marked.

Data: model/cost_of_living.py (BEA Regional Price Parities 2024 joined to the tier-50 orders at the
worked example). Writes straight to output/charts/exhibits/, which build_public_repo.py exports."""
import os
import sys

import matplotlib.pyplot as plt
from _common import ROOT, write_csv, theme

sys.path.insert(0, ROOT)
from model import cost_of_living as col  # noqa: E402

theme.apply("light"); P = theme.P
EXHIBITS = os.path.join(ROOT, "output", "charts", "exhibits")
SHORT = {"District of Columbia": "D.C."}
PAIRS = [("Children", "3"), ("Child care", "None (base support)"), ("Incomes", "\\$201,000 / \\$29,640")]
SRC = "Cost of living: BEA Regional Price Parities 2024. Orders: the fifty-jurisdiction comparison at the worked example."


# Site colours, and a black-and-white set for the printed petition (monochrome laser).
SITE = None   # filled from the theme palette in _pal()
PRINT = dict(eq="#9a9a9a", pr="#111111", ma="#111111", dot="#8a8a8a", text2="#333333", mute="#666666")


def _pal(mode):
    if mode == "print":
        return PRINT
    return dict(eq=P["series"][0], pr=P["series"][3], ma=P["series"][1], dot=P["series"][0],
                text2=P["text_2"], mute=P["text_mute"])


def bars(path=None, mode="site"):
    c = _pal(mode)
    ma, up = col.costlier()
    rs = [ma] + up
    rs = sorted(rs, key=lambda r: r["rpp"])          # costliest at the top of a barh
    fig, ax = theme.figure(8.6, 6.4)
    fig.subplots_adjust(left=0.33, right=0.96, top=0.74, bottom=0.2)
    h = 0.36
    y = list(range(len(rs)))
    eq_c, pr_c = c["eq"], c["pr"]
    ax.barh([i + h / 2 for i in y], [r["equal"] for r in rs], height=h, color=eq_c, label="Joint custody, equal time")
    ax.barh([i - h / 2 for i in y], [r["primary"] for r in rs], height=h, color=pr_c, label="Other parent has primary custody")
    ax.axvline(ma["equal"], color=c["ma"], lw=1.4, ls=(0, (4, 3)))
    ax.text(ma["equal"] + 60, len(rs) - 0.45, "Massachusetts at equal time", fontsize=8.5,
            color=c["ma"], va="top")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_xlim(0, max(r["primary"] for r in rs) * 1.1)
    ax.set_ylim(-0.7, len(rs) - 0.3)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Monthly child support order", labelpad=8)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.13), ncols=2, frameon=False)
    f = col.facts()
    theme.finish(ax, title="Every place that costs more to live in than Massachusetts orders less at equal time",
                 subtitle="Monthly order at the same incomes, costliest place first. The number beside each name is its "
                          "cost of living; the U.S. average is 100.",
                 pairs=PAIRS,
                 notes=f"At primary custody only Hawaii orders more than Massachusetts. Massachusetts at equal time "
                       f"orders more than {f['n_costlier_primary_below_ma_equal']} of the {f['n_costlier']} costlier "
                       f"places order at primary custody.",
                 source=SRC, legend=False)
    # After finish(): it resets the axis formatters, which wiped these labels on the first draw.
    ax.set_yticks(y)
    ax.set_yticklabels([f"{SHORT.get(r['state'], r['state'])}  (cost of living {r['rpp']:.1f})" for r in rs], fontsize=9)
    for lbl, r in zip(ax.get_yticklabels(), rs):
        if r["state"] == "Massachusetts":
            lbl.set_fontweight("bold"); lbl.set_color(c["ma"])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    return theme.save(fig, path or os.path.join(EXHIBITS, "E32-costlier-states-order-less.png"))


def scatter(path=None, mode="site"):
    c = _pal(mode)
    rs = col.rows()
    ma = next(r for r in rs if r["state"] == "Massachusetts")
    fig, ax = theme.figure(8.6, 6.0)
    fig.subplots_adjust(left=0.12, right=0.96, top=0.74, bottom=0.14)
    others = [r for r in rs if r["state"] != "Massachusetts"]
    ax.scatter([r["rpp"] for r in others], [r["equal"] for r in others], s=34, color=c["dot"], alpha=0.85,
               label="Other states", zorder=2)
    ax.scatter([ma["rpp"]], [ma["equal"]], s=80, color=c["ma"], zorder=3)
    ax.annotate("Massachusetts", xy=(ma["rpp"], ma["equal"]), xytext=(ma["rpp"] - 7.5, ma["equal"] + 150),
                fontsize=9, fontweight="bold", color=c["ma"],
                arrowprops=dict(arrowstyle="-", color=c["ma"], lw=0.8))
    _, up = col.costlier()
    for r in up:
        ax.annotate(SHORT.get(r["state"], r["state"]), xy=(r["rpp"], r["equal"]), xytext=(4, -3),
                    textcoords="offset points", fontsize=8, color=c["text2"])
    ax.axvline(ma["rpp"], color=c["mute"], lw=0.8, ls=(0, (3, 3)), zorder=1)
    ax.text(ma["rpp"] + 0.3, 700, "Costlier than\nMassachusetts",
            fontsize=8, color=c["text2"], va="bottom")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_xlabel("Cost of living, 2024 (U.S. average = 100)", labelpad=8)
    ax.set_ylabel("Monthly order at equal time", labelpad=8)
    ax.set_ylim(0, max(r["equal"] for r in rs) * 1.15)
    theme.finish(ax, title="Massachusetts orders the most at equal time, and it is not the most expensive place to live",
                 subtitle="Each dot is one state: its cost of living against its equal-time order for the same family.",
                 pairs=PAIRS,
                 notes="Georgia is held out of the fifty-state comparison. Cost of living: BEA Regional Price Parities, all items.",
                 source=SRC, legend=False)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    return theme.save(fig, path or os.path.join(EXHIBITS, "E33-cost-of-living-vs-equal-time-order.png"))


def print_pair(dst):
    """Black-and-white copies for the printed petition, written into dst. Returns both paths."""
    return (bars(os.path.join(dst, "E-COL1-costlier-states-order-less.png"), mode="print"),
            scatter(os.path.join(dst, "E-COL2-cost-of-living-vs-equal-time.png"), mode="print"))


def main():
    os.makedirs(EXHIBITS, exist_ok=True)
    bars()
    scatter()
    write_csv("fig13_cost_of_living.csv", ["state", "price_level_2024", "monthly_order_equal_time",
                                           "monthly_order_primary_custody"],
              [(r["state"], r["rpp"], r["equal"], r["primary"]) for r in col.rows()])
    print("fig13 written:", col.facts())


if __name__ == "__main__":
    main()
