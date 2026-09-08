#!/usr/bin/env python3
"""Generate assets/js/fixtures/calculator-v2.json from this repo's own frozen model/.

This is the v2 grid PART 5 of assets/js/calculator.test.js checks against: children 1/2/3 x
custody box 1/2 x six fixed income pairs, health premiums fixed at $33/$43, no child care,
kids_under_13=0 (the generic-grid convention used across this site). 36 rows, none disabled.

2026-09-08: this generator did not previously exist in the repo (the test file's own header
comment says "see /tmp/gen_calc_v2_fixtures.py's own header for the exact command" -- an ephemeral
script from an earlier session, not committed). Recreated here so the fixture can be regenerated
from the model rather than hand-edited, and so it passes box=box to net_position.analyze() --
without that, every box=1 row here would be computed under the wrong custody assumption (the
2026-09-08 fix to net_position.py's analyze()/household_net_incomes(); see that file's own
docstring and model/test_net_position.py).

Correctness gate: assets/js/calculator.test.js PART 5 checks every row to the dollar (order_wk,
payor_after, recip_after, recip_per_person) and to 0.001 on the two ratios (line_7e, true_pct_net),
plus the two badge thresholds (true_pct_net > 40%, recip_after > payor_after). No number ships
without a script that produces it -- see model/submission_figures.py's own docstring for the same
rule.

Run: python3 tools/gen_calculator_v2_fixtures.py
"""
import json
import os
import sys

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "model")
sys.path.insert(0, MODEL_DIR)
import worksheet as w          # noqa: E402
import net_position as npos    # noqa: E402

INCOME_PAIRS = [
    (201000, 29640),
    (150000, 30000),
    (250000, 60000),
    (120000, 80000),
    (300000, 0),
    (90000, 45000),
]

HEALTH_LO, HEALTH_HI = 33.0, 43.0

rows = []
disabled = []


def add_row(kids, box, higher, lower):
    label = "kids=%d box=%d higher=%d lower=%d" % (kids, box, higher, lower)
    try:
        r = w.run(box=box, a_gross=lower / 52.0, b_gross=higher / 52.0, children_under18=kids,
                  a_health=HEALTH_LO, b_health=HEALTH_HI)
        payor_gross = higher if r["payor"] == "B" else lower
        recip_gross = lower if r["payor"] == "B" else higher

        # box=box (2026-09-08): who claims the children for tax purposes now follows the custody
        # box this row is computed under -- see net_position.household_net_incomes().
        pos = npos.analyze(payor_gross, recip_gross, kids, r["7d"], 0.0, 0.0, kids_under_13=0, box=box)

        row = {
            "kids": kids, "box": box,
            "higher": higher, "lower": lower,
            "payor": r["payor"],
            "order_wk": r["7d"],
            "line_7e": r["7e"],
            "true_pct_net": pos["support_pct_of_payor_net"],
            "payor_net": pos["payor_net"],
            "payor_after": pos["payor_after"],
            "recip_after": pos["recip_after"],
            "recip_per_person": pos["recip_per_person"],
        }
        rows.append(row)
        print(label, "->",
              "7d=%.6f" % row["order_wk"], "7e=%.9f" % row["line_7e"],
              "true_pct_net=%.9f" % row["true_pct_net"],
              "payor_after=%.4f" % row["payor_after"], "recip_after=%.4f" % row["recip_after"])
    except Exception as e:
        disabled.append({"kids": kids, "box": box, "higher": higher, "lower": lower, "error": str(e)})
        print(label, "-> DISABLED:", e)


for kids in (1, 2, 3):
    for box in (1, 2):
        for higher, lower in INCOME_PAIRS:
            add_row(kids, box, higher, lower)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                         "assets", "js", "fixtures", "calculator-v2.json")
out_path = os.path.normpath(out_path)
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump({
        "conventions": {
            "childcare": 0,
            "health_lo": HEALTH_LO,
            "health_hi": HEALTH_HI,
            "kids_under_13": 0,
        },
        "rows": rows,
        "disabled": disabled,
    }, f, indent=2)

print("\n%d rows, %d disabled. Wrote %s" % (len(rows), len(disabled), out_path))
