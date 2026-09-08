---
layout: finding
title: Child care is split on income shares the order has already changed
permalink: /findings/child-care/
description: >-
  Worksheet Line 6b allocates child care using each parent's share of income before the base
  support order transfers any money between households. At the author's own order, that charges
  the payor 88 cents of every dollar of a $15,600 claim.
disclosure:
  - >-
    The worked example throughout (the payor, the recipient's $300-a-week child care claim) is my
    own child support order: three children, my income and my children's mother's income entered
    as the Worksheet requires. I disclose it because a reader should be able to check whether the
    arithmetic changes when the numbers are real, not hypothetical. It doesn't: the same
    allocation gap holds across income levels and child counts as well as at my own figures.
  - >-
    The model behind every number on this page is
    <a href="/model/childcare_post_transfer.py"><code>model/childcare_post_transfer.py</code></a>,
    checked by <a href="/model/test_childcare_post_transfer.py">its test suite</a> against
    <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>, with
    <a href="/model/runs/childcare-post-transfer-run-2026-09-08.txt">the printed run</a> behind
    the table below.
rail_label: "On this page"
sections:
  - id: mechanism
    label: "The mechanism"
  - id: exhibits
    label: "Three ways to split it"
  - id: range
    label: "Across children and incomes"
  - id: method
    label: "Method: the full split table"
  - id: caveats
    label: "What this isn't"
  - id: check
    label: "Check it yourself"
---

{% include disclosure.html %}

<section class="hero" markdown="1">
<p class="eyebrow">Finding 2 of 4</p>

# Line 6b charges the payor 88 cents of every dollar of child care, using an income split base support has already moved

<p class="lede">At the worked example, the payor funds 88 cents of every dollar of the recipient's
$15,600-a-year child care claim. Massachusetts allocates child care in proportion to income; the
defect is that the Worksheet measures the share before the base support order moves a single
dollar between the two households, and never revisits it.</p>
</section>

<div class="numeral-pair numeral-pair--solo">
  <div class="numeral">
    <span class="numeral-value">88&cent;</span>
    <p class="numeral-caption">Of every dollar of the recipient's $15,600-a-year child care claim, funded by the payor at the worked example, on an income share measured before the order moves any money</p>
  </div>
</div>

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

<div class="page-shell" markdown="1">
{% include chapter-rail.html %}
<div class="content-col" markdown="1">

<section id="mechanism" markdown="1">

## Line 6b uses the income split from before the base order moved money between the households

Line 3c is each parent's share of combined available income, computed before the base support
amount at Line 7d exists. Line 6a is the child care one parent actually pays; Line 6b multiplies
the *other* parent's Line 3c share by that amount, so if the recipient pays the provider, the
payor's Line 6b charge is his Line 3c share of her cost. By the time child care is added at Line 6,
the base order has already moved a large share of the payor's income to the recipient's household,
but Line 6b never re-measures the shares against that transfer.

</section>

<section id="exhibits" markdown="1">

## The payor's share falls from 88 cents to 53 cents once the split is measured after the order and after tax

{% include figure.html
   id="e06"
   img="/figures/exhibits/E06-child-care-share-three-rules-worked-example.png"
   alt="Bar chart of the payor's share of a $15,600 annual child care claim under four allocation rules, at the worked example."
   title="The payor's share of a $15,600 child care bill, four ways to split it."
   deck="Line 3c allocates 87.7 percent to the payor on pre-transfer income shares."
   notes="The § 2 fallback, adjusting shares by the base order alone (Line 6b-2), gives 64.5 percent. The § 2 primary redline, measured net of tax on a withholding basis (Line 6b-1), gives 53.0 percent. Counting refundable tax credits as well gives 52.0 percent, kept as analysis, not asked for, because the Worksheet has no field for which parent claims which child."
   source_script="model/charts/fig2_childcare.py"
   csv_href="/figures/working/fig2_childcare_worked_example.csv"
   lazy="false" %}

</section>

<section id="range" markdown="1">

## The gap widens with the number of children, in both directions the money can move

The same pre-transfer-versus-post-transfer gap shows up whichever parent pays the provider. Three
exhibits below hold the arrangement fixed at $100 a week per child and vary only the number of
children.

{% include figure.html
   id="e20"
   img="/figures/exhibits/E20-child-care-funding-gap-1-child.png"
   alt="Line chart of the gap between the payor's pre-transfer income share and the share of child care he actually funds under two post-transfer rules, one child, across a range of income shares."
   title="With one child, post-transfer child care funds the payor 26 points below his income share."
   deck="Share of the child care bill the payor funds against his pre-transfer income share (Line 3c), one child, $100 a week paid by the lower earner, under two post-transfer rules."
   notes="The gap is measured at the highest income share plotted."
   source_script="model/charts/fig2_childcare.py"
   csv_href="/figures/working/fig2_childcare_rules.csv" %}

{% include figure.html
   id="e21"
   img="/figures/exhibits/E21-child-care-funding-gap-2-children.png"
   alt="Line chart of the gap between the payor's pre-transfer income share and the share of child care he actually funds under two post-transfer rules, two children, across a range of income shares."
   title="With two children, post-transfer child care funds the payor 36 points below his income share."
   deck="Same construction as the one-child exhibit, two children."
   notes="The gap widens with the number of children."
   source_script="model/charts/fig2_childcare.py"
   csv_href="/figures/working/fig2_childcare_rules.csv" %}

{% include figure.html
   id="e22"
   img="/figures/exhibits/E22-child-care-funding-gap-3-children.png"
   alt="Line chart of the gap between the payor's pre-transfer income share and the share of child care he actually funds under two post-transfer rules, three children, across a range of income shares."
   title="With three children, post-transfer child care funds the payor 43 points below his income share."
   deck="Same construction as the one- and two-child exhibits, three children, the worked example's own child count."
   notes="This is the worked example's own child count."
   source_script="model/charts/fig2_childcare.py"
   csv_href="/figures/working/fig2_childcare_rules.csv" %}

## When both parents pay for care, the payor still bears more of it than his income share

The same mechanism runs in the other direction, too, when both parents pay for care during their
own parenting time.

<div class="exhibit-pair">
{% include figure.html
   id="e25"
   img="/figures/exhibits/E25-both-pay-child-care-who-pays-3-children.png"
   alt="Stacked bar chart comparing the payor's share of combined gross income against his share of a combined child care bill, equal shared parenting, three children."
   title="The payor bears 93 percent of the combined child care while earning 87 percent of the gross income."
   deck="Each parent pays $300 a week during their own parenting time, the ordinary case at equal time."
   notes="Two stacked bars: share of combined gross income and share of the combined $31,200 child care bill."
   source_script="model/charts/fig8_both_pay.py"
   csv_href="/figures/working/fig8_both_pay.csv" %}

{% include figure.html
   id="e26"
   img="/figures/exhibits/E26-both-pay-child-care-net-position-3-children.png"
   alt="Bar chart comparing net income outcomes when both parents pay $300 a week of child care under equal shared parenting, three scenarios: neither pays, only the recipient pays, both pay."
   title="Both parents paying child care costs the payor $29,008 a year, the recipient household $2,192."
   deck="Each parent's net position under three scenarios: neither pays, only the recipient pays $300 a week, both pay $300 a week."
   notes="The Worksheet allocates the recipient's cost to the payor through Line 6b and passes the payor's own cost back through Line 6e at about two cents on the dollar, so his own $15,600 reduces the order by only $270 a year. Order plus his own child care reaches 58 percent of his net income while Line 7e reads 33 percent. Per person the payor still leads."
   source_script="model/charts/fig8_both_pay.py"
   csv_href="/figures/working/fig8_both_pay.csv" %}
</div>

</section>

<section id="method" markdown="1">

<details markdown="1">
<summary>Method: the full split table, four ways to measure the same $15,600 bill</summary>

| Basis for the split | Payor's share | Payor funds |
|---|---:|---:|
| Line 3c, pre-transfer (what the form does today) | 87.7% | $13,678/yr (order rises to $1,276/wk) |
| Shares adjusted by the base order (fallback redline at Line 6b-2, without a net computation) | 64.5% | $10,054/yr (order $1,206/wk, $3,624/yr less than today) |
| Post-transfer net shares, withholding basis (the redline proposed, Line 6b-1; order $1,172/wk, $5,415/yr less than today) | 53.0% | $8,263/yr |
| Post-transfer net shares counting refundable tax credits (analysis only, not proposed) | 52.0% | $8,118/yr |

(Source: `model/runs/childcare-post-transfer-run-2026-09-08.txt`, printed by
`model/childcare_post_transfer.py` (the 2026-09-05 run predates rule 5, the withholding-basis
figure this table quotes, and is kept alongside for the record); the order figures are from
`model/runs/submission-figures-run-2026-09-05.txt`.) Exhibits E25 and E26 above show the same
mechanism when both parents pay for care: Line 6e limits how much of the payor's own claim he can
recover once his income share puts him outside the low-income protection the line was written for.

The calculator on the home page reports the same 53.0 percent. Unlike the figures that count the
refundable credits, this one does not depend on the children's ages, so the site and the comments
print one number, not two.

</details>

</section>

<section id="caveats" markdown="1">

## What this isn't

<p class="caveat">Allocating child care in proportion to income is not, by itself, an unreasonable
rule. The objection here is to which income the proportion is measured against, not to
proportionality as a concept. $300 a week is a real but not extreme claim relative to the
$430-per-child statutory ceiling; a smaller claim moves the split by less, a larger one by more.
This is one worked example, and how far a typical claim sits from it is not known from anything in
this repository.</p>

<p class="caveat">Per person, the payor remains ahead. Even in the scenario where both parents pay
for care and he is charged 93 percent of the combined bill, he still holds $58,163 for himself
against $22,907 each for the recipient's household of four.</p>

</section>

<section id="check" markdown="1">

<div class="check-yourself">
<h2>Check it yourself</h2>
<ul>
  <li><strong><a href="/model/childcare_post_transfer.py"><code>model/childcare_post_transfer.py</code></a></strong>
    Computes all four allocation rules: pre-transfer, post-transfer gross adjusted by the base
    order, post-transfer net on a withholding basis, and post-transfer net counting refundable
    credits.</li>
  <li><strong><a href="/model/test_childcare_post_transfer.py">Its test suite</a></strong>
    Pins the 87.7%, 64.5%, 53.0%, 52.0%, and resulting order figures quoted above.</li>
  <li><strong><a href="/model/worksheet.py"><code>model/worksheet.py</code></a> and
    <a href="/model/test_worksheet.py"><code>model/test_worksheet.py</code></a></strong>
    The Line 6a/6b/6e implementation, including the test that the payor bears roughly 93 percent
    of combined child care when both parents pay for it under equal shared parenting.</li>
  <li><strong><a href="/model/runs/childcare-post-transfer-run-2026-09-08.txt">The printed runs</a></strong>
    Behind every figure above, alongside
    <a href="/model/runs/submission-figures-run-2026-09-05.txt">the base-order run</a>.</li>
</ul>
</div>

</section>

</div>
</div>
