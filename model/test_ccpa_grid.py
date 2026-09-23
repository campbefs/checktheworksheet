#!/usr/bin/env python3
"""Pins every figure model/ccpa_grid.py produces that a document may quote.

Run: .venv/bin/python model/test_ccpa_grid.py

The most important test in this file is the FIRST one, and it is the one that
protects against our own argument: with no child care claimed, the Guidelines order
crosses no federal ceiling anywhere on the grid. If that ever starts failing, the
claim in every outbound document -- "the order alone stays under; child care is what
carries it past" -- has become false and must be rewritten, not patched.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import ccpa_grid as g
from model import net_caps as nc
from model import worksheet as w
from model.net_position import net_income_withholding_basis

CHECKS = []


def check(label, cond):
    CHECKS.append((label, bool(cond)))


# --- The statute's four rates -------------------------------------------------
check("four CCPA rates, 50/55/60/65", g.RATES == [0.50, 0.55, 0.60, 0.65])
check("supporting another household gives the LOWEST ceiling",
      g.CCPA_RATES[(True, False)] == 0.50 and g.CCPA_RATES[(False, True)] == 0.65)
check("net_caps' single-payor constant is one of the four",
      nc.CCPA_CEILING_THIS_PAYOR in g.RATES)
check("Guidelines child-care maximum is $430/child/week, s II.E.1",
      g.GUIDELINES_MAX_CHILDCARE_PER_CHILD == 430.0)

# --- The counterweight: no child care crosses nothing, anywhere ---------------
for kids in (1, 2, 3):
    for box in (1, 2):
        r = g.crossings(kids, box, 0.0)
        check(f"{kids} kids Box {box}: 1,147 cells", r["cells"] == 1147)
        check(f"{kids} kids Box {box}: NO crossing at any rate with no child care",
              all(r["over"][rate]["n"] == 0 for rate in g.RATES))
        check(f"{kids} kids Box {box}: max under the lowest ceiling with no child care",
              r["max"] < 0.50)

# The highest no-child-care share anywhere, which is the number quoted as the
# counterweight. 3 children, Box 2.
check("highest no-child-care share is 46.6% (3 kids, Box 2)",
      abs(g.crossings(3, 2, 0.0)["max"] - 0.466) < 0.001)

# --- At the worked example's own claim, $100/child/week -----------------------
w3b1 = g.crossings(3, 1, 300.0)
w3b2 = g.crossings(3, 2, 300.0)
check("3 kids Box 1 at $300/wk: 203 cells over 50%", w3b1["over"][0.50]["n"] == 203)
check("3 kids Box 1 at $300/wk: 72 cells over 60%", w3b1["over"][0.60]["n"] == 72)
check("3 kids Box 2 at $300/wk: 459 cells over 50%", w3b2["over"][0.50]["n"] == 459)
check("3 kids Box 2 at $300/wk: max 77.4% of net",
      abs(w3b2["max"] - 0.774) < 0.002)

# --- At the Guidelines' own maximum claim -------------------------------------
m3b2 = g.crossings(3, 2, 1290.0)
check("3 kids Box 2 at the maximum: every cell over 50%",
      m3b2["over"][0.50]["n"] == 1147)
check("3 kids Box 2 at the maximum: 1,133 cells over 60%",
      m3b2["over"][0.60]["n"] == 1133)
check("3 kids Box 2 at the maximum: max order exceeds the payor's whole net pay",
      m3b2["max"] > 1.0)

# --- Orderings that must hold for the analysis to mean anything ---------------
for kids in (1, 2, 3):
    for box in (1, 2):
        top = g.GUIDELINES_MAX_CHILDCARE_PER_CHILD * kids
        none, worked, mx = (g.crossings(kids, box, 0.0),
                            g.crossings(kids, box, 100.0 * kids),
                            g.crossings(kids, box, top))
        check(f"{kids}/{box}: more child care never reduces crossings",
              none["over"][0.50]["n"] <= worked["over"][0.50]["n"] <= mx["over"][0.50]["n"])
        check(f"{kids}/{box}: a lower ceiling is crossed by at least as many cells",
              all(mx["over"][g.RATES[i]]["n"] >= mx["over"][g.RATES[i + 1]]["n"]
                  for i in range(len(g.RATES) - 1)))

# --- The crossing cells are ordinary incomes, not the grid's extremes ---------
low = g.cells_over(3, 2, 50.0, 0.50)
check("at $50/wk total child care, 9 cells cross the 50% ceiling", len(low) == 9)
check("the first crossings are ORDINARY incomes, $60k-$100k, not the grid ceiling",
      all(60000.0 <= hi <= 100000.0 for hi, lo, s in low))
check("no crossing cell is a high earner -- this is not a rich-payor finding",
      max(hi for hi, lo, s in low) < 150000.0)
check("the first crossings are against a near-zero-income other parent",
      all(lo <= 5000.0 for hi, lo, s in low))

# --- The lowest claim that crosses, by configuration -------------------------
check("3 kids Box 2 crosses 50% at $50/wk total claimed child care",
      g.first_crossing_childcare(3, 2, 0.50) == 50.0)
check("1 child Box 1 needs $230/wk to cross 50%",
      g.first_crossing_childcare(1, 1, 0.50) == 230.0)

# --- The grid figure reproduces the worksheet directly (no wrapper drift) ----
# One cell, computed straight from worksheet.py, must match share_of_net.
hi, lo, kids, box, cc = 85000.0, 0.0, 3, 2, 50.0
direct = nc.order_and_cap(hi, lo / 52.0, kids, box, cc, g.A_HEALTH, g.B_HEALTH)
check("share_of_net matches order_and_cap on a named cell",
      abs(g.share_of_net(hi, lo, kids, box, cc) - direct["share_of_net"]) < 1e-12)
check("that cell's order really is above half the payor's net pay",
      direct["annual"] > 0.50 * net_income_withholding_basis(hi))

# --- Report ------------------------------------------------------------------
failed = [c for c in CHECKS if not c[1]]
for label, ok in CHECKS:
    if not ok:
        print(f"FAIL  {label}")
print(f"\n{len(CHECKS) - len(failed)}/{len(CHECKS)} checks passed")
sys.exit(1 if failed else 0)
