---
layout: finding
title: The Massachusetts child support guidelines do not comply with federal law
permalink: /findings/federal-law/
description: >-
  Federal law requires every child support order to rest on the parent's ability to pay. The
  Massachusetts Worksheet never computes what a parent keeps after tax, and with child care
  claimed it sets orders above the federal withholding ceiling, amounts the Commonwealth cannot
  lawfully collect.
disclosure:
  - >-
    I pay child support in Massachusetts myself, so I have a stake in the outcome. The figures on
    this page are not about one family. They cover every pair of incomes the model runs through
    the Worksheet, with three children and the other parent holding primary custody.
  - >-
    Every figure here comes from <a href="/model/ccpa_grid.py"><code>model/ccpa_grid.py</code></a>,
    which runs the Worksheet in <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>
    across the whole income grid and tests each order against the federal ceiling. It is
    checked by <a href="/model/test_ccpa_grid.py"><code>model/test_ccpa_grid.py</code></a>.
rail_label: "On this page"
sections:
  - id: ability-to-pay
    label: "Ability to pay"
  - id: ceiling
    label: "The federal ceiling"
  - id: net-and-gross
    label: "Net and gross"
  - id: fix
    label: "The fix"
  - id: limits
    label: "Limits"
  - id: check
    label: "Check it yourself"
---

<section class="hero" markdown="1">
<p class="eyebrow">Federal law</p>

# The Massachusetts child support guidelines do not comply with federal law

<p class="lede">While federal law requires every child support order to rest on the parent's
ability to pay, the Massachusetts Worksheet never computes what a parent keeps after tax. With
child care claimed, it sets orders above the federal withholding ceiling: amounts the
Commonwealth cannot lawfully collect.</p>
</section>

<div class="numeral-pair numeral-pair--solo">
  <div class="numeral">
    <span class="numeral-value">40%</span>
    <p class="numeral-caption">of income pairs produce an order over the federal ceiling with $100 a week of child care claimed per child (three children, primary custody)</p>
  </div>
</div>

<p class="confidence-tag">Every income pair run through the Worksheet's own arithmetic</p>

{% include disclosure.html %}

<div class="page-shell" markdown="1">
{% include chapter-rail.html %}
<div class="content-col" markdown="1">

<section id="ability-to-pay" markdown="1">

## Federal law requires every order to rest on the parent's ability to pay, and the Worksheet never measures it

Every state's child support guidelines must provide that the order is based on the parent's
"earnings, income, and other evidence of ability to pay," 45 C.F.R. § 302.56(c)(1), and meeting
that rule is a condition of federal approval of the state's child support plan, § 302.56(a).
Massachusetts says it does this. The Guidelines open by reciting the federal rule almost word for
word: "These guidelines are based on various considerations, including, but not limited to, each
parent's earnings, income, and other evidence of ability to pay."

While the Guidelines recite the standard, the Worksheet that produces the number holds none of
it. It has no line for net pay, after-tax income or disposable earnings, no line for tax, and the
words ability to pay appear nowhere on it. A form that does not know what a parent keeps cannot
base an order on what that parent is able to pay.

The federal agency that wrote the rule has already answered the objection that this is a state's
business. When commenters on the 2016 rule argued that orders were too high and discouraged
shared parenting, the Department of Health and Human Services replied that a state keeps its
discretion over the percentage, "so long as the resulting order takes into consideration the
noncustodial parent's ability to pay it," 81 Fed. Reg. 93528. The discretion is real and it comes
with a condition. Massachusetts has taken the discretion without meeting the condition.

</section>

<section id="ceiling" markdown="1">

## With child care claimed, the Worksheet sets orders the Commonwealth cannot lawfully collect

Congress caps what may be withheld from a paycheck for child support at 50 percent of take-home
pay, or 60 percent for a parent with no second family to support, 15 U.S.C. § 1673(b)(2). This site
calls the 50 percent line the federal ceiling.

The Worksheet has no line for the payor's household, so it cannot tell which of the two ceilings
applies to the order it sets. That ceiling limits collection, not the order. No federal rule limits how large an order may be,
so a court can order more than an employer may withhold, and the rest is still owed. The only
federal rule on the order itself is the ability-to-pay requirement, and it never says what ability
to pay is.

With $100 a week of child care claimed per child, well under the $430 the Guidelines allow, 40% of
income pairs produce a three-child primary-custody order over the federal ceiling. At the
Guidelines' own limit of $430 a child, every pair crosses it, and at its highest
the order reaches 186 percent of take-home pay, nearly twice what the parent brings home.

{% include figure.html
   id="e29"
   img="/figures/exhibits/E29-orders-over-federal-ceiling-by-child-care.png"
   alt="Line chart of the share of 1,147 income pairs whose order is above the federal withholding ceiling, as child care claimed rises from $0 to $430 per child per week, for primary custody and for joint custody at equal time."
   title="With child care claimed, the Worksheet produces orders the Commonwealth cannot lawfully collect."
   deck="Share of income pairs whose order is above the federal ceiling, by child care claimed per child per week."
   notes="Three children. Federal ceiling, 15 U.S.C. § 1673(b)(2), shown as a band: 50 percent of take-home pay for a payor with a second family, 60 percent for one without. At $100 a child, 40 percent of pairs cross the 50 percent line under primary custody."
   source_script="model/ccpa_grid.py"
   csv_href="/figures/working/fig_ceiling_share.csv"
   lazy="false" %}

The crossings are not a rich parent's problem. The pairs that cross first are payors earning
$60,000 to $100,000 against another parent with little or no income.

