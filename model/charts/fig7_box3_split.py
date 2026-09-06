"""Figure 7: splitting siblings lowers the order while raising the cost the schedule itself assumes.

Two children. Box 1 (both shared, equal time) against Box 3 (one child residing primarily with each
parent). The payor's care responsibility is one child-share either way. Line 6g nets the two columns
on the one-child schedule, so the Box 3 order is Table B(1)/Table B(2) = 71.4% of the Box 1 order,
while two homes each carrying a first child cost 2.00 on Table B against 1.40 in one home.
Letter § 5.1; `submission_figures.py` section 5.1."""
import numpy as np
import matplotlib.pyplot as plt
from _common import w, write_csv, out, theme, SOURCE_SRC, NOTE_CONV, EXAMPLE, HEALTH_LO, HEALTH_HI, facts, top_header, bottom_footer

theme.apply("light"); P = theme.P
HI = EXAMPLE["payor"]; KIDS = 2


def main():
    kk = dict(b_gross=HI / 52, children_under18=KIDS, a_health=HEALTH_LO, b_health=HEALTH_HI)
    rows = []
    for lo in np.linspace(2_000, 150_000, 75):
        b1 = w.run(box=1, a_gross=lo / 52, **kk)
        b3 = w.run(box=3, a_gross=lo / 52, a_children=(1, 0), b_children=(1, 0), **kk)
        if b1["payor"] != "B" or b3["payor"] != "B":
            continue
        rows.append((lo, b1["B_3c"], b1["7d"], b3["7d"], 1 - b3["7d"] / b1["7d"]))
    rows.sort(key=lambda r: r[1])
    x = [r[1] for r in rows]

    # worked-example incomes, two children (the letter's § 5.1 pair)
    e1 = w.run(box=1, a_gross=EXAMPLE["recip"] / 52, **kk)
    e3 = w.run(box=3, a_gross=EXAMPLE["recip"] / 52, a_children=(1, 0), b_children=(1, 0), **kk)
    ex_share, ex_b1, ex_b3 = e1["B_3c"], e1["7d"], e3["7d"]
    factor_one_home, factor_two_homes = w.TABLE_B[2], 2 * w.TABLE_B[1]

    fig, axs = plt.subplots(1, 2, figsize=(14, 5.4), gridspec_kw=dict(width_ratios=[1.7, 1]))
    fig.subplots_adjust(wspace=0.30, top=0.71, bottom=0.22)
    ax = axs[0]
    ax.plot(x, [r[2] for r in rows], color=P["series"][0], lw=2.2, label="Box 1: both children shared, equal time")
    ax.plot(x, [r[3] for r in rows], color=P["series"][1], lw=2.2, label="Box 3: one child residing primarily with each parent")
    ax.axvline(ex_share, color=P["text_mute"], lw=0.8)
    ax.text(ex_share - 0.005, ax.get_ylim()[1] * 0.02 + 40, "worked\nexample", fontsize=8, color=P["text_mute"], ha="right")
    ax.annotate(f"${ex_b1:,.0f}/wk", (ex_share, ex_b1), xytext=(-60, 10), textcoords="offset points", fontsize=9, color=P["text_2"])
    ax.annotate(f"${ex_b3:,.0f}/wk  ({1 - ex_b3 / ex_b1:.1%} lower)", (ex_share, ex_b3), xytext=(6, -28), textcoords="offset points", fontsize=9, color=P["text_2"])
    ax.set_xlim(0.5, 1.0)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_xlabel("Payor's share of combined available income (Line 3c)")
    ax.set_ylabel("Weekly order, Line 7d")
    ax.set_title("(a) Weekly order", loc="left", fontsize=10.5)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.16), ncols=1, frameon=False, fontsize=9)

    ax = axs[1]
    labels = ["One home,\ntwo children\n(Table B ×1.40)", "Two homes,\none child each\n(Table B ×1.00, twice)"]
    vals = [factor_one_home, factor_two_homes]
    theme.bars(ax, np.arange(2), vals, color=P["series"][3])
    ax.set_xticks(np.arange(2)); ax.set_xticklabels(labels, fontsize=9)
    theme.label_ends(ax, np.arange(2), vals, fmt="{:.2f}×")
    ax.set_ylim(0, 2.4); ax.set_ylabel("Multiple of the one-child schedule amount")
    ax.set_title("(b) Table B cost multiple", loc="left", fontsize=10.5)

    fig.subplots_adjust(top=top_header(fig, "Splitting the siblings cuts the order by a third while the schedule's own cost rises 43%",
        "Weekly order under Box 1 and Box 3 for the same two children, and Table B's cost of each.",
        facts("1v3", 2, "None (base support)", f"\\${HI:,.0f} / varies")))
    bottom_footer(fig, f"Box 3 = Table B(1)/B(2) = {w.TABLE_B[1] / w.TABLE_B[2]:.1%} of Box 1. Cuts against the lower earner. "
                  "Letter § 5.1. " + NOTE_CONV, SOURCE_SRC)
    fig.savefig(out("fig7_box3_inversion.png"), dpi=170); fig.savefig(out("fig7_box3_inversion.svg")); plt.close(fig)
    write_csv("fig7_box3_inversion.csv", ["lower_gross", "payor_3c", "box1_7d", "box3_7d", "box3_reduction"], rows)
    write_csv("fig7_box3_inversion_example.csv", ["item", "value"],
              [("payor_3c", ex_share), ("box1_7d", ex_b1), ("box3_7d", ex_b3), ("reduction", 1 - ex_b3 / ex_b1),
               ("tableB_one_home_two_children", factor_one_home), ("tableB_two_homes_one_each", factor_two_homes)])
    print("fig7 written", f"{ex_b1:.2f} {ex_b3:.2f} {1 - ex_b3 / ex_b1:.3f}")


if __name__ == "__main__":
    main()
