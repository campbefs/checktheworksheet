---
layout: page
title: Recommendations
permalink: /recommendations/
description: >-
  What the comments to the Trial Court ask for, and, going further, what would put
  Massachusetts's equal-time order in line with other states.
---

# What this project asks for, and what would put Massachusetts in line with other states

This page has two parts. Part one lists the redlines the comments actually ask the Trial Court to
adopt, each with its modelled effect. Part two goes beyond those comments to ask what a reform
matching other states would look like, using the same worked example throughout.

## What the comments ask the Trial Court to change

Three changes, each keyed to a Worksheet line, each with an effect measured at the worked example
($201,000 payor, $29,640 recipient, three children).

- **Measure the hardship test on the same income basis the order is paid from.** At $300 a week of
  claimed child care, Line 7e reads 33.4 percent of gross-derived income while the same order is
  47.4 percent of the payor's net; the presumption itself does not kick in until 56.9 percent of net.
  The fix changes what the form reports. It leaves every dollar amount untouched.
- **Allocate child care on the income split the order has already produced, instead of the split
  before it.** The lead redline measures that split net of tax, on a withholding basis (income tax
  and FICA for a single filer claiming no exemptions), taking the payor's child care share from
  87.7 percent to 53.0 percent and the order with $300 a week of child care from $1,275.77 to
  $1,171.64 a week, a $5,415-a-year change. Counting the refundable tax credits as well, under the
  alternating-year convention Box 1 now uses, would take the share to 49.7 percent; the comments
  stop short of that version, because the Worksheet has no
  field for which parent claims which child. A fallback confined to the Worksheet's existing
  gross-based lines, renumbered Line 6b-2, takes the share to 64.5 percent and the order to
  $1,206.08 a week. Part two below carries this further.
- **Apply the equal-parenting credit once, at the transfer, instead of clipping it as an entitlement.**
  Variant A takes the equal-time order from $1,012.73 to $935.06 a week, a 7.7 percent cut.

Nothing in this section changes the Worksheet's underlying schedule or its child-care ceiling. Every
figure is reproduced in the model files linked at the bottom of this page.

## What would put Massachusetts in line with other states

This part is analysis beyond what the comments ask for. It compares Massachusetts's Worksheet
against other states' schedules and against the child support recommendations the author has made
from that comparison.

### The joint-custody discount should come from a cross-credit, using the factor other states use

**At equal parenting time, Massachusetts's order should fall to what a standard cross-credit
formula produces, using the 1.5 duplication factor twenty-three other states already use.**

A cross-credit at a 1.5 duplication factor is already what the comments ask the Trial Court to
adopt as Variant B: it's what most states with a cross-credit use, and it's the one candidate that
keeps working as the income gap widens instead of collapsing the way today's credit does. It cuts
the order 30.8 percent, to a monthly figure 7.8 percent above Washington and 25.4 percent above
California, and 39.9 percent above the fifty-jurisdiction median.

A simpler alternative is a straight linear discount on the time split: no discount at one night in
three, a 50 percent discount at half the time, pricing Massachusetts 16.4 percent below Washington
and 2.8 percent below California. The cross-credit stays the recommendation, because the linear
version prices Massachusetts below both comparison states instead of in line with them.

| Rule | Weekly order | Monthly | Against the median | Against WA | Against CA |
|---|---|---|---|---|---|
| Today's Box 1 order (no credit redesign) | $1,012.73 | $4,388.48 | +102.0% | &mdash; | &mdash; |
| Variant A: 6e limitation moved to the transfer | $935.06 | $4,051.93 | +86.5% | +43.7% | +67.1% |
| **Cross-credit at duplication 1.5 (recommended)** | **$701.30** | **$3,038.95** | **+39.9%** | **+7.8%** | **+25.4%** |
| Linear discount at 50% of overnights | $543.95 | $2,357.11 | +8.5% | -16.4% | -2.8% |

"Against the median / WA / CA" states how far the candidate's monthly figure sits above or below
the fifty-jurisdiction median ($2,172.95), Washington's equal-time order ($2,819.56), and
California's equal-time order ($2,424.32). Today's Box 1 order's own distance from Washington and
California isn't printed by the model; its distance from the median (102.0 percent) is. Reaching
the median exactly would take a 50.5 percent cut to today's order, down to $511.27 a week.

