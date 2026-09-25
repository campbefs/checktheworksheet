---
layout: finding
title: Most states price joint custody with one formula, and Massachusetts does not use it
permalink: /findings/shared-parenting-formula/
description: >-
  Twenty states and the District of Columbia price joint custody with the cross-credit
  formula. At the worked example it orders $701 a week where Massachusetts orders $1,013. It should
  be the national standard for joint custody.
disclosure:
  - >-
    I pay child support in Massachusetts myself, so I have a stake in the outcome. Every figure on
    this page is for the worked example used across this site: two incomes of $201,000 and $29,640 a
    year, three children, equal parenting time and no child care unless stated.
  - >-
    The formula is computed in <a href="/model/box1_fix.py"><code>model/box1_fix.py</code></a> (Variant B)
    and measured against ability to pay in
    <a href="/model/ability_to_pay.py"><code>model/ability_to_pay.py</code></a>, checked by
    <a href="/model/test_ability_to_pay.py"><code>model/test_ability_to_pay.py</code></a>.
rail_label: "On this page"
sections:
  - id: formula
    label: "The formula"
  - id: worked
    label: "Worked through"
  - id: massachusetts
    label: "What Massachusetts does"
  - id: states
    label: "Which states"
  - id: ask
    label: "The ask"
  - id: limits
    label: "Limits"
---

<section class="hero" markdown="1">
<p class="eyebrow">Shared parenting</p>

# Most states price joint custody with one formula, and Massachusetts does not use it

<p class="lede">While 20 states and the District of Columbia price joint custody with the cross-credit formula, which credits
each parent for the time they house the children, Massachusetts has no parenting-time term at all.
For the same family that formula orders $701 a week at equal time, and Massachusetts orders
$1,013.</p>
</section>

<div class="numeral-pair">
  <div class="numeral">
    <span class="numeral-value">$701</span>
    <p class="numeral-caption">A week under the cross-credit formula at equal time</p>
  </div>
  <div class="numeral">
    <span class="numeral-value">$1,013</span>
    <p class="numeral-caption">A week under the Massachusetts Worksheet for the same family</p>
  </div>
</div>

<p class="confidence-tag">One family, equal parenting time, no child care</p>

{% include disclosure.html %}

<div class="page-shell" markdown="1">
{% include chapter-rail.html %}
<div class="content-col" markdown="1">

<section id="formula" markdown="1">

## The cross-credit charges each parent for the time the other has the children

When both parents house the children, each household pays for a bed, a kitchen and the drive to
school. The cross-credit starts from that. It raises the basic support amount by half to cover the
costs two households both carry, splits the larger amount between the parents by income, charges
each parent for the share of time the children spend with the other, and has the parent who owes
more pay the difference.

It is the method most states already use. A 2020 survey of state guidelines found it in 23
states and found no other method in use in more than two, Oldham and Venohr, 54 Fam. L.Q. 141, 152.

</section>

<section id="worked" markdown="1">

## Worked through for one family, the formula is six lines of arithmetic

The worked example earns $201,000 a year against the other parent's $29,640, has three children,
and splits the time equally. Every figure is weekly.

| Step | Amount |
|---|---:|
| Basic support for three children, from the Massachusetts schedule | $1,241 |
| Raised by half for the costs two households both carry | $1,861 |
| The higher earner's share, 87.7% of the income | $1,632 |
| The other parent's share | $229 |
| Each parent owes half their share, for the other's half of the time | $816 and $115 |
| **The higher earner pays the difference** | **$701** |

That order is 26.1% of the payor's ability to pay, meaning take-home pay less any child care he
pays himself. Where each parent pays $300 a week of child care during their own time, each should bear
their own, so the order stays at $701 and takes 29.4% of ability to pay. The Massachusetts
Worksheet would instead add $226 a week, because it charges the higher earner 87.7% of the other
parent's child care and credits him 12.3% of his own.

</section>

<section id="massachusetts" markdown="1">

## Massachusetts charges both households the full amount and then shrinks the credit

The Massachusetts Worksheet puts every child in both households at the full schedule amount and
subtracts one from the other. At equal time that is the cross-credit with the basic amount
doubled, which assumes two households cost twice what one does. A cap
on one line of the Worksheet then cuts the higher earner's credit by about half. For this family
Massachusetts orders $1,013 a week at equal time, only 6.9% below the $1,088 it orders when the
other parent has the children full time.

</section>

<section id="states" markdown="1">

## Twenty states and the District of Columbia use the cross-credit today, and four more states use a version of it

Read from each state's current guideline. Four rows rest on a secondary source and are marked.

| State | Added for shared costs | Applies from |
|---|---|---|
| Alabama | 50% | About equal time |
| Alaska | 50% | 30% of the year |
| Arkansas | Not stated in the text read | About equal time |
| Colorado | 50% until March 2026, then a table | 93 overnights until March 2026, then from one overnight |
| District of Columbia | 50% | 35% of the year |
| Florida | 50% | 73 overnights |
| Idaho | 50% | More than 25% of overnights |
| Illinois | 50% | 146 overnights (secondary source) |
| Maryland | 50% | 92 overnights |
| Mississippi | Not stated | Equal time (secondary source) |
| Montana | No flat amount | 110 days |
| Nebraska | 50% | More than 142 days (secondary source) |
| New Mexico | 50% | 35% of the year (secondary source) |
| North Carolina | 50% | 123 overnights |
| Oklahoma | 100%, 75% or 50%, falling as time rises | 121 overnights |
| South Carolina | 50% | 110 overnights |
| Vermont | 50% | 30% of the year |
| Virginia | 40% | 91 days |
| West Virginia | 60% | 127 days |
| Wisconsin | 50% | 92 overnights |
| Wyoming | 50% | More than 25% of the year |

Georgia, Michigan, Minnesota and Oregon use a curved version of the same formula, with no
threshold. Massachusetts is not on either list.

</section>

<section id="ask" markdown="1">

## Federal law should cap every joint-custody order at what the cross-credit produces

The federal rule that governs child support guidelines, 45 C.F.R. § 302.56, says nothing about
parenting time. So each state decides, and Massachusetts removed its parenting-time adjustment in
2017 and brought it back as a deviation in 2025. The petition to the Department of Health and Human Services asks for three
things. No state could order more for joint custody, meaning each parent has the children at least a
third of the time, than the cross-credit at the standard 50% produces. A state could keep its own
method so long as it stays under that line. Every order would be capped at 40%
of ability to pay. While the Department reviews the method, a joint-custody order would be capped
at 25%. The comments to the Chief Justice ask Massachusetts to adopt the same formula now.

The petition applies the formula as equal time across the whole joint-custody range, so parents
have no reason to litigate over each extra night. The states that use it charge by the actual
overnights instead.

</section>

<section id="limits" markdown="1">

## One family at one set of incomes, and a count that depends on the definition

<p class="caveat">Every dollar figure is for one family, the worked example, so the page shows how
the formula treats that one family. The count of 21 jurisdictions depends on the definition.
Nevada nets each parent's full amount with no charge for time, so it is not counted here, though
the 2020 survey counts it. North Dakota reduces only one parent's amount and is not counted either.
Texas lawyers commonly use the formula in practice, but Texas does not write it into its
guideline. With each parent paying $300 a week of their own child care, the cross-credit still takes 29.4% of
this family's ability to pay, above the 25% interim limit and under the 40% ceiling the petition
keeps on every order.</p>

</section>

</div>
</div>
