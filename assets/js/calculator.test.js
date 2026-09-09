#!/usr/bin/env node
// checktheworksheet.org -- fidelity tests for assets/js/lib/worksheet.js and
// assets/js/lib/net-position.js against the project's own Python outputs.
//
// Run with: node assets/js/calculator.test.js
//
// WHAT THIS PROVES, AND WHAT IT DOESN'T. It proves the two ported JS files reproduce, to the
// dollar (round_lines mode) or to six decimal places (unrounded mode), the exact numbers already
// printed by the project's own Python and checked into model/runs/. It does not re-derive the
// worksheet or the tax model independently -- it is a fidelity check on a port, matching the
// project's own convention that no number ships without a script that produces it (see
// model/submission_figures.py's own docstring for the same principle).
//
// Sources of the expected numbers below (all fixed, none invented for this test):
//   - model/runs/official-xfa-vs-model-2026-09-05.txt (six scenarios; A_GROSS=570.0,
//     B_GROSS=3865.38, three children, health premiums $33/$43 -- exactly the inputs
//     model/run_official_xfa.py uses, reproduced here by running python3 model/worksheet.py
//     with the identical arguments on 2026-09-06 to recover full precision, since the .txt file
//     itself only prints two decimal places)
//   - model/runs/submission-figures-run-2026-09-05.txt (the worked example: PAYOR_GROSS
//     $201,000/yr, RECIP_WEEKLY $570/wk -> $29,640/yr, three children, two under 13, Box 1,
//     no child care -- "child care/wk 0" row, and the "TAX POSITION" block)

'use strict';

var path = require('path');
var W = require(path.join(__dirname, 'lib', 'worksheet.js'));
var N = require(path.join(__dirname, 'lib', 'net-position.js'));

var failures = 0, checks = 0;

function close(actual, expected, tol, label) {
  checks++;
  var ok = Math.abs(actual - expected) <= tol;
  if (!ok) {
    failures++;
    console.error('FAIL ' + label + ': got ' + actual + ', expected ' + expected + ' (+/-' + tol + ')');
  } else {
    console.log('ok   ' + label + ': ' + actual);
  }
}

function equal(actual, expected, label) {
  checks++;
  if (actual !== expected) {
    failures++;
    console.error('FAIL ' + label + ': got ' + JSON.stringify(actual) + ', expected ' + JSON.stringify(expected));
  } else {
    console.log('ok   ' + label + ': ' + actual);
  }
}

// ---------------------------------------------------------------------------------------------
// PART 1 -- the six official-xfa-vs-model-2026-09-05.txt scenarios.
// A_GROSS/B_GROSS/health premiums fixed exactly as in model/run_official_xfa.py.
// ---------------------------------------------------------------------------------------------
var A_GROSS = 570.0, B_GROSS = 3865.38, A_HEALTH = 33.0, B_HEALTH = 43.0;

function ccTuple(total) {
  var per = total ? total / 3 : 0.0;
  return [per, per, per];
}

var CASES = [
  {
    label: '1. Box 1 (shared), no child care', box: 1, aCc: 0.0, bCc: 0.0,
    officialRoundedDollar: 1016, unroundedFull: 1012.7247867928149, unroundedE7: 0.264946129582306
  },
  {
    label: '2. Box 2 (Parent A primary), no child care', box: 2, aCc: 0.0, bCc: 0.0,
    officialRoundedDollar: 1091, unroundedFull: 1087.8965874113107, unroundedE7: 0.2846123586381549
  },
  {
    label: '3. Box 2, Parent A pays $300/wk child care', box: 2, aCc: 300.0, bCc: 0.0,
    officialRoundedDollar: 1355, unroundedFull: 1350.941791087063, unroundedE7: 0.353429484009194
  },
  {
    label: '4. Box 1, Parent A pays $300/wk child care', box: 1, aCc: 300.0, bCc: 0.0,
    officialRoundedDollar: 1280, unroundedFull: 1275.7699904685671, unroundedE7: 0.3337632549533451
  },
  {
    label: '5. Box 1, each parent pays $300/wk child care', box: 1, aCc: 300.0, bCc: 300.0,
    officialRoundedDollar: 1274, unroundedFull: 1270.578270747838, unroundedE7: 0.33240501225619584
  },
  {
    label: '6. Box 1, Parent B (payor) pays $300/wk child care', box: 1, aCc: 0.0, bCc: 300.0,
    officialRoundedDollar: 1010, unroundedFull: 1007.5330670720856, unroundedE7: 0.2635878868851568
  }
];

console.log('=== PART 1: six official-xfa-vs-model-2026-09-05.txt scenarios ===\n');

CASES.forEach(function (c) {
  var aCc = ccTuple(c.aCc), bCc = ccTuple(c.bCc);

  var rRound = W.run(c.box, A_GROSS, B_GROSS, 3, 0, {
    aHealth: A_HEALTH, bHealth: B_HEALTH, aChildcare: aCc, bChildcare: bCc, roundLines: true
  });
  var rUnround = W.run(c.box, A_GROSS, B_GROSS, 3, 0, {
    aHealth: A_HEALTH, bHealth: B_HEALTH, aChildcare: aCc, bChildcare: bCc, roundLines: false
  });

  console.log('-- ' + c.label + ' --');
  // round_lines=true reproduces the Commonwealth's own CJ-D 304 XFA calculate-scripts output
  // (model/runs/official-xfa-vs-model-2026-09-05.txt's "OFFICIAL XFA" column) TO THE DOLLAR.
  equal(rRound['7d'], c.officialRoundedDollar, c.label + ' round_lines 7d matches OFFICIAL XFA');
  // Default (unrounded) mode reproduces model/worksheet.py's own "MODEL unround" column to six
  // decimal places -- this is what every dollar figure in the project's letter, paper and
  // MEMORY.md was computed from.
  close(rUnround['7d'], c.unroundedFull, 1e-6, c.label + ' unrounded 7d matches MODEL unround');
  close(rUnround['7e'], c.unroundedE7, 1e-9, c.label + ' unrounded 7e matches MODEL unround');
  equal(rRound.payor, 'B', c.label + ' payor is Parent B, matching official 6f');
  console.log('');
});