{% include figure.html
   id="e08"
   img="/figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png"
   alt="Line chart of the percentage reduction in the order for equal parenting time versus the Box 2 order, against the payor's share of combined available income, for the current Worksheet and two redline variants."
   title="The Worksheet's credit for equal parenting time collapses as the income gap widens; a cross-credit narrows without collapsing."
   deck="Reduction in the order for equal time, against the Box 2 order (the paying parent has the children about a third of the time)."
   notes="The reduction falls from about 75 percent at a 57 percent payor income share to 7 percent at 88 percent and 1 percent at 96 percent: no parenting-time quantity enters any line. Variant A, applying Line 6e once, lifts the curve. Variant B, the standard cross-credit at a 1.5 duplication factor used by 23 states, stops it collapsing. Both are the letter's § 5 redlines."
   source_script="model/box1_fix.py"
   csv_href="/figures/working/fig3_credit_collapse.csv" %}

Today's uncredited equal-time order already sits above almost every state's primary-custody order,
which is the scale this recommendation is measured against.

{% include figure.html
   id="e17"
   img="/figures/exhibits/E17-ma-equal-time-vs-others-primary-custody.png"
   alt="Horizontal bar chart of Massachusetts's equal-time order against 49 other jurisdictions' primary-custody orders, with Massachusetts's own primary-custody order marked for scale."
   title="Only Wisconsin and Hawaii order more than Massachusetts does at equal time."
   deck="Monthly order: Massachusetts under Box 1 (children half the time each) against every other jurisdiction with the children primarily with the lower earner."
   notes="Only Hawaii and Wisconsin order more at primary custody than Massachusetts does at equal time. Massachusetts's own primary-custody order, $4,714, is marked for scale and isn't part of the ranked comparison. One fact pattern; Georgia held out."
   source_script="model/charts/fig10_ma_shared_vs_primary.py"
   csv_href="/figures/working/fig10_ma_shared_vs_primary.csv" %}

### Child care should be split on the income mix the order has already created

**Child care should be allocated on each parent's share of after-tax resources following the order,
instead of the 87.7 percent pre-order split the Worksheet uses today.**

At the worked example, three children, $300 a week in child care paid by the recipient: the payor's
Line 3c income share before the order is 87.7 percent, and Line 6b charges him that share of the
$15,600 a year. But the order has already moved money between the households: after the transfer,
his share of the combined gross is 64.3 percent, and on a withholding basis, income tax and FICA
for a single filer claiming no exemptions, his share of combined net is 53.0 percent.

The recommended fix, and now the comments' own lead redline, allocates child care on that
post-transfer net split, using new Worksheet Lines 6b-1a and 6b-1. It changes the order itself,
from $1,275.77 to $1,171.64 a week, because those lines sit inside the chain that produces Line
7d. The Worksheet holds no net-income figure today, so the comments also offer a fallback confined
to lines it already computes, renumbered Line 6b-2, which reaches 64.5 percent with no tax
computation at all.

Two other options the author raised are shown in the table below for comparison: removing child care
from the Worksheet entirely, so each parent bears 0 percent of the other's cost, and splitting it
50-50 after base support is computed, regardless of income.

