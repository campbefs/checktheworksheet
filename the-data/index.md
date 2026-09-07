---
layout: page
title: The data
description: What each dataset behind the model contains and how confident each row is.
---

# Six datasets, traced to a source and rated for confidence

Every number in a finding traces to one of these files, or a script in [the model](/the-model/).

## The form's own logic

[`data/extracted/cjd304-xfa.xml`](/data/extracted/cjd304-xfa.xml) holds the 2025 CJ-D 304's own
scripts, extracted by [`model/inspect_worksheet.py`](/model/inspect_worksheet.py). **Primary
source, executed directly**; [the model](/the-model/) matches it on all six scenarios.

## The support chart

[`data/extracted/guidelines-chart.json`](/data/extracted/guidelines-chart.json) holds 1,104
income-to-support pairs, $0-$8,654/wk, from the 2025 Guidelines Chart. **Checked against Table A,
no disagreement over one dollar** ([`model/test_guidelines.py`](/model/test_guidelines.py)).

## Three fifty-one-jurisdiction datasets, one fixed pattern

All three use the author's own order (disclosed on [about](/about/)): payor $201,000/yr, other
parent $570/wk, three children, no child care. Not a general claim.

- [`tier-50-2026-09-05.json`](/data/fifty-state/tier-50-2026-09-05.json): the monthly order in 50
  jurisdictions, equal time (`s1`) and primary custody (`s2`). Massachusetts: $4,388.48 /
  $4,714.22. **Tiered**: computed twice, reconciled, attacked; blind Massachusetts matched.
  Georgia excluded (its formula gives a lower order under primary custody than equal time).
- [`credit-at-122-2026-09-05.json`](/data/fifty-state/credit-at-122-2026-09-05.json): whether 122
  overnights earns a formula credit, 51 jurisdictions. Tally: 28 yes, 23 no, Massachusetts among
  the 23. **Profile text**, one pass per jurisdiction; `basis` names rows revised.
- [`ceilings-2026-09-06.json`](/data/fifty-state/ceilings-2026-09-06.json): where each schedule
  stops. 41 state a ceiling; Massachusetts $450,000, 13th of 41, median $360,000; 10 more have no
  ceiling. **39 rows high confidence, 12 medium**.

## Where gross-versus-net was, and wasn't, raised

[`data/deferrals-gross-vs-net.json`](/data/deferrals-gross-vs-net.json) has one row per
Massachusetts edition, 2017-2025, marked `DEFERRED` only where a verbatim quote exists in the
corpus, `NO RECORD IN CORPUS` otherwise. Only 2025 has one: the Brattle Economic Review's "decided
not to recommend a change from gross income to net income at this time." **Read from
`data/extracted/*.flow.txt`**, each row citing its matched `source_file` and `quote`.

## What is not in these files

No fifty-state child care estimate, no deviation rate net of imputed income and defaults, no
distribution of real orders. None of it exists here, or in any finding on this site.

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every figure above is read directly out of the linked file, never retyped from memory.</p>
  <ul>
    <li><a href="/the-model/">The model</a> that reads these files</li>
    <li><a href="/findings/">The findings</a> built from them</li>
    <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
  </ul>
</div>
