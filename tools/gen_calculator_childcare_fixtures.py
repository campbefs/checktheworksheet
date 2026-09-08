#!/usr/bin/env python3
"""Generate assets/js/fixtures/calculator-childcare.json from this repo's own frozen model/.

2026-09-07 addition: two figures ported from model/childcare_post_transfer.py for the Child care
tab's new readout line and "apply the proposed fix" toggle --

  dist_share3c / dist_gross_share / dist_net_share  (Change 1, always-visible readout): the higher
  earner's Line 3c income share, and where that pair of incomes lands (gross, net) after the
  NO-CHILD-CARE order -- rule1_share / rule2_gross_share / rule3_share in childcare_post_transfer.py.
  Independent of cc_lower/cc_higher; identical across every row sharing the same
  kids/box/health/higher/lower, which is deliberate -- it lets calculator.test.js check the same
  four numbers on many rows rather than adding a separate fixture file.

  fixed_rule_share / fixed_rule_order_wk  (Change 2, "on income after the order", a fallback):
  childcare_post_transfer.py's rule2b -- run the worksheet with NO child care to get the base order
  and the payor Line 6f names in THAT pass, allocate the row's combined weekly child care
  (cc_lower + cc_higher) on that payor's post-transfer Line 3a share instead of Line 3c, add it to
  the base order.

2026-09-07 (afternoon) addition: net_rule_share / net_rule_order_wk / net_rule_charge_wk (Change 3,
"on money after tax", what this project recommends, per the owner: "it should be net, that's
absurd" that the higher-earning parent is charged most of the child care while holding less of the
household's money after the order once tax is counted) -- childcare_post_transfer.py's rule3/rule4.
Those two are algebraically identical (the annual_childcare terms cancel out of the fixed point),
so this is exactly dist_net_share applied to the row's combined child care, with the order left
unchanged at the no-child-care base -- see net_rule() below. This is also why dist_net_share itself
was changed to the kids_under_13=0 convention this same day: the recommended rule needs to agree
with itself at any input, not just the worked example.

Correctness gate for the calculator's premium inputs and Child care tab (rebuilt 2026-09-07:
premiums became two number inputs, default $40/$40, and child care became two continuous
sliders -- dollar amounts, not a 0/1/2 scenario radio). Every combination the interface can
reach (any income pair, any premiums, any child-care split) is computed live in the browser by
the SAME ported functions this script calls in Python, so this fixture is a spot-check gate, not
a lookup table: it proves the JS port matches the Python at a representative grid of inputs, and
assets/js/calculator.test.js checks every row to the dollar. No number ships without a script
that produces it -- see model/submission_figures.py's own docstring for the same rule.

CONVENTION (matches calculator.js's computeWithFacts()): Parent A = lower earner, Parent B =
higher earner, always -- regardless of which the worksheet ultimately names payor. cc_lower is
Parent A's own total weekly out-of-pocket child care; cc_higher is Parent B's. Each is spread
EVENLY across `kids` array elements before being passed to worksheet.run()'s aChildcare/
bChildcare (e.g. cc_lower=$100, kids=3 -> [33.33, 33.33, 33.33]) -- this matches the interface's
own composition (a slider's dollar value is a COMBINED total across all children, capped at
$430 x kids) and is arithmetically identical to an unspread single-element array whenever the
total is under the per-child $430 benchmark, which is true of every combination below.

"Higher earner's share of lower earner's child care" = worksheet Line A_6b (Parent B's income
share x Parent A's own benchmarked child care) -- literally the dollar amount the higher earner's
column contributes toward the lower earner's out-of-pocket cost, exactly as Line 6b already
computes it. "The higher earner bears $Y of $X combined" = the higher earner's own direct payment
(cc_higher, benchmarked) plus what they owe the lower earner via 6b, minus what the lower earner
owes them back via 6b -- the same decomposition documented in calculator.js's header comment for
the "both pay" case, generalised to any split.

Grid: children 1/2/3 x custody box 1/2 x premiums {(33,43), (40,40)} x child care
{(0,0), (300,0), (300,300)} x six income pairs = 216 rows, PLUS four hand-picked extra rows at
the worked-example incomes (kids=3, box=1): premiums (0,0) and (150,60) at no child care, and
premiums (40,40) at cc=(100,0) -- the exact combination item 4 of the interface brief asks the
Child care tab to default to.

Run: python3 tools/gen_calculator_childcare_fixtures.py
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

HEALTH_PAIRS = [(33.0, 43.0), (40.0, 40.0)]
CC_PAIRS = [(0.0, 0.0), (300.0, 0.0), (300.0, 300.0)]

WORKED_EXAMPLE = (201000, 29640)
EXTRA = [
    # (higher, lower, kids, box, health_lo, health_hi, cc_lower, cc_higher)
    (WORKED_EXAMPLE[0], WORKED_EXAMPLE[1], 3, 1, 0.0, 0.0, 0.0, 0.0),
    (WORKED_EXAMPLE[0], WORKED_EXAMPLE[1], 3, 1, 150.0, 60.0, 0.0, 0.0),
    (WORKED_EXAMPLE[0], WORKED_EXAMPLE[1], 3, 1, 40.0, 40.0, 100.0, 0.0),
]


def distribution(higher, lower, kids, box, health_lo, health_hi):
    """Change 1: childcare_post_transfer.py's rule1_share / rule2_gross_share / rule3_share, at
    the NO-CHILD-CARE order. Higher earner = Parent B always (see module CONVENTION above); every
    row this script has ever computed names B the payor, so this does not special-case a flip.

    dist_net_share uses kids_under_13=0 -- the SAME convention as every other figure this script
    emits (2026-09-07 afternoon: dropped the earlier min(2, kids) exception that matched the
    letter's worked example at 48.2%; the owner's recommended "on money after tax" rule needs this
    number to agree with itself at any input, not just the worked example, and net_position.py's
    own kids_under_13=0 output there is 48.4%, not 48.2%)."""
    r0 = w.run(box=box, a_gross=lower / 52.0, b_gross=higher / 52.0, children_under18=kids,
               a_health=health_lo, b_health=health_hi)
    base = r0["7d"]
    combined_gross = higher + lower
    gross_share = (higher - base * 52) / combined_gross if combined_gross else 0.0
    pos = npos.analyze(higher, lower, kids, base, 0.0, 0.0, kids_under_13=0)
    return {
        "dist_base_order_wk": base,
        "dist_share3c": r0["B_3c"],
        "dist_gross_share": gross_share,
        "dist_net_share": pos["payor_after_share"],
    }


def fixed_rule(higher, lower, kids, box, health_lo, health_hi, weekly_childcare):
    """Change 2: childcare_post_transfer.py's rule2b -- "on income after the order" (fallback)."""
    r0 = w.run(box=box, a_gross=lower / 52.0, b_gross=higher / 52.0, children_under18=kids,
               a_health=health_lo, b_health=health_hi)
    base = r0["7d"]
    payor_3a = r0["A_3a"] if r0["payor"] == "A" else r0["B_3a"]
    combined_3b = r0["3b"]
    share = (payor_3a - base) / combined_3b if combined_3b else 0.0
    return {
        "fixed_rule_share": share,
        "fixed_rule_order_wk": base + share * weekly_childcare,
    }


