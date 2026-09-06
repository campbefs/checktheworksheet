---
layout: finding
title: The parenting-time credit shrinks as the income gap widens
description: >-
  The Worksheet's credit for equal parenting time is the difference between the parents' income
  shares, capped by one line, with no measure of time anywhere in it — so the credit shrinks as the
  gap between the parents' incomes widens, and very nearly disappears at a wide gap.
---

# The Worksheet's credit for equal parenting time is a gap between income shares, not a measure of time, and it shrinks as the income gap widens

<div class="disclosure">
<p>The worked example below is my own child support order: three children, equal parenting time,
my income and my children's mother's income entered as the Worksheet requires. I disclose it
because a reader should be able to check whether the arithmetic changes when the numbers are real,
not hypothetical. The model that produced every figure on this page is
<a href="/model/box1_fix.py"><code>model/box1_fix.py</code></a>, checked against
<a href="/model/worksheet.py"><code>model/worksheet.py</code></a> and against the form's own
official calculation scripts in
<a href="/model/runs/official-xfa-vs-model-2026-09-05.txt">model/runs/official-xfa-vs-model-2026-09-05.txt</a>.</p>
</div>

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

## Box 1's credit for equal parenting time equals the payor's own Line 6e, and Line 6e has no time in it

Massachusetts's Worksheet form (CJ-D 304) offers two relevant boxes: Box 2, where one parent has
the children the great majority of the time, and Box 1, where the parents share time equally. Both
boxes compute the same total support amount at Line 4c — $1,240.73 a week at the worked example
(three children, a payor at $201,000 a year, the other parent at $570 a week) — then divide it
between the parents by their shares of combined income. Line 5b assigns the payor 87.68 percent of
that amount, $1,087.90 a week; that figure is the order Box 2 would produce for the same family.

Box 1 subtracts a credit at Line 6g, and that credit is exactly the payor's own Line 6e: $75.17 a
week, capped there because his own income share (4.0 percent of his column's entitlement) is below
10 percent. $75.17 out of $1,087.90 is 6.9 percent. Nothing in Lines 4c through 6g asks how many
overnights either parent actually has.

<p class="stat-callout">
  <span class="stat-value">$75 of $1,088</span>
  <span class="stat-label">the equal-parenting credit at the worked example against the order Box 2 would produce for the same family — 6.9 percent, and no line in the calculation measures time</span>
</p>

## The credit tracks the income gap, not the calendar, and runs backward as the gap widens

Holding the payor's income and the three children fixed and moving only the other parent's income
shows the same equal-parenting arrangement priced very differently depending on how far apart the
two incomes are:

<table class="exhibit-table">
  <caption>The Box 1 credit for equal parenting time, by the other parent's weekly gross income — full data behind <a href="#e08">Exhibit E08</a></caption>
  <thead>
    <tr>
      <th scope="col">Other parent's weekly gross</th>
      <th scope="col">Payor's share of combined income</th>
      <th scope="col">Box 1 order</th>
      <th scope="col">Credit against Box 2</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="numeric">$2,500</td><td class="numeric">60.8%</td><td class="numeric">$340</td><td class="numeric">64.5%</td></tr>
    <tr><td class="numeric">$1,800</td><td class="numeric">68.4%</td><td class="numeric">$536</td><td class="numeric">46.2%</td></tr>
    <tr><td class="numeric">$1,200</td><td class="numeric">76.6%</td><td class="numeric">$826</td><td class="numeric">20.5%</td></tr>
    <tr><td class="numeric">$900</td><td class="numeric">81.5%</td><td class="numeric">$920</td><td class="numeric">13.3%</td></tr>
    <tr><td class="numeric">$700</td><td class="numeric">85.1%</td><td class="numeric">$977</td><td class="numeric">9.2%</td></tr>
    <tr class="is-reader-state"><td class="numeric">$570 (worked example)</td><td class="numeric">87.7%</td><td class="numeric">$1,013</td><td class="numeric">6.9%</td></tr>
    <tr><td class="numeric">$400</td><td class="numeric">91.2%</td><td class="numeric">$1,075</td><td class="numeric">2.6%</td></tr>
    <tr><td class="numeric">$250</td><td class="numeric">94.6%</td><td class="numeric">$1,103</td><td class="numeric">1.3%</td></tr>
  </tbody>
</table>

The wider the gap between the two incomes, the smaller the equal-parenting credit — from 64.5
percent of the Box 2 order at a 60.8 percent income share down to 1.3 percent at a 94.6 percent
share. At the worked example, an 87.7 percent income share, the credit has already fallen to 6.9
percent.

<figure class="exhibit" id="e08">
  <img src="/figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png"
       width="1770" height="1389"
       alt="Line chart of the Box 1 order's percentage reduction from the one-third-time order, across the payor's share of combined income, for the current Worksheet and two redlined variants, three children.">
  <figcaption>
    <h3 class="exhibit-title">The Worksheet's credit for equal parenting time collapses as the income gap widens; a cross-credit narrows without collapsing.</h3>
    <p class="exhibit-deck">The reduction in the order for equal time, against the one-third-time order, falls from about 75 percent at a 57 percent payor income share to 7 percent at 88 percent and 1 percent at 96 percent, because no parenting-time quantity enters any line.</p>
    <p class="exhibit-notes">Variant A, applying Line 6e once, lifts the curve; Variant B, the standard cross-credit at a 1.5 duplication factor used by 23 states, stops it collapsing.</p>
    <p class="exhibit-source">Source: <code>model/box1_fix.py</code> · <code>model/charts/fig3_credit.py</code> ·
      <a href="/figures/working/fig3_credit_collapse.csv">data (CSV)</a> ·
      <a href="/model/runs/box1-fix-run-2026-09-05.txt">printed run</a></p>
  </figcaption>
</figure>

## Even the fix other states use does not put the calendar into the calculation

The same clip that produces the 6.9 percent credit could be applied differently. Removing it once,
so the payor's own entitlement is not capped a second time (Variant A), raises the order's reduction
to 14.0 percent, an order of $935.06. Applying the standard cross-credit design used by 23 states,
at a 1.5 duplication factor (Variant B), raises the reduction to 35.5 percent, an order of $701.30 —
a 30.8 percent drop from the current $1,012.73. Neither variant adds a term for how much time either
parent actually has the children: both change how the income-share gap is priced, not what is being
priced.

## Priced as overnights, equal time comes out to a third of the calendar under one factor and just under half under another

Massachusetts's own commentary and the guidelines contain no number for how much of the shared-care
cost is duplicated between two households. Other states' cross-credit formulas do: solving the Box 1
arithmetic backward — asking what overnight share, run through a standard cross-credit, would
reproduce the actual $1,012.73 order — answers how much parenting time Massachusetts is effectively
pricing equal custody at. The answer depends entirely on which duplication factor is used, so the
factor must always be stated beside the number.

<p class="stat-callout">
  <span class="stat-value">33.3% at factor 1.5 · 46.9% at factor 2.0</span>
  <span class="stat-label">the overnight share the Box 1 order at the worked example implies under a standard cross-credit — never quote one of these numbers without its factor</span>
</p>

At the 1.5 duplication factor — the figure Indiana's Child Support Guideline 6 Commentary uses to
quantify equal-parenting duplication — the Box 1 order at the worked example implies an overnight
share of 33.3 percent. At the 2.0 factor implied by Box 1's own uncapped arithmetic (both parents'
columns carry every child at the full schedule amount), it implies 46.9 percent. Neither reaches the
50 percent the parent in the worked example actually has.

