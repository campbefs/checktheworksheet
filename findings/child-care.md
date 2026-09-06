---
layout: finding
title: Child care is split on income shares the order has already changed
permalink: /findings/child-care/
description: >-
  Worksheet Line 6b allocates child care using each parent's share of income before the base
  support order transfers any money between households. At the author's own order, that charges
  the payor 88 cents of every dollar of a $15,600 claim.
---

# Line 6b charges the payor 88 cents of every dollar of child care, using an income split base support has already moved

Massachusetts allocates child care in proportion to each parent's share of combined available
income. That's a defensible principle. But the worksheet measures the share at Line 3c — computed
before the base child support order transfers a single dollar between the two households — and then
never revisits it. At the author's own order, the recipient's $15,600-a-year child care claim is
split using that pre-transfer share, which charges the payor 88 cents of every dollar even though
the base order has already moved a large share of his income to her household.

## Line 6b uses the income split from before the base order moved money between the households

Line 3c is each parent's share of the two parents' combined available income (their Line 3a
figures, added together). It is computed early in the worksheet, before the base support amount at
Line 7d exists. Line 6a is the child care one parent actually pays out of pocket. Line 6b multiplies
the *other* parent's Line 3c share by that amount — so if the recipient pays the provider, the
payor's Line 6b charge is his Line 3c share of her cost.

The problem is timing. Line 3c reflects income *before* any support changes hands. By the time
child care is added at Line 6, the base order has already been set and, once paid, will move a
large share of the payor's income to the recipient's household every week. Line 6b never re-measures
the shares against that post-transfer reality — it keeps using the original, pre-transfer split for
the life of the order, on top of an obligation that has already re-weighted what each household
actually has.

## The payor's share falls from 88 cents to 48 cents once the split is measured after the order and after tax

The recipient claims $300 a week ($15,600 a year) of child care. Three ways of measuring the split,
same $15,600 bill:

| Basis for the split | Payor's share | Payor funds |
|---|---:|---:|
| Line 3c, pre-transfer (what the form does today) | 87.7% | $13,678/yr (order rises to $1,276/wk) |
| Shares adjusted by the base order (the redline proposed at Line 6b-1) | 64.5% | $10,054/yr (order $1,206/wk — $3,624/yr less than today) |
| Post-transfer net shares (income after the order and after tax) | 48.2% | $7,513/yr |

(Source: `model/runs/childcare-post-transfer-run-2026-09-05.txt`, printed by
`model/childcare_post_transfer.py`; the order figures are from
`model/runs/submission-figures-run-2026-09-05.txt`.) The pre-transfer share the form actually uses,
87.7 percent, rounds to 88 cents of every dollar of the claim funded by the payor.

The same mechanism runs in the other direction, too, when both parents pay for care during their
own parenting time. At equal shared parenting with each parent paying $300 a week, the combined
$31,200-a-year bill is split 93 percent to the payor and 7 percent to the recipient — while the
payor earns 87 percent of the combined income, not 93 percent of it. His own $15,600 of child care
reduces the order by only $270 a year, because Line 6e limits how much of his own claim he can
recover once his income share puts him outside the low-income protection the line was written for.

## The same gap shows up at every income level, and even when both parents pay for care themselves

<figure class="exhibit" id="e06">
  <img src="/figures/exhibits/E06-child-care-share-three-rules-worked-example.png"
       loading="lazy"
       alt="Bar chart of the payor's share of a $15,600 annual child care claim under three
            allocation rules, at the worked example.">
  <figcaption>
    <h3 class="exhibit-title">The payor's share of a $15,600 child care bill, three ways to split it.</h3>
    <p class="exhibit-deck">Line 3c, the § 2 redline, and post-transfer net shares, compared at the worked example.</p>
    <p class="exhibit-notes">Line 3c allocates 87.7 percent to the payor on pre-transfer income shares. Adjusting the shares by the base order, the § 2 redline, gives 64.5 percent. Post-transfer net shares give 48.2 percent. The middle bar is the redline; the right bar is where the argument goes once net income is admitted.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig2_childcare.py</code> ·
      <a href="/figures/working/fig2_childcare_worked_example.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e07">
  <img src="/figures/exhibits/E07-child-care-rules-across-incomes-1-2-3.png"
       loading="lazy"
       alt="Line chart of the payor's share of child care under three allocation rules across a
            range of the lower earner's income, shown separately for one, two, and three children.">
  <figcaption>
    <h3 class="exhibit-title">Child care is split on an income distribution that base support has already changed.</h3>
    <p class="exhibit-deck">The same three rules across the income range, for one, two and three children, $100 per child per week.</p>
    <p class="exhibit-notes">The gap between the current rule and either alternative widens with the number of children and with the income gap between the parents.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig2_childcare.py</code> ·
      <a href="/figures/working/fig2_childcare_rules.csv">data (CSV)</a></p>
  </figcaption>
</figure>

<figure class="exhibit" id="e15">
  <img src="/figures/exhibits/E15-both-parents-pay-child-care-payor-bears-93pct.png"
       loading="lazy"
       alt="Bar chart comparing net income outcomes when both parents pay $300 a week of child
            care under equal shared parenting, with the combined child care bill split between the
            two households.">
  <figcaption>
    <h3 class="exhibit-title">When both parents pay child care, the payor bears 93 percent of it on 87 percent of the income.</h3>
    <p class="exhibit-deck">Equal shared parenting, each parent paying $300/wk of child care during their own time.</p>
    <p class="exhibit-notes">The Worksheet allocates the recipient's cost to the payor through Line 6b and passes the payor's own cost back through Line 6e at about two cents on the dollar, so his own $15,600 reduces the order by $270 a year. Order plus his own child care reaches 58 percent of his net income while Line 7e reads 33 percent. Per person the payor still leads.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig8_both_pay.py</code> ·
      <a href="/figures/working/fig8_both_pay.csv">data (CSV)</a></p>
  </figcaption>
</figure>

## Proportional allocation is fair; the wrong income share is not, and per person the payor still leads

Allocating child care in proportion to income is not, by itself, an unreasonable rule — the
objection here is to which income the proportion is measured against, not to proportionality as a
concept. $300 a week is a real but not extreme claim relative to the $430-per-child statutory
ceiling; a smaller claim moves the split by less, a larger one by more. And this is one worked
example, not a distribution — how far a typical case's child care claim sits from this one is not
known from anything in this repository.

The standing caveat applies here as everywhere: per person, the payor remains ahead. Even in the
scenario where both parents pay for care and he is charged 93 percent of the combined bill, he
still holds $58,163 for himself against $22,907 each for the recipient's household of four.

## Check it yourself

- [`model/childcare_post_transfer.py`](/model/childcare_post_transfer.py) — computes all three
  allocation rules (pre-transfer, post-transfer gross adjusted by the base order, post-transfer net).
- [`model/test_childcare_post_transfer.py`](/model/test_childcare_post_transfer.py) — pins the
  87.7%, 64.5%, and resulting order figures the letter's § 2 redline quotes.
- [`model/worksheet.py`](/model/worksheet.py) and
  [`model/test_worksheet.py`](/model/test_worksheet.py) — the Line 6a/6b/6e implementation,
  including the test that the payor bears roughly 93 percent of combined child care when both
  parents pay for it under equal shared parenting.
- [`model/runs/childcare-post-transfer-run-2026-09-05.txt`](/model/runs/childcare-post-transfer-run-2026-09-05.txt)
  and [`model/runs/submission-figures-run-2026-09-05.txt`](/model/runs/submission-figures-run-2026-09-05.txt)
  — the printed runs behind every figure above.
