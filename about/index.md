---
layout: page
title: About
description: >-
  Who built this, the disclosure of a personal stake in the outcome, and an explicit statement
  of what the project does and does not claim.
disclosure:
  - >-
    The worked example running through every finding on this site (the $201,000 payor, the
    $570-a-week other parent, the three children) is my own child support order, computed under
    Massachusetts's 2025 worksheet. I disclose it before you read a single finding because a
    reader should reasonably wonder whether an interested party has shaded a number in his own
    favor, and the honest answer is to let you check it rather than ask you to trust me.
  - >-
    The worksheet that produced these figures is
    <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>, checked against the
    official form's own calculation scripts on <a href="/the-model/">the model page</a>. Run it
    on any numbers you choose, not just mine.
---

# One person built this, and the tests back the numbers, not the byline

Christopher Campbell built this site, the model, and the documents it links to, with no
institutional affiliation, co-author, or organization behind it. With no institution's name to
lend the numbers credibility, every number has to stand on being checkable instead: that is why
the disclosure below and the [model](/the-model/) and [data](/the-data/) pages exist.

{% include disclosure.html %}

## Three checkable claims about how the worksheet computes

Each is checkable independently of the other two and of my own case:

1. Section IV.C's hardship test is computed on gross-derived income while the obligation is
   paid from net income, so it reports a lower percentage than the payor's actual burden.
2. Line 6b allocates child care on each parent's income share measured before the base support
   order has already moved money between the households: one calculation, two income measures.
3. The credit for equal parenting time is the difference of two income shares with no
   parenting-time term in it, so it shrinks as the income gap widens rather than tracking the
   time actually shared.

Each has its own figures and source files on the [findings](/findings/) pages. All three are
about how the worksheet computes, not about what any resulting number ought to be.

## What this project does not claim

- **Not that any support order, including my own, is the wrong amount.** An internally
  inconsistent computation is not a finding about the correct number.
- **Not that Massachusetts is "the worst state"** for child support, or ranked against all
  fifty on any general measure. The fifty-jurisdiction comparisons hold one fact pattern fixed
  and say so on every figure; see [the data](/the-data/) for exactly what was and wasn't
  computed.
- **Not any claim about anyone else's case**, including the other parent named in my own order.
  The worked example is used because it is the one set of numbers I can disclose and verify
  firsthand, not because it is typical.
- **Not a legal filing**, and it creates no legal obligation on anyone. It is comments on how a
  public worksheet computes, prepared for submission to the body that maintains it. See
  [documents](/documents/) for the current, unsent status.

## License

Code is MIT
(<a href="https://github.com/campbefs/checktheworksheet/blob/main/LICENSE-CODE.txt">LICENSE-CODE.txt</a>);
documents and figures are CC BY 4.0. A checkable error, reported as an issue or pull request,
will be corrected and credited.

<div class="ask">
  <h2>Check it yourself</h2>
  <ul>
    <li><a href="/the-model/">The model</a></li>
    <li><a href="/the-data/">The data</a></li>
    <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
  </ul>
</div>
