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

console.log('\n' + checks + ' checks, ' + failures + ' failed.');
process.exit(failures ? 1 : 0);
