"""Ability to pay, defined: after-tax pay minus the child care the paying parent pays himself.

Added 2026-09-23 for the petition's definition ask. 45 C.F.R. 302.56(c)(1) requires every order to
be "based on ... ability to pay" and never defines it. The petition asks the federal rule to define
it as a number:

    ability-to-pay income = the payor's net pay (withholding basis: federal and state income tax,
                            Social Security and Medicare) minus the child care the payor pays
                            during his own parenting time
    presumptive order (child-care add-on included) may not exceed
        40 percent of it where the other parent has primary custody, and
        25 percent of it in joint custody (each parent at least a third of the time).

Reuses the Worksheet (model/worksheet.py) and the net-pay model already used for the 40/25 caps
(model/net_caps.py). No new tax or schedule arithmetic.

Run it: .venv/bin/python model/ability_to_pay.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import worksheet as w  # noqa: E402
import net_caps as nc  # noqa: E402
import ccpa_grid as cg  # noqa: E402

LIMIT = {1: 0.25, 2: 0.40}          # Box 1 joint custody, Box 2 the other parent has primary custody
PAYOR_GROSS = 201000.0
RECIP_WEEKLY = 570.0
KIDS = 3


def measure(payor_gross, recip_weekly, kids, box, recip_cc_total=0.0, payor_cc_total=0.0):
    """The order against ability-to-pay income. Child care totals are WEEKLY, across all children."""
    sheet = w.run(box=box, a_gross=recip_weekly, b_gross=payor_gross / 52.0, children_under18=kids,
                  a_health=cg.A_HEALTH, b_health=cg.B_HEALTH,
                  a_childcare=tuple([recip_cc_total / kids] * kids),
                  b_childcare=tuple([payor_cc_total / kids] * kids))
    order = sheet["7d"] * 52.0
    net = nc.net_income_withholding_basis(payor_gross)
    atp = net - payor_cc_total * 52.0
    share = order / atp if atp > 0 else float("inf")
    limit = LIMIT[box]
    return {"box": box, "order_annual": order, "order_weekly": sheet["7d"], "net": net,
            "payor_childcare_annual": payor_cc_total * 52.0, "atp": atp, "share_of_atp": share,
            "limit": limit, "over": share > limit, "allowed_weekly": limit * atp / 52.0}


def worked(box):
    """The worked example: $201,000 / $570 a week, three children, $100 a child a week of child care
    paid by each parent who has the children (both, in joint custody; the other parent alone under
    primary custody)."""
    payor_cc = 300.0 if box == 1 else 0.0
    return measure(PAYOR_GROSS, RECIP_WEEKLY, KIDS, box, 300.0, payor_cc)


def grid_share_over(box, per_child=100.0, kids=3):
    """Share of the published income grid whose order exceeds the limit, at per_child a week of child
    care paid by each parent who has the children."""
    pairs = cg.grid_pairs(kids, box)
    over = 0
    for hi, lo in pairs:
        r = measure(hi, lo / 52.0, kids, box, per_child * kids, per_child * kids if box == 1 else 0.0)
        over += r["over"]
    return over / len(pairs), over, len(pairs)


def cross_credit_worked(payor_cc_total=0.0, recip_cc_total=0.0, allocate_child_care=True):
    """Added 2026-09-25 for the cross-credit ask. The worked example at equal time under the
    cross-credit formula (model/box1_fix.py Variant B: duplication 1.5, no Line 6e limitation),
    measured against the same ability-to-pay income. Child care totals are WEEKLY.

    allocate_child_care=True runs child care through the Worksheet's split (Lines 6a/6b, income
    shares), which charges the payor 87.7% of the other parent's care and credits him 12.3% of his
    own. False is the proposed rule for joint custody: each parent bears the child care paid during
    his or her own time, so none enters the order, while ability to pay still subtracts the
    payor's own. Added the same day, from the question "if each parent pays $300 a week then I
    shouldn't be paying 38%"."""
    import box1_fix as bx
    kids = KIDS
    in_order = 1.0 if allocate_child_care else 0.0
    sheet = bx.run("B", RECIP_WEEKLY, PAYOR_GROSS / 52.0, kids, a_health=cg.A_HEALTH, b_health=cg.B_HEALTH,
                   a_childcare=tuple([in_order * recip_cc_total / kids] * kids) if in_order else (),
                   b_childcare=tuple([in_order * payor_cc_total / kids] * kids) if in_order else ())
    net = nc.net_income_withholding_basis(PAYOR_GROSS)
    atp = net - payor_cc_total * 52.0
    order = sheet["7d"] * 52.0
    basic = sheet["4c"]
    payor_share = sheet["B_3c"]          # Parent B is the payor in this call
    return {"order_weekly": sheet["7d"], "order_annual": order, "atp": atp,
            "share_of_atp": order / atp, "over_joint_limit": order / atp > LIMIT[1],
            # the arithmetic, step by step, for the site page
            "basic": basic, "enhanced": basic * bx.DUPLICATION, "payor_share": payor_share,
            "other_share": 1 - payor_share,
            "payor_part": basic * bx.DUPLICATION * payor_share,
            "other_part": basic * bx.DUPLICATION * (1 - payor_share),
            "payor_owes": sheet["A_5b"], "other_owes": sheet["B_5b"]}   # A's 5b is what B owes A