// ---------------------------------------------------------------------------------------------
// PART 2 -- the worked example: $201,000/yr payor, $29,640/yr recipient, three children, two
// under 13, Box 1, no child care. Must reproduce $1,013/week (model/runs/submission-figures-run-
// 2026-09-05.txt's "child care/wk 0" row: order 1,013, 7e 26.5%, true % of net 37.7%), plus the
// TAX POSITION block (payor +30.4%, recipient -38.9%).
// ---------------------------------------------------------------------------------------------
console.log('=== PART 2: the worked example ($201,000 / $29,640, three children, Box 1, no child care) ===\n');

var PAYOR_GROSS = 201000.0, RECIP_WEEKLY = 570.0, RECIP_GROSS = RECIP_WEEKLY * 52.0;
var KIDS = 3, KIDS_UNDER_13 = 2;

var we = W.run(1, RECIP_WEEKLY, PAYOR_GROSS / 52.0, KIDS, 0, { aHealth: 33.0, bHealth: 43.0 });

close(we['7d'], 1012.7257303613252, 1e-6, 'worked example 7d (unrounded)');
equal(Math.round(we['7d']), 1013, 'worked example 7d rounded to the dollar = $1,013/week');
close(we['7e'], 0.2649460565232583, 1e-9, 'worked example 7e (Line 7e reading)');
equal(we.payor, 'B', 'worked example payor is Parent B (the $201,000 earner)');

// box=1 (2026-09-08): this worked example is Box 1 (equal parenting time). credits DEFAULT
// FLIPPED TO FALSE 2026-09-09 (Task 3, private repo's simplify-to-withholding-basis plan): no
// explicit countRefundableCredits argument below, so this now reproduces net_position.py's
// analyze()'s new PUBLISHED default -- the withholding basis, no refundable credits, box no
// longer matters (see PART 6b below for the credits-ON comparison at this same worked example,
// both custody boxes).
var pos = N.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, we['7d'], 0.0, 0.0, undefined, KIDS_UNDER_13, 1);

close(pos.support_pct_of_payor_net, 0.3766031600352484, 1e-9, 'worked example true % of net = 37.7% (credits off, v13 default flip)');
equal(pos.support_pct_of_payor_net.toFixed(3), '0.377', 'worked example true % of net rounds to 37.7%');
close(pos.payor_eff_rate, 0.3043109452736319, 1e-9, 'payor effective tax rate = +30.4% (credits off)');
close(pos.recip_eff_rate, 0.16552834008097173, 1e-9, 'recipient effective tax rate = +16.6% (credits off, no longer negative -- no refundable credits)');
close(pos.payor_after, 87171.76202121109, 1e-4, 'payor keeps $87,172/yr (credits off)');
close(pos.recip_after, 77395.4779787889, 1e-4, 'recipient household holds $77,395/yr -- payor ahead (credits off, SIGN CHANGE from the pre-v13 credits-ON default)');
equal(Math.round(pos.payor_eff_rate * 1000) / 1000, 0.304, 'payor effective rate rounds to 30.4% (credits off)');

// ---------------------------------------------------------------------------------------------
// PART 3 -- the calculator.js compute() function itself, end to end, at the worked example.
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 3: calculator.js compute() at the worked example ===\n');

// calculator.js guards `typeof window === 'undefined'` before wiring up the DOM, so it is safe
// to require in Node -- but it reads window.MCSGWorksheet / window.MCSGNetPosition, which only
// exist in a browser. Reproduce its compute() logic directly here against the two libs, which is
// the same arithmetic calculator.js runs (see assets/js/calculator.js's own `compute()`).
function compute(higherAnnual, lowerAnnual, facts) {
  var lowerWk = lowerAnnual / 52.0, higherWk = higherAnnual / 52.0;
  var r = W.run(facts.box, lowerWk, higherWk, facts.kids, 0, { aHealth: facts.healthLow, bHealth: facts.healthHigh });
  var payorGross = r.payor === 'A' ? lowerAnnual : higherAnnual;
  var recipGross = r.payor === 'A' ? higherAnnual : lowerAnnual;
  // box=facts.box (2026-09-08): who claims the children for tax purposes now follows the
  // selected custody box -- see assets/js/lib/net-position.js's householdNetIncomes().
  var p = N.analyze(payorGross, recipGross, facts.kids, r['7d'], 0.0, 0.0, undefined, 0, facts.box);
  return {
    order_wk: r['7d'], line_7e: r['7e'], true_pct_net: p.support_pct_of_payor_net,
    payor_after: p.payor_after, recip_after: p.recip_after, recip_per_person: p.recip_per_person
  };
}

var FACTS = { kids: 3, box: 1, healthLow: 33.0, healthHigh: 43.0 };
var calcResult = compute(201000, 29640, FACTS);
equal(Math.round(calcResult.order_wk), 1013, 'calculator.js compute(): weekly order rounds to $1,013');
equal(calcResult.line_7e.toFixed(3), '0.265', 'calculator.js compute(): Line 7e rounds to 26.5%');
// The calculator passes kids_under_13=0 (matching model/charts/_common.py's generic-grid
// convention -- MCSGCalculatorFacts has no slider for how many children are under 13, since the
// brief specifies only two income inputs). kids_under_13 changes ONLY the recipient's refundable MA
// Child and Family Tax Credit -- under the corrected Box 1 fix (v12, private commit 723a7bf), the
// payor's claiming year is payorNetClaimsCtc(), which takes no kids_under_13 argument at all, so
// his net income (and therefore support_pct_of_payor_net = annual_support / payor_net) is IDENTICAL
// regardless of kids_under_13. DEFAULT FLIPPED TO FALSE 2026-09-09 (Task 3): compute() passes no
// explicit countRefundableCredits argument, so this now reproduces the credits-off published
// default, and kids_under_13 stops mattering for a second, stronger reason -- credits are off
// entirely, so neither box nor kids_under_13 has anything left to change.
equal(calcResult.true_pct_net.toFixed(3), '0.377', 'calculator.js compute(): true % of net rounds to 37.7% (credits off)');

