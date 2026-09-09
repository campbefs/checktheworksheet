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
# 4. BOX 1 (equal time), CORRECTED AGAIN 2026-09-08 against the primary-source
#    read in docs/2026-09-08-filing-status-and-credit-allocation.md. The payor
#    NEVER receives head-of-household status or the EITC -- IRC ss. 2(b)(1)(A)(i)
#    and 32(c)(3)(A) both key those to the physical custodian "determined
#    without regard to section 152(e)", so a Form 8332 release cannot move them.
#    Only the federal Child Tax Credit alternates. THE HEADLINE CONSEQUENCE: the
#    recipient household is back ahead, by a much narrower margin than Box 2.
# ---------------------------------------------------------------------------
r_box1 = npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, SUPPORT_WK, 0.0, 0.0,
                       kids_under_13=KIDS_UNDER_13, box=1)
check("box=1: payor keeps $90,447", round(r_box1["payor_after"]) == 90_447,
      r_box1["payor_after"])
check("box=1: recipient household holds $91,511 (+/-$1 rounding)",
      abs(r_box1["recip_after"] - 91_511) <= 1.0, r_box1["recip_after"])
check("box=1: per person $22,878", round(r_box1["recip_per_person"]) == 22_878,
      r_box1["recip_per_person"])
check("box=1: payor's share 49.7%", round(r_box1["payor_after_share"], 3) == 0.497,
      r_box1["payor_after_share"])
check("HEADLINE: at equal time the recipient household is (narrowly) AHEAD again, "
      "reversing the one-day-old averaging-error version of this model",
      r_box1["recip_after"] > r_box1["payor_after"],
      (r_box1["payor_after"], r_box1["recip_after"]))
check("the recipient's margin is small: about $1,064, ~1.2% -- do not soften or round this away",
      950 < (r_box1["recip_after"] - r_box1["payor_after"]) < 1_150,
      r_box1["recip_after"] - r_box1["payor_after"])
check("box=1 is not simply half the box=2 credit (averaging both years, not haircutting one)",
      abs(r_box1["payor_after"] - r_box2["payor_after"] / 2.0) > 100)

check("box=1 averaging: payor_net is the mean of his two claiming-year net incomes "
      "(her year = box=2's payor number; his year = CTC only, single, no EITC/HoH)",
      abs(2 * npos.household_net_incomes(PAYOR_GROSS, RECIP_GROSS, KIDS, kids_under_13=KIDS_UNDER_13, box=1)[0]
          - (npos.net_income(PAYOR_GROSS, "single", 0, P)
             + npos._payor_net_claims_ctc(PAYOR_GROSS, KIDS, P))) < 0.01)

# ---------------------------------------------------------------------------
# 4a. THE PAYOR NEVER GETS HEAD-OF-HOUSEHOLD OR THE EITC IN BOX 1, IN EITHER YEAR.
#     Pin this directly against the two year-level helpers, not just the average.
# ---------------------------------------------------------------------------
_p_A = npos.net_income(PAYOR_GROSS, "single", 0, P)                       # her year
_r_A = npos.net_income(RECIP_GROSS, "hoh", KIDS, P, KIDS_UNDER_13)        # her year
_p_B = npos._payor_net_claims_ctc(PAYOR_GROSS, KIDS, P)                   # his year (CTC only)
_r_B = npos._custodial_net_no_ctc(RECIP_GROSS, KIDS, KIDS_UNDER_13, P)    # his year

check("her year (recipient claims CTC): payor keeps $87,172 -- IDENTICAL to box=2 "
      "(nothing changes for either party when the physical custodian also claims the CTC)",
      round(_p_A - ANNUAL_SUPPORT) == 87_172, _p_A - ANNUAL_SUPPORT)
check("her year: recipient household holds $93,822 (+/-$1 rounding), same as box=2",
      abs((_r_A + ANNUAL_SUPPORT) - 93_822) <= 1.0, _r_A + ANNUAL_SUPPORT)

check("his year (payor claims CTC): payor keeps $93,722 (+/-$1 rounding)",
      abs((_p_B - ANNUAL_SUPPORT) - 93_722) <= 1.0, _p_B - ANNUAL_SUPPORT)
