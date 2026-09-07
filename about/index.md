---
layout: page
title: About
description: >-
  Who built this, the disclosure of a personal stake in the outcome, and an explicit statement
  of what the project does and does not claim.
---

# One person built this, and the tests back the numbers, not the byline

Christopher Campbell built this site, the model, and the documents it links to. He has no
institutional affiliation, no co-author, and no organization behind the work. That is exactly
why the disclosure below, and the model and data pages, exist: there is no institution's name to
lend the numbers credibility, so every number has to stand on being checkable instead.

<div class="disclosure">
  <p>The worked example running through every finding on this site (the $201,000 payor, the
  $570-a-week other parent, the three children) is my own child support order, computed under
  Massachusetts's 2025 worksheet. I am telling you this before you read a single finding because a
  reader should reasonably wonder whether an interested party has shaded a number in his own
  favor, and the honest answer to that is to let you check it rather than to ask you to trust me.
  The worksheet that produced these figures is at
  <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>, checked against the official
  form's own calculation scripts on <a href="/the-model/">the model page</a>. Run it on any
  numbers you choose, not just mine.</p>
</div>

## The project makes three checkable claims about how the worksheet computes

Each is checkable independently of the other two and of the author's own case:

1. The worksheet's Section IV.C hardship test is computed on gross-derived income while the
   obligation is paid from net income, so it reports a lower percentage than the payor's actual
   burden.
2. Line 6b allocates child care on each parent's income share measured before the base support
   order has already moved money between the two households: one calculation, two different
   income measures.
3. The credit the worksheet gives for equal parenting time is the difference in two income
   shares with no parenting-time term in it, so the credit shrinks as the gap between the
   parents' incomes widens rather than staying fixed to the time actually shared.

Each is laid out with its own figures and its own source files on the [findings](/findings/)
pages. All three are about how the worksheet computes, not about what any resulting number ought
to be.

## The project does not claim any order is wrong, or that Massachusetts is the worst state

- **It does not claim any support order, including the author's own, is the wrong amount.** A
  finding that a computation is internally inconsistent is not a finding about what the correct
  number is.
- **It does not claim Massachusetts is "the worst state" for child support**, or rank it against
  all fifty states on any general measure. The fifty-one-jurisdiction comparisons on this site
  hold one fact pattern fixed and say so on every figure; see [the data](/the-data/) for exactly
  what was and was not computed.
- **It does not make any claim about anyone else's child support case**, including the other
  parent named in the author's own order. The worked example is used because it is the one set
  of numbers the author can disclose and verify firsthand, not because it is claimed to be
  typical.
- **It is not a legal filing and creates no legal obligation on anyone.** It is a set of comments
  on how a public worksheet computes, prepared for submission to the body that maintains that
  worksheet. See [documents](/documents/) for the current, unsent status of that submission.

## License

Code is released under the MIT license
(<a href="https://github.com/campbefs/checktheworksheet/blob/main/LICENSE-CODE.txt">LICENSE-CODE.txt</a>).
The documents and figures are released under CC BY 4.0. A checkable error, reported as an issue
or pull request against the repository, will be corrected and credited.

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Nothing on this page needs to be taken on trust: the code, the data, and the documents are
  all linked from here.</p>
  <ul>
    <li><a href="/the-model/">The model</a></li>
    <li><a href="/the-data/">The data</a></li>
    <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
  </ul>
</div>
