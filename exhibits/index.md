---
layout: page
title: Exhibits
description: >-
  Twenty-three figures behind the paper's findings, one chart each, every one traced to the model
  script or the fifty-jurisdiction dataset that produced it, with the plotted values in a CSV or
  dataset beside every chart.
---

# Every exhibit here is a single chart, drawn from a committed script, with its plotted values linked beside it

<div class="disclosure">
<p>Many charts below use my own child support order: $201,000 and $29,640 a year, three children,
computed under Massachusetts's 2025 Worksheet. I disclose it so you can check the arithmetic
against real numbers as well as hypothetical ones. Where a chart sweeps a range of incomes, my own
figures are marked as one point among many. The worksheet behind these figures is
<a href="/model/worksheet.py"><code>model/worksheet.py</code></a>, checked against the official
form's own scripts on <a href="/the-model/">the model page</a>. None of these figures has been
sent to the Trial Court, and neither has anything else on this site (see
<a href="/documents/">Documents</a>); they were built for the working paper.</p>
</div>

Every chart below has one set of axes; an earlier set of exhibits mixed several panels into one
image, since split into the single-chart figures listed here. The fact line under each title states
the custody arrangement, child count, child care status, and incomes used, the same pattern the
chart is computed under. One fact pattern does not generalize to every family, and a household
comparison always carries its per-person counterpart.

## Contents

