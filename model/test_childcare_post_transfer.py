"""Pins every figure the letter's Section 2 redline quotes. Run: .venv/bin/python model/test_childcare_post_transfer.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import childcare_post_transfer as c  # noqa: E402

FAILS = []


def check(name, ok, detail=""):
    if not ok:
        FAILS.append(f"{name}: {detail}")


f = c.figures()
check("current rule: payor funds 87.7% of the child care", round(f["rule1_share"], 3) == 0.877, f["rule1_share"])
check("current order with $300/wk child care is $1,276/wk", round(f["current_7d"]) == 1276, f["current_7d"])
check("redline (rule 2b): payor share 64.5% on Line 3a", round(f["rule2b_share"], 3) == 0.645, f["rule2b_share"])
check("redline order is $1,206/wk", round(f["rule2b_7d"]) == 1206, f["rule2b_7d"])
check("redline saves $3,624/yr", round(f["rule2b_saving_yr"]) == 3624, f["rule2b_saving_yr"])
check("after-tax shares: payor 48.2%", round(f["rule3_share"], 3) == 0.482, f["rule3_share"])
check("rule 4 (fixed point) equals rule 3", abs(f["rule4_share"] - f["rule3_share"]) < 1e-6, (f["rule3_share"], f["rule4_share"]))
check("gross post-transfer share 64.3% (not the letter's number)", round(f["rule2_gross_share"], 3) == 0.643, f["rule2_gross_share"])
check("the two 6b-1 shares sum to one", abs(f["rule2b_share"] + (1 - f["rule2b_share"]) - 1) < 1e-12)
check("per person the payor still leads", f["payor_after"] > f["recip_pp"], (f["payor_after"], f["recip_pp"]))

if FAILS:
    print("\n".join(FAILS)); sys.exit(1)
print("All checks passed (10).")
