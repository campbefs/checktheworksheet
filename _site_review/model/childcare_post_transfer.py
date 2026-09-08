"""Child care allocated on POST-transfer shares instead of Line 3c.

The question: once base support has moved money between the households, the parties' shares of
combined income are no longer the Line 3c shares. What does child care look like on the shares that
actually exist after the transfer?

This is the basis of the letter's Section 2 redline (v4.6): new Worksheet Line 6b-1, each parent's
Line 3a moved by the base order (the Line 7d that results with Lines 6a and 6b at zero), using the
Payor/Recipient designations Line 6f gives in that case, divided by Line 3b; Line 6b then uses the
other parent's 6b-1 in place of Line 3c.

At the letter's worked example ($201,000 / $570 per week, three children, Box 1, $300/wk child care
paid by Parent A) the script prints the payor's share of that child care under:

  1.  current Worksheet: Line 3c, pre-transfer available income (what CJ-D 304 does);
  2.  post-transfer GROSS shares: (payor gross - base order) : (recipient gross + base order);
  2b. the redline as drafted: the same on Line 3a, over Line 3b — a fallback, not the ask;
  3.  post-transfer NET shares, after tax, from net_position.py — depends on filing status and
      who claims the children, facts CJ-D 304 does not collect;
  4.  rule 3 including the child care the recipient pays the provider (fixed point; equals rule 3);
  5.  post-transfer NET shares on the withholding basis (net_position.net_income_withholding_
      basis: tax and FICA only, no refundable credits) — the ask. Needs only gross income and the
      published schedules, so it is the version a Worksheet line can actually compute.

Pinned by model/test_childcare_post_transfer.py. Run: .venv/bin/python model/childcare_post_transfer.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import net_position as npos  # noqa: E402
import worksheet as w  # noqa: E402

PAYOR_GROSS = 201_000.0
RECIP_WEEKLY = 570.0
RECIP_GROSS = RECIP_WEEKLY * 52.0
KIDS, KIDS_UNDER_13 = 3, 2
CC_WEEKLY = 300.0


def base_order():
    """Box 1 order with no child care: Line 7d."""
    r = w.run(box=1, a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS / 52.0, children_under18=KIDS,
              a_health=33.0, b_health=43.0)
    return r["7d"]


def current_rule():
    per = CC_WEEKLY / 3.0
    return w.run(box=1, a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS / 52.0, children_under18=KIDS,
                 a_health=33.0, b_health=43.0, a_childcare=(per, per, per), b_childcare=(0, 0, 0))


def figures():
    """Every number the letter's Section 2 redline quotes, in one dict."""
    base = base_order()
    cur = current_rule()
    cc_annual = CC_WEEKLY * 52
    f = {"base_7d": base, "current_7d": cur["7d"], "cc_annual": cc_annual}
    f["rule1_share"] = (cur["7d"] - base) * 52 / cc_annual

    p_g, r_g = PAYOR_GROSS - base * 52, RECIP_GROSS + base * 52
    f["rule2_gross_share"] = p_g / (p_g + r_g)

    # 2b: the redline. Payor/Recipient are the Line 6f designations with child care suppressed, which
    # for this example is Parent B / Parent A. Denominator is Line 3b (uncapped combined available
    # income), not the capped Line 3d, so the two shares sum to one above the $8,654/wk cap as well.
    a3, b3 = cur["A_3a"], cur["B_3a"]
    f["rule2b_share"] = (b3 - base) / (a3 + b3)
    f["rule2b_7d"] = base + f["rule2b_share"] * CC_WEEKLY
    f["rule2b_saving_yr"] = (cur["7d"] - f["rule2b_7d"]) * 52

    pos = npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, base, 0.0, 0.0, kids_under_13=KIDS_UNDER_13)
    f["rule3_share"] = pos["payor_after_share"]
    f["payor_after"], f["recip_after"], f["recip_pp"] = pos["payor_after"], pos["recip_after"], pos["recip_per_person"]

    share = f["rule3_share"]
    for _ in range(50):
        pos4 = npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, base, CC_WEEKLY, share, kids_under_13=KIDS_UNDER_13)
        new = pos4["payor_after_share"]
        if abs(new - share) < 1e-9:
            break
        share = new
    f["rule4_share"] = share

    # 5. THE ASK: post-transfer net shares on the WITHHOLDING basis (tax and FICA, single filer,
    # no exemptions -- no refundable credits, because CJ-D 304 collects neither filing status nor
    # who claims which child). The order moves, because Line 6b-1 sits inside the
    # 6b -> 6c -> 6e -> 6g -> 7b -> 7d chain: the same linear step the gross fallback (rule 2b)
    # already uses.
    p5 = npos.net_income_withholding_basis(PAYOR_GROSS)
    r5 = npos.net_income_withholding_basis(RECIP_GROSS)
    f["rule5_payor_net"], f["rule5_recip_net"] = p5, r5
    a5, b5 = p5 - base * 52, r5 + base * 52
    f["rule5_share"] = a5 / (a5 + b5)
    f["rule5_7d"] = base + f["rule5_share"] * CC_WEEKLY
    f["rule5_saving_yr"] = (cur["7d"] - f["rule5_7d"]) * 52

    f["pre_transfer_gross_share"] = PAYOR_GROSS / (PAYOR_GROSS + RECIP_GROSS)
    return f


