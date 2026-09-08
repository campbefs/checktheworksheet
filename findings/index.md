---
layout: page
title: Findings
description: >-
  Three places where the Massachusetts Child Support Guidelines Worksheet's own arithmetic works
  against its own text, each pinned by a test suite against the form's own calculation scripts,
  plus one fifty-one-jurisdiction comparison at a single fact pattern.
disclosure:
  - >-
    The stat on each card below (57%, 88 cents, 6.9%, 47 of 49) comes from the worked example
    used throughout this site: my own child support order, three children, my income and my
    children's mother's income entered as the Worksheet requires. Each finding page states why,
    and shows the same gap holding across a range of incomes as well as at my own figures.
  - >-
    Every number traces to <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>,
    checked by <a href="/model/test_worksheet.py"><code>model/test_worksheet.py</code></a>
    against the form's own calculation scripts. More on <a href="/about/">About</a>.
---

# Six measurable effects in the worksheet's own arithmetic, ranked by how much each one changes the outcome

{% include disclosure.html %}

Each finding below traces to a script in this repository, or for the fourth, to the guidelines'
own text on deviation. They run in the order that each one changes what a family actually pays or
keeps, the most consequential first.

## 1. The payor funds 88 cents of every dollar of child care on an income split the order has already moved

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

Line 6b splits a child care claim by each parent's Line 3c income share, which is computed before
Line 7d's base support order transfers any money between the two households. At the worked example
that charges the payor 87.7 percent of a $15,600-a-year claim. Measuring the same split after the
base order moves money gives 64.5 percent. After tax as well, it is 48.2 percent. Line 6b never
looks back.

{% include figure.html
   id="e06"
   img="/figures/exhibits/E06-child-care-share-three-rules-worked-example.png"
   alt="Bar chart of the payor's share of a $15,600 annual child care claim under three allocation rules, at the worked example."
   title="The payor's share of a $15,600 child care bill, three ways to split it."
   deck="Line 3c allocates 87.7 percent to the payor on pre-transfer income shares."
   notes="Adjusting the shares by the base order, the letter's § 2 redline, gives 64.5 percent. Post-transfer net shares give 48.2 percent. The middle bar is the redline; the right bar is where the argument goes once net income is admitted."
   source_script="model/charts/fig2_childcare.py"
   csv_href="/figures/working/fig2_childcare_worked_example.csv"
   lazy="false" %}

[Read the full finding →](/findings/child-care/)

## 2. Equal parenting time earns a 6.9 percent discount, and it shrinks as the income gap widens

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

Line 6g nets the two parents' Line 6e amounts, which reduce to the gap between their income shares
once Box 1 puts zero children in the payor's column. No line multiplies by any share of overnights.
Moving from about a third of the parenting time to half lowers the order 6.9 percent at this
family's income gap; at a narrower gap the same move lowers it 77.6 percent. A wider income gap
buys a payor less credit for the same equal time. Research on custody decided mainly by a financial
incentive, separate from a family's actual circumstances, finds children can fare worse under it
(Fernandez-Kranz et al. 2021). That is an argument against pricing parenting time by formula at all.

{% include figure.html
   id="e08"
   img="/figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png"
   alt="Line chart of the Box 1 order's percentage reduction from the primary-custody order, across the payor's share of combined income, for the current Worksheet and two redlined variants, three children."
   title="The Worksheet's credit for equal parenting time collapses as the income gap widens; a cross-credit narrows without collapsing."
   deck="The discount for equal time, against the primary-custody order, falls from about 75 percent at a 57 percent payor income share to 7 percent at 88 percent and 1 percent at 96 percent, because no parenting-time quantity enters any line."
   notes="Variant A, applying Line 6e once, raises the discount to 14.0 percent. Variant B, the cross-credit design 23 states use at a 1.5 duplication factor, raises it to 35.5 percent and stops it collapsing."
   source_script="model/box1_fix.py · model/charts/fig3_credit.py"
   csv_href="/figures/working/fig3_credit_collapse.csv" %}

[Read the full finding →](/findings/parenting-time/)

## 3. The payor keeps 48 cents of the next dollar he earns

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

Of the next $10,000 the payor earns at $201,000, 20.3 percent goes to the increase in the order.
Another 31.3 percent goes to income and payroll tax combined. He keeps 48.3 percent. The order's
marginal share runs above Table A's own 10 percent top bracket, because both the child-count
multiplier and the payor's rising income share scale up with income. Run from $150,000 to $300,000
of payor income, the same computation keeps his retention between 39 and 48 percent throughout.

