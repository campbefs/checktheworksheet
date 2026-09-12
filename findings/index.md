---
layout: page
title: Findings
description: >-
  Three places where the Massachusetts Child Support Guidelines Worksheet's own arithmetic works
  against its own text, each pinned by a test suite against the form's own calculation scripts,
  plus one fifty-one-jurisdiction comparison at a single fact pattern.
disclosure:
  - >-
    The figures below (88 cents, 6.9%, 57%, 48%) come from the worked example used throughout this
    site: three children, the payor's income and the other parent's income entered as the
    Worksheet requires. They are Worksheet figures from a real Massachusetts case, and neither is
    either parent's current income. I pay child support in Massachusetts myself, so I have a stake
    in the outcome. Each finding page shows the same gap holding across a range of incomes as
    well as at this example's figures.
  - >-
    Every number traces to <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>,
    checked by <a href="/model/test_worksheet.py"><code>model/test_worksheet.py</code></a>
    against the form's own calculation scripts. More on <a href="/about/">About</a>.
---

# Seven problems with the Massachusetts child support guidelines

{% include disclosure.html %}

Each one traces to a script in this repository, or, for the sixth, to the guidelines' own text
on deviation. Biggest first.

## 1. The payor funds 88 cents of every dollar of child care, on money the order has already moved to the other parent

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

Line 6b splits a child care claim by each parent's Line 3c income share, computed before Line 7d's
base support order moves any money between the households, and never revisits the split
afterward.

{% include figure.html
   id="e06"
   img="/figures/exhibits/E06-child-care-share-three-rules-worked-example.png"
   alt="Bar chart of the payor's share of a $15,600 annual child care claim under three allocation rules, at the worked example."
   title="The payor's share of a $15,600 child care bill, three ways to split it."
   deck="Line 3c allocates 87.7 percent to the payor on pre-transfer income shares."
   notes="Adjusting the shares by the base order alone, the fallback confined to the Worksheet's existing gross-based lines (Line 6b-2), gives 64.5 percent. The letter's current § 2 redline, measured net of tax on a withholding basis (Line 6b-1), gives 53.0 percent."
   source_script="model/charts/fig2_childcare.py"
   csv_href="/figures/working/fig2_childcare_worked_example.csv"
   lazy="false" %}

[Read the full finding →](/findings/child-care/)

## 2. Splitting the children's time equally cuts the order by 6.9%. Utah cuts it by 55%, Montana and Hawaii by 52%

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

**Taking the children half the nights instead of a third of them is worth 6.9% off the order. At
the same two incomes, the states that give the largest reductions give more than half.**

Line 6g nets the two parents' Line 6e amounts, which reduce to the gap between their income shares
once Box 1 puts zero children in the payor's column; no line measures overnights. That gap shrinks
the discount from 77.6 percent at a narrower income share to 6.9 percent at this family's. Research
on custody decided mainly by a financial incentive finds children can fare worse under it
(Fernandez-Kranz, Roff and Sun 2021), an argument against pricing parenting time by formula in
either direction, whether a credit shrinks or grows. The
<a href="/recommendations/">recommendations</a> page's proposal for a larger credit is not exempt
from that caution.

{% include figure.html
   id="e08"
   img="/figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png"
   alt="Line chart of the Box 1 order's percentage reduction from the primary-custody order, across the payor's share of combined income, for the current Worksheet and two redlined variants, three children."
   title="The Worksheet's equal-time credit collapses as the income gap widens."
   deck="The discount for equal time, against the primary-custody order, falls from about 75 percent at a 57 percent payor income share to 7 percent at 88 percent and 1 percent at 96 percent, because no parenting-time quantity enters any line."
   notes="Variant A, applying Line 6e once, raises the discount to 14.0 percent. Variant B, the cross-credit design 23 states use at a 1.5 duplication factor, raises it to 35.5 percent and stops it collapsing."
   source_script="model/box1_fix.py · model/charts/fig3_credit.py"
   csv_href="/figures/working/fig3_credit_collapse.csv" %}

[Read the full finding →](/findings/parenting-time/)

## 3. Massachusetts charges more for joint custody than 47 states charge when the recipient has primary custody

<p class="confidence-tag">Tiered: a single fact pattern; see method</p>

Massachusetts orders more under equal parenting time than any of the fifty states modeled, and
more under primary custody than every one of them but Hawaii. Its joint-custody order is higher
than what 47 states charge a parent whose children live mainly with the other parent; only Hawaii
and Wisconsin charge more. Georgia is held out: its enacted formula orders less at equal time than
at primary custody.

{% include figure.html
   id="e11"
   img="/figures/exhibits/E11-fifty-states-equal-parenting-one-fact-pattern.png"
   alt="Horizontal bar chart of the monthly child support order in fifty states under equal parenting time, one fact pattern, Massachusetts highlighted."
   title="At equal parenting time, Massachusetts orders the most of the fifty states."
   deck="Monthly order at one fact pattern. Georgia held out."
   notes="Fifty of fifty-one jurisdictions survived every verification stage; Georgia is held out because its enacted formula produces a lower order under primary custody than under equal time, which the state's own calculator reproduces. Each row was profiled from primary sources, computed twice blind, reconciled, and attacked. Own premiums ($43/$33) as each state treats them. One fact pattern; the ranking generalizes to nothing else."
   source_script="model/charts/fig5_states.py"
   csv_href="/figures/working/fig5_states.csv" %}

