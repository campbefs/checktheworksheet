#!/usr/bin/env python3
"""Post-transfer spendable-income comparison for a MA child support order.

THE QUESTION THIS ANSWERS
-------------------------
Whether, after a guidelines order, the recipient household holds more spendable income than the payor.

This tests it. The guidelines compute support on GROSS (available income, which is gross
less a few support/insurance deductions and NO tax adjustment -- verified from Section I
of the 2025 Guidelines). The obligation is paid from NET. Child support is not deductible
to the payor and not taxable to the recipient. So the transfer is:

    measured in pre-tax dollars, paid out of post-tax dollars, received tax-free.

That is a units mismatch, and it compounds with the marginal rate. This script quantifies
where the two households actually land.

VERIFICATION STATUS
  FEDERAL constants re-verified 2026-09-09 directly against IRC text and IRS Rev. Proc.
  2025-32 (docs/2026-09-08-federal-tax-constants-verified.md) -- supersedes the
  2026-09-02 Tax Foundation pass. That review found and fixed a real bug (the
  head-of-household 24%/32% bracket had copied the single-filer figure) and added the
  EITC's statutory phase-in, which the model had previously skipped.
  MASSACHUSETTS constants re-verified 2026-09-09 directly against M.G.L. c.62 and DOR's
  2025 Form 1 instructions (docs/2026-09-08-massachusetts-tax-constants-verified.md) --
  supersedes the 2026-09-02 pass, which relied on a budget document quoting the statute
  rather than the statute itself. Rate, both personal exemptions, the $1,000 dependent
  exemption, the 40% EITC match, and the $440 Child and Family Tax Credit are all
  CONFIRMED. One genuinely open question survives with no DOR ruling either way
  (whether the $1,000 dependent exemption follows physical custody or the federal CTC
  claim in Box 1 -- see `_payor_net_claims_ctc()` below) and one stale comment was fixed
  (the surtax threshold, never computed, now reads its actual TY2026 figure -- see
  `ma_tax()` below).
Every constant lives in TAX_PARAMS so it can be corrected in one place.

CORRECTED 2026-09-08 -- analyze() used to hardcode the recipient as claiming every child
  and filing head of household in EVERY scenario, including Box 1 (equal parenting time),
  which does not reflect a joint-custody arrangement where the dependency claim is commonly
  shared or alternated by year. It now takes a `box` argument;
  Box 1 averages the payor-claims and recipient-claims years (see household_net_incomes()).
  This also required implementing the IRC s. 24(b) high-income Child Tax Credit taper
  (previously absent) and decoupling the federal CTC from the "hoh"-only gate in
  refundable_credits() -- both were latent bugs that produced a wrong number the moment a
  scenario credited the payor. See model/test_net_position.py.

Usage:
    python3 model/net_position.py
    python3 model/net_position.py --payor-gross 220000 --recipient-gross 31200 --kids 2
"""

import argparse
import math