// The mounted page's own static markup (index.html, MARKUP CONTRACT in calculator.js) hardcodes
// the sliders' default values and the data-calc-cell spans' starting text as the no-JS fallback.
// Check the formatted strings a reader actually sees match those exact defaults.
function moneyWk(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/wk'; }
function money(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/yr'; }
function pct1(v) { return (v * 100).toFixed(1) + '%'; }
// NOTE (2026-09-09, v13 default flip, Task 3): index.html's static no-JS fallback markup was
// ALREADY stale at the v12 credits-ON correction ($92,453/$85,168/36.3%/$21,292) and is now
// doubly stale under the credits-off default computed below. That markup is page prose, out of
// scope for this port fix -- flagged in this task's report, not fixed here. The values below are
// what the live, JS-computed readout now shows, which is what this test checks.
equal(moneyWk(calcResult.order_wk), '$1,013/wk', 'mounted defaults: formatted weekly order matches the markup\'s static $1,013/wk');
equal(pct1(calcResult.line_7e), '26.5%', 'mounted defaults: formatted Line 7e matches the markup\'s static 26.5%');
equal(pct1(calcResult.true_pct_net), '37.7%', 'mounted defaults: formatted true share of net = 37.7% (credits off; markup\'s static fallback is stale)');
equal(money(calcResult.payor_after), '$87,172/yr', 'mounted defaults: formatted payor-keeps = $87,172/yr (credits off; markup\'s static fallback is stale)');
equal(money(calcResult.recip_after), '$77,395/yr', 'mounted defaults: formatted recipient-household-holds = $77,395/yr (credits off; markup\'s static fallback is stale)');
equal(money(calcResult.recip_per_person), '$19,349/yr', 'mounted defaults: formatted recipient per-person = $19,349/yr (credits off; markup\'s static fallback is stale)');
equal(calcResult.recip_after > calcResult.payor_after, false,
  'mounted defaults: payor keeps more than the recipient household under the credits-off default (v13), so the is-warning class and "Above the payor" note should be OFF by default');
equal(calcResult.true_pct_net > 0.40, false,
  'mounted defaults: true share of net (37.7%) is below 40%, so the is-warning class is correctly OFF by default');

// ---------------------------------------------------------------------------------------------
// PART 4 -- the sanity guard (calculator.js's sanityCheckPasses()) fires on a broken constant and
// clears once the constant is restored. calculator.js itself only runs this in a browser (it
// early-returns when `window` is undefined), so this reproduces its exact check --
// Math.round(order_wk) === 1013 at the worked example -- against the same compute() logic used
// above, which is what PART 3 already established is faithful to calculator.js's own compute().
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 4: sanity guard fires on a broken constant, clears once restored ===\n');

var BROKEN_FACTS = { kids: 2, box: 1, healthLow: 33.0, healthHigh: 43.0 }; // kids 3 -> 2, temporarily
var brokenResult = compute(201000, 29640, BROKEN_FACTS);
var brokenGuardPasses = Math.round(brokenResult.order_wk) === 1013;
equal(brokenGuardPasses, false,
  'sanity guard: breaking kids from 3 to 2 makes the worked example diverge from $1,013 (guard would show "calculator unavailable")');

// Restore: the real FACTS (kids=3, matching MCSGCalculatorFacts in calculator.js) must reproduce
// $1,013 again -- proving the guard's own condition passes once the break is undone.
var restoredResult = compute(201000, 29640, FACTS);
var restoredGuardPasses = Math.round(restoredResult.order_wk) === 1013;
equal(restoredGuardPasses, true,
  'sanity guard: restoring kids=3 makes the worked example match $1,013 again (guard would pass, numbers render)');

// ---------------------------------------------------------------------------------------------
// PART 5 -- CORRECTNESS GATE: the full v2 fixture grid (children 1/2/3 x box 1/2 x six income
// pairs, generated straight from model/worksheet.py and model/net_position.py in the private
// repo -- see /tmp/gen_calc_v2_fixtures.py's own header for the exact command). Every cell the v2
// calculator can show must reproduce that Python output; the fixture's own "disabled" list (any
// combination the Python could not compute) must be empty, or those combinations must be
// disabled in the UI rather than shown with an unverified number.
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 5: v2 fixture grid (children x custody x six income pairs) against the Python ===\n');

var fixtures = require(path.join(__dirname, 'fixtures', 'calculator-v2.json'));

equal(fixtures.disabled.length, 0,
  'fixture grid: zero combinations were disabled by the Python (none too degenerate to compute)');
equal(fixtures.rows.length, 36,
  'fixture grid: 36 rows (3 children x 2 custody boxes x 6 income pairs)');

fixtures.rows.forEach(function (row) {
  var facts = { kids: row.kids, box: row.box, healthLow: 33.0, healthHigh: 43.0 };
  var got = compute(row.higher, row.lower, facts);
  var label = 'kids=' + row.kids + ' box=' + row.box + ' higher=' + row.higher + ' lower=' + row.lower;

  // "To the dollar": tolerance well under half a cent, so any dollar rounding downstream (the
  // moneyWk()/money() formatters) is guaranteed to land on the same integer dollar the fixture's
  // own Python run produced.
  close(got.order_wk, row.order_wk, 1e-6, label + ': order_wk (7d) matches Python to the dollar');
  close(got.payor_after, row.payor_after, 1e-4, label + ': payor_after matches Python to the dollar');
  close(got.recip_after, row.recip_after, 1e-4, label + ': recip_after matches Python to the dollar');
  close(got.recip_per_person, row.recip_per_person, 1e-4, label + ': recip_per_person matches Python to the dollar');

  // "To 0.001 on ratios": Line 7e and the true share of net are both fractions of 1.0; 0.001 is
  // 0.1 percentage point, tighter than the UI's own one-decimal pct1() display.
  close(got.line_7e, row.line_7e, 0.001, label + ': line_7e matches Python to 0.001');
  close(got.true_pct_net, row.true_pct_net, 0.001, label + ': true_pct_net matches Python to 0.001');

  // The is-warning thresholds calculator.js applies must agree with the fixture's own numbers --
  // this is what proves the UI would show the right colour/label on every one of the 36 cells,
  // not just the six-scenario/worked-example checks in PARTS 1-3.
  equal(got.true_pct_net > 0.40, row.true_pct_net > 0.40,
    label + ': true_pct_net > 40% threshold agrees with the fixture (drives the is-warning class)');
  equal(got.recip_after > got.payor_after, row.recip_after > row.payor_after,
    label + ': recip_after > payor_after agrees with the fixture (drives the household is-warning class)');
});

// ---------------------------------------------------------------------------------------------
// PART 6 -- CORRECTNESS GATE for the v4 interface (2026-09-07: tabs, two premium number inputs,
// two child-care sliders): the full fixture grid (children 1/2/3 x custody box 1/2 x premiums
// {(33,43),(40,40)} x child care {(0,0),(300,0),(300,300)} x six income pairs = 216 rows, plus 3
// hand-picked extra rows at the worked-example incomes -- 219 total, generated straight from this
// repo's own model/worksheet.py and model/net_position.py by
// tools/gen_calculator_childcare_fixtures.py. Every combination the interface can reach must
// reproduce that Python output; the fixture's own "disabled" list must be empty, or those
// combinations must be disabled in the UI rather than shown with an unverified number.
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 6: v4 fixture grid (children x custody x premiums x child care x six income pairs) ===\n');

// Reproduces calculator.js's own spreadCC()/computeWithFacts() exactly (see that file's v4 header
// comment) -- calculator.js itself is not required() here because it early-returns when `window`
// is undefined (see PART 3's comment for why the same approach is used there).
function spreadCC(total, kids) {
  if (!total) return [];
  var per = total / kids;
  var out = [];
  for (var i = 0; i < kids; i++) out.push(per);
  return out;
}

function computeV4(higherAnnual, lowerAnnual, facts) {
  var lowerWk = lowerAnnual / 52.0, higherWk = higherAnnual / 52.0;
  var aCc = spreadCC(facts.ccLower || 0, facts.kids);
  var bCc = spreadCC(facts.ccHigher || 0, facts.kids);
  var r = W.run(facts.box, lowerWk, higherWk, facts.kids, 0, {
    aHealth: facts.healthLow, bHealth: facts.healthHigh, aChildcare: aCc, bChildcare: bCc
  });
  var payorGross = r.payor === 'A' ? lowerAnnual : higherAnnual;
  var recipGross = r.payor === 'A' ? higherAnnual : lowerAnnual;
  var aOwnCc = aCc.reduce(function (s, v) { return s + v; }, 0);
  var bOwnCc = bCc.reduce(function (s, v) { return s + v; }, 0);
  var weeklyChildcare = aOwnCc + bOwnCc;
  var payorOwnCc = r.payor === 'A' ? aOwnCc : bOwnCc;
  var payorChildcareShare = weeklyChildcare > 0 ? payorOwnCc / weeklyChildcare : 0.0;
  // credits (v11, 2026-09-08; DEFAULT FLIPPED TO FALSE 2026-09-09, Task 3). Defaults to false
  // when facts.credits is undefined, matching calculator.js's own computeWithFacts() default
  // rule and net_position.py's analyze().
  var countCredits = facts.credits === undefined ? false : facts.credits;
  var p = N.analyze(payorGross, recipGross, facts.kids, r['7d'], weeklyChildcare, payorChildcareShare, undefined, 0, facts.box, countCredits);
  // Always compute the credits-off figures too, independent of facts.credits, so a single call
  // to computeV4 can check both the ON and OFF fixture columns without a second call.
  var pNoCredits = N.analyze(payorGross, recipGross, facts.kids, r['7d'], weeklyChildcare, payorChildcareShare, undefined, 0, facts.box, false);
  var higherShareOfLowerWk = r.A_6b;
  var higherShareOfLowerPct = r.A_6a ? r.A_6b / r.A_6a : 0.0;
  var higherBearsWk = bOwnCc - r.B_6b + r.A_6b;
  var higherBearsPct = weeklyChildcare > 0 ? higherBearsWk / weeklyChildcare : 0.0;
  return {
    order_wk: r['7d'], line_7e: r['7e'], true_pct_net: p.burden_pct_of_payor_net,
    payor_after: p.payor_after, recip_after: p.recip_after, recip_per_person: p.recip_per_person,
    true_pct_net_no_credits: pNoCredits.burden_pct_of_payor_net,
    payor_after_no_credits: pNoCredits.payor_after, recip_after_no_credits: pNoCredits.recip_after,
    recip_per_person_no_credits: pNoCredits.recip_per_person,
    combined_wk: weeklyChildcare,
    higher_share_of_lower_wk: higherShareOfLowerWk, higher_share_of_lower_pct: higherShareOfLowerPct,
    higher_bears_wk: higherBearsWk, higher_bears_pct: higherBearsPct
  };
}

var ccFixtures = require(path.join(__dirname, 'fixtures', 'calculator-childcare.json'));

equal(ccFixtures.disabled.length, 0,
  'v4 fixture grid: zero combinations were disabled by the Python');
equal(ccFixtures.rows.length, 219,
  'v4 fixture grid: 219 rows (3 children x 2 custody boxes x 2 premium pairs x 3 child-care pairs x 6 income pairs, plus 3 extra)');

ccFixtures.rows.forEach(function (row) {
  var facts = {
    kids: row.kids, box: row.box, healthLow: row.health_lo, healthHigh: row.health_hi,
    ccLower: row.cc_lower, ccHigher: row.cc_higher
  };
  var got = computeV4(row.higher, row.lower, facts);
  var label = 'kids=' + row.kids + ' box=' + row.box + ' health=' + row.health_lo + '/' + row.health_hi +
    ' cc=' + row.cc_lower + '/' + row.cc_higher + ' higher=' + row.higher + ' lower=' + row.lower;

  close(got.order_wk, row.order_wk, 1e-6, label + ': order_wk (7d) matches Python to the dollar');
  close(got.payor_after, row.payor_after, 1e-4, label + ': payor_after matches Python to the dollar');
  close(got.recip_after, row.recip_after, 1e-4, label + ': recip_after matches Python to the dollar');
  close(got.recip_per_person, row.recip_per_person, 1e-4, label + ': recip_per_person matches Python to the dollar');
  close(got.line_7e, row.line_7e, 0.001, label + ': line_7e matches Python to 0.001');
  close(got.true_pct_net, row.true_pct_net, 0.001, label + ': true_pct_net matches Python to 0.001');
  close(got.higher_share_of_lower_wk, row.higher_share_of_lower_wk, 1e-4, label + ': higher_share_of_lower_wk (Line A_6b) matches Python');
  close(got.higher_share_of_lower_pct, row.higher_share_of_lower_pct, 1e-6, label + ': higher_share_of_lower_pct matches Python');
  close(got.higher_bears_wk, row.higher_bears_wk, 1e-4, label + ': higher_bears_wk matches Python');
  close(got.higher_bears_pct, row.higher_bears_pct, 1e-6, label + ': higher_bears_pct matches Python');

  // The credits-off switch (added 2026-09-08): every row's count_refundable_credits=False figures,
  // independent of which mode facts.credits selects -- see computeV4's own comment above.
  close(got.payor_after_no_credits, row.payor_after_no_credits, 1e-4, label + ': payor_after_no_credits matches Python to the dollar');
  close(got.recip_after_no_credits, row.recip_after_no_credits, 1e-4, label + ': recip_after_no_credits matches Python to the dollar');
  close(got.recip_per_person_no_credits, row.recip_per_person_no_credits, 1e-4, label + ': recip_per_person_no_credits matches Python to the dollar');
  close(got.true_pct_net_no_credits, row.true_pct_net_no_credits, 0.001, label + ': true_pct_net_no_credits matches Python to 0.001');

  equal(got.true_pct_net >= 0.40, row.true_pct_net >= 0.40,
    label + ': true_pct_net >= 40% threshold agrees with the fixture (drives the hardship badge)');
  equal(got.recip_after > got.payor_after, row.recip_after > row.payor_after,
    label + ': recip_after > payor_after agrees with the fixture (drives the household badge)');
});

// The sanity guard's two fixed targets (calculator.js's SANITY_NO_CC / SANITY_CC, independent of
// any UI state): $33/$43 premiums, kids=3, box=1, worked-example incomes, $0 and then $300/wk
// (lower earner only) child care.
var sanityNoCc = computeV4(201000, 29640, { kids: 3, box: 1, healthLow: 33.0, healthHigh: 43.0, ccLower: 0, ccHigher: 0 });
equal(Math.round(sanityNoCc.order_wk), 1013, 'sanity guard target 1: $33/$43, no child care, rounds to $1,013/wk');
var sanityCc = computeV4(201000, 29640, { kids: 3, box: 1, healthLow: 33.0, healthHigh: 43.0, ccLower: 300, ccHigher: 0 });
equal(Math.round(sanityCc.order_wk), 1276, 'sanity guard target 2: $33/$43, $300/wk lower-earner child care, rounds to $1,276/wk');
equal(pct1(sanityCc.line_7e), '33.4%', 'sanity guard target 2: Line 7e rounds to 33.4%');
equal(pct1(sanityCc.true_pct_net), '47.4%', 'sanity guard target 2: true share of net rounds to 47.4% (v13 default flip, Task 3: credits off; was 46.4% credits-on default)');

// ---------------------------------------------------------------------------------------------
// PART 6b -- THE CREDITS-OFF SWITCH (added 2026-09-08), tested directly against N.analyze() at a
// FIXED weekly support ($1,012.73, the worked example's Box 1 order) -- mirroring
// model/test_net_position.py's own methodology exactly, so this checks net-position.js's tax
// treatment in isolation from worksheet.js's box-dependent order (Box 2's own order is a
// different figure; that is a worksheet fact, not a tax-model fact, and is checked separately by
// PART 6's fixture rows). The four-combination table is the one model/test_net_position.py pins.
// Reproduces model/net_position.py exactly (v12 correction, 2026-09-08, private commit 723a7bf):
// box=2/credits-on and box=1/credits-on BOTH have the recipient household ahead of the payor --
// narrowly (+$1,065) at box=1, by a wider margin (+$6,650) at box=2. credits-off has the payor
// ahead in both boxes.
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 6b: the credits-off switch, worked example, both custody boxes, fixed order ===\n');

var WE_PAYOR_GROSS = 201000.0, WE_RECIP_GROSS = 570.0 * 52.0, WE_SUPPORT_WK = 1012.73;
var box1CreditsOn = N.analyze(WE_PAYOR_GROSS, WE_RECIP_GROSS, 3, WE_SUPPORT_WK, 0.0, 0.0, undefined, 2, 1, true);
var box1CreditsOff = N.analyze(WE_PAYOR_GROSS, WE_RECIP_GROSS, 3, WE_SUPPORT_WK, 0.0, 0.0, undefined, 2, 1, false);
var box2CreditsOn = N.analyze(WE_PAYOR_GROSS, WE_RECIP_GROSS, 3, WE_SUPPORT_WK, 0.0, 0.0, undefined, 2, 2, true);
var box2CreditsOff = N.analyze(WE_PAYOR_GROSS, WE_RECIP_GROSS, 3, WE_SUPPORT_WK, 0.0, 0.0, undefined, 2, 2, false);

equal(Math.round(box1CreditsOn.payor_after), 90447, 'box=1, credits ON: payor keeps $90,447 (v12 correction)');
equal(Math.round(box1CreditsOn.recip_after), 91512, 'box=1, credits ON: recipient household holds $91,512 -- narrowly ahead (v12 correction)');
equal(Math.round(box2CreditsOn.payor_after), 87172, 'box=2, credits ON: payor keeps $87,172');
equal(Math.round(box2CreditsOn.recip_after), 93822, 'box=2, credits ON: recipient household holds $93,822 -- RECIPIENT AHEAD');
equal(Math.round(box1CreditsOff.payor_after), 87172, 'box=1, credits OFF: payor keeps $87,172');
equal(Math.round(box1CreditsOff.recip_after), 77396, 'box=1, credits OFF: recipient household holds $77,396 -- payor ahead');
equal(Math.round(box2CreditsOff.payor_after), 87172, 'box=2, credits OFF: payor keeps $87,172');
equal(Math.round(box2CreditsOff.recip_after), 77396, 'box=2, credits OFF: recipient household holds $77,396 -- payor ahead (SIGN CHANGE from box=2 credits-ON, same box)');
equal(box1CreditsOff.payor_after, box2CreditsOff.payor_after, 'credits OFF: box has no effect on payor_after (box only matters through credits)');
equal(box1CreditsOff.recip_after, box2CreditsOff.recip_after, 'credits OFF: box has no effect on recip_after');
close(N.netIncomeWithholdingBasis(WE_PAYOR_GROSS), 139833.50, 1e-2, 'credits OFF: netIncomeWithholdingBasis(payor gross) reproduces the pinned $139,833.50');
close(N.netIncomeWithholdingBasis(WE_RECIP_GROSS), 24733.74, 1e-2, 'credits OFF: netIncomeWithholdingBasis(recipient gross) reproduces the pinned $24,733.74');

// ---------------------------------------------------------------------------------------------
// PART 7 -- a fixed $40/$40-premium scenario, three children, Box 1, worked-example incomes.
// NOTE: index.html's own inputs default to $43/$33 (commit 796e52f, 2026-09-07, "Calculator
// defaults to the site's own premiums"), not $40/$40 -- this part's "matches markup's static"
// wording predates that commit and was never updated; PART 3 above is the block that actually
// reproduces index.html's live defaults. PART 7 is kept as a second, fixed fidelity point (JS
// against the Python at a scenario distinct from PART 3/6), not a markup-matching check. Values
// below are recomputed for the 2026-09-08 box fix (see net-position.js's householdNetIncomes()).
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 7: a fixed $40/$40-premium scenario and status badges (not the live markup defaults -- see note above) ===\n');

var baseDefault = computeV4(201000, 29640, { kids: 3, box: 1, healthLow: 40.0, healthHigh: 40.0, ccLower: 0, ccHigher: 0 });
equal(moneyWk(baseDefault.order_wk), '$1,015/wk', 'Base support tab default: order = $1,015/wk');
equal(pct1(baseDefault.line_7e), '26.5%', 'Base support tab default: Line 7e = 26.5%');
equal(pct1(baseDefault.true_pct_net), '37.8%', 'Base support tab default: true share of net = 37.8% (v13 default flip, Task 3: credits off; was 36.9% credits-on default)');
equal(money(baseDefault.payor_after), '$87,043/yr', 'Base support tab default: payor keeps $87,043/yr (v13 default flip: credits off; was $90,318/yr credits-on default)');
equal(money(baseDefault.recip_after), '$77,524/yr', 'Base support tab default: recipient household holds $77,524/yr (v13 default flip: credits off; was $90,760/yr credits-on default)');
equal(money(baseDefault.recip_per_person), '$19,381/yr', 'Base support tab default: recipient per person $19,381/yr (v13 default flip: credits off; was $22,690/yr credits-on default)');
equal(baseDefault.recip_after > baseDefault.payor_after, false,
  'Base support tab default: household badge is OFF (v13 default flip: credits off, payor now ahead)');
equal(baseDefault.true_pct_net >= 0.40, false,
  'Base support tab default: hardship badge is muted (37.8% is below 40%)');

var ccDefault = computeV4(201000, 29640, { kids: 3, box: 1, healthLow: 40.0, healthHigh: 40.0, ccLower: 100.0, ccHigher: 0.0 });
equal(moneyWk(ccDefault.order_wk), '$1,103/wk', 'Child care tab default: order = $1,103/wk');
equal(Math.round(ccDefault.order_wk - baseDefault.order_wk), 88,
  'Child care tab default: change from no child care rounds to +$88/wk (unaffected by the box fix -- worksheet-only)');
equal(pct1(ccDefault.higher_share_of_lower_pct), '87.8%',
  'Child care tab default: higher earner\'s share of the lower earner\'s child care = 87.8% (unaffected -- worksheet-only)');
equal(money(ccDefault.higher_share_of_lower_wk * 52), '$4,567/yr',
  'Child care tab default: same share, per year, = $4,567/yr (unaffected -- worksheet-only)');
equal(money(ccDefault.payor_after), '$82,476/yr', 'Child care tab default: payor keeps $82,476/yr (v13 default flip: credits off; was $85,751/yr credits-on default)');
equal(money(ccDefault.recip_after), '$76,891/yr', 'Child care tab default: recipient household holds $76,891/yr (v13 default flip: credits off; was $90,127/yr credits-on default)');
equal(money(ccDefault.recip_per_person), '$19,223/yr', 'Child care tab default: recipient per person $19,223/yr (v13 default flip: credits off; was $22,532/yr credits-on default)');
equal(ccDefault.recip_after > ccDefault.payor_after, false,
  'Child care tab default: household badge is OFF (v13 default flip: credits off, payor now ahead)');
equal(ccDefault.true_pct_net >= 0.40, true,
  'Child care tab default: hardship badge is LIT (41.0% is at/above 40%, v13 default flip: credits off; was 40.1% credits-on default)');
equal(pct1(ccDefault.true_pct_net), '41.0%', 'Child care tab default: true share of net (shown in the badge text) is 41.0% (v13 default flip: credits off; was 40.1% credits-on default)');

// The combined-child-care line (calculator.js's cc_combined_line) only fires in the DOM when BOTH
// sliders are above zero -- at the default (higher earner's slider is $0), calculator.js's own
// render() leaves it empty. That branch is DOM-only (it never reaches computeV4's return value),
// so it is checked in the browser pass, not here; the fixture default above (ccHigher: 0.0)
// documents the condition this test suite cannot itself exercise.

// With both parents paying $300/wk (the old v3 sanity targets, now reachable via both sliders):
// order $1,276/wk / Line 7e 33.4% / true share of net 47.4% when only the lower earner pays, and
// true share of net crossing 55% once both pay and the payor's own child care is counted.
var weBothPay = computeV4(201000, 29640, { kids: 3, box: 1, healthLow: 33.0, healthHigh: 43.0, ccLower: 300, ccHigher: 300 });
equal(weBothPay.true_pct_net > 0.55, true,
  'worked example, both pay $300/wk each: true share of net exceeds 55% once the payor\'s own child care is counted');
equal(weBothPay.combined_wk, 600, 'worked example, both pay $300/wk each: combined weekly child care is $600');

// ---------------------------------------------------------------------------------------------
// PART 8 -- Child care tab v5 (2026-09-07): the always-visible distribution readout (Change 1)
// and the "apply the proposed fix" toggle (Change 2), both ported from
// model/childcare_post_transfer.py. Reproduces calculator.js's own computeChildcareDistribution()/
// computeFixedRuleOrder() exactly (see that file's v5 header comment) -- calculator.js itself is
// not required() here for the same reason PART 3/6 give.
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 8: Child care tab distribution readout + proposed-fix toggle defaults ===\n');

function pct0(v) { return Math.round(v * 100) + '%'; }
function moneyBare(v) { return '$' + Math.round(v).toLocaleString('en-US'); }

function computeDistribution(higherAnnual, lowerAnnual, facts) {
  var lowerWk = lowerAnnual / 52.0, higherWk = higherAnnual / 52.0;
  var r0 = W.run(facts.box, lowerWk, higherWk, facts.kids, 0, { aHealth: facts.healthLow, bHealth: facts.healthHigh });
  var baseOrderWk = r0['7d'];
  var combinedGross = higherAnnual + lowerAnnual;
  var grossShare = combinedGross ? (higherAnnual - baseOrderWk * 52) / combinedGross : 0.0;
  // kids_under_13 = 0, the same convention as every other figure this calculator computes (2026-09-07
  // afternoon: dropped the earlier min(2, kids) exception -- see calculator.js's v7 header comment).
  // box=facts.box (2026-09-08): this analytical net_share now follows the selected custody box too.
  // countRefundableCredits=true EXPLICIT (2026-09-09, Task 3): net_share/dist_net_share is the
  // credits-included ANALYSIS figure (matches childcare_post_transfer.py's rule 3 and the fixture
  // generator's distribution()), not the withholding-basis ask -- N.analyze()'s own default
  // became false this same task, so this call must say so explicitly or dist_net_share would
  // silently collapse onto dist_net_withholding_share.
  var pos = N.analyze(higherAnnual, lowerAnnual, facts.kids, baseOrderWk, 0.0, 0.0, undefined, 0, facts.box, true);
  // v9: the withholding-basis post-transfer share (tax and FICA only, no refundable credits) --
  // childcare_post_transfer.py's rule5, the basis Section 2 asks for as of v4.9.
  var pw = N.netIncomeWithholdingBasis(higherAnnual);
  var rw = N.netIncomeWithholdingBasis(lowerAnnual);
  var aw = pw - baseOrderWk * 52, bw = rw + baseOrderWk * 52;
  var netWithholdingShare = (aw + bw) ? aw / (aw + bw) : 0.0;
  return {
    base_order_wk: baseOrderWk, share3c: r0.B_3c, gross_share: grossShare, net_share: pos.payor_after_share,
    net_withholding_share: netWithholdingShare
  };
}

// CHANGE 3 (v7, mechanism fixed v9): "on money after tax", the recommended rule. net_rule_share is
// computeDistribution()'s own net_withholding_share (childcare_post_transfer.py's rule5). The
// order MOVES: base order plus that share of the combined child care, because the letter's Line
// 6b-1 redline sits inside the Worksheet's own 6b -> 6c -> 6e -> 6g -> 7b -> 7d chain, the same
// linear step computeFixedRule already uses.
function computeNetRule(higherAnnual, lowerAnnual, facts, totalChildcareWk) {
  var d = computeDistribution(higherAnnual, lowerAnnual, facts);
  var share = d.net_withholding_share;
  return {
    base_order_wk: d.base_order_wk,
    net_rule_share: share,
    net_rule_order_wk: d.base_order_wk + share * totalChildcareWk,
    net_rule_charge_wk: share * totalChildcareWk
  };
}

function computeFixedRule(higherAnnual, lowerAnnual, facts) {
  var lowerWk = lowerAnnual / 52.0, higherWk = higherAnnual / 52.0;
  var r0 = W.run(facts.box, lowerWk, higherWk, facts.kids, 0, { aHealth: facts.healthLow, bHealth: facts.healthHigh });
  var baseOrderWk = r0['7d'];
  var payorThreeA = r0.payor === 'A' ? r0.A_3a : r0.B_3a;
  var combinedThreeB = r0['3b'];
  var share = combinedThreeB ? (payorThreeA - baseOrderWk) / combinedThreeB : 0.0;
  var totalChildcare = (facts.ccLower || 0) + (facts.ccHigher || 0);
  return { base_order_wk: baseOrderWk, fixed_rule_share: share, fixed_rule_order_wk: baseOrderWk + share * totalChildcare };
}

// Fixed $40/$40-premium scenario (see the PART 7 note above -- not the live markup defaults),
// three children, Box 1, worked-example incomes, Child care tab's own default $100/wk from the
// lower earner.
var distDefault = computeDistribution(201000, 29640, { kids: 3, box: 1, healthLow: 40.0, healthHigh: 40.0 });
equal(pct1(distDefault.share3c), '87.8%',
  'Child care tab default: higher earner\'s share of child care (Line 3c) = 87.8% (unaffected -- worksheet-only)');
equal(pct0(distDefault.gross_share), '64%',
  'Child care tab default: post-transfer gross share = 64% (unaffected -- worksheet-only)');
equal(pct0(distDefault.net_share), '50%',
  'Child care tab default: post-transfer net share = 50% (v12 correction, private commit 723a7bf; was 48% pre-box-fix, 52% under the first, superseded Box 1 fix)');

var fixDefault = computeFixedRule(201000, 29640, { kids: 3, box: 1, healthLow: 40.0, healthHigh: 40.0, ccLower: 100.0, ccHigher: 0.0 });
equal(moneyWk(fixDefault.fixed_rule_order_wk), '$1,080/wk',
  'Child care tab default: proposed-fix order matches markup\'s static $1,080/wk');
equal(moneyBare(ccDefault.order_wk), '$1,103',
  'Child care tab default: "was" figure matches the current order\'s markup static $1,103');

// ---------------------------------------------------------------------------------------------
// PART 9 -- CORRECTNESS GATE for Change 1/2: the same 219-row v4 fixture grid, checked against the
// dist_share3c/dist_gross_share/dist_net_share/fixed_rule_share/fixed_rule_order_wk fields
// tools/gen_calculator_childcare_fixtures.py now emits (2026-09-07 addition; see that script's
// distribution()/fixed_rule() for what produces them).
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 9: v5 fixture grid -- distribution readout + proposed-fix toggle ===\n');

ccFixtures.rows.forEach(function (row) {
  var label = 'kids=' + row.kids + ' box=' + row.box + ' health=' + row.health_lo + '/' + row.health_hi +
    ' cc=' + row.cc_lower + '/' + row.cc_higher + ' higher=' + row.higher + ' lower=' + row.lower;

  var gotDist = computeDistribution(row.higher, row.lower, { kids: row.kids, box: row.box, healthLow: row.health_lo, healthHigh: row.health_hi });
  close(gotDist.share3c, row.dist_share3c, 1e-6, label + ': dist_share3c (Line 3c) matches Python');
  close(gotDist.gross_share, row.dist_gross_share, 1e-6, label + ': dist_gross_share matches Python');
  close(gotDist.net_share, row.dist_net_share, 1e-6, label + ': dist_net_share matches Python');
  close(gotDist.net_withholding_share, row.dist_net_withholding_share, 1e-6, label + ': dist_net_withholding_share matches Python');

  var gotFix = computeFixedRule(row.higher, row.lower, {
    kids: row.kids, box: row.box, healthLow: row.health_lo, healthHigh: row.health_hi,
    ccLower: row.cc_lower, ccHigher: row.cc_higher
  });
  close(gotFix.fixed_rule_share, row.fixed_rule_share, 1e-6, label + ': fixed_rule_share matches Python');
  close(gotFix.fixed_rule_order_wk, row.fixed_rule_order_wk, 1e-4, label + ': fixed_rule_order_wk matches Python to the dollar');

  var totalCc = row.cc_lower + row.cc_higher;
  var gotNet = computeNetRule(row.higher, row.lower,
    { kids: row.kids, box: row.box, healthLow: row.health_lo, healthHigh: row.health_hi }, totalCc);
  close(gotNet.net_rule_share, row.net_rule_share, 1e-6, label + ': net_rule_share matches Python');
  close(gotNet.net_rule_order_wk, row.net_rule_order_wk, 1e-4, label + ': net_rule_order_wk matches Python (base order plus the withholding share of child care)');
  close(gotNet.net_rule_charge_wk, row.net_rule_charge_wk, 1e-4, label + ': net_rule_charge_wk matches Python to the dollar');
});

// ---------------------------------------------------------------------------------------------
// PART 10 -- FIDELITY PIN: model/childcare_post_transfer.py's own worked example (PAYOR_GROSS
// $201,000, RECIP_WEEKLY $570/wk, three children, Box 1, health $33/$43, $300/wk lower-earner
// child care) must reproduce that script's rule1_share/rule2_gross_share/rule3_share (87.7% /
// 64.3% / 49.9% at kids_under_13=0, the site-wide convention -- the script itself prints a
// slightly different figure at its own KIDS_UNDER_13=2, a different, real-fact-pattern constant
// this calculator does not use; both reflect the SECOND, corrected 2026-09-08 box=1
// alternating-year credit fix (private commit 723a7bf: only the CTC/dependency claim alternates;
// head of household and the EITC stay with the physical-custodian recipient) -- replacing the
// pre-fix 48.4%/48.2% and the first, superseded fix's 52.1%/52.0%) and rule2b_share/rule2b_7d
// (64.5% / $1,206.08/wk, unaffected by the box fix -- gross-basis, no net_position call) to the
// value it actually prints -- run 2026-09-08 (see model/childcare_post_transfer.py's own
// docstring). This is also calculator.js's fixedRuleSanityPasses() target: worked example, $300
// lower-earner child care, fix on -> $1,206/wk. PART 10 also pins the "on money after tax" rule
// (netRuleSanityPasses() target, v9): share 53.0% on the withholding basis, order $1,172/wk --
// unaffected by the box fix (net_income_withholding_basis has no box parameter) -- the letter's
// Line 6b-1 redline changes the order, matching childcare_post_transfer.py's rule5.
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 10: childcare_post_transfer.py fidelity -- 87.7% / 64.3% / 49.9%, rule2b $1,206/wk ===\n');

var weDist = computeDistribution(PAYOR_GROSS, RECIP_GROSS, { kids: KIDS, box: 1, healthLow: 33.0, healthHigh: 43.0 });
close(weDist.share3c, 0.8768174760022585, 1e-9, 'worked example dist_share3c (rule1_share) = 87.7%');
close(weDist.gross_share, 0.6431593046358441, 1e-9, 'worked example dist_gross_share (rule2_gross_share) = 64.3%');
close(weDist.net_share, 0.4994902626331263, 1e-9, 'worked example dist_net_share (rule3_share, kids_under_13=0) = 49.9% (v12 correction; was 52.1% under the first, superseded fix)');
close(weDist.net_withholding_share, 0.5297030078478019, 1e-9, 'worked example dist_net_withholding_share (rule5_share) = 53.0%');
equal(pct1(weDist.share3c), '87.7%', 'worked example: formatted higher earner\'s share of child care = 87.7%');
equal(pct0(weDist.gross_share), '64%', 'worked example: formatted post-transfer gross share = 64%');
equal(pct0(weDist.net_share), '50%', 'worked example: formatted post-transfer net share = 50% (v12 correction; was 52%)');
equal(pct0(weDist.net_withholding_share), '53%', 'worked example: formatted post-transfer net withholding share = 53%');

var weFix = computeFixedRule(PAYOR_GROSS, RECIP_GROSS, { kids: KIDS, box: 1, healthLow: 33.0, healthHigh: 43.0, ccLower: 300.0, ccHigher: 0.0 });
close(weFix.fixed_rule_share, 0.6445081434447836, 1e-9, 'worked example fixed_rule_share (rule2b_share) = 64.5%');
close(weFix.fixed_rule_order_wk, 1206.0781733947601, 1e-6, 'worked example fixed_rule_order_wk (rule2b_7d) = $1,206.08/wk');
equal(Math.round(weFix.fixed_rule_order_wk), 1206,
  'worked example: "on income after the order" rule rounds to $1,206/wk (calculator.js\'s fixedRuleSanityPasses() target)');
equal(moneyWk(weFix.fixed_rule_order_wk), '$1,206/wk', 'worked example: formatted "on income after the order" order = $1,206/wk');
equal(moneyWk(sanityCc.order_wk), '$1,276/wk', 'worked example: formatted Worksheet order (the comparison figure) = $1,276/wk');

var weNet = computeNetRule(PAYOR_GROSS, RECIP_GROSS, { kids: KIDS, box: 1, healthLow: 33.0, healthHigh: 43.0 }, 300.0);
close(weNet.net_rule_share, 0.5297030078478019, 1e-9, 'worked example net_rule_share (rule5_share, withholding basis) = 53.0%');
close(weNet.net_rule_order_wk, 1171.6366327156657, 1e-6, 'worked example net_rule_order_wk (rule5_7d) = $1,171.64/wk');
close(weNet.net_rule_charge_wk, 158.91090235434058, 1e-6, 'worked example net_rule_charge_wk at $300/wk lower-earner child care = $158.91/wk');
equal(Math.round(weNet.net_rule_order_wk), 1172,
  'worked example: "on money after tax" rule order rounds to $1,172/wk, MOVING from the no-child-care order (calculator.js\'s netRuleSanityPasses() target)');
equal(moneyWk(weNet.net_rule_order_wk), '$1,172/wk', 'worked example: formatted "on money after tax" order = $1,172/wk');
equal(money(weNet.net_rule_charge_wk * 52), '$8,263/yr', 'worked example: formatted "on money after tax" annual charge at $300/wk = $8,263/yr');

console.log('\n' + checks + ' checks, ' + failures + ' failed.');
process.exit(failures ? 1 : 0);
