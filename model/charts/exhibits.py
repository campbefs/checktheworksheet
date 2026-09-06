"""The exhibit set: one chart per file, named E<nn>-<what>-<scope>.png, in output/charts/exhibits/.

Follows docs/2026-09-05-chart-exhibit-guide.md. Multi-panel working figures stay where they are;
each panel that the guide rates becomes its own exhibit here. Single-panel figures are COPIED under
their exhibit name (the originals are never moved). Heatmap exhibits are drawn from the CSVs the
working figures wrote, so an exhibit and its figure can never disagree.

Run after make_all.py's figures: .venv/bin/python model/charts/exhibits.py"""
import csv
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from _common import out, theme, EXAMPLE, SOURCE_SRC, NOTE_CONV, NOTE_MASK, facts, top_header, bottom_footer

theme.apply("light"); P = theme.P
DIV = plt.matplotlib.colors.LinearSegmentedColormap.from_list("div", [P["div_low"], P["div_mid"], P["div_high"]])
SEQ = plt.matplotlib.colors.LinearSegmentedColormap.from_list("seq", P["seq"])
EX = os.path.join(os.path.dirname(out("x")), "exhibits")
os.makedirs(EX, exist_ok=True)


def ex(name):
    return os.path.join(EX, name)


def read_csv(name):
    with open(out(name)) as f:
        rd = csv.DictReader(f)
        return [{k: (float(v) if v not in ("", None) else np.nan) for k, v in row.items()} for row in rd]


def to_grid(rows, key):
    hi = np.array(sorted({r["higher_gross"] for r in rows}))
    lo = np.array(sorted({r["lower_gross"] for r in rows}))
    Z = np.full((len(lo), len(hi)), np.nan)
    ih = {v: j for j, v in enumerate(hi)}; il = {v: i for i, v in enumerate(lo)}
    for r in rows:
        Z[il[r["lower_gross"]], ih[r["higher_gross"]]] = r[key]
    H, L = np.meshgrid(hi, lo)
    return H, L, Z


def title_block(fig, title, subtitle, pairs=None, notes="", source=SOURCE_SRC):
    fig.subplots_adjust(top=top_header(fig, title, subtitle, pairs, panel_gap_pt=14))
    bottom_footer(fig, notes, source)


def heat(fname, rows, key, title, subtitle, diverging=True, contour=0.0, pct=False, vmax=None, contour_label="even",
         pairs=None, notes=""):
    H, L, Z = to_grid(rows, key)
    fig, ax = plt.subplots(figsize=(8.6, 6.8))
    fig.subplots_adjust(bottom=0.15, left=0.11, right=0.97)
    if diverging:
        lim = np.nanmax(np.abs(Z))
        im = ax.pcolormesh(H, L, Z, cmap=DIV, norm=TwoSlopeNorm(0, -lim, lim), shading="nearest")
    else:
        im = ax.pcolormesh(H, L, Z, cmap=SEQ, shading="nearest", vmin=0, vmax=vmax)
    cs = ax.contour(H, L, Z, levels=[contour], colors=[P["text"]], linewidths=1.4)
    ax.clabel(cs, fmt=(lambda v: f"{v:.0%}") if pct else (lambda v: contour_label), fontsize=8.5)
    cb = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.02)
    cb.ax.yaxis.set_major_formatter(plt.FuncFormatter((lambda v, _: f"{v:.0%}") if pct else (lambda v, _: f"{v / 1000:+,.0f}k")))
    cb.outline.set_visible(False)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v / 1000:.0f}k"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v / 1000:.0f}k"))
    ax.set_xlabel("Higher earner, gross per year"); ax.set_ylabel("Lower earner, gross per year")
    ax.plot(EXAMPLE["payor"], EXAMPLE["recip"], marker="o", ms=7, mfc="none", mec=P["text"], mew=1.6)
    ax.annotate("worked example", (EXAMPLE["payor"], EXAMPLE["recip"]), xytext=(8, 8), textcoords="offset points", fontsize=8.5, color=P["text"])
    ax.grid(False)
    title_block(fig, title, subtitle, pairs, notes)
    fig.savefig(ex(fname), dpi=170); plt.close(fig)
    print(fname)


def copy(src, dst):
    shutil.copyfile(out(src), ex(dst)); print(dst, "(copy of", src + ")")


