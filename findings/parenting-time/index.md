---
layout: finding
title: The parenting-time credit shrinks as the income gap widens
permalink: /findings/parenting-time/
description: >-
  The Worksheet's credit for equal parenting time falls from 77.6 percent to 6.9 percent as the
  income gap between the parents widens, and no line in the calculation ever measures time.
disclosure:
  - >-
    The worked example below is my own child support order: three children, equal parenting time,
    my income and my children's mother's income entered as the Worksheet requires. I disclose it
    because a reader should be able to check whether the arithmetic changes when the numbers are
    real, not hypothetical.
  - >-
    The model that produced every figure on this page is
    <a href="/model/box1_fix.py"><code>model/box1_fix.py</code></a>, checked against
    <a href="/model/worksheet.py"><code>model/worksheet.py</code></a> and against the form's own
    official calculation scripts in
    <a href="/model/runs/official-xfa-vs-model-2026-09-05.txt">model/runs/official-xfa-vs-model-2026-09-05.txt</a>.
rail_label: "On this page"
sections:
  - id: mechanism
    label: "The mechanism"
  - id: exhibits
    label: "How the credit collapses"
  - id: overnights
    label: "Priced as overnights"
  - id: method
    label: "Method: full range and income floor"
  - id: caveats
    label: "What this isn't"
  - id: check
    label: "Check it yourself"
---

{% include disclosure.html %}

<section class="hero">
<p class="eyebrow">Finding 3 of 4</p>

# The Worksheet's credit for equal parenting time falls from 77.6 percent to 6.9 percent as the income gap widens, with no measure of time anywhere in the calculation

<p class="lede">Box 1's credit for equal parenting time equals the payor's own Line 6e, and Line 6e
has no time in it. So the credit tracks how far apart the two incomes are, not how the children's
time is actually split.</p>
</section>

<div class="numeral-pair numeral-pair--solo">
  <div class="numeral">
    <span class="numeral-value">6.9%</span>
    <p class="numeral-caption">The equal-parenting credit at the worked example, an 87.7 percent payor income share, down from 77.6 percent at a 56.3 percent share</p>
  </div>
</div>

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

<div class="page-shell">
{% include chapter-rail.html %}
<div class="content-col">

<section id="mechanism">

## Box 1's credit for equal parenting time equals the payor's own Line 6e, and Line 6e has no time in it

Massachusetts's Worksheet form (CJ-D 304) offers two relevant boxes: Box 2, where one parent has the
children the great majority of the time, and Box 1, where the parents share time equally. Both boxes
compute the same total support amount at Line 4c ($1,240.73 a week at the worked example: three
children, a payor at $201,000 a year, the other parent at $570 a week), then divide it between the
parents by their shares of combined income. Line 5b assigns the payor 87.68 percent of that amount,
$1,087.90 a week — the order Box 2 would produce for the same family. Box 1 then subtracts a credit
at Line 6g, and that credit is exactly the payor's own Line 6e: $75.17 a week, capped there because
his own income share is below 10 percent. $75.17 out of $1,087.90 is 6.9 percent. Nothing in Lines
4c through 6g asks how many overnights either parent actually has.

<p class="stat-callout">
  <span class="stat-value">$75 of $1,088</span>
  <span class="stat-label">the equal-parenting credit at the worked example against the order Box 2 would produce for the same family: 6.9 percent, and no line in the calculation measures time</span>
</p>

</section>

<section id="exhibits">

## The credit tracks the income gap, not the calendar, and runs backward as the gap widens

{% include figure.html
   id="e08"
   img="/figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png"
   alt="Line chart of the Box 1 order's percentage reduction from the one-third-time order, across the payor's share of combined income, for the current Worksheet and two redlined variants, three children."
   title="The Worksheet's credit for equal parenting time collapses as the income gap widens; a cross-credit narrows without collapsing."
   deck="The reduction in the order for equal time, against the one-third-time order, falls from about 75 percent at a 57 percent payor income share to 7 percent at 88 percent and 1 percent at 96 percent, because no parenting-time quantity enters any line."
   notes="Variant A, applying Line 6e once, lifts the curve; Variant B, the standard cross-credit at a 1.5 duplication factor used by 23 states, stops it collapsing."
   source_script="model/box1_fix.py · model/charts/fig3_credit.py"
   csv_href="/figures/working/fig3_credit_collapse.csv"
   lazy="false" %}

Even the fix other states use does not put the calendar into the calculation. Removing the clip once,
so the payor's own entitlement is not capped a second time (Variant A), raises the order's reduction
to 14.0 percent, an order of $935.06. Applying the standard cross-credit design used by 23 states, at
a 1.5 duplication factor (Variant B), raises the reduction to 35.5 percent, an order of $701.30 — a
30.8 percent drop from the current $1,012.73. Neither variant adds a term for how much time either
parent actually has the children: both change how the income-share gap is priced, not what is being
priced.

