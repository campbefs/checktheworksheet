---
layout: page
title: The tax credits
permalink: /credits/
description: >-
  Four refundable tax credits are worth $15,328 a year at the worked example. The model leaves
  them out by default, and this page shows why, one income, one row per credit.
---

# Four refundable tax credits are worth $15,328 a year here, and the model leaves them out by default

The calculator and every finding on this site compute net income on a withholding basis: federal
income tax, Massachusetts income tax, and Social Security and Medicare, the same formula for both
parents, no filing status, no dependents, no credits. That basis is reproducible from a published
table by anyone. It also understates a low-income parent's real spendable income, because it
leaves out credits that pay out in cash. This page states what those credits are worth at the
recipient's income in the worked example, $29,640 a year, three children, two of them under 13,
with a source for each figure.

## The four credits, at one income

| Credit | Value | Cutoff | Source |
|---|---|---|---|
| Federal Earned Income Tax Credit | $7,020 | Zero above $62,974 with three qualifying children | IRS Rev. Proc. 2025-32 &sect; 3.06(1) |
| Federal Child Tax Credit, refundable part | $4,620 | Needs earned income; shrinks above $200,000, reaches zero at $332,000 | IRC &sect;&sect; 24(b), 24(h); Rev. Proc. 2025-32 &sect; 3.05 |
| Massachusetts Earned Income Tax Credit | $2,808 | 40% of the federal credit, so it disappears at the same income | M.G.L. c. 62 &sect; 6(h) |
| Massachusetts Child and Family Tax Credit | $880 | $440 per dependent under 13, two of the three children here | M.G.L. c. 62 &sect; 6(x) |
| **Total** | **$15,328** | | |

Against $3,808 of federal income tax, Massachusetts income tax, and FICA owed at that same income.
Re-derived from <a href="/model/net_position.py"><code>model/net_position.py</code></a> for this
page: <code>_federal_eitc()</code>, <code>refundable_credits()</code>, and
<code>ma_refundable_credits()</code>.

## What this page is not

<p class="caveat">Every figure above depends on which parent claims which child. The federal
credit follows the parent the children lived with more than half the year regardless of any
agreement, except the Child Tax Credit, which a signed release can move to the other parent for a
year. Massachusetts's credits follow the same split. CJ-D 304, the Worksheet, has no field that
records who claims whom, so no figure that depends on it can be reproduced from the form alone.</p>

<p class="caveat">No number in any letter this project writes, and no figure on any finding page,
in the comments, or in any chart uses anything from this table. Those are all held to the
withholding basis described above, so a reader can rebuild them from published tables without
knowing anything about either parent's tax return. The one place these credits are counted is the
calculator on the home page, which counts them by default and says so; switch it to "Leave them
out" to see the basis every other page uses.</p>

## See it with credits counted

The <a href="/#calculator">calculator on the home page</a> has a "Refundable tax credits" control.
"Count them" is the default there, because these are real money a low-income household receives and
leaving them out understates it. "Leave them out" switches to the withholding basis, which is what
every other page on this site and every figure in the comments uses. Counting them applies the four
credits above under the statutory rule: head-of-household status and both Earned
Income Tax Credits stay with whichever parent has the children more of the time, every year, and
cannot be moved by agreement. Only the Child Tax Credit can move, by a signed release. At equal
parenting time, the calculator averages a year each parent claims it; at primary custody, nothing
moves, because the custodial parent already holds all four credits.

<div class="ask">
  <h2>Check it yourself</h2>
  <p>Every figure above is computed by a function you can call directly.</p>
  <ul>
    <li><a href="/model/net_position.py"><code>model/net_position.py</code></a></li>
    <li><a href="/the-model/">The model, and its test suites</a></li>
    <li><a href="/findings/">The findings that use the withholding basis instead</a></li>
  </ul>
</div>
