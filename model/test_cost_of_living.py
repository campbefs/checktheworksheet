"""Pins what the cost-of-living page says. If any check fails, the page's claim is wrong and must be
rewritten, not the test. Run: .venv/bin/python model/test_cost_of_living.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import cost_of_living as c  # noqa: E402

n = 0


def check(name, ok):
    global n
    if not ok:
        raise SystemExit(f"FAIL {name}")
    n += 1


f = c.facts()
ma, up = c.costlier()
check("Massachusetts cost of living is 105.8", round(f["ma_rpp"], 1) == 105.8)
check("six places cost more to live in", f["n_costlier"] == 6)
check("the six are CA, HI, DC, NJ, NY, WA",
      sorted(r["state"] for r in up) == sorted(["California", "Hawaii", "District of Columbia",
                                                "New Jersey", "New York", "Washington"]))
check("all six order less at equal time", f["n_costlier_below_ma_equal"] == 6)
check("five of six order less at primary custody", f["n_costlier_below_ma_primary"] == 5)
check("the one exception at primary custody is Hawaii", f["costlier_above_ma_primary"] == ["Hawaii"])
check("MA at equal time orders more than five of the six do at primary custody",
      f["n_costlier_primary_below_ma_equal"] == 5)
check("the highest costlier equal-time order is New York's, below MA",
      f["highest_costlier_equal"] == c.state("New York", "equal") < f["ma_equal"])
check("every row has a cost of living and both orders", all(r["rpp"] and r["equal"] and r["primary"] for r in c.rows()))
check("forty-nine or fifty jurisdictions joined (Georgia held out)", len(c.rows()) >= 49)
# The cost-of-living figures the page quotes, rounded as printed.
for st, v in [("California", 110.7), ("Hawaii", 110.0), ("District of Columbia", 109.9), ("New Jersey", 108.8),
              ("New York", 107.9), ("Washington", 107.0), ("Maryland", 105.0), ("New Hampshire", 104.2),
              ("Connecticut", 103.6)]:
    check(f"{st} cost of living is {v}", round(c.state(st, "rpp"), 1) == v)
print(f"All checks passed ({n}).")