| Rule | Weekly order | Payor's child care share | Payor's yearly child care |
|---|---|---|---|
| Current worksheet (pre-transfer Line 3c shares) | $1,275.77 | 87.7% | $13,678 |
| Post-transfer shares of available income, Line 3a (Line 6b-2, fallback without a net computation) | $1,206.08 | 64.5% | $10,054 |
| Removed from the worksheet entirely | $1,012.73 | 0.0% | $0 |
| Split 50-50 after base support | $1,012.73 | 50.0% | $7,800 |
| **Post-transfer net shares, withholding basis (recommended; the comments' lead redline, Line 6b-1)** | **$1,171.64** | **53.0%** | **$8,263** |

The recommended row changes the order itself, because the line it adds sits inside the chain that
produces the order. The two rows above it, which move the payment outside the worksheet, leave the
order at the no-child-care figure.

Counting the refundable credits as well, under the alternating-year Child Tax Credit convention
this model now uses (head-of-household status and the Earned Income Tax Credits stay with
whoever has the children more), puts the higher earner's share at 49.7 percent, not 53.0. The
comments ask for the narrower figure, because the worksheet has no field for which parent claims
which child and that claim is often alternated year to year.

### The hardship test should be measured on the same income basis it is paid from

Section IV.C's presumption of substantial hardship does not kick in until the payor is at 57 percent of net income,
even though Line 7e itself reports only 40 percent at that point. This is
the same units mismatch as Part one's first ask, stated here because it is the standing condition
the parenting-time and child care recommendations above operate under: a test that reads gross-derived
income cannot see a burden priced in net income, however either credit is redesigned. The comments
ask the Trial Court to measure the combined obligation, child support and child care together, on
the basis it is actually paid from.

**What would fix it: a ceiling, not a presumption.** A presumption has to be raised by a party,
argued, and decided, which costs more than it returns in most cases. A ceiling is arithmetic the
form performs. The Worksheet would gain one line: the order is the lesser of Line 7d and 40 percent
of the payor's net weekly income.

Forty percent is not a new number. It is the figure Section IV.C already names. The only change is
the quantity it is measured against, from Line 3a available income to net pay.

**What it would cost, measured on the same income grids as the rest of this site.** With one child
or two, a 40 percent ceiling changes nothing at all: no primary-custody order anywhere on either
grid reaches it. With three children it reaches 41.2 percent of the grid.
At the worked example the order falls 1.1 percent,
from $1,087.90 a week
down to $1,075.64. It is a backstop for the worst cases, not a rewrite of the schedule.

The number the backstop catches is worth stating on its own. At primary custody with no child care
at all, the worked example's order is 40.5 percent of the payor's net pay, past the point Section
IV.C itself calls substantial hardship, while Line 7e reports 28.5 percent.

That is not one unlucky family. Across the same three-child grid the rest of this site uses, the
order passes that threshold in 473
of 1,147 income combinations, and Line 7e passes it in none of them.

{% include figure.html
   id="e28"
   img="/figures/exhibits/E28-hardship-test-vs-share-of-net-3-children-primary.png"
   alt="Scatter plot of Line 7e against the order as a share of the payor's net pay, one point per income combination on the three-child primary-custody grid, with the 40 percent threshold marked on both axes."
   title="The order passes 40 percent of net pay in 473 of 1,147 income combinations"
   deck="The Worksheet's own hardship test flags none of them. Each dot is one pair of incomes."
   notes="Across is what Line 7e prints; up is what the order actually takes. Every point sits above the dashed diagonal because Line 7e divides by a gross-derived figure, and the widest gap on this grid is 13.0 percentage points. Net is the withholding basis: gross less federal income tax at the single filing status with the standard deduction, Social Security and Medicare, and Massachusetts income tax."
   source_script="model/charts/fig12_net_pay_ceiling.py"
   csv_href="/figures/working/fig12_net_pay_ceiling.csv" %}

The threshold here is not ours. It is Section IV.C's own figure, in the units the order is actually
paid from.

**A net ceiling is not a new idea, though no state applies one to the order.** Federal law already
caps what may be garnished for child support at 50 to 65 percent of a worker's disposable earnings,
under the Consumer Credit Protection Act: 50 percent where the payor supports another spouse or
child and 60 percent where he does not, each rising five points where the arrears are more than
twelve weeks old. That limits collection, not the order, so a court may enter an order larger than
may lawfully be withheld to satisfy it.

The definition behind those percentages matters more than the percentages do. 15 U.S.C. 1672(b)
defines disposable earnings as earnings less "any amounts required by law to be withheld", which is
the same measure this page uses and the same one the Commonwealth's own consultant builds in every
review. So a net figure for child support is not an untried idea needing a new methodology. Congress
wrote the definition, and every employer in the country applies it to an income withholding order
each payday. The Worksheet is the one place in the chain that does not hold the number. Oregon's 2024 guidelines review,
prepared by the Center for Policy Research, states the principle while explaining why Oregon's
schedule stops at six children: "It makes no sense to assess child support at percentages more than
can legally be held from a parent's paycheck." West Virginia uses 40 percent of weekly disposable
earnings as the trigger for a right to petition to restructure payments, though only for one narrow
group of parents.

The Massachusetts Guidelines, the economic review and the Task Force report mention the Consumer
Credit Protection Act zero times, and disposable earnings zero times.

### Both ceilings need one new number, and it fits in ten rows

A ceiling on net pay needs a net figure, and the Worksheet holds none. That is the real obstacle:
five reviews have taken up gross versus net and none changed it.

It does not require anyone to do their taxes. Net income on the withholding basis is a straight line
between a small number of breakpoints, so a conversion table takes the same shape Table A already
uses, a starting amount and a rate per bracket, in ten rows. A parent reads one row and multiplies
once. At the worked example, $3,865.38 of gross a week gives $2,689.11 net a week, and the table and
the model agree to within five cents a week anywhere on the schedule.

The conversion itself is not new to these Guidelines either. The economic review commissioned for
every cycle since at least 2013 converts gross to net exactly this way, using withholding tables and
standard Social Security and Medicare, because the study the schedule is calibrated against is
denominated in net. The table would publish the conversion the Commonwealth's own consultant already
performs and then sets aside.

## A lower ceiling at joint custody, which no state has yet

This part is a policy position, not a correction of an arithmetic error, and it is separated from
the two parts above for that reason. Nothing here is asked of the Trial Court in the comments.

### Equal parenting time should carry a lower ceiling than primary custody

Where the children are with each parent about half the time, both households carry the fixed cost of
housing them, a bedroom in each home kept year round. Every income-shares state that credits shared
parenting through a cross-credit recognises this: 23 states apply a 1.5 duplication factor, and
Indiana's Guideline 6 Commentary puts the duplicated share of the basic obligation at 50 percent.
The Massachusetts Worksheet contains no parenting-time quantity in any line, so its credit for equal
time is only the difference in income shares, and it collapses as the income gap widens.

The position: at equal time the order should not exceed 25 percent of the payor's net pay, against
40 percent at primary custody.

**No state does this, and that should be said first.** The fifty-one jurisdiction corpus behind this
site contains no state that caps a support order at a share of net income as a general rule. The
support for a ceiling in principle, the federal garnishment cap and the Center for Policy Research
statement quoted in part two, is support for the idea of a net ceiling, not for this number.

**What it would cost, and it is not a backstop.** A 25 percent ceiling reaches 9.6 percent of
one-child equal-time orders on the published grid, 48.2 percent of two-child orders,
and 62.2 percent of three-child orders.
At the worked example it would take the order from $1,012.73 a week
down to $672.28. That is a different schedule for shared custody, and it should be argued as one.

**Where it bites is the argument for it.** The share of net an order takes is driven by the gap
between the two incomes, not by either income alone. Holding the higher earner at $201,000 with
three children at equal time, the ceiling binds while the other parent earns under about $85,000 and
stops binding above it. That is the same region where the equal-time credit collapses from 75
percent of the primary-custody order to under 7 percent. The ceiling reaches the cases the Worksheet
already handles worst.

## The numbers behind this page

Every figure above is printed by <a href="/model/recommendations.py"><code>model/recommendations.py</code></a>,
checked by <a href="/model/test_recommendations.py"><code>model/test_recommendations.py</code></a>,
and reproduced in the full run at
<a href="/model/runs/recommendations-run-2026-09-09.txt">model/runs/recommendations-run-2026-09-09.txt</a>.
The fifty-jurisdiction figures come from the same tiered dataset used throughout this site,
<a href="/data/fifty-state/tier-50-2026-09-05.json">tier-50-2026-09-05.json</a>; Washington and
California's own basis and income ceilings are in
<a href="/data/fifty-state/ceilings-2026-09-06.json">ceilings-2026-09-06.json</a>.

<div class="ask">
  <h2>Check it yourself</h2>
  <ul>
    <li><a href="/model/recommendations.py"><code>model/recommendations.py</code></a></li>
    <li><a href="/model/test_recommendations.py"><code>model/test_recommendations.py</code></a></li>
    <li><a href="/model/runs/recommendations-run-2026-09-09.txt">The full printed run</a></li>
    <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
  </ul>
</div>
