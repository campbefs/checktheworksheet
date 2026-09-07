// checktheworksheet.org -- the home-page two-income calculator (design brief SS3.7, item 1).
// Vanilla JS, no dependencies, no CDN. Unlike csv-slider.js (which powers the child-care valve
// slider and the credit-collapse slider by looking up a precomputed grid), this tool COMPUTES
// its answer for any two incomes, using a faithful, tested port of the worksheet and tax model
// -- assets/js/lib/worksheet.js and assets/js/lib/net-position.js. It is not a lookup because a
// two-income grid coarse enough to ship as JSON (the design brief's original $5,000-step
// heatmap) cannot reproduce the worked example ($201,000 / $29,640) to the dollar; the ported,
// tested computation can, and IS tested to the dollar against the Commonwealth's own CJ-D 304
// XFA calculate-scripts -- see assets/js/calculator.test.js and its own header comment.
//
// Three children, no child care, Box 1 (shared parenting), health premiums $33/wk (lower
// earner) and $43/wk (higher earner) -- the worked example's own facts, matching the convention
// already used by model/charts/_common.py's `order()` for every heatmap in this project (lower
// earner always gets the $33 premium, higher earner the $43 premium, regardless of which one
// the worksheet ends up naming "payor").
//
// ---------------------------------------------------------------------------------------------
// MARKUP CONTRACT
// ---------------------------------------------------------------------------------------------
// <div class="tool tool-two-up" data-calculator>
//   <div class="tool-slider-row">
//     <label for="calc-higher">Higher earner, gross per year
//       <output id="calc-higher-output" for="calc-higher">$201,000/yr</output>
//     </label>
//     <input type="range" id="calc-higher" data-calc-input="higher"
//            min="60000" max="300000" step="1000" value="201000">
//   </div>
//   <div class="tool-slider-row">
//     <label for="calc-lower">Lower earner, gross per year
//       <output id="calc-lower-output" for="calc-lower">$29,640/yr</output>
//     </label>
//     <input type="range" id="calc-lower" data-calc-input="lower"
//            min="0" max="120000" step="1000" value="29640">
//   </div>
//   <div class="tool-readout" aria-live="polite">
//     <p class="cell-value"><span class="cell-label">Weekly order (Line 7d)</span>
//        <span data-calc-cell="order_wk">$1,013/wk</span></p>
//     <p class="cell-value payor-line"><span class="cell-label">Line 7e's reading</span>
//        <span data-calc-cell="line_7e">26.5%</span></p>
//     <p class="cell-value true-burden"><span class="cell-label">True share of the payor's net income</span>
//        <span data-calc-cell="true_pct_net">37.7%</span></p>
//   </div>
//   <p class="tool-flag" data-calc-flag>&nbsp;</p>
// </div>
//
// - The two `data-calc-input` sliders MUST default (via their `value` attribute) to the worked
//   example's real incomes, and the three `data-calc-cell` spans MUST already contain that
//   baseline's real, precomputed numbers as static text ($1,013/wk, 26.5%, 37.7% -- see
//   model/runs/submission-figures-run-2026-09-05.txt, "child care/wk 0" row). A no-JS visitor
//   sees the worked example stated correctly and only loses the ability to change it -- never a
//   blank control (design brief SS3.7 item 1's no-JS fallback requirement).
// - `data-calc-flag`: this script fills it in on every change with a full sentence stating the
//   gap in percentage points; a page does not need to pre-write its text (unlike the sliders and
//   readouts, this element does not need real content before JS runs, since it is not load-
//   bearing information -- the two readouts above it already state both percentages).
// - This script requires `assets/js/lib/worksheet.js` and `assets/js/lib/net-position.js` to be
//   loaded first (as separate <script> tags, in that order, before this file) -- it does not
//   bundle them, so a page opts in with:
//     scripts: ["/assets/js/lib/worksheet.js", "/assets/js/lib/net-position.js", "/assets/js/calculator.js"]
//
// FIXED FACTS (not sliders, per design brief SS3.5's word budget -- three children, no child care):
var MCSGCalculatorFacts = { kids: 3, childcare: 0, box: 1, healthLow: 33.0, healthHigh: 43.0 };

