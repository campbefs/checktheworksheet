#!/usr/bin/env python3
"""Massachusetts 2025 Child Support Guidelines — base order calculation.

PROVENANCE OF EVERY COMPONENT (this matters; read before trusting output)
-------------------------------------------------------------------------
VERIFIED — reconstructed directly from the Commonwealth's own published chart:
  Table A, as applied.  `data/extracted/guidelines-chart.json` holds 1,104
  (combined available income -> weekly support, one child under 18) pairs parsed from
  data/source/MGuidelines.pdf, the official "2025 Child Support Guidelines Chart".
  Monotonic, no gaps. Range $0-$8,654/wk combined ( = $450,008/yr, matching the stated
  $450,000 maximum). Recovered marginal-rate profile:
      $304-$392   minimum tranche
      $392-$1,500   ~22% -> 21%
      $1,500-$2,400 ~18%
      $2,400-$3,500 ~14%
      $3,500-$8,654  10.0%   <- matches the Task Force's stated "10% applied to the
                                 highest income level listed in Table A"
  Eight tranches, six between $392 and $8,654 -- matches the Task Force report exactly.

VERIFIED — quoted from Commentary 2021 to Section II.L, carried forward into 2025:
  Table B adjustment factors: 1.4 (2 children), 1.68 (3), 1.85 (4), 1.94 (5).
  Table C: 25% discount for children 18-23, applied to the oldest children last.

*** INFERRED -- NOT VERIFIED -- THE WORKSHEET CJ-D 304 HAS NOT BEEN OBTAINED ***
  The ORDER OF OPERATIONS below is an inference, not the worksheet:
    (1) look up Table A on COMBINED available income
    (2) multiply by the Table B factor for the number of children
    (3) multiply by the payor's share of combined available income (Line 3c)
  Also NOT modelled at all: the combined child care / health care adjustment, the
  parenting-time treatment (shared / split / two-thirds boxes at Line 1b), Table C age
  adjustments, and the >$450,000 discretionary band.

  => Output is a BASE ESTIMATE. It is NOT the presumptive order. Do not put a number
     from this file in front of anyone until CJ-D 304 is encoded and this file
     reproduces a worked example from the worksheet itself.
"""

import bisect
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHART = os.path.join(_HERE, os.pardir, "data", "extracted", "guidelines-chart.json")

TABLE_B = {1: 1.0, 2: 1.4, 3: 1.68, 4: 1.85, 5: 1.94}

VERIFIED = {
    "table_a": True,       # reconstructed from the official published chart
    "table_b": True,       # quoted from Commentary 2021 s.II.L
    "order_of_operations": False,   # INFERRED -- needs CJ-D 304
    "childcare_adjustment": False,  # not modelled
    "parenting_time": False,        # not modelled
}


def _load():
    pairs = json.load(open(_CHART))
    return [p[0] for p in pairs], [p[1] for p in pairs]


_INC, _SUP = _load()


def table_a(combined_weekly):
    """Weekly support for ONE child under 18 at a given combined available income.

    This is a lookup against the Commonwealth's published chart, not a formula.
    Per the chart's own instruction: 'If available income falls between two numbers,
    use the lower support amount.'
    """
    if combined_weekly < 0:
        return 0.0
    if combined_weekly > _INC[-1]:
        # Above the $450,000 maximum the order is discretionary. Return the maximum
        # presumptive amount; the excess is NOT modelled.
        return float(_SUP[-1])
    i = bisect.bisect_right(_INC, combined_weekly) - 1
    return float(_SUP[max(0, i)])


def base_order(payor_weekly_available, recipient_weekly_available, children=1):
    """BASE ESTIMATE of the weekly order. See module docstring -- order of operations
    is INFERRED and the child care / parenting-time adjustments are NOT modelled."""
    if children not in TABLE_B:
        raise ValueError(f"children must be 1-5, got {children}")
    combined = payor_weekly_available + recipient_weekly_available
    if combined <= 0:
        # No income on either side: there is no share to apportion. The chart's $15
        # minimum-order row is a Table A value, not an order this function can assign.
        return 0.0
    total = table_a(combined) * TABLE_B[children]
    payor_share = payor_weekly_available / combined
    return total * payor_share


def describe(payor_annual, recipient_annual, children=1):
    pw, rw = payor_annual / 52.0, recipient_annual / 52.0
    combined = pw + rw
    one_child = table_a(combined)
    total = one_child * TABLE_B[children]
    share = pw / combined
    order = total * share
    return {
        "combined_weekly": combined,
        "combined_annual": combined * 52,
        "table_a_one_child": one_child,
        "table_b_factor": TABLE_B[children],
        "total_obligation_weekly": total,
        "payor_share": share,
        "base_order_weekly": order,
        "base_order_annual": order * 52,
        "over_maximum": combined > _INC[-1],
    }


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--payor-gross", type=float, default=220_000)
    p.add_argument("--recipient-gross", type=float, default=31_200)
    p.add_argument("--kids", type=int, default=2)
    a = p.parse_args()

    print("=" * 78)
    print("BASE ESTIMATE ONLY -- order of operations INFERRED; child care and")
    print("parenting-time adjustments NOT modelled. CJ-D 304 not yet obtained.")
    print("=" * 78)
    d = describe(a.payor_gross, a.recipient_gross, a.kids)
    print(f"\nCombined available   ${d['combined_annual']:>11,.0f}/yr  "
          f"(${d['combined_weekly']:,.0f}/wk)")
    if d["over_maximum"]:
        print("  ** ABOVE the $450,000 maximum -- amount above is discretionary, NOT modelled **")
    print(f"Table A, one child   ${d['table_a_one_child']:>11,.0f}/wk")
    print(f"Table B x{d['table_b_factor']:<4}       ${d['total_obligation_weekly']:>11,.0f}/wk total obligation")
    print(f"Payor share          {d['payor_share']:>11.1%}")
    print(f"\nBASE ORDER           ${d['base_order_weekly']:>11,.0f}/wk  "
          f"(${d['base_order_annual']:,.0f}/yr)")