def net_rule(dist, weekly_childcare):
    """Change 3 (2026-09-07): "on money after tax" -- what this project recommends. The higher
    earner's share is childcare_post_transfer.py's rule3/rule4 (algebraically identical -- the
    annual_childcare terms cancel out of the fixed point, so it is exactly dist_net_share at the
    NO-CHILD-CARE order, no separate worksheet run needed). Unlike fixed_rule, this rule does NOT
    change the order: the higher earner pays their share of the combined child care directly."""
    return {
        "net_rule_share": dist["dist_net_share"],
        "net_rule_order_wk": dist["dist_base_order_wk"],
        "net_rule_charge_wk": dist["dist_net_share"] * weekly_childcare,
    }


def spread(total, kids):
    """A combined weekly dollar amount spread evenly across `kids` array elements, matching
    the interface's own composition (see header comment)."""
    if not total:
        return ()
    per = total / kids
    return tuple(per for _ in range(kids))


rows = []
disabled = []


def add_row(kids, box, health_lo, health_hi, cc_lower, cc_higher, higher, lower):
    a_cc = spread(cc_lower, kids)
    b_cc = spread(cc_higher, kids)
    label = ("kids=%d box=%d health=%g/%g cc=%g/%g higher=%d lower=%d"
             % (kids, box, health_lo, health_hi, cc_lower, cc_higher, higher, lower))
    try:
        r = w.run(box=box, a_gross=lower / 52.0, b_gross=higher / 52.0,
                  children_under18=kids, a_health=health_lo, b_health=health_hi,
                  a_childcare=a_cc, b_childcare=b_cc)
        payor_gross = higher if r["payor"] == "B" else lower
        recip_gross = lower if r["payor"] == "B" else higher

        a_own_cc = sum(a_cc)
        b_own_cc = sum(b_cc)
        weekly_childcare = a_own_cc + b_own_cc
        payor_own_cc = a_own_cc if r["payor"] == "A" else b_own_cc
        payor_childcare_share = (payor_own_cc / weekly_childcare) if weekly_childcare else 0.0

        pos = npos.analyze(payor_gross, recip_gross, kids, r["7d"],
                            weekly_childcare, payor_childcare_share, kids_under_13=0)

        # Higher (B) earner's dollar/percentage share of the lower (A) earner's own child care --
        # Line A_6b, as documented in the header comment above.
        higher_share_of_lower_wk = r["A_6b"]
        higher_share_of_lower_pct = (r["A_6b"] / r["A_6a"]) if r["A_6a"] else 0.0

        # What the higher earner bears of the COMBINED child-care cost: their own direct payment,
        # plus what they owe the lower earner (A_6b), minus what the lower earner owes them back
        # (B_6b).
        higher_bears_wk = b_own_cc - r["B_6b"] + r["A_6b"]
        higher_bears_pct = (higher_bears_wk / weekly_childcare) if weekly_childcare else 0.0

        dist = distribution(higher, lower, kids, box, health_lo, health_hi)
        fixed = fixed_rule(higher, lower, kids, box, health_lo, health_hi, weekly_childcare)
        net = net_rule(dist, weekly_childcare)

        row = {
            "kids": kids, "box": box,
            "health_lo": health_lo, "health_hi": health_hi,
            "cc_lower": cc_lower, "cc_higher": cc_higher,
            "higher": higher, "lower": lower,
            "payor": r["payor"],
            "order_wk": r["7d"],
            "line_7e": r["7e"],
            "true_pct_net": pos["burden_pct_of_payor_net"],
            "payor_net": pos["payor_net"],
            "payor_after": pos["payor_after"],
            "recip_after": pos["recip_after"],
            "recip_per_person": pos["recip_after"] / (1 + kids),
            "higher_share_of_lower_wk": higher_share_of_lower_wk,
            "higher_share_of_lower_pct": higher_share_of_lower_pct,
            "higher_bears_wk": higher_bears_wk,
            "higher_bears_pct": higher_bears_pct,
            "combined_wk": weekly_childcare,
            "dist_share3c": dist["dist_share3c"],
            "dist_gross_share": dist["dist_gross_share"],
            "dist_net_share": dist["dist_net_share"],
            "fixed_rule_share": fixed["fixed_rule_share"],
            "fixed_rule_order_wk": fixed["fixed_rule_order_wk"],
            "net_rule_share": net["net_rule_share"],
            "net_rule_order_wk": net["net_rule_order_wk"],
            "net_rule_charge_wk": net["net_rule_charge_wk"],
        }
        rows.append(row)
        print(label, "->",
              "7d=%.6f" % row["order_wk"],
              "7e=%.9f" % row["line_7e"],
              "true_pct_net=%.9f" % row["true_pct_net"],
              "payor_after=%.4f" % row["payor_after"],
              "recip_after=%.4f" % row["recip_after"],
              "dist=%.6f/%.6f/%.6f" % (row["dist_share3c"], row["dist_gross_share"], row["dist_net_share"]),
              "fixed_rule_7d=%.6f" % row["fixed_rule_order_wk"],
              "net_rule_share=%.6f" % row["net_rule_share"])
    except Exception as e:
        disabled.append({"kids": kids, "box": box, "health_lo": health_lo, "health_hi": health_hi,
                          "cc_lower": cc_lower, "cc_higher": cc_higher,
                          "higher": higher, "lower": lower, "error": str(e)})
        print(label, "-> DISABLED:", e)


