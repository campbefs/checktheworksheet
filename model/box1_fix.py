#!/usr/bin/env python3
"""Box 1 (shared parenting) -- what it does now, why the credit collapses, and three
candidate redlines, each modelled through the transcribed worksheet.

    .venv/bin/python model/box1_fix.py

WHY THIS EXISTS
---------------
Submission section 5 currently asks only for a Commentary disclosure that the Box 1
credit is a function of income shares. That is an observation, not an ask. Shared parenting is the lead argument, so section 5 needs a
redline with reasons. This module is the modelling that has to exist before any
formula goes into the letter.

WHAT BOX 1 DOES NOW  (all identities verified against worksheet.run by the tests)
--------------------------------------------------------------------------------
Under Box 1 both columns carry every child, so 4c is the same in both columns and

    Parent A's 5b = 4c x (B's income share)      "what B owes A"
    Parent B's 5b = 4c x (A's income share)      "what A owes B"
    6g            = A's 6e - B's 6e

Because Box 2 puts zero children in the payor's column, Box 2's order is 4c x (B's
income share). So, exactly:

    shared-parenting credit = the payor's own Line 6e

and that quantity is destroyed twice over:

  (1) The payor's column entitlement is 4c x the RECIPIENT'S income share. The less
      the other parent earns, the less the payor is credited for having the children
      half the time. Nothing about parenting time enters the line.

  (2) Line 6e's income-disparity limitation then fires on the payor's column, because
      his column entitlement is small relative to his income (6d < 10%), and caps it
      at roughly 10% of the RECIPIENT'S income. At the worked example that halves
      $152.84 to $75.17.

The limitation at 6e is the same device that appears at Line 7a/7b in Box 2, where it
protects the payor by capping his OBLIGATION. Under Box 1 it is applied to each
column symmetrically, so on the payor's column it caps an ENTITLEMENT instead, and
the protection runs backwards.

THE EQUIVALENCE THAT NAMES THE PROBLEM
--------------------------------------
Strip the 6e limitation and Box 1 is algebraically the standard shared-parenting
cross-credit that most income-shares states use:

    transfer = (duplication factor) x (time share) x 4c x (difference in income shares)

Box 1 without the limitation gives 1.00 x 4c x (difference in income shares). At the
equal time Box 1 describes, the time share is 0.5, so the duplication factor implied
by the arithmetic is 2.0 -- the assumption that two households cost twice one. No
published estimate supports that. Indiana's Child Support Guideline 6 Commentary,
the only state commission to have quantified it, puts 50% of the basic obligation as
duplicated at equal parenting, which is a factor of 1.5.

A larger duplication factor means a LARGER transfer, so 2.0 is the harshest available
assumption, not the most generous. The three variants below are the ways out.

THE VARIANTS
------------
current  CJ-D 304 as transcribed.
A        The 6e limitation stops reducing a credit. Compute 6g from 6c unlimited,
         then apply the limitation once to the transfer, in the Box 2 form at 7a/7b.
         Smallest possible change; touches one line; restores the k=2.0 cross-credit.
B        A, plus one new sub-line under Box 1: multiply Line 5b by 0.75, which is a
         duplication factor of 1.5 at the equal time Box 1 already describes.
         Needs no new worksheet input, because Box 1 IS the equal-time case.
C        B, with 0.75 replaced by 1.5 x the other parent's share of overnights. At
         equal time this is identical to B. It also disposes of the one-third-to-half
         band that section II.D.4 currently routes to judicial deviation.
         This is the one that needs a new field, so it is the largest ask.

SCOPE. Every variant here is modelled for Box 1 ONLY. Box 3 shares the Box 1 path on
the form, so the same reversal at 6e must arise there, but this module does not model
Box 3 and the submission must not claim it does -- section 5.1 finds a defect running
in the opposite direction under Box 3, and the interaction is unchecked. Nothing here
touches Table A, the tranches, the $450,000 ceiling, or the $430-per-child benchmark.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worksheet as w  # noqa: E402

VARIANTS = ("current", "A", "B", "C")

# Indiana Child Support Guideline 6 Commentary: at equal parenting, 50% of the basic
# child support obligation is duplicated. Duplication factor 1.5, halved by the equal
# time share, gives the 0.75 applied to Line 5b.
DUPLICATION = 1.5


def run(variant, a_gross, b_gross, children_under18, children_18plus=0,
        a_health=0.0, b_health=0.0, a_childcare=(), b_childcare=(),
        a_overnight_share=0.5):
    """Box 1 line by line, under one of the four variants.

    Parent A / Parent B follow the worksheet's convention. `a_overnight_share` is
    Parent A's share of overnights and is used by variant C only; every other variant
    ignores it, which is precisely the defect being modelled.
    """
    if variant not in VARIANTS:
        raise ValueError(f"variant must be one of {VARIANTS}, got {variant!r}")

    n_u18, n_18p = children_under18, children_18plus

    # --- Section I / Line 3, identical in every variant
    a3a = max(0.0, a_gross - a_health)
    b3a = max(0.0, b_gross - b_health)
    b3b = a3a + b3a
    a3c = a3a / b3b if b3b else 0.0
    b3c = b3a / b3b if b3b else 0.0
    e3e = w.table_a(min(b3b, w.CAP))

    # --- Lines 3f-4c. Box 1 puts every child in BOTH columns, so the two are equal.
    f3f = w.TABLE_B[min(n_u18 + n_18p, 5)]
    g3g = e3e * f3f
    c4c = g3g - g3g * w.TABLE_C.get((n_u18, n_18p), 0.0)

    # --- Line 5. 5b is what the OTHER parent owes this parent, so it carries the
    # other parent's income share. Variants B and C scale it by the duplication
    # factor and the time share; the current form scales it by nothing.
    if variant == "B":
        d_a = d_b = DUPLICATION * 0.5
    elif variant == "C":
        # 5b is what the OTHER parent owes this parent, so it carries the time THIS
        # parent has the children: B owes A for A's overnights, and vice versa.
        d_a = DUPLICATION * a_overnight_share
        d_b = DUPLICATION * (1.0 - a_overnight_share)
    else:
        d_a = d_b = 1.0

    a5b = c4c * b3c * d_a
    b5b = c4c * a3c * d_b

    # 5c's low-income substitution is a strict IF/ELSE and is left exactly as written.
    a5c = a5b if b3a > w.LOW_INCOME else w.table_a(b3a)
    b5c = b5b if a3a > w.LOW_INCOME else w.table_a(a3a)
    # Where 5c substitutes the shaded-area amount, Line 5b (and so the duplication
    # factor) is discarded for that column. The cross-credit algebra below no longer
    # describes the order, which is why implied_overnight_share() refuses these.
    low_income_5c = (b3a <= w.LOW_INCOME) or (a3a <= w.LOW_INCOME)

    # --- Line 6a/6b child care, unchanged by every variant
    a6a = w._cc_benchmarked(list(zip(a_childcare, b_childcare))) if a_childcare else 0.0
    b6a = w._cc_benchmarked([(y, x) for x, y in zip(a_childcare, b_childcare)]) if b_childcare else 0.0
    a6c = a5c + b3c * a6a
    b6c = b5c + a3c * b6a

    # --- Line 6d/6e, the income-disparity limitation
    if variant == "current":
        a6d = 1.0 if a3a == 0 else a6c / a3a
        b6d = 1.0 if b3a == 0 else b6c / b3a
        a6e = a6c if a6d >= 0.10 else w._floor(min(a6c, (a6d + 0.10) * b3a), b3a)
        b6e = b6c if b6d >= 0.10 else w._floor(min(b6c, (b6d + 0.10) * a3a), a3a)
    else:
        # Variants A, B and C: the limitation no longer reduces either column's
        # credit. It is applied once, to the transfer, below.
        a6d = b6d = None
        a6e, b6e = a6c, b6c

    # --- Line 6f/6g
    if a6e >= b6e:
        recip, payor = "A", "B"
        r6e, p6e, payor_3a, recip_3a = a6e, b6e, b3a, a3a
    else:
        recip, payor = "B", "A"
        r6e, p6e, payor_3a, recip_3a = b6e, a6e, a3a, b3a
    g6g = max(0.0, r6e - p6e)

    # --- Line 7. The current form applies no limitation here under Box 1 (it already
    # applied one at 6e). Variants A-C apply the Box 2 limitation instead, which caps
    # the payor's share of his own income by reference to the recipient's.
    if variant == "current":
        a7a = None
        b7b = g6g
    else:
        a7a = 1.0 if recip_3a == 0 else g6g / recip_3a
        b7b = g6g if a7a >= 0.10 else w._floor(
            min(p6e, g6g, (a7a + 0.10) * payor_3a), payor_3a)

    d7d = max(0.0, b7b)
    e7e = 1.0 if payor_3a == 0 else d7d / payor_3a

    return {
        "variant": variant, "low_income_5c": low_income_5c, "A_3a": a3a, "B_3a": b3a, "A_3c": a3c, "B_3c": b3c,
        "3e": e3e, "4c": c4c, "A_5b": a5b, "B_5b": b5b, "A_5c": a5c, "B_5c": b5c,
        "A_6c": a6c, "B_6c": b6c, "A_6d": a6d, "B_6d": b6d,
        "A_6e": a6e, "B_6e": b6e, "recipient": recip, "payor": payor,
        "6g": g6g, "7a": a7a, "7d": d7d, "7e": e7e, "hardship_box": e7e >= 0.40,
        "payor_3a": payor_3a,
    }


# ---------------------------------------------------------------------------
# The worked example and the income-share sweep
# ---------------------------------------------------------------------------

PAYOR_GROSS_WEEKLY = 201_000.0 / 52.0
RECIP_WEEKLY = 570.0
KIDS = 3
A_HEALTH, B_HEALTH = 33.0, 43.0

# The sweep holds the payor's income, the children and the equal parenting fixed and
# varies only the other parent's income. Same construction as submission section 5.
SWEEP_RECIPIENT_WEEKLY = (2500.0, 1800.0, 1200.0, 900.0, 700.0, 570.0, 400.0, 250.0)

# The grid behind section 5's FIRST table, carried over from model/submission_figures.py
# so that section 5 is sourced to one script rather than two.
SECTION5_ORIGINAL_GRID = (3000.0, 2000.0, 1200.0, 570.0, 200.0)


def implied_overnight_share(result, duplication=DUPLICATION):
    """The payor overnight share a cross-credit would need to produce this order.

    Variant C's transfer is D x 4c x (payor's income share - payor's overnight
    share), because the two income shares sum to one, so the inversion is exact.
    Answers: the parent has the children half the time; what fraction is the order
    actually priced at? The answer moves with `duplication`, so quote the factor
    alongside it or the number means nothing.

    Returns None where Line 5c has substituted the shaded-area amount for a column,
    because the order is then not a cross-credit at all and the inversion is void.
    """
    if result["low_income_5c"]:
        return None
    payor_share = result["B_3c"] if result["payor"] == "B" else result["A_3c"]
    return payor_share - result["7d"] / (duplication * result["4c"])


def _box2(a_gross=RECIP_WEEKLY):
    return w.run(box=2, a_gross=a_gross, b_gross=PAYOR_GROSS_WEEKLY,
                 children_under18=KIDS, a_health=A_HEALTH, b_health=B_HEALTH)


def _variant(variant, a_gross=RECIP_WEEKLY):
    return run(variant, a_gross=a_gross, b_gross=PAYOR_GROSS_WEEKLY,
               children_under18=KIDS, a_health=A_HEALTH, b_health=B_HEALTH)


def main():
    print("=" * 78)
    print("BOX 1 SHARED PARENTING -- CURRENT MECHANICS AND THREE REDLINES")
    print("=" * 78)
    print("Worked example: payor $201,000/yr, other parent $570/wk, three children,")
    print("equal parenting, no child care. Every figure below is weekly.\n")

    cur = _variant("current")
    b2 = _box2()

    print("-- Where the credit goes, under the form as written --")
    print(f"  Line 4c   total support amount, both columns      ${cur['4c']:>9,.2f}")
    print(f"  A's 5b    4c x B's income share {cur['B_3c']:.4f}         ${cur['A_5b']:>9,.2f}")
    print(f"  B's 5b    4c x A's income share {cur['A_3c']:.4f}         ${cur['B_5b']:>9,.2f}")
    print(f"  B's 6d    his column entitlement / his own 3a     {cur['B_6d']:>9.4f}")
    print(f"  B's 6e    limited to (6d + 10%) x A's 3a          ${cur['B_6e']:>9,.2f}"
          f"   <- ${cur['B_5b'] - cur['B_6e']:,.2f} removed")
    print(f"  6g = 7d   A's 6e less B's 6e                      ${cur['7d']:>9,.2f}")
    print(f"  Box 2 order for the same family                   ${b2['7d']:>9,.2f}")
    print(f"  credit for equal parenting                        "
          f"${b2['7d'] - cur['7d']:>9,.2f}   {(b2['7d'] - cur['7d']) / b2['7d']:.1%}")
    print(f"  and the credit equals the payor's own 6e:         "
          f"{abs((b2['7d'] - cur['7d']) - cur['B_6e']) < 0.01}\n")

    print("-- The cross-credit equivalence --")
    print("   Box 1 puts every child in BOTH columns at Table B, so the two households")
    print("   are together charged twice the schedule amount for the same children.")
    print(f"     Line 4c, each column                           ${cur['4c']:>9,.2f}")
    print(f"     charged across the two columns                 ${cur['4c'] * 2:>9,.2f}")
    print(f"     Box 2, one household                           ${cur['4c']:>9,.2f}")
    print("   Written as the cross-credit most income-shares states use --")
    print("     transfer = D x (time share) x 4c x (difference in income shares)")
    print("   -- and solved at the equal time Box 1 describes, Box 1 without the 6e")
    print("   limitation is the D = 2.00 case. Transfers at each D:")
    spread = cur["4c"] * (cur["B_3c"] - cur["A_3c"])
    for d in (2.0, DUPLICATION, 1.0):
        print(f"     D = {d:.2f}   transfer ${d * 0.5 * spread:>9,.2f}/wk   "
              f"{(b2['7d'] - d * 0.5 * spread) / b2['7d']:>6.1%} below the Box 2 order")
    print("   Indiana Child Support Guideline 6 Commentary is the only state finding")
    print(f"   that quantifies the duplication: 50% at equal parenting, so D = {DUPLICATION}.\n")

    print("-- What each redline produces at the worked example --")
    print(f"  {'variant':<9} {'order/wk':>10} {'order/yr':>11} {'vs Box 2':>10} "
          f"{'credit':>8} {'Line 7e':>9}")
    for v in VARIANTS:
        r = _variant(v)
        print(f"  {v:<9} ${r['7d']:>9,.2f} ${r['7d'] * 52:>10,.0f} "
              f"${r['7d'] - b2['7d']:>9,.2f} {(b2['7d'] - r['7d']) / b2['7d']:>7.1%} "
              f"{r['7e']:>8.1%}")
    for v in ("A", "B"):
        r = _variant(v)
        print(f"  change from the current order under {v}: "
              f"{(cur['7d'] - r['7d']) / cur['7d']:.1%}  (${cur['7d']:,.2f} -> ${r['7d']:,.2f})")
    print()

    print("-- The credit across income disparity, which is the whole argument --")
    print("   Payor's income and the children are fixed; only the other parent's")
    print("   income moves. Percentages are the reduction from the Box 2 order.\n")
    print(f"  {'other parent':>13} {'payor':>7} | {'current':>18} | {'A':>18} | "
          f"{'B':>18}")
    print(f"  {'weekly gross':>13} {'share':>7} | {'order':>9}{'credit':>9} | "
          f"{'order':>9}{'credit':>9} | {'order':>9}{'credit':>9}")
    print("  " + "-" * 74)
    for a in SWEEP_RECIPIENT_WEEKLY:
        base = _box2(a)["7d"]
        cells = []
        for v in ("current", "A", "B"):
            r = _variant(v, a)
            cells.append(f"${r['7d']:>8,.0f}{(base - r['7d']) / base:>9.1%}")
        share = _variant("current", a)["B_3c"]
        print(f"  ${a:>12,.0f} {share:>7.1%} | {cells[0]} | {cells[1]} | {cells[2]}")
    print()

    print("-- What equal parenting is currently worth, priced as parenting time --")
    print("   Variant C's transfer is D x 4c x (B's income share - B's overnight")
    print("   share), because the two income shares sum to one. Solving that for the")
    print("   overnight share that reproduces the CURRENT Box 1 order answers: how")
    print("   much parenting time is Massachusetts actually pricing equal parenting")
    print("   at? Every row below is a parent with the children half the time.\n")
    print("   The answer depends on the duplication factor it is measured against, so")
    print("   both are shown: Indiana's 1.5, and the 2.0 that Box 1's own arithmetic")
    print("   already implies. Neither reaches the half the parent actually has.\n")
    print(f"  {'other parent':>13} {'payor':>7} {'current':>10}  {'priced at':>10} {'priced at':>10}")
    print(f"  {'weekly gross':>13} {'share':>7} {'order':>10}  {'D = 1.5':>10} {'D = 2.0':>10}")
    print("   n/a: Line 5c substitutes the shaded-area amount below $391 of available")
    print("        income, so the order is no longer a cross-credit and cannot be")
    print("        expressed as one.")
    print("  " + "-" * 56)
    for a in SWEEP_RECIPIENT_WEEKLY:
        r = _variant("current", a)
        i15, i20 = implied_overnight_share(r, DUPLICATION), implied_overnight_share(r, 2.0)
        fmt = lambda x: "n/a" if x is None else f"{x:.1%}"
        print(f"  ${a:>12,.0f} {r['B_3c']:>7.1%} ${r['7d']:>9,.2f}  "
              f"{fmt(i15):>10} {fmt(i20):>10}")
    print()

    print("-- Variant C: the credit tracking parenting time --")
    print("   Other parent at $570/wk throughout; only the overnight split moves.")
    print("   Section II.D.4 currently sends everything between a third and a half")
    print("   to judicial deviation, which is why the middle rows have no formula.\n")
    print(f"  {'payor overnights':>17} {'C order':>10} {'vs Box 2':>10} {'credit':>8}")
    for payor_share in (0.50, 0.45, 0.40, 0.35, 1.0 / 3.0):
        r = run("C", a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS_WEEKLY,
                children_under18=KIDS, a_health=A_HEALTH, b_health=B_HEALTH,
                a_overnight_share=1.0 - payor_share)
        print(f"  {payor_share:>16.1%} ${r['7d']:>9,.2f} "
              f"${r['7d'] - b2['7d']:>9,.2f} {(b2['7d'] - r['7d']) / b2['7d']:>7.1%}")
    print()

    print("-- Section 5's opening table, reproduced from this module --")
    print(f"  {'payor':>7} {'Box 2':>10} {'Box 1':>10} {'reduction':>10}")
    for a in SECTION5_ORIGINAL_GRID:
        r, base = _variant("current", a), _box2(a)["7d"]
        print(f"  {r['B_3c']:>7.1%} ${base:>9,.0f} ${r['7d']:>9,.0f} "
              f"{(base - r['7d']) / base:>10.1%}")
    print()

    print("-- The redlines with child care present --")
    print("   The letter's lead example turns on child care, and 6c (the line the")
    print("   first redline moves) includes the child care allocation at 6b. If the")
    print("   fix behaved differently once 6a is populated, the ask would be unsafe.\n")
    print(f"  {'child care/wk':>13} {'current':>10} {'A':>10} {'B':>10} {'A credit':>9} {'B credit':>9}")
    for cc in (0.0, 150.0, 300.0, 600.0, 1290.0):
        per = cc / 3.0
        kw = dict(a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS_WEEKLY, children_under18=KIDS,
                  a_health=A_HEALTH, b_health=B_HEALTH,
                  a_childcare=(per, per, per), b_childcare=(0.0, 0.0, 0.0))
        base = w.run(box=2, **kw)["7d"]
        cur_, va, vb = (run(v, **kw) for v in ("current", "A", "B"))
        print(f"  ${cc:>12,.0f} ${cur_['7d']:>9,.2f} ${va['7d']:>9,.2f} ${vb['7d']:>9,.2f} "
              f"{(base - va['7d']) / base:>9.1%} {(base - vb['7d']) / base:>9.1%}")
    print()

    print("-- The symmetric case: the LOWER earner is the payor --")
    print("   Section 5.1 finds that Box 3's defect cuts against the lower earner, so")
    print("   the redlines have to be checked for overcorrection in the other")
    print("   direction. Parent A here earns more; the payor is whoever 6f names.\n")
    print(f"  {'A weekly':>9} {'B weekly':>9} {'payor':>6} {'current':>10} {'A':>10} {'B':>10}")
    for a_wk, b_wk in ((3822.0, 570.0), (2000.0, 1200.0), (1200.0, 900.0), (900.0, 800.0)):
        kw = dict(a_gross=a_wk, b_gross=b_wk, children_under18=KIDS,
                  a_health=A_HEALTH, b_health=B_HEALTH)
        rows = [run(v, **kw) for v in ("current", "A", "B")]
        print(f"  ${a_wk:>8,.0f} ${b_wk:>8,.0f} {rows[0]['payor']:>6} "
              + " ".join(f"${r['7d']:>9,.2f}" for r in rows))
    print()

    print("-- Sanity gate --")
    print("   Variant 'current' must reproduce worksheet.run(box=1) exactly, or none")
    print("   of the above means anything. Run model/test_box1_fix.py.")
    ref = w.run(box=1, a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS_WEEKLY,
                children_under18=KIDS, a_health=A_HEALTH, b_health=B_HEALTH)
    print(f"   worksheet.run(box=1) 7d = ${ref['7d']:,.2f}; "
          f"box1_fix 'current' 7d = ${cur['7d']:,.2f}; "
          f"match = {abs(ref['7d'] - cur['7d']) < 0.005}")


if __name__ == "__main__":
    main()