[Read the full finding →](/findings/fifty-one-jurisdictions/)

## 4. The hardship test measures gross income when it should measure net

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

**The hardship presumption is supposed to fire at 40% of the payor's income. It does not fire
until the order takes 57% of the payor's net pay.**

Section IV.C calls an order at 40% of income a presumptive hardship, and Line 7e is the box on the
Worksheet that tests for it. But Line 7e divides by Line 3a, which is gross income less health
premiums and any other support orders and carries no tax adjustment at all, while the order is
paid out of net. The test is in gross, the payment is in net, and the gap between them widens as
the payor's tax rate rises. At the worked example that gap is 17 points.

[Read the full finding →](/findings/hardship-test/)

## 5. The payor keeps less than half of every extra dollar earned

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

At $201,000, of the next $10,000 the payor earns, 20.3% goes to the order and 31.3% to income and
payroll tax. The payor keeps 48.3%. The order's share of a raise is roughly double Table A's own
10% top bracket, because the child-count multiplier and the payor's rising income share both scale
up with income. Across $150,000 to $300,000 of payor income the share kept stays between 39% and
48%, so the effect is not particular to this example.

{% include figure.html
   id="e10"
   img="/figures/exhibits/E10-cents-kept-of-next-dollar-worked-example.png"
   alt="Line chart of cents kept of the payor's next dollar of income, from $100,000 to $400,000 of payor income, both with and without $300 a week of child care."
   title="Of the payor's next dollar, the payor keeps between a third and a half."
   deck="Marginal retention after federal and state tax and the change in the order."
   notes="The order's marginal take runs near 20 percent, above Table A's 10 percent top bracket, because the child-count multiplier and the rising income share both scale with the payor's income. $5,000 steps. Dashed line: 50 cents. Two of three children under 13 (MA credit); premiums $43/$33."
   source_script="model/charts/fig4_retention.py · model/marginal_retention.py"
   csv_href="/figures/working/fig4_marginal_retention.csv" %}

## 6. Challenging the order can cost more than it saves, so wrong orders go uncontested

<p class="confidence-tag">The deviation data is the Commonwealth's own; the rate at which a contested deviation succeeds is not measured anywhere in it.</p>

Federal law requires the guidelines amount to carry a rebuttable presumption, and Massachusetts's
own guidelines make rebutting it conditional on a judge making four specific findings: the
guidelines amount, that applying it would be unjust or inappropriate, the facts justifying
departure, and that departure is consistent with the child's best interest. Meeting that bar costs
legal time, so contesting a child care claim or a parenting-time credit worth a few thousand
dollars a year can cost more than the amount in dispute. The Commonwealth publishes how often the
presumption is rebutted, but not the one number that would say whether contesting is worth it: how
often a deviation motion the parties did not simply agree to still succeeds.

## 7. At equal parenting time, the recipient household ends up with more money than the payor in 10% of income combinations

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

Across the three-child equal-time grid, the recipient's household ends up holding more money than
the payor in about 10% of income combinations. The payor still holds more per person in
99% of them, because that household is supporting four people and the payor one (E01, E02).

At this site's own worked example the payor is the one ahead, keeping $87,172 a year
against the recipient household's $77,395,
which is $19,349 each for the four people in it.

Both figures come from the withholding basis — federal and Massachusetts income tax, Social
Security and Medicare, no refundable credits — because a figure that turns on which parent claims
which child in a given year is not something CJ-D 304 collects or a reader can reproduce from
published rate tables.

{% include figure.html
   id="e01"
   img="/figures/exhibits/E01-who-holds-more-3-children.png"
   alt="Heatmap of the recipient household's net income minus the payor's, in dollars per year, across combinations of higher-earner gross income from $60,000 to $300,000 and lower-earner gross income from $0 to $120,000, three children, equal parenting time, no child care."
   title="With three children, the recipient household holds more after the order in 10 percent of income combinations."
   deck="Recipient household net minus payor net, per year."
   notes="Of the 10 percent of the grid where the recipient household is ahead, 75 percent sits below $150,000 of higher-earner income, and none above $175,000. The closed contour inside the red region is Line 6e's limitation, which stops binding once the payor's Line 6d crosses 10 percent; the order then drops about $110 a week in one step. Per person the payor still leads almost everywhere (E02). Masked where the lower earner would out-earn the higher. Premiums $43/$33 a week; MA under-13 credit set to zero; no refundable tax credits counted."
   source_script="model/charts/fig1_heatmaps.py · model/worksheet.py · model/net_position.py"
   csv_href="/figures/working/fig1_heatmap_3child_box1.csv" %}

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every number above traces to a script and a printed run in this repository: see
  <a href="/the-model/">the model</a> and <a href="/the-data/">the data</a>, or each finding's own
  "Check it yourself" section for the exact file.</p>
</div>
