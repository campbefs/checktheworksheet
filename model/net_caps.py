#!/usr/bin/env python3
"""Two hard ceilings on a support order, expressed as a share of the payor's net pay.

The proposal, in the owner's words: child support at joint custody should never
exceed 25 percent of net pay, and child support at primary custody should never
exceed 40 percent of net pay, both written into the Guidelines rather than left
to a deviation a party has to litigate for.

WHERE THE TWO NUMBERS COME FROM, and they are not the same kind of number.

The 40 percent is the Commonwealth's own. Section IV.C already presumes
substantial hardship when an order reaches "40% or more of the payor's
available income" for a current child support order. This proposal does not
invent that threshold; it changes the quantity the threshold is measured
against, from Line 3a available income (gross, less a short list of support
orders and insurance premiums) to net pay, and changes the consequence from a
rebuttable presumption a party must raise to a ceiling the Worksheet applies.
At the worked example the difference between those two measures is 12
percentage points: Line 7e reads 28.5 percent where the order is 40.5 percent
of net.

The 25 percent is a policy choice and this file does not pretend otherwise. No
Massachusetts document names it. What can be said from the model is what it
costs and where it binds, which is what the sweep below prints. The argument
for a lower ceiling at equal time is that both households carry the full fixed
cost of housing a child -- a bedroom in each home -- which is the same premise
behind the 1.5 duplication factor in the cross-credit that 23 states use, and
Indiana's Guideline 6 Commentary putting the duplicated share of the basic
obligation at 50 percent.

NET HERE IS THE WITHHOLDING BASIS, the published model's default: gross less
federal income tax (single filer, standard deduction), less Social Security and
Medicare, less Massachusetts income tax. About eight constants, reproducible in
a spreadsheet, and the method the Commonwealth's own consultant uses to convert
gross to net in every review. No refundable credits, no filing status, no
dependents. A ceiling defined on a number a parent cannot verify is not a
ceiling; this one a parent can check with a calculator.

    .venv/bin/python model/net_caps.py

THE ADOPTION PROBLEM, stated plainly because it is the whole risk. The Worksheet
holds no net-income line, and five reviews have taken up gross versus net and
none changed it. A ceiling on net therefore needs one new input the form does
not collect today. The narrowest version, and the one the redline in
docs/ proposes, is a single published lookup: one column of net pay against
gross, computed once a year by the same method the economic review already
uses, so the parent reads a row rather than doing a tax computation.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import worksheet as w
from model.net_position import net_income_withholding_basis

# The proposal.
CAP_SHARED = 0.25   # Box 1 and Box 3: the children are with each parent about half the time
CAP_PRIMARY = 0.40  # Box 2: the children are primarily with one parent

# The worked example that runs through this project's documents.
PAYOR_GROSS = 201000.0
RECIP_WEEKLY = 570.0
KIDS = 3
A_HEALTH, B_HEALTH = 33.0, 43.0

# The federal collection ceiling that applies to THIS payor, 15 U.S.C. s 1673(b)(2):
# four rates -- 50/55/60/65 percent of disposable earnings -- turning on whether the
# payor supports another spouse or dependent child and whether any arrears predate the
# twelve weeks before the workweek. This payor supports no other household and carries
# no arrears, so his rate is the lower of the two "no other household" rates, 60 percent.
# It is a fact-pattern constant, not a general legal ceiling -- a payor supporting
# another household would be at 50 or 55 percent instead. See
# docs/2026-09-10-ccpa-disposable-earnings.md section 1.
CCPA_CEILING_THIS_PAYOR = 0.60


def cap_for(box):
    """The ceiling that applies to a custody box.

    Box 3 (split) takes the shared ceiling: every line the Guidelines write for
    Box 1 says "Box 1 or Box 3", and in a split each parent is the primary
    residence for at least one child, so both households carry the duplicated
    fixed costs the lower ceiling is meant to recognise.
    """
    return CAP_PRIMARY if box == 2 else CAP_SHARED


def order_and_cap(payor_gross, recipient_weekly, kids, box, childcare_total=0.0,
                  a_health=0.0, b_health=0.0):
    """Return the Worksheet order, the payor's net, and what the ceiling does to it.

    Every figure is annual except the two weekly order amounts, which are the
    units the Worksheet itself uses at Line 7d.
    """
    per = childcare_total / 3.0 if kids == 3 else childcare_total / max(kids, 1)
    sheet = w.run(
        box=box,
        a_gross=recipient_weekly,
        b_gross=payor_gross / 52.0,
        children_under18=kids,
        a_health=a_health,
        b_health=b_health,
        a_childcare=tuple([per] * kids),
        b_childcare=tuple([0.0] * kids),
    )
    weekly = sheet["7d"]
    annual = weekly * 52.0
    net = net_income_withholding_basis(payor_gross)
    cap = cap_for(box)
    ceiling_annual = cap * net
    binds = annual > ceiling_annual
    capped_annual = min(annual, ceiling_annual)

    return {
        "box": box,
        "childcare_total": childcare_total,
        "weekly": weekly,
        "annual": annual,
        "net": net,
        "share_of_net": annual / net,
        "line_7e": sheet["7e"],
        "cap": cap,
        "ceiling_annual": ceiling_annual,
        "ceiling_weekly": ceiling_annual / 52.0,
        "binds": binds,
        "capped_annual": capped_annual,
        "capped_weekly": capped_annual / 52.0,
        "reduction_annual": annual - capped_annual,
        "reduction_pct": (annual - capped_annual) / annual if annual else 0.0,
    }


def worked_example():
    rows = []
    for box in (1, 2):
        for cc in (0.0, 300.0):
            rows.append(order_and_cap(PAYOR_GROSS, RECIP_WEEKLY, KIDS, box, cc,
                                      A_HEALTH, B_HEALTH))
    return rows


def sweep_gap(payor_gross=PAYOR_GROSS, kids=KIDS, box=1, childcare_total=0.0,
              lo=10000, hi=160000, step=15000):
    """Hold the payor fixed, vary the other parent: this is what the ceiling responds to.

    Sweeping payor income alone is misleading, because it holds the income GAP
    wide by construction and makes the ceiling look as though it binds
    everywhere. The order's share of the payor's net is driven by the gap, not
    by either income on its own.
    """
    return [
        order_and_cap(payor_gross, g / 52.0, kids, box, childcare_total,
                      A_HEALTH, B_HEALTH)
        for g in range(lo, hi + 1, step)
    ]


def cap_orderings(payor_gross, recipient_weekly, kids, box, childcare_total,
                  a_health=0.0, b_health=0.0):
    """Where the ceiling sits relative to the Line 6b child-care allocation.

    The child-care cost enters Line 7d through a chain: the other parent's
    claimed cost at 6a, this parent's share of it at 6b, then 6c, 6e, 6g, 7b,
    7d. A ceiling can be applied at either end of that chain, and the two give
    different answers whenever child care is claimed.

    AFTER (the redline's new Line 7g, and what order_and_cap does): compute
    Line 7d as the Worksheet computes it today, child care included, then cap
    the whole figure. The ceiling is a ceiling on everything the payor owes.

    BEFORE: cap the base support amount, then add the child-care component on
    top of the capped figure. Child care is treated as a reimbursement of a
    cost actually incurred rather than as part of the transfer, so it is not
    something a hardship ceiling should refuse.

    The child-care component is measured, not modelled: it is Line 7d with the
    cost claimed less Line 7d without it, so whatever the 6e limitation does to
    it on the way through is carried faithfully.

    Returns both, plus the two facts that decide between them: whether the
    capped order still covers the payor's own 6b allocation, and whether the
    BEFORE figure still exceeds the ceiling it was supposed to be bounded by.
    """
    full = order_and_cap(payor_gross, recipient_weekly, kids, box,
                         childcare_total, a_health, b_health)
    base = order_and_cap(payor_gross, recipient_weekly, kids, box,
                         0.0, a_health, b_health)
    cc_component_annual = full["annual"] - base["annual"]

    after_annual = full["capped_annual"]
    before_annual = min(base["annual"], base["ceiling_annual"]) + cc_component_annual

    ceiling = full["ceiling_annual"]
    return {
        "box": box,
        "childcare_total": childcare_total,
        "uncapped_annual": full["annual"],
        "ceiling_annual": ceiling,
        "cc_component_annual": cc_component_annual,
        "after_annual": after_annual,
        "before_annual": before_annual,
        "after_weekly": after_annual / 52.0,
        "before_weekly": before_annual / 52.0,
        "gap_annual": before_annual - after_annual,
        # A ceiling the result exceeds is not a ceiling. This is the whole case
        # against applying it before the allocation.
        "before_exceeds_ceiling": before_annual > ceiling + 0.01,
        "before_share_of_net": before_annual / full["net"],
        "after_share_of_net": after_annual / full["net"],
        # And this is the whole case for it: does the capped order still leave
        # the recipient the payor's share of a cost she has actually paid?
        "cc_covered_after": after_annual >= cc_component_annual - 0.01,
        "net": full["net"],
    }


def sweep_childcare(payor_gross=None, recipient_weekly=None, kids=None, box=1,
                    amounts=(0.0, 100.0, 200.0, 300.0, 430.0, 600.0, 900.0, 1290.0)):
    """The two orderings across the legal range of claimed child care.

    $1,290 a week is three children at the Guidelines' own $430 per child
    ceiling at Section II.E.1, so the top of this sweep is the most that may
    lawfully be claimed for this family, not a worst case invented here.
    """
    payor_gross = PAYOR_GROSS if payor_gross is None else payor_gross
    recipient_weekly = RECIP_WEEKLY if recipient_weekly is None else recipient_weekly
    kids = KIDS if kids is None else kids
    return [cap_orderings(payor_gross, recipient_weekly, kids, box, cc,
                          A_HEALTH, B_HEALTH) for cc in amounts]


def ccpa_crossing(box, ceiling=CCPA_CEILING_THIS_PAYOR, payor_gross=None,
                  recipient_weekly=None, kids=None, top=1290.0):
    """Where the ORDER TODAY -- current Guidelines, no reform -- crosses a federal
    collection ceiling, as claimed child care rises from $0 to the legal maximum.

    This is not the 25/40 percent ceiling this file proposes. It is the federal
    ceiling on GARNISHMENT, 15 U.S.C. s 1673(b)(2), which already binds every
    order in the country regardless of whether Massachusetts adopts anything.
    The point is not that Massachusetts is violating it -- the Act caps
    collection, not the amount a court may order, so an order above the ceiling
    simply is not fully collectible in the pay period it is due; the excess
    accrues. The point is that "the order stays well under the federal ceiling"
    is not true once ordinary child care is claimed, so a reader should not be
    told it is.

    $1,290/wk (top) is three children at the Guidelines' own $430-per-child
    ceiling, Section II.E.1 -- the most that may lawfully be claimed for this
    family, not a worst case invented here.

    Scans in $1 steps because the order is piecewise linear in claimed child
    care (the 6e limitation can change slope) rather than searching for a
    closed form; 1,291 evaluations is cheap and exact to the dollar.
    """
    payor_gross = PAYOR_GROSS if payor_gross is None else payor_gross
    recipient_weekly = RECIP_WEEKLY if recipient_weekly is None else recipient_weekly
    kids = KIDS if kids is None else kids

    def share_at(cc):
        r = order_and_cap(payor_gross, recipient_weekly, kids, box, cc, A_HEALTH, B_HEALTH)
        return r["share_of_net"]

    share_at_0 = share_at(0.0)
    share_at_top = share_at(top)

    crossing_wk = None
    if share_at_top > ceiling:
        for cc in range(0, int(top) + 1):
            if share_at(float(cc)) > ceiling:
                crossing_wk = float(cc)
                break

    return {
        "box": box,
        "ceiling": ceiling,
        "share_at_0": share_at_0,
        "share_at_top": share_at_top,
        "top_childcare": top,
        "crossing_wk": crossing_wk,
    }


GRID_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "output", "charts")
if not os.path.isfile(os.path.join(GRID_DIR, "fig1_heatmap_3child_box1.csv")):  # the published repo carries the same CSVs at figures/working/
    GRID_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "figures", "working")


def grid_share_over(kids, box):
    """How much of the published income grid each ceiling would reach.

    Reads the committed CSV that the published heat maps are drawn from rather
    than recomputing, so this figure and the figure on the site cannot disagree.
    Those grids use the project's generic conventions: premiums $33/$43 weekly,
    no child care, and the kids-under-13 credit set to zero -- which does not
    matter under the withholding basis, where no credit enters at all. 1,147
    cells, higher earner $60,000 to $300,000 against lower earner $0 to
    $120,000, masked where the lower earner earns more.

    Verified against the live model on 2026-09-10: a sample of cells reproduced
    to the cent.
    """
    import csv

    path = os.path.join(GRID_DIR, f"fig1_heatmap_{kids}child_box{box}.csv")
    with open(path, newline="", encoding="utf-8") as fh:
        shares = [float(r["order_pct_payor_net"]) for r in csv.DictReader(fh)]
    cap = cap_for(box)
    over = [s for s in shares if s > cap]
    return {
        "kids": kids,
        "box": box,
        "cells": len(shares),
        "cap": cap,
        "over": len(over),
        "share_over": len(over) / len(shares) if shares else 0.0,
        "max": max(shares) if shares else 0.0,
        "median": sorted(shares)[len(shares) // 2] if shares else 0.0,
    }


def _fmt(r):
    flag = "CAPPED" if r["binds"] else "  ok  "
    return (f"  {flag}  order ${r['weekly']:8.2f}/wk  ${r['annual']:9,.0f}/yr"
            f"  = {r['share_of_net']*100:5.1f}% of net"
            f"   ceiling {r['cap']*100:.0f}% = ${r['ceiling_weekly']:8.2f}/wk"
            f"   new order ${r['capped_weekly']:8.2f}/wk"
            f"   ({r['reduction_pct']*100:4.1f}% lower)")


def main():
    print("Two ceilings on a support order, as a share of the payor's net pay")
    print("net = the withholding basis: gross less federal income tax (single filer,")
    print("standard deduction), Social Security and Medicare, and Massachusetts income tax")
    print()
    print(f"Proposal: {CAP_SHARED*100:.0f}% of net at joint custody (Box 1, Box 3), "
          f"{CAP_PRIMARY*100:.0f}% at primary custody (Box 2)")
    print()

    print(f"THE WORKED EXAMPLE  payor ${PAYOR_GROSS:,.0f}/yr, other parent "
          f"${RECIP_WEEKLY*52:,.0f}/yr, {KIDS} children, premiums "
          f"${A_HEALTH:.0f}/${B_HEALTH:.0f} weekly")
    net = net_income_withholding_basis(PAYOR_GROSS)
    print(f"  payor net ${net:,.2f}/yr")
    print()
    for r in worked_example():
        box_label = "Box 1, equal time " if r["box"] == 1 else "Box 2, primary    "
        cc = f"child care ${r['childcare_total']:.0f}/wk" if r["childcare_total"] else "no child care     "
        print(f"  {box_label} {cc}")
        print(_fmt(r))
        print(f"          Line 7e reports {r['line_7e']*100:.1f}% of available income "
              f"against {r['share_of_net']*100:.1f}% of net"
              f"  ({(r['share_of_net']-r['line_7e'])*100:.1f} points apart)")
        print()

    print("HOW MUCH OF THE PUBLISHED INCOME GRID EACH CEILING REACHES")
    print("  1,147 cells: higher earner $60,000-$300,000 against lower earner $0-$120,000,")
    print("  no child care, premiums $33/$43 weekly. Each box measured against its own ceiling.")
    print()
    print(f"  {'grid':30s} {'ceiling':>8s} {'cells over':>12s} {'median':>8s} {'max':>7s}")
    for kids in (1, 2, 3):
        for box in (1, 2):
            g = grid_share_over(kids, box)
            label = f"{kids} child{'ren' if kids > 1 else ' '}, {'equal time' if box == 1 else 'primary custody'}"
            print(f"  {label:30s} {g['cap']*100:6.0f}%  {g['over']:5d} ({g['share_over']*100:4.1f}%)"
                  f"  {g['median']*100:6.1f}%  {g['max']*100:5.1f}%")
    print()
    print("  Read this before quoting it. The 40 percent ceiling reaches NOTHING with one or")
    print("  two children anywhere on the grid; it is a backstop for three-child orders. The")
    print("  25 percent ceiling reaches about half of two-child and two thirds of three-child")
    print("  equal-time orders, so it is not a backstop, it is a different schedule for shared")
    print("  custody. Those are two different kinds of proposal and they will be received")
    print("  differently.")
    print()

    print("WHERE THE CEILING SITS RELATIVE TO THE LINE 6b CHILD-CARE ALLOCATION")
    print("  AFTER = cap Line 7d as computed, child care included (the redline's new Line 7g).")
    print("  BEFORE = cap base support, then add the child-care component on top.")
    print(f"  Worked example, payor ${PAYOR_GROSS:,.0f}, other parent ${RECIP_WEEKLY*52:,.0f}, "
          f"{KIDS} children.")
    print()
    for box in (1, 2):
        cap = cap_for(box)
        label = "equal time (Box 1)" if box == 1 else "primary custody (Box 2)"
        print(f"  {label}, ceiling {cap*100:.0f}% of net "
              f"= ${cap*net_income_withholding_basis(PAYOR_GROSS)/52.0:,.2f}/wk")
        print(f"    {'child care':>12s} {'uncapped':>10s} {'AFTER':>10s} {'BEFORE':>10s}"
              f" {'BEFORE % net':>13s} {'over ceiling?':>14s} {'cc covered?':>12s}")
        for r in sweep_childcare(box=box):
            print(f"    {r['childcare_total']:>10,.0f}/wk"
                  f" {r['uncapped_annual']/52:>10,.2f} {r['after_weekly']:>10,.2f}"
                  f" {r['before_weekly']:>10,.2f} {r['before_share_of_net']*100:>12.1f}%"
                  f" {('YES' if r['before_exceeds_ceiling'] else 'no'):>14s}"
                  f" {('yes' if r['cc_covered_after'] else 'NO'):>12s}")
        print()
    print("  Read this before choosing. BEFORE produces an order above the ceiling in every row")
    print("  where child care is claimed, so a rule written that way is not a ceiling. AFTER")
    print("  holds the line but can cut the order below the payor's own 6b allocation, which")
    print("  means the parent who paid the provider is not made whole.")
    print()

    print(f"WHERE THE ORDER TODAY CROSSES THIS PAYOR'S OWN {CCPA_CEILING_THIS_PAYOR*100:.0f}%")
    print("  FEDERAL COLLECTION CEILING (15 U.S.C. s 1673(b)(2), no other household, no arrears)")
    print("  Current Guidelines, no reform -- not this file's 25/40 percent proposal. The Act")
    print("  caps collection, not the order, so crossing this line does not mean a violation;")
    print("  the excess simply cannot be collected in the pay period it is due and accrues.")
    print()
    for box in (1, 2):
        label = "equal time (Box 1)" if box == 1 else "primary custody (Box 2)"
        r = ccpa_crossing(box)
        cross = f"${r['crossing_wk']:,.0f}/wk" if r["crossing_wk"] is not None else "never, within the legal range"
        print(f"  {label}")
        print(f"    no child care        {r['share_at_0']*100:5.1f}% of net")
        print(f"    crosses {CCPA_CEILING_THIS_PAYOR*100:.0f}% at    {cross}")
        print(f"    legal maximum ($1,290/wk, $430/child x 3)   {r['share_at_top']*100:5.1f}% of net")
        print()

    print(f"WHAT THE CEILING RESPONDS TO  payor ${PAYOR_GROSS:,.0f}, equal time, "
          f"{KIDS} children, no child care")
    print("  The share of net is driven by the income GAP, not by either income alone.")
    for g, r in zip(range(10000, 160001, 15000), sweep_gap()):
        flag = "CAPPED" if r["binds"] else "      "
        print(f"  other parent ${g:7,}  order ${r['weekly']:8.2f}/wk"
              f"  {r['share_of_net']*100:5.1f}% of net  {flag}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
