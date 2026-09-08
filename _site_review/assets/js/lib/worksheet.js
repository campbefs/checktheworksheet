// checktheworksheet.org -- faithful JavaScript port of model/worksheet.py (CJ-D 304, the 2025
// Massachusetts Child Support Guidelines Worksheet), for the home-page two-income calculator.
//
// THIS IS A PORT, NOT A REIMPLEMENTATION. Every function and line below corresponds to the
// same-named function/line in model/worksheet.py (read that file's own docstring for what each
// worksheet line means -- it is not repeated here). Do not change the arithmetic here without
// making the identical change there, and re-running calculator.test.js afterwards.
//
// TESTED FIDELITY (assets/js/calculator.test.js, run with `node assets/js/calculator.test.js`):
// reproduces, field for field, all six fact patterns in
// model/runs/official-xfa-vs-model-2026-09-05.txt, both in "round_lines" mode (which matches the
// Commonwealth's own CJ-D 304 XFA calculate-scripts to the dollar on every one of the six) and in
// the default unrounded mode (which is what every dollar figure quoted in the letter, the paper
// and this site's own MEMORY.md was computed from -- e.g. the worked example's $1,013/week).
//
// KNOWN, NEGLIGIBLE DIVERGENCE FROM THE PYTHON: Python's round() is round-half-to-even;
// Math.round() below is round-half-away-from-zero. The two disagree only when a value lands
// exactly on a .5 cent or .5-dollar boundary, which does not occur at any input this project has
// tested (see calculator.test.js). Documented here rather than hidden.
//
// Usage (browser): <script src="/assets/js/lib/worksheet.js"></script> attaches
// `window.MCSGWorksheet`. Usage (Node, for tests): `require('./lib/worksheet.js')`.

