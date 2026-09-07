---
layout: finding
title: Equal parenting time buys a 6.9 percent discount, and here is why
permalink: /findings/parenting-time/
description: >-
  Equal parenting time earns a 6.9 percent discount off the Worksheet's primary-custody order,
  because the credit is just the gap between the two parents' income shares. No line measures time.
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
  - id: third
    label: "Why the form starts at \"a third\""
  - id: small
    label: "Why the credit is so small"
  - id: cross-credit
    label: "What a cross-credit formula would say"
  - id: caveats
    label: "What this isn't"
  - id: check
    label: "Check it yourself"
---

{% include disclosure.html %}

<section class="hero" markdown="1">
<p class="eyebrow">Finding 3 of 4</p>

# A 6.9 percent discount is what equal parenting time buys at the worked example, against the Worksheet's primary-custody order

<p class="lede">The primary-custody order is $1,087.90 a week. The equal-time order is $1,012.73.
This $75.17 gap is the whole discount for splitting time equally instead of the other way: 6.9
percent. The next two sections explain where the "a third" language comes from and why the discount
is this small.</p>
</section>

<div class="numeral-pair numeral-pair--solo">
  <div class="numeral">
    <span class="numeral-value">6.9%</span>
    <p class="numeral-caption">The equal-parenting discount at the worked example, an 87.7 percent payor income share, down from 77.6 percent at a 56.3 percent share</p>
  </div>
</div>

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

<div class="page-shell" markdown="1">
{% include chapter-rail.html %}
<div class="content-col" markdown="1">

<section id="mechanism" markdown="1">

## Both custody boxes start from the same total, split by income, then Box 1 subtracts one credit

Massachusetts's Worksheet form (CJ-D 304) has two custody boxes, primary (Box 2) and equal time
(Box 1). Both start from the same total support amount at Line 4c: $1,240.73 a week at the worked example (three children, a payor at
$201,000 a year, the other parent at $570 a week). Line 5b splits that by income share, giving the
payor 87.68 percent, $1,087.90, the order Box 2 produces. Box 1 then subtracts one credit at Line 6g,
which turns out to equal the payor's own Line 6e, capped low because his income share sits below 10
percent: $75.17, leaving $1,012.73, a 6.9 percent reduction. Nothing between Line 4c and Line 6g
asks how many overnights either parent has.

<p class="stat-callout">
  <span class="stat-value">$75 of $1,088</span>
  <span class="stat-label">the equal-parenting discount at the worked example against the order Box 2 would produce for the same family: 6.9 percent, and no line in the calculation measures time</span>
</p>

</section>

<section id="third" markdown="1">

## Box 2, the primary-custody box, already assumes the paying parent has the children about a third of the nights

Box 2 is not a zero-time box for the parent paying support. Its own calculation assumes that parent
already has the children about one night in three; that is the arrangement Box 2 is built around.
Checking Box 1 instead, the equal-time box, is what produces the 6.9 percent discount above. It is
not a separate credit for having the children a third of the time, and there is no such credit
anywhere on this form. The one-third figure describes the paying parent's own time under Box 2, not
the other parent's time.

</section>

<section id="small" markdown="1">

## The discount is small because no line on the form measures parenting time

Line 6g is the difference between the two parents' Line 6e amounts, and Line 6e reduces to each
parent's income share once Box 1 assigns zero children to the payor's column. So the discount tracks
how far apart the two incomes are, not how the children's time is split, and it shrinks as the income
gap widens.

{% include figure.html
   id="e08"
   img="/figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png"
   alt="Line chart of the Box 1 order's percentage reduction from the primary-custody order, across the payor's share of combined income, for the current Worksheet and two redlined variants, three children."
   title="The Worksheet's credit for equal parenting time collapses as the income gap widens; a cross-credit narrows without collapsing."
   deck="The discount for equal time, against the primary-custody order, falls from about 75 percent at a 57 percent payor income share to 7 percent at 88 percent and 1 percent at 96 percent, because no parenting-time quantity enters any line."
   notes="Variant A, applying Line 6e once, raises the discount to 14.0 percent. Variant B, the cross-credit design 23 states use at a 1.5 duplication factor, raises it to 35.5 percent and stops it collapsing."
   source_script="model/box1_fix.py · model/charts/fig3_credit.py"
   csv_href="/figures/working/fig3_credit_collapse.csv"
   lazy="false" %}

