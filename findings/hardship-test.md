---
layout: finding
title: The hardship test reads the wrong income
permalink: /findings/hardship-test/
description: >-
  Worksheet Line 7e tests for hardship by dividing the support order by a gross-derived income
  figure, but the order is paid from net income. At the author's own order, the line reports 40
  percent at the exact point his true burden has already reached 57 percent of net.
---

# Line 7e reports 40 percent of income at the point the payor has already reached 57 percent of net

<div class="disclosure">
<p>The worked example throughout &mdash; the payor, the $201,000 income, the child care figures &mdash;
is my own child support order: three children, my income and my children's mother's income entered
as the Worksheet requires. I disclose it because a reader should be able to check whether the
arithmetic changes when the numbers are real, not hypothetical. It doesn't: the same 17-point gap
holds across the income and child-care ranges charted below, not only at my own figures. The model
that produced every number here is <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>,
checked by <a href="/model/test_worksheet.py"><code>model/test_worksheet.py</code></a> against the
form's own calculation scripts, with
<a href="/model/runs/submission-figures-run-2026-09-05.txt">the printed run</a> behind the table
below.</p>
</div>

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

Section IV.C of the Massachusetts Child Support Guidelines presumes hardship once a support order
reaches 40 percent of the payor's available income. Worksheet Line 7e is the form's own test for
that threshold. It divides the order (Line 7d) by Line 3a — a figure computed before any tax is
withheld — while the order itself is paid out of what's left after taxes. At the worked example
below, that unit mismatch means Line 7e reports exactly 40 percent of income at the same point the
payor has actually reached 57 percent of his net income: a 17-point gap between what the form sees
and what he is actually paying.

## Line 7e divides by a pre-tax figure while the order is paid from net income

The worksheet computes Line 3a as gross income minus a short list of specific deductions (existing
support orders, health and dental premiums for the children) — nothing on the list is a tax. Line
7d is the presumptive support order. Line 7e is 7d ÷ 3a, expressed as a percentage, and the form
flags it once that percentage reaches 40 percent, triggering Section IV.C's rebuttable presumption
of hardship. The comparison the line is trying to make — does this order leave the payor too little
to live on — is a question about spendable income. Line 3a answers a different question: it is a
pre-tax figure with no tax adjustment of any kind. So the 40 percent line on Line 7e and the 40
percent line that matters to the payor's actual budget are not the same 40 percent.

## The lag runs from nothing at $0 of child care to 17 points at the $589 trigger

The example holds base support fixed and raises the recipient's claimed child care from $0 to the
statutory ceiling for three children ($1,290/week), tracking what Line 7e reports against the
payor's true share of net income at each point.

| Child care claimed | Order | Order (annual) | Line 7e reads | True share of net |
|---:|---:|---:|---:|---:|
| $0/wk | $1,013/wk | $52,662/yr | 26.5% | 37.7% |
| $100/wk | $1,100/wk | $57,221/yr | 28.8% | 40.9% |
| $300/wk | $1,276/wk | $66,340/yr | 33.4% | 47.4% |
| $589/wk | $1,529/wk | $79,506/yr | 40.0% | 56.9% |
| $1,290/wk (ceiling) | $2,144/wk | $111,479/yr | 56.1% | 79.7% |

Line 7e does not reach 40 percent until $589 a week of claimed child care — 46 percent of the
$1,290 statutory ceiling for three children. By the time it fires, the payor's true burden is
already 56.9 percent of his net income, a lag of 17 points between what the form reports and what
is actually true. (Source: `model/runs/submission-figures-run-2026-09-05.txt`, printed by
`model/submission_figures.py`.)

## The blind spot holds across the income range and across the child care range

<figure class="exhibit" id="e04">
  <img src="/figures/exhibits/E04-order-as-share-of-payor-net-3-children.png"
       loading="lazy"
       alt="Heatmap of the support order as a share of the payor's net income across a grid of
            higher-earner and lower-earner gross incomes, three children, Box 1, with a 40 percent
            contour line.">
  <figcaption>
    <h3 class="exhibit-title">The order exceeds 40 percent of the payor's net income only where the lower earner makes about $25,000 or less.</h3>
    <p class="exhibit-deck">Order as a share of the payor's net income, three children, Box 1, across a grid of both incomes.</p>
    <p class="exhibit-notes">The 40 percent contour, computed on net income, sits at a lower-earner income of about $25,000, up to roughly $235,000 of higher-earner income; above that the order never reaches 40 percent of net anywhere on the modelled grid. That is the region Section IV.C's hardship presumption is written for — E05 shows what the Worksheet itself reports there. Measured on the same 1,147-cell grid, the payor stays ahead per person in 99% of cells even where the household comparison favors the recipient.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig1_heatmaps.py</code> ·
      <a href="/figures/working/fig1_heatmap_3child_box1.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e05">
  <img src="/figures/exhibits/E05-what-line-7e-sees-vs-true-burden-worked-example.png"
       loading="lazy"
       alt="Line chart of Line 7e's reported percentage versus the true share of the payor's net
            income, against child care claimed from $0 to $600 a week, at the worked example.">
  <figcaption>
    <h3 class="exhibit-title">The hardship valve fires late because it reads the wrong income.</h3>
    <p class="exhibit-deck">Line 7e's reading vs. the true burden as claimed child care rises, worked example.</p>
    <p class="exhibit-notes">The true burden passes 40% of net at $80/week of child care; Line 7e reports 40% at $590/week, by which point the true burden is 57%. Nothing on the form flags the gap.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig6_valve.py</code> ·
      <a href="/figures/working/fig6_valve_units_lag.csv">data (CSV)</a></p>
  </figcaption>
</figure>

## The valve fires eventually; the defect is when, not whether

The valve does eventually fire. This is not a claim that Section IV.C's hardship presumption is
unreachable — at $589 a week of claimed child care it reports the 40 percent threshold, and a payor
can still raise it. The defect is a 17-point lag, not an impossibility.

$430 a child, and $1,290 a week for three children, is the statutory ceiling on allowable child
care — not a typical claim. Most cases will involve a smaller amount, and the gap between what Line
7e reports and the payor's true burden narrows as claimed child care falls (at $100 a week the gap
is about 12 points, not 17). One worked example is not a distribution across cases; how often actual
claims sit near the benchmark is not known from anything in this repository.

And as with every household comparison here: per person, the payor remains ahead. Across the full
grid behind E04, the payor holds more per person than the recipient's household in 99 percent of the
1,147 modelled cells, even in the 55 percent of cells where the recipient's household holds more in
total.

## Check it yourself

The Line 7e figures above are pinned by the worksheet's own test suite, not asserted from a chart:

- [`model/worksheet.py`](/model/worksheet.py) — the line-by-line implementation, transcribed from
  form CJ-D 304 (12/01/2025) and checked against the form's own calculation scripts.
- [`model/test_worksheet.py`](/model/test_worksheet.py) — the test that pins Line 7e's behavior as
  child care rises, including that it does **not** fire at $300/week ("7e≈33.4%") and that it rises
  monotonically with claimed child care.
- [`model/runs/submission-figures-run-2026-09-05.txt`](/model/runs/submission-figures-run-2026-09-05.txt)
  — the printed run behind the table above.
