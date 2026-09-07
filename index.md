---
layout: page
title: The Massachusetts child support worksheet, checked against its own arithmetic
description: >-
  A code reproduction of the Massachusetts Child Support Guidelines Worksheet (CJ-D 304, 2025),
  checked against the form's own calculation scripts, finds three internal inconsistencies and one
  fifty-one-jurisdiction comparison. Every number here traces to a file in this repository.
---

<div class="hero">
  <p class="eyebrow">Massachusetts Child Support Guidelines Worksheet, verified in code</p>
  <h1>Massachusetts's hardship test reads 40 percent when a payor is already at 57 percent of net income.</h1>
  <p class="lede">This site reproduces the Massachusetts Child Support Guidelines Worksheet (form CJ-D 304,
  2025 edition) in code, checks it against the form's own calculation scripts, and finds three places
  where the worksheet's arithmetic works against its own text, plus one fifty-one-jurisdiction
  comparison. Section IV.C presumes hardship at 40 percent of a payor's income; at the worked example,
  that payor's true share of net income is already 57 percent by the time the form itself still reads
  40.</p>
</div>

<div class="disclosure">
  <p>The worked example throughout — including the order above — is my own child support order,
  disclosed here because a reader should be able to check whether the arithmetic changes when the numbers
  are real rather than illustrative. It doesn't: the same defects hold across the income ranges charted on
  each finding's page, not only at my own figures. The model that produced every number here is at
  <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>, with the test suites that pin it to
  the form's own calculation scripts.</p>
</div>

## What the worksheet does that its text does not say

<ul class="finding-list">
  <li class="finding-card">
    <h3><a href="/findings/hardship-test/">The hardship test reads a different income than the order pays from</a></h3>
    <p class="confidence-tag">Verified against the form's own calculation scripts</p>
    <p>Section IV.C presumes hardship once an order reaches 40 percent of a payor's available income, but
    Line 7e computes that share on gross-derived income while the order itself is paid from net. At the
    worked example, the true burden already exceeds 40 percent of net income at $80 a week of claimed
    child care, while Line 7e does not report 40 percent until $590 a week — by which point the real
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
    shares once Box 1 assigns zero children to the payor's column — nothing in the calculation multiplies
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
    <p class="confidence-tag">Tiered — one fact pattern, not a distribution; see method</p>
    <p>At one fact pattern — three children, $201,000 and $29,640 a year, no child care — fifty of
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

## Line 7e's reading diverges from the true burden as child care rises

<figure class="exhibit" id="e05">
  <img src="/figures/exhibits/E05-what-line-7e-sees-vs-true-burden-worked-example.png"
       alt="Line chart of Line 7e's reported percentage versus the true share of the payor's net
            income, against child care claimed from $0 to $600 a week, at the worked example.">
  <figcaption>
    <h3 class="exhibit-title">The hardship valve fires late because it reads the wrong income.</h3>
    <p class="exhibit-deck">Line 7e's reading vs. the true burden as claimed child care rises, worked example.</p>
    <p class="exhibit-notes">The true burden passes 40% of net at $80/week of child care; Line 7e reports 40% at $590/week, by which point the true burden is 57%.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig6_valve.py</code> ·
      <a href="/figures/working/fig6_valve_units_lag.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every number above traces to a script and a printed run in this repository. Each link below goes to
  the specific test and run output for one finding, not to a general resources page.</p>
  <ul>
    <li><strong>The hardship test:</strong> <a href="/model/test_worksheet.py"><code>model/test_worksheet.py</code></a>
      pins Line 7e to the form's own calculation scripts; <a href="/model/runs/submission-figures-run-2026-09-05.txt">the printed run</a>
      shows the 40/57 percent gap.</li>
    <li><strong>Child care allocation:</strong> <a href="/model/childcare_post_transfer.py"><code>model/childcare_post_transfer.py</code></a>
      and its <a href="/model/test_childcare_post_transfer.py">test suite</a>;
      <a href="/model/runs/childcare-post-transfer-run-2026-09-05.txt">the printed run</a>.</li>
    <li><strong>The parenting-time credit:</strong> <a href="/model/box1_fix.py"><code>model/box1_fix.py</code></a>
      and its <a href="/model/test_box1_fix.py">test suite</a>;
      <a href="/model/runs/box1-fix-run-2026-09-05.txt">the printed run</a>.</li>
    <li><strong>Fifty-one jurisdictions:</strong> <a href="/data/fifty-state/tier-50-2026-09-05.json">the dataset</a>
      and <a href="/model/charts/fig5_states.py"><code>model/charts/fig5_states.py</code></a>, the script that reads it.</li>
  </ul>
</div>

## Documents

<ul class="doc-list">
  <li class="doc-item">
    <span class="doc-title">Comments to the Trial Court, with Attachments A and D</span>
    <span class="confidence-tag">Prepared for submission — not yet sent</span>
    <span class="doc-context">The full submission as it will go to the Chief Justice, with the redline
      language for each of the findings above.
      <a href="/paper/Comments-to-the-Trial-Court-with-Attachments-A-and-D.pdf">PDF</a></span>
  </li>
  <li class="doc-item">
    <span class="doc-title">Attachment E — Figures</span>
    <span class="confidence-tag">Working paper appendix, externally reviewed</span>
    <span class="doc-context">All seventeen figures with their captions, for the working paper version
      of this analysis. <a href="/paper/Attachment-E-figures.pdf">PDF</a></span>
  </li>
</ul>

<p>The full document list, with context and confidence for each, is at <a href="/documents/">Documents</a>.</p>
