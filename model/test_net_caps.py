#!/usr/bin/env python3
"""Tests for the two net-pay ceilings in model/net_caps.py.

Same local check()/FAILS shape as every other suite in this folder -- not
pytest.

    .venv/bin/python model/test_net_caps.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import net_caps as nc
from model.net_position import net_income_withholding_basis
from model import worksheet as w

N = 0
FAILS = []


def check(name, ok, detail=""):
    global N
    N += 1
    if not ok:
        FAILS.append(f"{name}{(' -- ' + detail) if detail else ''}")


def close(a, b, tol=0.01):
    return abs(a - b) <= tol


# --- which ceiling applies to which box ------------------------------------

check("Box 1 takes the shared ceiling", nc.cap_for(1) == nc.CAP_SHARED)
check("Box 2 takes the primary ceiling", nc.cap_for(2) == nc.CAP_PRIMARY)
check("Box 3 takes the shared ceiling, not the primary one",
      nc.cap_for(3) == nc.CAP_SHARED,
      "a split has both households carrying duplicated fixed costs")
check("the shared ceiling is below the primary ceiling",
      nc.CAP_SHARED < nc.CAP_PRIMARY)

# --- the worked example ----------------------------------------------------

rows = {(r["box"], r["childcare_total"]): r for r in nc.worked_example()}

b1 = rows[(1, 0.0)]
check("worked example Box 1 order is unchanged by this file",
      close(b1["weekly"], 1012.73),
      f"got {b1['weekly']:.2f}, expected the published 1012.73")
check("worked example payor net is the withholding basis",
      close(b1["net"], net_income_withholding_basis(nc.PAYOR_GROSS)))
check("worked example Box 1 is over the 25 percent ceiling",
      b1["binds"] and close(b1["share_of_net"], 0.3766, 0.0005),
      f"got {b1['share_of_net']*100:.2f}% of net")

b2 = rows[(2, 0.0)]
check("worked example Box 2 order is unchanged by this file",
      close(b2["weekly"], 1087.90),
      f"got {b2['weekly']:.2f}")
check("worked example Box 2 is over the 40 percent ceiling, with no child care at all",
      b2["binds"] and b2["share_of_net"] > 0.40,
      f"got {b2['share_of_net']*100:.2f}% of net -- this is the headline")
check("worked example Box 2 clears 40 percent by less than a point",
      b2["share_of_net"] - 0.40 < 0.01,
      f"got {(b2['share_of_net']-0.40)*100:.2f} points over")

# The units gap is the reason the existing Section IV.C presumption does not
# fire here: it reads Line 7e, which is computed on a gross-derived figure.
for key, r in rows.items():
    check(f"Line 7e reads lower than the true share of net, box {key[0]} cc {key[1]:.0f}",
          r["line_7e"] < r["share_of_net"],
          f"7e {r['line_7e']*100:.1f}% vs net {r['share_of_net']*100:.1f}%")

check("the units gap at the worked example is at least 10 points",
      b2["share_of_net"] - b2["line_7e"] >= 0.10,
      f"got {(b2['share_of_net']-b2['line_7e'])*100:.1f} points")

# --- the ceiling arithmetic itself -----------------------------------------

for r in rows.values():
    check(f"capped order never exceeds the ceiling, box {r['box']} cc {r['childcare_total']:.0f}",
          r["capped_annual"] <= r["ceiling_annual"] + 0.01)
    check(f"capped order never exceeds the uncapped order, box {r['box']} cc {r['childcare_total']:.0f}",
          r["capped_annual"] <= r["annual"] + 0.01)
    check(f"reduction is the difference, box {r['box']} cc {r['childcare_total']:.0f}",
          close(r["reduction_annual"], r["annual"] - r["capped_annual"]))

# A ceiling that does not bind must change nothing at all.
easy = nc.order_and_cap(nc.PAYOR_GROSS, 120000 / 52.0, 3, 1, 0.0, 33.0, 43.0)
check("a ceiling that does not bind leaves the order alone",
      not easy["binds"] and close(easy["capped_weekly"], easy["weekly"]),
      f"{easy['share_of_net']*100:.1f}% of net")
check("a ceiling that does not bind reports a zero reduction",
      close(easy["reduction_annual"], 0.0))

# --- child care always pushes toward the ceiling ---------------------------

for box in (1, 2):
    dry = rows[(box, 0.0)]
    wet = rows[(box, 300.0)]
    check(f"child care raises the share of net, box {box}",
          wet["share_of_net"] > dry["share_of_net"])
    check(f"child care cannot lower the capped order, box {box}",
          wet["capped_annual"] >= dry["capped_annual"] - 0.01)

# --- the gap, not the level, is what drives the ceiling --------------------

gap = nc.sweep_gap()
shares = [r["share_of_net"] for r in gap]
check("share of net falls monotonically as the other parent earns more",
      all(a >= b - 1e-9 for a, b in zip(shares, shares[1:])),
      "this is why sweeping payor income alone overstates how often the ceiling binds")
check("the 25 percent ceiling stops binding once the gap narrows",
      gap[0]["binds"] and not gap[-1]["binds"])

# --- the published grids ---------------------------------------------------

grids = {(k, b): nc.grid_share_over(k, b) for k in (1, 2, 3) for b in (1, 2)}

for key, g in grids.items():
    check(f"grid {key} has the project's standard 1,147 cells",
          g["cells"] == 1147, f"got {g['cells']}")
    check(f"grid {key} measures against its own box's ceiling",
          close(g["cap"], nc.cap_for(key[1]), 1e-9))

check("the 40 percent ceiling reaches nothing with one child",
      grids[(1, 2)]["over"] == 0)
check("the 40 percent ceiling reaches nothing with two children",
      grids[(2, 2)]["over"] == 0,
      "so this ask changes no one- or two-child primary order anywhere on the grid")
check("the 40 percent ceiling does reach three-child primary orders",
      grids[(3, 2)]["over"] > 0 and 0.40 < grids[(3, 2)]["share_over"] < 0.45,
      f"got {grids[(3,2)]['share_over']*100:.1f}% of cells")

check("the 25 percent ceiling reaches most three-child equal-time orders",
      0.60 < grids[(3, 1)]["share_over"] < 0.65,
      f"got {grids[(3,1)]['share_over']*100:.1f}% of cells")
check("the 25 percent ceiling reaches about half of two-child equal-time orders",
      0.45 < grids[(2, 1)]["share_over"] < 0.52,
      f"got {grids[(2,1)]['share_over']*100:.1f}% of cells")
check("the 25 percent ceiling reaches few one-child equal-time orders",
      grids[(1, 1)]["share_over"] < 0.12,
      f"got {grids[(1,1)]['share_over']*100:.1f}% of cells")

# The asymmetry is the finding, so pin it: the shared ceiling is a schedule
# change and the primary ceiling is a backstop, and no rounding should let
# those two be described the same way.
check("the shared ceiling reaches far more of its grid than the primary one does",
      grids[(3, 1)]["share_over"] > grids[(3, 2)]["share_over"] + 0.15,
      f"{grids[(3,1)]['share_over']*100:.1f}% vs {grids[(3,2)]['share_over']*100:.1f}%")

# --- where the ceiling sits relative to the Line 6b allocation --------------

# With nothing claimed there is no allocation, so the question does not arise
# and the two orderings must not be able to disagree.
for box in (1, 2):
    z = nc.cap_orderings(nc.PAYOR_GROSS, nc.RECIP_WEEKLY, nc.KIDS, box, 0.0,
                         nc.A_HEALTH, nc.B_HEALTH)
    check(f"the two orderings agree exactly with no child care, box {box}",
          close(z["before_annual"], z["after_annual"]) and abs(z["cc_component_annual"]) < 0.01)

# The measured pass-through: the child-care component of Line 7d is the payor's
# own 6b allocation, not some function of it.
sheet = w.run(box=1, a_gross=nc.RECIP_WEEKLY, b_gross=nc.PAYOR_GROSS / 52.0,
              children_under18=nc.KIDS, a_health=nc.A_HEALTH, b_health=nc.B_HEALTH,
              a_childcare=(100.0, 100.0, 100.0), b_childcare=(0.0, 0.0, 0.0))
cc300 = nc.cap_orderings(nc.PAYOR_GROSS, nc.RECIP_WEEKLY, nc.KIDS, 1, 300.0,
                         nc.A_HEALTH, nc.B_HEALTH)
check("the child-care component of Line 7d is the payor's own 6b allocation",
      close(cc300["cc_component_annual"] / 52.0, sheet["A_6b"]),
      f"component {cc300['cc_component_annual']/52:.2f} vs 6b {sheet['A_6b']:.2f}")

for box in (1, 2):
    swept = nc.sweep_childcare(box=box)
    ceiling = swept[0]["ceiling_annual"]

    check(f"capping after the allocation never breaches the ceiling, box {box}",
          all(r["after_annual"] <= r["ceiling_annual"] + 0.01 for r in swept))
    check(f"capping before the allocation breaches it whenever care is claimed, box {box}",
          all(r["before_exceeds_ceiling"] for r in swept if r["childcare_total"] > 0),
          "this is the case against writing the rule that way -- it is not a ceiling")
    check(f"capping before the allocation is never lower than capping after, box {box}",
          all(r["before_annual"] >= r["after_annual"] - 0.01 for r in swept))
    check(f"at the Guidelines' own $430 per child maximum the ceiling still holds, box {box}",
          close(swept[-1]["after_annual"], ceiling),
          f"got {swept[-1]['after_annual']:.2f} against {ceiling:.2f}")

# The headline against BEFORE: a ceiling named 25 or 40 percent that permits far
# more than that. Pin both figures so a constant change cannot quietly soften it.
worst1 = nc.sweep_childcare(box=1)[-1]
worst2 = nc.sweep_childcare(box=2)[-1]
check("a 25 percent ceiling applied before the allocation permits over 65 percent of net",
      worst1["before_share_of_net"] > 0.65,
      f"got {worst1['before_share_of_net']*100:.1f}%")
check("a 40 percent ceiling applied before the allocation permits over 80 percent of net",
      worst2["before_share_of_net"] > 0.80,
      f"got {worst2['before_share_of_net']*100:.1f}%")

# The case FOR applying it before: at high claimed child care the capped order
# no longer covers what the payor owes toward a cost already paid.
check("the capped order still covers the payor's child-care share at $300 a week",
      cc300["cc_covered_after"])
check("the capped order stops covering it at the legal maximum, equal time",
      not worst1["cc_covered_after"],
      "this is the real cost of capping after the allocation and it must be stated")
check("that crossover sits above half the legal maximum, so it is the uncommon case",
      nc.cap_orderings(nc.PAYOR_GROSS, nc.RECIP_WEEKLY, nc.KIDS, 1, 645.0,
                       nc.A_HEALTH, nc.B_HEALTH)["cc_covered_after"],
      "at $645 a week, half the $430-per-child maximum, the allocation is still covered")

# --- the exhibit's own claim ------------------------------------------------

# E28 (model/charts/fig12_net_pay_ceiling.py) says the order passes 40 percent of
# the payor's net pay in 473 of 1,147 income combinations while Line 7e flags none
# of them. The chart asserts this for itself at render time; this pins it in the
# suite as well, so a constant change is caught before anyone rebuilds a figure.
import csv as _csv

_grid = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "output", "charts", "fig1_heatmap_3child_box2.csv")
if not os.path.isfile(_grid):  # the published repo carries the same CSV at figures/working/
    _grid = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "figures", "working", "fig1_heatmap_3child_box2.csv")
with open(_grid, newline="", encoding="utf-8") as _fh:
    _rows = list(_csv.DictReader(_fh))
_net = [float(r["order_pct_payor_net"]) for r in _rows]
_e7 = [float(r["line_7e"]) for r in _rows]

check("E28: 473 of the 1,147 three-child primary cells pass 40 percent of net",
      sum(n > 0.40 for n in _net) == 473 and len(_rows) == 1147,
      f"got {sum(n > 0.40 for n in _net)} of {len(_rows)}")
check("E28: Line 7e passes 40 percent in none of them",
      sum(x > 0.40 for x in _e7) == 0,
      "the exhibit's second clause fails if this is ever nonzero")
check("E28: every cell's Line 7e understates the true share of net",
      all(x < n for x, n in zip(_e7, _net)),
      "the scatter sits entirely above the diagonal, and the caption says so")

# --- where the order today crosses the federal CCPA collection ceiling -----
# Pins the petition's section 5 figures, so a constant change is caught here
# before it can go stale in an outbound document again.

check("this payor's CCPA ceiling is 60 percent, not the general 25 percent cap",
      nc.CCPA_CEILING_THIS_PAYOR == 0.60,
      "15 U.S.C. s 1673(b)(2)(B): no other household, no arrears")

for _box, _cross_expect, _top_expect in ((1, 686.0, 0.7972), (2, 600.0, 0.8252)):
    _r = nc.ccpa_crossing(_box)
    check(f"box {_box}: no-child-care share matches order_and_cap's own figure",
          close(_r["share_at_0"],
                nc.order_and_cap(nc.PAYOR_GROSS, nc.RECIP_WEEKLY, nc.KIDS, _box,
                                 0.0, nc.A_HEALTH, nc.B_HEALTH)["share_of_net"],
                tol=1e-9))
    check(f"box {_box}: order today crosses 60 percent within the legal child-care range",
          _r["crossing_wk"] is not None)
    check(f"box {_box}: crossing point is ${_cross_expect:.0f}/wk",
          _r["crossing_wk"] == _cross_expect,
          f"got {_r['crossing_wk']}")
    check(f"box {_box}: crossing point is well under the $1,290/wk legal maximum",
          _r["crossing_wk"] < 1290.0,
          "an ordinary claimed amount, not only the extreme case")
    check(f"box {_box}: share at the legal maximum is {_top_expect*100:.1f} percent",
          close(_r["share_at_top"], _top_expect, tol=0.0005),
          f"got {_r['share_at_top']}")
    check(f"box {_box}: share rises monotonically past the ceiling once it crosses",
          nc.order_and_cap(nc.PAYOR_GROSS, nc.RECIP_WEEKLY, nc.KIDS, _box,
                           _r["crossing_wk"] + 50.0, nc.A_HEALTH, nc.B_HEALTH)["share_of_net"]
          > nc.CCPA_CEILING_THIS_PAYOR,
          "fifty dollars further in should still be over, not back under")

check("box 2 (primary) crosses the ceiling at less claimed child care than box 1 (equal time)",
      nc.ccpa_crossing(2)["crossing_wk"] < nc.ccpa_crossing(1)["crossing_wk"])

check("the grid's own no-child-care maximum (46.6%) is still under this payor's ceiling",
      nc.grid_share_over(3, 2)["max"] < nc.CCPA_CEILING_THIS_PAYOR,
      "confirms the petition's 46.6% figure is compatible with 'crosses only once "
      "child care is claimed', not a second contradiction")

# --- report ----------------------------------------------------------------

if FAILS:
    print(f"FAILED {len(FAILS)} of {N} checks:")
    for f in FAILS:
        print("  -", f)
    sys.exit(1)
print(f"All checks passed ({N}).")
