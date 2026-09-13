"""Figure 12: what the Worksheet's hardship test reports against what the order actually takes.

The proposed 40 percent net-pay ceiling (docs/2026-09-10-net-pay-ceilings.md, Ask A) does not
invent a threshold. Section IV.C already presumes substantial hardship at "40% or more of the
payor's available income". This figure shows what that test measures against what the payor
actually pays, one point per income combination.

Every point is one pair of incomes on the project's published three-child primary-custody grid.
The horizontal position is Line 7e, the number the Worksheet prints. The vertical position is the
same order as a share of the payor's net pay on the withholding basis. Every point sits above the
diagonal, because 7e divides by a gross-derived figure.

Data: output/charts/fig1_heatmap_3child_box2.csv, which carries both columns already.
"""
import csv
import os

import matplotlib.pyplot as plt
from _common import ROOT, out, theme, write_csv

theme.apply("light"); P = theme.P
GRID = os.path.join(ROOT, "output", "charts", "fig1_heatmap_3child_box2.csv")
THRESHOLD = 0.40


def main():
    rows = list(csv.DictReader(open(GRID)))
    e7 = [float(r["line_7e"]) for r in rows]
    net = [float(r["order_pct_payor_net"]) for r in rows]

    over = sum(n > THRESHOLD for n in net)
    flagged = sum(x > THRESHOLD for x in e7)
    blind = sum(n > THRESHOLD and x <= THRESHOLD for n, x in zip(net, e7))
    assert flagged == 0 and blind == over, (
        f"the caption assumes the test flags none of them: flagged={flagged} blind={blind} over={over}")

    fig, ax = theme.figure(8.4, 5.6)

    # The band that is the whole point: past the Guidelines' own hardship threshold on the
    # quantity the payor pays from, below it on the quantity the form measures.
    ax.axhspan(THRESHOLD, 1.0, xmin=0, xmax=1, color=P["series"][1], alpha=0.07, zorder=0)

    ax.scatter(e7, net, s=7, color=P["series"][0], alpha=0.5, linewidths=0, zorder=3)

    # Square limits, so the dashed diagonal reads as the 45 degrees it is. Held tight to the
    # data rather than run down to zero: two thirds of the panel was empty at 10 percent.
    lo, hi = 0.20, max(max(net), THRESHOLD) * 1.06
    ax.plot([lo, hi], [lo, hi], color=P["axis"], lw=0.9, ls=(0, (4, 3)), zorder=2)
    ax.axhline(THRESHOLD, color=P["series"][1], lw=1.2, zorder=4)
    ax.axvline(THRESHOLD, color=P["series"][1], lw=1.2, ls=(0, (2, 2)), zorder=4)

    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v*100:.0f}%"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v*100:.0f}%"))
    ax.set_aspect("equal", adjustable="box")

    theme.annotate(ax, f"{over:,} of {len(rows):,} combinations\nsit in this band",
                   xy=(0.305, THRESHOLD + 0.022), xytext=(0.212, hi - 0.030))
    theme.annotate(ax, "Line 7e never reaches\nthe same threshold",
                   xy=(THRESHOLD, 0.272), xytext=(0.288, 0.222))

    theme.finish(
        ax,
        title=(f"The order passes 40 percent of net pay in {over:,} of {len(rows):,} "
               "income combinations"),
        subtitle="The Worksheet's own hardship test flags none of them. Each dot is one pair of incomes.",
        xlabel="Line 7e: order as a share of Line 3a available income",
        ylabel="Order as a share of the payor's net pay",
        comma=False,
        pairs=[("Custody", "Primary custody (Box 2)"), ("Children", "3"),
               ("Child care", "None (base support)"),
               ("Incomes", "Higher \\$60,000-\\$300,000, lower \\$0-\\$120,000")],
        notes=("Net is the withholding basis: gross less federal income tax at the single filing "
               "status with the standard deduction, Social Security and Medicare, and Massachusetts "
               "income tax. The dashed diagonal is where the two measures would agree."),
        source="output/charts/fig1_heatmap_3child_box2.csv",
    )
    theme.save(fig, out("fig12_net_pay_ceiling.png"))
    write_csv("fig12_net_pay_ceiling.csv",
              ["higher_gross", "lower_gross", "line_7e", "order_pct_payor_net", "over_40pct_of_net"],
              [(r["higher_gross"], r["lower_gross"], r["line_7e"], r["order_pct_payor_net"],
                int(float(r["order_pct_payor_net"]) > THRESHOLD)) for r in rows])
    print(f"fig12 written: {over} of {len(rows)} cells over {THRESHOLD:.0%} of net; "
          f"Line 7e over {THRESHOLD:.0%} in {flagged}; largest lag "
          f"{max(n - x for n, x in zip(net, e7))*100:.1f} points")


if __name__ == "__main__":
    main()