def cross_credit_post_transfer(payor_cc_total=300.0, recip_cc_total=300.0):
    """The cross-credit with child care split the way the Comments ask (section 2, "split on the money
    each parent has after the order"): each parent's share of ALL child care is that parent's share of
    net pay (withholding basis) after the base order moves between them, and each is credited with what
    he or she pays. Added 2026-09-25 (Chris: "Childcare should be split based on the money after the
    order for both parties"). Same one-step convention as model/childcare_post_transfer.py rule 5."""
    import net_position as npos
    base = cross_credit_worked(0.0, 0.0)["order_weekly"]
    p = npos.net_income_withholding_basis(PAYOR_GROSS)
    r = npos.net_income_withholding_basis(RECIP_WEEKLY * 52.0)
    a_, b_ = p - base * 52.0, r + base * 52.0
    share = a_ / (a_ + b_)
    total = payor_cc_total + recip_cc_total
    order = base + share * total - payor_cc_total
    atp = nc.net_income_withholding_basis(PAYOR_GROSS) - payor_cc_total * 52.0
    return {"base_weekly": base, "payor_post_share": share, "payor_cc_burden": share * total,
            "order_weekly": order, "atp": atp, "share_of_atp": order * 52.0 / atp}

def main():
    for box, label in ((2, "primary custody (limit 40%)"), (1, "joint custody (limit 25%)")):
        r = worked(box)
        print(f"{label}: order ${r['order_weekly']:,.0f}/wk; net ${r['net']:,.0f}; payor child care "
              f"${r['payor_childcare_annual']:,.0f}; ability to pay ${r['atp']:,.0f}; "
              f"order = {r['share_of_atp']*100:.1f}% of it; allowed ${r['allowed_weekly']:,.0f}/wk")
        s, n, t = grid_share_over(box)
        print(f"   grid, 3 children, $100/child: {s*100:.1f}% ({n} of {t}) over the limit")
    for cc in (0.0, 300.0):
        r = cross_credit_worked(cc, cc)
        print(f"cross-credit at 1.5, equal time, each parent paying ${cc:,.0f}/wk child care: order "
              f"${r['order_weekly']:,.2f}/wk = {r['share_of_atp']*100:.1f}% of ability to pay")
    r = cross_credit_post_transfer(300.0, 300.0)
    print(f"cross-credit at 1.5, equal time, $300/wk each, child care split after the order: order "
          f"${r['order_weekly']:,.2f}/wk = {r['share_of_atp']*100:.1f}% of ability to pay "
          f"(payor carries {r['payor_post_share']*100:.1f}% of it)")
    r = cross_credit_worked(300.0, 300.0, allocate_child_care=False)
    print(f"cross-credit at 1.5, equal time, each parent paying their OWN $300/wk: order "
          f"${r['order_weekly']:,.2f}/wk = {r['share_of_atp']*100:.1f}% of ability to pay")


if __name__ == "__main__":
    main()
