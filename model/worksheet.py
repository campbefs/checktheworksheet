#!/usr/bin/env python3
"""Faithful implementation of CJ-D 304, the 2025 Child Support Guidelines Worksheet.

This is no longer inferred. The line-by-line logic below is transcribed from the
worksheet itself (CJD 304, 12/01/2025), obtained 2026-09-02.

TABLE A is printed on page 4 of the worksheet and is implemented here directly. It was
independently cross-checked against every one of the 1,104 rows published in the
Guidelines Chart, with no disagreement greater than $1. (An earlier docstring said
'1,194 points'; no code ever produced that number. The chart has 1,104 rows.)

WHAT IS IMPLEMENTED
  2a  gross weekly income      2e/2f  insurance deductions     2g  child care paid
  3a  available income = 2a + 2c - 2d - 2e - 2f, floor 0
  3b  combined        3c  share       3d  applicable (cap $8,654)
  3e  Table A         3f  Table B     3g  combined support amount
  4   Table C age adjustment
  5a/5b  proportional shares       5c  low-income payor adjustment
  6a  child care benchmark ($430/child cap, pro-rated)
  6b  other parent's share of benchmark cost
  6c  = 5c + 6b        6d  support as % of available income
  6e  income-disparity adjustment    6f  payor/recipient    6g  netted obligation
  7a/7b  recipient-side disparity adjustment
  7d  final obligation    7e  the 40% substantial-hardship test

  1b  Box 1 (shared) / Box 2 (primary ~2/3) / Box 3 (split) -- all three implemented

NOT implemented: Social Security dependency benefits (2b/2c/7c), and section 8
(additional income above $8,654). Both are $0 in the cases modelled here.
"""

TABLE_B = {0: 0.00, 1: 1.00, 2: 1.40, 3: 1.68, 4: 1.85, 5: 1.94}

# Table C: adjustment percentage, keyed (children under 18, children 18+)
TABLE_C = {
    (0, 1): .25, (0, 2): .25, (0, 3): .25, (0, 4): .25, (0, 5): .25,
    (1, 1): .07, (1, 2): .11, (1, 3): .13, (1, 4): .14,
    (2, 1): .04, (2, 2): .06, (2, 3): .07,
    (3, 1): .02, (3, 2): .03,
    (4, 1): .01,
}

CAP = 8654          # 3d
CC_BENCHMARK = 430  # 6a, per child per week
LOW_INCOME = 391    # 5c / 6e shaded-area threshold


def table_a(x):
    """Table A as printed on CJ-D 304 page 4. Weekly, one child under 18."""
    if x < 0:
        return 0.0
    if x <= 301:      # CJ-D 304 places $0 inside this bracket: the minimum order is $15
        return 15.0
    if x <= 391:
        return 15 + 0.20 * (x - 301)
    if x <= 1000:
        return 0.22 * x
    if x <= 1600:
        return 220 + 0.21 * (x - 1000)
    if x <= 2400:
        return 346 + 0.18 * (x - 1600)
    if x <= 3500:
        return 490 + 0.14 * (x - 2400)
    if x <= 5000:
        return 644 + 0.11 * (x - 3500)
    return 809 + 0.10 * (x - 5000)


def _floor(value, other_3a):
    """The "but not less than an amount from the shaded area of the Guidelines Chart"
    floor on Lines 6e and 7b. The shaded area of the Chart is the band at or below
    $391 of available income, so the floor only bites there."""
    return max(value, table_a(other_3a)) if other_3a <= LOW_INCOME else value


def _cc_benchmarked(per_child_paid):
    """6a. Per child: if the TOTAL both parents paid for that child exceeds $430,
    scale this parent's share down proportionally. Returns this parent's total."""
    out = 0.0
    for a, b in per_child_paid:      # (this parent paid, other parent paid)
        total = a + b
        out += a if total <= CC_BENCHMARK else a * (CC_BENCHMARK / total)
    return out