# ---------------------------------------------------------------------------
# PARAMETERS -- federal verified TY2026; MA approximate (see module docstring)
# ---------------------------------------------------------------------------
TAX_PARAMS = {
    "federal_verified": True,   # TY2026, re-verified 2026-09-09 against Rev. Proc.
                                 # 2025-32 directly. docs/2026-09-08-federal-tax-
                                 # constants-verified.md (supersedes the 2026-09-02 pass).
    # MA re-verified 2026-09-09 directly against M.G.L. c.62 and DOR's 2025 Form 1
    # instructions -- docs/2026-09-08-massachusetts-tax-constants-verified.md, stronger
    # sourcing than the 2026-09-02 pass below (a budget document quoting the statute,
    # not the statute itself). CONFIRMED: rate 5% (c.62 s.4(b)); exemptions single
    # $4,400 / HoH $6,800 (c.62 s.3(B)(b)(1)/(1A)); $1,000 per dependent
    # (c.62 s.3(B)(b)(3)); MA EITC 40% of the federal credit, refundable
    # (c.62 s.6(h)(1)); Child and Family Tax Credit $440/dependent, refundable, no cap
    # on the number of dependents, dependents under 13 (or disabled, or 65+) only for
    # the age-based prong (c.62 s.6(x); the $310-to-$440 raise is St. 2023 c.50
    # ss.21-22, both enacted the same year). OPEN, no DOR ruling either way:
    #   (1) whether the $1,000 dependent exemption follows physical custody (this
    #       model's convention) or the federal CTC claim -- see
    #       _payor_net_claims_ctc()'s docstring; real effect ~$75/yr, Box 1 only.
    #   (2) whether CFTC prong (i) requires household membership like prongs
    #       (ii)/(iii) -- moot to every output, since the credit is already gated on
    #       HoH status and the payor is never modelled as that parent.
    # Earlier pass (2026-09-02, superseded but not wrong on any figure): confirmed via
    # malegislature.gov and the Commonwealth's FY26 tax expenditure budget
    # (budget.digital.mass.gov, item 1.628), which quotes the statute. See
    # docs/2026-09-02-ma-tax-constants-verified.md.
    "ma_verified": True,
    "tax_year": 2026,
    "std_deduction": {"single": 16_100, "hoh": 24_150},
    "brackets": {
        # (rate, upper bound of taxable income). TY2026, verified 2026-09-02.
        "single": [
            (0.10, 12_400), (0.12, 50_400), (0.22, 105_700), (0.24, 201_775),
            (0.32, 256_225), (0.35, 640_600), (0.37, float("inf")),
        ],
        "hoh": [
            (0.10, 17_700), (0.12, 67_450), (0.22, 105_700),
            # Rev. Proc. 2025-32, head of household. $201,775 is the SINGLE figure and
            # was copied here in error. No dollar effect at either income this project
            # models; corrected because it would misfire elsewhere.
            (0.24, 201_750),
            (0.32, 256_200), (0.35, 640_600), (0.37, float("inf")),
        ],
    },
    # FICA -- flagged NOT RE-VERIFIED by the 2026-09-09 Massachusetts pass (out of its
    # scope) but independently verified the same week by the federal pass: SSA's 2026
    # COLA fact sheet (rate and wage base) and IRC s.3101(b)(2) (Additional Medicare
    # Tax rate and its $200,000 threshold, fixed by statute and not indexed).
    # docs/2026-09-08-federal-tax-constants-verified.md section 3.
    "ss_rate": 0.062,               # IRC s.3101(a), OASDI.
    "ss_wage_base": 184_500,        # SSA 2026 COLA fact sheet.
    "medicare_rate": 0.0145,        # IRC s.3101(b), HI.
    "addl_medicare_rate": 0.009,    # IRC s.3101(b)(2), Additional Medicare Tax.
    "addl_medicare_threshold": 200_000,  # IRC s.3101(b)(2); not indexed.
    "ma_rate": 0.05,
    "ma_personal_exemption": {"single": 4_400, "hoh": 6_800},
    "ma_dependent_exemption": 1_000,
    "ma_eitc_pct": 0.40,
    "ma_cftc_per_dependent": 440,
    # Refundable credits that flow to the lower-income parent claiming the children.
    "ctc_per_child": 2_200,
    "ctc_refundable_cap": 1_700,
    # IRC s. 24(b): the Child Tax Credit phases out $50 per $1,000 (or fraction) of
    # MAGI over $200,000 for single/HoH filers ($400,000 MFJ -- not modelled, no
    # filer in this project files jointly). A TAPER, not a cliff: at $201,000 with
    # three children the reduction is $50 on a $6,600 credit; it does not reach zero
    # until about $332,000. Added 2026-09-08 -- the payor's $201,000 gross is $1,000
    # over the threshold, so any scenario crediting him the CTC needs this to be right.
    "ctc_phaseout_threshold": {"single": 200_000, "hoh": 200_000},
    "ctc_phaseout_per_1000": 50,
    # EITC by number of qualifying children -- TY2026 verified 2026-09-02.
    # (max credit, phaseout start HoH/single, phaseout end)
    "eitc": {
        0: (664, 10_860, 19_540),
        1: (4_427, 23_890, 51_593),
        2: (7_316, 23_890, 58_629),
        3: (8_231, 23_890, 62_974),
    },
    # IRC s.32(b)(1): the EITC phases IN below the plateau at a statutory credit
    # percentage (a fixed rate of earned income, not inflation-adjusted). Added
    # 2026-09-09 -- the model previously returned the plateau maximum for ANY
    # income up to the phaseout-start figure above, which overstates the credit
    # below roughly $18,290 of earned income (3+ children). Verbatim, Rev. Proc.
    # 2025-32 quoting IRC s.32(b)(1): "In the case of an eligible individual with:
    # ... 3 or more qualifying children[,] [t]he credit percentage is: 45[%]."
    # Cross-checked independently: $8,231 / (62,974 - 23,890) = 21.06%, matching
    # the statute's stated phaseout percentage for the same row to four
    # significant figures (docs/2026-09-08-federal-tax-constants-verified.md
    # section 4). The 0/1/2-child rows (7.65% / 34% / 40%) are the well-known
    # statutory figures at 26 U.S.C. s.32(b)(1) but were NOT independently
    # re-verified this session -- every fact pattern this project publishes uses
    # 3 children, so only the 45% row is load-bearing.
    "eitc_phase_in_rate": {0: 0.0765, 1: 0.34, 2: 0.40, 3: 0.45},
}


def federal_tax(gross, status, params):
    """Ordinary federal income tax before credits."""
    taxable = max(0.0, gross - params["std_deduction"][status])
    tax, last = 0.0, 0.0
    for rate, upper in params["brackets"][status]:
        if taxable <= last:
            break
        tax += rate * (min(taxable, upper) - last)
        last = upper
    return tax


