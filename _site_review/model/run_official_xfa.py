#!/usr/bin/env python3
"""Run CJ-D 304's OWN embedded XFA calculation scripts (via model/official_xfa_harness.js)
against model/worksheet.py, on six fact patterns built from the worked example's parameters,
and print a line-by-line comparison.

This is a cross-check of the model against the Commonwealth's own form logic, not a
re-derivation of it -- model/worksheet.py is not touched here.

    .venv/bin/python model/run_official_xfa.py
    (or python3, no third-party deps needed for this script; node must be on PATH)
"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
XFA_XML = os.path.join(REPO, "data", "extracted", "cjd304-xfa.xml")
HARNESS = os.path.join(HERE, "official_xfa_harness.js")

sys.path.insert(0, HERE)
import worksheet as w  # noqa: E402

A_GROSS = 570.0
B_GROSS = 3865.38
A_HEALTH = 33.0
B_HEALTH = 43.0
CHILDREN_UNDER18 = 3
CHILDREN_18PLUS = 0


def cc_tuple(total):
    """Split a combined weekly child-care figure evenly across the three children,
    matching the convention model/submission_figures.py already uses ((100,100,100)
    for $300/wk) -- the benchmarking in both the model and the real form is invariant
    to how a sub-$430-per-child total is split among children, so this is just for
    like-for-like comparability, not a substantive choice.

    Always returns a CHILDREN_UNDER18-length tuple, including all-zero. worksheet.py's
    `run()` does `zip(a_childcare, b_childcare)` to pair up each child's two amounts;
    zip() silently truncates to the SHORTER of the two iterables, so pairing a real
    tuple with the empty-tuple default silently drops every element and zeroes out
    the child care that WAS entered. That is a bug in this driver script's own
    input-building, not in worksheet.py -- caught by cross-checking against the XFA
    harness on case 3, where the two disagreed by $264/wk before this fix."""
    per = (total / CHILDREN_UNDER18) if total else 0.0
    return tuple([per] * CHILDREN_UNDER18)


def xfa_inputs(box, a_cc_total=0.0, b_cc_total=0.0):
    """Build the CJ-D 304 XFA input dict for one of the six fact patterns."""
    if box == 1:
        d_pA, e_pA, d_pB, e_pB = CHILDREN_UNDER18, CHILDREN_18PLUS, CHILDREN_UNDER18, CHILDREN_18PLUS
    elif box == 2:
        d_pA, e_pA, d_pB, e_pB = CHILDREN_UNDER18, CHILDREN_18PLUS, 0, 0
    else:
        raise ValueError("only Box 1 / Box 2 are used in these six cases")

    a_cc = cc_tuple(a_cc_total)
    b_cc = cc_tuple(b_cc_total)

    inputs = {
        "Value_1a": CHILDREN_UNDER18 + CHILDREN_18PLUS,
        "RadioButtonList": str(box),
        "Value_1c_pA": "Parent A",
        "Value_1c_pB": "Parent B",
        "Value_1d_pA": d_pA, "Value_1e_pA": e_pA,
        "Value_1d_pB": d_pB, "Value_1e_pB": e_pB,
        "Value_2a_pA": A_GROSS, "Value_2a_pB": B_GROSS,
        "SS_benefit": "No",
        "Value_2d_pA": 0, "Value_2d_pB": 0,          # other support obligations
        "Value_2e_pA": A_HEALTH, "Value_2e_pB": B_HEALTH,  # health premium
        "Value_2f_pA": 0, "Value_2f_pB": 0,          # dental/vision
    }
    for i in range(1, 6):
        inputs[f"Value_2g_pA_c{i}"] = a_cc[i - 1] if i <= len(a_cc) else 0
        inputs[f"Value_2g_pB_c{i}"] = b_cc[i - 1] if i <= len(b_cc) else 0
    return inputs


def run_xfa(inputs):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(inputs, f)
        path = f.name
    try:
        out = subprocess.run(
            ["node", HARNESS, XFA_XML, path],
            capture_output=True, text=True, check=True,
        )
    finally:
        os.unlink(path)
    if out.stderr.strip():
        print("  [node stderr]", out.stderr.strip(), file=sys.stderr)
    return json.loads(out.stdout)


def run_model(box, a_cc_total, b_cc_total, round_lines):
    a_cc = cc_tuple(a_cc_total)
    b_cc = cc_tuple(b_cc_total)
    return w.run(
        box=box, a_gross=A_GROSS, b_gross=B_GROSS,
        children_under18=CHILDREN_UNDER18, children_18plus=CHILDREN_18PLUS,
        a_health=A_HEALTH, b_health=B_HEALTH,
        a_childcare=a_cc, b_childcare=b_cc,
        round_lines=round_lines,
    )


CASES = [
    ("1. Box 1 (shared), no child care",                    1, 0.0,   0.0),
    ("2. Box 2 (Parent A primary), no child care",          2, 0.0,   0.0),
    ("3. Box 2, Parent A pays $300/wk child care",          2, 300.0, 0.0),
    ("4. Box 1, Parent A pays $300/wk child care",          1, 300.0, 0.0),
    ("5. Box 1, each parent pays $300/wk child care",       1, 300.0, 300.0),
    ("6. Box 1, Parent B (payor) pays $300/wk child care",  1, 0.0,   300.0),
]


def fmt(x, nd=2):
    if x is None:
        return "n/a"
    if isinstance(x, str):
        return x
    return f"{x:,.{nd}f}"


def official_payor(xfa):
    """Which parent the official worksheet's own 6f fields name as Payor."""
    if xfa.get("Value_6f_pA") == "Payor":
        return "A"
    if xfa.get("Value_6f_pB") == "Payor":
        return "B"
    return "?"