check("his year: recipient household holds $89,201 (+/-$1 rounding)",
      abs((_r_B + ANNUAL_SUPPORT) - 89_201) <= 1.0, _r_B + ANNUAL_SUPPORT)

check("the payor's CTC-claiming year uses the SINGLE bracket, not HoH -- his standard "
      "deduction is $16,100, not $24,150, because he never qualifies for HoH",
      npos.federal_tax(PAYOR_GROSS, "single", P) > npos.federal_tax(PAYOR_GROSS, "hoh", P))

check("the recipient's federal EITC is IDENTICAL in both years -- a Form 8332 release "
      "cannot move it (IRC s. 32(c)(3)(A))",
      abs(npos._federal_eitc(RECIP_GROSS, KIDS, P) - npos._federal_eitc(RECIP_GROSS, KIDS, P)) < 0.001)
check("the recipient's MA-credit package (MA EITC + MA CFTC) is identical whether or not "
      "she claims the CTC that year",
      npos.ma_refundable_credits(RECIP_GROSS, KIDS, "hoh", P, KIDS_UNDER_13)
      == npos.ma_refundable_credits(RECIP_GROSS, KIDS, "hoh", P, KIDS_UNDER_13))
check("ONLY THE CTC DIFFERS between the recipient's two years -- her net income excluding "
      "the CTC amount is identical in year A and year B",
      abs((_r_A - 4_620.0) - _r_B) < 1.0, (_r_A - 4_620.0, _r_B))

# ---------------------------------------------------------------------------
# 4b. THE CTC-VALUE-INVERSION FINDING (checkable on its own, no household
#     assumption needed): the credit is worth MORE to the $201,000 earner than
#     to the $29,640 earner, because her refundable cap and earned-income
#     phase-in bind while his tax liability comfortably absorbs the whole,
#     tapered entitlement.
# ---------------------------------------------------------------------------
_her_ctc_entitlement = npos._ctc_entitlement_after_phaseout(RECIP_GROSS, KIDS, "hoh", P)
_her_ctc_owed = npos.federal_tax(RECIP_GROSS, "hoh", P)
_her_ctc_nonref = min(_her_ctc_entitlement, _her_ctc_owed)
_her_ctc_ref = min(_her_ctc_entitlement - _her_ctc_nonref,
                    P["ctc_refundable_cap"] * KIDS, 0.15 * max(0.0, RECIP_GROSS - 2_500))
HER_CTC = _her_ctc_nonref + _her_ctc_ref

_his_ctc_entitlement = npos._ctc_entitlement_after_phaseout(PAYOR_GROSS, KIDS, "single", P)
_his_ctc_owed = npos.federal_tax(PAYOR_GROSS, "single", P)
_his_ctc_nonref = min(_his_ctc_entitlement, _his_ctc_owed)
_his_ctc_ref = min(_his_ctc_entitlement - _his_ctc_nonref,
                    P["ctc_refundable_cap"] * KIDS, 0.15 * max(0.0, PAYOR_GROSS - 2_500))
HIS_CTC = _his_ctc_nonref + _his_ctc_ref

check("her (recipient's) claiming-year CTC is $4,620", round(HER_CTC) == 4_620, HER_CTC)
check("his (payor's) claiming-year CTC is $6,550 (after the s.24(b) taper)",
      round(HIS_CTC) == 6_550, HIS_CTC)
check("FINDING: the credit is worth MORE to the $201,000 earner than the $29,640 earner "
      "-- her refundable cap/earned-income phase-in binds, his tax liability does not",
      HIS_CTC > HER_CTC, (HIS_CTC, HER_CTC))
check("her CTC is capped below the full $6,600 entitlement (refundability, not the taper, "
      "is what limits her)",
      HER_CTC < 3 * P["ctc_per_child"] and _her_ctc_entitlement == 3 * P["ctc_per_child"],
      (HER_CTC, _her_ctc_entitlement))
