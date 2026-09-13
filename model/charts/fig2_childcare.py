"""Figure 2: who funds the child care. Payor's funded share under two rules, by the payor's
income share before the order, for 1/2/3 children; plus the worked-example bars (three rules:
as the Worksheet splits it today, the section 2 gross fallback, and the section 2 primary
redline (withholding basis, the ask)). A credits-inclusive analysis line/bar (rule 3 in
childcare_post_transfer.py) was dropped from both charts 2026-09-11: it is never a proposal, and
sitting in a row of allocation rules made it read as a fourth option a task force could adopt.
It stays in net_position.py / the site calculator as a labelled analysis endpoint, not here."""
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
    return base["B_3c"], r1, r2


def main():
    los = np.linspace(0, 150_000, 61)
    fig, axs = plt.subplots(1, 3, figsize=(16, 5.7), sharey=True)
    fig.subplots_adjust(wspace=0.12, top=0.73, bottom=0.26)
    rows = []
    for ax, kids in zip(axs, (1, 2, 3)):
        pts = [(lo,) + s for lo in los if (s := shares(kids, lo))]
        x = [p[1] for p in pts]
        ax.plot(x, [p[2] for p in pts], color=P["series"][3], lw=2.2, label="As the Worksheet splits it today")
        ax.plot(x, [p[3] for p in pts], color=P["series"][0], lw=2.2, label="If split on income after the order")
        ax.plot(x, x, color=P["axis"], lw=1, ls="--")
        ax.set_title(f"{kids} child{'ren' if kids > 1 else ''}", loc="left", fontsize=11, color=P["text"])
        ax.set_xlim(0.5, 1.0); ax.set_ylim(0, 1.0)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.set_xlabel("Payor's share of combined income (before the order)")
        rows += [(kids, p[0], p[1], p[2], p[3]) for p in pts]
    axs[0].set_ylabel("Share of the child care the payor funds")
    # Anchored on axs[0] (transAxes), not fig.legend(): that makes it a child of that axes,
    # so bottom_footer's tightbbox measurement below sees it and Notes/Source land below the
    # legend row instead of on top of it (a figure-level legend is invisible to that check).
    axs[0].legend(loc="upper left", bbox_to_anchor=(0.0, -0.22), ncols=2, frameon=False)
    fig.subplots_adjust(top=top_header(fig, "Child care is split on an income distribution that base support has already changed",
        "Share of the child care bill the payor funds under two rules, by income share.",
        facts(1, "1, 2 and 3", f"\\${CC_PER_CHILD_WK:.0f}/child/wk, paid by the lower earner", f"\\${HI:,.0f} / varies")))
    bottom_footer(fig, "Dashed: funded share = income share. Child care is included in the order. " + NOTE_CONV, SOURCE_SRC)
    fig.savefig(out("fig2_childcare_rules.png"), dpi=170); fig.savefig(out("fig2_childcare_rules.svg")); plt.close(fig)
    write_csv("fig2_childcare_rules.csv", ["children", "lower_gross", "payor_3c", "rule1_current", "rule2_post_gross"], rows)

    # worked-example bars, the letter's figures (childcare_post_transfer.figures(); v4.9: rule 5 is
    # the § 2 primary redline (withholding basis), rule 2b the § 2 fallback (gross basis)). Ordered
    # by value, descending. Rule 3 (credits-inclusive) is computed by the module but not plotted here.
    import childcare_post_transfer as cpt  # noqa
    F = cpt.figures()
    r1, r2b, r5 = F["rule1_share"], F["rule2b_share"], F["rule5_share"]
    vals = [r1, r2b, r5]
    fig, ax = theme.figure(8, 4.6)
    # Plain, self-contained tick labels (owner-approved wording, 2026-09-11): the line numbers
    # and basis move to Notes, per the chart-anatomy text budget.
    labels = ["As the Worksheet\nsplits it today", "If split on income\nafter the order", "If split on\ntake-home pay"]
    theme.bars(ax, np.arange(3), vals, color=P["series"][0])
    ax.set_xticks(np.arange(3)); ax.set_xticklabels(labels)
    theme.label_ends(ax, np.arange(3), vals, fmt="{:.1%}")
    theme.finish(ax, title="The payor's share of a \\$15,600 child care bill, three ways to split it",
                 subtitle="Payor's share of the same \\$15,600 bill under three allocation rules.",
                 pct=True,
                 pairs=facts(1, 3, "\\$300/wk, paid by the recipient", "\\$201,000 / \\$29,640"),
                 notes="Fallback is new Line 6b-2, gross basis; primary redline (the ask) is new Lines 6b-1a and 6b-1, withholding basis. Two of three children under 13; premiums \\$43/\\$33.",
                 source="model/childcare_post_transfer.py")
    ax.set_ylim(0, 1)
    theme.save(fig, out("fig2_childcare_worked_example.png"))
    write_csv("fig2_childcare_worked_example.csv", ["rule", "payor_share"], list(zip(labels, vals)))
    print("fig2 written", " ".join(f"{v:.3f}" for v in vals))


if __name__ == "__main__":
    main()
