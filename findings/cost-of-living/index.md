---
layout: finding
title: Massachusetts does not order more because it costs more to live here
permalink: /findings/cost-of-living/
description: >-
  Six places cost more to live in than Massachusetts, and every one of them orders less child
  support at equal parenting time for the same family. Massachusetts at equal time charges more
  than five of the six charge when one parent has the children full time.
disclosure:
  - >-
    I pay child support in Massachusetts myself, so I have a stake in the outcome. Every order on
    this page is for the same family in every state: two incomes of $201,000 and $29,640 a year,
    three children and no child care, the worked example used across this site.
  - >-
    Cost-of-living figures are the U.S. Bureau of Economic Analysis's Regional Price Parities for 2024, all
    items, in <a href="/data/bea/SARPP_STATE_2008_2024.csv"><code>data/bea/SARPP_STATE_2008_2024.csv</code></a>.
    The join is <a href="/model/cost_of_living.py"><code>model/cost_of_living.py</code></a>, checked
    by <a href="/model/test_cost_of_living.py"><code>model/test_cost_of_living.py</code></a>.
rail_label: "On this page"
sections:
  - id: costlier
    label: "The costlier places"
  - id: primary
    label: "Against primary custody"
  - id: all-states
    label: "All fifty"
  - id: limits
    label: "Limits"
  - id: check
    label: "Check it yourself"
---

<section class="hero" markdown="1">
<p class="eyebrow">Cost of living</p>

# Massachusetts does not order more because it costs more to live here

<p class="lede">While Massachusetts is an expensive state, six places cost more to live in, and
every one of them orders less child support for the same family at equal parenting time. Five of
the six order less even when one parent has the children full time.</p>
</section>

<div class="numeral-pair numeral-pair--solo">
  <div class="numeral">
    <span class="numeral-value">6 of 6</span>
    <p class="numeral-caption">Places that cost more to live in than Massachusetts and order less child support at equal parenting time</p>
  </div>
</div>

<p class="confidence-tag">The same two incomes and three children, in every state</p>

{% include disclosure.html %}

<div class="page-shell" markdown="1">
{% include chapter-rail.html %}
<div class="content-col" markdown="1">

<section id="costlier" markdown="1">

## Every place that costs more to live in than Massachusetts orders less at equal time

The usual defence of the Massachusetts amounts is that Massachusetts is expensive, so its child
support should be too. The federal government publishes a cost-of-living index for every state, where the
U.S. average is 100. Massachusetts scores 105.8. California, Hawaii, the District of Columbia, New
Jersey, New York and Washington all score higher, and at equal parenting time every one of them
orders less than Massachusetts for the same family.

| Place | Cost of living | Equal time, per month | Primary custody, per month |
|---|---:|---:|---:|
| California | 110.7 | $2,424 | $3,436 |
| Hawaii | 110.0 | $2,774 | $5,821 |
| District of Columbia | 109.9 | $2,254 | $3,468 |
| New Jersey | 108.8 | $3,002 | $3,002 |
| New York | 107.9 | $4,068 | $4,068 |
| Washington | 107.0 | $2,820 | $2,820 |
| **Massachusetts** | **105.8** | **$4,388** | **$4,714** |

{% include figure.html
   id="e32"
   img="/figures/exhibits/E32-costlier-states-order-less.png"
   alt="Grouped bar chart of the monthly order at equal time and at primary custody for Massachusetts and the six places with a higher cost of living, with a line marking Massachusetts's equal-time order."
   title="Every place that costs more to live in than Massachusetts orders less at equal time."
   deck="Monthly order at the same incomes, costliest place first, at equal time and at primary custody."
   notes="Cost of living: BEA Regional Price Parities 2024, all items, U.S. average 100. Three children, $201,000 and $29,640 a year, no child care."
   source_script="model/cost_of_living.py"
   csv_href="/figures/working/fig13_cost_of_living.csv"
   lazy="false" %}

</section>

<section id="primary" markdown="1">

## Massachusetts charges more for joint custody than five of the six costlier places charge for primary custody

The gap is widest where it matters most. Massachusetts orders $4,388 a month when the parents
split the time equally. California, the District of Columbia, New Jersey, New York and Washington
all order less than that even when the other parent has the children full time. One fact runs
against this: at primary custody Hawaii orders $5,821, more than Massachusetts's $4,714, and it is
the only costlier place that does.

</section>

<section id="all-states" markdown="1">

## Across all fifty states, the cost of living does not explain the Massachusetts amount

The states with a cost of living just below Massachusetts order well below it too. Maryland scores
105.0 and orders $2,310 at equal time, New Hampshire scores 104.2 and orders $3,839, and
Connecticut scores 103.6 and orders $3,138. Plotted across all fifty, Massachusetts sits alone at
the top of the chart while the costliest places sit well below it.

{% include figure.html
   id="e33"
   img="/figures/exhibits/E33-cost-of-living-vs-equal-time-order.png"
   alt="Scatter plot of each state's 2024 cost of living against its monthly equal-time order for the same family, with Massachusetts marked at the top and the six costlier places labelled."
   title="Massachusetts orders the most at equal time, and it is not the most expensive place to live."
   deck="Each dot is one state: its cost of living against its equal-time order for the same family."
   notes="Georgia is held out: its enacted formula orders less at equal time than at primary custody. Cost of living: BEA Regional Price Parities, all items."
   source_script="model/cost_of_living.py"
   csv_href="/figures/working/fig13_cost_of_living.csv" %}

</section>

<section id="limits" markdown="1">

## The comparison is one family at one year's prices, measured with a cost-of-living index that includes housing

<p class="caveat">Every order here is for one family at one set of incomes, the worked example
this site uses throughout, so the comparison shows how each state treats that family and does not
average across families. The cost-of-living figures are for 2024 and cover all items, housing included,
which is the cost a parent keeping a second home for the children actually faces. Georgia is held
out: its enacted formula orders less at equal time than at primary custody, so it is absent here.</p>

</section>

<section id="check" markdown="1">

<div class="check-yourself">
<h2>Check it yourself</h2>
<p>Every number on this page is read from the two published sources, not typed.</p>
<ul>
  <li><strong><a href="/model/cost_of_living.py"><code>model/cost_of_living.py</code></a></strong>
    Joins the 2024 cost-of-living figures to the fifty-state orders and prints the table above.</li>
  <li><strong><a href="/model/test_cost_of_living.py"><code>model/test_cost_of_living.py</code></a></strong>
    Pins every claim on this page, including the Hawaii exception.</li>
  <li><strong><a href="/figures/working/fig13_cost_of_living.csv">fig13_cost_of_living.csv</a></strong>
    Every state's cost of living and both orders.</li>
  <li><strong><a href="/findings/fifty-one-jurisdictions/">The fifty-jurisdiction comparison</a></strong>
    How each state's order was computed and checked.</li>
</ul>
</div>

</section>

</div>
</div>
