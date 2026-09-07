---
layout: page
title: The data
description: >-
  What each dataset behind the model contains, where it came from, and how confident each row
  is: the form's own extracted calculation logic, the published support chart, and three
  fifty-one-jurisdiction datasets.
---

# Five datasets: one extracted from the official form itself, one published chart, three built jurisdiction by jurisdiction

Every number in a finding traces back to one of these files, or to a script in
[the model](/the-model/) that reads one of them.

## The form's own calculation logic, extracted from the blank official worksheet

[`data/extracted/cjd304-xfa.xml`](/data/extracted/cjd304-xfa.xml) is the XFA template of the 2025
CJ-D 304, as published on mass.gov, with its embedded calculation scripts intact. It is not a
transcription or a summary; it is the actual field definitions and JavaScript the Trial Court's
own form runs when a field changes, extracted by
[`model/inspect_worksheet.py`](/model/inspect_worksheet.py). **Verification status: primary
source, executed directly.** [The model](/the-model/) runs these scripts through a harness on six
scenarios and diffs the result against the Python reimplementation; the two agree on the final
order in all six.

## The published support chart used to validate the schedule

[`data/extracted/guidelines-chart.json`](/data/extracted/guidelines-chart.json) holds 1,104
combined-available-income-to-weekly-support pairs, covering $0 to $8,654 a week ($450,008 a
year), read from the Commonwealth's own published 2025 Child Support Guidelines Chart.
**Verification status: every one of the 1,104 rows was checked against the model's Table A, with
no disagreement greater than one dollar.** The check itself is
[`model/test_guidelines.py`](/model/test_guidelines.py), 20 of whose checks are this comparison.

## Three fifty-one-jurisdiction datasets, one fact pattern held constant throughout

All three datasets use the same fact pattern: a payor at $201,000 a year, the other parent at
$570 a week, three children, no child care. That fact pattern is the author's own order,
disclosed on the [about](/about/) page. Comparisons drawn from these files are about that one
fact pattern; they are not a claim about jurisdictions generally.

- [`data/fifty-state/tier-50-2026-09-05.json`](/data/fifty-state/tier-50-2026-09-05.json): the
  monthly order in each of 50 jurisdictions at that fact pattern, under two custody scenarios:
  `s1` (equal parenting time) and `s2` (the other parent has primary custody). Massachusetts
  reads $4,388.48 (`s1`) and $4,714.22 (`s2`). **Verification status: tiered.** Each row was
  built from that jurisdiction's own primary documents, computed twice independently, reconciled
  where the two disagreed, and checked by an adversarial review pass; Massachusetts was computed
  blind as a control and reproduced these same two figures. Georgia is not in this file: its
  enacted formula produces a lower order under primary custody than under equal time, which the
  state's own calculator reproduces, so it was held out rather than ranked.

- [`data/fifty-state/credit-at-122-2026-09-05.json`](/data/fifty-state/credit-at-122-2026-09-05.json):
  for each of 51 jurisdictions, whether a parent with the children 122 overnights a year (a
  third of the year, the equal-parenting fact pattern used elsewhere on this site) receives a
  formula credit for it. The file's own tally: 28 yes, 23 no. Massachusetts is among the 23; its
  Box 2, the roughly-two-thirds-time category, is treated as the one-third case rather than as a
  credit against a higher default. **Verification status: profile text**, read from each
  jurisdiction's own guidelines by one research pass per jurisdiction, not independently
  double-computed the way the two dollar-figure datasets were; the `basis` field on each row
  says so, and says which few rows were revised after a later adversarial check (for example
  South Dakota, revised after the review found an abatement provision the first pass missed).

- [`data/fifty-state/ceilings-2026-09-06.json`](/data/fifty-state/ceilings-2026-09-06.json):
  for all 51 jurisdictions, where the presumptive schedule stops. 41 jurisdictions state a
  combined-income ceiling; Massachusetts's is $450,000 a year, 13th of the 41, against a median
  of $360,000. The other 10 use a percentage-of-obligor, Melson, or open formula with no combined
  ceiling and are listed, not ranked, in the same file. **Verification status: 39 rows high
  confidence, 12 medium**, each row's `confidence` field stating which, and each `citation` field
  quoting the source text directly rather than paraphrasing it. No figure in this file was
  estimated where a document did not state one.

## What is not in these files

None of the five datasets contains a fifty-state estimate of typical child care claims, a
deviation rate broken out from imputed-income and default cases, or a distribution of orders
across real families; those numbers do not exist here, and no finding on this site asserts them.

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every figure above is read directly out of the linked file; none is retyped from memory.</p>
  <ul>
    <li><a href="/the-model/">The model</a> that reads these files</li>
    <li><a href="/findings/">The findings</a> built from them</li>
    <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
  </ul>
</div>
