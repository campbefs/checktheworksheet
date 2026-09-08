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
  47.4 percent of the payor's net; the presumption itself does not kick in until 57 percent of net.
  The fix changes what the form reports. It leaves every dollar amount untouched.
- **Allocate child care on the income split the order has already produced, instead of the split
  before it.** The new Line 6b-1 redline takes the payor's child care share from 87.7 percent to 64.5
  percent and the order from $1,275.77 to $1,206.08 a week. Part two below carries this further.
- **Apply the equal-parenting credit once, at the transfer, instead of clipping it as an entitlement.**
  Variant A takes the equal-time order from $1,012.73 to $935.06 a week, a 7.7 percent cut.

Nothing in this section changes the Worksheet's underlying schedule or its child-care ceiling. Every
figure is reproduced in the model files linked at the bottom of this page.

## What would put Massachusetts in line with other states

This part is analysis beyond what the comments ask for. It compares Massachusetts's Worksheet
against other states' schedules and against the child support recommendations Chris has made from
that comparison. Nothing here has been submitted to the Trial Court.

### The joint-custody discount should come from a cross-credit, using the factor other states use

**At equal parenting time, Massachusetts's order should fall to what a standard cross-credit
formula produces, using the 1.5 duplication factor twenty-three other states already use.**

At the worked example, today's equal-time order is $1,012.73 a week. A cross-credit at a 1.5
duplication factor puts it at $701.30 a week, a 30.8 percent cut. The monthly figure, $3,038.95,
sits 7.8 percent above Washington and 25.4 percent above California, the two comparably high cost
of living states, and 39.9 percent above the fifty-jurisdiction median. This is already what the
comments ask the Trial Court to adopt as Variant B, because it is what most states with a
cross-credit use, and because it is the one candidate that keeps working as the income gap widens
instead of collapsing the way today's credit does.

A simpler alternative is a straight linear discount on the time split: no discount at one night in
three, a 50 percent discount at half the time. This rule gives $543.95 a week, or $2,357.11 a month,
16.4 percent below Washington and 2.8 percent below California. The cross-credit stays the
recommendation, because this linear version prices Massachusetts below both comparison states
instead of in line with them.

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
   title="Massachusetts's equal-time order exceeds the primary-custody order of 47 of the 49 other ranked jurisdictions."
   deck="Monthly order: Massachusetts under Box 1 (children half the time each) against every other jurisdiction with the children primarily with the lower earner."
   notes="Only Hawaii and Wisconsin order more at primary custody than Massachusetts does at equal time. Massachusetts's own primary-custody order, $4,714, is marked for scale and isn't part of the ranked comparison. One fact pattern; Georgia held out."
   source_script="model/charts/fig10_ma_shared_vs_primary.py"
   csv_href="/figures/working/fig10_ma_shared_vs_primary.csv" %}

### Child care should be split on the income mix the order has already created

**Child care is allocated on the 87.7 percent income split that the order has already changed to
64.3 percent of gross and 48.2 percent of net.**

At the worked example, three children, $300 a week in child care paid by the recipient: the payor's
Line 3c income share before the order is 87.7 percent, and Line 6b charges him that share of the
$15,600 a year. But the order has already moved money between the households. After the transfer,
his share of the combined gross is 64.3 percent, and his share of combined net is 48.2 percent.
Child care is charged against the income split that no longer describes either household's actual
resources.

The recommended fix allocates child care on the post-transfer split. On post-transfer shares of
available income (Line 3a), the redline already in the comments (Line 6b-1), his share falls from 87.7 percent to 64.5 percent
and the order falls from $1,275.77 to $1,206.08 a week. The fuller version uses post-transfer net
shares, 48.2 percent, which the paper treats as the principled endpoint: the Worksheet cannot compute
it today because it holds no net-income figure anywhere in its calculation.

Two other options Chris raised are shown for comparison. Removing child care from the Worksheet
entirely returns the order to $1,012.73 a week and leaves the payor bearing 0 percent of the $15,600,
each parent covering only what they pay directly. Splitting child care 50-50 after base support is
computed leaves the base order unchanged and charges each parent $7,800 a year regardless of income.

| Rule | Weekly order | Payor's child care share | Payor's yearly child care |
|---|---|---|---|
| Current worksheet (pre-transfer Line 3c shares) | $1,275.77 | 87.7% | $13,678 |
| Removed from the worksheet entirely | $1,012.73 | 0.0% | $0 |
| Split 50-50 after base support | $1,012.73 | 50.0% | $7,800 |
| **Post-transfer shares of available income, Line 3a (Line 6b-1, recommended now)** | **$1,206.08** | **64.5%** | **$10,054** |
| Post-transfer net shares (principled endpoint, not computable today) | $1,012.73 | 48.2% | $7,513 |

The post-transfer net row uses the same $1,012.73 base order as the current rule and the two
Chris-proposed alternatives; only the child-care split changes across the table.

### The hardship test should be measured on the same income basis it is paid from

Section IV.C's presumption of substantial hardship does not kick in until the payor is at 57
percent of net income, even though Line 7e itself reports only 40 percent at that point. This is
the same units mismatch as Part one's first ask, stated here because it is the standing condition
the parenting-time and child care recommendations above operate under: a test that reads gross-derived
income cannot see a burden priced in net income, however either credit is redesigned. The comments
ask the Trial Court to measure the combined obligation, child support and child care together, on
the basis it is actually paid from.

## The numbers behind this page

Every figure above is printed by <a href="/model/recommendations.py"><code>model/recommendations.py</code></a>,
checked by <a href="/model/test_recommendations.py"><code>model/test_recommendations.py</code></a>,
and reproduced in the full run at
<a href="/model/runs/recommendations-run-2026-09-07.txt">model/runs/recommendations-run-2026-09-07.txt</a>.
The fifty-jurisdiction figures come from the same tiered dataset used throughout this site,
<a href="/data/fifty-state/tier-50-2026-09-05.json">tier-50-2026-09-05.json</a>; Washington and
California's own basis and income ceilings are in
<a href="/data/fifty-state/ceilings-2026-09-06.json">ceilings-2026-09-06.json</a>.

<div class="ask">
  <h2>Check it yourself</h2>
  <ul>
    <li><a href="/model/recommendations.py"><code>model/recommendations.py</code></a></li>
    <li><a href="/model/test_recommendations.py"><code>model/test_recommendations.py</code></a></li>
    <li><a href="/model/runs/recommendations-run-2026-09-07.txt">The full printed run</a></li>
    <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
  </ul>
</div>