def fica(gross, params):
    ss = params["ss_rate"] * min(gross, params["ss_wage_base"])
    med = params["medicare_rate"] * gross
    addl = params["addl_medicare_rate"] * max(0.0, gross - params["addl_medicare_threshold"])
    return ss + med + addl


def ma_tax(gross, status, params, kids=0):
    """Massachusetts income tax before the refundable state credits.

    Dependents reduce taxable income by $1,000 each on top of the filing-status
    exemption. The 4% surtax (M.G.L. c.62 s.4(d)) is not modelled -- no scenario in
    this project approaches it. STALE COMMENT FIXED 2026-09-09: this docstring used to
    say the threshold is "$1,000,000". That is the statute's base figure, but s.4(d)
    itself indexes it annually and DOR has published three successive higher numbers
    ($1,053,750 TY2024, $1,083,150 TY2025, $1,107,750 TY2026 -- mass.gov "Massachusetts
    tax rates," updated 2025-12-30). $0 effect either way: the surtax is never
    computed, and neither party in this project's fact patterns ($29,640 and $201,000
    gross) is within a factor of five of the threshold under any year's figure.
    docs/2026-09-08-massachusetts-tax-constants-verified.md section 1.

    Also checked and confirmed NOT to apply, so not modelled: MA No Tax Status
    (AGI <= $14,400 + $1,000/dependent for HoH) and the Limited Income Credit
    (a worksheet computation that phases out as regular tax approaches 10% of the AGI
    above the No-Tax-Status threshold). At the $29,640 worked example the recipient is
    above No Tax Status, and although her AGI falls inside the Limited Income Credit's
    eligibility band, the worksheet yields $0 because her regular tax ($992) is already
    below the credit's implicit cap ($1,224). Both DOR FORM INSTRUCTION (2025 Form 1
    Instructions, Line 29 worksheet); docs/2026-09-08-massachusetts-tax-constants-
    verified.md section 6(b)."""
    exempt = params["ma_personal_exemption"][status] + params["ma_dependent_exemption"] * kids
    return params["ma_rate"] * max(0.0, gross - exempt)


def ma_refundable_credits(gross, kids, status, params, kids_under_13=None):
    """MA EITC (40% of the federal credit) plus the Child and Family Tax Credit.

    Both are refundable, so for a low-income recipient they are cash, not just tax
    forgiveness -- which is precisely the mechanism the Task Force said "can materially
    affect a household's available income" and then deferred.

    kids_under_13 defaults to all children. The CFTC is limited to dependents under 13
    (or disabled, or 65+), so a household of teenagers gets the EITC portion only.

    OPEN QUESTION, moot to this function's output (docs/2026-09-08-massachusetts-tax-
    constants-verified.md section 4): does CFTC prong (i) -- the under-13 dependent --
    require the dependent to live in the claiming taxpayer's household, the way
    prongs (ii)/(iii) (disabled dependent, elderly dependent) explicitly do? No DOR
    Technical Information Release or regulation resolves it either way. It cannot
    change what this function returns: the `status != "hoh"` gate above already denies
    the credit to anyone not modelled as the household-maintaining parent, so the
    household-membership question never actually gets asked."""
    if status != "hoh" or kids == 0:
        return 0.0
    if kids_under_13 is None:
        kids_under_13 = kids
    fed_eitc = _federal_eitc(gross, kids, params)
    return params["ma_eitc_pct"] * fed_eitc + params["ma_cftc_per_dependent"] * kids_under_13


def _federal_eitc(gross, kids, params):
    """IRC s.32(b): phases IN at a statutory rate from $0 of earned income, plateaus
    at the maximum once the phase-in reaches it, holds flat until the phaseout-start
    figure, then phases OUT linearly to zero. The phase-in breakpoint (the "earned
    income amount") is not stored separately -- it falls out of min(rate * gross, mx),
    which is exact by construction and matches the back-solved figure in
    docs/2026-09-08-federal-tax-constants-verified.md ($8,231 / 0.45 = $18,291 for
    3+ children). Fixed 2026-09-09: an earlier version returned the plateau maximum
    for any income up to `start`, overstating the credit in the phase-in region. No
    effect at this project's $29,640 recipient income, which sits inside the
    phase-out region where this function was already exact."""
    mx, start, end = params["eitc"][min(kids, 3)]
    rate = params["eitc_phase_in_rate"][min(kids, 3)]
    if gross <= start:
        return min(rate * gross, float(mx))
    if gross >= end:
        return 0.0
    return mx * (end - gross) / (end - start)