</section>

<section id="overnights">

## Priced as overnights, equal time comes out to a third of the calendar under one factor and just under half under another

Massachusetts's own commentary and guidelines contain no number for how much of the shared-care cost
is duplicated between two households. Other states' cross-credit formulas do, which makes it
possible to solve the Box 1 arithmetic backward: asking what overnight share, run through a standard
cross-credit, would reproduce the actual $1,012.73 order answers how much parenting time
Massachusetts is effectively pricing equal custody at. The answer depends entirely on which
duplication factor is used, so the factor must always be stated beside the number.

<p class="stat-callout">
  <span class="stat-value">33.3% at factor 1.5 &middot; 46.9% at factor 2.0</span>
  <span class="stat-label">the overnight share the Box 1 order at the worked example implies under a standard cross-credit. Never quote one of these numbers without its factor</span>
</p>

{% include figure.html
   id="e09"
   img="/figures/exhibits/E09-implied-overnight-share-by-factor-3-children.png"
   alt="Line chart of the overnight share that would reproduce the Box 1 order under a standard cross-credit, at duplication factors 1.5 and 2.0, across the payor's income share, three children."
   title="At the worked example, equal parenting time is priced as a third of overnights at factor 1.5, and 47 percent at factor 2.0."
   deck="The overnight share that reproduces the Box 1 order under a standard cross-credit. The number depends on the duplication factor, so the factor is always stated beside it."
   notes="The curve is blank below the Line 5c floor, where the order is no longer a cross-credit and cannot be expressed as an implied overnight share."
   source_script="model/box1_fix.py · model/charts/fig3_credit.py"
   csv_href="/figures/working/fig3_credit_collapse.csv" %}

At the 1.5 duplication factor (the figure Indiana's Child Support Guideline 6 Commentary uses to
quantify equal-parenting duplication), the Box 1 order at the worked example implies an overnight
share of 33.3 percent. At the 2.0 factor implied by Box 1's own uncapped arithmetic — both parents'
columns carry every child at the full schedule amount — it implies 46.9 percent. Neither reaches the
50 percent the parent in the worked example actually has.

</section>

<section id="method">

<details markdown="1">
<summary>Method: the credit across incomes, and where it stops meaning anything</summary>

Holding the payor's income and the three children fixed and moving only the other parent's income
shows the same equal-parenting arrangement priced very differently depending on how far apart the
two incomes are:

<table class="exhibit-table">
  <caption>The Box 1 credit for equal parenting time, by the other parent's weekly gross income: full data behind <a href="#e08">Exhibit E08</a></caption>
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

The wider the gap between the two incomes, the smaller the equal-parenting credit: from 64.5 percent
of the Box 2 order at a 60.8 percent income share down to 1.3 percent at a 94.6 percent share.

At $400 and $250 a week for the other parent, the printed run marks the implied-overnight-share
columns "n/a." Below $391 a week of the other parent's available income, Line 5c substitutes a fixed
shaded-area amount rather than a percentage of income, so the Box 1 order is no longer a
cross-credit and no overnight share can be backed out of it. The chart's curve is left blank over
that range rather than showing a number that would not mean what it appears to mean.

</details>

</section>

<section id="caveats">

## What this isn't

<p class="caveat">Every figure on this page comes from one fact pattern: three children, equal
parenting time, no child care claimed, at the incomes stated. The mechanism — Box 1's credit
equalling the payor's own capped Line 6e — is a property of the form itself and does not depend on
the fact pattern; the specific dollar amounts and percentages do. This page says nothing about Box
2, about primary custody, or about any arrangement other than equal time.</p>

<p class="caveat">Per person, the standing caveat applies here too: nothing on this page compares
what the payor keeps for himself against what each member of the recipient's household holds. See
the <a href="/findings/hardship-test/">hardship-test</a> and <a href="/findings/child-care/">child
care</a> findings for that comparison at the same worked example.</p>

</section>

<section id="check">

<div class="check-yourself">
<h2>Check it yourself</h2>
<p>Every number above is printed by a committed script and backed by a CSV of the plotted values.</p>
<ul>
  <li><strong><a href="/model/box1_fix.py"><code>model/box1_fix.py</code></a></strong>
    Computes the Box 1 credit, the two redlined variants, and the implied overnight share.</li>
  <li><strong><a href="/model/runs/box1-fix-run-2026-09-05.txt">The full printed run</a></strong>
    Behind every figure on this page.</li>
  <li><strong><a href="/figures/working/fig3_credit_collapse.csv">fig3_credit_collapse.csv</a></strong>
    The data behind Exhibits E08 and E09.</li>
  <li><strong><a href="https://github.com/campbefs/checktheworksheet">The repository</a></strong></li>
</ul>
</div>

</section>

</div>
</div>
