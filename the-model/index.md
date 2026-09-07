---
layout: page
title: The model
description: >-
  A Python reproduction of the Massachusetts worksheet, a federal and state tax model, three
  extension models, four test suites, and a harness that runs the official form's own
  calculation scripts and diffs them against the model.
---

# A model of the worksheet, checked against the form's own calculation scripts, not just against itself

This page describes what is reproduced in code and how each part is checked. The findings
themselves, what the checks show, are on the [findings](/findings/) pages. This page is the
proof that the numbers behind them are computed, not asserted.

## The worksheet model reimplements CJ-D 304 line by line, from the form's own text

[`model/worksheet.py`](/model/worksheet.py) is a transcription of the 2025 Child Support
Guidelines Worksheet (CJ-D 304, 12/1/2025): gross and available income (Lines 2a–3a), the
combined-income shares and applicable cap (3b–3d), Table A and Table B support amounts, the
Table C age adjustment, the proportional shares and low-income adjustment (5a–5c), the child
care benchmark and allocation (6a–6c), the income-disparity adjustment and netting (6d–6g), the
recipient-side adjustment (7a–7b), the final obligation and the 40 percent hardship test (7d–7e),
and all three custody boxes: Box 1 (shared), Box 2 (primary, roughly two-thirds time), and
Box 3 (split, each parent primary for different children).

[`model/guidelines.py`](/model/guidelines.py) holds Table A and Table B as published. Table A was
cross-checked against every one of the 1,104 combined-income-to-support-amount rows in the
Commonwealth's own published Guidelines Chart, reconstructed at
[`data/extracted/guidelines-chart.json`](/data/extracted/guidelines-chart.json), with no
disagreement greater than one dollar. Table B (the multiplier for two, three, four and more
children) is transcribed from the guidelines' own commentary.

## A tax model computes what each party actually keeps after the order

[`model/net_position.py`](/model/net_position.py) converts each party's gross income to spendable
income after federal and Massachusetts tax: brackets, the standard deduction, the Social
Security wage base, the federal Earned Income Tax Credit and Child Tax Credit, and Massachusetts's
own exemption, EITC match, and refundable Child and Family Tax Credit. This is what lets a
finding compare a support order, which is computed on gross income, against what each household
actually has to spend.

## Three extension models test one mechanism each

- [`model/box1_fix.py`](/model/box1_fix.py): how the Box 1 equal-parenting credit is computed,
  and three redlines that would give it a parenting-time term.
- [`model/childcare_post_transfer.py`](/model/childcare_post_transfer.py): what child care looks
  like when it is split on the income shares that exist *after* the base support transfer, instead
  of the pre-transfer shares Line 6b actually uses.
- [`model/marginal_retention.py`](/model/marginal_retention.py): of the next dollar the payor
  earns, how much is kept after tax and the resulting change in the order.

[`model/submission_figures.py`](/model/submission_figures.py) prints every figure quoted in the
comments to the Trial Court, by section, from the worksheet and tax models above, so no number
in the documents is quoted without a script that produces it.

## Four test suites, 348 checks together, gate every quoted number

| Suite | Checks | What it pins |
|---|---|---|
| [`model/test_guidelines.py`](/model/test_guidelines.py) | 20 | Table A and Table B against the published chart |
| [`model/test_worksheet.py`](/model/test_worksheet.py) | 60 | The worksheet, pinned to a real order and to the form's own rounding |
| [`model/test_box1_fix.py`](/model/test_box1_fix.py) | 258 | The Box 1 credit and its three redline variants |
| [`model/test_childcare_post_transfer.py`](/model/test_childcare_post_transfer.py) | 10 | Child care on post-transfer income shares |

All four pass as of this writing; run them yourself with the commands below.

## A harness runs the Commonwealth's own calculation scripts, not a re-derivation of them

The 2025 CJ-D 304 published on mass.gov is a fillable XFA form carrying its own embedded
calculation scripts. [`data/extracted/cjd304-xfa.xml`](/data/extracted/cjd304-xfa.xml) is that
logic, extracted from the blank official form. [`model/official_xfa_harness.js`](/model/official_xfa_harness.js)
is a small, dependency-free Node program that executes those scripts to a fixed point, exactly as
the form does when a field changes. [`model/run_official_xfa.py`](/model/run_official_xfa.py)
drives the harness on six scenarios built from the worked example: Box 1 and Box 2, with and
without child care, and with child care paid by one or both parents, and it prints a line-by-line
comparison against `model/worksheet.py`.

**What the comparison shows.** In [`model/runs/official-xfa-vs-model-2026-09-05.txt`](/model/runs/official-xfa-vs-model-2026-09-05.txt),
the official form's own scripts and the model's rounded output agree on the final weekly order
(Line 7d) in all six scenarios: $1,016, $1,091, $1,355, $1,280, $1,274 and $1,010. The model's
unrounded arithmetic differs from these by a few dollars in each case (for example $1,012.72
against $1,016 in the first scenario), the effect of the form rounding every line to
the cent before the next line uses it, which the model reproduces when run with its
`round_lines=True` option. This is the strongest check in the project: it compares the model
against the Commonwealth's own code, not against another analyst's reading of the form.

## Reproduce every number here

No third-party packages are needed for the worksheet, tax model, or test suites, only the
standard library, and Node (no npm packages) for the XFA harness.

```bash
python3 model/test_guidelines.py                 # 20 checks: Table A against all 1,104 published rows
python3 model/test_worksheet.py                  # 60 checks: the worksheet, pinned to a real order
python3 model/test_box1_fix.py                   # 258 checks: the Box 1 credit and its redlines
python3 model/test_childcare_post_transfer.py    # 10 checks: child care on post-transfer shares
python3 model/submission_figures.py              # prints every figure quoted in the comments
python3 model/run_official_xfa.py                # runs the form's own scripts on six scenarios and diffs them (node must be on PATH)
```

Redrawing the figures needs `matplotlib` and `numpy`; reading a fresh copy of the PDF form needs
`pypdf`:

```bash
python3 -m venv .venv && .venv/bin/pip install matplotlib numpy pypdf
.venv/bin/python model/charts/make_all.py        # redraws every figure into figures/working/ and figures/exhibits/
```

[`model/inspect_worksheet.py`](/model/inspect_worksheet.py) is the extraction script that pulled
the calculation logic out of the blank PDF in the first place. It is what produced
`data/extracted/cjd304-xfa.xml`, and is included so the extraction step itself can be checked
against a fresh copy of the form.

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every command above runs against the files in this repository, with no network access and no
  hidden inputs.</p>
  <ul>
    <li><a href="/the-data/">The data</a></li>
    <li><a href="/findings/">The findings the model produces</a></li>
    <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
  </ul>
</div>
