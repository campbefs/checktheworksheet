---
layout: finding
title: Federal law requires child support to be based on what a parent can actually pay
permalink: /findings/federal-law/
description: >-
  Federal law requires every child support order to rest on the parent's ability to pay. The Massachusetts Worksheet never computes what a parent keeps after tax, and federal law never says what ability to pay means once the basics are met. With child care claimed, the order it produces can come out higher than federal law lets the state collect from wages. No court or agency has ruled on whether that adds up to a problem.
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

# Federal law requires child support to be based on what a parent can actually pay

<p class="lede">Federal law says a child support order has to be based on what a parent can actually pay. Massachusetts runs that math on gross income and stops there, so take-home pay never enters it. With child care added, the guidelines can set child support higher than federal law lets the state collect from wages. Federal law should close that gap.</p>
</section>

<p class="caveat">No court or federal agency has ruled on whether the guidelines meet this
standard. Federal approval of the state's plan has not addressed it. What follows is our
argument, built from the federal rule and the Commonwealth's own documents.</p>

<p class="caveat">This argument concerns the Guidelines themselves, the worksheet that sets the
presumptive amount, rather than any individual order. Federal law makes that presumptive amount
rebuttable, and a judge may deviate from it, 45 C.F.R. § 302.56(f), (g). We do not think deviation
answers this: it is case-by-case relief available only to a parent who can afford to litigate it,
and it changes nothing about what the Guidelines themselves compute or presume correct for every
case that does not deviate.</p>

<div class="numeral-pair">
  <div class="numeral">
    <span class="numeral-value">40%</span>
    <p class="numeral-caption">of three-child, primary-custody income pairs on our model grid, at $100 a week of child care per child, have an order that takes more than half of take-home pay</p>
  </div>
  <div class="numeral">
    <span class="numeral-value">10.6%</span>
    <p class="numeral-caption">cross 60 percent, the federal limit on what can be withheld from wages. All of those also cross the Guidelines&rsquo; own hardship line: &ldquo;Whenever application of the guidelines requires a payor to pay a recipient 40% or more of the payor&rsquo;s available income in Line 3a of the guidelines worksheet for a current child support order, there shall be a rebuttable presumption of a substantial hardship, justifying a deviation from the guidelines,&rdquo; 2025 Guidelines § IV.C. That presumption is new to the 2025 Guidelines and is a real protection. It is also a presumption, not an automatic correction: a parent has to raise it, and the deviation it allows is still up to the judge. We have not measured how often that happens.</p>
  </div>
</div>

<p class="confidence-tag">Share of income pairs on our model grid, not a share of actual Massachusetts orders. Every pair run through the Worksheet's own arithmetic.</p>

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

The federal rule spells out three specific things a state's method must do: count all the parent's income, protect a floor for low earners, and limit how much can be imputed, 45 C.F.R. § 302.56(c)(1)(i)–(iii). Massachusetts's Worksheet does all three. What the rule does not spell out is what ability to pay means once those three boxes are checked. Massachusetts never answers that question the way most people would, by asking what a parent actually takes home after tax. The Worksheet has no line for net pay, after-tax income, or disposable earnings, and the words ability to pay appear nowhere on the form itself.

When commenters on the 2016 rule argued that orders were too high and discouraged shared
parenting, and asked the federal agency to require guidelines based on the marginal cost of
raising a child, the Department of Health and Human Services said no: "We do not agree with this
suggestion." Its full answer cuts both ways. It affirmed state flexibility: "Once a parent's
income is ascertained, the rule does not limit States' flexibility in defining the percentage or
amount of income ordered to be paid as child support, so long as the resulting order takes into
consideration the noncustodial parent's ability to pay it," and "this rule only establishes
minimum components for State child support guidelines... and does not impose more specific
requirements," 81 Fed. Reg. 93528. That answer settles less than it looks like it does. It tells states how to set the percentage. It does not say what counts as taking ability to pay into consideration, or how a state would know if it had. Massachusetts has never had to answer that question, because nobody has ever made it ask.

</section>

<section id="ceiling" markdown="1">

## The Massachusetts guidelines can set child support higher than federal law lets the state collect from wages

Congress caps what can be withheld from a paycheck for child support at 60 percent of take-home pay, 15 U.S.C. § 1673(b)(2).[^ceiling] We also mark orders that take more than half of take-home pay, because an order that size is worth a second look on its own.

