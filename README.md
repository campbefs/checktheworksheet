# The Massachusetts child support worksheet, line by line

> **Status, September 2026.** The comments described here are prepared for submission to the Chief Justice of
> the Massachusetts Trial Court, and a petition for rulemaking is prepared for the U.S. Department of Health
> and Human Services. Neither has been sent as of this writing; this page will record the dates once they are.
> The model, the data and the figures are final and can be checked today.

This repository holds a reproduction in code of the Massachusetts Child Support Guidelines Worksheet
(form CJ-D 304, 2025 edition), the tests that pin it to the form's own calculation scripts, a federal
and Massachusetts tax model, a fifty-one-jurisdiction comparison at one fact pattern, and the figures
drawn from them. Everything a reader needs to check a number is here.

## What the worksheet does that its text does not say

1. **The hardship test reads the wrong income.** Section IV.C presumes hardship when an order reaches
   40 percent of a payor's available income. Line 7e divides by gross-derived income; the order is paid
   from after-tax income. At the worked example the form reports 40 percent when the payor is at 57
   percent of net. [E05](figures/exhibits/E05-what-line-7e-sees-vs-true-burden-worked-example.png)
2. **Child care is split on an income measure the form has already adjusted away from.** Line 6b
   allocates child care on pre-transfer income shares after base support has moved money between the
   households. [E06](figures/exhibits/E06-child-care-share-three-rules-worked-example.png)
3. **The credit for equal parenting time contains no parenting-time term.** It is the difference in
   income shares, clipped by Line 6e, so it shrinks as the income gap widens: 75 percent of the
   one-third-time order at a 57 percent payor income share, 7 percent at 88 percent.
   [E08](figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png)
4. **At equal parenting time, Massachusetts orders more than 47 of 49 other jurisdictions do at
   primary custody**, one fact pattern.
   [E17](figures/exhibits/E17-ma-equal-time-vs-others-primary-custody.png)

The worked example throughout is the author's own order, and the comments disclose that plainly. The claims are about the internal consistency of a computation, not about whether
any support amount is right.

## Check it yourself

```
python3 -m venv .venv && .venv/bin/pip install matplotlib numpy pypdf
.venv/bin/python model/test_guidelines.py      # Table A reconstruction against all 1,104 published chart rows
.venv/bin/python model/test_worksheet.py       # the worksheet, pinned to the form's own XFA scripts
.venv/bin/python model/submission_figures.py   # prints every figure quoted in the comments
node model/official_xfa_harness.js             # runs the form's own calculation scripts (see run_official_xfa.py)
.venv/bin/python model/charts/make_all.py      # redraws every figure into figures/
```

`data/extracted/cjd304-xfa.xml` is the calculation logic extracted from the blank official form; `model/run_official_xfa.py`
executes it and diffs it against the model on six scenarios (`model/runs/official-xfa-vs-model-2026-09-05.txt`).

## Contents

| Folder | What |
|---|---|
| `model/` | `worksheet.py` (CJ-D 304), `guidelines.py` (Tables A and B), `net_position.py` (TY2026 federal + MA tax), `box1_fix.py`, `childcare_post_transfer.py`, `marginal_retention.py`, tests, the XFA harness |
| `model/runs/` | Printed output of each script on the date named |
| `data/fifty-state/` | The fifty-one-jurisdiction rows (`tier-50`), the credit-at-122-overnights tally, the schedule ceilings |
| `figures/exhibits/` | One chart per file, E01 to E17, each with its CSV beside the working figure in `figures/working/` |
| `paper/` | The figures appendix (Attachment E), and the comments to the Trial Court as prepared for submission |

## Method for the fifty-one jurisdictions

Each jurisdiction was profiled from its own primary documents, computed twice independently, reconciled
on disagreement, and subjected to an adversarial review; Massachusetts was run blind as a control.
Fifty of fifty-one survived every stage; Georgia is held out because its enacted formula produces a
lower order under primary custody than under equal time. The full verification record (about 300
primary documents and the per-state analyst notes) is available from the author on request.

## Author

Christopher Campbell, independent. Code under the MIT licence (`LICENSE-CODE.txt`); documents and figures
under CC BY 4.0. Corrections are welcome as issues or pull requests; a checkable error will be fixed and
credited.
