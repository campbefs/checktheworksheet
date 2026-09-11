---
layout: page
title: Mission
description: The mission, the disclosure of a personal stake, and what this project does not claim.
disclosure:
  - >-
    The worked example running through every finding on this site (a payor at $201,000, another
    parent at $570 a week, three children, equal parenting time) is computed under
    Massachusetts's 2025 worksheet. I pay child support in Massachusetts myself, so I have a
    stake in the outcome, and a reader should reasonably wonder whether an interested party
    shaded a number in his own favor. So every figure is published with the code that produced it. Check
    it yourself.
  - >-
    The worksheet that produced these figures is
    <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>, checked against the
    official form's own scripts on <a href="/the-model/">the model page</a>. Run it on any
    numbers you choose.
---

# Mission

This project aims to advocate for reform of the Massachusetts Child Support Guidelines, to make
them more fair and to hold the Commonwealth accountable for the Worksheet. The Worksheet has never
had a proper review. No task force has examined how its math actually works economically.

A Worksheet that sets a presumptive order should be accurate whichever way it's off, and the three
checkable claims below name where it isn't. The [recommendations](/recommendations/) page goes
further, and not every proposal there lowers an order: alongside redlines for those three, it asks
for two changes that lower none at all, both first proposed by an advocacy coalition that argues
the opposite side of most of what's here. Every figure comes from a published model with tests. Anyone
can check the arithmetic.

## Who built this

An independent Massachusetts child support payor built this site, with no institution behind it. Every number stands on being
checkable. That is why the disclosure and the [model](/the-model/)/[data](/the-data/) pages exist.

{% include disclosure.html %}

## Three checkable claims, argued with figures on [findings](/findings/)

These claims are about how the worksheet computes, not what a number ought to be. Section IV.C's
hardship test runs on gross-derived income while the order is paid from net. Line 6b allocates
child care on pre-transfer income shares. The equal-parenting credit, an income-share difference
with no parenting-time term, shrinks as the income gap widens.

## What this project does not claim

- **No order is claimed to be wrong.** An inconsistent computation isn't a
  finding about the correct number.
- **Massachusetts isn't claimed to be "the worst state,"** or ranked against all fifty. See
  [the data](/the-data/) for the fixed fact pattern.
- **No claim is made about anyone else's case.**
- **This isn't a legal filing** and creates no obligation on anyone.

## License

Code: <a href="/LICENSE-CODE.txt">MIT</a>;
documents/figures: CC BY 4.0.

<div class="ask">
  <h2>Check it yourself</h2>
  <ul>
    <li><a href="/the-model/">The model</a></li>
    <li><a href="/the-data/">The data</a></li>
  </ul>
</div>