[^ceiling]: The limit is 50 percent for a parent supporting a second family. Both limits step up once the support being withheld is more than twelve weeks overdue: "the 50 per centum specified in clause (A) shall be deemed to be 55 per centum and the 60 per centum specified in clause (B) shall be deemed to be 65 per centum," 15 U.S.C. § 1673(b)(2). The figures on this page use 60 percent.

The 60 percent limit caps collection, not the order itself. No federal rule limits how large an
order may be, so a court can order more than an employer may withhold, and the rest is still
owed. The only federal rule on the order itself is the ability-to-pay requirement, and it never
says what ability to pay is.

At the worked example running throughout this site, a payor earning $201,000 a year, the
other parent earning $29,640, $100 a week of child care claimed per child, well under the
$430 the Guidelines allow, is enough to put the order over half of take-home pay. It does not
cross the 60 percent limit at that claim level.

{% include figure.html
   id="e30"
   img="/figures/exhibits/E30-order-against-federal-ceiling-by-income.png"
   alt="Line chart of the order as a share of the payor's take-home pay across payor incomes from $50,000 to $300,000, with no child care and at $100, $200 and $430 per child per week, against a line for the federal limit on wage withholding at 60 percent."
   title="The more child care is claimed, the further the order goes over the federal limit on wage withholding"
   deck="The order as a share of the payor's take-home pay, three children, the other parent primary, the other parent earning $29,640 a year."
   notes="The solid line is the federal limit on wage withholding, 60 percent of take-home pay, less for a payor with a second family. The dashed line marks half of take-home pay, a burden flag, not a legal limit. Take-home pay is after federal and state income tax, Social Security and Medicare."
   source_script="model/ccpa_grid.py"
   csv_href="/figures/working/fig_ceiling_by_income.csv" %}

Across the full grid of income pairs behind this site, 40% have an order that takes more than
half of take-home pay at $100 a week of child care per child, and 10.6% cross 60 percent, the
limit itself. All of those also cross the Guidelines' own hardship line: "Whenever application of the guidelines requires a payor to pay a recipient 40% or more of the payor's available income in Line 3a of the guidelines worksheet for a current child support order, there shall be a rebuttable presumption of a substantial hardship, justifying a deviation from the guidelines," 2025 Guidelines § IV.C. That presumption is new to the 2025 Guidelines and is a real protection. It is also a presumption, not an automatic correction: a parent has to raise it, and the deviation it allows is still up to the judge. We have not measured how often that happens. Both figures are shares of income pairs on our model grid, not of actual Massachusetts orders. At the Guidelines' own limit of $430 a
child, the benchmark for infant center-based care, and well above what this site's worked
example uses, every pair crosses it. That is a stress test, not a typical family: three
children all still needing infant-level center-based care at once is uncommon. On that stress test,
the highest order reaches 186 percent of take-home pay. It says nothing about whether
Massachusetts's low-income adjustment works: that adjustment operates on income, and this figure
comes from child care claimed at its maximum, not from a low-income pair.

{% include figure.html
   id="e31"
   img="/figures/exhibits/E31-income-pairs-over-ceiling-grid.png"
   alt="Grid of 1,147 income pairs, payor income across and other parent's income up, shaded where the order at $100 of child care per child is over the federal limit on wage withholding."
   title="At $100 a child, 10.6% of income pairs produce an order over the federal limit on wage withholding."
   deck="Each square is one pair of incomes: the Worksheet's order with $300 a week of child care claimed for three children, primary custody."
   notes="Dark squares are over the federal limit on wage withholding, 60 percent of take-home pay. Light squares are over half of take-home pay but under that limit. Hatched squares are pairs where the other parent would be the higher earner. 10.6 percent of squares are dark. All of them also cross the Guidelines' own hardship line: 'Whenever application of the guidelines requires a payor to pay a recipient 40% or more of the payor's available income in Line 3a of the guidelines worksheet for a current child support order, there shall be a rebuttable presumption of a substantial hardship, justifying a deviation from the guidelines,' 2025 Guidelines § IV.C. That presumption is new to the 2025 Guidelines and is a real protection. It is also a presumption, not an automatic correction: a parent has to raise it, and the deviation it allows is still up to the judge. We have not measured how often that happens."
   source_script="model/ccpa_grid.py"
   csv_href="/figures/working/fig_ceiling_grid.csv" %}

