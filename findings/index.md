---
layout: page
title: Findings
description: >-
  The Massachusetts child support guidelines do not comply with federal law: the Worksheet never
  measures ability to pay and, with child care claimed, sets orders the Commonwealth cannot
  lawfully collect. Seven more problems follow, each pinned to the form's own calculation scripts.
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

# Eight problems with the Massachusetts child support guidelines, and the first is that they do not comply with federal law

{% include disclosure.html %}

Each one traces to a script in this repository, or, for the seventh, to the guidelines' own text
on deviation. Biggest first.

## 1. The Massachusetts child support guidelines do not comply with federal law

<p class="confidence-tag">Every income pair run through the Worksheet's own arithmetic</p>

**While federal law requires every order to rest on the parent's ability to pay, the Worksheet
never computes what a parent keeps after tax. With child care claimed, it sets orders above the
federal withholding ceiling, amounts the Commonwealth cannot lawfully collect.**

Federal rules require a state's guidelines to base the order on the parent's "earnings, income,
and other evidence of ability to pay," 45 C.F.R. § 302.56(c)(1), and the Massachusetts Guidelines
recite that standard. The Worksheet has no line for tax or take-home pay. At $100 a week of child
care claimed per child, three children and primary custody, 40% of income pairs produce an order
above the federal withholding ceiling, 50 percent of take-home pay, 15 U.S.C. § 1673(b)(2). With no
child care claimed, none do.

{% include figure.html
   id="e31"
   img="/figures/exhibits/E31-income-pairs-over-ceiling-grid.png"
   alt="Grid of 1,147 income pairs, payor income across and other parent's income up, shaded where the order at $100 of child care per child is over the federal ceiling."
   title="At $100 a child, 40 percent of income pairs produce an order over the federal ceiling."
   deck="Each square is one pair of incomes: the Worksheet's order with $300 a week of child care claimed for three children, primary custody."
   notes="Dark squares are over both federal ceilings (60 percent); light squares are over the 50 percent ceiling that applies to a payor with a second family. Hatched squares are pairs where the other parent would be the higher earner."
   source_script="model/ccpa_grid.py"
   csv_href="/figures/working/fig_ceiling_grid.csv"
   lazy="false" %}

[Read the full finding →](/findings/federal-law/)

## 2. The payor funds 88 cents of every dollar of child care, on money the order has already moved to the other parent

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
   %}

[Read the full finding →](/findings/child-care/)

## 3. Splitting the children's time equally cuts the order by 6.9%. Utah cuts it by 55%, Montana and Hawaii by 52%

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

**Taking the children half the nights instead of a third of them is worth 6.9% off the order. At
the same two incomes, the states that give the largest reductions give more than half.**

Line 6g nets the two parents' Line 6e amounts, which reduce to the gap between their income shares
once Box 1 (equal parenting time) puts zero children in the payor's column; no line measures overnights. That gap shrinks
the discount from 77.6 percent at a narrower income share to 6.9 percent at this family's. Research
on custody decided mainly by a financial incentive finds children can fare worse under it
(Fernández-Kranz, Roff and Sun, *Journal of Economic Behavior & Organization* 189 (2021)), an argument against pricing parenting time by formula in
either direction, whether a credit shrinks or grows. The
<a href="/recommendations/">recommendations</a> page's proposal for a larger credit is not exempt
from that caution.

{% include figure.html
   id="e08"
   img="/figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png"
   alt="Line chart of the Box 1 order's percentage reduction from the primary-custody order, across the payor's share of combined income, for the current Worksheet and two redlined variants, three children."
   title="The Worksheet's equal-time credit collapses as the income gap widens."
   deck="The discount for equal time, against the primary-custody order, falls from about 75 percent at a 57 percent payor income share to 7 percent at 88 percent and 1 percent at 96 percent, because no parenting-time quantity enters any line."
   notes="Variant A, applying Line 6e once, raises the discount to 14.0 percent. Variant B, the cross-credit design 18 states and DC use at a 1.5 duplication factor, raises it to 35.5 percent and stops it collapsing."
   source_script="model/box1_fix.py · model/charts/fig3_credit.py"
   csv_href="/figures/working/fig3_credit_collapse.csv" %}