def _ctc_entitlement_after_phaseout(gross, kids, status, params):
    """IRC s. 24(b): CTC entitlement before the tax-liability/refundability split,
    reduced $50 per $1,000 (or fraction) of gross over the filer's threshold. A
    taper, not a cliff -- do not round the excess down to the nearest $1,000."""
    entitlement = params["ctc_per_child"] * kids
    threshold = params["ctc_phaseout_threshold"].get(status, params["ctc_phaseout_threshold"]["single"])
    if gross <= threshold:
        return entitlement
    steps = math.ceil((gross - threshold) / 1_000.0)
    reduction = params["ctc_phaseout_per_1000"] * steps
    return max(0.0, entitlement - reduction)


def refundable_credits(gross, kids, status, params):
    """Federal CTC (any filing status) + EITC (custodial-parent proxy only).

    IRC s. 24(d): the refundable Additional Child Tax Credit is the LEAST of the
    entitlement remaining after it offsets tax liability, $1,700 per child, and
    15% of earned income above $2,500. An earlier version omitted the earned-income
    phase-in and added a flat credit on top of a fully-subtracted liability, which
    OVERSTATED the recipient by about $480/yr on the worked example. The docstring
    then called that "deliberately conservative" -- it was conservative in the wrong
    direction, i.e. it flattered this project's own argument. Caught in QA 2026-09-02.

    DECOUPLED FROM FILING STATUS 2026-09-08. The old code returned 0.0 for any
    non-"hoh" filer, which is wrong for the CTC: a parent who claims a qualifying
    child (via a custody order or a signed Form 8332) can claim the Child Tax
    Credit filing single, and this project needs exactly that case once a Box 1
    (equal-time) scenario alternates the claim between the two parents by year.
    The EITC keeps ITS OWN rule, unchanged: it requires the child to have lived
    with the claimant for more than half the year, which is what "hoh" stands in
    for in this simplified model, so it is not extended to a "single, claims the
    kids on paper only" filer.

    CORRECTED AGAIN 2026-09-08 (same day): the sentence that used to end this
    docstring said the payor should be modelled as HoH "he is the modelled
    physical custodian that year" in his CTC-claiming year. That is not what the
    statute allows and is not what this file does anymore. IRC s. 2(b)(1)(A)(i)
    defines head of household "determined without regard to section 152(e))" --
    a Form 8332 release cannot move HoH status, and s. 32(c)(3)(A) keeps the
    EITC with the physical custodian on the same "without regard to section
    152(e)" language. Only the CTC/ACTC family moves with the release (s. 152(e)
    itself, which s. 24(c)(1) inherits and neither s. 2(b) nor s. 32(c) does).
    See docs/2026-09-08-filing-status-and-credit-allocation.md. The payor's
    CTC-claiming year is now modelled by `_payor_net_claims_ctc()` below: single
    filer, CTC only, no EITC, no HoH, no MA EITC, no MA Child and Family Tax
    Credit -- ever. The physical custodian's non-claiming year is modelled by
    `_custodial_net_no_ctc()`: HoH, EITC, MA EITC and MA CFTC unaffected by the
    release; only the federal CTC drops out.

    ALTERNATIVE ACTC FORMULA FOR 3+ CHILDREN, added 2026-09-09
    (docs/2026-09-08-federal-tax-constants-verified.md section 5). IRC s.24(d)(1)(B)
    takes the GREATER of two paths: (i) 15% of earned income above $2,500 (the only
    path this function computed until now), or (ii), for a taxpayer with 3 or more
    qualifying children, the excess (if any) of the taxpayer's "social security
    taxes" over the s.32 EITC computed above. "Social security taxes" is defined at
    s.24(d)(2)(A) as the full employee-side FICA under IRC ss.3101 and 3201(a) --
    i.e. the 7.65% OASDI-plus-Medicare figure `fica()` already computes, not just
    the 6.2% OASDI piece -- so `fica()` is used directly as that proxy. This
    project's own fact pattern is 3 children, which is exactly who s.24(d)(1)(B)(ii)
    is written for, so the path is implemented rather than merely documented. It is
    $0 at the $29,640 recipient income this project quotes (her EITC of $7,020
    exceeds her FICA of $2,267, so the excess is negative, i.e. zero) -- confirmed
    by test_net_position.py, which pins that no quoted figure moved. Path (ii) is
    NOT wired into `_payor_net_claims_ctc()` below: at every income this project
    publishes for the payor, his tax liability alone absorbs the full CTC
    entitlement (nonrefundable == entitlement), so the refundable portion -- the
    only place either path matters -- is already $0 regardless of which path
    governs. A future caller who runs that helper at a much lower payor income
    would not get path (ii); this function is the one place it is implemented."""
    if kids == 0:
        return 0.0
    entitlement = _ctc_entitlement_after_phaseout(gross, kids, status, params)
    tax_owed = federal_tax(gross, status, params)
    nonrefundable = min(entitlement, tax_owed)
    eitc = _federal_eitc(gross, kids, params) if status == "hoh" else 0.0
    path_i = 0.15 * max(0.0, gross - 2_500)
    if kids >= 3:
        path_ii = max(0.0, fica(gross, params) - eitc)
        refundable_formula = max(path_i, path_ii)
    else:
        refundable_formula = path_i
    refundable = min(entitlement - nonrefundable,
                     params["ctc_refundable_cap"] * kids,
                     refundable_formula)
    return nonrefundable + refundable + eitc