{% include figure.html
   id="e29"
   img="/figures/exhibits/E29-orders-over-federal-ceiling-by-child-care.png"
   alt="Line chart of the share of 1,147 income pairs whose order is above the federal withholding ceiling, as child care claimed rises from $0 to $430 per child per week, for primary custody and for joint custody at equal time."
   title="The Massachusetts guidelines can set child support higher than federal law lets the state collect from wages."
   deck="Share of income pairs whose order is above the federal limit on wage withholding, by child care claimed per child per week."
   notes="Three children. Federal limit on wage withholding, 15 U.S.C. § 1673(b)(2): 60 percent of take-home pay, less for a payor with a second family. At $100 a child, 10.6 percent of pairs cross it under primary custody. 40 percent have an order over half of take-home pay."
   source_script="model/ccpa_grid.py"
   csv_href="/figures/working/fig_ceiling_share.csv"
   lazy="false" %}

The crossings are not a rich parent's problem. The pairs that cross first are payors earning
$60,000 to $100,000 against another parent with little or no income, the widest income gap
our grid tests, not necessarily the most common one. The Guidelines only credit child care that is
work-related, actually paid, and not already covered by a discount or subsidy (2025 Guidelines
§ II.E.1, § II.E.4), so a lower-earning parent with little or no income and work-necessary child
care is a narrower group than the grid alone shows. We have not measured how many real
Massachusetts cases fall in it.

With no child care claimed, no order on the grid crosses the federal ceiling. Child care is what
carries it past, and child care is inside the Guidelines: the same Worksheet adds it to the order,
up to $430 a week per child. So the Guidelines themselves can set child support higher than federal law lets the state collect from wages. We believe an order that size is not, on its own,
evidence the guideline is based on ability to pay.

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

Most states set support from gross income, and that alone is not the gap we are describing. Federal law tests the order that comes out, not the income measure that goes in. When
the Department of Health and Human Services wrote the rule in 2016, it said a state may set the
percentage as it chooses "so long as the resulting order takes into consideration the
noncustodial parent's ability to pay it." What sets Massachusetts apart is what comes out: the
highest joint-custody orders in the nation, a hardship rule that cannot see an order until it
takes more than half of take-home pay, and, with child care claimed, orders above the federal
ceiling. This site has run that test on Massachusetts only. A gross-income state that produced
the same result would have the same problem.

</section>

<section id="fix" markdown="1">

## The fix is a federal definition of ability to pay, with a limit for primary and for joint custody

Federal law already requires an order to rest on ability to pay, and it never defines what that means. What would settle the question this page raises is a federal definition, not a ruling that Massachusetts broke the rule.
Federal law should define ability to pay as the payor's net pay less the child care the payor
pays, because both come out of the same paycheck. A presumptive order, child care included,
should never take more than 40 percent of it, and never more than 30 percent in joint custody. The 40 percent is Massachusetts's own
hardship threshold, applied to the income the order is actually paid from. Federal law already
requires a floor of this kind for a low earner and leaves the method to the state,
§ 302.56(c)(1)(ii), so a ceiling at the top is the same kind of rule.

Three jurisdictions already cap
the order itself: Delaware at 50 percent of available income (Family Court Civil Rule 506(b)),
Washington at 45 percent of net income except for good cause shown, which the statute names as
including day care expenses and larger families among other grounds (RCW 26.19.065(1)), and the
District of Columbia at 35 percent of adjusted gross income with child care included (D.C. Code
§ 16-916.01(n)). No state checks the order against the federal withholding ceiling when it sets it.

Parents paying orders set under the current Guidelines should be able to ask for an immediate
reduction to what the corrected rule allows, without showing any other change in circumstances.
Today an order can only be reviewed back to the Guidelines, 42 U.S.C. § 666(a)(10), which, if Massachusetts's guidelines do not rest on ability to pay the way federal law requires, is no review at all. The full list of changes is on the
[recommendations page](/recommendations/#federal).

</section>

<section id="limits" markdown="1">

## Nobody has ruled on this yet, and federal approval of the state's plan has not addressed it

<p class="caveat">This is an argument from the federal rule and the Commonwealth's own documents,
not a finding by any court or agency. No court or federal agency has ruled on whether the
guidelines meet this standard, and federal approval of the state's plan has not addressed it. The
rule does not require a worksheet line labeled ability to pay, and most states set support from
gross income under approved plans. Massachusetts's low-income adjustment meets the rule's
protection at the bottom of the income range. Above that range, the only test is the 40-percent-of-
gross hardship presumption, and it works only through deviation: in our worked example it is not
triggered until the order takes 56.9 percent of take-home pay.</p>

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
