---
layout: page
title: The model
description: >-
  A Python reproduction of the Massachusetts worksheet, a federal and state tax model, three
  extension models, four test suites, and a harness that runs the official form's own
  calculation scripts and diffs them against the model.
---

# A model of the worksheet, checked against the form's own scripts, not just against itself

The [findings](/findings/) pages state what the checks show. This page is the proof: what is
reproduced in code, and how each part is checked.

## `model/worksheet.py` reimplements CJ-D 304 line by line

[`model/worksheet.py`](/model/worksheet.py) transcribes the 2025 Guidelines Worksheet start to
finish: gross and available income, the combined-income shares and cap, Table A and Table B, the
Table C age adjustment, the low-income floor, child care, the income-disparity adjustment and
netting, the hardship test, and all three custody boxes (shared, primary, split).

[`model/guidelines.py`](/model/guidelines.py) holds Table A and Table B as published. Table A
was checked against all 1,104 rows of the Commonwealth's own Guidelines Chart, reconstructed at
[`data/extracted/guidelines-chart.json`](/data/extracted/guidelines-chart.json), with no
disagreement over one dollar.

## A tax model computes what each party actually keeps

[`model/net_position.py`](/model/net_position.py) converts gross income to spendable income
after federal and Massachusetts tax: brackets, the EITC and Child Tax Credit, and Massachusetts's
own exemption, EITC match, and refundable Child and Family Tax Credit. This lets a finding
compare an order, computed on gross income, against what a household actually spends.

## Three extension models, and one script that prints every quoted figure

- [`model/box1_fix.py`](/model/box1_fix.py): the Box 1 equal-parenting credit, and three
  redlines that would give it a parenting-time term.
- [`model/childcare_post_transfer.py`](/model/childcare_post_transfer.py): child care split on
  income shares measured *after* the base support transfer, not the pre-transfer shares Line 6b
  uses.
- [`model/marginal_retention.py`](/model/marginal_retention.py): how much of the payor's next
  dollar is kept after tax, and the resulting change in the order.
- [`model/submission_figures.py`](/model/submission_figures.py): prints every figure quoted in
  the comments to the Trial Court, so none is quoted without a script producing it.

## Four test suites, 348 checks, gate every quoted number

| Suite | Checks | What it pins |
|---|---|---|
| [`model/test_guidelines.py`](/model/test_guidelines.py) | 20 | Table A and Table B against the published chart |
| [`model/test_worksheet.py`](/model/test_worksheet.py) | 60 | The worksheet, pinned to a real order and the form's rounding |
| [`model/test_box1_fix.py`](/model/test_box1_fix.py) | 258 | The Box 1 credit and its redline variants |
| [`model/test_childcare_post_transfer.py`](/model/test_childcare_post_transfer.py) | 10 | Child care on post-transfer shares |

All four pass as of this writing.

## A harness runs the Commonwealth's own scripts, not a re-derivation of them

The published CJ-D 304 is a fillable XFA form with its own embedded calculation scripts,
extracted at [`data/extracted/cjd304-xfa.xml`](/data/extracted/cjd304-xfa.xml) by
[`model/inspect_worksheet.py`](/model/inspect_worksheet.py).
[`model/official_xfa_harness.js`](/model/official_xfa_harness.js), a dependency-free Node
program, executes those scripts exactly as the form does; [`model/run_official_xfa.py`](/model/run_official_xfa.py)
runs six scenarios (Box 1 and Box 2, with and without child care, paid by one or both parents)
and diffs the result against `model/worksheet.py`.

In [`model/runs/official-xfa-vs-model-2026-09-05.txt`](/model/runs/official-xfa-vs-model-2026-09-05.txt),
the official scripts and the model's rounded output agree on the final weekly order in all six
scenarios: $1,016, $1,091, $1,355, $1,280, $1,274, $1,010. The unrounded arithmetic differs by a
few dollars (for example $1,012.72 against $1,016), the effect of the form rounding every line to
the cent before the next line uses it, reproduced with `round_lines=True`. This is the project's
strongest check: the Commonwealth's own code, not another analyst's reading of the form.

## Reproduce every number here

Nothing beyond the standard library is needed, and Node for the XFA harness.

```bash
python3 model/test_guidelines.py                 # 20 checks: Table A against all 1,104 published rows
python3 model/test_worksheet.py                  # 60 checks: the worksheet, pinned to a real order
python3 model/test_box1_fix.py                   # 258 checks: the Box 1 credit and its redlines
python3 model/test_childcare_post_transfer.py    # 10 checks: child care on post-transfer shares
python3 model/submission_figures.py              # prints every figure quoted in the comments
python3 model/run_official_xfa.py                # runs the form's own scripts and diffs them (node on PATH)
```

Redrawing the figures needs `matplotlib` and `numpy`:

```bash
python3 -m venv .venv && .venv/bin/pip install matplotlib numpy
.venv/bin/python model/charts/make_all.py        # redraws every figure into figures/working/ and figures/exhibits/
```

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every command above runs against the files in this repository, with no network access and
  no hidden inputs.</p>
  <ul>
    <li><a href="/the-data/">The data</a></li>
    <li><a href="/findings/">The findings the model produces</a></li>
    <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
  </ul>
</div>