def net_income(gross, status, kids, params, kids_under_13=None):
    """After-tax income including federal AND Massachusetts refundable credits.

    ASSUMPTION, disclosed 2026-09-09 (docs/2026-09-08-federal-tax-constants-verified.md
    section 7, item 4): both filers are modelled taking the STANDARD deduction. No
    itemized path (mortgage interest, state and local taxes, charitable gifts) is
    computed for either party. If the payor itemizes -- plausible for a $201,000
    Massachusetts earner with a mortgage, since mortgage interest plus roughly 5%
    Massachusetts income tax alone can exceed the $16,100 single standard deduction --
    his real taxable income and real tax are LOWER than this function returns, so his
    real net income is HIGHER than this function shows. That cuts AGAINST this
    project's own argument that he is the more heavily burdened party. No mortgage or
    SALT figures are given for either party in this project, so the size is not
    estimated; only the direction is stated. See output/ATTACHMENT-A-method.md."""
    tax = (federal_tax(gross, status, params) + fica(gross, params)
           + ma_tax(gross, status, params, kids))
    return (gross - tax
            + refundable_credits(gross, kids, status, params)
            + ma_refundable_credits(gross, kids, status, params, kids_under_13))


def net_income_withholding_basis(gross, params=TAX_PARAMS):
    """Net of federal and Massachusetts income tax and FICA. NO refundable credits.

    This is the basis Section 2 of the comments asks for as of v4.9, and the basis
    Section 1 already asks for at Line 7e. It is deliberately narrower than
    `net_income` above: it applies the schedules to a single filer claiming no
    exemptions, so it needs nothing beyond gross income and the published rates.

    Why the credits are excluded, although they are large and real: the refundable
    credits and head-of-household status both turn on which parent claims which
    child, CJ-D 304 collects neither fact, and in a shared-parenting case the
    claim is commonly alternated by year. tools/net_basis_sensitivity.py brackets
    it: across the two extreme filing conventions who claims the children moves
    the post-transfer share 7.8 points, and the credits alone (both filing single)
    are worth up to 4.8 points against the no-credit figure at the top of that
    bracket. A Worksheet line cannot rest on an input the Worksheet does not have.

    The omission runs AGAINST the payor: including the credits, under the
    alternating-year convention `net_income()` above now uses (statutory fix,
    2026-09-08 -- only the Child Tax Credit moves; head-of-household, the EITC and
    the MA EITC stay with whoever has more overnights), puts his share at 49.7%
    rather than 53.0%, so the rule as proposed understates the case for it.
    """
    return gross - (federal_tax(gross, "single", params)
                    + fica(gross, params)
                    + ma_tax(gross, "single", params, 0))


def _payor_net_claims_ctc(gross, kids, params):
    """The payor's net income in the year a s. 152(e)/Form 8332 release moves the
    Child Tax Credit to him. He never gains head-of-household status, the EITC, the
    MA EITC, or the MA Child and Family Tax Credit -- none of the four is movable by
    a release (IRC ss. 2(b)(1)(A)(i), 32(c)(3)(A); the MA credits piggyback on the
    federal EITC/HoH test). He files single. The MA per-dependent exemption is
    modelled as tracking physical custody, not the CTC release, like the four
    credits above -- there is no statute or DOR ruling on point for that specific
    MA exemption (docs/2026-09-08-filing-status-and-credit-allocation.md, item 21),
    but treating it like the other custody-linked benefits is what this project's
    own worked-example arithmetic requires, and it is consistent with the same
    physical-custody logic as the rest of this function. So `kids` here drives ONLY
    the CTC computation; ma_tax() below is always called with 0 dependents for the
    payor. See docs/2026-09-08-filing-status-and-credit-allocation.md Q1/Q3/Q4/Q6.

    UPDATE 2026-09-09 (docs/2026-09-08-massachusetts-tax-constants-verified.md
    section 2): a second, Massachusetts-focused reading DISAGREES with this
    convention and is recorded here rather than resolved. M.G.L. c.62 s.3(B)(b)(3)
    ties the $1,000 exemption to whoever "qualifies for exemption as a dependent
    under section one hundred and fifty-one (c) of the Code," with NO "without regard
    to section 152(e)" carve-out -- unlike MA's own head-of-household provision
    (s.3(b)(1A), cross-referencing IRC s.2(b), which DOES carry that carve-out) and
    unlike the MA EITC (s.6(h)(1), piggybacking on federal s.32(c)(3)(A), which also
    carries it). On that reading the exemption moves WITH the federal
    dependency/CTC claim, i.e. to the payor in his claiming year -- the opposite of
    what this function does. Still no DOR ruling or TIR either way. Size: $1,000 x 3
    dependents x 5% = $150 shifted in the payor's claiming year only, averaged to
    about $75/yr each way over household_net_incomes()'s two-year Box 1 cycle -- real,
    but small next to the credits this function already carries, and it does not touch
    the Box 2 worked example the comments quote. This function's convention (kids=0
    for the payor) is UNCHANGED pending a ruling; every figure it feeds in Box 1 with
    credits on is graded C in data/figure-registry.json for exactly this reason,
    among others."""
    tax = federal_tax(gross, "single", params) + fica(gross, params) + ma_tax(gross, "single", params, 0)
    entitlement = _ctc_entitlement_after_phaseout(gross, kids, "single", params)
    tax_owed = federal_tax(gross, "single", params)
    nonrefundable = min(entitlement, tax_owed)
    refundable = min(entitlement - nonrefundable,
                     params["ctc_refundable_cap"] * kids,
                     0.15 * max(0.0, gross - 2_500))
    return gross - tax + nonrefundable + refundable


