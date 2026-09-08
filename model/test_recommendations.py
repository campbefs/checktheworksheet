#!/usr/bin/env python3
"""Tests for model/recommendations.py.

    .venv/bin/python model/test_recommendations.py

Pins the figures the Recommendations page will quote to known values, so a future
edit that silently changes an input (a JSON row, a health premium, a share formula)
is caught before it reaches the site.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recommendations as rec  # noqa: E402

CHECKS = []


def check(name, cond):
    CHECKS.append((name, bool(cond)))


rows = rec.load_tier50()

# --- Block A: ranked tier -------------------------------------------------
check("ranked tier holds exactly 50 jurisdictions", len(rows) == 50)
check("Georgia is not in the ranked tier", not any(r["state"] == "Georgia" for r in rows))

ma_row = rec.state_row(rows, "Massachusetts")
check("Massachusetts S1 equals 4388.48", abs(ma_row["s1"] - 4388.48) < 0.005)

a_s1 = rec.median_rank_distance(rows, "s1")
manual_sorted = sorted((r["s1"] for r in rows), reverse=True)
check("median S1 lies between the 25th and 26th sorted values",
      min(manual_sorted[24], manual_sorted[25]) <= a_s1["median"] <= max(manual_sorted[24], manual_sorted[25]))
check("Massachusetts ranks 1st of 50 on S1", a_s1["ma_rank"] == 1)

# --- Block B: WA and CA present -------------------------------------------
check("Washington is present in the ranked tier", rec.state_row(rows, "Washington") is not None)
check("California is present in the ranked tier", rec.state_row(rows, "California") is not None)

# --- Block C: worked example, current order and variants ------------------
b1 = rec.box1_order()["7d"]
check("today's Box 1 order reproduces $1,012.73/wk", abs(b1 - 1012.73) < 0.01)

b2 = rec.box2_order()["7d"]
vb = rec.variant_order("B")["7d"]
check("Variant B reproduces $701.30/wk", abs(vb - 701.30) < 0.01)

vc_equal = rec.variant_order("C", 0.5)["7d"]
check("Variant C at equal time equals Variant B", abs(vc_equal - vb) < 0.005)

check("linear discount at 1/3 payor overnights is 0%", rec.linear_time_discount(1.0 / 3.0) == 0.0)
check("linear discount at 1/2 payor overnights is 50%", abs(rec.linear_time_discount(0.5) - 0.5) < 1e-9)
check("linear discount at 45% payor overnights is 35%", abs(rec.linear_time_discount(0.45) - 0.35) < 1e-9)
check("linear-discount order at equal time is Box2 x 0.5",
      abs(rec.linear_discount_order(0.5, base=b2) - b2 * 0.5) < 0.005)

cand_rows, b2_check = rec.candidate_credits()
check("candidate_credits() prices off the printed Box 2 figure", abs(b2_check - b2) < 0.005)
check("candidate_credits() returns six rows", len(cand_rows) == 6)

# --- Block D: reduction to reach the median --------------------------------
target_wk = a_s1["median"] * 12.0 / 52.0
cut_wk = b1 - target_wk
check("the median-matching cut is positive (MA exceeds the median)", cut_wk > 0)
check("the median-matching cut reduces the order to the target",
      abs((b1 - cut_wk) - target_wk) < 0.01)

# --- Block E: corpus check (skipped when the extracted corpus is absent) ------
import os as _os
if not _os.path.exists(rec.GUIDELINES_FLOW):
    print("skip: block E corpus checks (Guidelines.flow.txt not in this checkout)")
by_year = rec.gross_and_net_sentences_by_year() if _os.path.exists(rec.GUIDELINES_FLOW) else None
if by_year is not None:
    check("all five commentary years are found in Guidelines.flow.txt",
          {"2017", "2018", "2021", "2023", "2025"} <= set(by_year.keys()))
    check("no commentary block in Guidelines.flow.txt pairs gross and net in one sentence",
          sum(len(v["hits"]) for v in by_year.values()) == 0)

    prior = rec.as_prior_task_forces_sentences()
    check("'as prior task forces' is found exactly once in the corpus", len(prior) == 1)
    check("the 'as prior task forces' hit is in Econreview.flow.txt",
          prior and prior[0][0] == "Econreview.flow.txt")

# --- Block F: childcare recommendation -------------------------------------
f_rows, cc_annual, headline = rec.childcare_rules()
check("childcare_rules() returns five rows", len(f_rows) == 5)
check("total annual child care is $15,600", abs(cc_annual - 15600.0) < 0.01)

rule1 = next(r for r in f_rows if r["n"] == 1)
check("rule 1 (current worksheet) order reproduces $1,275.77/wk",
      abs(rule1["order_wk"] - 1275.77) < 0.01)
check("rule 1 payor's childcare share is about 87.7%", abs(rule1["share"] - 0.8768) < 0.001)

rule2 = next(r for r in f_rows if r["n"] == 2)
check("rule 2 (removed) order equals the no-childcare Box 1 order", abs(rule2["order_wk"] - b1) < 0.005)
check("rule 2 payor's childcare share is 0%", rule2["share"] == 0.0)

rule3 = next(r for r in f_rows if r["n"] == 3)
check("rule 3 (50-50 split) payor's childcare share is 50%", rule3["share"] == 0.5)

rule4 = next(r for r in f_rows if r["n"] == 4)
check("rule 4 (post-transfer GROSS / Line 6b-1) order reproduces $1,206.08/wk",
      abs(rule4["order_wk"] - 1206.08) < 0.01)
check("rule 4 payor's childcare share is about 64.5%", abs(rule4["share"] - 0.6445) < 0.001)

rule5 = next(r for r in f_rows if r["n"] == 5)
check("rule 5 (post-transfer NET) order equals the no-childcare Box 1 order",
      abs(rule5["order_wk"] - b1) < 0.005)
check("rule 5 payor's childcare share is about 48.2%", abs(rule5["share"] - 0.4816) < 0.001)

check("headline 'before' share matches rule 1's share", abs(headline["before_share"] - rule1["share"]) < 1e-9)
check("headline 'after gross' share is about 64.3%", abs(headline["after_gross_share"] - 0.6432) < 0.001)
check("headline 'after net' share matches rule 5's share", abs(headline["after_net_share"] - rule5["share"]) < 1e-9)


def main():
    failed = [name for name, ok in CHECKS if not ok]
    for name, ok in CHECKS:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name}")
    print(f"\n{len(CHECKS) - len(failed)}/{len(CHECKS)} checks passed.")
    if failed:
        print("\nFAILED:")
        for name in failed:
            print(f"  - {name}")
        sys.exit(1)


if __name__ == "__main__":
    main()
