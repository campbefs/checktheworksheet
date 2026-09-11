---
layout: page
title: The model
description: >-
  A Python reproduction of the Massachusetts worksheet, a tax model, three extension models,
  four test suites, and a harness that runs the official form's own scripts against the model.
---

# A model of the worksheet, checked against the form's own scripts as well as against itself

[Findings](/findings/) states what the checks show. This page is the proof.

## `model/worksheet.py` reimplements CJ-D 304 line by line

[`model/worksheet.py`](/model/worksheet.py) transcribes the 2025 Guidelines Worksheet start to
finish: income, income shares and cap, Table A and B, the age adjustment, the low-income floor,
child care, the income-disparity adjustment, the hardship test, and all three custody boxes.
[`model/guidelines.py`](/model/guidelines.py) holds Table A and B as published, checked against
all 1,104 rows of the Commonwealth's own Guidelines Chart
([`data/extracted/guidelines-chart.json`](/data/extracted/guidelines-chart.json)), with no
disagreement over one dollar.

## A tax model computes what each party actually keeps

[`model/net_position.py`](/model/net_position.py) converts gross income to spendable income after
tax, so a finding can compare an order against what a household spends. Every published figure on
this site uses its withholding basis: federal income tax, Massachusetts income tax, and Social
Security and Medicare, the same formula for both parents, no filing status, no dependents, no
credits — reproducible from a published table by anyone. The module can also compute a
credits-inclusive figure, adding the EITC, Child Tax Credit, and the refundable Massachusetts
Child and Family Tax Credit; that mode is not used for any published figure and is exposed only as
the calculator's optional "count credits" view, [explained on its own
page](/credits/).

## Three extension models, and one script printing every quoted figure

- [`model/box1_fix.py`](/model/box1_fix.py): the Box 1 equal-parenting credit, and three
  redlines that give it a parenting-time term.
- [`model/childcare_post_transfer.py`](/model/childcare_post_transfer.py): child care split on
  income shares measured *after* base support transfers, not Line 6b's pre-transfer shares.
- [`model/marginal_retention.py`](/model/marginal_retention.py): how much of the payor's next
  dollar is kept after tax.
- [`model/submission_figures.py`](/model/submission_figures.py): prints every figure quoted to
  the Trial Court, so none is quoted without a script producing it.
- [`model/recommendations.py`](/model/recommendations.py): the figures behind the
  [recommendations page](/recommendations/), including the fifty-state medians and the child-care
  split options.

## Four test suites, 358 checks, all passing, gate every quoted number

| Suite | Checks | What it pins |
|---|---|---|
| [`model/test_guidelines.py`](/model/test_guidelines.py) | 20 | Table A/B vs. the published chart |
| [`model/test_worksheet.py`](/model/test_worksheet.py) | 60 | The disclosed order and the form's rounding |
| [`model/test_box1_fix.py`](/model/test_box1_fix.py) | 258 | The Box 1 credit and its redlines |
| [`model/test_childcare_post_transfer.py`](/model/test_childcare_post_transfer.py) | 20 | Child care on post-transfer shares |

## A harness runs the Commonwealth's own scripts instead of a re-derivation

The published CJ-D 304 is a fillable XFA form with embedded scripts, extracted at
[`data/extracted/cjd304-xfa.xml`](/data/extracted/cjd304-xfa.xml) by
[`model/inspect_worksheet.py`](/model/inspect_worksheet.py). The dependency-free
[`model/official_xfa_harness.js`](/model/official_xfa_harness.js) (Node) executes those scripts.
[`model/run_official_xfa.py`](/model/run_official_xfa.py) runs six scenarios against
`model/worksheet.py`.

The two agree on the final order in all six:
[$1,016, $1,091, $1,355, $1,280, $1,274, $1,010](/model/runs/official-xfa-vs-model-2026-09-05.txt)
(unrounded arithmetic differs by a few dollars, e.g. $1,012.72 against $1,016, from rounding each
line before the next uses it, reproduced with `round_lines=True`). This is the project's strongest
check: the Commonwealth's own code, not another analyst's reading of the form.

## Reproduce every number here

Nothing beyond the standard library is needed, plus Node on PATH for the XFA harness. Each file
above runs as `python3 <path>`. Redrawing the figures needs `matplotlib` and `numpy`, then
`python3 model/charts/make_all.py`.

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every command above runs against files in this repository; no network access needed.</p>
  <ul>
    <li><a href="/the-data/">The data</a></li>
    <li><a href="/findings/">The findings the model produces</a></li>
  </ul>
</div>