def _custodial_net_no_ctc(gross, kids, kids_under_13, params):
    """The majority-nights parent's net income in a year where the s. 152(e)/Form
    8332 release moves the federal Child Tax Credit to the other parent. Head of
    household, the federal EITC, the MA EITC (40% of federal), and the MA Child and
    Family Tax Credit are all UNAFFECTED by the release -- see the four statutory
    anchors in docs/2026-09-08-filing-status-and-credit-allocation.md Q3's table
    (IRC ss. 2(b)(1)(A)(i), 32(c)(3)(A), 21(e)(5)). The MA per-dependent exemption is
    modelled as staying with this parent too (see _payor_net_claims_ctc()'s
    docstring). Only the federal CTC/ACTC family drops out for this parent this
    year -- ma_tax() below still carries the full dependent count."""
    tax = federal_tax(gross, "hoh", params) + fica(gross, params) + ma_tax(gross, "hoh", params, kids)
    fed_eitc = _federal_eitc(gross, kids, params) if kids else 0.0
    ma_credits = ma_refundable_credits(gross, kids, "hoh", params, kids_under_13)
    return gross - tax + fed_eitc + ma_credits


def household_net_incomes(payor_gross, recipient_gross, kids, params=TAX_PARAMS,
                           kids_under_13=None, box=2, count_refundable_credits=True):
    """Each party's annual net income, given who claims the children for tax purposes.

    count_refundable_credits=False (added 2026-09-08 -- the credits-off switch) lets a reader
    who does not accept any assumption about which parent claims which child -- an economist,
    most pointedly -- validate the arithmetic anyway. In this mode BOTH parties' net income
    comes from net_income_withholding_basis() -- tax and FICA only, a single filer claiming no
    exemptions -- and `box` and `kids_under_13` are ignored entirely: filing status and who
    claims which child matter ONLY because they gate the refundable credits computed below, so
    once the credits are off there is nothing left for either fact to change. That is the point
    of the mode, not an approximation of it -- it is the basis the Commonwealth's own consultant
    uses each review cycle ("state-specific income withholding tables ... and standard
    withholding for Social Security and Medicare"), which contains no refundable credits, and
    it is the basis net_income_withholding_basis() already documents for the Section 2
    child-care ask.

    Box 2 (primary custody, the DEFAULT -- matches every caller written before
    2026-09-08): the recipient is the physical custodian, claims every child, and
    files head of household. Unchanged from the original hardcoded behaviour.

    Box 1 (equal parenting time): CORRECTED AGAIN 2026-09-08, same day, against
    docs/2026-09-08-filing-status-and-credit-allocation.md, a primary-source read
    of IRC ss. 2(b), 7703(b), 152(c)/(e), 21(e)(5), 24(b)/(h), 32(c)(3)(A), and the
    corresponding MA statutes. The FIRST attempt at this fix (same day, superseded)
    had the two parents swap EVERYTHING in alternating years -- filing status, the
    EITC, and the CTC. The statute does not allow that: a s. 152(e)/Form 8332
    release moves ONLY the dependency claim and the federal CTC/ACTC family (s.
    152(e)(1)-(2), s. 24(c)(1)). Head of household stays with the physical
    custodian regardless of any release (s. 2(b)(1)(A)(i): the qualifying-child
    test is "determined without regard to section 152(e)"). The EITC stays with
    the physical custodian too, on the identical "without regard to ... section
    152(e)" language in s. 32(c)(3)(A). The child and dependent care credit is
    likewise pinned to the custodial parent by s. 21(e)(5) (not modelled here --
    this project's Box 1 child-care scenarios are computed elsewhere -- but the
    same statutory pattern). This project's own 182/183-overnight convention
    (recipient holds 183, the majority) makes the RECIPIENT the physical
    custodian in every year; the PAYOR never receives head-of-household status or
    the EITC in Box 1, in either claiming year.

    So this returns the expected value of alternating ONLY the CTC/dependency
    claim: the payor-claims year (recipient keeps HoH/EITC/MA EITC/MA CFTC, payor
    gets only the CTC as a single filer -- see `_payor_net_claims_ctc()`) and the
    recipient-claims year (identical to Box 2 in every respect -- the recipient
    already had everything, so nothing changes when she also claims the CTC),
    averaged for both parties. This is not approximated as "half the credit" --
    computing both years separately is what makes the IRC s. 24(b) high-income
    taper apply correctly in the payor's claiming year, which a flat 50% haircut
    would not reproduce. Pinned in model/test_net_position.py; see that file and
    the source doc for the reproduced worked-example figures."""
    if not count_refundable_credits:
        return (net_income_withholding_basis(payor_gross, params),
                net_income_withholding_basis(recipient_gross, params))
    if box == 1:
        # Year A: the recipient (majority-nights parent) claims the CTC too --
        # identical to Box 2 in every respect, since she already had HoH, the
        # EITC, and the MA credits regardless of the CTC claim.
        payor_net_recipient_claims = net_income(payor_gross, "single", 0, params)
        recip_net_recipient_claims = net_income(recipient_gross, "hoh", kids, params, kids_under_13)
        # Year B: the s. 152(e)/Form 8332 release moves ONLY the CTC to the payor.
        # He never becomes HoH and never gets the EITC; she keeps both, plus the
        # MA EITC and MA CFTC, and simply loses the federal CTC for that year.
        payor_net_payor_claims = _payor_net_claims_ctc(payor_gross, kids, params)
        recip_net_payor_claims = _custodial_net_no_ctc(recipient_gross, kids, kids_under_13, params)
        payor_net = (payor_net_recipient_claims + payor_net_payor_claims) / 2.0
        recip_net = (recip_net_recipient_claims + recip_net_payor_claims) / 2.0
    else:
        payor_net = net_income(payor_gross, "single", 0, params)
        recip_net = net_income(recipient_gross, "hoh", kids, params, kids_under_13)
    return payor_net, recip_net


