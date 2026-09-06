#!/usr/bin/env python3
"""Regression tests for the CJ-D 304 worksheet implementation.

The important ones are the VALIDATION tests: the model is pinned against a real
Massachusetts child support calculation whose output is independently known. If a
future change breaks those, the change is wrong.

    python3 model/test_worksheet.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worksheet as w  # noqa: E402

FAILURES = []


def _raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + ("" if cond else f"   {detail}"))
    if not cond:
        FAILURES.append(name)


def case(cc_total, box=1):
    """The worked example (the author's own order, disclosed in the Comments): $201,000 / $570wk / 3 children, premiums $43 / $33."""
    per = cc_total / 3.0
    return w.run(box=box, a_gross=570.0, b_gross=201000 / 52.0, children_under18=3,
                 a_health=33.0, b_health=43.0,
                 a_childcare=(per, per, per), b_childcare=(0, 0, 0))


def main():
    print("\n-- Table A, transcribed from CJ-D 304 page 4 --")
    for x, expect in [(301, 15), (391, 33), (1000, 220), (1600, 346),
                      (2400, 490), (3500, 644), (5000, 809), (8654, 1174)]:
        got = w.table_a(x)
        check(f"Table A(${x:,}) == ${expect:,}", abs(got - expect) <= 1, f"got ${got:,.0f}")

    print("\n-- Table B and C, quoted from the worksheet --")
    check("Table B: 0 children -> 0.00", w.TABLE_B[0] == 0.00)
    check("Table B: 3 children -> 1.68", w.TABLE_B[3] == 1.68)
    check("Table C: 2 under 18 + 1 over -> 4%", w.TABLE_C[(2, 1)] == .04)

    print("\n-- VALIDATION against the disclosed order (the load-bearing tests) --")
    r0 = case(0)
    check("shared 50-50, no child care -> ~$1,013/wk",
          1008 <= r0["7d"] <= 1018, f"got ${r0['7d']:,.0f}")
    r300 = case(300)
    check("shared 50-50, $300/wk child care -> ~$1,276/wk",
          1271 <= r300["7d"] <= 1281, f"got ${r300['7d']:,.0f}")
    check("payor is Parent B (the higher earner)", r0["payor"] == "B")
    check("3a nets out health premiums: his $3,865.38 - $43 = $3,822.38",
          abs(r0["B_3a"] - 3822.38) < 0.01, f"got ${r0['B_3a']:,.2f}")
    check("his share of combined available income ~87.68%",
          abs(r0["B_3c"] - 0.8768) < 0.001, f"got {r0['B_3c']:.2%}")

    print("\n-- Child care flows into Line 7e (the correction of 2026-09-02) --")
    check("child care RAISES the order", r300["7d"] > r0["7d"],
          "if this fails, child care is not reaching 6c/6g/7d")
    check("child care RAISES 7e", r300["7e"] > r0["7e"])
    check("$300/wk child care adds ~$263/wk to the order",
          260 <= r300["7d"] - r0["7d"] <= 266, f"got ${r300['7d']-r0['7d']:,.0f}")
    check("6b = other parent's income share x child care paid",
          abs(r300["A_6b"] - 0.8768 * 300) < 1.0)

    print("\n-- The 40% hardship box --")
    check("does NOT fire at $300/wk child care (7e ~33.4%)",
          not r300["hardship_box"], f"7e={r300['7e']:.1%}")
    check("DOES fire at $900/wk child care", case(900)["hardship_box"])
    check("7e rises monotonically with child care",
          all(case(c)["7e"] <= case(c + 100)["7e"] for c in range(0, 1200, 100)))

    print("\n-- $430/child benchmark cap (6a) --")
    over = case(3 * 600)          # $600/child, above the $430 cap
    at_cap = case(3 * 430)
    check("child care above $430/child is capped at the benchmark",
          abs(over["7d"] - at_cap["7d"]) < 1.0,
          f"${over['7d']:,.0f} vs ${at_cap['7d']:,.0f}")

    print("\n-- Parenting time: Box 2 costs MORE than Box 1 --")
    b1, b2 = case(0, box=1), case(0, box=2)
    check("primary (Box 2) order exceeds shared (Box 1)", b2["7d"] > b1["7d"])
    credit = 1 - b1["7d"] / b2["7d"]
    check("joint-custody credit is ~6.9%", 0.06 <= credit <= 0.08, f"got {credit:.1%}")

    print("\n-- Shared-parenting adjustment vs income disparity (submission section 5) --")
    def diff(a_gross):
        k = dict(b_gross=201000 / 52.0, children_under18=3, a_health=33.0, b_health=43.0)
        b1 = w.run(box=1, a_gross=a_gross, **k)
        b2 = w.run(box=2, a_gross=a_gross, **k)
        return b1["B_3c"], 1 - b1["7d"] / b2["7d"]
    pts = [diff(a) for a in (200, 400, 570, 800, 1200, 1600, 2000, 2500, 3000)]
    check("the Box 2 -> Box 1 reduction falls as the payor's income share rises",
          all(pts[i][1] < pts[i + 1][1] for i in range(len(pts) - 1)),
          f"{[f'{s:.1%}->{d:.1%}' for s, d in pts]}")
    check("~77.6% at a 56.3% payor share", abs(pts[-1][1] - 0.776) < 0.01, f"{pts[-1][1]:.1%}")
    check("~1.3% at a 95.8% payor share", abs(pts[0][1] - 0.013) < 0.005, f"{pts[0][1]:.1%}")

    print("\n-- Child care allocation ignores the parenting box (and the 6e clip) --")
    kk = dict(a_gross=570.0, b_gross=201000 / 52.0, children_under18=3,
              a_health=33.0, b_health=43.0)
    cc = (100, 100, 100)
    hers = {b: w.run(box=b, a_childcare=cc, b_childcare=(0, 0, 0), **kk) for b in (1, 2)}
    his = {b: w.run(box=b, a_childcare=(0, 0, 0), b_childcare=cc, **kk) for b in (1, 2)}
    base = {b: w.run(box=b, **kk) for b in (1, 2)}
    check("6b is identical under Box 1 and Box 2 -- no parenting-time term",
          abs(hers[1]["A_6b"] - hers[2]["A_6b"]) < 1e-9)
    check("payor funds ~87.7% of child care the recipient pays, either box",
          all(abs(hers[b]["A_6b"] / 300 - 0.8768) < 0.001 for b in (1, 2)))
    up = {b: hers[b]["7d"] - base[b]["7d"] for b in (1, 2)}
    check("the order rises by the same amount in both boxes",
          abs(up[1] - up[2]) < 0.01, f"{up[1]:.2f} vs {up[2]:.2f}")
    down = {b: base[b]["7d"] - his[b]["7d"] for b in (1, 2)}
    check("Box 2: payor paying child care recovers the full 12.3% (~$36.95)",
          abs(down[2] - 36.95) < 0.05, f"got ${down[2]:.2f}")
    check("Box 1: the 6e clip cuts that credit to ~$5.19 (1.7c on the dollar)",
          abs(down[1] - 5.19) < 0.05, f"got ${down[1]:.2f}")
    check("the clip factor is the ratio of available incomes (537/3822 = 14.0%)",
          abs(down[1] / down[2] - his[1]["A_3a"] / his[1]["B_3a"]) < 0.002,
          f"{down[1]/down[2]:.3f} vs {his[1]['A_3a']/his[1]['B_3a']:.3f}")
    check("so shared custody is WORSE than primary for child care the payor pays",
          down[1] < down[2])

    print("\n-- Both parents paying child care under Box 1 --")
    both = w.run(box=1, a_childcare=cc, b_childcare=cc, **kk)
    check("with both paying $300/wk the $430/child benchmark does NOT bind ($200 total)",
          abs(both["A_6a"] - 300) < 1e-9 and abs(both["B_6a"] - 300) < 1e-9)
    check("the payor's own $300/wk reduces the order by only ~$5.19/wk",
          abs((hers[1]["7d"] - both["7d"]) - 5.19) < 0.05,
          f"got ${hers[1]['7d']-both['7d']:.2f}")
    check("so the payor bears ~93% of combined child care across both households",
          abs(((both["7d"] - base[1]["7d"]) * 52 + 300 * 52) / (2 * 300 * 52) - 0.93) < 0.01,
          f"got {((both['7d']-base[1]['7d'])*52+300*52)/(2*300*52):.1%}")

    print("\n-- Box 3 (split) --")
    k = dict(a_gross=570.0, b_gross=201000 / 52.0, a_health=33.0, b_health=43.0)
    s21 = w.run(box=3, children_under18=3, a_children=(2, 0), b_children=(1, 0), **k)
    s12 = w.run(box=3, children_under18=3, a_children=(1, 0), b_children=(2, 0), **k)
    check("split 2/1 -> payor is still the higher earner", s21["payor"] == "B")
    check("the more children with the payor, the smaller the order", s12["7d"] < s21["7d"])
    check("Box 3 uses per-column Table B (2 children -> 1.40 in A's column)",
          abs(s21["A_4c"] / s21["3e"] - 1.40) < 1e-9, f"got {s21['A_4c']/s21['3e']:.4f}")
    check("Box 3 takes the Box 1 path at 7a (N/A, not the Box 2 branch)", s21["7a"] is None)
    for bad, why in [
        (dict(a_children=(2, 0), b_children=(2, 0)), "counts that do not sum"),
        (dict(a_children=(3, 0), b_children=(0, 0)), "a parent with no children"),
        (dict(), "missing child counts"),
    ]:
        try:
            w.run(box=3, children_under18=3, **bad, **k)
            check(f"Box 3 rejects {why}", False, "no error raised")
        except ValueError:
            check(f"Box 3 rejects {why}", True)
    check("box=4 is rejected",
          _raises(lambda: w.run(box=4, children_under18=1, **k), ValueError))

    print("\n-- Splitting siblings LOWERS the order despite raising total cost --")
    two_b1 = w.run(box=1, children_under18=2, **k)
    two_b3 = w.run(box=3, children_under18=2, a_children=(1, 0), b_children=(1, 0), **k)
    check("2 children: Box 3 one-each is ~30% below Box 1 shared",
          0.28 <= 1 - two_b3["7d"] / two_b1["7d"] <= 0.32,
          f"got {1 - two_b3['7d']/two_b1['7d']:.1%}")
    check("the driver is Table B: 2 x 1.00 split vs 1.40 shared",
          abs(w.TABLE_B[1] * 2 / w.TABLE_B[2] - 1.4286) < 1e-3)

    print("\n-- Per-line rounding (CJ-D 304: 'Round all numbers to the nearest whole dollar or percentage') --")
    rk = dict(a_gross=570.0, b_gross=201000 / 52.0, children_under18=3, a_health=33.0, b_health=43.0)
    ex0 = w.run(box=1, **rk)["7d"]; rd0 = w.run(box=1, round_lines=True, **rk)["7d"]
    check("rounded run returns whole dollars", rd0 == round(rd0))
    check("rounding moves the no-child-care order by ~+$3/wk (3c 87.68% -> 88%)",
          2.5 <= rd0 - ex0 <= 4.0, f"exact {ex0:.2f} rounded {rd0:.0f}")
    check("rounded 3c is exactly 88%", w.run(box=1, round_lines=True, **rk)["B_3c"] == 0.88)
    check("rounded order still validates against the disclosed order (~$1,013-1,016)",
          1008 <= rd0 <= 1020, f"got {rd0:.0f}")

    print("\n-- Structural --")
    check("$8,654 cap applied at 3d", w.run(box=1, a_gross=5000, b_gross=9000,
                                            children_under18=1)["3d"] == 8654)
    check("available income floors at $0",
          w.run(box=1, a_gross=10, b_gross=1000, children_under18=1,
                a_health=500)["A_3a"] == 0.0)

    # ---- 2026-09-05: pinned against the official CJ-D 304 XFA scripts (model/official_xfa_harness.js)
    print("\nOFFICIAL-SCRIPT PARITY (2026-09-05)")
    off = w.run(box=2, a_gross=12000.0, b_gross=12100.0, children_under18=3, round_lines=True)
    check("Box 2 near-equal incomes: 7b caps on the RECIPIENT's 6e, order is $986 as the form computes",
          off["7d"] == 986.0, f"got {off['7d']}")
    check("Box 2 near-equal incomes: order is not zeroed by using the payor's 6e", off["7d"] > 0)
    r1 = w.run(box=1, round_lines=True, **rk)
    check("round_lines does not round the (6d+10%) x 3a term (form leaves it fractional): B_6e = 75.18",
          abs(r1["B_6e"] - 75.18) < 0.005, f"got {r1['B_6e']}")
    check("round_lines Box 1 order still $1,016 as the form prints", r1["7d"] == 1016.0, f"got {r1['7d']}")
    cc_a = w.run(box=1, a_childcare=(150.0, 150.0), b_childcare=(0.0, 0.0, 300.0), **rk)
    cc_b = w.run(box=1, a_childcare=(150.0, 150.0, 0.0), b_childcare=(0.0, 0.0, 300.0), **rk)
    check("child-care tuples of unequal length are zero-padded, not truncated",
          abs(cc_a["7d"] - cc_b["7d"]) < 1e-9 and cc_a["B_6a"] > 0, f"{cc_a['7d']} vs {cc_b['7d']}, B_6a={cc_a['B_6a']}")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S): {FAILURES}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