<figure class="exhibit" id="e09">
  <img src="/figures/exhibits/E09-implied-overnight-share-by-factor-3-children.png"
       width="1756" height="1387"
       loading="lazy"
       alt="Line chart of the overnight share that would reproduce the Box 1 order under a standard cross-credit, at duplication factors 1.5 and 2.0, across the payor's income share, three children.">
  <figcaption>
    <h3 class="exhibit-title">At the worked example, equal parenting time is priced as a third of overnights at factor 1.5, and 47 percent at factor 2.0.</h3>
    <p class="exhibit-deck">The overnight share that reproduces the Box 1 order under a standard cross-credit. The number depends on the duplication factor, so the factor is always stated beside it.</p>
    <p class="exhibit-notes">The curve is blank below the Line 5c floor, where the order is no longer a cross-credit and cannot be expressed as an implied overnight share.</p>
    <p class="exhibit-source">Source: <code>model/box1_fix.py</code> · <code>model/charts/fig3_credit.py</code> ·
      <a href="/figures/working/fig3_credit_collapse.csv">data (CSV)</a> ·
      <a href="/model/runs/box1-fix-run-2026-09-05.txt">printed run</a></p>
  </figcaption>
</figure>

## Below the Worksheet's income floor, this relationship cannot be expressed at all

At $400 and $250 a week for the other parent — both above the worked example's $570 but shown here
because the floor sits nearby — the printed run marks the implied-overnight-share columns "n/a."
Below $391 a week of the other parent's available income, Line 5c substitutes a fixed shaded-area
amount rather than a percentage of income, so the Box 1 order is no longer a cross-credit and no
overnight share can be backed out of it. The chart's curve is left blank over that range rather than
showing a number that would not mean what it appears to mean.

## What this does and doesn't show

Every figure on this page comes from one fact pattern: three children, equal parenting time, no
child care claimed, at the incomes stated. The mechanism — Box 1's credit equalling the payor's own
capped Line 6e — is a property of the form itself and does not depend on the fact pattern; the
specific dollar amounts and percentages do. This page says nothing about Box 2, about primary
custody, or about any arrangement other than equal time.

<div class="ask">
<h2>Check it yourself</h2>
<p>Every number above is printed by a committed script and backed by a CSV of the plotted values.</p>
<ul>
  <li><a href="/the-model/">The model</a></li>
  <li><a href="/model/box1_fix.py"><code>model/box1_fix.py</code></a></li>
  <li><a href="/model/runs/box1-fix-run-2026-09-05.txt">The full printed run behind this page</a></li>
  <li><a href="/figures/working/fig3_credit_collapse.csv">The data behind Exhibits E08 and E09 (CSV)</a></li>
  <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
</ul>
</div>
