"""The exhibit set: one chart per file, named E<nn>-<what>-<scope>.png, in output/charts/exhibits/.

Follows docs/2026-09-05-chart-exhibit-guide.md and the 2026-09-06 exhibit direction
(docs/plans/2026-09-06-exhibit-direction.md): ONE EXHIBIT, ONE GRAPH. No multi-panel exhibits.
Multi-panel working figures (fig1_headline_household_gap, fig2_childcare_rules, fig7_box3_inversion,
fig8_both_pay) stay in output/charts/ for the paper; each panel that belongs in the exhibit set is
split into its own single-chart exhibit here, drawn from the SAME CSVs those working figures already
wrote. Nothing is recomputed by hand. Single-panel figures are COPIED under their exhibit name (the
originals are never moved). Heatmap exhibits are drawn from the CSVs the working figures wrote, so an
exhibit and its figure can never disagree.

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


def pct_positive(rows, key):
    """Share of rows where the column is > 0, measured from the CSV (never typed by hand)."""
    return 100.0 * sum(1 for r in rows if r[key] > 0) / len(rows)


def word_children(kids):
    return {1: "one child", 2: "two children", 3: "three children"}[kids]


def title_block(fig, title, subtitle, pairs=None, notes="", source=SOURCE_SRC):
    fig.subplots_adjust(top=top_header(fig, title, subtitle, pairs, panel_gap_pt=14))
    bottom_footer(fig, notes, source)


def heat(fname, rows, key, title, subtitle, diverging=True, contour=0.0, pct=False, vmax=None, contour_label="even",
         pairs=None, notes="", mark=True):
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
    if mark:
        ax.plot(EXAMPLE["payor"], EXAMPLE["recip"], marker="o", ms=7, mfc="none", mec=P["text"], mew=1.6)
        ax.annotate("worked example", (EXAMPLE["payor"], EXAMPLE["recip"]), xytext=(8, 8), textcoords="offset points", fontsize=8.5, color=P["text"])
    ax.grid(False)
    title_block(fig, title, subtitle, pairs, notes)
    fig.savefig(ex(fname), dpi=170); plt.close(fig)
    print(fname)


def copy(src, dst):
    shutil.copyfile(out(src), ex(dst)); print(dst, "(copy of", src + ")")


def childcare_rule_split(fname, rows_all, kids, exhibit_no):
    """One exhibit per child count, split from fig2_childcare_rules.csv (was the 3-panel E07)."""
    rs = sorted([r for r in rows_all if int(r["children"]) == kids], key=lambda r: r["payor_3c"])
    x = [r["payor_3c"] for r in rs]
    gross = [r["rule2_post_gross"] for r in rs]
    net = [r["rule3_post_net"] for r in rs]
    gap_pts = (x[-1] - net[-1]) * 100  # measured from the CSV's own last (highest-share) row

    fig, ax = theme.figure(8.6, 5.0)
    ax.plot(x, gross, color=P["series"][0], lw=2.2, label="Post-transfer gross shares")
    ax.plot(x, net, color=P["series"][2], lw=2.2, label="Post-transfer net shares")
    ax.plot(x, x, color=P["axis"], lw=1, ls="--", label="Current rule (Line 3c) = income share")
    ax.annotate(f"{gap_pts:.0f} points below\nincome share", (x[-1], net[-1]), xytext=(-90, -6),
                textcoords="offset points", fontsize=8.7, color=P["text_2"])
    ax.set_xlim(0.5, 1.0); ax.set_ylim(0, 1.0)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    theme.finish(ax, title=f"With {word_children(kids)}, post-transfer child care funds the payor {gap_pts:.0f} points below his income share",
                 subtitle="Share of the child care bill the payor funds, by his pre-transfer income share, two post-transfer rules.",
                 pct=True, xlabel="Payor's share of combined available income (Line 3c)", ylabel="Share of child care the payor funds",
                 pairs=facts(1, kids, "\\$100/child/wk, paid by the lower earner", f"\\${EXAMPLE['payor']:,.0f} / varies"),
                 notes="Child care is included in the order. Gap measured at the highest income share plotted. " + NOTE_CONV,
                 source=SOURCE_SRC + "; fig2_childcare.py")
    theme.save(fig, ex(fname))
    print(fname, f"(E{exhibit_no}, gap {gap_pts:.1f} pts)")


def main():
    # --- E01/E02/E04 from the 3-child Box 1 grid (unchanged) ---
    g3 = read_csv("fig1_heatmap_3child_box1.csv")
    F3 = facts(1, 3)
    pct3 = pct_positive(g3, "gap_household")
    heat("E01-who-holds-more-3-children.png", g3, "gap_household",
         f"With three children, the recipient household holds more after the order in {pct3:.0f}% of income combinations",
         "Recipient household net minus payor net, per year.", pairs=F3,
         notes="Measured from the grid's own cells (fig1_heatmap_3child_box1.csv). The inner 'even' loop is Line 6e's limit ending "
               "at 6d = 10%: the order drops ~\\$110/wk in one step. " + NOTE_MASK + NOTE_CONV)
    heat("E02-who-holds-more-per-person-3-children.png", g3, "gap_per_person",
         "Per person, the payor holds more almost everywhere",
         "Recipient household net ÷ 4, minus payor net. Companion to E01.", pairs=F3,
         notes="Payor ahead in 99% of cells. " + NOTE_MASK + NOTE_CONV)
    pct40 = pct_positive([{"order_pct_payor_net": r["order_pct_payor_net"] - 0.40} for r in g3], "order_pct_payor_net")
    heat("E04-order-as-share-of-payor-net-3-children.png", g3, "order_pct_payor_net",
         "The order exceeds 40% of the payor's net income only where the lower earner makes about \\$20,000 or less",
         "Order as a share of payor net; line at 40%.", diverging=False, contour=0.40, pct=True, vmax=0.60, pairs=F3,
         notes=f"{pct40:.0f}% of cells. Scale fixed 0–60%. " + NOTE_MASK + NOTE_CONV)

    # --- E18/E19: the 1-child and 2-child panels split from fig1_headline_household_gap (was E03). ---
    # The 3-child panel is E01 above; fig1_headline_household_gap.png stays as the working figure for
    # the paper (all three side by side), but is no longer copied into the exhibit set.
    g1 = read_csv("fig1_heatmap_1child_box1.csv")
    g2 = read_csv("fig1_heatmap_2child_box1.csv")
    pct1 = pct_positive(g1, "gap_household")
    pct2 = pct_positive(g2, "gap_household")
    heat("E18-who-holds-more-1-child.png", g1, "gap_household",
         f"With one child, the recipient household holds more after the order in only {pct1:.0f}% of income combinations",
         "Recipient household net minus payor net, per year. Companion to E01/E19 (same grid, 2 and 3 children).",
         pairs=facts(1, 1), mark=False,
         notes="Measured from the grid's own cells (fig1_heatmap_1child_box1.csv). " + NOTE_MASK + NOTE_CONV)
    heat("E19-who-holds-more-2-children.png", g2, "gap_household",
         f"With two children, the recipient household holds more after the order in {pct2:.0f}% of income combinations",
         "Recipient household net minus payor net, per year. Companion to E01/E18 (same grid, 1 and 3 children).",
         pairs=facts(1, 2), mark=False,
         notes="Measured from the grid's own cells (fig1_heatmap_2child_box1.csv). " + NOTE_MASK + NOTE_CONV)

    # --- E05/E06 (unchanged single-panel copies) ---
    copy("fig6_valve_units_lag.png", "E05-what-line-7e-sees-vs-true-burden-worked-example.png")
    copy("fig2_childcare_worked_example.png", "E06-child-care-share-three-rules-worked-example.png")

    # --- E20/E21/E22: 1/2/3-child panels split from fig2_childcare_rules (was E07) ---
    r2 = read_csv("fig2_childcare_rules.csv")
    childcare_rule_split("E20-child-care-funding-gap-1-child.png", r2, 1, 20)
    childcare_rule_split("E21-child-care-funding-gap-2-children.png", r2, 2, 21)
    childcare_rule_split("E22-child-care-funding-gap-3-children.png", r2, 3, 22)

    # --- E08/E09 from fig3's CSV (unchanged) ---
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
    theme.finish(ax, title="The Worksheet's credit for equal parenting time collapses as the income gap widens; a cross-credit narrows without collapsing",
                 subtitle="Reduction in the order for equal time, against the Box 2 order (the paying parent has the children about a third of the time).",
                 xlabel="Payor's share of combined available income (Line 3c)", ylabel="Reduction vs the Box 2 order", pct=True,
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
    theme.finish(ax, title="The equal-time credit is what a standard formula pays a parent who has the children one night in three",
                 subtitle="Massachusetts's credit for half the nights, converted into the overnight share a cross-credit "
                          "formula would need to produce it.",
                 xlabel="Payor's share of combined available income (Line 3c)", ylabel="Overnight share under a cross-credit", pct=True,
                 pairs=facts(1, 3, "None (base support)", f"\\${EXAMPLE['payor']:,.0f} / varies"),
                 notes="At the worked example (87.7% payor income share): 33% of overnights at factor 1.5, 47% at factor 2.0. "
                       "Blank below the Line 5c floor. " + NOTE_CONV,
                 source=SOURCE_SRC + "; box1_fix.py")
    theme.save(fig, ex("E09-implied-overnight-share-by-factor-3-children.png")); print("E09")

    # --- E10: unchanged single-panel copy ---
    copy("fig4_marginal_retention.png", "E10-cents-kept-of-next-dollar-worked-example.png")

    # --- E11/E12/E13: unchanged single-panel copies. E12 restyled with E17 as a pair
    #     (shared axis range, ordering, colours) inside fig5_states.py itself. ---
    copy("fig5a_states_S1.png", "E11-fifty-states-equal-parenting-one-fact-pattern.png")
    copy("fig5b_states_S2.png", "E12-fifty-states-lower-earner-primary-one-fact-pattern.png")
    copy("fig5c_credit_at_122_tilemap.png", "E13-credit-at-122-overnights-28-of-51.png")

    # --- E23/E24: the two panels split from fig7_box3_inversion (was E14) ---
    box3 = read_csv("fig7_box3_inversion.csv")
    box3.sort(key=lambda r: r["payor_3c"])
    with open(out("fig7_box3_inversion_example.csv")) as f:
        ex_vals = {row["item"]: float(row["value"]) for row in csv.DictReader(f)}

    fig, ax = theme.figure(9, 5.0)
    ax.plot([r["payor_3c"] for r in box3], [r["box1_7d"] for r in box3], color=P["series"][0], lw=2.2,
            label="Box 1: both children shared, equal time")
    ax.plot([r["payor_3c"] for r in box3], [r["box3_7d"] for r in box3], color=P["series"][1], lw=2.2,
            label="Box 3: one child residing primarily with each parent")
    ax.axvline(ex_vals["payor_3c"], color=P["text_mute"], lw=0.8)
    ax.annotate(f"${ex_vals['box1_7d']:,.0f}/wk", (ex_vals["payor_3c"], ex_vals["box1_7d"]), xytext=(-70, 8),
                textcoords="offset points", fontsize=9, color=P["text_2"])
    ax.annotate(f"${ex_vals['box3_7d']:,.0f}/wk ({ex_vals['reduction']:.0%} lower)", (ex_vals["payor_3c"], ex_vals["box3_7d"]),
                xytext=(6, -22), textcoords="offset points", fontsize=9, color=P["text_2"])
    ax.set_xlim(0.5, 1.0)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    theme.finish(ax, title=f"Splitting two children across two homes cuts the weekly order by {ex_vals['reduction']:.0%}",
                 subtitle="Weekly order for the same two children: both shared equal time (Box 1) vs one child with each parent (Box 3).",
                 xlabel="Payor's share of combined available income (Line 3c)", ylabel="Weekly order, Line 7d", money=True,
                 pairs=facts("1v3", 2, "None (base support)", f"\\${EXAMPLE['payor']:,.0f} / varies"),
                 notes="Companion to E24 (the schedule's own cost moves the opposite way). Letter § 5.1. " + NOTE_CONV,
                 source=SOURCE_SRC + "; fig7_box3_split.py")
    theme.save(fig, ex("E23-split-siblings-weekly-order-2-children.png")); print("E23")

    fig, ax = theme.figure(6.6, 5.0)
    labels = ["One home,\ntwo children\n(Table B ×1.40)", "Two homes,\none child each\n(Table B ×1.00, twice)"]
    vals = [ex_vals["tableB_one_home_two_children"], ex_vals["tableB_two_homes_one_each"]]
    pct_more = vals[1] / vals[0] - 1
    theme.bars(ax, np.arange(2), vals, color=P["series"][3])
    ax.set_xticks(np.arange(2)); ax.set_xticklabels(labels, fontsize=9)
    theme.label_ends(ax, np.arange(2), vals, fmt="{:.2f}×")
    ax.set_ylim(0, 2.4); ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}"))
    theme.finish(ax, title=f"Two homes, one child each, cost {pct_more:.0%} more on the schedule than one home with two",
                 subtitle="Table B's cost multiple: one home raising two children vs two homes each raising one.",
                 ylabel="Multiple of the one-child schedule amount", legend=False, comma=False,
                 pairs=facts("1v3", 2, "None (base support)", f"\\${EXAMPLE['payor']:,.0f} / varies"),
                 notes="Companion to E23 (the order itself falls even as the schedule's own cost rises). Letter § 5.1.",
                 source=SOURCE_SRC + "; fig7_box3_split.py")
    theme.save(fig, ex("E24-split-siblings-schedule-cost-2-children.png")); print("E24")

    # --- E25/E26: the two panels split from fig8_both_pay (was E15) ---
    with open(out("fig8_both_pay.csv")) as f:
        b8 = {row["scenario"]: row for row in csv.DictReader(f)}
    shares = b8["shares"]; combined = b8["combined childcare"]
    income_share = float(shares["his_childcare"])
    payor_cc_share = float(shares["payor_keeps"]); recip_cc_share = float(shares["recipient_holds"])
    total_cc = float(combined["order_wk"])
    his_extra = float(combined["payor_keeps"]); her_extra = float(combined["recipient_holds"])
    scenario_order = ["Neither pays child care", "Only the recipient pays $300/wk", "Both pay $300/wk"]
    scen_labels = ["Neither pays\nchild care", "Only the recipient\npays $300/wk", "Both pay\n$300/wk"]

    fig, ax = theme.figure(7.6, 4.4)
    cats = ["Share of combined\ngross income", "Share of the combined\nchild care bill"]
    payor_vals = [income_share, payor_cc_share]
    recip_vals = [1 - income_share, recip_cc_share]
    y = np.arange(2)[::-1]
    ax.barh(y, payor_vals, height=0.5, color=P["series"][0], label="Payor")
    ax.barh(y, recip_vals, left=[v + 0.004 for v in payor_vals], height=0.5, color=P["series"][1], label="Recipient")
    for yi, pv, rv in zip(y, payor_vals, recip_vals):
        ax.text(pv / 2, yi, f"{pv:.0%}", ha="center", va="center", fontsize=10, color="white")
        ax.text(pv + 0.004 + rv / 2, yi, f"{rv:.0%}", ha="center", va="center", fontsize=9, color=P["text"])
    ax.set_yticks(y); ax.set_yticklabels(cats)
    ax.set_xlim(0, 1.0); ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.grid(False)
    theme.finish(ax, title=f"The payor bears {payor_cc_share:.0%} of the combined child care while earning {income_share:.0%} of the gross income",
                 subtitle=f"Who pays a combined \\${total_cc:,.0f}/yr of child care, both parents paying \\$300/wk in their own home.",
                 comma=False, legend=True,
                 pairs=facts(1, 3, "\\$300/wk in each home", "\\$201,000 / \\$29,640"),
                 notes="Companion to E26 (each parent's net position under three scenarios). Two of three children under 13.",
                 source="model/submission_figures.py § 2.1; fig8_both_pay.py")
    theme.save(fig, ex("E25-both-pay-child-care-who-pays-3-children.png")); print("E25")

    fig, ax = theme.figure(7.6, 4.6)
    him = [float(b8[s]["payor_keeps"]) for s in scenario_order]
    her = [float(b8[s]["recipient_holds"]) for s in scenario_order]
    xs = np.arange(3); wd = 0.36
    ax.bar(xs - wd / 2, him, width=wd, color=P["series"][0], label="Payor keeps (one person)")
    ax.bar(xs + wd / 2, her, width=wd, color=P["series"][1], label="Recipient household holds (four people)")
    for i in range(3):
        ax.text(i - wd / 2, him[i] + 1500, f"${him[i] / 1000:,.0f}k", ha="center", fontsize=8.5, color=P["text_2"])
        ax.text(i + wd / 2, her[i] + 1500, f"${her[i] / 1000:,.0f}k", ha="center", fontsize=8.5, color=P["text_2"])
    ax.set_xticks(xs); ax.set_xticklabels(scen_labels, fontsize=9)
    ax.set_ylim(0, 120_000); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v / 1000:,.0f}k"))
    theme.finish(ax, title=f"Both parents paying child care costs the payor \\${his_extra:,.0f} a year, the recipient household \\${her_extra:,.0f}",
                 subtitle="Each parent's net position, neither, one, or both paying $300/wk of child care.",
                 legend=True,
                 pairs=facts(1, 3, "\\$0 / \\$300 / \\$300 per wk (see scenarios)", "\\$201,000 / \\$29,640"),
                 notes=f"Companion to E25. The payor's own \\${float(b8['Both pay $300/wk']['his_childcare']):,.0f} cuts the order by only "
                       f"\\${float(shares['her_childcare']):,.0f}/yr (Line 6e clip). Per person he still leads.",
                 source="model/submission_figures.py § 2.1; fig8_both_pay.py")
    theme.save(fig, ex("E26-both-pay-child-care-net-position-3-children.png")); print("E26")

    # --- E16/E17: unchanged single-panel copies (E17 restyled as a pair with E12 in its own script) ---
    copy("fig9_schedule_ceilings.png", "E16-where-each-presumptive-schedule-stops-51.png")
    copy("fig10_ma_shared_vs_primary.png", "E17-ma-equal-time-vs-others-primary-custody.png")

    # --- E27: the deferral timeline (new, item 5 of the 2026-09-06 direction) ---
    copy("fig11_deferral_timeline.png", "E27-gross-vs-net-deferred-1-of-5-cycles.png")

    # --- Retire the old multi-panel exhibits from a prior run (never delete: moved, not removed) ---
    RETIRED_DIR = ex("_retired-2026-09-06-multi-panel")
    RETIRED_PREFIXES = ("E03-", "E07-", "E14-", "E15-")
    stale = [n for n in os.listdir(EX) if n.endswith(".png") and n.startswith(RETIRED_PREFIXES)]
    if stale:
        os.makedirs(RETIRED_DIR, exist_ok=True)
        for n in stale:
            shutil.move(ex(n), os.path.join(RETIRED_DIR, n))
            print("retired ->", n)

    with open(ex("README.md"), "w") as f:
        f.write("# Exhibit set — one chart per file\n\n")
        f.write("Built by `model/charts/exhibits.py` from the working figures in `output/charts/` (never edit these by hand; rebuild). "
                "Naming and ratings: `docs/2026-09-05-chart-exhibit-guide.md`. No exhibit has more than one set of axes "
                "(2026-09-06: \"I told you ONE EXHIBIT, ONE GRAPH\").\n\n")
        f.write("Heatmap exhibits E01/E02/E04/E18/E19 are drawn from `fig1_heatmap_{1,2,3}child_box1.csv`; E20-E22 from "
                "`fig2_childcare_rules.csv`; E08/E09 from `fig3_credit_collapse.csv`; E23/E24 from `fig7_box3_inversion*.csv`; "
                "E25/E26 from `fig8_both_pay.csv`; E27 from `data/deferrals-gross-vs-net.json`. The rest are copies of "
                "single-panel figures.\n\n")
        f.write("**Retired from the exhibit set (multi-panel; kept as working figures for the paper only):** "
                "`fig1_headline_household_gap.png` (was E03; its three panels are now E18/E19/E01), "
                "`fig2_childcare_rules.png` (was E07; now E20/E21/E22), `fig7_box3_inversion.png` (was E14; now E23/E24), "
                "`fig8_both_pay.png` (was E15; now E25/E26). The old E03/E07/E14/E15 exhibit PNGs are retired from the set: "
                "in the source repository they sit in `_retired-2026-09-06-multi-panel/`; a copy of this folder may still "
                "carry them unlinked. Nothing in the live set references them.\n\n")
        f.write("The per-person exhibit (E02) travels with E01/E18/E19. The lead pair is E12 then E17 (same states, same "
                "axis range, same colours, same ordering rule): E12 ranks every jurisdiction's primary-custody order with "
                "Massachusetts marked; E17 replaces Massachusetts's bar with its equal-time order. Generic grids set the MA "
                "under-13 credit to zero.\n\n")
        for n in sorted(os.listdir(EX)):
            if n.endswith(".png"):
                f.write(f"- `{n}`\n")
    print("exhibits README written")


if __name__ == "__main__":
    main()