Variant A's order is $935.06; Variant B's is $701.30, a 30.8 percent drop from today's $1,012.73.
Neither redline adds a term for how much time either parent actually has. Both just change how the
income gap is priced, not what is being priced.

<details markdown="1">
<summary>Method: the credit at eight other incomes for the other parent</summary>

<table class="exhibit-table">
  <caption>The Box 1 discount for equal parenting time, by the other parent's weekly gross income: full data behind <a href="#e08">Exhibit E08</a></caption>
  <thead>
    <tr>
      <th scope="col">Other parent's weekly gross</th>
      <th scope="col">Payor's share of combined income</th>
      <th scope="col">Box 1 order</th>
      <th scope="col">Discount against Box 2</th>
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

Below $391 a week of the other parent's available income (the bottom two rows), Line 5c substitutes
a fixed floor amount rather than a percentage of income, so the order stops behaving like a
cross-credit. (Source: `model/runs/box1-fix-run-2026-09-05.txt`, printed by `model/box1_fix.py`.)

</details>

</section>

<section id="cross-credit" markdown="1">

<details markdown="1">
<summary>What a cross-credit formula would say</summary>

Massachusetts doesn't say how much cost two households duplicate when they share custody. Twenty-three
other states answer that with a cross-credit: multiply the basic obligation by a duplication factor
(Indiana's commentary sets 1.5) before subtracting the lower earner's share.

Solving the Box 1 arithmetic backward through that formula turns up a coincidence, not a description
of anyone's actual time: the 6.9 percent discount Massachusetts gives for full equal time is close to
what a cross-credit would give a parent who has the children one night in three, a different "third"
from the Box 2 assumption above: this one comes from running a number backward through another
state's formula, not from anything Massachusetts's own form assumes.

<p class="stat-callout">
  <span class="stat-value">33.3% at factor 1.5 &middot; 46.9% at factor 2.0</span>
  <span class="stat-label">the overnight share the Box 1 order at the worked example implies under a standard cross-credit. Never quote one of these numbers without its factor</span>
</p>

{% include figure.html
   id="e09"
   img="/figures/exhibits/E09-implied-overnight-share-by-factor-3-children.png"
   alt="Line chart of the overnight share that would reproduce the Box 1 order under a standard cross-credit, at duplication factors 1.5 and 2.0, across the payor's income share, three children."
   title="At the worked example, equal parenting time is priced as a third of overnights at factor 1.5, and 47 percent at factor 2.0."
   deck="The overnight share that reproduces the Box 1 order under a standard cross-credit, at the stated factor. Never quoted without the factor beside it."
   notes="Blank below the Line 5c floor, where the order is no longer a cross-credit and no overnight share can be backed out of it."
   source_script="model/box1_fix.py · model/charts/fig3_credit.py"
   csv_href="/figures/working/fig3_credit_collapse.csv" %}

At the 1.5 factor, neither implied share (33.3 percent or 46.9 percent) reaches the 50 percent this
parent actually has.

</details>

</section>

<section id="caveats" markdown="1">

## What this isn't

<p class="caveat">Every figure on this page comes from one fact pattern: three children, equal
parenting time, no child care claimed, at the incomes stated. The mechanism, Box 1's discount
equalling the payor's own capped Line 6e, is a property of the form itself and does not depend on
the fact pattern; the specific dollar amounts and percentages do. This page says nothing about Box
2, about primary custody, or about any arrangement other than equal time.</p>

<p class="caveat">Per person, the standing caveat applies here too: nothing on this page compares
what the payor keeps for himself against what each member of the recipient's household holds. See
the <a href="/findings/hardship-test/">hardship-test</a> and <a href="/findings/child-care/">child
care</a> findings for that comparison at the same worked example.</p>

</section>

<section id="check" markdown="1">

<div class="check-yourself">
<h2>Check it yourself</h2>
<p>Every number above is printed by a committed script and backed by a CSV of the plotted values.</p>
<ul>
  <li><strong><a href="/model/box1_fix.py"><code>model/box1_fix.py</code></a></strong>
    Computes the Box 1 discount, the two redlined variants, and the implied overnight share.</li>
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
