"""Pins the ability-to-pay figures the petition, letters and site quote. If a check fails, the
documents are wrong and are rewritten, not the test. Run: .venv/bin/python model/test_ability_to_pay.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ability_to_pay as a  # noqa: E402

n = 0


def check(name, ok):
    global n
    if not ok:
        raise SystemExit(f"FAIL {name}")
    n += 1


p, j = a.worked(2), a.worked(1)
check("the measure is net pay minus the payor's own child care", abs(j["atp"] - (j["net"] - 300 * 52)) < 1e-6)
check("under primary custody the payor pays no child care of his own", p["atp"] == p["net"])
check("limits are 40 percent primary, 25 percent joint", (p["limit"], j["limit"]) == (0.40, 0.25))
check("worked example, primary: order is 50.2 percent of ability to pay", round(p["share_of_atp"] * 100, 1) == 50.2)
check("worked example, joint: order is 53.2 percent of ability to pay", round(j["share_of_atp"] * 100, 1) == 53.2)
check("worked example, primary: the limit allows $1,076 a week", round(p["allowed_weekly"]) == 1076)
check("worked example, joint: the limit allows $597 a week", round(j["allowed_weekly"]) == 597)
s2, n2, t = a.grid_share_over(2)
s1, n1, _ = a.grid_share_over(1)
check("grid, primary, $100 a child: every combination over 40 percent", (n2, t) == (1147, 1147))
check("grid, joint, $100 a child each: 79.9 percent over 25 percent", round(s1 * 100, 1) == 79.9 and n1 == 917)
# Reconciles with the no-child-care counts already published (MEMORY 2026-09-20, net_caps).
z2 = sum(a.measure(h, l / 52, 3, 2)["over"] for h, l in a.cg.grid_pairs(3, 2))
z1 = sum(a.measure(h, l / 52, 3, 1)["over"] for h, l in a.cg.grid_pairs(3, 1))
check("no child care: 473 primary cells over 40 percent (41.2 percent)", z2 == 473)
check("no child care: 714 joint cells over 25 percent (62.2 percent)", z1 == 714)
# Cross-credit at 1.5 (box1_fix Variant B), equal time, added 2026-09-25.
c0, c3 = a.cross_credit_worked(0.0, 0.0), a.cross_credit_worked(300.0, 300.0)
check("cross-credit, no child care: $701.30 a week", round(c0["order_weekly"], 2) == 701.30)
check("cross-credit, no child care: 26.1 percent of ability to pay", round(c0["share_of_atp"] * 100, 1) == 26.1)
check("cross-credit, each parent $300 child care: $927.39 a week", round(c3["order_weekly"], 2) == 927.39)
check("cross-credit, each parent $300 child care: 38.8 percent of ability to pay",
      round(c3["share_of_atp"] * 100, 1) == 38.8)
check("the cross-credit alone does not bring the worked example under the 25 percent limit",
      c0["over_joint_limit"] and c3["over_joint_limit"])
# The site page's step-by-step arithmetic reconciles to the order.
check("step by step: basic x 1.5, split by income, halved, netted, equals the order",
      abs(c0["payor_owes"] - c0["other_owes"] - c0["order_weekly"]) < 0.01
      and abs(c0["payor_part"] / 2 - c0["payor_owes"]) < 0.01 and abs(c0["enhanced"] - 1.5 * c0["basic"]) < 1e-9)
# Joint custody under the proposed rule: each parent bears his or her own child care (2026-09-25).
co = a.cross_credit_worked(300.0, 300.0, allocate_child_care=False)
check("own child care: the order is the no-child-care order, $701.30", round(co["order_weekly"], 2) == 701.30)
check("own child care: the payor's $300 still comes off ability to pay", abs(co["atp"] - c3["atp"]) < 1e-6)
check("own child care: 29.4 percent of ability to pay", round(co["share_of_atp"] * 100, 1) == 29.4)
check("the Worksheet's child-care split adds $226.09 a week when both pay the same",
      round(c3["order_weekly"] - co["order_weekly"], 2) == 226.09)
# The proposed rule: child care split on net pay after the order (Comments section 2), 2026-09-25.
cp = a.cross_credit_post_transfer(300.0, 300.0)
check("post-transfer: payor carries 62.8 percent of all child care", round(cp["payor_post_share"] * 100, 1) == 62.8)
check("post-transfer: the order is $778.16 a week", round(cp["order_weekly"], 2) == 778.16)
check("post-transfer: 32.6 percent of ability to pay", round(cp["share_of_atp"] * 100, 1) == 32.6)
check("post-transfer: ability to pay is the same measure as the own-child-care case", abs(cp["atp"] - co["atp"]) < 1e-6)
print(f"All checks passed ({n}).")
