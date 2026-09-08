#!/usr/bin/env python3
"""Every figure quoted in output/DRAFT-submission-to-trial-court.md, in one place.

WHY THIS EXISTS
---------------
A number that lives only in a chat transcript or only in a prose document cannot be
re-checked, and a wrong number in front of the Task Force is unrecoverable. Each
figure the submission asserts is printed here, by the section that uses it, from
`worksheet.py` (CJ-D 304, transcribed) and `net_position.py` (tax model).

    .venv/bin/python model/submission_figures.py

Run `model/test_worksheet.py` and `model/test_guidelines.py` first -- both must pass
before anything printed here goes into the submission.

THE WORKED EXAMPLE. ** These are the author's own case parameters, not a constructed
hypothetical. ** The submission discloses this; the figures are real either way. Parameters, all weekly except where noted:

    Parent B (payor)      $201,000/yr gross, health premium $43
    Parent A (recipient)  $570/wk gross,     health premium $33
    Three children, two under 13 and one aged 13 to 17
    Box 1 -- shared financial responsibility and parenting time

These sit inside the presumptive range (combined available income well under $8,654/wk)
and involve no imputed income, no dependency benefit, and no children over 18, so the
example exercises the ordinary path through the worksheet.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import net_position as npos  # noqa: E402
import worksheet as w  # noqa: E402

PAYOR_GROSS = 201_000.0
RECIP_WEEKLY = 570.0
RECIP_GROSS = RECIP_WEEKLY * 52.0
KIDS = 3
# Two under 13 and one aged 13 to 17. All three are under 18 (so Table C does not engage) and all three
# are federal EITC qualifying children (under 19) and federal CTC eligible (under 17).
# Only the 5- and 8-year-old are under 13, so the MA Child and Family Tax Credit
# ($440, M.G.L. c. 62 s. 6(x)) reaches TWO of the three, not all three.
KIDS_UNDER_13 = 2


def sheet(cc_total, box=1):
    per = cc_total / 3.0
    return w.run(box=box, a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS / 52.0,
                 children_under18=KIDS, a_health=33.0, b_health=43.0,
                 a_childcare=(per, per, per), b_childcare=(0, 0, 0))


def position(r, cc_total):
    """Net position implied by a worksheet result.

    The payor's child care share is ALREADY INSIDE the order: 6b flows through
    6c -> 6e -> 6g -> 7b -> 7d, which is why $300/wk of claimed child care raises
    7d by $263/wk. So `payor_childcare_share` is 0 here -- charging him 6b again
    on top of 7d double-counts it, which an earlier version of this script did.
    The recipient pays the provider and is reimbursed through the order, so the
    full child care amount is subtracted from her side."""
    return npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, r["7d"], cc_total, 0.0,
                        kids_under_13=KIDS_UNDER_13)


def solve_7e_40():
    """Weekly child care at which Line 7e first reaches 40% and the box checks."""
    lo, hi = 0.0, 1290.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if sheet(mid)["7e"] < 0.40:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    print(__doc__.split("THE WORKED EXAMPLE.")[1].split("These sit")[0].strip())
    print()

    r0, r300 = sheet(0), sheet(300)
    p0, p300 = position(r0, 0), position(r300, 300)

    print("== TAX POSITION (net_position.py; federal AND MA constants verified 2026-09-02) ==")
    print(f"  payor effective rate      {p0['payor_eff_rate']:+.1%}")
    print(f"  recipient effective rate  {p0['recip_eff_rate']:+.1%}   "
          f"(negative = net refundable credits)")
    print(f"  spread                    "
          f"{(p0['payor_eff_rate'] - p0['recip_eff_rate']) * 100:.0f} points")
    print()

    print("== SECTION 1 -- the Line 7e units lag ==")
    print(f"  {'child care/wk':>14} {'order/wk':>10} {'order/yr':>11} "
          f"{'7e reads':>9} {'true % of net':>14} {'box':>5}")
    trigger = solve_7e_40()
    for cc in [0, 100, 300, trigger, 3 * 430]:
        r = sheet(cc)
        p = position(r, cc)
        print(f"  {cc:>14,.0f} {r['7d']:>10,.0f} {r['7d']*52:>11,.0f} "
              f"{r['7e']:>9.1%} {p['burden_pct_of_payor_net']:>14.1%} "
              f"{'YES' if r['hardship_box'] else '-':>5}")
    print(f"  Line 7e first reaches 40% at ${trigger:,.0f}/wk of child care "
          f"({trigger/3:,.0f}/child), which is {trigger/(3*430):.0%} of the "
          f"${3*430:,} statutory benchmark.")
    print(f"  At that point the payor's true burden is "
          f"{position(sheet(trigger), trigger)['burden_pct_of_payor_net']:.1%} of net -- "
          f"a lag of "
          f"{(position(sheet(trigger), trigger)['burden_pct_of_payor_net'] - 0.40)*100:.0f}"
          f" points.")
    print()

    print("== SECTION 2 -- household standard of living (IV.B.13) ==")
    for label, r, p, cc in [("no child care", r0, p0, 0), ("$300/wk child care", r300, p300, 300)]:
        print(f"  {label:<20} payor keeps ${p['payor_after']:>9,.0f}   "
              f"recipient household ${p['recip_after']:>9,.0f}   "
              f"payor share {p['payor_after_share']:.1%}")
    print(f"  Per person the payor still leads: ${p0['payor_after']:,.0f} for one "
          f"against ${p0['recip_per_person']:,.0f} each for four. State this.")
    print()

    print("== SECTION 4 -- who funds claimed child care ==")
    cc = 300.0
    delta_yr = (r300["7d"] - r0["7d"]) * 52
    spend_yr = cc * 52
    print(f"  claimed by recipient          ${spend_yr:,.0f}/yr (${cc:,.0f}/wk)")
    print(f"  increase in the order         ${delta_yr:,.0f}/yr "
          f"(${r300['7d']-r0['7d']:,.0f}/wk)")
    print(f"  payor's 6b allocation         {r300['A_6b']/cc:.2%} "
          f"(= recipient's 3c is {r0['A_3c']:.2%}; payor's 3c is {r0['B_3c']:.2%})")
    print(f"  share of the expense funded by the payor via the order: "
          f"{delta_yr/spend_yr:.0%}")
    print()

    print("== SECTION 5 -- the shared-parenting differential ==")
    b1, b2 = sheet(0, box=1), sheet(0, box=2)
    print(f"  Box 2 (children reside with A ~2/3 of the time)  ${b2['7d']:,.0f}/wk "
          f"(${b2['7d']*52:,.0f}/yr)")
    print(f"  Box 1 (shared equally)                           ${b1['7d']:,.0f}/wk "
          f"(${b1['7d']*52:,.0f}/yr)")
    print(f"  difference {1 - b1['7d']/b2['7d']:.1%}  =  "
          f"${(b2['7d']-b1['7d'])*52:,.0f}/yr for moving from about one third of "
          f"the parenting time to half of it.")
    print("  Mechanism (CJ-D 304 6f/6g): at Box 2 the payor's column carries 0 children,")
    print("  so Table B = 0.00 and 6g reduces to the difference in income shares. No")
    print("  parenting-time quantity enters the arithmetic at any line.")
    print()

    print("== SECTION 5 -- the shared-parenting adjustment across income disparity ==")
    print(f"  {'payor 3c':>9} {'Box 2':>8} {'Box 1':>8} {'reduction':>10}")
    for a in (3000, 2500, 2000, 1600, 1200, 800, 570, 400, 200):
        kk = dict(b_gross=PAYOR_GROSS / 52.0, children_under18=KIDS,
                  a_health=33.0, b_health=43.0)
        x1 = w.run(box=1, a_gross=a, **kk)
        x2 = w.run(box=2, a_gross=a, **kk)
        print(f"  {x1['B_3c']:>9.1%} {x2['7d']:>8,.0f} {x1['7d']:>8,.0f} "
              f"{1 - x1['7d']/x2['7d']:>10.1%}")
    print("  Same children, same equal-parenting arrangement. Only the other parent's")
    print("  income varies. No parenting-time quantity enters any line of the worksheet.")
    print()

    print("== SECTION 5.1 -- Box 3 (split): identical care, different box ==")
    kk = dict(b_gross=PAYOR_GROSS / 52.0, a_health=33.0, b_health=43.0)
    t1 = w.run(box=1, a_gross=RECIP_WEEKLY, children_under18=2, **kk)
    t3 = w.run(box=3, a_gross=RECIP_WEEKLY, children_under18=2,
               a_children=(1, 0), b_children=(1, 0), **kk)
    print(f"  Box 1  shared 50-50 of 2 children   ${t1['7d']:>6,.0f}/wk   "
          f"(payor: 2 x 50% = 1.0 child-share)")
    print(f"  Box 3  one child residing with each ${t3['7d']:>6,.0f}/wk   "
          f"(payor: 1 x 100% = 1.0 child-share)")
    print(f"  difference {1 - t3['7d']/t1['7d']:.1%}  =  ${(t1['7d']-t3['7d'])*52:,.0f}/yr")
    print(f"  driver: 6g nets the columns on the ONE-child schedule. "
          f"TableB(1)/TableB(2) = {w.TABLE_B[1]/w.TABLE_B[2]:.3f}")
    print(f"  but a split DESTROYS the economies of scale Table B exists to capture:")
    print(f"  combined factor across two homes is "
          f"{w.TABLE_B[1]*2:.2f} vs {w.TABLE_B[2]:.2f} in one home "
          f"({w.TABLE_B[1]*2/w.TABLE_B[2]-1:+.0%} more expensive).")
    print()
    for a, b in [((2, 0), (1, 0)), ((1, 0), (2, 0))]:
        r = w.run(box=3, a_gross=RECIP_WEEKLY, children_under18=3,
                  a_children=a, b_children=b, **kk)
        base = sheet(0)
        print(f"  3 children, split A={a[0]} B={b[0]}: ${r['7d']:,.0f}/wk "
              f"vs Box 1 ${base['7d']:,.0f}  ({1-r['7d']/base['7d']:.1%} lower)")
    print()

    print("== SECTION 2 -- child care ignores the parenting box; the payor's own credit is clipped ==")
    kk = dict(a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS / 52.0, children_under18=KIDS,
              a_health=33.0, b_health=43.0)
    cc = (100.0, 100.0, 100.0)
    hers = {b: w.run(box=b, a_childcare=cc, b_childcare=(0, 0, 0), **kk) for b in (1, 2)}
    his = {b: w.run(box=b, a_childcare=(0, 0, 0), b_childcare=cc, **kk) for b in (1, 2)}
    base = {b: w.run(box=b, **kk) for b in (1, 2)}
    print(f"  recipient pays $300/wk: payor's 6b share ${hers[1]['A_6b']:,.2f}/wk under Box 1, "
          f"${hers[2]['A_6b']:,.2f} under Box 2 (identical; no parenting-time term)")
    for b in (2, 1):
        print(f"  payor pays $300/wk himself, Box {b}: order falls ${base[b]['7d'] - his[b]['7d']:,.2f}/wk "
              f"({(base[b]['7d'] - his[b]['7d']) / 300:.1%} of face value)")
    _r = w.run(box=1, a_gross=570.0, b_gross=201000 / 52.0, children_under18=3, a_health=33.0, b_health=43.0, b_childcare=(300.0,))
    print(f"  payor's Line 6d where the payor pays $300/wk child care under Box 1 = {_r['B_6d']:.2%} (below 10%, so 6e limits)")
    print(f"  payor's share of combined GROSS income = {(201000/52.0)/(201000/52.0+570.0):.2%}")
    print(f"  clip factor under Box 1 = recipient 3a / payor 3a = "
          f"{base[1]['A_3a']:.0f}/{base[1]['B_3a']:.0f} = {base[1]['A_3a'] / base[1]['B_3a']:.1%}")
    print()

    print("== SECTION 2.1 -- BOTH parents pay child care under equal shared parenting ==")
    print("  The realistic 50-50 case: each parent needs care during their own parenting time.")
    pn = npos.net_income(PAYOR_GROSS, "single", 0, npos.TAX_PARAMS)
    rn = npos.net_income(RECIP_GROSS, "hoh", KIDS, npos.TAX_PARAMS,
                         kids_under_13=KIDS_UNDER_13)
    kk = dict(a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS / 52.0, children_under18=KIDS,
              a_health=33.0, b_health=43.0)
    rows = [("neither pays child care", (0, 0, 0), (0, 0, 0)),
            ("only the recipient pays $300/wk", (100, 100, 100), (0, 0, 0)),
            ("BOTH pay $300/wk", (100, 100, 100), (100, 100, 100))]
    out = {}
    for label, a, b in rows:
        r = w.run(box=1, a_childcare=a, b_childcare=b, **kk)
        order, his_cc, her_cc = r["7d"] * 52, sum(b) * 52, sum(a) * 52
        him, her = pn - order - his_cc, rn + order - her_cc
        out[label] = (order, his_cc, him, her)
        print(f"  {label:<34} order ${r['7d']:>6,.0f}/wk  7e {r['7e']:>5.1%}")
        print(f"  {'':<34} he keeps ${him:>9,.0f}   she holds ${her:>9,.0f}   "
              f"his share {him/(him+her):>5.1%}")
        print(f"  {'':<34} order+his own care = {(order+his_cc)/pn:.1%} of his net")
    o_none = out["neither pays child care"]
    o_both = out["BOTH pay $300/wk"]
    o_hers = out["only the recipient pays $300/wk"]
    total_cc = 300 * 52 * 2
    his_extra = (o_both[0] + o_both[1]) - o_none[0]
    her_extra = o_none[3] - o_both[3]
    print(f"  Combined child care across both households: ${total_cc:,.0f}/yr")
    print(f"    borne by the payor:     ${his_extra:>9,.0f}  ({his_extra/total_cc:.0%})")
    print(f"    borne by the recipient: ${her_extra:>9,.0f}  ({her_extra/total_cc:.0%})")
    print(f"  The payor's OWN ${300*52:,.0f} of child care reduces the order by "
          f"${o_hers[0]-o_both[0]:,.0f}/yr -- the Line 6e clip.")
    print("  CAVEAT, state it: per person the payor still leads -- "
          f"${o_both[2]:,.0f} for one against ${o_both[3]/4:,.0f} each for four.")
    print()

    print("== CAVEATS THAT TRAVEL WITH EVERY FIGURE ==")
    print("  1. Per person the payor leads. Say it before the household comparison.")
    print("  2. $430/child is a statutory ceiling, not a typical amount. Lead with the")
    print(f"     ${trigger:,.0f}/wk trigger point, never the ${3*430:,} maximum.")
    print("  3. One worked example is not a distribution. The frequency of claimed")
    print("     child care near the benchmark is unknown -- which is why the submission")
    print("     supports better data collection rather than asserting a prevalence.")
    print("  4. The MA Child and Family Tax Credit ($440/dependent) requires the child to be")
    print(f"     UNDER 13. At two under 13 and one aged 13 to 17 exactly {KIDS_UNDER_13} of the 3 qualify, which is what")
    print("     the figures above use. Sensitivity across the whole range:")
    import net_position as _n
    for k13 in (3, 2, 1, 0):
        net = _n.net_income(RECIP_GROSS, "hoh", KIDS, _n.TAX_PARAMS, kids_under_13=k13)
        print(f"       {k13} child(ren) under 13: {1 - net/RECIP_GROSS:+.1%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
