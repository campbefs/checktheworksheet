#!/usr/bin/env python3
"""Tests for the guidelines reconstruction.

The point of these tests is that a reader who does not trust this project can run them
and confirm the model reproduces the Commonwealth's own published figures. Everything
asserted here is checkable against data/source/MGuidelines.pdf or the Guidelines text.

    python3 model/test_guidelines.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guidelines as g  # noqa: E402

FAILURES = []


def check(name, cond, detail=""):
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}   {detail}")
        FAILURES.append(name)


def main():
    pairs = json.load(open(g._CHART))
    print(f"\nChart: {len(pairs)} rows, ${pairs[0][0]:,}-${pairs[-1][0]:,}/wk combined\n")

    print("-- Table A reproduces the published chart exactly --")
    mismatches = [(i, s, g.table_a(i)) for i, s in pairs if g.table_a(i) != s]
    check("every chart row round-trips through table_a()",
          not mismatches, f"{len(mismatches)} mismatches, e.g. {mismatches[:3]}")

    print("\n-- Chart properties stated by the Task Force --")
    check("maximum combined available income is $8,654/wk",
          pairs[-1][0] == 8654, f"got ${pairs[-1][0]:,}")
    check("$8,654/wk annualizes to ~$450,000 (the stated maximum)",
          abs(pairs[-1][0] * 52 - 450_000) < 100, f"got ${pairs[-1][0]*52:,}")
    check("support is non-decreasing in income",
          all(pairs[i + 1][1] >= pairs[i][1] for i in range(len(pairs) - 1)))
    check("minimum order at $0 available income is $15",
          pairs[0][1] == 15, f"got ${pairs[0][1]}")

    top_marginal = (g.table_a(8600) - g.table_a(4000)) / (8600 - 4000)
    check("top-tranche marginal rate is 10% (Task Force: '10% applied to the highest "
          "income level listed in Table A')",
          abs(top_marginal - 0.10) < 0.005, f"got {top_marginal:.3%}")

    print("\n-- Table B, quoted from Commentary 2021 s.II.L --")
    for n, f in [(2, 1.4), (3, 1.68), (4, 1.85), (5, 1.94)]:
        check(f"Table B factor for {n} children is {f}", g.TABLE_B[n] == f)

    print("\n-- Behavioural sanity --")
    check("chart instruction honoured: value between rows uses the LOWER amount",
          g.table_a(pairs[10][0] + 1) == pairs[10][1])
    check("zero income gives zero order", g.base_order(0, 0, 1) == 0.0)
    check("a payor earning 100% of combined pays the whole obligation",
          abs(g.base_order(1000, 0, 1) - g.table_a(1000)) < 1e-9)
    check("equal incomes split the obligation in half",
          abs(g.base_order(500, 500, 1) - g.table_a(1000) / 2) < 1e-9)
    check("more children never lowers the order",
          all(g.base_order(3000, 1000, n + 1) >= g.base_order(3000, 1000, n)
              for n in range(1, 5)))
    check("order rises with payor income share",
          g.base_order(4000, 800, 2) > g.base_order(2400, 2400, 2))
    check("above the maximum, table_a is capped at the top published amount",
          g.table_a(20_000) == float(pairs[-1][1]))

    print("\n-- Provenance flags are honest about what is NOT verified --")
    check("order_of_operations is flagged UNVERIFIED",
          g.VERIFIED["order_of_operations"] is False)
    check("childcare_adjustment is flagged UNVERIFIED",
          g.VERIFIED["childcare_adjustment"] is False)
    check("parenting_time is flagged UNVERIFIED",
          g.VERIFIED["parenting_time"] is False)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S): {FAILURES}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