def main():
    # --- E01–E04 from the 3-child Box 1 grid ---
    g3 = read_csv("fig1_heatmap_3child_box1.csv")
    F3 = facts(1, 3)
    heat("E01-who-holds-more-3-children.png", g3, "gap_household",
         "The recipient household holds more below about \\$230k of higher-earner income; the payor above it",
         "Recipient household net minus payor net, per year.", pairs=F3,
         notes="Recipient ahead in 55% of cells. The inner 'even' loop is Line 6e's limit ending at 6d = 10%: the order "
               "drops ~\\$110/wk in one step. " + NOTE_MASK + NOTE_CONV)
    heat("E02-who-holds-more-per-person-3-children.png", g3, "gap_per_person",
         "Per person, the payor holds more almost everywhere",
         "Recipient household net ÷ 4, minus payor net. Companion to E01.", pairs=F3,
         notes="Payor ahead in 99% of cells. " + NOTE_MASK + NOTE_CONV)
    heat("E04-order-as-share-of-payor-net-3-children.png", g3, "order_pct_payor_net",
         "The order tops 40% of the payor's net only when the lower earner makes under about \\$25,000",
         "Order as a share of payor net; line at 40%.", diverging=False, contour=0.40, pct=True, vmax=0.60, pairs=F3,
         notes="15% of cells. Scale fixed 0–60%. " + NOTE_MASK + NOTE_CONV)
    copy("fig1_headline_household_gap.png", "E03-children-decide-who-holds-more-1-2-3.png")

    # --- E05–E07 ---
    copy("fig6_valve_units_lag.png", "E05-what-line-7e-sees-vs-true-burden-worked-example.png")
    copy("fig2_childcare_worked_example.png", "E06-child-care-share-three-rules-worked-example.png")
    copy("fig2_childcare_rules.png", "E07-child-care-rules-across-incomes-1-2-3.png")

    # --- E08 / E09 from fig3's CSV ---
    r3 = read_csv("fig3_credit_collapse.csv")
    r3.sort(key=lambda r: r["payor_3c"])
    x = [r["payor_3c"] for r in r3]

    fig, ax = theme.figure(9.5, 5.2)
    ax.plot(x, [r["reduction_current"] for r in r3], color=P["series"][3], lw=2.2, label="Worksheet today (Box 1 vs Box 2)")
    ax.plot(x, [r["reduction_A"] for r in r3], color=P["series"][0], lw=2.2, label="Variant A: Line 6e applied once")
    ax.plot(x, [r["reduction_B"] for r in r3], color=P["series"][2], lw=2.2, label="Variant B: cross-credit, factor 1.5")
    ax.set_xlim(0.5, 1.0); ax.set_ylim(0, 1)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.axvline(0.877, color=P["text_mute"], lw=0.8); ax.text(0.879, 0.93, "worked\nexample", fontsize=8, color=P["text_mute"])
    theme.finish(ax, title="The equal-time credit collapses with the income gap; a cross-credit only narrows",
                 subtitle="Reduction in the order for equal time vs the one-third-time (Box 2) order.",
                 xlabel="Payor's share of combined available income (Line 3c)", ylabel="Reduction vs the ⅓-time order", pct=True,
                 pairs=facts("1v2", 3, "None (base support)", f"\\${EXAMPLE['payor']:,.0f} / varies"),
                 notes="Variants A and B: the letter's § 5 redlines (box1_fix.py). " + NOTE_CONV,
                 source=SOURCE_SRC)
    theme.save(fig, ex("E08-credit-shrinks-as-gap-widens-3-children.png")); print("E08")

    fig, ax = theme.figure(9.5, 5.2)
    ax.plot(x, [r["implied_share_1.5"] for r in r3], color=P["series"][2], lw=2.2, label="Duplication factor 1.5 (Indiana; Variant B)")
    ax.plot(x, [r["implied_share_2.0"] for r in r3], color=P["series"][1], lw=2.2, label="Duplication factor 2.0 (Box 1's own structure)")
    ax.axhline(0.5, color=P["axis"], lw=1, ls="--"); ax.text(0.51, 0.51, "actual: 50% of overnights", fontsize=8.5, color=P["text_2"])
    ax.set_xlim(0.5, 1.0); ax.set_ylim(0, 0.6)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.axvline(0.877, color=P["text_mute"], lw=0.8); ax.text(0.879, 0.56, "worked\nexample", fontsize=8, color=P["text_mute"])
    theme.finish(ax, title="Equal time is priced as a third of overnights at factor 1.5, and 47% at factor 2.0",
                 subtitle="Overnight share that reproduces the Box 1 order under a cross-credit.",
                 xlabel="Payor's share of combined available income (Line 3c)", ylabel="Implied payor overnight share", pct=True,
                 pairs=facts(1, 3, "None (base support)", f"\\${EXAMPLE['payor']:,.0f} / varies"),
                 notes="Blank below the Line 5c floor. State the factor with the number. " + NOTE_CONV,
                 source=SOURCE_SRC + "; box1_fix.py")
    theme.save(fig, ex("E09-implied-overnight-share-by-factor-3-children.png")); print("E09")

    # --- E10–E15 ---
    copy("fig4_marginal_retention.png", "E10-cents-kept-of-next-dollar-worked-example.png")
    copy("fig5a_states_S1.png", "E11-fifty-states-equal-parenting-one-fact-pattern.png")
    copy("fig5b_states_S2.png", "E12-fifty-states-lower-earner-primary-one-fact-pattern.png")
    copy("fig5c_credit_at_122_tilemap.png", "E13-credit-at-122-overnights-28-of-51.png")
    copy("fig7_box3_inversion.png", "E14-split-siblings-lower-order-higher-cost-2-children.png")
    copy("fig8_both_pay.png", "E15-both-parents-pay-child-care-payor-bears-93pct.png")
    copy("fig9_schedule_ceilings.png", "E16-where-each-presumptive-schedule-stops-51.png")
    copy("fig10_ma_shared_vs_primary.png", "E17-ma-equal-time-vs-others-primary-custody.png")

    with open(ex("README.md"), "w") as f:
        f.write("# Exhibit set — one chart per file\n\n")
        f.write("Built by `model/charts/exhibits.py` from the working figures in `output/charts/` (never edit these by hand; rebuild). "
                "Naming and ratings: `docs/2026-09-05-chart-exhibit-guide.md`. Heatmap exhibits E01/E02/E04 are drawn from "
                "`fig1_heatmap_3child_box1.csv`; E08/E09 from `fig3_credit_collapse.csv`; the rest are copies of single-panel figures.\n\n")
        f.write("The per-person exhibit (E02) travels with E01. The fifty-state exhibits are at one fact pattern. "
                "E09 states its duplication factor in the title. Generic grids set the MA under-13 credit to zero.\n\n")
        for n in sorted(os.listdir(EX)):
            if n.endswith(".png"):
                f.write(f"- `{n}`\n")
    print("exhibits README written")


if __name__ == "__main__":
    main()
