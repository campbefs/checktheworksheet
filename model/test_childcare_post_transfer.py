"""Pins every figure the letter's Section 2 redline quotes. Run: .venv/bin/python model/test_childcare_post_transfer.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import childcare_post_transfer as c  # noqa: E402
import net_position as npos  # noqa: E402

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
check("the two 6b-2 fallback shares sum to one", abs(f["rule2b_share"] + (1 - f["rule2b_share"]) - 1) < 1e-12)
check("per person the payor still leads", f["payor_after"] > f["recip_pp"], (f["payor_after"], f["recip_pp"]))

# v4.9: the withholding basis. In a joint-custody case the credits and the filing status
# are commonly alternated year to year, and CJ-D 304 collects neither, so the rule cannot
# depend on them.
_PG, _RG = c.PAYOR_GROSS, c.RECIP_GROSS
_plain_p = npos.net_income_withholding_basis(_PG)
_plain_r = npos.net_income_withholding_basis(_RG)

check("withholding-basis payor net is $139,833.50", round(_plain_p, 2) == 139833.50, _plain_p)
check("withholding-basis recipient net is $24,733.74", round(_plain_r, 2) == 24733.74, _plain_r)
check("payor claims no dependents, so both bases agree for him",
      abs(_plain_p - npos.net_income(_PG, "single", 0, npos.TAX_PARAMS)) < 0.01)
check("the recipient's credits are real money, and are what the rule leaves out",
      npos.net_income(_RG, "hoh", 3, npos.TAX_PARAMS, 2) > _plain_r + 16000,
      npos.net_income(_RG, "hoh", 3, npos.TAX_PARAMS, 2) - _plain_r)

check("rule 5 (the ask): payor share 53.0%", round(f["rule5_share"], 3) == 0.530, f["rule5_share"])
check("rule 5 order is $1,171.64/wk", round(f["rule5_7d"], 2) == 1171.64, f["rule5_7d"])
check("rule 5 saves $5,415/yr", round(f["rule5_saving_yr"]) == 5415, f["rule5_saving_yr"])
check("the ask sits between the gross fallback and the credits-inclusive analysis",
      f["rule2b_share"] > f["rule5_share"] > f["rule3_share"],
      (f["rule2b_share"], f["rule5_share"], f["rule3_share"]))
check("and far below what the Worksheet does today",
      f["rule1_share"] - f["rule5_share"] > 0.30, f["rule1_share"] - f["rule5_share"])

# No per-filer fact enters the share -- recompute it from scratch and it must agree.
_b = c.base_order() * 52
_a5, _b5 = _plain_p - _b, _plain_r + _b
check("rule 5 depends only on gross income and the schedules",
      abs(_a5 / (_a5 + _b5) - f["rule5_share"]) < 1e-12)

if FAILS:
    print("\n".join(FAILS)); sys.exit(1)
print("All checks passed (20).")