def main():
    print("=" * 100)
    print("CJ-D 304 official XFA calculate-scripts vs model/worksheet.py")
    print(f"Fixed pattern: {CHILDREN_UNDER18} children under 18, Parent A gross ${A_GROSS}/wk, "
          f"Parent B gross ${B_GROSS}/wk, health premiums ${A_HEALTH}/${B_HEALTH}")
    print("=" * 100)

    any_logic_diff = False

    for label, box, a_cc, b_cc in CASES:
        print()
        print("-" * 100)
        print(label)
        print("-" * 100)

        xfa = run_xfa(xfa_inputs(box, a_cc, b_cc))
        meta = xfa.get("__meta__", {})
        if meta.get("warnings"):
            print("  ! node warnings:", meta["warnings"])
        if not meta.get("converged"):
            print(f"  ! did NOT converge in {meta.get('passes')} passes")

        m_round = run_model(box, a_cc, b_cc, round_lines=True)
        m_unround = run_model(box, a_cc, b_cc, round_lines=False)

        off_payor = official_payor(xfa)
        model_payor = m_round["payor"]

        off_7d = xfa.get("Value_7d")
        off_7e = xfa.get("Value_7e")
        off_3c_pA = xfa.get("Value_3c_pA")
        off_3c_pB = xfa.get("Value_3c_pB")
        off_6e_pA = xfa.get("Value_6e_pA")
        off_6e_pB = xfa.get("Value_6e_pB")
        off_6g = xfa.get("Value_6g")

        rows = [
            ("payor (per 6f / model)", off_payor, model_payor, model_payor),
            ("final weekly order (7d)", fmt(off_7d, 0), fmt(m_round["7d"]), fmt(m_unround["7d"])),
            ("7e (% of payor's 3a)", fmt(off_7e), fmt(m_round["7e"]), fmt(m_unround["7e"])),
            ("3c Parent A (income share)", fmt(off_3c_pA), fmt(m_round["A_3c"]), fmt(m_unround["A_3c"])),
            ("3c Parent B (income share)", fmt(off_3c_pB), fmt(m_round["B_3c"]), fmt(m_unround["B_3c"])),
            ("6e Parent A", fmt(off_6e_pA), fmt(m_round["A_6e"]), fmt(m_unround["A_6e"])),
            ("6e Parent B", fmt(off_6e_pB), fmt(m_round["B_6e"]), fmt(m_unround["B_6e"])),
            ("6g (netted obligation)", fmt(off_6g), fmt(m_round["6g"]), fmt(m_unround["6g"])),
        ]

        print(f"  {'line':32s} {'OFFICIAL XFA':>14s} {'MODEL round':>14s} {'MODEL unround':>14s}")
        for name, off, mr, mu in rows:
            flag = ""
            try:
                if off not in ("n/a", "?") and abs(float(off) - float(mr)) > 0.5:
                    flag = "  <-- differs by >$0.50 / >0.5pp from rounded model"
            except (TypeError, ValueError):
                pass
            print(f"  {name:32s} {off!s:>14s} {mr!s:>14s} {mu!s:>14s}{flag}")

        # Sanity check on case 1 only, never forced.
        if label.startswith("1."):
            print()
            print(f"  Sanity check (case 1): official 7d = {off_7d} "
                  f"(project expectation: 1016), model unrounded 7d = {m_unround['7d']:.2f} "
                  f"(project expectation: 1012.73)")

    print()
    print("=" * 100)


if __name__ == "__main__":
    main()