def analyze(payor_gross, recipient_gross, kids, weekly_support, weekly_childcare,
            payor_childcare_share, params=TAX_PARAMS, kids_under_13=None, box=2,
            count_refundable_credits=False):
    """box: which custody box the credits should follow (see household_net_incomes()).
    Defaults to 2 (recipient claims all children). Only matters when
    count_refundable_credits=True -- see below. A caller modelling a Box 1 (equal-time)
    scenario with credits on must pass box=1 explicitly to get the corrected
    alternating-year treatment.

    count_refundable_credits: the credits-off switch (added 2026-09-08; DEFAULT FLIPPED
    TO FALSE 2026-09-09, Task 3 of docs/plans/2026-09-09-simplify-to-withholding-basis.md).
    The credits are real but "too complex to reproduce at scale" -- an
    economist reviewing this work will not accept a model that computes every household's
    filing arrangement. So the PUBLISHED default is the withholding basis: net = gross -
    federal income tax (single filer, standard deduction) - Social Security and Medicare -
    Massachusetts income tax, the SAME formula for both parents. About eight constants,
    reproducible in a spreadsheet. This is not a new methodology -- it is the Commonwealth's
    own consultant's method, verbatim from the Economic Review the Task Force adopted: "we
    calculated the net income equivalents of gross weekly income amounts for Massachusetts,
    since the guidelines use gross income and Dr. Betson's study uses net income. We made
    this adjustment using state-specific income withholding tables for Massachusetts and
    standard withholding for Social Security and Medicare." False (the default) removes
    every refundable credit from every figure this function returns: both parties' net
    income comes from net_income_withholding_basis() alone, and `box` and `kids_under_13`
    stop mattering, because filing status and who claims which child matter only because
    they gate the refundable credits. True restores the pre-2026-09-09 behaviour --
    federal and Massachusetts refundable credits (EITC, Child Tax Credit, MA EITC, the MA
    Child and Family Tax Credit) counted in both parties' net income, which requires
    assuming a filing status and who claims which child (`box`) -- kept for the teaching
    tab and any analysis that says so explicitly; it is real, but it is not the ask. See
    household_net_incomes()'s docstring for the reasoning."""
    annual_support = weekly_support * 52.0
    annual_childcare = weekly_childcare * 52.0
    payor_cc = annual_childcare * payor_childcare_share

    payor_net, recip_net = household_net_incomes(payor_gross, recipient_gross, kids,
                                                  params, kids_under_13, box,
                                                  count_refundable_credits)

    payor_after = payor_net - annual_support - payor_cc
    # Support is received tax-free; recipient bears the remaining childcare cost.
    recip_after = recip_net + annual_support - (annual_childcare - payor_cc)

    combined_gross = payor_gross + recipient_gross
    return {
        "payor_gross": payor_gross,
        "recipient_gross": recipient_gross,
        "payor_gross_share": payor_gross / combined_gross,
        "payor_net": payor_net,
        "recip_net": recip_net,
        "payor_eff_rate": 1 - payor_net / payor_gross,
        "recip_eff_rate": 1 - recip_net / recipient_gross if recipient_gross else 0.0,
        "annual_support": annual_support,
        "payor_childcare": payor_cc,
        "support_pct_of_payor_gross": annual_support / payor_gross,
        "support_pct_of_payor_net": annual_support / payor_net,
        "burden_pct_of_payor_net": (annual_support + payor_cc) / payor_net,
        "payor_after": payor_after,
        "recip_after": recip_after,
        "payor_after_share": payor_after / (payor_after + recip_after),
        "recip_per_person": recip_after / (1 + kids),
        "payor_per_person": payor_after,
        "gap": payor_after - recip_after,
    }


