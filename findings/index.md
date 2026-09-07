---
layout: page
title: Findings
description: >-
  Four places where the Massachusetts Child Support Guidelines Worksheet's own arithmetic works
  against its own text, each pinned by a test suite against the form's own calculation scripts,
  plus one fifty-one-jurisdiction comparison at a single fact pattern.
---

# Four internal inconsistencies in the worksheet's own arithmetic, and one cross-jurisdiction comparison

Each finding below reproduces one part of the Massachusetts Child Support Guidelines Worksheet
(form CJ-D 304, 2025 edition) in code, checks it against the form's own embedded calculation
scripts, and states what the arithmetic does that the guidelines' own text does not say. The first
three are internal; they hold regardless of what any particular family's incomes are. The fourth
compares Massachusetts's order at one fact pattern against fifty other jurisdictions' own
guidelines, and is tiered accordingly: it generalizes to nothing beyond that one fact pattern.

<ul class="finding-list">
  <li class="finding-card">
    <h3><a href="/findings/hardship-test/">The hardship test reads a different income than the order pays from</a></h3>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <p>Section IV.C presumes hardship once an order reaches 40 percent of a payor's available income, but
    Line 7e computes that share on gross-derived income while the order itself is paid from net. At the
    worked example, the true burden already exceeds 40 percent of net income at $80 a week of claimed
    child care, while Line 7e does not report 40 percent until $590 a week, by which point the real
    share is 57 percent.</p>
    <p class="stat-callout">
      <span class="stat-value">57%</span>
      <span class="stat-label">of the payor's net income at the worked example, at the point Line 7e itself still reads 40%</span>
    </p>
  </li>
  <li class="finding-card">
    <h3><a href="/findings/child-care/">Child care is split on income the order has already changed</a></h3>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <p>Line 3c allocates child care on each parent's income share before the base child support order has
    moved any money between the households. At the worked example this assigns 87.7 percent of a $15,600
    child care bill to the payor; recomputing the shares after the transfer gives 64.5 percent, and
    after-tax shares give 48.2 percent.</p>
    <p class="stat-callout">
      <span class="stat-value">88 cents</span>
      <span class="stat-label">of every dollar of claimed child care, funded by the payor at the worked example, on an income share computed before the order moves any money</span>
    </p>
  </li>
  <li class="finding-card">
    <h3><a href="/findings/parenting-time/">The credit for equal parenting time contains no parenting-time term</a></h3>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <p>Line 6g nets the two parents' Line 6e amounts, which reduce to the difference in their income
    shares once Box 1 assigns zero children to the payor's column; nothing in the calculation multiplies
    by any share of overnights. So the reduction the credit produces for equal parenting time collapses as
    the income gap between the parents widens: 77.6 percent at a 56.3 percent payor income share, 6.9
    percent at the worked example's 87.7 percent, and 1.3 percent at 95.8 percent.</p>
    <p class="stat-callout">
      <span class="stat-value">6.9%</span>
      <span class="stat-label">the reduction equal parenting time earns at the worked example, down from 77.6% when the other parent earns much less</span>
    </p>
  </li>
  <li class="finding-card">
    <h3><a href="/findings/fifty-one-jurisdictions/">Massachusetts's equal-time order exceeds 47 of 49 other jurisdictions' primary orders</a></h3>
    <p class="confidence-tag">Tiered: one fact pattern, not a distribution; see method</p>
    <p>At one fact pattern (three children, $201,000 and $29,640 a year, no child care), fifty of
    fifty-one jurisdictions were profiled from primary documents, computed twice independently,
    reconciled, and checked by an adversarial review; Georgia was held out because its enacted formula
    orders less at equal time than at primary custody. Comparing Massachusetts's own equal-time order
    against every other jurisdiction's primary-custody order at that pattern, only Hawaii and Wisconsin
    order more than Massachusetts does at equal time.</p>
    <p class="stat-callout">
      <span class="stat-value">47 of 49</span>
      <span class="stat-label">other ranked jurisdictions' primary-custody orders, exceeded by Massachusetts's own equal-time order at one fact pattern</span>
    </p>
  </li>
</ul>

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every number above traces to a script and a printed run in this repository. See
  <a href="/the-model/">the model</a> and <a href="/the-data/">the data</a> for the full list, or
  each finding's own "Check it yourself" section for the exact file behind its numbers.</p>
</div>
