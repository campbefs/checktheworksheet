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

VERIFICATION STATUS (2026-09-02)
  FEDERAL constants VERIFIED for TY2026 -- brackets, standard deduction, SS wage base,
  EITC maxima and phaseouts, CTC. Source: Tax Foundation TY2026 tables.
  MASSACHUSETTS constants STILL APPROXIMATE -- ma_rate and ma_personal_exemption have
  NOT been checked against MA DOR. The runtime banner says so on every run.
Every constant lives in TAX_PARAMS so it can be corrected in one place.

Usage:
    python3 model/net_position.py
    python3 model/net_position.py --payor-gross 220000 --recipient-gross 31200 --kids 2
"""

import argparse

# ---------------------------------------------------------------------------
# PARAMETERS -- federal verified TY2026; MA approximate (see module docstring)
# ---------------------------------------------------------------------------
TAX_PARAMS = {
    "federal_verified": True,   # TY2026, checked 2026-09-02
    # MA verified 2026-09-02. Rate 5%; exemptions single $4,400 / HoH $6,800 (HoH was
    # previously ASSUMED, now confirmed) / $1,000 per dependent.
    # Two REFUNDABLE MA credits were missing entirely until 2026-09-02 and both flow to
    # the lower-income parent claiming the children:
    #   MA EITC = 40% of the federal EITC (raised from 30% by the 2023 tax act).
    #   Child and Family Tax Credit = $440 per qualifying dependent, TY2024 and after,
    #     M.G.L. c. 62 s. 6(x), no cap on the number of dependents, but limited to
    #     dependents UNDER AGE 13 (or disabled, or 65+).
    # mass.gov 403s automated fetch; confirmed via malegislature.gov and the Commonwealth's
    # FY26 tax expenditure budget (budget.digital.mass.gov, item 1.628), which quotes the
    # statute. See docs/2026-09-02-ma-tax-constants-verified.md.
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
            (0.10, 17_700), (0.12, 67_450), (0.22, 105_700), (0.24, 201_775),
            (0.32, 256_200), (0.35, 640_600), (0.37, float("inf")),
        ],
    },
    "ss_rate": 0.062,
    "ss_wage_base": 184_500,
    "medicare_rate": 0.0145,
    "addl_medicare_rate": 0.009,
    "addl_medicare_threshold": 200_000,
    "ma_rate": 0.05,
    "ma_personal_exemption": {"single": 4_400, "hoh": 6_800},
    "ma_dependent_exemption": 1_000,
    "ma_eitc_pct": 0.40,
    "ma_cftc_per_dependent": 440,
    # Refundable credits that flow to the lower-income parent claiming the children.
    "ctc_per_child": 2_200,
    "ctc_refundable_cap": 1_700,
    # EITC by number of qualifying children -- TY2026 verified 2026-09-02.
    # (max credit, phaseout start HoH/single, phaseout end)
    "eitc": {
        0: (664, 10_860, 19_540),
        1: (4_427, 23_890, 51_593),
        2: (7_316, 23_890, 58_629),
        3: (8_231, 23_890, 62_974),
    },
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
    exemption. The 4% surtax on income over $1,000,000 is not modelled -- no scenario
    in this project approaches it."""
    exempt = params["ma_personal_exemption"][status] + params["ma_dependent_exemption"] * kids
    return params["ma_rate"] * max(0.0, gross - exempt)


def ma_refundable_credits(gross, kids, status, params, kids_under_13=None):
    """MA EITC (40% of the federal credit) plus the Child and Family Tax Credit.

    Both are refundable, so for a low-income recipient they are cash, not just tax
    forgiveness -- which is precisely the mechanism the Task Force said "can materially
    affect a household's available income" and then deferred.

    kids_under_13 defaults to all children. The CFTC is limited to dependents under 13
    (or disabled, or 65+), so a household of teenagers gets the EITC portion only."""
    if status != "hoh" or kids == 0:
        return 0.0
    if kids_under_13 is None:
        kids_under_13 = kids
    fed_eitc = _federal_eitc(gross, kids, params)
    return params["ma_eitc_pct"] * fed_eitc + params["ma_cftc_per_dependent"] * kids_under_13


def _federal_eitc(gross, kids, params):
    mx, start, end = params["eitc"][min(kids, 3)]
    if gross <= start:
        return float(mx)
    if gross >= end:
        return 0.0
    return mx * (end - gross) / (end - start)


def refundable_credits(gross, kids, status, params):
    """Federal CTC + EITC for the parent claiming the children.

    IRC s. 24(d): the refundable Additional Child Tax Credit is the LEAST of the
    entitlement remaining after it offsets tax liability, $1,700 per child, and
    15% of earned income above $2,500. An earlier version omitted the earned-income
    phase-in and added a flat credit on top of a fully-subtracted liability, which
    OVERSTATED the recipient by about $480/yr on the worked example. The docstring
    then called that "deliberately conservative" -- it was conservative in the wrong
    direction, i.e. it flattered this project's own argument. Caught in QA 2026-09-02."""
    if status != "hoh" or kids == 0:
        return 0.0
    entitlement = params["ctc_per_child"] * kids
    tax_owed = federal_tax(gross, status, params)
    nonrefundable = min(entitlement, tax_owed)
    refundable = min(entitlement - nonrefundable,
                     params["ctc_refundable_cap"] * kids,
                     0.15 * max(0.0, gross - 2_500))
    return nonrefundable + refundable + _federal_eitc(gross, kids, params)


def net_income(gross, status, kids, params, kids_under_13=None):
    """After-tax income including federal AND Massachusetts refundable credits."""
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
    claim is commonly alternated by year. Measured in tools/net_basis_sensitivity.py:
    who claims the children moves the post-transfer share 7.8 points, more than the
    credits themselves are worth (4.8 points). A Worksheet line cannot rest on an
    input the Worksheet does not have.

    The omission runs AGAINST the payor: including the credits would put his share
    at 48.2% rather than 53.0%, so the rule as proposed understates the case for it.
    """
    return gross - (federal_tax(gross, "single", params)
                    + fica(gross, params)
                    + ma_tax(gross, "single", params, 0))


def analyze(payor_gross, recipient_gross, kids, weekly_support, weekly_childcare,
            payor_childcare_share, params=TAX_PARAMS, kids_under_13=None):
    annual_support = weekly_support * 52.0
    annual_childcare = weekly_childcare * 52.0
    payor_cc = annual_childcare * payor_childcare_share

    payor_net = net_income(payor_gross, "single", 0, params)
    recip_net = net_income(recipient_gross, "hoh", kids, params, kids_under_13)

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
              params=TAX_PARAMS, kids_under_13=None):
    """Weekly support at which the recipient household passes the payor in spendable income."""
    lo, hi = 0.0, 5_000.0
    for _ in range(200):
        mid = (lo + hi) / 2
        r = analyze(payor_gross, recipient_gross, kids, mid, weekly_childcare,
                    payor_childcare_share, params, kids_under_13)
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