{% include figure.html
   id="e30"
   img="/figures/exhibits/E30-order-against-federal-ceiling-by-income.png"
   alt="Line chart of the order as a share of the payor's take-home pay across payor incomes from $50,000 to $300,000, with no child care and at $100, $200 and $430 per child per week, against a line for the federal ceiling at 50 percent."
   title="The more child care is claimed, the further the order goes over the federal ceiling."
   deck="The order as a share of the payor's take-home pay, three children, the other parent primary, the other parent earning $29,640 a year."
   notes="The shaded band is the federal ceiling: 50 percent of take-home pay for a payor with a second family, 60 percent for one without. Take-home pay is after federal and state income tax, Social Security and Medicare."
   source_script="model/ccpa_grid.py"
   csv_href="/figures/working/fig_ceiling_by_income.csv" %}

{% include figure.html
   id="e31"
   img="/figures/exhibits/E31-income-pairs-over-ceiling-grid.png"
   alt="Grid of 1,147 income pairs, payor income across and other parent's income up, shaded where the order at $100 of child care per child is over the federal ceiling."
   title="At $100 a child, 40 percent of income pairs produce an order over the federal ceiling."
   deck="Each square is one pair of incomes: the Worksheet's order with $300 a week of child care claimed for three children, primary custody."
   notes="Dark squares are over both federal ceilings (60 percent); light squares are over the 50 percent ceiling that applies to a payor with a second family. Hatched squares are pairs where the other parent would be the higher earner."
   source_script="model/ccpa_grid.py"
   csv_href="/figures/working/fig_ceiling_grid.csv" %}

With no child care claimed, no order on the grid crosses the federal ceiling. Child care is what
carries it past, and child care is inside the Guidelines: the same Worksheet adds it to the order,
up to $430 a week per child. So the Guidelines themselves produce amounts the Commonwealth may not
collect in full, and an amount a state may not lawfully take is not evidence of ability to pay.

</section>

<section id="net-and-gross" markdown="1">

## Massachusetts collects the order from net pay and sets it from gross pay

The Commonwealth's own collection statute, G.L. c. 119A § 12, cites the federal withholding
ceiling three times. While the Commonwealth measures the paycheck in net pay when it takes the
money, it measures it in gross pay when it decides how much to take, and the Guidelines never
compute net pay at all. A state that can compute net pay to collect an order can compute it to set
one.

The Guidelines' own hardship rule shows what that costs. It presumes an order is too high once it
takes 40 percent of the payor's income, but it measures that income before tax. In the worked
example it stays silent until the order is taking 56.9 percent of take-home pay. The
[hardship test page](/findings/hardship-test/) works through it line by line.

</section>

<section id="fix" markdown="1">

## The fix is a federal definition of ability to pay, with a limit for primary and for joint custody

Federal law should define ability to pay as the payor's net pay less the child care he pays
himself, because both come out of the same paycheck. A presumptive order, child care included,
should never take more than 40 percent of it, and never more than 30 percent in joint custody. The 40 percent is Massachusetts's own
hardship threshold, applied to the income the order is actually paid from. Federal law already
requires a floor of this kind for a low earner and leaves the method to the state,
§ 302.56(c)(1)(ii), so a ceiling at the top is the same kind of rule.

Three jurisdictions already cap
the order itself: Delaware at 50 percent of available income, Washington at 45 percent of net income, and
the District of Columbia at 35 percent of adjusted gross income with child care included. No state
checks the order against the federal withholding ceiling when it sets it.

Parents paying orders set under the current Guidelines should be able to ask for an immediate
reduction to what the corrected rule allows, without showing any other change in circumstances.
Today an order can only be reviewed back to the Guidelines, 42 U.S.C. § 666(a)(10), which for a
guideline that does not comply is no review at all. The full list of changes is on the
[recommendations page](/recommendations/#federal).

</section>

<section id="limits" markdown="1">

## Nobody has ruled on this yet, and the federal office has approved the Massachusetts plan

<p class="caveat">This is an argument from the federal rule and the Commonwealth's own documents,
not a finding by any court or agency. The federal Office of Child Support Services has approved
the Massachusetts plan with this Worksheet in it, and the rule does not require a worksheet line
labeled ability to pay. Most states set support from gross income under approved plans, and
Massachusetts's low-income adjustment meets the rule's protection at the bottom of the income
range. The question is whether anything in the Massachusetts Guidelines tests the resulting order
against what the parent can pay, and above the low-income range nothing does.</p>

<p class="caveat">The federal ceiling limits what may be withheld from a paycheck, not the size of
the order a court may enter, which is how the Worksheet can set an amount above it. The part of
that order above the ceiling cannot be withheld from the parent's pay.</p>

</section>

<section id="check" markdown="1">

<div class="check-yourself">
<h2>Check it yourself</h2>
<p>Every number on this page is computed, not typed.</p>
<ul>
  <li><strong><a href="/model/ccpa_grid.py"><code>model/ccpa_grid.py</code></a></strong>
    Runs the Worksheet over every income pair at each child care level and counts the orders
    over the federal ceiling.</li>
  <li><strong><a href="/model/test_ccpa_grid.py"><code>model/test_ccpa_grid.py</code></a></strong>
    Pins the counts on this page, including that no order crosses any ceiling with no child care
    claimed.</li>
  <li><strong><a href="/model/net_caps.py"><code>model/net_caps.py</code></a></strong>
    The take-home pay calculation and the 40 and 30 percent ceilings.</li>
  <li><strong><a href="/figures/working/fig_ceiling_grid.csv">fig_ceiling_grid.csv</a></strong>
    Every income pair behind the grid chart, with its order and share of take-home pay.</li>
</ul>
</div>

</section>

</div>
</div>
