"""Figure 2: who funds the child care. Payor's funded share under three allocation rules, by the
payor's pre-transfer income share, for 1/2/3 children; plus the worked-example bars (88 / 64 / 48)."""
import numpy as np
import matplotlib.pyplot as plt
from _common import order, npos, write_csv, out, theme, SOURCE_SRC, NOTE_CONV, KIDS_UNDER_13, EXAMPLE, facts, top_header, bottom_footer

theme.apply("light"); P = theme.P
HI = EXAMPLE["payor"]
CC_PER_CHILD_WK = 100.0


def shares(kids, lo):
    cc = CC_PER_CHILD_WK * kids
    base = order(HI, lo, kids, 1)
    with_cc = order(HI, lo, kids, 1, cc_lo_total=cc)
    if base["payor"] != "B" or with_cc["payor"] != "B":
        return None
    r1 = (with_cc["7d"] - base["7d"]) * 52 / (cc * 52)
    b = base["7d"] * 52
    r2 = (HI - b) / ((HI - b) + (lo + b))
    pos = npos.analyze(HI, lo, kids, base["7d"], 0.0, 0.0, kids_under_13=KIDS_UNDER_13)
    r3 = pos["payor_after_share"]
    return base["B_3c"], r1, r2, r3


def main():
    los = np.linspace(0, 150_000, 61)
    fig, axs = plt.subplots(1, 3, figsize=(16, 5.4), sharey=True)
    fig.subplots_adjust(wspace=0.12, top=0.71, bottom=0.22)
    rows = []
    for ax, kids in zip(axs, (1, 2, 3)):
        pts = [(lo,) + s for lo in los if (s := shares(kids, lo))]
        x = [p[1] for p in pts]
        ax.plot(x, [p[2] for p in pts], color=P["series"][3], lw=2.2, label="Current: Line 3c, pre-transfer")
        ax.plot(x, [p[3] for p in pts], color=P["series"][0], lw=2.2, label="Post-transfer gross shares")
        ax.plot(x, [p[4] for p in pts], color=P["series"][2], lw=2.2, label="Post-transfer net shares")
        ax.plot(x, x, color=P["axis"], lw=1, ls="--")
        ax.set_title(f"{kids} child{'ren' if kids > 1 else ''}", loc="left", fontsize=11, color=P["text"])
        ax.set_xlim(0.5, 1.0); ax.set_ylim(0, 1.0)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.set_xlabel("Payor's share of combined available income (Line 3c)")
        rows += [(kids, p[0], p[1], p[2], p[3], p[4]) for p in pts]
    axs[0].set_ylabel("Share of the child care the payor funds")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower left", bbox_to_anchor=(0.06, 0.02), ncols=3, frameon=False)
    fig.subplots_adjust(top=top_header(fig, "Child care is split on an income distribution that base support has already changed",
        "Share of the child care bill the payor funds under three rules, by income share.",
        facts(1, "1, 2 and 3", f"\\${CC_PER_CHILD_WK:.0f}/child/wk, paid by the lower earner", f"\\${HI:,.0f} / varies")))
    bottom_footer(fig, "Dashed: funded share = income share. Child care is included in the order. " + NOTE_CONV, SOURCE_SRC)
    fig.savefig(out("fig2_childcare_rules.png"), dpi=170); fig.savefig(out("fig2_childcare_rules.svg")); plt.close(fig)
    write_csv("fig2_childcare_rules.csv", ["children", "lower_gross", "payor_3c", "rule1_current", "rule2_post_gross", "rule3_post_net"], rows)

    # worked-example bars, the letter's figures (childcare_post_transfer.figures(); v4.9: rule 5 is
    # the § 2 primary redline (withholding basis), rule 2b the § 2 fallback (gross basis), rule 3 the
    # credits-inclusive analysis the comments do not ask for). Ordered by value, descending.
    import childcare_post_transfer as cpt  # noqa
    F = cpt.figures()
    r1, r2b, r5, r3 = F["rule1_share"], F["rule2b_share"], F["rule5_share"], F["rule3_share"]
    vals = [r1, r2b, r5, r3]
    fig, ax = theme.figure(8, 4.6)
    # Short, one-line ticks: the line numbers and basis move to Notes, per the chart-anatomy
    # text budget (a two-line tick ending in a long parenthetical overlaps its neighbour once
    # there are four bars instead of three).
    labels = ["Worksheet today", "§ 2 fallback", "§ 2 primary redline", "Credits-inclusive"]
    theme.bars(ax, np.arange(4), vals, color=P["series"][0])
    ax.set_xticks(np.arange(4)); ax.set_xticklabels(labels)
    theme.label_ends(ax, np.arange(4), vals, fmt="{:.1%}")
    theme.finish(ax, title="The payor's share of a \\$15,600 child care bill, four ways to split it",
                 subtitle="Payor's share of the same \\$15,600 bill under four allocation rules.",
                 pct=True,
                 pairs=facts(1, 3, "\\$300/wk, paid by the recipient", "\\$201,000 / \\$29,640"),
                 notes="Fallback is new Line 6b-2, gross basis; primary redline is new Lines 6b-1a and 6b-1, withholding basis. Last bar counts refundable credits, not proposed. Two of three children under 13; premiums \\$43/\\$33.",
                 source="model/childcare_post_transfer.py")
    ax.set_ylim(0, 1)
    theme.save(fig, out("fig2_childcare_worked_example.png"))
    write_csv("fig2_childcare_worked_example.csv", ["rule", "payor_share"], list(zip(labels, vals)))
    print("fig2 written", " ".join(f"{v:.3f}" for v in vals))


if __name__ == "__main__":
    main()