[Read the full finding →](/findings/parenting-time/) · [The formula most states use instead →](/findings/shared-parenting-formula/)

## 4. Massachusetts charges more for joint custody than 47 states charge when the recipient has primary custody

<p class="confidence-tag">One set of incomes, fifty states. <a href="/findings/fifty-one-jurisdictions/">How each state was checked</a></p>

Massachusetts orders more under equal parenting time than any of the fifty states modeled, and
more under primary custody than every one of them but Hawaii. Its joint-custody order is higher
than the primary-custody order in 47 states. Only Hawaii and Wisconsin's primary-custody orders
are higher than Massachusetts's joint-custody order. Georgia is held out: its enacted formula
orders less at equal time than at primary custody.

{% include figure.html
      id="e17"
   img="/figures/exhibits/E17-ma-equal-time-vs-others-primary-custody.png"
   alt="Bar chart of Massachusetts's equal-time order against 49 other jurisdictions' primary-custody orders, Massachusetts highlighted, its own primary-custody order marked for scale."
   title="At primary custody, only Wisconsin and Hawaii order more than Massachusetts does at equal time."
   deck="Monthly order: Massachusetts at equal time against every other state with the children primarily with the lower earner. Georgia held out."
   notes="Fifty of fifty-one jurisdictions passed every check; Georgia is held out because its enacted formula produces a lower order under primary custody than under equal time, which the state's own calculator reproduces. Each state's amount comes from its own guidelines, worked out twice and checked for errors. Own premiums ($43/$33) as each state treats them. One worked example; the ranking generalizes to nothing else."
      source_script="model/charts/fig10_ma_shared_vs_primary.py"
   csv_href="/figures/working/fig10_ma_shared_vs_primary.csv" %}

[Read the full finding →](/findings/fifty-one-jurisdictions/) · [Why cost of living does not explain it →](/findings/cost-of-living/)

## 5. The hardship test measures gross income when it should measure net

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

**The hardship presumption is supposed to fire at 40% of the payor's income. It does not fire
until the order takes 57% of the payor's net pay.**

Section IV.C calls an order at 40% of income a presumptive hardship, and Line 7e is the box on the
Worksheet that tests for it. But Line 7e divides by Line 3a, which is gross income less health
premiums and any other support orders and carries no tax adjustment at all, while the order is
paid out of net. The test is in gross, the payment is in net, and the gap between them widens as
the payor's tax rate rises. At the worked example that gap is 17 points.

[Read the full finding →](/findings/hardship-test/)

## 6. The payor keeps less than half of every extra dollar earned

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

## 7. Challenging the order can cost more than it saves, so wrong orders go uncontested

<p class="confidence-tag">The deviation rate is the Commonwealth's own figure. How often a contested deviation succeeds is not published.</p>

Federal law requires the guidelines amount to carry a rebuttable presumption. Massachusetts's own
guidelines make rebutting it conditional on a judge making four specific findings: the guidelines
amount, that applying it would be unjust or inappropriate, the facts justifying departure, and that
departure is consistent with the child's best interest. Meeting that bar takes a lawyer, and a
lawyer costs more than a child care claim or a parenting-time credit is usually worth.

So the right exists and cannot be exercised.

The Commonwealth publishes how often the presumption is rebutted. It does not publish the one
number that would tell a parent whether contesting is worth it: how often a deviation motion the
parties did not simply agree to still succeeds.

## 8. At equal parenting time, the recipient household ends up with more money than the payor in 10% of income combinations

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

Across the three-child equal-time grid (Box 1, the Worksheet's equal-time calculation), the recipient's household ends up holding more money than
the payor in 9.9% (114 of 1,147) of income combinations. In every one of those 114 the payor still
holds more per person, because that household is supporting four people and the payor one
(E01, E02).

At this site's own worked example the payor is the one ahead, keeping $87,172 a year
against the recipient household's $77,395,
which is $19,349 each for the four people in it.

Both figures take out federal and Massachusetts income tax, Social Security and Medicare, and
count no refundable credits. A credit turns on which parent claims which child in a given year,
which CJ-D 304 does not collect and a reader cannot reproduce from published rate tables.

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