(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.MCSGWorksheet = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var TABLE_B = { 0: 0.00, 1: 1.00, 2: 1.40, 3: 1.68, 4: 1.85, 5: 1.94 };

  // Table C: adjustment percentage, keyed "u18,18p" (children under 18, children 18+).
  var TABLE_C = {
    '0,1': 0.25, '0,2': 0.25, '0,3': 0.25, '0,4': 0.25, '0,5': 0.25,
    '1,1': 0.07, '1,2': 0.11, '1,3': 0.13, '1,4': 0.14,
    '2,1': 0.04, '2,2': 0.06, '2,3': 0.07,
    '3,1': 0.02, '3,2': 0.03,
    '4,1': 0.01
  };

  var CAP = 8654;          // 3d
  var CC_BENCHMARK = 430;  // 6a, per child per week
  var LOW_INCOME = 391;    // 5c / 6e shaded-area threshold

  // Table A as printed on CJ-D 304 page 4. Weekly, one child under 18.
  function tableA(x) {
    if (x < 0) return 0.0;
    if (x <= 301) return 15.0;                        // CJ-D 304 places $0 here: minimum order $15
    if (x <= 391) return 15 + 0.20 * (x - 301);
    if (x <= 1000) return 0.22 * x;
    if (x <= 1600) return 220 + 0.21 * (x - 1000);
    if (x <= 2400) return 346 + 0.18 * (x - 1600);
    if (x <= 3500) return 490 + 0.14 * (x - 2400);
    if (x <= 5000) return 644 + 0.11 * (x - 3500);
    return 809 + 0.10 * (x - 5000);
  }

  // The "but not less than an amount from the shaded area of the Guidelines Chart" floor on
  // Lines 6e and 7b. The shaded area is the band at or below $391 of available income, so the
  // floor only bites there.
  function floorShaded(value, otherThreeA) {
    return otherThreeA <= LOW_INCOME ? Math.max(value, tableA(otherThreeA)) : value;
  }

  // 6a. Per child: if the TOTAL both parents paid for that child exceeds $430, scale this
  // parent's share down proportionally. Returns this parent's total across all children.
  function ccBenchmarked(perChildPaid) {
    var out = 0.0;
    for (var i = 0; i < perChildPaid.length; i++) {
      var a = perChildPaid[i][0], b = perChildPaid[i][1];
      var total = a + b;
      out += total <= CC_BENCHMARK ? a : a * (CC_BENCHMARK / total);
    }
    return out;
  }

  /**
   * Port of worksheet.py's run(). Parent A / Parent B per the worksheet's own convention.
   * For Box 2, Parent A is the parent the children primarily reside with.
   *
   * @param {number} box 1 (shared), 2 (primary), or 3 (split)
   * @param {number} aGross Parent A gross weekly income
   * @param {number} bGross Parent B gross weekly income
   * @param {number} childrenUnder18
   * @param {number} [children18plus=0]
   * @param {object} [opts]
   *   aHealth, bHealth, aDental, bDental (weekly premiums, default 0)
   *   aOtherSupport, bOtherSupport (weekly, default 0)
   *   aChildcare, bChildcare (arrays of per-child weekly amounts, default [])
   *   aChildren, bChildren ([under18, 18plus] tuples, Box 3 only)
   *   roundLines (bool, default false) -- round every line as CJ-D 304's own XFA scripts do
   * @returns {object} same field names as worksheet.py's dict (bracket-accessed: result['3b'])
   */
  function run(box, aGross, bGross, childrenUnder18, children18plus, opts) {
    children18plus = children18plus || 0;
    opts = opts || {};
    var aHealth = opts.aHealth || 0.0, bHealth = opts.bHealth || 0.0;
    var aDental = opts.aDental || 0.0, bDental = opts.bDental || 0.0;
    var aOtherSupport = opts.aOtherSupport || 0.0, bOtherSupport = opts.bOtherSupport || 0.0;
    var aChildcare = opts.aChildcare || [];
    var bChildcare = opts.bChildcare || [];
    var roundLines = !!opts.roundLines;

    // CJ-D 304 page 1: "Round all numbers to the nearest whole dollar or percentage." By
    // default (roundLines=false) this carries full precision so the arithmetic is traceable,
    // matching model/worksheet.py's own default and every dollar figure quoted in the project's
    // documents; roundLines=true rounds each line as the physical form does.
    var R = roundLines ? function (x) { return Math.round(x); } : function (x) { return x; };
    var P = roundLines ? function (x) { return Math.round(x * 100) / 100; } : function (x) { return x; };

    // --- 3a available income
    var a3a = R(Math.max(0.0, aGross - aOtherSupport - aHealth - aDental));
    var b3a = R(Math.max(0.0, bGross - bOtherSupport - bHealth - bDental));
    var b3b = a3a + b3a;
    var a3c = b3b ? P(a3a / b3b) : 0.0;
    var b3c = b3b ? P(b3a / b3b) : 0.0;
    var d3d = Math.min(b3b, CAP);
    var e3e = R(tableA(d3d));

    // --- 1d/1e: child counts per column depend on the box. The ONLY thing the box selection
    // changes. Every later line naming a box says "Box 1 or Box 3" and treats them identically
    // (5c, 6d, 6e, 6f, 6g, 7a), so split follows the shared path from here on.
    var aCnt, bCnt;
    if (box === 1) {
      aCnt = bCnt = [childrenUnder18, children18plus];
    } else if (box === 2) {
      aCnt = [childrenUnder18, children18plus];
      bCnt = [0, 0];
    } else if (box === 3) {
      if (!opts.aChildren || !opts.bChildren) {
        throw new Error('Box 3 requires opts.aChildren and opts.bChildren as [under18, 18plus]');
      }
      aCnt = opts.aChildren.slice();
      bCnt = opts.bChildren.slice();
      if (aCnt[0] + bCnt[0] !== childrenUnder18 || aCnt[1] + bCnt[1] !== children18plus) {
        throw new Error('Box 3 child counts do not sum to the totals given');
      }
      if ((aCnt[0] + aCnt[1]) === 0 || (bCnt[0] + bCnt[1]) === 0) {
        throw new Error('Box 3 requires each parent to have at least one child; otherwise use Box 2');
      }
    } else {
      throw new Error('box must be 1, 2 or 3, got ' + box);
    }

    // Lines 3f, 3g, 4a, 4b, 4c for one column. Table C is keyed on the children in THAT
    // column's 1d/1e -- under Box 1 both columns hold every child so this is the same as
    // keying it globally; under Box 3 it is not.
    function col(cnt) {
      var nU18 = cnt[0], n18p = cnt[1];
      var nCol = nU18 + n18p;
      var f3f = TABLE_B[Math.min(nCol, 5)];
      var g3g = R(e3e * f3f);
      var pct = nCol ? (TABLE_C[nU18 + ',' + n18p] || 0.0) : 0.0;
      var b4b = R(g3g * pct);
      var c4c = g3g - b4b;
      return [g3g, c4c];
    }

    var a4c = col(aCnt)[1];
    var b4c = col(bCnt)[1];

    // --- 5a / 5b. Each column's 5b is what the OTHER parent owes this parent.
    var a5a = R(a3c * a4c), b5a = R(b3c * b4c);
    var a5b = a4c - a5a, b5b = b4c - b5a;
    // --- 5c low-income payor adjustment (shaded area applies only at 3a <= $391). 5c is a
    // strict IF/ELSE on the form, not a min(): "If the other parent's 3a > $391, enter 5b. If
    // <= $391, enter the amount from the shaded area of the Chart." Box 2 has its OWN rule that
    // overrides this: "enter $0 for Parent B, and for Parent A: if Parent B 3a > $391, enter
    // 5b..."
    var a5c = b3a > LOW_INCOME ? a5b : tableA(b3a);
    var b5c;
    if (box === 2) {
      b5c = 0.0;
    } else {
      b5c = a3a > LOW_INCOME ? b5b : tableA(a3a);
    }

    // --- 6a / 6b child care. Pad both arrays to equal length (worksheet.py notes: zip() would
    // silently drop a child listed by one parent only).
    var n = Math.max(aChildcare.length, bChildcare.length);
    var acc = aChildcare.slice(); while (acc.length < n) acc.push(0.0);
    var bcc = bChildcare.slice(); while (bcc.length < n) bcc.push(0.0);
    var a6a = 0.0, b6a = 0.0;
    if (aChildcare.length) {
      var pairsA = []; for (var i = 0; i < n; i++) pairsA.push([acc[i], bcc[i]]);
      a6a = ccBenchmarked(pairsA);
    }
    if (bChildcare.length) {
      var pairsB = []; for (var j = 0; j < n; j++) pairsB.push([bcc[j], acc[j]]);
      b6a = ccBenchmarked(pairsB);
    }
    var a6b = R(b3c * a6a), b6b = R(a3c * b6a); // other parent's share of what this parent paid

    var a6c = a5c + a6b, b6c = b5c + b6b;

    // --- 6d / 6e income-disparity adjustment (Box 1 and Box 3 share this path)
    var a6d, b6d, a6e, b6e;
    if (box === 2) {
      a6d = null; b6d = null;
      a6e = a6c; b6e = b6c;
    } else {
      a6d = a3a === 0 ? 1.0 : P(a6c / a3a);
      b6d = b3a === 0 ? 1.0 : P(b6c / b3a);
      // 6e: "...whichever is less, BUT NOT LESS THAN an amount from the shaded area of the
      // Guidelines Chart." The form's own script leaves (6d + 10%) x 3a unrounded (Value_6e_pA/pB
      // in data/extracted/cjd304-xfa.xml); only 7d rounds.
      a6e = a6d >= 0.10 ? a6c : floorShaded(Math.min(a6c, (a6d + 0.10) * b3a), b3a);
      b6e = b6d >= 0.10 ? b6c : floorShaded(Math.min(b6c, (b6d + 0.10) * a3a), a3a);
    }

    // --- 6f payor / recipient
    var recip, payor, r6e, p6e, payorThreeA, recipThreeA;
    if (box === 2) {
      recip = 'A'; payor = 'B';
      r6e = a6e; p6e = b6e;
      payorThreeA = b3a; recipThreeA = a3a;
    } else if (a6e >= b6e) {
      recip = 'A'; payor = 'B'; r6e = a6e; p6e = b6e; payorThreeA = b3a; recipThreeA = a3a;
    } else {
      recip = 'B'; payor = 'A'; r6e = b6e; p6e = a6e; payorThreeA = a3a; recipThreeA = b3a;
    }

    var g6g = Math.max(0.0, r6e - p6e);

    // --- 7a / 7b
    var a7a = null, b7b;
    if (box === 2) {
      a7a = recipThreeA === 0 ? 1.0 : P(g6g / recipThreeA);
      if (a7a >= 0.10) {
        b7b = g6g;
      } else {
        // "enter 6e, 6g, or ((7a + 10%) x Payor 3a), whichever is less": the form's Value_7b
        // script reads the RECIPIENT's 6e here (r6e), not the payor's -- using the payor's 6e
        // zeroed the order whenever this branch fired (fixed 2026-09-05 in worksheet.py).
        b7b = floorShaded(Math.min(r6e, g6g, (a7a + 0.10) * payorThreeA), payorThreeA);
      }
    } else {
      b7b = g6g;
    }

    var d7d = R(Math.max(0.0, b7b));                              // form: Math.round(7b - 7c)
    var e7e = payorThreeA === 0 ? 1.0 : P(d7d / payorThreeA);      // form: (7d / payor 3a).toFixed(2)

    return {
      A_3a: a3a, B_3a: b3a, '3b': b3b, A_3c: a3c, B_3c: b3c,
      '3d': d3d, '3e': e3e, A_4c: a4c, B_4c: b4c,
      A_5c: a5c, B_5c: b5c, A_6a: a6a, B_6a: b6a,
      A_6b: a6b, B_6b: b6b, A_6c: a6c, B_6c: b6c,
      A_6d: a6d, B_6d: b6d, A_6e: a6e, B_6e: b6e,
      recipient: recip, payor: payor,
      '6g': g6g, '7a': a7a, '7d': d7d, '7e': e7e,
      hardship_box: e7e >= 0.40,
      payor_3a: payorThreeA
    };
  }

  return {
    run: run,
    tableA: tableA,
    TABLE_B: TABLE_B,
    TABLE_C: TABLE_C,
    CAP: CAP,
    CC_BENCHMARK: CC_BENCHMARK,
    LOW_INCOME: LOW_INCOME
  };
}));
