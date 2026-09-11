// checktheworksheet.org -- the home-page two-income calculator (design brief SS3.7, item 1).
// Vanilla JS, no dependencies, no CDN. Computes its answer for any two incomes, using a tested
// port of the worksheet and tax model -- assets/js/lib/worksheet.js and
// assets/js/lib/net-position.js -- checked to the dollar against the Commonwealth's own CJ-D 304
// XFA calculate-scripts. See assets/js/calculator.test.js.
//
// v12 (2026-09-08, later the same day) ports net_position.py's SECOND Box 1 fix (private commit
// 723a7bf) into assets/js/lib/net-position.js. The v10 fix below had the two parents swap
// EVERYTHING in alternating years -- filing status, the EITC, and the CTC. The statute does not
// allow that: a s. 152(e)/Form 8332 release moves ONLY the dependency claim and the federal
// CTC/ACTC family; head of household and the EITC stay with the physical-custodian recipient
// regardless of any release (IRC ss. 2(b)(1)(A)(i), 32(c)(3)(A)). See net-position.js's
// householdNetIncomes()/payorNetClaimsCtc()/custodialNetNoCtc() and
// docs/2026-09-08-filing-status-and-credit-allocation.md. THE REVISED HEADLINE CONSEQUENCE, at the
// worked example (Box 1, no child care, this calculator's kidsUnder13=0 convention): the recipient
// household again holds slightly more than the payor keeps -- $90,631 vs $90,447 (not the v10
// entry's $85,168 vs $92,453). At the site's real fact pattern (two of three children under 13,
// used elsewhere on this site) the corrected figures are $91,512 vs $90,447. Every dollar figure
// and sanity-guard constant below reflects this correction; see calculator.test.js for the pinned
// values.
//
// v11 (2026-09-08) adds the CREDITS-OFF SWITCH (data-calc-radio="credits", values "1"/"0",
// default "1" -- matches every figure this site has published, so the switch changes no number
// on load). "Count them" (default) is unchanged. "Leave them out" removes every federal and
// Massachusetts refundable tax credit from payor_after/recip_after/recip_per_person/true_pct_net:
// both parties' net income comes from net_position.js's netIncomeWithholdingBasis() alone, and
// custody box / who-claims-which-child stop mattering, because credits are the only place either
// fact enters this calculator's tax math. This lets a reader who does not accept the
// who-claims-which-child assumption behind Box 1's alternating-year averaging -- an economist,
// most pointedly -- validate the arithmetic without accepting it. See
// assets/js/lib/net-position.js's analyze()/householdNetIncomes() and model/net_position.py's
// matching docstring. Sanity-gated by creditsOffSanityPasses() (folded into the main guard, since
// this switch reaches the main readout, not a fallback control): worked example, no child care,
// credits off -> payor $87,172, recipient household $77,396 (the "no credits to either" row
// model/test_net_position.py pins).
//
// v10 (2026-09-08) fixes both N.analyze() call sites (the main readout's computeWithFacts and the
// Child care tab's computeChildcareDistribution) to pass the selected custody box (facts.box)
// through to net-position.js's analyze(). Before this, analyze() always used its default (box=2,
// "recipient claims every child and files head of household"), even when Box 1 (equal parenting
// time) was selected -- so payor_after/recip_after/recip_per_person and the analytical net_share
// were computed under the wrong custody assumption for every Box 1 scenario, which is most of what
// this calculator is built to show. See assets/js/lib/net-position.js's own 2026-09-08 note and
// model/net_position.py's docstring. THE HEADLINE CONSEQUENCE, at the worked example (Box 1, no
// child care): the recipient household no longer holds more than the payor keeps -- $92,453 vs
// $85,168, not the reverse. The order (order_wk, line_7e, Line-3a-based figures like the "on
// income after the order" fallback) is unaffected -- those come from worksheet.js, which has no
// tax logic and was never wrong.
//
// v9 (2026-09-08) fixes a mismatch between this calculator and the letter's own Section 2 ask:
// "On money after tax" (computeNetRuleOrder) used to leave the support order at the no-child-care
// figure and describe the higher earner's share as a private side payment. The letter's redline is
// a Worksheet LINE (new Line 6b-1) inside the chain 6b -> 6c -> 6e -> 6g -> 7b -> 7d, so adopting it
// changes the order itself -- an amount inside a court order carries contempt, wage assignment and
// state collection; a side payment carries none of that. Two changes fix it:
//   1. THE SHARE is now `net_withholding_share` (computeChildcareDistribution), the post-transfer
//      share on net_position.net_income_withholding_basis -- tax and FICA only, single filer, no
//      exemptions, NO refundable credits. Ported from model/childcare_post_transfer.py's rule5, the
//      figure Section 2 asks for as of v4.9. `net_share` (credits included) is unchanged and still
//      shown as the analytical figure in the distribution callout; it is not what a Worksheet line
//      can compute, because CJ-D 304 collects neither filing status nor who claims which child.
//   2. THE ORDER moves: net_rule_order_wk = base_order_wk + net_rule_share * totalChildcare, the
//      same linear step the "on income after the order" fallback already uses, because both are
//      now Worksheet-line redlines, not a private payment.
//
// v7 (2026-09-07, afternoon) adds a SECOND child-care allocation rule and cleans up the on/off
// control, both from owner feedback on v6:
//   1. THREE-WAY RULE SELECTOR replaces the single "apply the proposed fix" checkbox
//      (data-calc-radio="ccRule", values worksheet/nettax/linebased):
//        - "As the Worksheet does it" (default): today's Line 6b, unchanged.
//        - "On money after tax" (computeNetRuleOrder): what this project recommends, as of v9 a
//          Worksheet-line redline like the fallback below, not a side payment -- see the v9 note
//          above.
//        - "On income after the order" (computeFixedRuleOrder, unchanged arithmetic): the former
//          sole toggle, now labelled a fallback for when post-tax figures cannot be computed.
//      All three share one explanatory line (data-calc-cell="cc_rule_note") that states what the
//      selected rule charges the higher earner and, where the rule changes the order, the result
//      beside the Worksheet's own figure. Each rule has its own sanity gate
//      (fixedRuleSanityPasses/netRuleSanityPasses); a rule that fails disables its own radio with a
//      note instead of showing a wrong number, and reverts the selection to "As the Worksheet does
//      it" if it was the one selected.
//   2. THE DISTRIBUTION READOUT'S NET LEG now uses kidsUnder13 = 0, the same convention as every
//      other figure in this calculator (previously min(2, kids), a deliberate exception to match
//      the letter's worked-example figures). Dropped so the callout agrees with the "on money after
//      tax" rule's own math at any input, not only the worked example -- the worked example's own
//      number moves from 48.2% to 48.4% as a result (verified against net_position.py directly).
//   3. CHILD CARE ON/OFF became a two-option segmented control (data-calc-radio="ccOn", values
//      "0"/"1", reusing the same .segmented/.segmented-option classes as Children/Custody above it)
//      instead of a bare checkbox. The heading itself now carries the state
//      (data-calc-cc-state, "not included"/"included") so a reader does not have to find the
//      control to know whether child care is on.
//
// v6 (2026-09-07) REMOVES THE TWO-TAB STRUCTURE. On a narrow phone the "Child care" tab button and
// its panel could be a full screen apart (the shared controls sit between them), so tapping the
// tab visibly did nothing. There is now ONE continuous readout and ONE child-care ON/OFF control
// (data-calc-input="ccOn", a checkbox), not two tabs:
//   - The shared controls (incomes, children, custody, premiums) sit above, unchanged.
//   - The MAIN readout (order_wk / line_7e / true_pct_net / payor_after / recip_after /
//     recip_per_person) always shows the ACTIVE result: the no-child-care numbers when the
//     checkbox is off, the child-care numbers (from the two sliders below) when it is on. There is
//     only ever one set of numbers on the page for those six cells.
//   - Below the main readout, a "Child care" heading holds the checkbox and, revealed directly
//     underneath it when checked (data-calc-childcare-body, toggled via the native `hidden`
//     attribute, aria-expanded/aria-controls on the checkbox), the distribution readout, the two
//     child-care sliders, the with-child-care order and its change from the no-child-care order,
//     the higher earner's share of the lower earner's child care, the combined-both-pay line, and
//     the "apply the proposed fix" toggle. All of that is computed every render() regardless of
//     whether it is visible, so switching the checkbox on never shows a stale number.
//
// v5 (2026-09-07) added two computations to the child-care figures, both from
// model/childcare_post_transfer.py (not a new computation -- see that file's own docstring for the
// five rules it prints and model/test_childcare_post_transfer.py for what pins them):
//   1. THE DISTRIBUTION READOUT (computeChildcareDistribution): the higher earner's Line 3c income
//      share (the pre-order share Line 6b already uses to allocate child care), and where that same
//      pair of incomes actually lands after the NO-CHILD-CARE order -- as a share of gross and, using
//      net-position.js, of net. Independent of the two child-care sliders; it is a property of income,
//      children and the custody box alone. Its net-share leg uses kidsUnder13 = min(2, kids) -- the
//      site's own worked example's fact (two of three children are under 13), NOT the zero used
//      everywhere else in this section -- because the task was to reproduce childcare_post_transfer.py's
//      87.7/64.3/48.2 at that worked example, and that script uses kidsUnder13=2. Every OTHER figure in
//      this section keeps the site-wide zero convention; only this one readout differs, and it says so.
//   2. A TOGGLE (computeFixedRuleOrder), "the comments' Line 6b-2 fallback": recomputes the child-care order by
//      running the worksheet ONCE with no child care to get the base order and the Payor/Recipient
//      designation Line 6f would give in that pass (avoids the circularity a 2026-09-05 review caught --
//      see childcare_post_transfer.py's own header), then allocates the combined child-care dollars on
//      that payor's post-transfer Line 3a share instead of the pre-order Line 3c share. A dedicated
//      sanity check (fixedRuleSanityPasses) gates the toggle alone: if it fails, the toggle disables
//      with a note instead of showing a wrong number, without taking down the rest of the calculator.
//
// v4 (2026-09-07) was an interface rebuild, not a new computation. Two of its three changes remain
// true today (PREMIUMS and STATUS BADGES); its tab structure is what v6 above removes:
//   2. PREMIUMS became two number inputs (was a fixed $33/$43 constant).
//   3. STATUS BADGES. A two-badge strip sits above the readout and updates with it: which
//      household is ahead after tax, and whether the order is at or above 40% of the payor's net
//      income (the true share, INCLUDING the payor's own child care once the section is switched
//      on). This replaces the old data-calc-flag / data-calc-flag-household text flags, which said
//      the same two things in prose.
//
// CHILD CARE COMPOSITION: each of the two child-care sliders is a COMBINED weekly dollar amount
// (one parent's total across all children), spread evenly across `kids` array elements before
// being handed to worksheet.run()'s aChildcare/bChildcare -- e.g. $100 at 3 children becomes
// [33.33, 33.33, 33.33]. This is arithmetically identical to an unspread single-element array
// whenever the total is under the per-child $430 benchmark (Line 6a), which is always true here
// since each slider's own max is $430 x kids. Parent A = lower earner, Parent B = higher earner,
// always, regardless of which the worksheet ultimately names payor (matches
// model/charts/_common.py's order() convention and tools/gen_calculator_childcare_fixtures.py).
//
// "Higher earner's share of lower earner's child care" is Line A_6b, unchanged from the
// worksheet's own definition (the higher earner's income share x the lower earner's own
// benchmarked child care) -- see run()'s return object in assets/js/lib/worksheet.js.
// "The higher earner bears $Y of $X combined" nets both parents' own payments against Lines
// A_6b/B_6b: higher earner's own payment, plus what they owe the lower earner via 6b, minus what
// the lower earner owes them back via 6b. Verified against
// tools/gen_calculator_childcare_fixtures.py's identical Python composition -- see that script's
// header comment for the same decomposition, and assets/js/calculator.test.js PART 6, which
// checks every fixture row (including this quantity) to the dollar.
//
// Correctness gate: assets/js/fixtures/calculator-childcare.json (219 rows: 3 children x 2
// custody boxes x 2 premium pairs x 3 child-care pairs x 6 income pairs, plus 3 hand-picked extra
// rows at the worked-example incomes), generated by tools/gen_calculator_childcare_fixtures.py
// from this repo's own model/.
//
// ---------------------------------------------------------------------------------------------
// MARKUP CONTRACT (see index.html's #calculator section for the actual markup)
// ---------------------------------------------------------------------------------------------
// <div class="tool tool-two-up" data-calculator>
//   <input data-calc-input="higher"> <input data-calc-input="lower">   (income sliders, shared)
//   <input data-calc-radio="kids">   <input data-calc-radio="box">     (shared)
//   <input data-calc-radio="credits" value="1|0">                     (shared, default "1")
//   <input data-calc-input="healthHigh"> <input data-calc-input="healthLow">  (number inputs, shared)
//   <span data-calc-badge="household">  <span data-calc-badge="hardship">    (status strip, shared)
//   <div data-calc-panel="main">    ... data-calc-cell="order_wk" / "line_7e" / "true_pct_net" ...
//                                    ... data-calc-cell="payor_after" / "recip_after" / "recip_per_person" ...
//                                    (always the ACTIVE result -- no child care when ccOn is off,
//                                    the two sliders' figures when it is on: one set of numbers)
//   <div data-calc-childcare>
//     <input data-calc-radio="ccOn" type="radio" value="0"> <input data-calc-radio="ccOn" type="radio" value="1">
//     <span data-calc-cc-state>                              (heading state, "not included"/"included")
//     <div id="calc-childcare-body" hidden>            (revealed in place when ccOn radio "1" is checked)
//       ... data-calc-cell="cc_dist_share3c" / "cc_dist_gross" / "cc_dist_net" ...
//       <input data-calc-input="ccLower"> <input data-calc-input="ccHigher">  (child-care sliders)
//       ... data-calc-cell="cc_order_wk" / "cc_delta_wk" / "cc_share_pct" / "cc_share_wk" ...
//       ... data-calc-cell="cc_combined_line" (only filled in when BOTH sliders > 0) ...
//       <input data-calc-radio="ccRule" type="radio" value="worksheet|nettax|linebased">  (the rule selector)
//       ... data-calc-cell="cc_rule_note" (one sentence, full text set by rule) ...
//       ... data-calc-note="cc_rule" (disable message if a rule's own sanity check fails) ...
//     </div>
//   </div>
// </div>
//
// - Every `data-calc-*` element MUST already contain the real, precomputed defaults as static
//   text (no-JS fallback) -- see index.html. A no-JS visitor sees the default (no-child-care)
//   reading stated correctly and only loses the ability to change any control, including turning
//   child care on -- the checkbox is inert without JS, so the child-care body (already `hidden` in
//   the markup) stays unreachable, an acceptable narrowing of the existing no-JS fallback, since
//   the main readout still renders a complete, correct, static reading.
// - SANITY GUARD: before wiring up any control, this script recomputes TWO fixed scenarios,
//   independent of whatever the UI currently shows or whatever premiums/child-care the reader has
//   entered -- $33/$43 premiums, kids=3, box=1, at the worked-example incomes, with $0 and then
//   $300/wk (lower earner only) child care -- and checks the weekly order rounds to $1,013 and
//   $1,276 respectively (calculator.test.js PARTS 1-2 and 6 pin the same two numbers). If either
//   fails, every control is disabled and a visible "calculator unavailable" message replaces every
//   number -- never a plausible-looking wrong figure.
(function () {
  'use strict';

  if (typeof window === 'undefined') return; // Node (calculator.test.js) loads the libs directly.

  var W = window.MCSGWorksheet;
  var N = window.MCSGNetPosition;

  function money(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/yr'; }
  function moneyWk(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/wk'; }
  function pct1(v) { return (v * 100).toFixed(1) + '%'; }
  function pct0(v) { return Math.round(v * 100) + '%'; }
  function signedMoneyWk(v) {
    var sign = v >= 0 ? '+' : '−';
    return sign + '$' + Math.round(Math.abs(v)).toLocaleString('en-US') + '/wk';
  }

  // A combined weekly dollar amount spread evenly across `kids` array elements -- see the header
  // comment above. Identical to model/charts and tools/gen_calculator_childcare_fixtures.py.
  function spreadCC(total, kids) {
    if (!total) return [];
    var per = total / kids;
    var out = [];
    for (var i = 0; i < kids; i++) out.push(per);
    return out;
  }

  // The single computation this whole tool is built on. `facts` = { kids, box, healthLow,
  // healthHigh, ccLower, ccHigher, credits }. ccLower/ccHigher are the two child-care sliders'
  // combined weekly totals (Parent A = lower earner, Parent B = higher earner, always -- see
  // header). `credits` (added 2026-09-08, defaults to true if omitted) is the credits-off switch:
  // false removes every refundable tax credit from payor_after/recip_after/recip_per_person/
  // true_pct_net, so a reader who does not accept the who-claims-which-child assumption behind
  // those credits -- an economist, most pointedly -- can check the arithmetic without it. See
  // assets/js/lib/net-position.js's analyze() and model/net_position.py's own docstring.
  // Exported on window for calculator.test.js and a manual console spot-check.
  function computeWithFacts(higherAnnual, lowerAnnual, facts) {
    var lowerWk = lowerAnnual / 52.0;
    var higherWk = higherAnnual / 52.0;
    var aCc = spreadCC(facts.ccLower || 0, facts.kids);
    var bCc = spreadCC(facts.ccHigher || 0, facts.kids);
    var r = W.run(facts.box, lowerWk, higherWk, facts.kids, 0,
      { aHealth: facts.healthLow, bHealth: facts.healthHigh, aChildcare: aCc, bChildcare: bCc });
    var payorGross = r.payor === 'A' ? lowerAnnual : higherAnnual;
    var recipGross = r.payor === 'A' ? higherAnnual : lowerAnnual;

    var aOwnCc = aCc.reduce(function (s, v) { return s + v; }, 0);
    var bOwnCc = bCc.reduce(function (s, v) { return s + v; }, 0);
    var weeklyChildcare = aOwnCc + bOwnCc;
    var payorOwnCc = r.payor === 'A' ? aOwnCc : bOwnCc;
    var payorChildcareShare = weeklyChildcare > 0 ? payorOwnCc / weeklyChildcare : 0.0;

    // kids_under_13 fixed at 0 -- the generic-grid convention used across this site (no control
    // for how many children are under 13); see CONVENTIONS.md SS11. box=facts.box (v10, 2026-09-08):
    // who claims the children for tax purposes now follows the custody box the reader selected,
    // instead of always defaulting to "recipient claims everyone" -- see the v10 header note.
    // credits (v11, 2026-09-08; default false 2026-09-09 Task 3; DEFAULT FLIPPED BACK TO TRUE
    // 2026-09-09 evening: leave refundable tax credits on with the option to turn them off,
    // as the better default for the tool. This is the TOOL's default only.
    // net_position.py's analyze() still defaults to FALSE, and every figure in the comments, on
    // the finding pages and in the charts is computed on that withholding basis -- the tool
    // passes an explicit value either way, so the two never disagree. Fixtures cover both.
    var countCredits = facts.credits === undefined ? true : facts.credits;
    var pos = N.analyze(payorGross, recipGross, facts.kids, r['7d'], weeklyChildcare,
      payorChildcareShare, undefined, 0, facts.box, countCredits);

    // Line A_6b: the higher earner's (B's) income-share x the lower earner's (A's) own
    // benchmarked child care -- literally "the higher earner's share of the lower earner's child
    // care." See the header comment for the "bears" decomposition.
    var higherShareOfLowerWk = r.A_6b;
    var higherShareOfLowerPct = r.A_6a ? r.A_6b / r.A_6a : 0.0;
    var higherBearsWk = bOwnCc - r.B_6b + r.A_6b;
    var higherBearsPct = weeklyChildcare > 0 ? higherBearsWk / weeklyChildcare : 0.0;

    return {
      order_wk: r['7d'],
      line_7e: r['7e'],
      true_pct_net: pos.burden_pct_of_payor_net,
      payor_after: pos.payor_after,
      recip_after: pos.recip_after,
      recip_per_person: pos.recip_per_person,
      payor_is: r.payor === 'A' ? 'lower' : 'higher',
      combined_wk: weeklyChildcare,
      higher_share_of_lower_wk: higherShareOfLowerWk,
      higher_share_of_lower_pct: higherShareOfLowerPct,
      higher_bears_wk: higherBearsWk,
      higher_bears_pct: higherBearsPct
    };
  }

  // CHANGE 1 -- the Child care section's distribution readout. Port of
  // model/childcare_post_transfer.py's rule1_share (Line 3c) / rule2_gross_share / rule3_share, at
  // the NO-CHILD-CARE order -- the author's direction: "have the base support calculated first and
  // then figure out what the net percentage mix is." Independent of facts.ccLower/facts.ccHigher; only
  // kids/box/healthLow/healthHigh matter. "Higher earner" is Parent B always (see header comment);
  // every fixture row this site has ever computed names B the payor, so this does not special-case
  // a flip. net_share uses kidsUnder13 = 0 (the same convention as every other figure in this
  // calculator, see v7 header comment) -- it is also the "on money after tax" rule's own share
  // (computeNetRuleOrder), since the fixed point in childcare_post_transfer.py's rule4 always
  // equals rule3's cc=0 share; no separate function needed for that number.
  function computeChildcareDistribution(higherAnnual, lowerAnnual, facts) {
    var lowerWk = lowerAnnual / 52.0, higherWk = higherAnnual / 52.0;
    var r0 = W.run(facts.box, lowerWk, higherWk, facts.kids, 0,
      { aHealth: facts.healthLow, bHealth: facts.healthHigh });
    var baseOrderWk = r0['7d'];
    var combinedGross = higherAnnual + lowerAnnual;
    var grossShare = combinedGross ? (higherAnnual - baseOrderWk * 52) / combinedGross : 0.0;
    // box=facts.box (v10): see the v10 header note -- who claims the children now follows the
    // selected custody box for this analytical figure too. credits: FIXED TRUE (2026-09-09,
    // Task 3), no longer tracking facts.credits -- net_share is the credits-included ANALYSIS
    // figure (matches childcare_post_transfer.py's rule 3, the fixture generator's
    // distribution(), and calculator.test.js's own computeDistribution()), not the
    // withholding-basis ask. It is not currently bound to any visible cell (cc_dist_net shows
    // net_withholding_share, which never counts credits) -- kept correct here regardless.
    var pos = N.analyze(higherAnnual, lowerAnnual, facts.kids, baseOrderWk, 0.0, 0.0, undefined, 0, facts.box, true);
    // v9: the withholding-basis post-transfer share -- tax and FICA only, single filer, no
    // exemptions, no refundable credits. This is what Section 2 of the comments asks for as of
    // v4.9, because CJ-D 304 collects neither filing status nor who claims which child; net_share
    // above (credits included) stays as the analytical figure shown in the distribution callout.
    var pw = N.netIncomeWithholdingBasis(higherAnnual);
    var rw = N.netIncomeWithholdingBasis(lowerAnnual);
    var aw = pw - baseOrderWk * 52, bw = rw + baseOrderWk * 52;
    var netWithholdingShare = (aw + bw) ? aw / (aw + bw) : 0.0;
    return {
      base_order_wk: baseOrderWk,
      share3c: r0.B_3c,
      gross_share: grossShare,
      net_share: pos.payor_after_share,
      net_withholding_share: netWithholdingShare
    };
  }

  // CHANGE 3 (v7, mechanism fixed v9) -- "on money after tax", the rule this project recommends.
  // The higher earner's share is computeChildcareDistribution's own net_withholding_share (v9: the
  // withholding basis, no refundable credits -- childcare_post_transfer.py's rule5, the figure
  // Section 2 of the comments asks for as of v4.9). The order MOVES: base_order_wk plus that share
  // of the combined child care, because the letter's Line 6b-1 redline sits inside the Worksheet's
  // own 6b -> 6c -> 6e -> 6g -> 7b -> 7d chain, the same linear step the "on income after the
  // order" fallback below already uses. (Superseded description: v7-v8 kept the order at the
  // no-child-care base and described this as a private side payment -- that modelled a different
  // remedy from the one the letter proposes and was fixed 2026-09-08.)
  function computeNetRuleOrder(higherAnnual, lowerAnnual, facts) {
    var dist = computeChildcareDistribution(higherAnnual, lowerAnnual, facts);
    var totalChildcare = (facts.ccLower || 0) + (facts.ccHigher || 0);
    // v9: the share is the WITHHOLDING-basis post-transfer net share, and the child care
    // it allocates moves through the ORDER, because the letter's Line 6b-1 feeds
    // 6b -> 6c -> 6e -> 6g -> 7b -> 7d. Same linear step the gross fallback (linebased) uses.
    var share = dist.net_withholding_share;
    return {
      base_order_wk: dist.base_order_wk,
      net_rule_share: share,
      net_rule_order_wk: dist.base_order_wk + share * totalChildcare,
      net_rule_charge_wk: share * totalChildcare
    };
  }

  // CHANGE 2 -- the "apply the proposed fix" toggle. Port of childcare_post_transfer.py's rule2b:
  // run the worksheet with NO child care to get the base order and the Payor/Recipient designation
  // Line 6f would give in that pass, then allocate the COMBINED weekly child care on that payor's
  // post-transfer Line 3a share (Line 3a moved by the base order, over Line 3b) instead of the
  // pre-order Line 3c share Line 6b uses today. This is the letter's Section 2 gross fallback, new
  // Worksheet Line 6b-2 (the primary ask is the withholding-basis Line 6b-1, computed elsewhere in
  // this file). Uses r0.payor generically (not a hardcoded "B") to match the Python's own
  // "whichever parent Line 6f names payor in that pass" -- see the file's header comment on why a
  // literal Payor/Recipient label from an EARLIER pass, not the current one, avoids a circularity a
  // 2026-09-05 review caught.
  function computeFixedRuleOrder(higherAnnual, lowerAnnual, facts) {
    var lowerWk = lowerAnnual / 52.0, higherWk = higherAnnual / 52.0;
    var r0 = W.run(facts.box, lowerWk, higherWk, facts.kids, 0,
      { aHealth: facts.healthLow, bHealth: facts.healthHigh });
    var baseOrderWk = r0['7d'];
    var payorThreeA = r0.payor === 'A' ? r0.A_3a : r0.B_3a;
    var combinedThreeB = r0['3b'];
    var share = combinedThreeB ? (payorThreeA - baseOrderWk) / combinedThreeB : 0.0;
    var totalChildcare = (facts.ccLower || 0) + (facts.ccHigher || 0);
    return {
      base_order_wk: baseOrderWk,
      fixed_rule_share: share,
      fixed_rule_order_wk: baseOrderWk + share * totalChildcare
    };
  }

  // Sanity guard targets: $33/$43 premiums, kids=3, box=1, worked-example incomes, independent of
  // any UI state. See calculator.test.js PARTS 1/2/6 for the same two figures.
  var SANITY_HIGHER = 201000, SANITY_LOWER = 29640;
  var SANITY_NO_CC = { kids: 3, box: 1, healthLow: 33.0, healthHigh: 43.0, ccLower: 0, ccHigher: 0 };
  var SANITY_CC = { kids: 3, box: 1, healthLow: 33.0, healthHigh: 43.0, ccLower: 300, ccHigher: 0 };

  // The Change-1 readout's own sanity target: $33/$43 premiums, kids=3, box=1, worked-example
  // incomes, no child care -- reproduces net_position.py's own 87.7% / 64.3% / 49.9% at
  // kidsUnder13=0 (rule1_share / rule2_gross_share / rule3_share, the same convention as the rest
  // of this calculator; see v7 header comment). net_share went 48.4% (pre-box-fix) -> 52.1% (the
  // FIRST, superseded Box 1 fix, which swapped filing status/EITC along with the CTC) -> 49.9%
  // (v12, 2026-09-08 same day, ported from private commit 723a7bf: only the CTC/dependency claim
  // alternates by year; head of household and the EITC stay with the physical-custodian recipient
  // in both years -- see net-position.js's householdNetIncomes()). If this fails it is as serious
  // as the order itself being wrong, so it is folded into the main guard below, not the
  // rule-selector-only one.
  function distributionSanityPasses() {
    try {
      var d = computeChildcareDistribution(SANITY_HIGHER, SANITY_LOWER, SANITY_NO_CC);
      return Math.round(d.share3c * 1000) === 877 &&
             Math.round(d.gross_share * 100) === 64 &&
             Math.round(d.net_share * 1000) === 499;
    } catch (e) {
      if (window.console) console.error('calculator.js: distribution sanity check threw', e);
      return false;
    }
  }

  // The credits-off switch's own sanity target: worked example, no child care, credits off ->
  // both parties' net income is net_position.py's net_income_withholding_basis() alone, payor
  // keeps $87,172, recipient household holds $77,395. FIXED 2026-09-08 (found during v12 browser
  // verification, unrelated to the box fix -- credits-off mode ignores box entirely): this used to
  // say $77,396, model/test_net_position.py's pinned figure for a FIXED, rounded-to-cents order of
  // $1,012.73/wk. computeWithFacts() here instead feeds the LIVE, unrounded worksheet order
  // ($1,012.7257303613252/wk), which is correct -- the calculator never rounds the order before
  // using it in a downstream computation, only for display -- but it lands at $77,395.48, which
  // rounds to $77,395, not $77,396. Verified against Python at the identical unrounded order. If
  // this fails the switch is wrong, which is as serious as the order itself being wrong, so it is
  // folded into the main guard.
  var SANITY_NO_CC_NOCREDITS = { kids: 3, box: 1, healthLow: 33.0, healthHigh: 43.0, ccLower: 0, ccHigher: 0, credits: false };
  function creditsOffSanityPasses() {
    try {
      var r = computeWithFacts(SANITY_HIGHER, SANITY_LOWER, SANITY_NO_CC_NOCREDITS);
      return Math.round(r.payor_after) === 87172 && Math.round(r.recip_after) === 77395;
    } catch (e) {
      if (window.console) console.error('calculator.js: credits-off sanity check threw', e);
      return false;
    }
  }

  function sanityCheckPasses() {
    try {
      var noCc = computeWithFacts(SANITY_HIGHER, SANITY_LOWER, SANITY_NO_CC);
      var withCc = computeWithFacts(SANITY_HIGHER, SANITY_LOWER, SANITY_CC);
      return Math.round(noCc.order_wk) === 1013 && Math.round(withCc.order_wk) === 1276 &&
             distributionSanityPasses() && creditsOffSanityPasses();
    } catch (e) {
      if (window.console) console.error('calculator.js: sanity check threw', e);
      return false;
    }
  }

  // The "on income after the order" rule's OWN gate, separate from the main guard above: worked
  // example, $300 lower-earner child care, this rule on -> $1,206/wk (childcare_post_transfer.py's
  // rule2b_7d). If this fails, only that rule's radio disables (see initCalculator) -- the rest of
  // the calculator keeps working, per the brief: never show a wrong number, but don't take down the
  // whole tool for one figure either.
  function fixedRuleSanityPasses() {
    try {
      var f = computeFixedRuleOrder(SANITY_HIGHER, SANITY_LOWER, SANITY_CC);
      return Math.round(f.fixed_rule_order_wk) === 1206;
    } catch (e) {
      if (window.console) console.error('calculator.js: fixed-rule sanity check threw', e);
      return false;
    }
  }

  // The "on money after tax" rule's OWN gate, mirroring the one above: worked example, $300
  // lower-earner child care, withholding-basis share 53.0%, order $1,172/wk (rounds from
  // model/childcare_post_transfer.py's rule5_7d, $1,171.64).
  function netRuleSanityPasses() {
    try {
      var n = computeNetRuleOrder(SANITY_HIGHER, SANITY_LOWER, SANITY_CC);
      return Math.round(n.net_rule_order_wk) === 1172 && Math.round(n.net_rule_share * 1000) === 530;
    } catch (e) {
      if (window.console) console.error('calculator.js: net-rule sanity check threw', e);
      return false;
    }
  }

  function showUnavailable(root, allInputs, allRadios, allCells, allBadges) {
    root.setAttribute('data-calc-unavailable', 'true');
    allInputs.forEach(function (el) { el.disabled = true; });
    allRadios.forEach(function (el) { el.disabled = true; });
    allCells.forEach(function (el) {
      if (el.hasAttribute('data-calc-cell')) el.textContent = 'not available';
    });
    allBadges.forEach(function (el) {
      el.textContent = 'Calculator unavailable';
      el.className = 'tool-flagline';
      el.hidden = false;
    });
    if (window.console) console.error('calculator.js: sanity check failed -- worked example did not reproduce $1,013/$1,276');
  }

  function initCalculator(root) {
    if (!W || !N) {
      root.setAttribute('data-calc-load-failed', 'true');
      if (window.console) console.error('calculator.js: assets/js/lib/worksheet.js or net-position.js not loaded');
      return;
    }

    var inputs = {};
    Array.prototype.slice.call(root.querySelectorAll('[data-calc-input]')).forEach(function (el) {
      inputs[el.getAttribute('data-calc-input')] = el;
    });
    // The editable income fields (data-calc-income-edit="higher"/"lower") are a second, typed
    // path to the SAME two sliders in `inputs` above -- not a new fact. Kept in their own map so
    // they can be disabled by showUnavailable() and wired below without disturbing `inputs`,
    // which the rest of this file treats as "the slider is the source of truth."
    var incomeEdits = {};
    Array.prototype.slice.call(root.querySelectorAll('[data-calc-income-edit]')).forEach(function (el) {
      incomeEdits[el.getAttribute('data-calc-income-edit')] = el;
    });
    var radios = Array.prototype.slice.call(root.querySelectorAll('[data-calc-radio]'));
    var allInputs = Object.keys(inputs).map(function (k) { return inputs[k]; })
      .concat(Object.keys(incomeEdits).map(function (k) { return incomeEdits[k]; }));
    var cells = {};
    Array.prototype.slice.call(root.querySelectorAll('[data-calc-cell]')).forEach(function (el) {
      cells[el.getAttribute('data-calc-cell')] = el;
    });
    var notes = {};
    Array.prototype.slice.call(root.querySelectorAll('[data-calc-note]')).forEach(function (el) {
      notes[el.getAttribute('data-calc-note')] = el;
    });
    var badges = {};
    Array.prototype.slice.call(root.querySelectorAll('[data-calc-badge]')).forEach(function (el) {
      badges[el.getAttribute('data-calc-badge')] = el;
    });
    var ccBody = root.querySelector('[data-calc-childcare] .tool-childcare-body');
    var ccStateLabel = root.querySelector('[data-calc-cc-state]');

    // The two incomes' EXACT committed values, independent of what a <input type="range"> can
    // hold. A range input's own value-sanitization algorithm snaps whatever is assigned to
    // `.value` onto the step grid -- confirmed empirically (assigning "187450" to a step=120
    // slider reads back "187440"), which is exactly the $29,640-snapped-to-$30,000 bug this
    // typed-input feature exists to not repeat. So `committed` is the one source of truth render()
    // computes from; the sliders are a second, approximate INPUT path that happens to always land
    // on-step (a drag can only stop at a step), and their on-screen thumb position is a third,
    // purely VISUAL approximation of `committed` that may itself snap to the nearest step when an
    // off-step typed value is written into it -- never read back for computation.
    var committed = { higher: Number(inputs.higher.value), lower: Number(inputs.lower.value) };

    // Visual-only: sets a slider's thumb position from `committed`. May snap to the slider's own
    // step grid (see the note above) -- that is fine, since nothing downstream reads it back.
    function syncSliderVisual(which) {
      var slider = inputs[which];
      if (slider) slider.value = String(committed[which]);
    }

    // Same rule slider-dragging has always used (touch, never cross), now applied to `committed`
    // instead of the sliders' own .value, so it works whether the crossing was produced by a drag
    // or by a typed edit.
    function clampCrossedCommitted(moved) {
      if (committed.higher < committed.lower) {
        if (moved === 'lower') committed.lower = committed.higher;
        else committed.higher = committed.lower;
      }
    }

    if (!sanityCheckPasses()) {
      showUnavailable(root, allInputs, radios,
        Object.keys(cells).map(function (k) { return cells[k]; }),
        Object.keys(badges).map(function (k) { return badges[k]; }));
      return;
    }

    function outputFor(input) {
      return document.getElementById(input.id + '-output') || root.querySelector('output[for="' + input.id + '"]');
    }

    // outputFor() resolves both a plain <output> (child-care sliders) and the editable income
    // <input type="text"> (higher/lower earner) by the same "id + '-output'" convention -- an
    // <output>'s display text is its child text node, an <input>'s is its `value` property. This
    // is the one place that distinction has to be made explicit.
    function setDisplayText(el, text) {
      if (!el) return;
      if (el.tagName === 'INPUT') el.value = text;
      else el.textContent = text;
    }

    function setNote(key, text) {
      var el = notes[key];
      if (!el) return;
      if (text) { el.textContent = text; el.classList.add('visible'); }
      else { el.textContent = ' '; el.classList.remove('visible'); }
    }

    // A flag is an annotation, not a control: it appears only when its condition is true, and it
    // is hidden outright otherwise (owner, 2026-09-07: the old always-on pills read as buttons a
    // reader could click). `mutedText` is accepted and ignored so existing call sites still work.
    function setBadge(key, lit, litText, mutedText) {
      var el = badges[key];
      if (!el) return;
      if (lit) {
        el.textContent = litText;
        el.className = 'tool-flagline';
        el.hidden = false;
      } else {
        el.textContent = '';
        el.className = 'tool-flagline';
        el.hidden = true;
      }
    }

    function currentFacts() {
      var ccOnRadio = document.querySelector('[data-calc-radio="ccOn"]:checked');
      var ccRuleRadio = document.querySelector('[data-calc-radio="ccRule"]:checked');
      var creditsRadio = document.querySelector('[data-calc-radio="credits"]:checked');
      return {
        kids: Number(document.querySelector('[data-calc-radio="kids"]:checked').value),
        box: Number(document.querySelector('[data-calc-radio="box"]:checked').value),
        healthHigh: Number(inputs.healthHigh.value) || 0,
        healthLow: Number(inputs.healthLow.value) || 0,
        ccOn: ccOnRadio ? ccOnRadio.value === '1' : false,
        ccLower: inputs.ccLower ? Number(inputs.ccLower.value) || 0 : 0,
        ccHigher: inputs.ccHigher ? Number(inputs.ccHigher.value) || 0 : 0,
        ccRule: ccRuleRadio ? ccRuleRadio.value : 'worksheet',
        // The credits-off switch (added 2026-09-08; DEFAULT FLIPPED TO FALSE 2026-09-09, Task 3).
        // Defaults to TRUE (count them) if the control is missing from the markup, matching the
        // tool's own default as of 2026-09-09 evening. The published figures elsewhere on this
        // site remain on the withholding basis; see the note at countCredits above.
        credits: creditsRadio ? creditsRadio.value === '1' : true
      };
    }

    // The Child-care sliders' max is $430/child; update it (and clamp the current value) whenever
    // the children radio changes, so the slider can never claim more than the benchmark allows.
    function updateChildcareBounds(kids) {
      if (!inputs.ccLower || !inputs.ccHigher) return;
      var max = 430 * kids;
      [inputs.ccLower, inputs.ccHigher].forEach(function (el) {
        el.max = String(max);
        if (Number(el.value) > max) el.value = String(max);
      });
    }

    function renderIncomeOutputs(higher, lower) {
      var out = outputFor(inputs.higher);
      setDisplayText(out, money(higher));
      inputs.higher.setAttribute('aria-valuetext', 'Higher earner: ' + money(higher).replace('/yr', '') + ' a year');
      var outLo = outputFor(inputs.lower);
      setDisplayText(outLo, money(lower));
      inputs.lower.setAttribute('aria-valuetext', 'Lower earner: ' + money(lower).replace('/yr', '') + ' a year');
    }

    // Parses whatever a visitor typed into an income field: strips everything but digits and a
    // single decimal point (so "$187,450", "187450", " 187,450.00 " and "187450 dollars" all
    // parse; a bare "-" is treated the same as any other non-digit and dropped, so a typed
    // negative reads as its magnitude rather than erroring). Returns NaN -- never a rejected
    // number -- for empty or non-numeric input, so the caller knows to abandon rather than commit.
    function parseIncomeInput(raw) {
      if (raw == null) return NaN;
      var cleaned = String(raw).replace(/[^0-9.]/g, '');
      if (!cleaned) return NaN;
      var firstDot = cleaned.indexOf('.');
      if (firstDot !== -1) {
        cleaned = cleaned.slice(0, firstDot + 1) + cleaned.slice(firstDot + 1).replace(/\./g, '');
      }
      var n = parseFloat(cleaned);
      return isFinite(n) ? Math.round(n) : NaN;
    }

    // Commits a typed income: parse, clamp into the slider's own [min, max] (a typed $5,000,000
    // lands at the slider's $300,000 ceiling, not off the model's tested range), apply the same
    // higher/lower crossing rule dragging uses, then render. The clamped value goes straight into
    // `committed` -- NEVER through a slider's own .value setter, which would snap it onto the
    // $120 step grid (see the note above `committed`'s declaration). That exact figure is what
    // every downstream computation uses; the sliders' thumb positions are re-synced from it purely
    // for display and may visually approximate it. Invalid input (empty, no digits) is rejected
    // outright: nothing is parsed or applied, and render() just redraws the field with the
    // last-committed value, so a rejected input is never the source of a displayed number.
    function commitIncomeEdit(which, editEl) {
      var slider = inputs[which];
      if (!slider || !editEl) return;
      var parsed = parseIncomeInput(editEl.value);
      if (isNaN(parsed)) { render(); return; }
      var min = Number(slider.min), max = Number(slider.max);
      committed[which] = Math.min(max, Math.max(min, parsed));
      clampCrossedCommitted(which);
      syncSliderVisual('higher');
      syncSliderVisual('lower');
      render();
    }

    function render() {
      // `committed` (not the sliders' own .value) is the source of truth -- see its declaration
      // above for why. Math.max/min stay as defense in depth; clampCrossedCommitted already
      // enforces higher >= lower at every write.
      var higherRaw = committed.higher;
      var lowerRaw = committed.lower;
      var higher = Math.max(higherRaw, lowerRaw);
      var lower = Math.min(higherRaw, lowerRaw);
      renderIncomeOutputs(higher, lower);

      var facts = currentFacts();
      var noCcFacts = { kids: facts.kids, box: facts.box, healthHigh: facts.healthHigh, healthLow: facts.healthLow, ccLower: 0, ccHigher: 0, credits: facts.credits };
      var baseResult = computeWithFacts(higher, lower, noCcFacts);
      var ccResult = computeWithFacts(higher, lower, facts);
      // The single set of numbers the main readout shows: the no-child-care result when the
      // Child care section is off, the two sliders' result when it is on. Computed every render
      // regardless of visibility, so the child-care section never reveals a stale figure.
      var active = facts.ccOn ? ccResult : baseResult;

      // -- Child care section: the distribution readout (Change 1), computed either way so the
      // numbers are already correct the instant the section is revealed. --
      var dist = computeChildcareDistribution(higher, lower, noCcFacts);
      if (cells.cc_dist_share3c) cells.cc_dist_share3c.textContent = pct1(dist.share3c);
      if (cells.cc_dist_gross) cells.cc_dist_gross.textContent = pct0(dist.gross_share);
      // Bound to the WITHHOLDING-basis share (the "on money after tax" rule below, and the
      // figure Section 2 of the comments asks for), not dist.net_share (credits-inclusive,
      // 52% at the worked example as of the same-day box fix; was 48%) -- the two were shown
      // side by side until 2026-09-08 with nothing to say they used different tax bases, while
      // the "What this project asks for" tag pointed at this cell.
      if (cells.cc_dist_net) cells.cc_dist_net.textContent = pct0(dist.net_withholding_share);

      if (inputs.ccLower) {
        var ccLowOut = outputFor(inputs.ccLower);
        if (ccLowOut) ccLowOut.textContent = moneyWk(facts.ccLower);
      }
      if (inputs.ccHigher) {
        var ccHighOut = outputFor(inputs.ccHigher);
        if (ccHighOut) ccHighOut.textContent = moneyWk(facts.ccHigher);
      }

      // -- Main readout: always the ACTIVE result (one set of numbers, not two). --
      if (cells.order_wk) cells.order_wk.textContent = moneyWk(active.order_wk);
      if (cells.line_7e) cells.line_7e.textContent = pct1(active.line_7e);
      if (cells.true_pct_net) {
        cells.true_pct_net.textContent = pct1(active.true_pct_net);
        cells.true_pct_net.classList.toggle('is-warning', active.true_pct_net >= 0.40);
      }
      if (cells.payor_after) cells.payor_after.textContent = money(active.payor_after);
      if (cells.recip_after) {
        cells.recip_after.textContent = money(active.recip_after);
        var ahead = active.recip_after > active.payor_after;
        cells.recip_after.classList.toggle('is-warning', ahead);
        setNote('recip_after', ahead ? 'Above the payor' : '');
      }
      if (cells.recip_per_person) cells.recip_per_person.textContent = money(active.recip_per_person);

      // -- Child care section body: the with-child-care order, its change from the no-child-care
      // order above, the allocation, and the combined-both-pay line. --
      if (cells.cc_order_wk) cells.cc_order_wk.textContent = moneyWk(ccResult.order_wk);
      if (cells.cc_delta_wk) cells.cc_delta_wk.textContent = signedMoneyWk(ccResult.order_wk - baseResult.order_wk);
      if (cells.cc_share_pct) cells.cc_share_pct.textContent = facts.ccLower > 0 ? pct1(ccResult.higher_share_of_lower_pct) : '—';
      if (cells.cc_share_wk) {
        cells.cc_share_wk.textContent = facts.ccLower > 0 ? money(ccResult.higher_share_of_lower_wk * 52) : '—';
      }
      if (cells.cc_combined_line) {
        if (facts.ccLower > 0 && facts.ccHigher > 0) {
          cells.cc_combined_line.textContent = 'Of ' + money(ccResult.combined_wk * 52) + ' combined child care, the higher ' +
            'earner bears ' + money(ccResult.higher_bears_wk * 52) + ' (' + pct1(ccResult.higher_bears_pct) + ').';
          cells.cc_combined_line.classList.add('visible');
        } else {
          cells.cc_combined_line.textContent = '';
          cells.cc_combined_line.classList.remove('visible');
        }
      }

      // -- Child care section: the three-way allocation-rule selector (v7). All three rules are
      // computed every render, independent of which is selected, same policy as the rest of this
      // section. A rule whose own sanity check fails disables its radio and falls back to "As the
      // Worksheet does it" rather than showing a wrong number. --
      var ccRuleRadios = {};
      Array.prototype.slice.call(root.querySelectorAll('[data-calc-radio="ccRule"]')).forEach(function (el) {
        ccRuleRadios[el.value] = el;
      });
      var fixOk = fixedRuleSanityPasses();
      var netOk = netRuleSanityPasses();
      if (ccRuleRadios.linebased) ccRuleRadios.linebased.disabled = !fixOk;
      if (ccRuleRadios.nettax) ccRuleRadios.nettax.disabled = !netOk;
      var selectedRule = facts.ccRule;
      if ((selectedRule === 'linebased' && !fixOk) || (selectedRule === 'nettax' && !netOk)) {
        selectedRule = 'worksheet';
        if (ccRuleRadios.worksheet) ccRuleRadios.worksheet.checked = true;
      }
      var unavailableRules = [];
      if (!netOk) unavailableRules.push('on take-home pay, after the order');
      if (!fixOk) unavailableRules.push('on gross income, after the order');
      setNote('cc_rule', unavailableRules.length ? ('Unavailable: ' + unavailableRules.join(', ') + '.') : '');

      var totalChildcareWk = facts.ccLower + facts.ccHigher;
      var fixResult = computeFixedRuleOrder(higher, lower, facts);
      var netResult = computeNetRuleOrder(higher, lower, facts);
      var worksheetChargeWk = dist.share3c * totalChildcareWk;
      var linebasedChargeWk = fixResult.fixed_rule_share * totalChildcareWk;
      var ruleNote = '';
      if (selectedRule === 'nettax') {
        ruleNote = 'On take-home pay, after the order, the higher earner would carry ' + pct1(netResult.net_rule_share) +
          ' (' + money(netResult.net_rule_charge_wk * 52) + ') of the child care, and the order would be ' +
          moneyWk(netResult.net_rule_order_wk) + ' instead of the Worksheet’s ' + moneyWk(ccResult.order_wk) + '.';
      } else if (selectedRule === 'linebased') {
        ruleNote = 'On gross income, after the order, the higher earner would be charged ' + pct1(fixResult.fixed_rule_share) +
          ' (' + money(linebasedChargeWk * 52) + ') of the child care through the order. Resulting order ' +
          moneyWk(fixResult.fixed_rule_order_wk) + ', the Worksheet gives ' + moneyWk(ccResult.order_wk) + '.';
      } else {
        ruleNote = 'The Worksheet charges the higher earner ' + pct1(dist.share3c) +
          ' (' + money(worksheetChargeWk * 52) + ') of the child care, while he holds ' + pct0(dist.gross_share) +
          ' of the money after the order on paper and ' + pct0(dist.net_withholding_share) + ' of it after tax.';
      }
      if (cells.cc_rule_note) cells.cc_rule_note.textContent = ruleNote;

      // -- Status strip: reflects whichever result is active (see `active` above). --
      // "impossible" (2026-09-10, red team F2): an extreme but slider-reachable combination
      // (a low income, high claimed child care) can make the order bigger than the payor has
      // anything left to pay it from. The Worksheet's own arithmetic does not stop that -- it
      // is a defect this site documents, not a bug to hide -- so the figures stay on screen,
      // but never without this flag naming what they are.
      setBadge('impossible', active.payor_after < 0,
        'This combination makes the order bigger than the payor has left after tax. The '
        + 'Worksheet’s own formula allows that -- it is one of the defects this site documents -- '
        + 'so read the figures below as what the formula produces, not an order a court could '
        + 'actually collect.', '');
      // The seam (2026-09-11, cold read): with credits counted -- the default -- this flag lights
      // at the site's own worked example, while every findings page, on the published
      // credits-off withholding basis, has the payor ahead. Both are right under their own basis,
      // and which basis you use is itself one of the findings. But a reader who meets the
      // contradiction here and finds no explanation until a block 100 lines down has simply been
      // contradicted. Name the cause where the flip is visible, and point at the control that
      // undoes it rather than asserting a counterfactual figure the reader cannot check.
      setBadge('household', active.recip_after > active.payor_after,
        'The recipient household ends up with more money than the payor.'
        + (facts.credits
            ? ' Counting the refundable tax credits is what puts it there; every published figure'
              + ' on this site leaves them out. Switch them off above to see the difference.'
            : ''), '');
      setBadge('hardship', active.true_pct_net >= 0.40,
        'The order takes ' + pct1(active.true_pct_net) + ' of the payor’s net income, past the 40 percent '
        + 'the Guidelines call a hardship.', '');

      // -- Child care section: reveal the body in place directly under the control, and keep the
      // heading's state text (and the "with child care" radio's aria-expanded) honest. --
      var ccOnWithRadio = document.querySelector('[data-calc-radio="ccOn"][value="1"]');
      if (ccOnWithRadio) ccOnWithRadio.setAttribute('aria-expanded', facts.ccOn ? 'true' : 'false');
      if (ccStateLabel) {
        ccStateLabel.textContent = facts.ccOn ? 'included' : 'not included';
        ccStateLabel.classList.toggle('is-on', facts.ccOn);
      }
      if (ccBody) {
        if (facts.ccOn) ccBody.removeAttribute('hidden');
        else ccBody.setAttribute('hidden', '');
      }
    }

    // F1 fix (2026-09-10 red team): the two income sliders' native ranges overlap
    // ($60,000-$120,000 on both), so an ordinary drag can push one past the other. render()'s
    // own Math.max/min swap already computed the correct higher/lower VALUES either way, but
    // left the two sliders' own thumb positions and on-screen labels free to disagree with
    // which slider a reader is actually looking at -- confusing even though the arithmetic
    // underneath was right. clampCrossedCommitted (declared above, by `committed`) now carries
    // this rule; a drag re-derives `committed` from the slider that just moved, clamps it against
    // the crossing rule, then re-syncs BOTH thumb positions from `committed` so the two can touch
    // but never cross, and the swap in render() stays pure defense in depth.
    inputs.higher && inputs.higher.addEventListener('input', function () {
      committed.higher = Number(inputs.higher.value);
      clampCrossedCommitted('higher');
      syncSliderVisual('higher');
      syncSliderVisual('lower');
      render();
    });
    inputs.lower && inputs.lower.addEventListener('input', function () {
      committed.lower = Number(inputs.lower.value);
      clampCrossedCommitted('lower');
      syncSliderVisual('higher');
      syncSliderVisual('lower');
      render();
    });
    // 'change' resync (2026-09-10 red team F3): a malformed automation call was observed
    // leaving a slider's raw .value ahead of its own aria-valuetext and the readout below,
    // because that call never dispatched the 'input' event render() listens for. No ordinary
    // mouse, touch or keyboard drag can do this -- a native range input fires 'input'
    // synchronously with every value change as part of the browser's own slider
    // implementation, so render() cannot be skipped by a real gesture -- but 'change' (which
    // fires when a drag or key sequence ends, regardless of what fired mid-drag) costs nothing
    // to also re-derive `committed` from, so any future desync of this kind self-heals the
    // instant the interaction completes rather than waiting for the next unrelated click.
    inputs.higher && inputs.higher.addEventListener('change', function () {
      committed.higher = Number(inputs.higher.value);
      clampCrossedCommitted('higher');
      syncSliderVisual('higher');
      syncSliderVisual('lower');
      render();
    });
    inputs.lower && inputs.lower.addEventListener('change', function () {
      committed.lower = Number(inputs.lower.value);
      clampCrossedCommitted('lower');
      syncSliderVisual('higher');
      syncSliderVisual('lower');
      render();
    });

    // Typed income fields (data-calc-income-edit). Nothing is parsed or applied while the visitor
    // is still typing -- only on Enter or blur, per spec ("commit on both Enter and blur"). Escape
    // abandons the edit: since the underlying slider is never touched mid-edit, redrawing via
    // render() alone restores the last-committed, correctly formatted text with nothing parsed.
    Object.keys(incomeEdits).forEach(function (which) {
      var el = incomeEdits[which];
      el.addEventListener('focus', function () { el.select(); });
      el.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          commitIncomeEdit(which, el);
          el.blur();
        } else if (e.key === 'Escape') {
          e.preventDefault();
          render();
          el.blur();
        }
      });
      el.addEventListener('blur', function () { commitIncomeEdit(which, el); });
    });

    inputs.healthHigh && inputs.healthHigh.addEventListener('input', render);
    inputs.healthLow && inputs.healthLow.addEventListener('input', render);
    inputs.ccLower && inputs.ccLower.addEventListener('input', render);
    inputs.ccHigher && inputs.ccHigher.addEventListener('input', render);
    radios.forEach(function (el) {
      el.addEventListener('change', function () {
        if (el.getAttribute('data-calc-radio') === 'kids') updateChildcareBounds(Number(el.value));
        render();
      });
    });

    updateChildcareBounds(Number(document.querySelector('[data-calc-radio="kids"]:checked').value));
    render();
  }

  window.MCSGCalculatorComputeWithFacts = computeWithFacts;
  window.MCSGCalculatorComputeChildcareDistribution = computeChildcareDistribution;
  window.MCSGCalculatorComputeFixedRuleOrder = computeFixedRuleOrder;
  window.MCSGCalculatorComputeNetRuleOrder = computeNetRuleOrder;
  document.querySelectorAll('[data-calculator]').forEach(initCalculator);
})();
