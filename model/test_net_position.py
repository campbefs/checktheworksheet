"""Pins net_position.py's tax model: the IRC s. 24(b) CTC taper, the CTC/EITC decoupling,
and the Box 1 (equal-time) alternating-year credit averaging fixed 2026-09-08.

Run: .venv/bin/python model/test_net_position.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import net_position as npos  # noqa: E402

FAILS = []
N = [0]


def check(name, ok, detail=""):
    N[0] += 1
    if not ok:
        FAILS.append(f"{name}: {detail}")


P = npos.TAX_PARAMS

# ---------------------------------------------------------------------------
# The worked example: payor $201,000/yr, recipient $29,640/yr, 3 kids (2 under 13).
# ---------------------------------------------------------------------------
PAYOR_GROSS = 201_000.0
RECIP_GROSS = 570.0 * 52.0
KIDS, KIDS_UNDER_13 = 3, 2
SUPPORT_WK = 1_012.73
ANNUAL_SUPPORT = SUPPORT_WK * 52.0

# ---------------------------------------------------------------------------
# 1. THE IRC s. 24(b) TAPER: threshold, slope, and a mid-taper value.
# ---------------------------------------------------------------------------
check("no reduction at exactly the $200,000 threshold",
      npos._ctc_entitlement_after_phaseout(200_000.0, 3, "hoh", P) == 3 * P["ctc_per_child"])

check("$1 over the threshold still costs a full $50 step (rounds up, not down)",
      npos._ctc_entitlement_after_phaseout(200_001.0, 3, "hoh", P)
      == 3 * P["ctc_per_child"] - 50)

check("at $201,000 (the worked example) the reduction is $50 on a $6,600 credit",
      npos._ctc_entitlement_after_phaseout(201_000.0, 3, "hoh", P) == 6_600 - 50,
      npos._ctc_entitlement_after_phaseout(201_000.0, 3, "hoh", P))

check("MID-TAPER: at $250,000 with 3 kids the reduction is $2,500 (50 steps of $50)",
      npos._ctc_entitlement_after_phaseout(250_000.0, 3, "hoh", P) == 6_600 - 2_500,
      npos._ctc_entitlement_after_phaseout(250_000.0, 3, "hoh", P))

check("the taper is a slope, not a cliff: it does not zero out a 3-child credit until ~$332,000",
      npos._ctc_entitlement_after_phaseout(331_000.0, 3, "hoh", P) > 0
      and npos._ctc_entitlement_after_phaseout(332_000.0, 3, "hoh", P) == 0.0,
      (npos._ctc_entitlement_after_phaseout(331_000.0, 3, "hoh", P),
       npos._ctc_entitlement_after_phaseout(332_000.0, 3, "hoh", P)))

check("the taper floors at zero, never goes negative",
      npos._ctc_entitlement_after_phaseout(1_000_000.0, 3, "hoh", P) == 0.0)

# ---------------------------------------------------------------------------
# 2. THE CTC/EITC DECOUPLING: a single filer with children gets the CTC but not
#    the EITC; a HoH filer at the same gross gets both.
# ---------------------------------------------------------------------------
_single_credits = npos.refundable_credits(50_000.0, 2, "single", P)
_hoh_credits = npos.refundable_credits(50_000.0, 2, "hoh", P)
check("a single filer with 2 qualifying children gets a nonzero credit (no silent zero)",
      _single_credits > 0.0, _single_credits)
check("the single filer's credit is the CTC alone: $4,400 (no phaseout at $50,000)",
      round(_single_credits, 2) == 4_400.00, _single_credits)
check("the HoH filer at the same gross gets MORE (the CTC plus the EITC)",
      _hoh_credits > _single_credits, (_hoh_credits, _single_credits))
check("kids=0 still returns zero regardless of status",
      npos.refundable_credits(50_000.0, 0, "single", P) == 0.0
      and npos.refundable_credits(50_000.0, 0, "hoh", P) == 0.0)

# ---------------------------------------------------------------------------
# 3. BOX 2 (primary custody) IS UNCHANGED: recipient claims all, files HoH.
# ---------------------------------------------------------------------------
r_box2 = npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, SUPPORT_WK, 0.0, 0.0,
                       kids_under_13=KIDS_UNDER_13, box=2)
r_default = npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, SUPPORT_WK, 0.0, 0.0,
                          kids_under_13=KIDS_UNDER_13)
check("box=2 matches the no-box-argument default (backward compatible)",
      abs(r_box2["payor_after"] - r_default["payor_after"]) < 0.01
      and abs(r_box2["recip_after"] - r_default["recip_after"]) < 0.01)
check("box=2 (recipient claims all, today): payor keeps $87,172",
      round(r_box2["payor_after"]) == 87_172, r_box2["payor_after"])
check("box=2: recipient household holds $93,821 (+/-$1 rounding)",
      abs(r_box2["recip_after"] - 93_821) <= 1.0, r_box2["recip_after"])
check("box=2: per person $23,455", round(r_box2["recip_per_person"]) == 23_455,
      r_box2["recip_per_person"])
check("box=2: payor's share 48.2%", round(r_box2["payor_after_share"], 3) == 0.482,
      r_box2["payor_after_share"])

# ---------------------------------------------------------------------------
# 4. BOX 1 (equal time): the NEW default the owner asked for -- alternating
#    years, averaged for both parties. THE HEADLINE CONSEQUENCE: the recipient
#    household no longer holds more.
# ---------------------------------------------------------------------------
r_box1 = npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, SUPPORT_WK, 0.0, 0.0,
                       kids_under_13=KIDS_UNDER_13, box=1)
check("box=1: payor keeps $92,893", round(r_box1["payor_after"]) == 92_893,
      r_box1["payor_after"])
check("box=1: recipient household holds $85,608 (+/-$1 rounding)",
      abs(r_box1["recip_after"] - 85_608) <= 1.0, r_box1["recip_after"])
check("box=1: per person $21,402", round(r_box1["recip_per_person"]) == 21_402,
      r_box1["recip_per_person"])
check("box=1: payor's share 52.0%", round(r_box1["payor_after_share"], 3) == 0.520,
      r_box1["payor_after_share"])
check("HEADLINE: at equal time the payor is now AHEAD of the recipient household",
      r_box1["payor_after"] > r_box1["recip_after"],
      (r_box1["payor_after"], r_box1["recip_after"]))
check("box=1 is not simply half the box=2 credit (averaging both years, not haircutting one)",
      abs(r_box1["payor_after"] - r_box2["payor_after"] / 2.0) > 100)

check("box=1 averaging: payor_net is the mean of his two claiming-year net incomes",
      abs(2 * npos.household_net_incomes(PAYOR_GROSS, RECIP_GROSS, KIDS, kids_under_13=KIDS_UNDER_13, box=1)[0]
          - (npos.net_income(PAYOR_GROSS, "single", 0, P)
             + npos.net_income(PAYOR_GROSS, "hoh", KIDS, P, KIDS_UNDER_13))) < 0.01)

# "Payor claims, his year" (not the default -- an intermediate check that the
# averaged figure sits between the two years, and reproduces the target row).
_p_payor_claims = npos.net_income(PAYOR_GROSS, "hoh", KIDS, P, KIDS_UNDER_13) - ANNUAL_SUPPORT
_r_payor_claims = npos.net_income(RECIP_GROSS, "single", 0, P) + ANNUAL_SUPPORT
check("payor-claims-year: he keeps $98,615", round(_p_payor_claims) == 98_615, _p_payor_claims)
check("payor-claims-year: recipient household holds $77,395 (+/-$1 rounding)",
      abs(_r_payor_claims - 77_395) <= 1.0, _r_payor_claims)
check("the box=1 average sits between the two single-year figures for the payor",
      r_box2["payor_after"] < r_box1["payor_after"] < _p_payor_claims,
      (r_box2["payor_after"], r_box1["payor_after"], _p_payor_claims))

# "No credits to either" reference row -- both single filers, no children claimed.
_p_none = npos.net_income(PAYOR_GROSS, "single", 0, P) - ANNUAL_SUPPORT
_r_none = npos.net_income(RECIP_GROSS, "single", 0, P) + ANNUAL_SUPPORT
check("no-credits reference: payor keeps $87,172 (same as box=2 -- he never gets credits there)",
      round(_p_none) == 87_172, _p_none)
check("no-credits reference: recipient household holds $77,395 (+/-$1 rounding)",
      abs(_r_none - 77_395) <= 1.0, _r_none)
check("no-credits reference: payor's share 53.0%",
      round(_p_none / (_p_none + _r_none), 3) == 0.530, _p_none / (_p_none + _r_none))

# ---------------------------------------------------------------------------
# 5. UNCHANGED: net_income_withholding_basis() has no credits and is untouched
#    by any of the above -- it is the basis Section 2's Line 6b-1 ask uses.
# ---------------------------------------------------------------------------
check("withholding-basis payor net is still $139,833.50",
      round(npos.net_income_withholding_basis(PAYOR_GROSS), 2) == 139_833.50)
check("withholding-basis recipient net is still $24,733.74",
      round(npos.net_income_withholding_basis(RECIP_GROSS), 2) == 24_733.74)

if FAILS:
    print("\n".join(FAILS))
    sys.exit(1)
print(f"All checks passed ({N[0]}).")
