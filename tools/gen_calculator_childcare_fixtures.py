#!/usr/bin/env python3
"""Generate assets/js/fixtures/calculator-childcare.json from this repo's own frozen model/.

This is the correctness gate for the calculator's third control, child care (added 2026-09-07,
alongside the existing children/custody controls documented in CONVENTIONS.md SS11). Every
combination the child-care control can select must reproduce this script's Python output to the
dollar -- see assets/js/calculator.test.js PART 6, which loads the JSON this script writes and
checks every row. No number in the calculator ships without a script that produces it (the
project's standing rule -- see model/submission_figures.py's own docstring for the same
principle in the source model).

Grid: children 1/2/3 x custody box 1/2 x child-care scenario 0/1/2 x six income pairs
(the same six pairs as calculator-v2.json / tools/gen_calc_v2_fixtures.py's grid) = 108 rows.

Child-care scenarios (fixed at $300/wk total, not a slider -- see the header comment in
assets/js/calculator.js for why a discrete scenario choice was used instead of a fourth slider):
  0 = none            -- no child care claimed by either parent.
  1 = recipient pays  -- Parent A (the lower earner in this tool's convention) pays $300/wk to
                          the provider out of pocket; the other parent's Line 6b share of it is
                          reimbursed through the order, exactly as the worksheet already does.
  2 = both pay         -- each parent pays their own $300/wk during their own parenting time (the
                          ordinary case at equal parenting time; model/submission_figures.py
                          SS2.1's "both pay" scenario), for $600/wk combined.

Composition into net_position.analyze()'s weekly_childcare / payor_childcare_share: this script
reuses analyze() exactly as it already exists (no new function) --
  weekly_childcare       = the two parents' own out-of-pocket amounts, summed
  payor_childcare_share  = whichever parent the worksheet names payor, their own out-of-pocket
                            amount, divided by the combined total (0 if nobody pays)
This reduces to payor_childcare_share=0 in scenario 1 whenever the higher earner is payor (the
worksheet's usual case), and to exactly 0.5 in scenario 2 regardless of which parent is payor,
since both contribute the same $300/wk -- verified algebraically against
model/submission_figures.py SS2.1's manual arithmetic before this script was written.

Run: python3 tools/gen_calculator_childcare_fixtures.py
"""
import json
import os
import sys

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "model")
sys.path.insert(0, MODEL_DIR)
import worksheet as w          # noqa: E402
import net_position as npos    # noqa: E402

HEALTH_LO, HEALTH_HI = 33.0, 43.0
KIDS_UNDER_13 = 0          # same generic-grid convention as calculator-v2.json / _common.py
CHILDCARE_AMOUNT = 300.0   # fixed weekly amount per scenario -- see header comment

INCOME_PAIRS = [
    (201000, 29640),
    (150000, 30000),
    (250000, 60000),
    (120000, 80000),
    (300000, 0),
    (90000, 45000),
]

SCENARIOS = {
    0: "none",
    1: "recipient pays",
    2: "both pay",
}


def childcare_arrays(scenario):
    """(a_childcare, b_childcare) tuples for worksheet.run(), per SCENARIOS above."""
    if scenario == 1:
        return (CHILDCARE_AMOUNT,), ()
    if scenario == 2:
        return (CHILDCARE_AMOUNT,), (CHILDCARE_AMOUNT,)
    return (), ()


rows = []
disabled = []

for kids in (1, 2, 3):
    for box in (1, 2):
        for scenario in (0, 1, 2):
            a_cc, b_cc = childcare_arrays(scenario)
            for higher, lower in INCOME_PAIRS:
                label = ("kids=%d box=%d childcare=%d(%s) higher=%d lower=%d"
                         % (kids, box, scenario, SCENARIOS[scenario], higher, lower))
                try:
                    r = w.run(box=box, a_gross=lower / 52.0, b_gross=higher / 52.0,
                              children_under18=kids, a_health=HEALTH_LO, b_health=HEALTH_HI,
                              a_childcare=a_cc, b_childcare=b_cc)
                    payor_gross = higher if r["payor"] == "B" else lower
                    recip_gross = lower if r["payor"] == "B" else higher

                    a_own_cc = sum(a_cc)
                    b_own_cc = sum(b_cc)
                    weekly_childcare = a_own_cc + b_own_cc
                    payor_own_cc = a_own_cc if r["payor"] == "A" else b_own_cc
                    payor_childcare_share = (payor_own_cc / weekly_childcare) if weekly_childcare else 0.0

                    pos = npos.analyze(payor_gross, recip_gross, kids, r["7d"],
                                        weekly_childcare, payor_childcare_share,
                                        kids_under_13=KIDS_UNDER_13)
                    row = {
                        "kids": kids,
                        "box": box,
                        "childcare": scenario,
                        "higher": higher,
                        "lower": lower,
                        "payor": r["payor"],
                        "order_wk": r["7d"],
                        "line_7e": r["7e"],
                        # "true_pct_net" is burden_pct_of_payor_net, not support_pct_of_payor_net --
                        # it must include the payor's own out-of-pocket child care (scenario 2),
                        # which support_pct_of_payor_net never does. The two are identical whenever
                        # the payor pays nothing directly (scenarios 0 and 1 with Parent B as
                        # payor), so this is a strict generalisation, not a different figure.
                        "true_pct_net": pos["burden_pct_of_payor_net"],
                        "payor_net": pos["payor_net"],
                        "payor_after": pos["payor_after"],
                        "recip_after": pos["recip_after"],
                        "recip_per_person": pos["recip_after"] / (1 + kids),
                    }
                    rows.append(row)
                    print(label, "->",
                          "7d=%.6f" % row["order_wk"],
                          "7e=%.9f" % row["line_7e"],
                          "true_pct_net=%.9f" % row["true_pct_net"],
                          "payor_after=%.4f" % row["payor_after"],
                          "recip_after=%.4f" % row["recip_after"])
                except Exception as e:
                    disabled.append({"kids": kids, "box": box, "childcare": scenario,
                                      "higher": higher, "lower": lower, "error": str(e)})
                    print(label, "-> DISABLED:", e)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                         "assets", "js", "fixtures", "calculator-childcare.json")
out_path = os.path.normpath(out_path)
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump({
        "conventions": {
            "childcare_amount": CHILDCARE_AMOUNT,
            "scenarios": SCENARIOS,
            "health_lo": HEALTH_LO,
            "health_hi": HEALTH_HI,
            "kids_under_13": KIDS_UNDER_13,
        },
        "rows": rows,
        "disabled": disabled,
    }, f, indent=2)

print("\n%d rows, %d disabled. Wrote %s" % (len(rows), len(disabled), out_path))