def main():
    f = figures()
    cc = f["cc_annual"]
    print(f"Worked example: payor ${PAYOR_GROSS:,.0f}, recipient ${RECIP_GROSS:,.0f}, "
          f"{KIDS} children, Box 1, child care ${CC_WEEKLY:.0f}/wk paid by recipient")
    print(f"Base order (no child care)          ${f['base_7d']:,.0f}/wk  ${f['base_7d']*52:,.0f}/yr")
    print()
    print(f"1.  CURRENT (Line 3c, pre-transfer)       payor funds {f['rule1_share']:6.1%} of child care "
          f"(+${f['rule1_share']*cc:,.0f}/yr; order ${f['current_7d']:,.0f}/wk)")
    print(f"2.  POST-TRANSFER GROSS shares            payor {f['rule2_gross_share']:6.1%} -> funds ${f['rule2_gross_share']*cc:,.0f}/yr")
    print(f"2b. POST-TRANSFER on Line 3a (redline)    payor {f['rule2b_share']:6.1%} / recipient {1-f['rule2b_share']:6.1%}  "
          f"-> funds ${f['rule2b_share']*cc:,.0f}/yr; order ${f['rule2b_7d']:,.0f}/wk vs ${f['current_7d']:,.0f} "
          f"(saves ${f['rule2b_saving_yr']:,.0f}/yr)")
    print(f"3.  POST-TRANSFER NET shares              payor {f['rule3_share']:6.1%} / recipient {1-f['rule3_share']:6.1%}  "
          f"(${f['payor_after']:,.0f} vs ${f['recip_after']:,.0f})  -> funds ${f['rule3_share']*cc:,.0f}/yr")
    print(f"4.  POST-TRANSFER NET incl. child care    payor {f['rule4_share']:6.1%} (fixed point; equals rule 3)")
    print(f"5.  POST-TRANSFER NET, withholding basis  payor {f['rule5_share']:6.1%} / recipient "
          f"{1-f['rule5_share']:6.1%}  -> order ${f['rule5_7d']:,.2f}/wk vs ${f['current_7d']:,.2f} "
          f"(saves ${f['rule5_saving_yr']:,.0f}/yr)   <-- THE ASK")
    print(f"    payor net ${f['rule5_payor_net']:,.0f} ({1-f['rule5_payor_net']/PAYOR_GROSS:.1%} effective), "
          f"recipient net ${f['rule5_recip_net']:,.0f} ({1-f['rule5_recip_net']/RECIP_GROSS:.1%} effective)")
    print()
    print(f"Pre-transfer gross share (Line 3c basis, approx): payor {f['pre_transfer_gross_share']:6.1%}")
    print("Caveat that travels with every line: per person the payor still leads "
          f"(${f['payor_after']:,.0f} for one vs ${f['recip_pp']:,.0f} each for four, rule 3).")


if __name__ == "__main__":
    main()
