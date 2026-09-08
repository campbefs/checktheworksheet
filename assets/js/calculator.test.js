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

var pos = N.analyze(PAYOR_GROSS, RECIP_GROSS, KIDS, we['7d'], 0.0, 0.0, undefined, KIDS_UNDER_13);

close(pos.support_pct_of_payor_net, 0.3766031600352484, 1e-9, 'worked example true % of net = 37.7%');
equal(pos.support_pct_of_payor_net.toFixed(3), '0.377', 'worked example true % of net rounds to 37.7%');
close(pos.payor_eff_rate, 0.3043109452736319, 1e-9, 'payor effective tax rate = +30.4%');
close(pos.recip_eff_rate, -0.3886514379009409, 1e-9, 'recipient effective tax rate = -38.9%');
close(pos.payor_after, 87171.76202121109, 1e-4, 'payor keeps $87,172/yr');
close(pos.recip_after, 93821.3665981728, 1e-4, 'recipient household holds $93,821/yr');
equal(Math.round(pos.payor_eff_rate * 1000) / 1000, 0.304, 'payor effective rate rounds to 30.4%');

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
  var p = N.analyze(payorGross, recipGross, facts.kids, r['7d'], 0.0, 0.0, undefined, 0);
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
// brief specifies only two income inputs). kids_under_13 changes ONLY the RECIPIENT's refundable
// MA credit, which net_position.py's support_pct_of_payor_net never reads (it is
// annual_support / payor_net, and payor_net depends only on the payor's own gross) -- so this
// particular readout is identical either way, verified here rather than assumed. It DOES change
// payor_after/recip_after (the recipient's own refundable credits), which is why v2's "after tax"
// row runs slightly lower than the site's own worked-example figures elsewhere (kids_under_13=2
// there) -- see calculator.js's header comment and CONVENTIONS.md SS11.
equal(calcResult.true_pct_net.toFixed(3), '0.377', 'calculator.js compute(): true % of net rounds to 37.7%, same as the worked example');