def crossover(payor_gross, recipient_gross, kids, weekly_childcare, payor_childcare_share,
              params=TAX_PARAMS, kids_under_13=None, box=2, count_refundable_credits=False):
    """Weekly support at which the recipient household passes the payor in spendable income.

    count_refundable_credits: threaded straight through to analyze() -- see that function's
    docstring. DEFAULT FLIPPED TO FALSE 2026-09-09 alongside analyze(), so this function's
    own default stays consistent with the one it calls; pass True explicitly for the
    credits-on comparison."""
    lo, hi = 0.0, 5_000.0
    for _ in range(200):
        mid = (lo + hi) / 2
        r = analyze(payor_gross, recipient_gross, kids, mid, weekly_childcare,
                    payor_childcare_share, params, kids_under_13, box,
                    count_refundable_credits)
        if r["gap"] > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--payor-gross", type=float, default=220_000)
    p.add_argument("--recipient-gross", type=float, default=31_200)  # ~MA minimum wage FT
    p.add_argument("--kids", type=int, default=2)
    p.add_argument("--weekly-support", type=float, default=None)
    p.add_argument("--weekly-childcare", type=float, default=0.0)
    a = p.parse_args()

    if not TAX_PARAMS["federal_verified"]:
        print("!" * 78)
        print("! FEDERAL TAX CONSTANTS UNVERIFIED -- DO NOT QUOTE ANY NUMBER BELOW.          !")
        print("!" * 78)
    if not TAX_PARAMS["ma_verified"]:
        print("-" * 78)
        print("- NOTE: federal constants verified TY2026. MASSACHUSETTS rate and personal    -")
        print("- exemption are still APPROXIMATE and unchecked against MA DOR publications.  -")
        print("-" * 78)
    print()

    combined = a.payor_gross + a.recipient_gross
    cc_share = a.payor_gross / combined  # proxy for Line 3c available-income share

    print(f"Payor gross      ${a.payor_gross:>12,.0f}")
    print(f"Recipient gross  ${a.recipient_gross:>12,.0f}")
    print(f"Payor gross share of combined: {cc_share:.1%}   Children: {a.kids}\n")

    xo = crossover(a.payor_gross, a.recipient_gross, a.kids, a.weekly_childcare, cc_share)
    print(f"CROSSOVER: recipient household passes payor at ${xo:,.0f}/week "
          f"(${xo*52:,.0f}/yr) of support.\n")

    supports = [500, 750, 1000, 1250, 1500] if a.weekly_support is None else [a.weekly_support]
    hdr = (f"{'wk supp':>8} {'%gross':>7} {'%NET':>7} {'payor after':>13} "
           f"{'recip after':>13} {'payor shr':>10} {'recip/person':>13}")
    print(hdr)
    print("-" * len(hdr))
    for s in supports:
        r = analyze(a.payor_gross, a.recipient_gross, a.kids, s, a.weekly_childcare, cc_share)
        flag = "  <-- SHE IS AHEAD" if r["gap"] < 0 else ""
        print(f"{s:>8,.0f} {r['support_pct_of_payor_gross']:>6.1%} "
              f"{r['support_pct_of_payor_net']:>6.1%} {r['payor_after']:>13,.0f} "
              f"{r['recip_after']:>13,.0f} {r['payor_after_share']:>9.1%} "
              f"{r['recip_per_person']:>13,.0f}{flag}")

    r = analyze(a.payor_gross, a.recipient_gross, a.kids, 1000, a.weekly_childcare, cc_share)
    print(f"\nPayor effective tax rate:     {r['payor_eff_rate']:.1%}")
    print(f"Recipient effective tax rate: {r['recip_eff_rate']:.1%}  (negative = net credits)")
    print("\nThe 40%-of-gross valve at Line 3a fires at "
          f"${0.40*a.payor_gross/52:,.0f}/week of support.")
    print("Expressed against NET, that same order is "
          f"{0.40*a.payor_gross/r['payor_net']:.1%} of take-home.")


if __name__ == "__main__":
    main()