def run(box, a_gross, b_gross, children_under18, children_18plus=0,
        a_health=0.0, b_health=0.0, a_dental=0.0, b_dental=0.0,
        a_other_support=0.0, b_other_support=0.0,
        a_childcare=(), b_childcare=(),
        a_children=None, b_children=None, round_lines=False):
    """Parent A / Parent B per the worksheet's own convention.

    For Box 2, Parent A is the parent the children primarily reside with.

    For Box 3 (split), pass `a_children` and `b_children` as (under 18, 18 or over)
    tuples giving the children who primarily reside with each parent. They must sum
    to `children_under18` / `children_18plus`, and each parent must have at least one
    child -- that is what makes the arrangement a split rather than a Box 2.
    """
    n = children_under18 + children_18plus

    # CJ-D 304 page 1: "Round all numbers to the nearest whole dollar or percentage."
    # By default this model carries cents so the arithmetic is traceable; pass
    # round_lines=True to round each line as the form does. On the worked example
    # the difference is +$3-4/wk (Line 3c 87.68% -> 88%). Raised by the fifty-state
    # attack stage 2026-09-03.
    R = (lambda x: float(round(x))) if round_lines else (lambda x: x)
    P = (lambda x: round(x, 2)) if round_lines else (lambda x: x)

    # --- 3a available income
    a3a = R(max(0.0, a_gross - a_other_support - a_health - a_dental))
    b3a = R(max(0.0, b_gross - b_other_support - b_health - b_dental))
    b3b = a3a + b3a
    a3c = P(a3a / b3b) if b3b else 0.0
    b3c = P(b3a / b3b) if b3b else 0.0
    d3d = min(b3b, CAP)
    e3e = R(table_a(d3d))

    # --- 1d/1e: child counts per column depend on the box.
    # This is the ONLY thing the box selection changes. Every later line on CJ-D 304
    # that names a box says "Box 1 or Box 3" and treats them identically (5c, 6d, 6e,
    # 6f, 6g, 7a), so split follows the shared path from here on.
    if box == 1:            # shared: both columns carry all children
        a_cnt = b_cnt = (children_under18, children_18plus)
    elif box == 2:          # primary: all children in Parent A's column
        a_cnt, b_cnt = (children_under18, children_18plus), (0, 0)
    elif box == 3:          # split: each column carries the children residing there
        if a_children is None or b_children is None:
            raise ValueError("Box 3 requires a_children and b_children as "
                             "(under 18, 18 or over) tuples")
        a_cnt, b_cnt = tuple(a_children), tuple(b_children)
        if (a_cnt[0] + b_cnt[0], a_cnt[1] + b_cnt[1]) != (children_under18, children_18plus):
            raise ValueError(f"Box 3 child counts {a_cnt} + {b_cnt} do not sum to "
                             f"({children_under18}, {children_18plus})")
        if sum(a_cnt) == 0 or sum(b_cnt) == 0:
            raise ValueError("Box 3 requires each parent to have at least one child "
                             "primarily residing with them; otherwise use Box 2")
    else:
        raise ValueError(f"box must be 1, 2 or 3, got {box!r}")

    def col(cnt):
        """Lines 3f, 3g, 4a, 4b, 4c for one column.

        Table C is keyed on the children in THAT column's 1d/1e -- the worksheet says
        'the adjustment percentage for the ages of the children listed in 1d and 1e'
        and prints a separate multiplier box per parent. Under Box 1 both columns hold
        every child so this is the same as keying it globally; under Box 3 it is not."""
        n_u18, n_18p = cnt
        n_col = n_u18 + n_18p
        f3f = TABLE_B[min(n_col, 5)]
        g3g = R(e3e * f3f)
        pct = TABLE_C.get((n_u18, n_18p), 0.0) if n_col else 0.0
        b4b = R(g3g * pct)
        c4c = g3g - b4b
        return g3g, c4c

    _, a4c = col(a_cnt)
    _, b4c = col(b_cnt)

    # --- 5a / 5b. Each column's 5b is what the OTHER parent owes this parent.
    a5a, b5a = R(a3c * a4c), R(b3c * b4c)
    a5b, b5b = a4c - a5a, b4c - b5a
    # --- 5c low-income payor adjustment (shaded area applies only at 3a <= $391)
    # 5c is a strict IF/ELSE on the form, not a min(): "If the other parent's 3a >
    # $391, enter 5b. If <= $391, enter the amount from the shaded area of the Chart."
    # Box 2 has its OWN rule that overrides this: "enter $0 for Parent B, and for
    # Parent A: if Parent B 3a > $391, enter 5b..." Omitting that override made a
    # Box 2 order $15 too low at a low recipient income (caught in QA 2026-09-02).
    a5c = a5b if b3a > LOW_INCOME else table_a(b3a)
    if box == 2:
        b5c = 0.0
    else:
        b5c = b5b if a3a > LOW_INCOME else table_a(a3a)

    # --- 6a / 6b child care
    # zip() would silently drop a child listed by one parent only; pad to equal length.
    _n = max(len(a_childcare), len(b_childcare))
    _acc = tuple(a_childcare) + (0.0,) * (_n - len(a_childcare))
    _bcc = tuple(b_childcare) + (0.0,) * (_n - len(b_childcare))
    a6a = _cc_benchmarked([(x, y) for x, y in zip(_acc, _bcc)]) if a_childcare else 0.0
    b6a = _cc_benchmarked([(y, x) for x, y in zip(_acc, _bcc)]) if b_childcare else 0.0
    a6b, b6b = R(b3c * a6a), R(a3c * b6a)      # other parent's share of what this parent paid

    a6c, b6c = a5c + a6b, b5c + b6b

    # --- 6d / 6e income-disparity adjustment  (Box 1 and Box 3 share this path)
    if box == 2:
        a6d = b6d = None                 # "N/A"
        a6e, b6e = a6c, b6c
    else:
        a6d = 1.0 if a3a == 0 else P(a6c / a3a)
        b6d = 1.0 if b3a == 0 else P(b6c / b3a)
        # 6e: "...whichever is less, BUT NOT LESS THAN an amount from the shaded
        # area of the Guidelines Chart" -- the floor was previously unimplemented.
        # The form's own script leaves (6d + 10%) x 3a unrounded (Value_6e_pA/pB in
        # data/extracted/cjd304-xfa.xml); only 7d rounds. Verified 2026-09-05.
        a6e = a6c if a6d >= 0.10 else _floor(min(a6c, (a6d + 0.10) * b3a), b3a)
        b6e = b6c if b6d >= 0.10 else _floor(min(b6c, (b6d + 0.10) * a3a), a3a)

    # --- 6f payor / recipient
    if box == 2:
        recip, payor = "A", "B"
        r6e, p6e = a6e, b6e
        payor_3a = b3a
        recip_3a = a3a
    else:
        if a6e >= b6e:
            recip, payor, r6e, p6e, payor_3a, recip_3a = "A", "B", a6e, b6e, b3a, a3a
        else:
            recip, payor, r6e, p6e, payor_3a, recip_3a = "B", "A", b6e, a6e, a3a, b3a

    g6g = max(0.0, r6e - p6e)

    # --- 7a / 7b
    if box == 2:
        a7a = 1.0 if recip_3a == 0 else P(g6g / recip_3a)
        if a7a >= 0.10:
            b7b = g6g
        else:
            # "enter 6e, 6g, or ((7a + 10%) x Payor 3a), whichever is less": the form's
            # Value_7b script reads the RECIPIENT's 6e here (recipient_6e). Using the
            # payor's 6e zeroed the order whenever this branch fired. Fixed 2026-09-05.
            b7b = _floor(min(r6e, g6g, (a7a + 0.10) * payor_3a), payor_3a)
    else:
        a7a = None
        b7b = g6g

    d7d = R(max(0.0, b7b))                      # form: Math.round(7b - 7c)
    e7e = 1.0 if payor_3a == 0 else P(d7d / payor_3a)   # form: (7d / payor 3a).toFixed(2)

    return {
        "A_3a": a3a, "B_3a": b3a, "3b": b3b, "A_3c": a3c, "B_3c": b3c,
        "3d": d3d, "3e": e3e, "A_4c": a4c, "B_4c": b4c,
        "A_5c": a5c, "B_5c": b5c, "A_6a": a6a, "B_6a": b6a,
        "A_6b": a6b, "B_6b": b6b, "A_6c": a6c, "B_6c": b6c,
        "A_6d": a6d, "B_6d": b6d, "A_6e": a6e, "B_6e": b6e,
        "recipient": recip, "payor": payor,
        "6g": g6g, "7a": a7a, "7d": d7d, "7e": e7e,
        "hardship_box": e7e >= 0.40,
        "payor_3a": payor_3a,
    }