// The mounted page's own static markup (index.html, MARKUP CONTRACT in calculator.js) hardcodes
// the sliders' default values and the data-calc-cell spans' starting text as the no-JS fallback.
// Check the formatted strings a reader actually sees match those exact defaults.
function moneyWk(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/wk'; }
function money(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/yr'; }
function pct1(v) { return (v * 100).toFixed(1) + '%'; }
equal(moneyWk(calcResult.order_wk), '$1,013/wk', 'mounted defaults: formatted weekly order matches the markup\'s static $1,013/wk');
equal(pct1(calcResult.line_7e), '26.5%', 'mounted defaults: formatted Line 7e matches the markup\'s static 26.5%');
equal(pct1(calcResult.true_pct_net), '37.7%', 'mounted defaults: formatted true share of net matches the markup\'s static 37.7%');
equal(money(calcResult.payor_after), '$87,172/yr', 'mounted defaults: formatted payor-keeps matches the markup\'s static $87,172/yr');
equal(money(calcResult.recip_after), '$92,941/yr', 'mounted defaults: formatted recipient-household-holds matches the markup\'s static $92,941/yr');
equal(money(calcResult.recip_per_person), '$23,235/yr', 'mounted defaults: formatted recipient per-person matches the markup\'s static $23,235/yr');
equal(calcResult.recip_after > calcResult.payor_after, true,
  'mounted defaults: recipient household exceeds payor keeps, so the is-warning class and "Above the payor" note are correctly on by default');
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
  var p = N.analyze(payorGross, recipGross, facts.kids, r['7d'], weeklyChildcare, payorChildcareShare, undefined, 0);
  var higherShareOfLowerWk = r.A_6b;
  var higherShareOfLowerPct = r.A_6a ? r.A_6b / r.A_6a : 0.0;
  var higherBearsWk = bOwnCc - r.B_6b + r.A_6b;
  var higherBearsPct = weeklyChildcare > 0 ? higherBearsWk / weeklyChildcare : 0.0;
  return {
    order_wk: r['7d'], line_7e: r['7e'], true_pct_net: p.burden_pct_of_payor_net,
    payor_after: p.payor_after, recip_after: p.recip_after, recip_per_person: p.recip_per_person,
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
equal(pct1(sanityCc.true_pct_net), '47.4%', 'sanity guard target 2: true share of net rounds to 47.4%');

// ---------------------------------------------------------------------------------------------
// PART 7 -- the interface's actual DEFAULTS (index.html's static no-JS fallback text): $40/$40
// premiums, three children, Box 1, worked-example incomes. Base support tab = $0/$0 child care;
// Child care tab defaults to $100/wk from the lower earner, $0 from the higher earner. Every
// number and every badge state below must match what a reader sees on first load, in both the
// markup's static text and calculator.js's own render() logic.
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 7: interface defaults ($40/$40 premiums) and status badges ===\n');

var baseDefault = computeV4(201000, 29640, { kids: 3, box: 1, healthLow: 40.0, healthHigh: 40.0, ccLower: 0, ccHigher: 0 });
equal(moneyWk(baseDefault.order_wk), '$1,015/wk', 'Base support tab default: order matches markup\'s static $1,015/wk');
equal(pct1(baseDefault.line_7e), '26.5%', 'Base support tab default: Line 7e matches markup\'s static 26.5%');
equal(pct1(baseDefault.true_pct_net), '37.8%', 'Base support tab default: true share of net matches markup\'s static 37.8%');
equal(money(baseDefault.payor_after), '$87,043/yr', 'Base support tab default: payor keeps matches markup\'s static $87,043/yr');
equal(money(baseDefault.recip_after), '$93,070/yr', 'Base support tab default: recipient household holds matches markup\'s static $93,070/yr');
equal(money(baseDefault.recip_per_person), '$23,267/yr', 'Base support tab default: recipient per person matches markup\'s static $23,267/yr');
equal(baseDefault.recip_after > baseDefault.payor_after, true,
  'Base support tab default: household badge is lit ("payee household ends up ahead")');
equal(baseDefault.true_pct_net >= 0.40, false,
  'Base support tab default: hardship badge is muted (37.8% is below 40%)');

var ccDefault = computeV4(201000, 29640, { kids: 3, box: 1, healthLow: 40.0, healthHigh: 40.0, ccLower: 100.0, ccHigher: 0.0 });
equal(moneyWk(ccDefault.order_wk), '$1,103/wk', 'Child care tab default: order matches markup\'s static $1,103/wk');
equal(Math.round(ccDefault.order_wk - baseDefault.order_wk), 88,
  'Child care tab default: change from no child care rounds to +$88/wk, matching the markup');
equal(pct1(ccDefault.higher_share_of_lower_pct), '87.8%',
  'Child care tab default: higher earner\'s share of the lower earner\'s child care matches markup\'s static 87.8%');
equal(money(ccDefault.higher_share_of_lower_wk * 52), '$4,567/yr',
  'Child care tab default: same share, per year, matches markup\'s static $4,567/yr');
equal(money(ccDefault.payor_after), '$82,476/yr', 'Child care tab default: payor keeps matches markup\'s static $82,476/yr');
equal(money(ccDefault.recip_after), '$92,437/yr', 'Child care tab default: recipient household holds matches markup\'s static $92,437/yr');
equal(money(ccDefault.recip_per_person), '$23,109/yr', 'Child care tab default: recipient per person matches markup\'s static $23,109/yr');
equal(ccDefault.recip_after > ccDefault.payor_after, true,
  'Child care tab default: household badge is lit ("payee household ends up ahead")');
equal(ccDefault.true_pct_net >= 0.40, true,
  'Child care tab default: hardship badge is LIT (41.0% is at or above 40%) -- the Child care tab\'s own default demonstrates the flag');
equal(pct1(ccDefault.true_pct_net), '41.0%', 'Child care tab default: true share of net (shown in the badge text) is 41.0%');

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
  var pos = N.analyze(higherAnnual, lowerAnnual, facts.kids, baseOrderWk, 0.0, 0.0, undefined, 0);
  return { base_order_wk: baseOrderWk, share3c: r0.B_3c, gross_share: grossShare, net_share: pos.payor_after_share };
}

// CHANGE 3 (v7): "on money after tax", the recommended rule. net_rule_share is exactly
// computeDistribution()'s own net_share (see calculator.js's computeNetRuleOrder for why the
// rule3/rule4 fixed point in childcare_post_transfer.py always reduces to the cc=0 share); the
// order stays at the no-child-care base, and the charge is that share applied to the row's
// combined weekly child care.
function computeNetRule(higherAnnual, lowerAnnual, facts, totalChildcareWk) {
  var d = computeDistribution(higherAnnual, lowerAnnual, facts);
  return {
    base_order_wk: d.base_order_wk,
    net_rule_share: d.net_share,
    net_rule_order_wk: d.base_order_wk,
    net_rule_charge_wk: d.net_share * totalChildcareWk
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

// Interface defaults: $40/$40 premiums, three children, Box 1, worked-example incomes, Child care
// tab's own default $100/wk from the lower earner. Must match index.html's static no-JS fallback.
var distDefault = computeDistribution(201000, 29640, { kids: 3, box: 1, healthLow: 40.0, healthHigh: 40.0 });
equal(pct1(distDefault.share3c), '87.8%',
  'Child care tab default: higher earner\'s share of child care (Line 3c) matches markup\'s static 87.8%');
equal(pct0(distDefault.gross_share), '64%',
  'Child care tab default: post-transfer gross share matches markup\'s static 64%');
equal(pct0(distDefault.net_share), '48%',
  'Child care tab default: post-transfer net share matches markup\'s static 48%');

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
  close(gotNet.net_rule_order_wk, row.net_rule_order_wk, 1e-4, label + ': net_rule_order_wk matches Python (stays at the no-child-care order)');
  close(gotNet.net_rule_charge_wk, row.net_rule_charge_wk, 1e-4, label + ': net_rule_charge_wk matches Python to the dollar');
});

// ---------------------------------------------------------------------------------------------
// PART 10 -- FIDELITY PIN: model/childcare_post_transfer.py's own worked example (PAYOR_GROSS
// $201,000, RECIP_WEEKLY $570/wk, three children, Box 1, health $33/$43, $300/wk lower-earner
// child care) must reproduce that script's rule1_share/rule2_gross_share/rule3_share (87.7% /
// 64.3% / 48.4% at kids_under_13=0, the site-wide convention -- the script itself prints 48.2% at
// its own KIDS_UNDER_13=2, a different, real-fact-pattern constant this calculator does not use)
// and rule2b_share/rule2b_7d (64.5% / $1,206.08/wk) to the value it actually prints -- run
// 2026-09-07 (see model/childcare_post_transfer.py's own docstring). This is also calculator.js's
// fixedRuleSanityPasses() target: worked example, $300 lower-earner child care, fix on ->
// $1,206/wk. PART 10 also pins the "on money after tax" rule (netRuleSanityPasses() target):
// order stays at $1,013/wk, share 48.4%.
// ---------------------------------------------------------------------------------------------
console.log('\n=== PART 10: childcare_post_transfer.py fidelity -- 87.7% / 64.3% / 48.4%, rule2b $1,206/wk ===\n');

var weDist = computeDistribution(PAYOR_GROSS, RECIP_GROSS, { kids: KIDS, box: 1, healthLow: 33.0, healthHigh: 43.0 });
close(weDist.share3c, 0.8768174760022585, 1e-9, 'worked example dist_share3c (rule1_share) = 87.7%');
close(weDist.gross_share, 0.6431593046358441, 1e-9, 'worked example dist_gross_share (rule2_gross_share) = 64.3%');
close(weDist.net_share, 0.4839833869380114, 1e-9, 'worked example dist_net_share (rule3_share, kids_under_13=0) = 48.4%');
equal(pct1(weDist.share3c), '87.7%', 'worked example: formatted higher earner\'s share of child care = 87.7%');
equal(pct0(weDist.gross_share), '64%', 'worked example: formatted post-transfer gross share = 64%');
equal(pct0(weDist.net_share), '48%', 'worked example: formatted post-transfer net share = 48%');

var weFix = computeFixedRule(PAYOR_GROSS, RECIP_GROSS, { kids: KIDS, box: 1, healthLow: 33.0, healthHigh: 43.0, ccLower: 300.0, ccHigher: 0.0 });
close(weFix.fixed_rule_share, 0.6445081434447836, 1e-9, 'worked example fixed_rule_share (rule2b_share) = 64.5%');
close(weFix.fixed_rule_order_wk, 1206.0781733947601, 1e-6, 'worked example fixed_rule_order_wk (rule2b_7d) = $1,206.08/wk');
equal(Math.round(weFix.fixed_rule_order_wk), 1206,
  'worked example: "on income after the order" rule rounds to $1,206/wk (calculator.js\'s fixedRuleSanityPasses() target)');
equal(moneyWk(weFix.fixed_rule_order_wk), '$1,206/wk', 'worked example: formatted "on income after the order" order = $1,206/wk');
equal(moneyWk(sanityCc.order_wk), '$1,276/wk', 'worked example: formatted Worksheet order (the comparison figure) = $1,276/wk');

var weNet = computeNetRule(PAYOR_GROSS, RECIP_GROSS, { kids: KIDS, box: 1, healthLow: 33.0, healthHigh: 43.0 }, 300.0);
close(weNet.net_rule_share, 0.4839833869380114, 1e-9, 'worked example net_rule_share = 48.4%');
close(weNet.net_rule_order_wk, 1012.7257303613252, 1e-6, 'worked example net_rule_order_wk stays at the no-child-care order');
close(weNet.net_rule_charge_wk, 145.19501608140342, 1e-6, 'worked example net_rule_charge_wk at $300/wk lower-earner child care = $145.20/wk');
equal(Math.round(weNet.net_rule_order_wk), 1013,
  'worked example: "on money after tax" rule order rounds to $1,013/wk, unchanged from the no-child-care order (calculator.js\'s netRuleSanityPasses() target)');
equal(moneyWk(weNet.net_rule_order_wk), '$1,013/wk', 'worked example: formatted "on money after tax" order = $1,013/wk');
equal(money(weNet.net_rule_charge_wk * 52), '$7,550/yr', 'worked example: formatted "on money after tax" annual charge at $300/wk = $7,550/yr');

console.log('\n' + checks + ' checks, ' + failures + ' failed.');
process.exit(failures ? 1 : 0);