for kids in (1, 2, 3):
    for box in (1, 2):
        for health_lo, health_hi in HEALTH_PAIRS:
            for cc_lower, cc_higher in CC_PAIRS:
                for higher, lower in INCOME_PAIRS:
                    add_row(kids, box, health_lo, health_hi, cc_lower, cc_higher, higher, lower)

for higher, lower, kids, box, health_lo, health_hi, cc_lower, cc_higher in EXTRA:
    add_row(kids, box, health_lo, health_hi, cc_lower, cc_higher, higher, lower)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                         "assets", "js", "fixtures", "calculator-childcare.json")
out_path = os.path.normpath(out_path)
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump({
        "conventions": {
            "health_pairs": HEALTH_PAIRS,
            "cc_pairs": CC_PAIRS,
            "note": "cc_lower/cc_higher are COMBINED weekly totals, spread evenly across `kids` "
                    "array elements before being passed to worksheet.run() -- see spread() above. "
                    "dist_share3c/dist_gross_share/dist_net_share (Change 1) are independent of "
                    "cc_lower/cc_higher -- see distribution() above; dist_net_share uses "
                    "kids_under_13=0, the same convention as every other figure here. "
                    "fixed_rule_share/fixed_rule_order_wk (Change 2, 'on income after the order', "
                    "a fallback) are childcare_post_transfer.py's rule2b -- see fixed_rule() above. "
                    "net_rule_share/net_rule_order_wk/net_rule_charge_wk (Change 3, 'on money after "
                    "tax', what this project recommends) are childcare_post_transfer.py's rule3/4 -- "
                    "see net_rule() above; net_rule_order_wk always equals dist_base_order_wk "
                    "because this rule does not change the order, only who pays the child care.",
        },
        "rows": rows,
        "disabled": disabled,
    }, f, indent=2)

print("\n%d rows, %d disabled. Wrote %s" % (len(rows), len(disabled), out_path))
