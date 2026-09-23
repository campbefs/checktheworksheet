#!/usr/bin/env python3
"""Where the Guidelines order exceeds the federal ceiling on what may be collected.

Asked for by the owner, 2026-09-21: "if we can show that the guidelines exceed the
federal maximum in addition to just not computing the net that would be a very
strong story."

WHAT THE FEDERAL CEILING IS, AND WHAT IT IS NOT. 15 U.S.C. s 1673(b)(2) caps what
an employer may WITHHOLD from a paycheck for support. It does not cap what a court
may order. That distinction is the whole reason this file reports a crossing rather
than a violation: an order above the ceiling is not unlawful, it is UNCOLLECTIBLE
IN FULL, and the uncollected part becomes arrears against a parent who never
refused to pay. Saying otherwise is the trap recorded three times in
context/MEMORY.md -- "arguing that a floor is a roof".

THE CEILING IS FOUR NUMBERS, NOT ONE, and which one applies is a fact about the
payor's household, not about the order:

    50%  supports another spouse or dependent child, no arrears 12+ weeks old
    55%  supports another spouse or dependent child, arrears 12+ weeks old
    60%  no other household,                        no arrears 12+ weeks old
    65%  no other household,                        arrears 12+ weeks old

So a REMARRIED payor, or one with a child in a second household, has the LOWEST
ceiling and is the easiest to push past it. Every table below reports all four,
because quoting one rate as "the federal maximum" is how this argument gets
dismissed.

THE GRID is the published one: the income pairs in output/charts/fig1_heatmap_*.csv,
higher earner $60,000 to $300,000 against lower earner $0 to $120,000, masked where
the lower earner earns more. 1,147 cells per (children, box). Reading the pairs from
the committed CSV rather than regenerating them is deliberate: this figure and the
published heat maps cannot then disagree about which incomes were tested.

CHILD CARE IS PART OF THE GUIDELINES, NOT AN ADD-ON TO THEM. Section II.E.1 lets a
parent claim up to $430 per child per week, and the Worksheet puts the claim on
Line 2g inside the same calculation that produces the order. An order that crosses
the ceiling only once child care is claimed has still been produced by the
Guidelines. That is the finding, and the no-child-care column is reported beside it
so nobody can say it was hidden.

    .venv/bin/python model/ccpa_grid.py
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import net_caps as nc

# 15 U.S.C. s 1673(b)(2). Keyed by (supports another household, arrears 12+ weeks).
CCPA_RATES = {
    (True, False): 0.50,
    (True, True): 0.55,
    (False, False): 0.60,
    (False, True): 0.65,
}
RATES = sorted(set(CCPA_RATES.values()))

# Section II.E.1: the most that may lawfully be claimed, per child, per week.
GUIDELINES_MAX_CHILDCARE_PER_CHILD = 430.0

# The project's generic grid conventions, matching the published heat maps.
A_HEALTH, B_HEALTH = 33.0, 43.0

GRID_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "output", "charts")
if not os.path.isfile(os.path.join(GRID_DIR, "fig1_heatmap_3child_box1.csv")):  # the published repo carries the same CSVs at figures/working/
    GRID_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "figures", "working")


def grid_pairs(kids, box):
    """The (higher_gross, lower_gross) pairs the published heat map was drawn from."""
    path = os.path.join(GRID_DIR, f"fig1_heatmap_{kids}child_box{box}.csv")
    with open(path, newline="", encoding="utf-8") as fh:
        return [(float(r["higher_gross"]), float(r["lower_gross"]))
                for r in csv.DictReader(fh)]


def share_of_net(payor_gross, lower_gross, kids, box, childcare_total):
    """The order as a share of the payor's net pay, on the withholding basis.

    childcare_total is the WEEKLY total claimed across all children, which is how
    order_and_cap takes it and how Line 2g reads.
    """
    r = nc.order_and_cap(payor_gross, lower_gross / 52.0, kids, box,
                         childcare_total, A_HEALTH, B_HEALTH)
    return r["share_of_net"]


def crossings(kids, box, childcare_total):
    """How many grid cells put the order above each of the four federal ceilings."""
    pairs = grid_pairs(kids, box)
    shares = [share_of_net(hi, lo, kids, box, childcare_total) for hi, lo in pairs]
    out = {
        "kids": kids,
        "box": box,
        "childcare_total": childcare_total,
        "cells": len(shares),
        "max": max(shares),
        "median": sorted(shares)[len(shares) // 2],
        "over": {},
    }
    for rate in RATES:
        n = sum(1 for s in shares if s > rate)
        out["over"][rate] = {"n": n, "pct": n / len(shares) if shares else 0.0}
    return out


def first_crossing_childcare(kids, box, rate, step=10.0):
    """The lowest weekly child-care claim at which ANY grid cell crosses `rate`.

    Steps in $10 of TOTAL weekly claim up to the Guidelines' own maximum. Returns
    None when the ceiling is never reached, which is the honest answer for the
    combinations where it is not.
    """
    top = GUIDELINES_MAX_CHILDCARE_PER_CHILD * kids
    cc = 0.0
    while cc <= top:
        pairs = grid_pairs(kids, box)
        if any(share_of_net(hi, lo, kids, box, cc) > rate for hi, lo in pairs):
            return cc
        cc += step
    return None


# The worked example's own claim: $100 per child per week, which is what the owner's
# order carries. Far below the $430 the Guidelines allow, so a crossing here cannot be
# called an extreme.
WORKED_EXAMPLE_PER_CHILD = 100.0


def cells_over(kids, box, childcare_total, rate):
    """The (payor gross, other parent gross, share of net) of every crossing cell.

    Exists so a claim about how many cells cross can be checked against WHICH ones
    do. A count alone invites "you picked the extremes"; this answers it.
    """
    out = []
    for hi, lo in grid_pairs(kids, box):
        s = share_of_net(hi, lo, kids, box, childcare_total)
        if s > rate:
            out.append((hi, lo, s))
    return sorted(out, key=lambda r: -r[2])


def report(kids_list=(1, 2, 3), boxes=(1, 2)):
    rows = []
    for kids in kids_list:
        for box in boxes:
            top = GUIDELINES_MAX_CHILDCARE_PER_CHILD * kids
            rows.append({
                "kids": kids,
                "box": box,
                "none": crossings(kids, box, 0.0),
                "worked": crossings(kids, box, WORKED_EXAMPLE_PER_CHILD * kids),
                "maxcc": crossings(kids, box, top),
                "worked_childcare": WORKED_EXAMPLE_PER_CHILD * kids,
                "top_childcare": top,
            })
    return rows


def main():
    print("WHERE THE GUIDELINES ORDER EXCEEDS THE FEDERAL COLLECTION CEILING")
    print("15 U.S.C. s 1673(b)(2) caps WITHHOLDING, not the order. An order above")
    print("the ceiling is not unlawful; it is uncollectible in full, and the excess")
    print("becomes arrears. 1,147 grid cells per row.")
    print()
    print("Box 1 = joint custody   Box 2 = the other parent has primary custody")
    print(f"Child care maximum = ${GUIDELINES_MAX_CHILDCARE_PER_CHILD:.0f}/child/week, "
          "Guidelines s II.E.1")
    print()

    for row in report():
        k, b = row["kids"], row["box"]
        print(f"--- {k} child{'ren' if k > 1 else ''}, Box {b} "
              f"(child-care maximum ${row['top_childcare']:,.0f}/wk total)")
        for label, r in (("no child care claimed", row["none"]),
                         (f"child care at $100/child (${row['worked_childcare']:,.0f}/wk)",
                          row["worked"]),
                         ("child care at the Guidelines maximum", row["maxcc"])):
            over = "  ".join(
                f"{int(rate*100)}%: {r['over'][rate]['n']:>4} "
                f"({r['over'][rate]['pct']*100:4.1f}%)" for rate in RATES)
            print(f"    {label:<38} max {r['max']*100:5.1f}% of net   {over}")
        print()

    print("LOWEST CLAIM THAT PUTS ANY CELL OVER A CEILING (total weekly child care)")
    for kids in (1, 2, 3):
        for box in (1, 2):
            parts = []
            for rate in RATES:
                cc = first_crossing_childcare(kids, box, rate)
                parts.append(f"{int(rate*100)}%: " +
                             (f"${cc:,.0f}" if cc is not None else "never"))
            print(f"  {kids} child{'ren' if kids > 1 else ''}, Box {box}:  "
                  + "   ".join(parts))


if __name__ == "__main__":
    main()
