---
layout: page
title: About
description: The disclosure of a personal stake, and what this project does not claim.
disclosure:
  - >-
    The worked example running through every finding on this site (the $201,000 payor, the
    $570-a-week other parent, three children) is my own child support order, computed under
    Massachusetts's 2025 worksheet. A reader should reasonably wonder whether an interested party
    shaded a number in his own favor. The honest answer is to let you check it, not to ask you to
    trust me.
  - >-
    The worksheet that produced these figures is
    <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>, checked against the
    official form's own scripts on <a href="/the-model/">the model page</a>. Run it on any
    numbers you choose, not just mine.
---

# One person built this; the tests back the numbers, not the byline

Christopher Campbell built this site, with no institution behind it. Every number stands on being
checkable. That is why the disclosure and the [model](/the-model/)/[data](/the-data/) pages exist.

{% include disclosure.html %}

## Three checkable claims, argued with figures on [findings](/findings/)

These claims are about how the worksheet computes, not what a number ought to be. Section IV.C's
hardship test runs on gross-derived income while the order is paid from net. Line 6b allocates
child care on pre-transfer income shares. The equal-parenting credit, an income-share difference
with no parenting-time term, shrinks as the income gap widens.

## What this project does not claim

- **No order, including my own, is claimed to be wrong.** An inconsistent computation isn't a
  finding about the correct number.
- **Massachusetts isn't claimed to be "the worst state,"** or ranked against all fifty. See
  [the data](/the-data/) for the fixed fact pattern.
- **No claim is made about anyone else's case**, including the other parent in my order.
- **This isn't a legal filing** and creates no obligation on anyone. See [documents](/documents/).

## License

Code: <a href="https://github.com/campbefs/checktheworksheet/blob/main/LICENSE-CODE.txt">MIT</a>;
documents/figures: CC BY 4.0.

<div class="ask">
  <h2>Check it yourself</h2>
  <ul>
    <li><a href="/the-model/">The model</a></li>
    <li><a href="/the-data/">The data</a></li>
    <li><a href="https://github.com/campbefs/checktheworksheet">Repository</a></li>
  </ul>
</div>
