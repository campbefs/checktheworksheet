---
layout: page
title: Findings
description: >-
  Four places where the Massachusetts Child Support Guidelines Worksheet's own arithmetic works
  against its own text, each pinned by a test suite against the form's own calculation scripts,
  plus one fifty-one-jurisdiction comparison at a single fact pattern.
disclosure:
  - >-
    The stat on each card below (57%, 88 cents, 6.9%, 47 of 49) comes from the worked example
    used throughout this site: my own child support order, three children, my income and my
    children's mother's income entered as the Worksheet requires. Each finding page states why,
    and shows the same gap holding across a range of incomes, not only at my own figures.
  - >-
    Every number traces to <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>,
    checked by <a href="/model/test_worksheet.py"><code>model/test_worksheet.py</code></a>
    against the form's own calculation scripts. More on <a href="/about/">About</a>.
---

# Four internal inconsistencies in the worksheet's own arithmetic, and one cross-jurisdiction comparison

{% include disclosure.html %}

Each finding below reproduces one part of the Massachusetts Child Support Guidelines Worksheet
(form CJ-D 304, 2025 edition) in code, checks it against the form's own embedded calculation
scripts, and states what the arithmetic does that the guidelines' own text does not say. The first
three are internal; they hold regardless of what any particular family's incomes are. The fourth
compares Massachusetts's order at one fact pattern against fifty other jurisdictions' own
guidelines, and is tiered accordingly: it generalizes to nothing beyond that one fact pattern.

<h2 class="vh">The four findings</h2>

<div class="finding-grid">

<article class="finding-card">
  <div class="thumb"><img src="/figures/exhibits/E05-what-line-7e-sees-vs-true-burden-worked-example.png" alt="Line chart of Line 7e's reading against the true burden as child care claimed rises." loading="lazy"></div>
  <div class="body">
    <p class="tag">Verified against the form's own calculation scripts</p>
    <h3><a href="/findings/hardship-test/">The hardship test reads a different income than the order pays from</a></h3>
    <p>Section IV.C presumes hardship at 40 percent of a payor's available income, but Line 7e
    computes that share on gross-derived income while the order itself is paid from net.</p>
    <div class="stat">
      <span class="stat-value">57%</span>
      <span class="stat-label">of the payor's net income, at the worked example, the moment Line 7e itself still reads 40%</span>
    </div>
  </div>
</article>

<article class="finding-card">
  <div class="thumb"><img src="/figures/exhibits/E06-child-care-share-three-rules-worked-example.png" alt="Bar chart of the payor's share of a child care bill under three allocation rules." loading="lazy"></div>
  <div class="body">
    <p class="tag">Verified against the form's own calculation scripts</p>
    <h3><a href="/findings/child-care/">Child care is split on income the order has already changed</a></h3>
    <p>Line 3c allocates child care on each parent's income share before the base support order
    has moved any money between the households, and never revisits it.</p>
    <div class="stat">
      <span class="stat-value">88&cent;</span>
      <span class="stat-label">of every dollar of claimed child care, funded by the payor at the worked example, on an income share computed before the order moves any money</span>
    </div>
  </div>
</article>

<article class="finding-card">
  <div class="thumb"><img src="/figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png" alt="Line chart of the equal-parenting-time credit collapsing as the income gap widens." loading="lazy"></div>
  <div class="body">
    <p class="tag">Verified against the form's own calculation scripts</p>
    <h3><a href="/findings/parenting-time/">The credit for equal parenting time contains no parenting-time term</a></h3>
    <p>Line 6g nets the two parents' Line 6e amounts, which reduce to the difference in their
    income shares once Box 1 assigns zero children to the payor's column; nothing multiplies by
    any share of overnights.</p>
    <div class="stat">
      <span class="stat-value">6.9%</span>
      <span class="stat-label">the credit equal parenting time earns at the worked example, down from 77.6% when the other parent earns much less</span>
    </div>
  </div>
</article>

<article class="finding-card">
  <div class="thumb"><img src="/figures/exhibits/E12-fifty-states-lower-earner-primary-one-fact-pattern.png" alt="Bar chart ranking fifty jurisdictions' primary-custody child support orders." loading="lazy"></div>
  <div class="body">
    <p class="tag">Tiered: one fact pattern, not a distribution; see method</p>
    <h3><a href="/findings/fifty-one-jurisdictions/">Massachusetts's equal-time order exceeds 47 of 49 other jurisdictions' primary orders</a></h3>
    <p>At one fact pattern, fifty of fifty-one jurisdictions were profiled from primary documents,
    computed twice independently, reconciled, and adversarially attacked. Georgia was held out
    because its enacted formula orders less at equal time than at primary custody.</p>
    <div class="stat">
      <span class="stat-value">47 of 49</span>
      <span class="stat-label">other ranked jurisdictions' primary-custody orders, exceeded by Massachusetts's own equal-time order at one fact pattern</span>
    </div>
  </div>
</article>

</div>

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every number above traces to a script and a printed run in this repository. See
  <a href="/the-model/">the model</a> and <a href="/the-data/">the data</a> for the full list, or
  each finding's own "Check it yourself" section for the exact file behind its numbers.</p>
</div>
