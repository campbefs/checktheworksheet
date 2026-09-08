#!/usr/bin/env python3
"""Tests for model/box1_fix.py.

    .venv/bin/python model/test_box1_fix.py

The first and most important group is the fidelity gate: variant "current" must
reproduce worksheet.run(box=1) to the cent across a grid, because every claim the
submission would make about the redlines is a comparison against that baseline. If
the baseline drifts, the comparison is meaningless.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box1_fix as bf  # noqa: E402
import worksheet as w  # noqa: E402

CHECKS = []


def check(name, cond):
    CHECKS.append((name, bool(cond)))


PAYOR = 201_000.0 / 52.0
GRID_RECIP = (2500.0, 1800.0, 1200.0, 900.0, 700.0, 570.0, 400.0, 250.0, 150.0, 0.0)


# --- 1. Fidelity: "current" IS the transcribed worksheet -----------------------
for a in GRID_RECIP:
    for kids in (1, 2, 3, 4):
        for cc in ((), (100.0, 100.0, 100.0, 100.0)[:kids]):
            ref = w.run(box=1, a_gross=a, b_gross=PAYOR, children_under18=kids,
                        a_health=33.0, b_health=43.0,
                        a_childcare=cc, b_childcare=(0.0,) * len(cc))
            got = bf.run("current", a_gross=a, b_gross=PAYOR, children_under18=kids,
                         a_health=33.0, b_health=43.0,
                         a_childcare=cc, b_childcare=(0.0,) * len(cc))
            check(f"current reproduces worksheet box=1 7d at A=${a:.0f}, {kids} kids, "
                  f"cc={bool(cc)}", abs(ref["7d"] - got["7d"]) < 0.005)
            check(f"current reproduces 6g at A=${a:.0f}, {kids} kids, cc={bool(cc)}",
                  abs(ref["6g"] - got["6g"]) < 0.005)

# --- 2. The credit IS the payor's own Line 6e ---------------------------------
for a in (2500.0, 1200.0, 570.0, 250.0):
    cur = bf.run("current", a_gross=a, b_gross=PAYOR, children_under18=3,
                 a_health=33.0, b_health=43.0)
    b2 = w.run(box=2, a_gross=a, b_gross=PAYOR, children_under18=3,
               a_health=33.0, b_health=43.0)
    payor_6e = cur["B_6e"] if cur["payor"] == "B" else cur["A_6e"]
    check(f"shared credit equals the payor's own 6e at A=${a:.0f}",
          abs((b2["7d"] - cur["7d"]) - payor_6e) < 0.01)

# --- 3. The D = 2.00 identity -------------------------------------------------
for a in (2500.0, 1200.0, 570.0):
    r = bf.run("A", a_gross=a, b_gross=PAYOR, children_under18=3,
               a_health=33.0, b_health=43.0)
    spread = r["4c"] * abs(r["B_3c"] - r["A_3c"])
    check(f"Box 1 without the 6e limitation is the D=2.0 cross-credit at A=${a:.0f}",
          abs(r["6g"] - 2.0 * 0.5 * spread) < 0.01)

# --- 4. Variant C at equal time is variant B ----------------------------------
for a in (2500.0, 1200.0, 570.0, 250.0):
    b = bf.run("B", a_gross=a, b_gross=PAYOR, children_under18=3,
               a_health=33.0, b_health=43.0)
    c = bf.run("C", a_gross=a, b_gross=PAYOR, children_under18=3,
               a_health=33.0, b_health=43.0, a_overnight_share=0.5)
    check(f"C at equal overnights equals B at A=${a:.0f}", abs(b["7d"] - c["7d"]) < 0.005)

# --- 5. C moves the right way with parenting time -----------------------------
prev = None
for payor_share in (1.0 / 3.0, 0.35, 0.40, 0.45, 0.50):
    r = bf.run("C", a_gross=570.0, b_gross=PAYOR, children_under18=3,
               a_health=33.0, b_health=43.0, a_overnight_share=1.0 - payor_share)
    if prev is not None:
        check(f"C order falls as payor overnights rise to {payor_share:.0%}", r["7d"] < prev)
    prev = r["7d"]

# --- 6. No redline is worse for the payor than the form as written ------------
for a in GRID_RECIP:
    cur = bf.run("current", a_gross=a, b_gross=PAYOR, children_under18=3,
                 a_health=33.0, b_health=43.0)
    va = bf.run("A", a_gross=a, b_gross=PAYOR, children_under18=3,
                a_health=33.0, b_health=43.0)
    vb = bf.run("B", a_gross=a, b_gross=PAYOR, children_under18=3,
                a_health=33.0, b_health=43.0)
    check(f"A never exceeds the current order at A=${a:.0f}", va["7d"] <= cur["7d"] + 0.005)
    check(f"B never exceeds A at A=${a:.0f}", vb["7d"] <= va["7d"] + 0.005)

# --- 7. The collapse, and that B does not collapse ----------------------------
# This is the whole argument, so it is pinned: the current credit falls away as the
# income gap widens, and the duplication-factor redline does not.
cur_credits, b_credits = [], []
for a in GRID_RECIP[:-1]:                      # exclude A=0, where Box 2 and Box 1 degenerate
    base = w.run(box=2, a_gross=a, b_gross=PAYOR, children_under18=3,
                 a_health=33.0, b_health=43.0)["7d"]
    cur_credits.append((base - bf.run("current", a_gross=a, b_gross=PAYOR,
                                      children_under18=3, a_health=33.0,
                                      b_health=43.0)["7d"]) / base)
    b_credits.append((base - bf.run("B", a_gross=a, b_gross=PAYOR, children_under18=3,
                                    a_health=33.0, b_health=43.0)["7d"]) / base)

check("current credit collapses below 5% at wide income disparity", min(cur_credits) < 0.05)
check("current credit is monotone decreasing in the payor's income share",
      all(x >= y - 1e-9 for x, y in zip(cur_credits, cur_credits[1:])))
check("B keeps at least a 25% credit everywhere on the grid", min(b_credits) >= 0.25)
check("B's credit range is far narrower than the current one",
      (max(b_credits) - min(b_credits)) < (max(cur_credits) - min(cur_credits)))

# --- 9. The implied-overnight inversion is exact, and knows its own scope -----
# Feeding an implied share back into variant C must reproduce the order it came
# from. If this fails, "priced as one-third time" is rhetoric, not a computation.
for a in (2500.0, 1200.0, 570.0, 400.0, 250.0):
    cur = bf.run("current", a_gross=a, b_gross=PAYOR, children_under18=3,
                 a_health=33.0, b_health=43.0)
    for d in (1.5, 2.0):
        p_share = bf.implied_overnight_share(cur, d)
        if cur["low_income_5c"]:
            check(f"metric refuses the shaded-area case at A=${a:.0f}, D={d}",
                  p_share is None)
            continue
        saved, bf.DUPLICATION = bf.DUPLICATION, d
        back = bf.run("C", a_gross=a, b_gross=PAYOR, children_under18=3,
                      a_health=33.0, b_health=43.0,
                      a_overnight_share=1.0 - p_share)
        bf.DUPLICATION = saved
        check(f"implied overnight share inverts at A=${a:.0f}, D={d}",
              abs(back["7d"] - cur["7d"]) < 0.01)

# Against Indiana's factor, equal parenting is never priced at the half actually
# held. Against Box 1's own implicit 2.0 it is priced at exactly half wherever the
# 6e limitation does not fire, and below half wherever it does -- so the limitation
# is the whole of the shortfall on that benchmark. Both are stated in the letter.
for a in (2500.0, 1800.0, 1200.0, 900.0, 700.0, 570.0):
    cur = bf.run("current", a_gross=a, b_gross=PAYOR, children_under18=3,
                 a_health=33.0, b_health=43.0)
    check(f"priced below half against Indiana's 1.5 at A=${a:.0f}",
          bf.implied_overnight_share(cur, 1.5) < 0.50)
    clip_fired = cur["B_6e"] < cur["B_6c"] - 0.005
    at_2 = bf.implied_overnight_share(cur, 2.0)
    check(f"against D=2.0, priced below half iff the 6e limit fired at A=${a:.0f}",
          (at_2 < 0.4999) == clip_fired)

# --- 10. Section 5's opening table is reproducible from THIS module ------------
# It was previously sourced only to model/submission_figures.py, so the letter's
# section 5 cited two scripts. These five rows are the ones printed in the letter.
EXPECTED = {"56.3": 0.776, "66.0": 0.515, "76.6": 0.205, "87.7": 0.069, "95.8": 0.013}
for a in bf.SECTION5_ORIGINAL_GRID:
    cur = bf.run("current", a_gross=a, b_gross=PAYOR, children_under18=3,
                 a_health=33.0, b_health=43.0)
    base = w.run(box=2, a_gross=a, b_gross=PAYOR, children_under18=3,
                 a_health=33.0, b_health=43.0)["7d"]
    key = f"{cur['B_3c'] * 100:.1f}"
    check(f"section 5 opening row {key}% is reproduced", key in EXPECTED)
    if key in EXPECTED:
        check(f"section 5 opening row {key}% reduction matches the letter",
              abs((base - cur["7d"]) / base - EXPECTED[key]) < 0.0005)

# --- 11. The redlines behave with child care present --------------------------
# 6c includes the child care allocation at 6b, and 6c is the line the first redline
# moves, so a fix that misbehaved once 6a is populated would be unsafe to propose.
prev_a_credit = None
for cc in (0.0, 150.0, 300.0, 600.0, 1290.0):
    per = cc / 3.0
    kw = dict(a_gross=570.0, b_gross=PAYOR, children_under18=3, a_health=33.0,
              b_health=43.0, a_childcare=(per, per, per), b_childcare=(0.0, 0.0, 0.0))
    base = w.run(box=2, **kw)["7d"]
    cur, va, vb = (bf.run(v, **kw) for v in ("current", "A", "B"))
    check(f"A never exceeds current at ${cc:.0f} child care", va["7d"] <= cur["7d"] + 0.005)
    check(f"B never exceeds A at ${cc:.0f} child care", vb["7d"] <= va["7d"] + 0.005)
    credit = (base - va["7d"]) / base
    if prev_a_credit is not None:
        check(f"the credit shrinks as child care rises, at ${cc:.0f}", credit < prev_a_credit)
    prev_a_credit = credit

# --- 12. No redline flips who pays -------------------------------------------
for a_wk, b_wk in ((3822.0, 570.0), (2000.0, 1200.0), (1200.0, 900.0), (900.0, 800.0),
                   (570.0, 3822.0), (800.0, 900.0)):
    kw = dict(a_gross=a_wk, b_gross=b_wk, children_under18=3, a_health=33.0, b_health=43.0)
    payors = {bf.run(v, **kw)["payor"] for v in bf.VARIANTS}
    check(f"payor identity is unchanged by variant at ${a_wk:.0f}/${b_wk:.0f}",
          len(payors) == 1)
    orders = [bf.run(v, **kw)["7d"] for v in ("current", "A", "B")]
    check(f"no redline raises the order at ${a_wk:.0f}/${b_wk:.0f}",
          orders[1] <= orders[0] + 0.005 and orders[2] <= orders[1] + 0.005)


# --- 8. Variant validation ----------------------------------------------------
try:
    bf.run("D", a_gross=570.0, b_gross=PAYOR, children_under18=3)
    check("unknown variant raises", False)
except ValueError:
    check("unknown variant raises", True)


if __name__ == "__main__":
    failed = [n for n, ok in CHECKS if not ok]
    for n in failed:
        print(f"FAIL: {n}")
    print(f"{len(CHECKS) - len(failed)}/{len(CHECKS)} checks passed")
    sys.exit(1 if failed else 0)