{% include figure.html
   id="e10"
   img="/figures/exhibits/E10-cents-kept-of-next-dollar-worked-example.png"
   alt="Line chart of cents kept of the payor's next dollar of income, from $100,000 to $400,000 of payor income, both with and without $300 a week of child care."
   title="Of the payor's next dollar, the payor keeps between a third and a half."
   deck="Marginal retention after federal and state tax and the change in the order."
   notes="The order's marginal take runs near 20 percent, above Table A's 10 percent top bracket, because the child-count multiplier and the rising income share both scale with the payor's income. $5,000 steps. Dashed line: 50 cents. Two of three children under 13 (MA credit); premiums $43/$33."
   source_script="model/charts/fig4_retention.py · model/marginal_retention.py"
   csv_href="/figures/working/fig4_marginal_retention.csv" %}

## 4. Rebutting the presumptive order takes four written findings, which can cost more than the amount in dispute

<p class="confidence-tag">The deviation data is the Commonwealth's own; the rate at which a contested deviation succeeds is not measured anywhere in it.</p>

Federal law requires the guidelines amount to carry a rebuttable presumption, and Massachusetts's
own guidelines make rebutting it conditional on a judge making four specific findings: the
guidelines amount, that applying it would be unjust or inappropriate, the facts justifying
departure, and that departure is consistent with the child's best interest. Meeting that bar costs
legal time, so contesting a child care claim or a parenting-time credit worth a few thousand
dollars a year can cost more than the amount actually in dispute. The Commonwealth publishes how
often the presumption is rebutted. It does not publish the one number that would say whether
contesting is worth attempting: how often a deviation motion the parties did not simply agree to
still succeeds.

## 5. After tax and the order, the recipient household holds $93,821 to the payor's $87,172, though the payor still holds more per person

<p class="confidence-tag">Verified against the form's own calculation scripts</p>

At the worked example, with no child care claimed, the payor's income after tax and after the
order comes to $87,172 a year. The recipient's household, after tax and after receiving the order,
comes to $93,821. Divided across household size, the payor still holds more for himself than the
recipient's household holds per person, $87,172 for one against $23,455 each for four. Both figures
are true at once; which one answers a reader's question depends on whether the question is about
the household or about the person in it.

{% include figure.html
   id="e01"
   img="/figures/exhibits/E01-who-holds-more-3-children.png"
   alt="Heatmap of the recipient household's net income minus the payor's, in dollars per year, across combinations of higher-earner gross income from $60,000 to $300,000 and lower-earner gross income from $0 to $120,000, three children, equal parenting time, no child care."
   title="With three children, the recipient household holds more after the order in 55 percent of income combinations."
   deck="Recipient household net minus payor net, per year."
   notes="The recipient household is ahead in 96 percent of the grid below $150,000 of higher-earner income, and nowhere above $230,000. The closed contour inside the red region is Line 6e's limitation, which stops binding once the payor's Line 6d crosses 10 percent; the order then drops about $110 a week in one step. Per person the payor still leads almost everywhere (E02). Masked where the lower earner would out-earn the higher. Premiums $43/$33 a week; MA under-13 credit set to zero."
   source_script="model/charts/fig1_heatmaps.py · model/worksheet.py · model/net_position.py"
   csv_href="/figures/working/fig1_heatmap_3child_box1.csv" %}

## 6. Massachusetts's equal-time order exceeds 47 of the other 49 ranked jurisdictions' primary-custody orders

<p class="confidence-tag">Tiered: a single fact pattern; see method</p>

Fifty jurisdictions were profiled from their own primary documents at one fact pattern, computed
twice independently and reconciled, then checked against an adversarial attack. Massachusetts
orders more under equal parenting time than any of them, and more under primary custody than every
one of them but Hawaii. Its own equal-time order exceeds the primary-custody order of 47 of the
other 49 ranked jurisdictions. Georgia was held out: its enacted formula orders less at equal time
than at primary custody. The ranking says nothing beyond this one fact pattern.

{% include figure.html
   id="e11"
   img="/figures/exhibits/E11-fifty-states-equal-parenting-one-fact-pattern.png"
   alt="Horizontal bar chart of the monthly child support order in fifty jurisdictions under equal parenting time, one fact pattern, Massachusetts highlighted."
   title="Equal parenting time: Massachusetts orders the most of fifty jurisdictions."
   deck="Monthly order at one fact pattern. Georgia held out."
   notes="Fifty of fifty-one jurisdictions survived every verification stage; Georgia is held out because its enacted formula produces a lower order under primary custody than under equal time, which the state's own calculator reproduces. Each row was profiled from primary sources, computed twice blind, reconciled, and attacked. Own premiums ($43/$33) as each state treats them. One fact pattern; the ranking generalizes to nothing else."
   source_script="model/charts/fig5_states.py"
   csv_href="/figures/working/fig5_states.csv" %}

[Read the full finding →](/findings/fifty-one-jurisdictions/)

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every number above traces to a script and a printed run in this repository. See
  <a href="/the-model/">the model</a> and <a href="/the-data/">the data</a> for the full list, or
  each finding's own "Check it yourself" section for the exact file behind its numbers.</p>
</div>