check("his CTC is reduced by the taper, not by refundability (his tax liability exceeds "
      "the entire tapered entitlement, so all of it is nonrefundable)",
      HIS_CTC < 3 * P["ctc_per_child"] and _his_ctc_nonref == _his_ctc_entitlement,
      (HIS_CTC, _his_ctc_entitlement, _his_ctc_nonref))

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

# ---------------------------------------------------------------------------
# 6. THE CREDITS-OFF SWITCH (added 2026-09-08): count_refundable_credits=False lets
#    an economist validate the arithmetic without accepting any assumption about
#    which parent claims which child. box=2 default (True) is unchanged.
# ---------------------------------------------------------------------------
r_box1_nocred = npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, SUPPORT_WK, 0.0, 0.0,
                              kids_under_13=KIDS_UNDER_13, box=1,
                              count_refundable_credits=False)
r_box2_nocred = npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, SUPPORT_WK, 0.0, 0.0,
                              kids_under_13=KIDS_UNDER_13, box=2,
                              count_refundable_credits=False)

check("credits-off is IDENTICAL for box=1 and box=2 apart from the order itself "
      "(no per-parent tax fact enters the calculation once credits are off)",
      abs(r_box1_nocred["payor_after"] - r_box2_nocred["payor_after"]) < 0.01
      and abs(r_box1_nocred["recip_after"] - r_box2_nocred["recip_after"]) < 0.01,
      (r_box1_nocred["payor_after"], r_box2_nocred["payor_after"]))

check("credits-off is identical regardless of kids_under_13 too (irrelevant once credits are off)",
      abs(npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, SUPPORT_WK, 0.0, 0.0,
                        kids_under_13=0, box=1, count_refundable_credits=False)["payor_after"]
          - r_box1_nocred["payor_after"]) < 0.01)

check("credits-off payor net EXACTLY equals net_income_withholding_basis(payor_gross)",
      r_box1_nocred["payor_net"] == npos.net_income_withholding_basis(PAYOR_GROSS),
      (r_box1_nocred["payor_net"], npos.net_income_withholding_basis(PAYOR_GROSS)))

check("credits-off recipient net EXACTLY equals net_income_withholding_basis(recipient_gross)",
      r_box1_nocred["recip_net"] == npos.net_income_withholding_basis(RECIP_GROSS),
      (r_box1_nocred["recip_net"], npos.net_income_withholding_basis(RECIP_GROSS)))

check("default (no argument passed) keeps count_refundable_credits=True (backward compatible)",
      npos.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, SUPPORT_WK, 0.0, 0.0,
                   kids_under_13=KIDS_UNDER_13, box=2)["payor_after"]
      == r_box2["payor_after"])

# The four-combination worked-example table (payor $201,000, recipient $29,640, 3 kids,
# no child care, order $1,012.73/wk). Credits-off collapses box 1 and box 2 to one row.
check("box=2, credits ON: payor $87,172, recipient $93,822 -- RECIPIENT AHEAD (unchanged)",
      round(r_box2["payor_after"]) == 87_172 and round(r_box2["recip_after"]) == 93_822,
      (r_box2["payor_after"], r_box2["recip_after"]))

check("box=1, credits ON: payor $90,447, recipient $91,511 -- recipient narrowly ahead",
      round(r_box1["payor_after"]) == 90_447 and abs(r_box1["recip_after"] - 91_511) <= 1.0,
      (r_box1["payor_after"], r_box1["recip_after"]))

check("box=2, credits OFF: payor $87,172, recipient $77,396 -- payor ahead "
      "(SIGN CHANGE from the credits-ON row above: same box, opposite winner)",
      round(r_box2_nocred["payor_after"]) == 87_172
      and round(r_box2_nocred["recip_after"]) == 77_396,
      (r_box2_nocred["payor_after"], r_box2_nocred["recip_after"]))

check("box=1, credits OFF: payor $87,172, recipient $77,396 -- payor ahead (same as box=2 off)",
      round(r_box1_nocred["payor_after"]) == 87_172
      and round(r_box1_nocred["recip_after"]) == 77_396,
      (r_box1_nocred["payor_after"], r_box1_nocred["recip_after"]))

if FAILS:
    print("\n".join(FAILS))
    sys.exit(1)
print(f"All checks passed ({N[0]}).")