1. [With three children, the recipient household holds more after the order in 10 percent of income combinations.](#e01)
2. [Per person, the payor holds more almost everywhere.](#e02)
3. [With one child, the recipient household holds more after the order in no income combinations.](#e18)
4. [With two children, the recipient household holds more after the order in 0 percent of income combinations.](#e19)
5. [The order exceeds 40 percent of the payor's net income only where the lower earner makes about $20,000 or less.](#e04)
6. [The hardship valve fires late because it reads the wrong income.](#e05)
7. [Of the payor's next dollar, the payor keeps between a third and a half.](#e10)
8. [The payor's share of a $15,600 child care bill, four ways to split it.](#e06)
9. [With one child, post-transfer child care funds the payor 26 points below his income share.](#e20)
10. [With two children, post-transfer child care funds the payor 36 points below his income share.](#e21)
11. [With three children, post-transfer child care funds the payor 43 points below his income share.](#e22)
12. [The payor bears 93 percent of the combined child care while earning 87 percent of the gross income.](#e25)
13. [Both parents paying child care costs the payor $29,008 a year, the recipient household $2,192.](#e26)
14. [The Worksheet's credit for equal parenting time collapses as the income gap widens; a cross-credit narrows without collapsing.](#e08)
15. [The equal-time credit is what a standard formula pays a parent who has the children one night in three.](#e09)
16. [Splitting two children across two homes cuts the weekly order by 30 percent.](#e23)
17. [Two homes, one child each, cost 43 percent more on the schedule than one home with two.](#e24)
18. [At equal parenting time, Massachusetts orders the most of the fifty states.](#e11)
19. [With the lower earner primary, only Hawaii orders more than Massachusetts.](#e12)
20. [In Massachusetts and 22 other states, a parent with the children one night in three pays the same as a parent with no overnights.](#e13)
21. [Massachusetts's presumptive formula runs to $450,000; 12 schedules run higher, 28 stop lower.](#e16)
22. [Only Wisconsin and Hawaii order more than Massachusetts does at equal time.](#e17)
23. [Five reviews have taken up gross versus net. None changed it.](#e27)

## Who holds more after the order

<div class="exhibit-pair">

<figure class="exhibit" id="e01">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E01-who-holds-more-3-children.png"
     data-caption="With three children, the recipient household holds more after the order in 10 percent of income combinations."
     data-csv-href="/figures/working/fig1_heatmap_3child_box1.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E01-who-holds-more-3-children.png"
         alt="Heatmap of the recipient household's net income minus the payor's, in dollars per year, across combinations of higher-earner gross income from $60,000 to $300,000 and lower-earner gross income from $0 to $120,000, three children, equal parenting time, no child care.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">With three children, the recipient household holds more after the order in 10 percent of income combinations.</h3>
    <p class="exhibit-deck">Recipient household net minus payor net, per year.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>Vary (axes)</dd></div>
    </dl>
    <p class="exhibit-notes">Of the 10 percent of the grid where the recipient household is ahead, 75 percent sits below $150,000 of higher-earner income, and none above $175,000. The closed contour inside the red region is Line 6e's limitation, which stops binding once the payor's Line 6d crosses 10 percent; the order then drops about $110 a week in one step. Per person the payor still leads almost everywhere (E02). Masked where the lower earner would out-earn the higher. Premiums $43/$33 a week; MA under-13 credit set to zero; no refundable tax credits counted.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig1_heatmaps.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code> ·
      <a href="/figures/working/fig1_heatmap_3child_box1.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e02">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E02-who-holds-more-per-person-3-children.png"
     data-caption="Per person, the payor holds more almost everywhere."
     data-csv-href="/figures/working/fig1_heatmap_3child_box1.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E02-who-holds-more-per-person-3-children.png"
         loading="lazy"
         alt="Heatmap of the same net-income gap divided by household size, one person against four, same income grid, three children, equal parenting time, no child care.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">Per person, the payor holds more almost everywhere.</h3>
    <p class="exhibit-deck">Recipient household net ÷ 4, minus payor net. Companion to E01.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>Vary (axes)</dd></div>
    </dl>
    <p class="exhibit-notes">The payor is ahead in 99 percent of the grid. This pairs with E01, since per person is the comparison a reader will raise first. Masked where the lower earner would out-earn the higher. Premiums $43/$33 a week; MA under-13 credit set to zero.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig1_heatmaps.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code> ·
      <a href="/figures/working/fig1_heatmap_3child_box1.csv">data (CSV)</a></p>
  </figcaption>
</figure>

</div>

<div class="exhibit-pair">

<figure class="exhibit" id="e18">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E18-who-holds-more-1-child.png"
     data-caption="With one child, the recipient household holds more after the order in no income combinations."
     data-csv-href="/figures/working/fig1_heatmap_1child_box1.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E18-who-holds-more-1-child.png"
         loading="lazy"
         alt="Heatmap of the recipient household's net income minus the payor's, in dollars per year, same income grid as E01, one child, equal parenting time, no child care.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">With one child, the recipient household holds more after the order in no income combinations.</h3>
    <p class="exhibit-deck">Recipient household net minus payor net, per year. Companion to E01/E19 (same grid, two and three children).</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>1</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>Vary (axes)</dd></div>
    </dl>
    <p class="exhibit-notes">Same grid and colour scale as E01, one child instead of three. With E19, this shows the number of children, not any one family's facts, decides which household comes out ahead. Per person the payor leads far more broadly still (E02 holds at all three child counts). Masked where the lower earner would out-earn the higher. Premiums $43/$33 a week; MA under-13 credit set to zero.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig1_heatmaps.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code> ·
      <a href="/figures/working/fig1_heatmap_1child_box1.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e19">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E19-who-holds-more-2-children.png"
     data-caption="With two children, the recipient household holds more after the order in 0 percent of income combinations."
     data-csv-href="/figures/working/fig1_heatmap_2child_box1.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E19-who-holds-more-2-children.png"
         loading="lazy"
         alt="Heatmap of the recipient household's net income minus the payor's, in dollars per year, same income grid as E01, two children, equal parenting time, no child care.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">With two children, the recipient household holds more after the order in 0 percent of income combinations.</h3>
    <p class="exhibit-deck">Recipient household net minus payor net, per year. Companion to E01/E18 (same grid, one and three children).</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>2</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>Vary (axes)</dd></div>
    </dl>
    <p class="exhibit-notes">Same grid and colour scale as E01 and E18. The share stays at zero at one child and two, and rises to 10 percent at three, a child-count effect, not an artifact of one income pair. Masked where the lower earner would out-earn the higher. Premiums $43/$33 a week; MA under-13 credit set to zero; no refundable tax credits counted.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig1_heatmaps.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code> ·
      <a href="/figures/working/fig1_heatmap_2child_box1.csv">data (CSV)</a></p>
  </figcaption>
</figure>

</div>

<figure class="exhibit" id="e04">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E04-order-as-share-of-payor-net-3-children.png"
     data-caption="The order exceeds 40 percent of the payor's net income only where the lower earner makes about $20,000 or less."
     data-csv-href="/figures/working/fig1_heatmap_3child_box1.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E04-order-as-share-of-payor-net-3-children.png"
         loading="lazy"
         alt="Heatmap of the order as a percentage of the payor's net income, with a 40 percent contour line, same income grid, three children, equal parenting time, no child care.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">The order exceeds 40 percent of the payor's net income only where the lower earner makes about $20,000 or less.</h3>
    <p class="exhibit-deck">Order as a share of payor net; line at 40%.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>Vary (axes)</dd></div>
    </dl>
    <p class="exhibit-notes">The 40 percent contour sits near $20,000 of lower-earner income up to about $205,000 of higher-earner income; above that, the order never reaches 40 percent of net on the grid (11 percent of cells). Scale fixed 0 to 60 percent. Section IV.C's hardship presumption is written for the region under this contour; E05 shows what the Worksheet reports there. Masked where the lower earner would out-earn the higher. Premiums $43/$33 a week; MA under-13 credit set to zero.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig1_heatmaps.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code> ·
      <a href="/figures/working/fig1_heatmap_3child_box1.csv">data (CSV)</a></p>
  </figcaption>
</figure>

## The hardship test and its units

<figure class="exhibit" id="e05">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E05-what-line-7e-sees-vs-true-burden-worked-example.png"
     data-caption="The hardship valve fires late because it reads the wrong income."
     data-csv-href="/figures/working/fig6_valve_units_lag.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E05-what-line-7e-sees-vs-true-burden-worked-example.png"
         loading="lazy"
         alt="Line chart of Line 7e's reported percentage versus the true share of the payor's net income, against child care claimed from $0 to $600 a week, at the worked example.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">The hardship valve fires late because it reads the wrong income.</h3>
    <p class="exhibit-deck">Line 7e's reading vs the true share of net income as claimed child care rises.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>Rises to the $430/child ceiling (recipient)</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / $29,640</dd></div>
    </dl>
    <p class="exhibit-notes">As claimed child care rises, the true burden passes 40 percent of net at $130 a week; Line 7e reports 40 percent only at $590 a week, by which point the true burden is 55 percent. Nothing on the form flags the gap. Child care is included in the order. Two of three children under 13 (MA credit); premiums $43/$33.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig6_valve.py</code>; <code>model/submission_figures.py</code> ·
      <a href="/figures/working/fig6_valve_units_lag.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e10">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E10-cents-kept-of-next-dollar-worked-example.png"
     data-caption="Of the payor's next dollar, the payor keeps between a third and a half."
     data-csv-href="/figures/working/fig4_marginal_retention.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E10-cents-kept-of-next-dollar-worked-example.png"
         loading="lazy"
         alt="Line chart of cents kept of the payor's next dollar of income, from $100,000 to $400,000 of payor income, with and without $300 a week of child care.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">Of the payor's next dollar, the payor keeps between a third and a half.</h3>
    <p class="exhibit-deck">Marginal retention after federal and state tax and the change in the order.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>None vs $300/wk (recipient)</dd></div>
      <div><dt>Incomes</dt><dd>Varies / $29,640</dd></div>
    </dl>
    <p class="exhibit-notes">The order's marginal take runs near 20 percent, above Table A's 10 percent top bracket, because the child-count multiplier and the rising income share both scale with the payor's income. $5,000 steps. Dashed line: 50 cents. Two of three children under 13 (MA credit); premiums $43/$33.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig4_retention.py</code>; <code>model/marginal_retention.py</code> ·
      <a href="/figures/working/fig4_marginal_retention.csv">data (CSV)</a></p>
  </figcaption>
</figure>

## Child care

<figure class="exhibit" id="e06">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E06-child-care-share-three-rules-worked-example.png"
     data-caption="The payor's share of a $15,600 child care bill, four ways to split it."
     data-csv-href="/figures/working/fig2_childcare_worked_example.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E06-child-care-share-three-rules-worked-example.png"
         loading="lazy"
         alt="Bar chart of the payor's share of a $15,600 annual child care bill under four allocation rules, at the worked example.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">The payor's share of a $15,600 child care bill, four ways to split it.</h3>
    <p class="exhibit-deck">Third bar: what the comments ask for (new Lines 6b-1a and 6b-1).</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>$300/wk, paid by the recipient</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / $29,640</dd></div>
    </dl>
    <p class="exhibit-notes">Line 3c allocates 87.7 percent to the payor on pre-transfer income shares. The second bar is the fallback (new Line 6b-2), adjusting shares by the base order on a gross basis: 64.5 percent. The third bar is what the comments ask for: the same adjustment measured after federal and Massachusetts income tax and FICA, for a single filer claiming no exemptions, giving 53.0 percent. The fourth bar adds the refundable tax credits back in, under the alternating-year Child Tax Credit convention Box 1 now uses, 49.7 percent; that basis is not asked for, because CJ-D 304 collects neither parent's filing status nor which parent claims which child. Child care is included in the order. Two of three children under 13 (MA credit); premiums $43/$33.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig2_childcare.py</code>; <code>model/childcare_post_transfer.py</code> ·
      <a href="/figures/working/fig2_childcare_worked_example.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e20">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E20-child-care-funding-gap-1-child.png"
     data-caption="With one child, post-transfer child care funds the payor 26 points below his income share."
     data-csv-href="/figures/working/fig2_childcare_rules.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E20-child-care-funding-gap-1-child.png"
         loading="lazy"
         alt="Line chart of the payor's funded share of a child care bill against his pre-transfer income share, under two post-transfer allocation rules, one child, $100 a week paid by the lower earner.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">With one child, post-transfer child care funds the payor 26 points below his income share.</h3>
    <p class="exhibit-deck">Share of the child care bill the payor funds, by his pre-transfer income share, two post-transfer rules.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>1</dd></div>
      <div><dt>Child care</dt><dd>$100/child/wk, paid by the lower earner</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / varies</dd></div>
    </dl>
    <p class="exhibit-notes">The gap is measured at the highest income share plotted on the CSV. Companion to E21 and E22 (two and three children): the gap widens with the number of children. Child care is included in the order. Premiums $43/$33 a week; MA under-13 credit set to zero.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig2_childcare.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code> ·
      <a href="/figures/working/fig2_childcare_rules.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e21">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E21-child-care-funding-gap-2-children.png"
     data-caption="With two children, post-transfer child care funds the payor 36 points below his income share."
     data-csv-href="/figures/working/fig2_childcare_rules.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E21-child-care-funding-gap-2-children.png"
         loading="lazy"
         alt="Line chart of the payor's funded share of a child care bill against his pre-transfer income share, under two post-transfer allocation rules, two children, $100 a week per child paid by the lower earner.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">With two children, post-transfer child care funds the payor 36 points below his income share.</h3>
    <p class="exhibit-deck">Share of the child care bill the payor funds, by his pre-transfer income share, two post-transfer rules.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>2</dd></div>
      <div><dt>Child care</dt><dd>$100/child/wk, paid by the lower earner</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / varies</dd></div>
    </dl>
    <p class="exhibit-notes">Same construction as E20, two children instead of one: the gap grows from 26 points to 36. Child care is included in the order. Premiums $43/$33 a week; MA under-13 credit set to zero.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig2_childcare.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code> ·
      <a href="/figures/working/fig2_childcare_rules.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e22">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E22-child-care-funding-gap-3-children.png"
     data-caption="With three children, post-transfer child care funds the payor 43 points below his income share."
     data-csv-href="/figures/working/fig2_childcare_rules.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E22-child-care-funding-gap-3-children.png"
         loading="lazy"
         alt="Line chart of the payor's funded share of a child care bill against his pre-transfer income share, under two post-transfer allocation rules, three children, $100 a week per child paid by the lower earner.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">With three children, post-transfer child care funds the payor 43 points below his income share.</h3>
    <p class="exhibit-deck">Share of the child care bill the payor funds, by his pre-transfer income share, two post-transfer rules.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>$100/child/wk, paid by the lower earner</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / varies</dd></div>
    </dl>
    <p class="exhibit-notes">Same construction as E20 and E21, three children, the worked example's own count: the gap reaches 43 points. Child care is included in the order. Premiums $43/$33 a week; MA under-13 credit set to zero.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig2_childcare.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code> ·
      <a href="/figures/working/fig2_childcare_rules.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<div class="exhibit-pair">

<figure class="exhibit" id="e25">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E25-both-pay-child-care-who-pays-3-children.png"
     data-caption="The payor bears 93 percent of the combined child care while earning 87 percent of the gross income."
     data-csv-href="/figures/working/fig8_both_pay.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E25-both-pay-child-care-who-pays-3-children.png"
         loading="lazy"
         alt="Stacked bar chart of each parent's share of combined gross income and of a combined $31,200 child care bill, both parents paying $300 a week in their own home, three children.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">The payor bears 93 percent of the combined child care while earning 87 percent of the gross income.</h3>
    <p class="exhibit-deck">Who pays a combined $31,200/yr of child care, both parents paying $300/wk in their own home.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>$300/wk in each home</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / $29,640</dd></div>
    </dl>
    <p class="exhibit-notes">Each parent pays $300 a week during their own parenting time, the ordinary case at equal time. E26 shows each parent's resulting net position. Two of three children under 13; premiums $43/$33.</p>
    <p class="exhibit-source">Source: <code>model/submission_figures.py</code> § 2.1; <code>model/charts/fig8_both_pay.py</code> ·
      <a href="/figures/working/fig8_both_pay.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e26">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E26-both-pay-child-care-net-position-3-children.png"
     data-caption="Both parents paying child care costs the payor $29,008 a year, the recipient household $2,192."
     data-csv-href="/figures/working/fig8_both_pay.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E26-both-pay-child-care-net-position-3-children.png"
         loading="lazy"
         alt="Bar chart of each parent's net income under three child care scenarios, neither pays, only the recipient pays, both pay $300 a week, three children.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">Both parents paying child care costs the payor $29,008 a year, the recipient household $2,192.</h3>
    <p class="exhibit-deck">Each parent's net position, neither, one, or both paying $300/wk of child care.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>$0 / $300 / $300 per wk (see scenarios)</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / $29,640</dd></div>
    </dl>
    <p class="exhibit-notes">The Worksheet allocates the recipient's cost to the payor through Line 6b, but credits the payor's own cost back through Line 6e at about two cents on the dollar: his $15,600 reduces the order by only $270 a year. Order plus his own child care reaches 56 percent of his net income while Line 7e reads 33 percent. Per person the payor still leads ($63,885 vs. $20,854 each for four). Two of three children under 13; premiums $43/$33.</p>
    <p class="exhibit-source">Source: <code>model/submission_figures.py</code> § 2.1; <code>model/charts/fig8_both_pay.py</code> ·
      <a href="/figures/working/fig8_both_pay.csv">data (CSV)</a></p>
  </figcaption>
</figure>

</div>

## Parenting time

<figure class="exhibit" id="e08">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png"
     data-caption="The Worksheet's credit for equal parenting time collapses as the income gap widens; a cross-credit narrows without collapsing."
     data-csv-href="/figures/working/fig3_credit_collapse.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png"
         loading="lazy"
         alt="Line chart of the percentage reduction in the order for equal parenting time versus the Box 2 order, against the payor's share of combined available income, for the current Worksheet and two redline variants.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">The Worksheet's credit for equal parenting time collapses as the income gap widens; a cross-credit narrows without collapsing.</h3>
    <p class="exhibit-deck">Reduction in the order for equal time, against the Box 2 order (the paying parent has the children about a third of the time).</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint (Box 1) vs primary (Box 2)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / varies</dd></div>
    </dl>
    <p class="exhibit-notes">The reduction falls from about 75 percent at a 57 percent payor income share to 7 percent at 88 percent and 1 percent at 96 percent: no parenting-time quantity enters any line. Variant A, applying Line 6e once, lifts the curve. Variant B, the standard cross-credit at a 1.5 duplication factor used by 23 states, stops it collapsing. Both are the letter's § 5 redlines.</p>
    <p class="exhibit-source">Source: <code>model/charts/exhibits.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code>; <code>model/box1_fix.py</code> ·
      <a href="/figures/working/fig3_credit_collapse.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e09">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E09-implied-overnight-share-by-factor-3-children.png"
     data-caption="The equal-time credit is what a standard formula pays a parent who has the children one night in three."
     data-csv-href="/figures/working/fig3_credit_collapse.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E09-implied-overnight-share-by-factor-3-children.png"
         loading="lazy"
         alt="Line chart of the overnight share that reproduces the Box 1 order under a standard cross-credit, against the payor's share of combined available income, at duplication factors 1.5 and 2.0.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">The equal-time credit is what a standard formula pays a parent who has the children one night in three.</h3>
    <p class="exhibit-deck">Massachusetts's credit for half the nights, converted into the overnight share a cross-credit formula would need to produce it.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint (Box 1) vs primary (Box 2)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / varies</dd></div>
    </dl>
    <p class="exhibit-notes">The duplication factor decides the number: 33.3 percent at a factor of 1.5, 46.9 percent at 2.0. State the factor beside the number always. Blank below the Line 5c floor, where the order is no longer a cross-credit.</p>
    <p class="exhibit-source">Source: <code>model/charts/exhibits.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code>; <code>model/box1_fix.py</code> ·
      <a href="/figures/working/fig3_credit_collapse.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<div class="exhibit-pair">

<figure class="exhibit" id="e23">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E23-split-siblings-weekly-order-2-children.png"
     data-caption="Splitting two children across two homes cuts the weekly order by 30 percent."
     data-csv-href="/figures/working/fig7_box3_inversion.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E23-split-siblings-weekly-order-2-children.png"
         loading="lazy"
         alt="Line chart of the weekly child support order against the payor's income share, under Box 1 with both children shared and Box 3 with one child residing primarily with each parent, two children.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">Splitting two children across two homes cuts the weekly order by 30 percent.</h3>
    <p class="exhibit-deck">Weekly order under Box 1 and Box 3 for the same two children.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint (Box 1) vs split (Box 3)</dd></div>
      <div><dt>Children</dt><dd>2</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / varies</dd></div>
    </dl>
    <p class="exhibit-notes">Under Box 1 both children are shared equal time; under Box 3 one lives primarily with each parent. The payor's care responsibility is one child-share either way, but Line 6g nets the columns on the one-child schedule (Table B 1.00 against 1.40), so Box 3 comes out at 70 percent of Box 1 ($581 against $835 a week) even though the arrangement costs more on the schedule's own measure (E24). This one cuts against the lower earner. Premiums $43/$33 a week; MA under-13 credit set to zero.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig7_box3_split.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code> ·
      data (CSV): <a href="/figures/working/fig7_box3_inversion.csv">curve</a>,
      <a href="/figures/working/fig7_box3_inversion_example.csv">worked-example point</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e24">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E24-split-siblings-schedule-cost-2-children.png"
     data-caption="Two homes, one child each, cost 43 percent more on the schedule than one home with two."
     data-csv-href="/figures/working/fig7_box3_inversion.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E24-split-siblings-schedule-cost-2-children.png"
         loading="lazy"
         alt="Bar chart comparing Table B's cost multiplier for one home raising two children against two homes each raising one child.">
  </a>
  <figcaption>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <h3 class="exhibit-title">Two homes, one child each, cost 43 percent more on the schedule than one home with two.</h3>
    <p class="exhibit-deck">Table B's cost multiple: one home raising two children vs two homes each raising one.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint (Box 1) vs split (Box 3)</dd></div>
      <div><dt>Children</dt><dd>2</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / varies</dd></div>
    </dl>
    <p class="exhibit-notes">Table B charges one home raising two children 1.40 times the one-child amount; two homes raising one child each are charged 1.00 twice, 2.00 combined. The order moves the opposite way (E23): the more expensive arrangement produces the smaller transfer.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig7_box3_split.py</code>; <code>model/worksheet.py</code>; <code>model/net_position.py</code> ·
      data (CSV): <a href="/figures/working/fig7_box3_inversion.csv">curve</a>,
      <a href="/figures/working/fig7_box3_inversion_example.csv">worked-example point</a></p>
  </figcaption>
</figure>

</div>

## Fifty-one jurisdictions

<figure class="exhibit" id="e11">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E11-fifty-states-equal-parenting-one-fact-pattern.png"
     data-caption="At equal parenting time, Massachusetts orders the most of the fifty states."
     data-csv-href="/figures/working/fig5_states.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E11-fifty-states-equal-parenting-one-fact-pattern.png"
         loading="lazy"
         alt="Horizontal bar chart of the monthly child support order in fifty states under equal parenting time, one fact pattern, Massachusetts highlighted.">
  </a>
  <figcaption>
    <p class="confidence-tag">Tiered: a single fact pattern; see method</p>
    <h3 class="exhibit-title">At equal parenting time, Massachusetts orders the most of the fifty states.</h3>
    <p class="exhibit-deck">Monthly order at one fact pattern. Georgia held out.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Joint, equal time (Box 1)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / $29,640</dd></div>
    </dl>
    <p class="exhibit-notes">Fifty of fifty-one jurisdictions survived every verification stage; Georgia is held out because its own enacted formula, reproduced by its own calculator, gives a lower order under primary custody than under equal time. Each row was profiled from primary sources, computed twice blind, reconciled, and attacked. Own premiums ($43/$33) as each state treats them. One fact pattern; the ranking generalizes to nothing else.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig5_states.py</code> ·
      <a href="/data/fifty-state/tier-50-2026-09-05.json">data (JSON)</a> ·
      <a href="/figures/working/fig5_states.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<details>
<summary>Full ranking behind E11: all 50 jurisdictions</summary>

  <div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable data table for E11">
    <table class="exhibit-table" id="e11-table">
    <caption>Monthly order, equal parenting time (S1) &mdash; full data behind <a href="#e11">E11</a></caption>
    <thead>
      <tr><th scope="col">Rank</th><th scope="col">Jurisdiction</th><th scope="col" class="numeric">Monthly order</th></tr>
    </thead>
    <tbody>
      <tr class="is-reader-state"><td>1</td><td>Massachusetts<span class="visually-hidden">, this page&rsquo;s worked example</span></td><td class="numeric">$4,388.48</td></tr>
      <tr><td>2</td><td>New York</td><td class="numeric">$4,067.61</td></tr>
      <tr><td>3</td><td>New Hampshire</td><td class="numeric">$3,838.66</td></tr>
      <tr><td>4</td><td>Texas</td><td class="numeric">$3,510.00</td></tr>
      <tr><td>5</td><td>Missouri</td><td class="numeric">$3,139.00</td></tr>
      <tr><td>6</td><td>Connecticut</td><td class="numeric">$3,138.20</td></tr>
      <tr><td>7</td><td>Wisconsin</td><td class="numeric">$3,117.35</td></tr>
      <tr><td>8</td><td>New Jersey</td><td class="numeric">$3,002.31</td></tr>
      <tr><td>9</td><td>North Dakota</td><td class="numeric">$2,939.00</td></tr>
      <tr><td>10</td><td>Maine</td><td class="numeric">$2,899.02</td></tr>
      <tr><td>11</td><td>Washington</td><td class="numeric">$2,819.56</td></tr>
      <tr><td>12</td><td>Hawaii</td><td class="numeric">$2,774.00</td></tr>
      <tr><td>13</td><td>Rhode Island</td><td class="numeric">$2,684.45</td></tr>
      <tr><td>14</td><td>Colorado</td><td class="numeric">$2,652.32</td></tr>
      <tr><td>15</td><td>Iowa</td><td class="numeric">$2,630.25</td></tr>
      <tr><td>16</td><td>Ohio</td><td class="numeric">$2,564.15</td></tr>
      <tr><td>17</td><td>California</td><td class="numeric">$2,424.32</td></tr>
      <tr><td>18</td><td>Pennsylvania</td><td class="numeric">$2,378.42</td></tr>
      <tr><td>19</td><td>Alaska</td><td class="numeric">$2,367.95</td></tr>
      <tr><td>20</td><td>Maryland</td><td class="numeric">$2,309.54</td></tr>
      <tr><td>21</td><td>Kansas</td><td class="numeric">$2,296.63</td></tr>
      <tr><td>22</td><td>Indiana</td><td class="numeric">$2,283.25</td></tr>
      <tr><td>23</td><td>Delaware</td><td class="numeric">$2,281.35</td></tr>
      <tr><td>24</td><td>District of Columbia</td><td class="numeric">$2,253.73</td></tr>
      <tr><td>25</td><td>Louisiana</td><td class="numeric">$2,227.23</td></tr>
      <tr><td>26</td><td>Arkansas</td><td class="numeric">$2,118.68</td></tr>
      <tr><td>27</td><td>Mississippi</td><td class="numeric">$2,097.44</td></tr>
      <tr><td>28</td><td>Wyoming</td><td class="numeric">$1,900.85</td></tr>
      <tr><td>29</td><td>North Carolina</td><td class="numeric">$1,883.12</td></tr>
      <tr><td>30</td><td>Illinois</td><td class="numeric">$1,881.45</td></tr>
      <tr><td>31</td><td>Virginia</td><td class="numeric">$1,872.18</td></tr>
      <tr><td>32</td><td>Nevada</td><td class="numeric">$1,842.80</td></tr>
      <tr><td>33</td><td>Tennessee</td><td class="numeric">$1,833.00</td></tr>
      <tr><td>34</td><td>South Carolina</td><td class="numeric">$1,832.22</td></tr>
      <tr><td>35</td><td>New Mexico</td><td class="numeric">$1,823.64</td></tr>
      <tr><td>36</td><td>Idaho</td><td class="numeric">$1,794.22</td></tr>
      <tr><td>37</td><td>South Dakota</td><td class="numeric">$1,788.96</td></tr>
      <tr><td>38</td><td>Alabama</td><td class="numeric">$1,746.00</td></tr>
      <tr><td>39</td><td>Florida</td><td class="numeric">$1,735.21</td></tr>
      <tr><td>40</td><td>West Virginia</td><td class="numeric">$1,724.21</td></tr>
      <tr><td>41</td><td>Vermont</td><td class="numeric">$1,686.42</td></tr>
      <tr><td>42</td><td>Nebraska</td><td class="numeric">$1,475.23</td></tr>
      <tr><td>43</td><td>Montana</td><td class="numeric">$1,461.00</td></tr>
      <tr><td>44</td><td>Michigan</td><td class="numeric">$1,445.25</td></tr>
      <tr><td>45</td><td>Arizona</td><td class="numeric">$1,309.36</td></tr>
      <tr><td>46</td><td>Oklahoma</td><td class="numeric">$1,284.42</td></tr>
      <tr><td>47</td><td>Minnesota</td><td class="numeric">$1,174.71</td></tr>
      <tr><td>48</td><td>Kentucky</td><td class="numeric">$1,087.80</td></tr>
      <tr><td>49</td><td>Oregon</td><td class="numeric">$1,072.00</td></tr>
      <tr><td>50</td><td>Utah</td><td class="numeric">$1,058.31</td></tr>
    </tbody>
  </table>
  </div>

</details>

<figure class="exhibit" id="e12">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E12-fifty-states-lower-earner-primary-one-fact-pattern.png"
     data-caption="With the lower earner primary, only Hawaii orders more than Massachusetts."
     data-csv-href="/figures/working/fig5_states.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E12-fifty-states-lower-earner-primary-one-fact-pattern.png"
         loading="lazy"
         alt="Horizontal bar chart of the monthly child support order in fifty states with the children primarily with the lower earner, one fact pattern, Massachusetts highlighted.">
  </a>
  <figcaption>
    <p class="confidence-tag">Tiered: a single fact pattern; see method</p>
    <h3 class="exhibit-title">With the lower earner primary, only Hawaii orders more than Massachusetts.</h3>
    <p class="exhibit-deck">Monthly order at one fact pattern. Georgia held out. First of a pair with E17.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>Primary with the lower earner (Box 2)</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / $29,640</dd></div>
    </dl>
    <p class="exhibit-notes">Same fact pattern, children primarily with the lower earner. Hawaii's design, shared with Delaware and Montana, exhausts the self-support reserve differently from an income-shares schedule at this income gap. Same states, axis range, colors, and ordering rule as E17, so the two read as a pair.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig5_states.py</code> ·
      <a href="/data/fifty-state/tier-50-2026-09-05.json">data (JSON)</a> ·
      <a href="/figures/working/fig5_states.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<details>
<summary>Full ranking behind E12: all 50 jurisdictions</summary>

  <div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable data table for E12">
    <table class="exhibit-table" id="e12-table">
    <caption>Monthly order, children primarily with the lower earner (S2) &mdash; full data behind <a href="#e12">E12</a></caption>
    <thead>
      <tr><th scope="col">Rank</th><th scope="col">Jurisdiction</th><th scope="col" class="numeric">Monthly order</th></tr>
    </thead>
    <tbody>
      <tr><td>1</td><td>Hawaii</td><td class="numeric">$5,821.00</td></tr>
      <tr class="is-reader-state"><td>2</td><td>Massachusetts<span class="visually-hidden">, this page&rsquo;s worked example</span></td><td class="numeric">$4,714.22</td></tr>
      <tr><td>3</td><td>Wisconsin</td><td class="numeric">$4,491.71</td></tr>
      <tr><td>4</td><td>New York</td><td class="numeric">$4,067.61</td></tr>
      <tr><td>5</td><td>Delaware</td><td class="numeric">$3,990.73</td></tr>
      <tr><td>6</td><td>New Hampshire</td><td class="numeric">$3,838.66</td></tr>
      <tr><td>7</td><td>Kansas</td><td class="numeric">$3,838.03</td></tr>
      <tr><td>8</td><td>Iowa</td><td class="numeric">$3,744.73</td></tr>
      <tr><td>9</td><td>Texas</td><td class="numeric">$3,510.00</td></tr>
      <tr><td>10</td><td>District of Columbia</td><td class="numeric">$3,467.96</td></tr>
      <tr><td>11</td><td>Alaska</td><td class="numeric">$3,462.96</td></tr>
      <tr><td>12</td><td>California</td><td class="numeric">$3,436.04</td></tr>
      <tr><td>13</td><td>Maryland</td><td class="numeric">$3,295.11</td></tr>
      <tr><td>14</td><td>Louisiana</td><td class="numeric">$3,269.06</td></tr>
      <tr><td>15</td><td>North Dakota</td><td class="numeric">$3,219.00</td></tr>
      <tr><td>16</td><td>Missouri</td><td class="numeric">$3,139.00</td></tr>
      <tr><td>17</td><td>Connecticut</td><td class="numeric">$3,138.20</td></tr>
      <tr><td>18</td><td>Rhode Island</td><td class="numeric">$3,123.22</td></tr>
      <tr><td>19</td><td>Colorado</td><td class="numeric">$3,090.30</td></tr>
      <tr><td>20</td><td>Pennsylvania</td><td class="numeric">$3,086.76</td></tr>
      <tr><td>21</td><td>Montana</td><td class="numeric">$3,073.50</td></tr>
      <tr><td>22</td><td>Illinois</td><td class="numeric">$3,037.90</td></tr>
      <tr><td>23</td><td>New Jersey</td><td class="numeric">$3,002.31</td></tr>
      <tr><td>24</td><td>North Carolina</td><td class="numeric">$2,934.30</td></tr>
      <tr><td>25</td><td>Maine</td><td class="numeric">$2,899.02</td></tr>
      <tr><td>26</td><td>Washington</td><td class="numeric">$2,819.56</td></tr>
      <tr><td>27</td><td>Michigan</td><td class="numeric">$2,808.44</td></tr>
      <tr><td>28</td><td>Wyoming</td><td class="numeric">$2,801.97</td></tr>
      <tr><td>29</td><td>New Mexico</td><td class="numeric">$2,795.32</td></tr>
      <tr><td>30</td><td>Alabama</td><td class="numeric">$2,736.00</td></tr>
      <tr><td>31</td><td>Virginia</td><td class="numeric">$2,672.09</td></tr>
      <tr><td>32</td><td>South Carolina</td><td class="numeric">$2,669.21</td></tr>
      <tr><td>33</td><td>South Dakota</td><td class="numeric">$2,623.12</td></tr>
      <tr><td>34</td><td>Vermont</td><td class="numeric">$2,594.42</td></tr>
      <tr><td>35</td><td>Mississippi</td><td class="numeric">$2,564.76</td></tr>
      <tr><td>36</td><td>Ohio</td><td class="numeric">$2,564.15</td></tr>
      <tr><td>37</td><td>Idaho</td><td class="numeric">$2,549.85</td></tr>
      <tr><td>38</td><td>Indiana</td><td class="numeric">$2,548.03</td></tr>
      <tr><td>39</td><td>West Virginia</td><td class="numeric">$2,518.77</td></tr>
      <tr><td>40</td><td>Florida</td><td class="numeric">$2,512.99</td></tr>
      <tr><td>41</td><td>Nevada</td><td class="numeric">$2,485.00</td></tr>
      <tr><td>42</td><td>Nebraska</td><td class="numeric">$2,402.03</td></tr>
      <tr><td>43</td><td>Arkansas</td><td class="numeric">$2,349.64</td></tr>
      <tr><td>44</td><td>Utah</td><td class="numeric">$2,332.66</td></tr>
      <tr><td>45</td><td>Arizona</td><td class="numeric">$2,290.06</td></tr>
      <tr><td>46</td><td>Minnesota</td><td class="numeric">$2,271.30</td></tr>
      <tr><td>47</td><td>Tennessee</td><td class="numeric">$2,031.00</td></tr>
      <tr><td>48</td><td>Oklahoma</td><td class="numeric">$2,008.78</td></tr>
      <tr><td>49</td><td>Kentucky</td><td class="numeric">$1,871.67</td></tr>
      <tr><td>50</td><td>Oregon</td><td class="numeric">$1,772.00</td></tr>
    </tbody>
  </table>
  </div>

</details>

<figure class="exhibit" id="e13">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E13-credit-at-122-overnights-28-of-51.png"
     data-caption="In Massachusetts and 22 other states, a parent with the children one night in three pays the same as a parent with no overnights."
     data-csv-href="/data/fifty-state/credit-at-122-2026-09-05.json" data-csv-label="Data (JSON)">
  <img src="/figures/exhibits/E13-credit-at-122-overnights-28-of-51.png"
         loading="lazy"
         alt="Tile map of fifty-one jurisdictions, each colored by whether a formula credit applies when a parent has the children 122 overnights a year, about one-third of the time.">
  </a>
  <figcaption>
    <p class="confidence-tag">Tiered: a single fact pattern; see method</p>
    <h3 class="exhibit-title">In Massachusetts and 22 other states, a parent with the children one night in three pays the same as a parent with no overnights.</h3>
    <p class="exhibit-deck">Twenty-eight states give that parent a formula credit; 23 do not. Blue: a credit at 122 overnights a year. Grey: none.</p>
    <dl class="exhibit-facts">
      <div><dt>Counted</dt><dd>Any formula credit at 122 overnights</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>None</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / $29,640</dd></div>
    </dl>
    <p class="exhibit-notes">A count, not a dollar amount. Massachusetts is among the 23: its Box 2 already assumes the paying parent has the children about a third of the time, without a discrete credit for it. In the one clean pairing with a credit-giving state the dollar effect runs the other way, so this count is a structural fact and nothing more.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig5_states.py</code> ·
      <a href="/data/fifty-state/credit-at-122-2026-09-05.json">data (JSON)</a></p>
  </figcaption>
</figure>

<details>
<summary>Full table behind E13: all 51 jurisdictions</summary>

  <div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable data table for E13">
    <table class="exhibit-table" id="e13-table">
    <caption>Formula credit at 122 overnights (one-third time), by jurisdiction &mdash; full data behind <a href="#e13">E13</a></caption>
    <thead>
      <tr><th scope="col">Jurisdiction</th><th scope="col">Formula credit at 122 overnights</th></tr>
    </thead>
    <tbody>
      <tr><td>Alabama</td><td>No</td></tr>
      <tr><td>Alaska</td><td>Yes</td></tr>
      <tr><td>Arizona</td><td>Yes</td></tr>
      <tr><td>Arkansas</td><td>No</td></tr>
      <tr><td>California</td><td>Yes</td></tr>
      <tr><td>Colorado</td><td>Yes</td></tr>
      <tr><td>Connecticut</td><td>No</td></tr>
      <tr><td>Delaware</td><td>Yes</td></tr>
      <tr><td>District of Columbia</td><td>No</td></tr>
      <tr><td>Florida</td><td>Yes</td></tr>
      <tr><td>Georgia</td><td>Yes</td></tr>
      <tr><td>Hawaii</td><td>No</td></tr>
      <tr><td>Idaho</td><td>Yes</td></tr>
      <tr><td>Illinois</td><td>No</td></tr>
      <tr><td>Indiana</td><td>Yes</td></tr>
      <tr><td>Iowa</td><td>No</td></tr>
      <tr><td>Kansas</td><td>No</td></tr>
      <tr><td>Kentucky</td><td>Yes</td></tr>
      <tr><td>Louisiana</td><td>No</td></tr>
      <tr><td>Maine</td><td>No</td></tr>
      <tr><td>Maryland</td><td>Yes</td></tr>
      <tr class="is-reader-state"><td>Massachusetts<span class="visually-hidden">, this page&rsquo;s worked example</span></td><td>No</td></tr>
      <tr><td>Michigan</td><td>Yes</td></tr>
      <tr><td>Minnesota</td><td>Yes</td></tr>
      <tr><td>Mississippi</td><td>No</td></tr>
      <tr><td>Missouri</td><td>Yes</td></tr>
      <tr><td>Montana</td><td>Yes</td></tr>
      <tr><td>Nebraska</td><td>No</td></tr>
      <tr><td>Nevada</td><td>No</td></tr>
      <tr><td>New Hampshire</td><td>No</td></tr>
      <tr><td>New Jersey</td><td>Yes</td></tr>
      <tr><td>New Mexico</td><td>No</td></tr>
      <tr><td>New York</td><td>No</td></tr>
      <tr><td>North Carolina</td><td>No</td></tr>
      <tr><td>North Dakota</td><td>Yes</td></tr>
      <tr><td>Ohio</td><td>Yes</td></tr>
      <tr><td>Oklahoma</td><td>Yes</td></tr>
      <tr><td>Oregon</td><td>Yes</td></tr>
      <tr><td>Pennsylvania</td><td>No</td></tr>
      <tr><td>Rhode Island</td><td>No</td></tr>
      <tr><td>South Carolina</td><td>Yes</td></tr>
      <tr><td>South Dakota</td><td>Yes</td></tr>
      <tr><td>Tennessee</td><td>Yes</td></tr>
      <tr><td>Texas</td><td>No</td></tr>
      <tr><td>Utah</td><td>Yes</td></tr>
      <tr><td>Vermont</td><td>Yes</td></tr>
      <tr><td>Virginia</td><td>Yes</td></tr>
      <tr><td>Washington</td><td>No</td></tr>
      <tr><td>West Virginia</td><td>No</td></tr>
      <tr><td>Wisconsin</td><td>Yes</td></tr>
      <tr><td>Wyoming</td><td>Yes</td></tr>
    </tbody>
  </table>
  </div>

</details>

<figure class="exhibit" id="e16">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E16-where-each-presumptive-schedule-stops-51.png"
     data-caption="Massachusetts's presumptive formula runs to $450,000; 12 schedules run higher, 28 stop lower."
     data-csv-href="/figures/working/fig9_schedule_ceilings.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E16-where-each-presumptive-schedule-stops-51.png"
         loading="lazy"
         alt="Horizontal bar chart ranking 41 jurisdictions by the combined income at which their presumptive child support schedule stops, Massachusetts highlighted.">
  </a>
  <figcaption>
    <p class="confidence-tag">Tiered: a single fact pattern; see method</p>
    <h3 class="exhibit-title">Massachusetts's presumptive formula runs to $450,000; 12 schedules run higher, 28 stop lower.</h3>
    <p class="exhibit-deck">Combined income at which each state's presumptive schedule ends; above it, support is discretionary.</p>
    <dl class="exhibit-facts">
      <div><dt>Ranked</dt><dd>41 combined-income schedules (29 gross, 11 net, 1 other basis)</dd></div>
      <div><dt>Not ranked</dt><dd>10: percentage-of-obligor, Melson or open formula</dd></div>
      <div><dt>Basis</dt><dd>Annual; monthly ×12, weekly ×52</dd></div>
    </dl>
    <p class="exhibit-notes">Forty-one jurisdictions have a combined-income schedule that stops at a stated figure: median $360,000, seven stop at exactly $40,000 a month, Utah's runs to $1.2 million. Ten use a percentage-of-obligor, Melson, or open formula with no combined ceiling. Net-income ceilings aren't dollar-for-dollar comparable with gross ones. Not ranked: Alaska, California, Delaware, Hawaii, Mississippi, Montana, Nevada, North Dakota, Texas, Wisconsin. This corrects an earlier comparison against nine benchmark states, where Massachusetts appeared second; among the 41 with a stated ceiling it is thirteenth.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig9_ceilings.py</code> ·
      <a href="/data/fifty-state/ceilings-2026-09-06.json">data (JSON)</a> ·
      <a href="/figures/working/fig9_schedule_ceilings.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<details>
<summary>Full ranking behind E16: 41 combined-income schedules</summary>

  <div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable data table for E16">
    <table class="exhibit-table" id="e16-table">
    <caption>Combined income at which the presumptive schedule stops &mdash; full data behind <a href="#e16">E16</a></caption>
    <thead>
      <tr><th scope="col">Rank</th><th scope="col">Jurisdiction</th><th scope="col" class="numeric">Combined-income ceiling</th><th scope="col">Basis</th></tr>
    </thead>
    <tbody>
      <tr><td>1</td><td>Utah</td><td class="numeric">$1,200,000</td><td>gross</td></tr>
      <tr><td>2</td><td>Louisiana</td><td class="numeric">$600,000</td><td>gross</td></tr>
      <tr><td>3</td><td>Washington</td><td class="numeric">$600,000</td><td>net</td></tr>
      <tr><td>4</td><td>Virginia</td><td class="numeric">$510,000</td><td>gross</td></tr>
      <tr><td>5</td><td>Colorado</td><td class="numeric">$480,000</td><td>gross</td></tr>
      <tr><td>6</td><td>Georgia</td><td class="numeric">$480,000</td><td>gross</td></tr>
      <tr><td>7</td><td>Missouri</td><td class="numeric">$480,000</td><td>gross</td></tr>
      <tr><td>8</td><td>New Mexico</td><td class="numeric">$480,000</td><td>gross</td></tr>
      <tr><td>9</td><td>North Carolina</td><td class="numeric">$480,000</td><td>gross</td></tr>
      <tr><td>10</td><td>Rhode Island</td><td class="numeric">$480,000</td><td>gross</td></tr>
      <tr><td>11</td><td>South Carolina</td><td class="numeric">$480,000</td><td>gross</td></tr>
      <tr><td>12</td><td>Indiana</td><td class="numeric">$478,400</td><td>gross</td></tr>
      <tr class="is-reader-state"><td>13</td><td>Massachusetts<span class="visually-hidden">, this page&rsquo;s worked example</span></td><td class="numeric">$450,000</td><td>gross</td></tr>
      <tr><td>14</td><td>Idaho</td><td class="numeric">$440,000</td><td>gross</td></tr>
      <tr><td>15</td><td>West Virginia</td><td class="numeric">$420,000</td><td>gross</td></tr>
      <tr><td>16</td><td>Maine</td><td class="numeric">$400,000</td><td>gross</td></tr>
      <tr><td>17</td><td>New Hampshire</td><td class="numeric">$373,068</td><td>gross</td></tr>
      <tr><td>18</td><td>Vermont</td><td class="numeric">$360,300</td><td>other</td></tr>
      <tr><td>19</td><td>Alabama</td><td class="numeric">$360,000</td><td>gross</td></tr>
      <tr><td>20</td><td>Arizona</td><td class="numeric">$360,000</td><td>gross</td></tr>
      <tr><td>21</td><td>Arkansas</td><td class="numeric">$360,000</td><td>gross</td></tr>
      <tr><td>22</td><td>Iowa</td><td class="numeric">$360,000</td><td>net</td></tr>
      <tr><td>23</td><td>Kentucky</td><td class="numeric">$360,000</td><td>gross</td></tr>
      <tr><td>24</td><td>Maryland</td><td class="numeric">$360,000</td><td>gross</td></tr>
      <tr><td>25</td><td>Oregon</td><td class="numeric">$360,000</td><td>gross</td></tr>
      <tr><td>26</td><td>Pennsylvania</td><td class="numeric">$360,000</td><td>net</td></tr>
      <tr><td>27</td><td>South Dakota</td><td class="numeric">$360,000</td><td>net</td></tr>
      <tr><td>28</td><td>Tennessee</td><td class="numeric">$339,000</td><td>gross</td></tr>
      <tr><td>29</td><td>Ohio</td><td class="numeric">$336,000</td><td>gross</td></tr>
      <tr><td>30</td><td>Illinois</td><td class="numeric">$328,500</td><td>net</td></tr>
      <tr><td>31</td><td>Connecticut</td><td class="numeric">$312,000</td><td>net</td></tr>
      <tr><td>32</td><td>District of Columbia</td><td class="numeric">$240,000</td><td>gross</td></tr>
      <tr><td>33</td><td>Minnesota</td><td class="numeric">$240,000</td><td>gross</td></tr>
      <tr><td>34</td><td>Nebraska</td><td class="numeric">$240,000</td><td>net</td></tr>
      <tr><td>35</td><td>Kansas</td><td class="numeric">$216,000</td><td>gross</td></tr>
      <tr><td>36</td><td>Michigan</td><td class="numeric">$214,459</td><td>net</td></tr>
      <tr><td>37</td><td>New York</td><td class="numeric">$193,000</td><td>gross</td></tr>
      <tr><td>38</td><td>New Jersey</td><td class="numeric">$187,200</td><td>net</td></tr>
      <tr><td>39</td><td>Oklahoma</td><td class="numeric">$180,000</td><td>gross</td></tr>
      <tr><td>40</td><td>Wyoming</td><td class="numeric">$180,000</td><td>net</td></tr>
      <tr><td>41</td><td>Florida</td><td class="numeric">$120,000</td><td>net</td></tr>
    </tbody>
  </table>
  </div>

</details>

<figure class="exhibit" id="e17">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E17-ma-equal-time-vs-others-primary-custody.png"
     data-caption="Only Wisconsin and Hawaii order more than Massachusetts does at equal time."
     data-csv-href="/figures/working/fig10_ma_shared_vs_primary.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E17-ma-equal-time-vs-others-primary-custody.png"
         loading="lazy"
         alt="Horizontal bar chart of Massachusetts's equal-time order against 49 other jurisdictions' primary-custody orders, with Massachusetts's own primary-custody order marked for scale.">
  </a>
  <figcaption>
    <p class="confidence-tag">Tiered: a single fact pattern; see method</p>
    <h3 class="exhibit-title">Only Wisconsin and Hawaii order more than Massachusetts does at equal time.</h3>
    <p class="exhibit-deck">Monthly order: Massachusetts under Box 1 (children half the time each) against every other jurisdiction with the children primarily with the lower earner.</p>
    <dl class="exhibit-facts">
      <div><dt>Custody</dt><dd>MA equal time (Box 1) vs others primary</dd></div>
      <div><dt>Children</dt><dd>3</dd></div>
      <div><dt>Child care</dt><dd>None (base support)</dd></div>
      <div><dt>Incomes</dt><dd>$201,000 / $29,640</dd></div>
    </dl>
    <p class="exhibit-notes">Only Hawaii and Wisconsin order more at primary custody than Massachusetts does at equal time. Massachusetts's own primary-custody order, $4,714, is marked for scale and isn't part of the ranked comparison. The Commonwealth's consultant attributes the higher amounts to cost of living, which bears on both households; whatever it explains about the level, it doesn't explain why an arrangement giving each parent half the time is priced where sole primary custody is priced almost everywhere else. One fact pattern; Georgia held out (see E11).</p>
    <p class="exhibit-source">Source: <code>model/charts/fig10_ma_shared_vs_primary.py</code> ·
      <a href="/data/fifty-state/tier-50-2026-09-05.json">data (JSON)</a> ·
      <a href="/figures/working/fig10_ma_shared_vs_primary.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<details>
<summary>Full ranking behind E17: Massachusetts vs. 49 other jurisdictions' primary-custody orders</summary>

  <div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable data table for E17">
    <table class="exhibit-table" id="e17-table">
    <caption>Massachusetts&rsquo;s equal-time order vs. every other jurisdiction&rsquo;s primary-custody order &mdash; full data behind <a href="#e17">E17</a></caption>
    <thead>
      <tr><th scope="col">Rank</th><th scope="col">Jurisdiction</th><th scope="col">Custody basis</th><th scope="col" class="numeric">Monthly order</th></tr>
    </thead>
    <tbody>
      <tr><td>1</td><td>Hawaii</td><td>Primary, lower earner</td><td class="numeric">$5,821.00</td></tr>
      <tr class="is-reader-state"><td>&mdash;</td><td>Massachusetts<span class="visually-hidden">, this page&rsquo;s worked example</span></td><td>Primary (Box 2) &mdash; for scale, not ranked</td><td class="numeric">$4,714.22</td></tr>
      <tr><td>2</td><td>Wisconsin</td><td>Primary, lower earner</td><td class="numeric">$4,491.71</td></tr>
      <tr class="is-reader-state"><td>3</td><td>Massachusetts<span class="visually-hidden">, this page&rsquo;s worked example</span></td><td>Equal time (Box 1)</td><td class="numeric">$4,388.48</td></tr>
      <tr><td>4</td><td>New York</td><td>Primary, lower earner</td><td class="numeric">$4,067.61</td></tr>
      <tr><td>5</td><td>Delaware</td><td>Primary, lower earner</td><td class="numeric">$3,990.73</td></tr>
      <tr><td>6</td><td>New Hampshire</td><td>Primary, lower earner</td><td class="numeric">$3,838.66</td></tr>
      <tr><td>7</td><td>Kansas</td><td>Primary, lower earner</td><td class="numeric">$3,838.03</td></tr>
      <tr><td>8</td><td>Iowa</td><td>Primary, lower earner</td><td class="numeric">$3,744.73</td></tr>
      <tr><td>9</td><td>Texas</td><td>Primary, lower earner</td><td class="numeric">$3,510.00</td></tr>
      <tr><td>10</td><td>District of Columbia</td><td>Primary, lower earner</td><td class="numeric">$3,467.96</td></tr>
      <tr><td>11</td><td>Alaska</td><td>Primary, lower earner</td><td class="numeric">$3,462.96</td></tr>
      <tr><td>12</td><td>California</td><td>Primary, lower earner</td><td class="numeric">$3,436.04</td></tr>
      <tr><td>13</td><td>Maryland</td><td>Primary, lower earner</td><td class="numeric">$3,295.11</td></tr>
      <tr><td>14</td><td>Louisiana</td><td>Primary, lower earner</td><td class="numeric">$3,269.06</td></tr>
      <tr><td>15</td><td>North Dakota</td><td>Primary, lower earner</td><td class="numeric">$3,219.00</td></tr>
      <tr><td>16</td><td>Missouri</td><td>Primary, lower earner</td><td class="numeric">$3,139.00</td></tr>
      <tr><td>17</td><td>Connecticut</td><td>Primary, lower earner</td><td class="numeric">$3,138.20</td></tr>
      <tr><td>18</td><td>Rhode Island</td><td>Primary, lower earner</td><td class="numeric">$3,123.22</td></tr>
      <tr><td>19</td><td>Colorado</td><td>Primary, lower earner</td><td class="numeric">$3,090.30</td></tr>
      <tr><td>20</td><td>Pennsylvania</td><td>Primary, lower earner</td><td class="numeric">$3,086.76</td></tr>
      <tr><td>21</td><td>Montana</td><td>Primary, lower earner</td><td class="numeric">$3,073.50</td></tr>
      <tr><td>22</td><td>Illinois</td><td>Primary, lower earner</td><td class="numeric">$3,037.90</td></tr>
      <tr><td>23</td><td>New Jersey</td><td>Primary, lower earner</td><td class="numeric">$3,002.31</td></tr>
      <tr><td>24</td><td>North Carolina</td><td>Primary, lower earner</td><td class="numeric">$2,934.30</td></tr>
      <tr><td>25</td><td>Maine</td><td>Primary, lower earner</td><td class="numeric">$2,899.02</td></tr>
      <tr><td>26</td><td>Washington</td><td>Primary, lower earner</td><td class="numeric">$2,819.56</td></tr>
      <tr><td>27</td><td>Michigan</td><td>Primary, lower earner</td><td class="numeric">$2,808.44</td></tr>
      <tr><td>28</td><td>Wyoming</td><td>Primary, lower earner</td><td class="numeric">$2,801.97</td></tr>
      <tr><td>29</td><td>New Mexico</td><td>Primary, lower earner</td><td class="numeric">$2,795.32</td></tr>
      <tr><td>30</td><td>Alabama</td><td>Primary, lower earner</td><td class="numeric">$2,736.00</td></tr>
      <tr><td>31</td><td>Virginia</td><td>Primary, lower earner</td><td class="numeric">$2,672.09</td></tr>
      <tr><td>32</td><td>South Carolina</td><td>Primary, lower earner</td><td class="numeric">$2,669.21</td></tr>
      <tr><td>33</td><td>South Dakota</td><td>Primary, lower earner</td><td class="numeric">$2,623.12</td></tr>
      <tr><td>34</td><td>Vermont</td><td>Primary, lower earner</td><td class="numeric">$2,594.42</td></tr>
      <tr><td>35</td><td>Mississippi</td><td>Primary, lower earner</td><td class="numeric">$2,564.76</td></tr>
      <tr><td>36</td><td>Ohio</td><td>Primary, lower earner</td><td class="numeric">$2,564.15</td></tr>
      <tr><td>37</td><td>Idaho</td><td>Primary, lower earner</td><td class="numeric">$2,549.85</td></tr>
      <tr><td>38</td><td>Indiana</td><td>Primary, lower earner</td><td class="numeric">$2,548.03</td></tr>
      <tr><td>39</td><td>West Virginia</td><td>Primary, lower earner</td><td class="numeric">$2,518.77</td></tr>
      <tr><td>40</td><td>Florida</td><td>Primary, lower earner</td><td class="numeric">$2,512.99</td></tr>
      <tr><td>41</td><td>Nevada</td><td>Primary, lower earner</td><td class="numeric">$2,485.00</td></tr>
      <tr><td>42</td><td>Nebraska</td><td>Primary, lower earner</td><td class="numeric">$2,402.03</td></tr>
      <tr><td>43</td><td>Arkansas</td><td>Primary, lower earner</td><td class="numeric">$2,349.64</td></tr>
      <tr><td>44</td><td>Utah</td><td>Primary, lower earner</td><td class="numeric">$2,332.66</td></tr>
      <tr><td>45</td><td>Arizona</td><td>Primary, lower earner</td><td class="numeric">$2,290.06</td></tr>
      <tr><td>46</td><td>Minnesota</td><td>Primary, lower earner</td><td class="numeric">$2,271.30</td></tr>
      <tr><td>47</td><td>Tennessee</td><td>Primary, lower earner</td><td class="numeric">$2,031.00</td></tr>
      <tr><td>48</td><td>Oklahoma</td><td>Primary, lower earner</td><td class="numeric">$2,008.78</td></tr>
      <tr><td>49</td><td>Kentucky</td><td>Primary, lower earner</td><td class="numeric">$1,871.67</td></tr>
      <tr><td>50</td><td>Oregon</td><td>Primary, lower earner</td><td class="numeric">$1,772.00</td></tr>
    </tbody>
  </table>
  </div>

</details>

## The gross-versus-net question

<figure class="exhibit" id="e27">
  <a class="lightbox-trigger" data-lightbox href="/figures/exhibits/E27-gross-vs-net-deferred-1-of-5-cycles.png"
     data-caption="Five reviews have taken up gross versus net. None changed it."
     data-csv-href="/figures/working/fig11_deferral_timeline.csv" data-csv-label="Data (CSV)">
  <img src="/figures/exhibits/E27-gross-vs-net-deferred-1-of-5-cycles.png"
         loading="lazy"
         alt="Timeline of seven Massachusetts child support guidelines reviews from 2002 to 2025, marking the five whose own report or economic review declined to move from gross to net income.">
  </a>
  <figcaption>
    <p class="confidence-tag">Documentary: built only from primary-text quotes</p>
    <h3 class="exhibit-title">Five reviews have taken up gross versus net. None changed it.</h3>
    <p class="exhibit-deck">Massachusetts guidelines reviews since 2002. Filled: the cycle's own report or economic review declines the change.</p>
    <dl class="exhibit-facts">
      <div><dt>Question</dt><dd>Gross vs. net income basis (not the separate alimony/tax question)</dd></div>
      <div><dt>Corpus</dt><dd>Every task force report and economic review, 2001 to 2025</dd></div>
      <div><dt>Cycles</dt><dd>7 reviews, 2002 to 2025</dd></div>
    </dl>
    <p class="exhibit-notes">Every filled year carries a verbatim quote from that cycle's own report or economic review, with page numbers in the source file. The 2009 Task Force found "little support ... for basing orders on net income"; the 2012 Task Force "declines to recommend this change." The 2002 and 2006 cycles say nothing on the question.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig11_deferral_timeline.py</code> ·
      <a href="/data/deferrals-gross-vs-net.json">data (JSON)</a> ·
      <a href="/figures/working/fig11_deferral_timeline.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<div class="ask">
<h2>Check any of these yourself</h2>
<p>Every figure above is drawn by a script under <code>model/charts/</code> from the models and
datasets linked from its own Source line. Rebuild the whole set with
<code>model/charts/make_all.py</code>, then the exhibit crop with
<code>model/charts/exhibits.py</code>; every PNG has a CSV or dataset beside it holding the values
actually plotted.</p>
<ul>
  <li><a href="/the-model/">The model</a></li>
  <li><a href="/the-data/">The data</a></li>
  <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
</ul>
</div>