(function () {
  'use strict';

  if (typeof window === 'undefined') return; // Node (calculator.test.js) loads the libs directly.

  var W = window.MCSGWorksheet;
  var N = window.MCSGNetPosition;

  function money(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/yr'; }
  function moneyWk(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/wk'; }
  function pct1(v) { return (v * 100).toFixed(1) + '%'; }

  // The single computation this whole tool is built on: given the two annual gross incomes,
  // return the weekly order, Line 7e's reading, and the true share of the payor's net income.
  // Exported on window for calculator.test.js to call directly with fixed test incomes.
  function compute(higherAnnual, lowerAnnual) {
    var lowerWk = lowerAnnual / 52.0;
    var higherWk = higherAnnual / 52.0;
    var r = W.run(MCSGCalculatorFacts.box, lowerWk, higherWk,
      MCSGCalculatorFacts.kids, 0,
      { aHealth: MCSGCalculatorFacts.healthLow, bHealth: MCSGCalculatorFacts.healthHigh });
    // Parent A = lower earner, Parent B = higher earner (matches model/charts/_common.py's
    // order() convention). Map worksheet's A/B payor designation back onto actual gross incomes.
    var payorGross = r.payor === 'A' ? lowerAnnual : higherAnnual;
    var recipGross = r.payor === 'A' ? higherAnnual : lowerAnnual;
    var pos = N.analyze(payorGross, recipGross, MCSGCalculatorFacts.kids, r['7d'], 0.0, 0.0, undefined, 0);
    return {
      order_wk: r['7d'],
      line_7e: r['7e'],
      true_pct_net: pos.support_pct_of_payor_net,
      payor_is: r.payor === 'A' ? 'lower' : 'higher'
    };
  }

  function initCalculator(root) {
    if (!W || !N) {
      // Libraries failed to load -- leave the page's own static worked-example text untouched
      // (see MARKUP CONTRACT above); never show a broken control.
      root.setAttribute('data-calc-load-failed', 'true');
      if (window.console) console.error('calculator.js: assets/js/lib/worksheet.js or net-position.js not loaded');
      return;
    }

    var inputs = {};
    Array.prototype.slice.call(root.querySelectorAll('[data-calc-input]')).forEach(function (el) {
      inputs[el.getAttribute('data-calc-input')] = el;
    });
    var cells = {};
    Array.prototype.slice.call(root.querySelectorAll('[data-calc-cell]')).forEach(function (el) {
      cells[el.getAttribute('data-calc-cell')] = el;
    });
    var flag = root.querySelector('[data-calc-flag]');

    function outputFor(input) {
      return document.getElementById(input.id + '-output') || root.querySelector('output[for="' + input.id + '"]');
    }

    function render() {
      var higher = Number(inputs.higher.value);
      var lower = Number(inputs.lower.value);
      // Sliders are independent controls; a reader can drag "lower" past "higher". Normalise so
      // labels stay honest -- the arithmetic itself does not care which slider is which, only
      // which of the two incomes is larger (health premiums and the worked-example framing do).
      var hi = Math.max(higher, lower);
      var lo = Math.min(higher, lower);
      var result = compute(hi, lo);

      if (cells.order_wk) cells.order_wk.textContent = moneyWk(result.order_wk);
      if (cells.line_7e) cells.line_7e.textContent = pct1(result.line_7e);
      if (cells.true_pct_net) cells.true_pct_net.textContent = pct1(result.true_pct_net);

      var out = outputFor(inputs.higher);
      if (out) out.textContent = money(higher);
      inputs.higher.setAttribute('aria-valuetext', 'Higher earner: ' + money(higher).replace('/yr', '') + ' a year');

      var outLo = outputFor(inputs.lower);
      if (outLo) outLo.textContent = money(lower);
      inputs.lower.setAttribute('aria-valuetext', 'Lower earner: ' + money(lower).replace('/yr', '') + ' a year');

      if (flag) {
        var gapPts = (result.true_pct_net - result.line_7e) * 100;
        if (gapPts >= 5) {
          flag.textContent = 'Line 7e reads ' + pct1(result.line_7e) + ' of available income. The payor\'s ' +
            'true burden is already ' + pct1(result.true_pct_net) + ' of net income, a gap of ' +
            gapPts.toFixed(0) + ' percentage points.';
          flag.classList.add('visible');
        } else {
          flag.textContent = '';
          flag.classList.remove('visible');
        }
      }
    }

    inputs.higher && inputs.higher.addEventListener('input', render);
    inputs.lower && inputs.lower.addEventListener('input', render);
    render();
  }

  window.MCSGCalculatorCompute = compute; // exposed for calculator.test.js / manual console checks
  document.querySelectorAll('[data-calculator]').forEach(initCalculator);
})();
