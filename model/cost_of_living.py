"""The cost-of-living defence, tested: does Massachusetts order more because it costs more to live here?

Added 2026-09-23 for the site's cost-of-living page, which answers the argument that
Massachusetts's amounts are justified by its cost of living: it compares Massachusetts with every
state whose cost of living is equal or higher, at primary custody and at joint custody.

Joins two published sources, no new arithmetic about support:
  * BEA Regional Price Parities, all items, 2024 (released February 19, 2026), a state's price
    level against the national average of 100: data/source/bea/SARPP_STATE_2008_2024.csv.
  * The fifty-jurisdiction comparison at the worked example ($201,000 / $29,640, three children,
    no child care), monthly orders: data/fifty-state/tier-50-2026-09-05.json. s1 = equal
    parenting time, s2 = the lower earner has primary custody. Georgia is held out there, so it
    is absent here.

Run it to print the table: .venv/bin/python model/cost_of_living.py
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RPP_CSV = os.path.join(ROOT, "data", "source", "bea", "SARPP_STATE_2008_2024.csv")
if not os.path.isfile(RPP_CSV):  # the published repo carries the same file at data/bea/
    RPP_CSV = os.path.join(ROOT, "data", "bea", "SARPP_STATE_2008_2024.csv")
TIER = os.path.join(ROOT, "data", "fifty-state", "tier-50-2026-09-05.json")
YEAR = "2024"


def rpp():
    """State -> 2024 all-items price parity (US = 100)."""
    out = {}
    with open(RPP_CSV, encoding="latin-1", newline="") as fh:
        for r in csv.DictReader(fh):
            if (r.get("LineCode") or "").strip() != "1":
                continue
            name = (r.get("GeoName") or "").strip().rstrip("*").strip()
            if not name or name == "United States":
                continue
            try:
                out[name] = float(r[YEAR])
            except (TypeError, ValueError):
                continue
    return out


def rows():
    """Every jurisdiction with both a price parity and an order, costliest first."""
    price = rpp()
    tier = json.load(open(TIER, encoding="utf-8"))
    joined = [dict(state=t["state"], rpp=price[t["state"]], equal=t["s1"], primary=t["s2"])
              for t in tier if t["state"] in price]
    return sorted(joined, key=lambda r: -r["rpp"])


def costlier():
    """Massachusetts, and every place whose price level is at or above it, costliest first."""
    rs = rows()
    ma = next(r for r in rs if r["state"] == "Massachusetts")
    return ma, [r for r in rs if r["rpp"] >= ma["rpp"] and r["state"] != "Massachusetts"]


def facts():
    ma, up = costlier()
    return {
        "ma_rpp": ma["rpp"],
        "ma_equal": ma["equal"],
        "ma_primary": ma["primary"],
        "n_costlier": len(up),
        "n_costlier_below_ma_equal": sum(r["equal"] < ma["equal"] for r in up),
        "n_costlier_below_ma_primary": sum(r["primary"] < ma["primary"] for r in up),
        # Massachusetts's EQUAL-TIME order against the costlier places' PRIMARY-custody orders.
        "n_costlier_primary_below_ma_equal": sum(r["primary"] < ma["equal"] for r in up),
        "costlier_above_ma_primary": [r["state"] for r in up if r["primary"] > ma["primary"]],
        "highest_costlier_equal": max(r["equal"] for r in up),
    }


def state(name, field):
    """One cell, for the figure registry: field in rpp / equal / primary."""
    return next(r for r in rows() if r["state"] == name)[field]


def main():
    ma, up = costlier()
    print(f"{'State':22} {'Price level':>11} {'Equal time':>11} {'Primary':>9}")
    for r in [ma] + up:
        print(f"{r['state']:22} {r['rpp']:11.1f} ${r['equal']:>9,.0f} ${r['primary']:>8,.0f}")
    for k, v in facts().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
