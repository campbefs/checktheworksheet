---
layout: finding
title: The hardship test reads the wrong income
permalink: /findings/hardship-test/
description: >-
  Worksheet Line 7e tests for hardship by dividing the support order by a gross-derived income
  figure, but the order is paid from net income. At the author's own order, the hardship
  presumption does not kick in until the payor is at 57 percent of net income.
disclosure:
  - >-
    The worked example throughout (the payor, the $201,000 income, the child care figures) is my
    own child support order: three children, my income and my children's mother's income entered
    as the Worksheet requires. I disclose it because a reader should be able to check whether the
    arithmetic changes when the numbers are real, not hypothetical. It doesn't: the same 17-point
    gap holds across the income and child-care ranges charted below as well as at my own figures.
  - >-
    The model behind every number on this page is
    <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>, checked by
    <a href="/model/test_worksheet.py"><code>model/test_worksheet.py</code></a> against the
    form's own calculation scripts, with
    <a href="/model/runs/submission-figures-run-2026-09-05.txt">the printed run</a> behind the
    table below.
rail_label: "On this page"
sections:
  - id: mechanism
    label: "The mechanism"
  - id: exhibits
    label: "Across the income range"
  - id: method
    label: "Method: the full lag table"
  - id: caveats
    label: "What this isn't"
  - id: check
    label: "Check it yourself"
---

{% include disclosure.html %}

<section class="hero" markdown="1">
<p class="eyebrow">Finding 1 of 4</p>

# The hardship presumption does not kick in until the payor is at 57 percent of net income

<p class="lede">Section IV.C presumes hardship once a support order reaches 40 percent of the
payor's available income. The Worksheet's own test for that threshold divides the order by a
figure computed before tax, while the order is paid out of what's left after tax. At the worked
example, the presumption doesn't actually kick in until the payor is at 57 percent of his net
income.</p>
</section>

<div class="numeral-pair numeral-pair--solo">
  <div class="numeral">
    <span class="numeral-value">17</span>
    <p class="numeral-caption">Point gap, at the worked example, between what Line 7e reports and the payor's true share of net income at the moment the hardship presumption finally kicks in</p>
  </div>
</div>

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

<div class="page-shell" markdown="1">
{% include chapter-rail.html %}
<div class="content-col" markdown="1">

<section id="mechanism" markdown="1">

## Line 7e divides by a pre-tax figure while the order is paid from net income

Worksheet Line 7e divides Line 7d (the presumptive order) by Line 3a (available income) and flags
the result once it reaches 40 percent, triggering Section IV.C's rebuttable presumption of hardship.
Line 3a is gross income minus a short list of specific deductions (existing support orders, and
health and dental premiums for the children), none of them a tax — so Line 7e answers a question
about spendable income with a figure that has no tax adjustment at all.

</section>

<section id="exhibits" markdown="1">

## The blind spot holds across the child care range and across the income range

{% include figure.html
   id="e05"
   img="/figures/exhibits/E05-what-line-7e-sees-vs-true-burden-worked-example.png"
   alt="Line chart of Line 7e's reported percentage versus the true share of the payor's net income, against child care claimed from $0 to $600 a week, at the worked example."
   title="The hardship valve fires late because it reads the wrong income."
   deck="At the worked example, Line 7e divides the order by gross-derived available income while the order is paid from net income."
   notes="As child care claimed by the recipient rises, the true burden passes 40 percent of net at $80 a week of child care; Line 7e reports 40 percent at $589 a week, by which point the true burden is 56.9 percent. Nothing on the form flags the gap."
   source_script="model/charts/fig6_valve.py"
   csv_href="/figures/working/fig6_valve_units_lag.csv"
   lazy="false" %}

{% include figure.html
   id="e04"
   img="/figures/exhibits/E04-order-as-share-of-payor-net-3-children.png"
   alt="Heatmap of the support order as a share of the payor's net income across a grid of higher-earner and lower-earner gross incomes, three children, Box 1, with a 40 percent contour line."
   title="The order exceeds 40 percent of the payor's net income only where the lower earner makes about $20,000 or less."
   deck="Order as a share of the payor's net income, three children, Box 1, across a grid of both incomes."
   notes="The 40 percent contour, computed on net income, sits at a lower-earner income of about $20,000, up to roughly $205,000 of higher-earner income; above that the order never reaches 40 percent of net on the grid. Section IV.C's hardship presumption targets this region; E05 shows what the Worksheet reports there."
   source_script="model/charts/fig1_heatmaps.py"
   csv_href="/figures/working/fig1_heatmap_3child_box1.csv" %}

</section>

<section id="method" markdown="1">

<details markdown="1">
<summary>Method: the full lag table, and how Line 7e is computed</summary>

The table below holds base support fixed and raises the recipient's claimed child care from $0 to
the statutory ceiling for three children ($1,290 a week), tracking what Line 7e reports against the
payor's true share of net income at each point.

| Child care claimed | Order | Order (annual) | Line 7e reads | True share of net |
|---:|---:|---:|---:|---:|
| $0/wk | $1,013/wk | $52,662/yr | 26.5% | 37.7% |
| $100/wk | $1,100/wk | $57,221/yr | 28.8% | 40.9% |
| $300/wk | $1,276/wk | $66,340/yr | 33.4% | 47.4% |
| $589/wk | $1,529/wk | $79,506/yr | 40.0% | 56.9% |
| $1,290/wk (ceiling) | $2,144/wk | $111,479/yr | 56.1% | 79.7% |

Line 7e does not reach 40 percent until $589 a week of claimed child care, 46 percent of the $1,290
statutory ceiling for three children, by which point the payor's true burden is 54.6 percent of his
net income. That 17-point lag narrows as claimed child care falls, to about 12 points at $100 a
week. (Source: `model/runs/submission-figures-run-2026-09-05.txt`, printed by
`model/submission_figures.py`.)

</details>

</section>

<section id="caveats" markdown="1">

## What this isn't

<p class="caveat">The valve does eventually fire; this isn't a claim that Section IV.C's hardship
presumption is unreachable, only that it fires 17 points late. $1,290 a week for three children is
the statutory ceiling on allowable child care, not a typical claim. This is one worked example, and
how often actual claims sit near that benchmark isn't known from anything in this repository.</p>

<p class="caveat">Per person, the payor remains ahead. Across the full grid behind the heatmap
above, the payor holds more per person than the recipient's household in 99 percent of the 1,147
modelled cells, and holds more per household too in 90 percent of them. The recipient's household
still holds more in total in the remaining 10 percent.</p>

</section>

<section id="check" markdown="1">

<div class="check-yourself">
<h2>Check it yourself</h2>
<p>The Line 7e figures above are pinned by the worksheet's own test suite, not asserted from a
chart.</p>
<ul>
  <li><strong><a href="/model/worksheet.py"><code>model/worksheet.py</code></a></strong>
    The line-by-line implementation, transcribed from form CJ-D 304 (12/01/2025) and checked
    against the form's own calculation scripts.</li>
  <li><strong><a href="/model/test_worksheet.py"><code>model/test_worksheet.py</code></a></strong>
    Pins Line 7e's behavior as child care rises, including that it does not fire at $300/week
    ("7e ≈ 33.4%") and that it rises monotonically with claimed child care.</li>
  <li><strong><a href="/model/runs/submission-figures-run-2026-09-05.txt">The printed run</a></strong>
    The output behind the table above.</li>
  <li><strong><a href="/figures/working/fig6_valve_units_lag.csv">fig6_valve_units_lag.csv</a></strong>
    The 130-row data file behind the line chart.</li>
</ul>
</div>

</section>

</div>
</div>
