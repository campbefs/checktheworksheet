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
// v2 (2026-09-07) adds two real controls -- children (1/2/3, default 3) and custody (Box 1
// shared / Box 2 primary with the lower earner, default Box 1) -- plus a second output row,
// "after tax and the order, per year," inside a <details open>. Health premiums stay fixed at
// $33/wk (lower earner) / $43/wk (higher earner) and child care stays $0, matching the
// convention already used by model/charts/_common.py's `order()` for every heatmap in this
// project (lower earner always gets the $33 premium, higher earner the $43 premium, regardless
// of which one the worksheet ends up naming "payor"). The MA Child and Family Tax Credit for
// children under 13 is fixed at ZERO qualifying children on this tool -- the same generic-grid
// convention as every heatmap on this site (there is no control for how many of the children are
// under 13) -- so the recipient-household figures below run slightly LOWER than the site's own
// worked-example figures elsewhere, which use two of three children under 13. See the method
// line in the markup and CONVENTIONS.md SS11.
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
//            min="60000" max="300000" step="120" value="201000">
//   </div>
//   <div class="tool-slider-row">
//     <label for="calc-lower">Lower earner, gross per year
//       <output id="calc-lower-output" for="calc-lower">$29,640/yr</output>
//     </label>
//     <input type="range" id="calc-lower" data-calc-input="lower"
//            min="0" max="120000" step="120" value="29640">
//   </div>
//   <div class="tool-controls-row">
//     <fieldset class="segmented">
//       <legend>Children</legend>
//       <label class="segmented-option"><input type="radio" name="calc-kids" value="1" data-calc-radio="kids">1</label>
//       <label class="segmented-option"><input type="radio" name="calc-kids" value="2" data-calc-radio="kids">2</label>
//       <label class="segmented-option"><input type="radio" name="calc-kids" value="3" data-calc-radio="kids" checked>3</label>
//     </fieldset>
//     <fieldset class="segmented">
//       <legend>Custody</legend>
//       <label class="segmented-option"><input type="radio" name="calc-custody" value="1" data-calc-radio="custody" checked>Shared, equal time (Box 1)</label>
//       <label class="segmented-option"><input type="radio" name="calc-custody" value="2" data-calc-radio="custody">Primary with the lower earner (Box 2)</label>
//     </fieldset>
//   </div>
//   <div class="tool-readout" aria-live="polite">
//     <div>
//       <p class="cell-label">Weekly order (Line 7d)</p>
//       <p class="cell-value" data-calc-cell="order_wk">$1,013/wk</p>
//     </div>
//     <div>
//       <p class="cell-label">Line 7e's reading</p>
//       <p class="cell-value payor-line" data-calc-cell="line_7e">26.5%</p>
//     </div>
//     <div>
//       <p class="cell-label">True share of the payor's net income</p>
//       <p class="cell-value" data-calc-cell="true_pct_net">37.7%</p>
//       <p class="cell-note" data-calc-note="true_pct_net">&nbsp;</p>
//     </div>
//   </div>
//   <p class="tool-flag" data-calc-flag>&nbsp;</p>
//   <details class="tool-detail" open>
//     <summary>After tax and the order, per year</summary>
//     <div class="tool-readout tool-readout--pair">
//       <div>
//         <p class="cell-label">Payor keeps</p>
//         <p class="cell-value" data-calc-cell="payor_after">$87,172/yr</p>
//       </div>
//       <div>
//         <p class="cell-label">Recipient household holds</p>
//         <p class="cell-value is-warning" data-calc-cell="recip_after">$92,941/yr</p>
//         <p class="cell-sub">Per person: <strong data-calc-cell="recip_per_person">$23,235/yr</strong></p>
//         <p class="cell-note" data-calc-note="recip_after">Above the payor</p>
//       </div>
//     </div>
//     <p class="tool-flag" data-calc-flag-household>&nbsp;</p>
//   </details>
// </div>
//
// (`.tool-readout` is a 3-column CSS grid in assets/css/site.css -- exactly three direct
// children, each a wrapper `<div>` holding one `.cell-label` + one `.cell-value` pair, matching
// the pattern the child-care valve slider already uses. `.tool-readout--pair` is the 2-column
// modifier used inside the <details>.)
//
// - The two `data-calc-input` sliders MUST default (via their `value` attribute) to the worked
//   example's real incomes, the two `data-calc-radio` groups MUST default to kids=3/box=1 (the
//   `checked` attribute), and every `data-calc-cell` span MUST already contain that baseline's
//   real, precomputed numbers as static text ($1,013/wk, 26.5%, 37.7%, $87,172/yr, $92,941/yr,
//   $23,235/yr -- see assets/js/fixtures/calculator-v2.json, kids=3/box=1/higher=201000/lower=29640).
//   A no-JS visitor sees the worked example stated correctly and only loses the ability to change
//   it -- never a blank control (design brief SS3.7 item 1's no-JS fallback requirement). The
//   `<details open>` renders its content with no JavaScript at all -- only the ability to collapse
//   it is progressive enhancement (the browser's own native behaviour, not this script's).
// - `data-calc-flag` / `data-calc-flag-household`: this script fills each in on every change; a
//   page does not need to pre-write their text (unlike the sliders, radios and readouts, these
//   elements do not need real content before JS runs, since they restate information the
//   readouts above them already state).
// - `data-calc-note`: a short bold text label paired with the warning colour (WCAG 1.4.1 -- colour
//   is never the only channel). Two of them: one beside "True share of the payor's net income"
//   ("above 40% of net"), one beside "Recipient household holds" ("above the payor"). Both start
//   empty (a non-breaking space) and are filled in only when the condition is true.
// - This script requires `assets/js/lib/worksheet.js` and `assets/js/lib/net-position.js` to be
//   loaded first (as separate <script> tags, in that order, before this file) -- it does not
//   bundle them, so a page opts in with:
//     scripts: ["/assets/js/lib/worksheet.js", "/assets/js/lib/net-position.js", "/assets/js/calculator.js"]
// - SANITY GUARD: before wiring up the sliders and radios, this script recomputes the worked
//   example (higher $201,000, lower $29,640, kids=3, box=1 -- fixed DEFAULT_FACTS below,
//   independent of whatever the radios currently show) and checks the weekly order rounds to
//   $1,013 -- the same figure calculator.test.js pins. If it doesn't (a bad edit to either lib/
//   file, a load that silently returned wrong data), every control is disabled, every
//   `data-calc-cell` is replaced with "not available," and both flags explain why -- never a
//   plausible-looking wrong number. See sanityCheckPasses()/showUnavailable() below.
// - MOUNT-TIME BUG FOUND AND FIXED 2026-09-07: `step="1000"` on `min="0"` makes the lower
//   slider's default `value="29640"` an invalid step -- a browser silently rounds a range
//   input's live `.value` to the nearest valid step from `min` on parse, so the DOM read
//   `30000`, not `29640`, and the on-load render computed $1,011/wk instead of $1,013/wk (a
//   wrong-but-plausible number the sanity guard above does NOT catch, since it recomputes
//   directly against the fixed constants 201000/29640, not against what the sliders' own
//   `.value` returns). `step="120"` divides both sliders' `(value - min)` exactly (GCD of the
//   two required offsets, 141000 and 29640, is 120), so both defaults hold on load in every
//   browser. Found by reading the live DOM after mounting, not by any of the Node-side tests --
//   a lesson for any future markup contract change: check `element.value`, not only the
//   `value` attribute, once real HTML is in a real page.
//
// FIXED FACTS, not sliders (per design brief SS3.5's word budget): no child care, health
// premiums $33/wk lower earner, $43/wk higher earner, MA under-13 credit fixed at zero
// qualifying children. Children and custody are now real controls (see MCSGCalculatorFacts).
var MCSGCalculatorDefaults = { kids: 3, box: 1, childcare: 0, healthLow: 33.0, healthHigh: 43.0 };
var MCSGCalculatorFacts = { kids: 3, box: 1, childcare: 0, healthLow: 33.0, healthHigh: 43.0 };

(function () {
  'use strict';

  if (typeof window === 'undefined') return; // Node (calculator.test.js) loads the libs directly.

  var W = window.MCSGWorksheet;
  var N = window.MCSGNetPosition;

  function money(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/yr'; }
  function moneyWk(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/wk'; }
  function pct1(v) { return (v * 100).toFixed(1) + '%'; }

  // The single computation this whole tool is built on: given the two annual gross incomes and
  // a facts object (kids, box, childcare, healthLow, healthHigh), return the weekly order, Line
  // 7e's reading, the true share of the payor's net income, and the after-tax/after-order yearly
  // figures for both households. Exported on window for calculator.test.js to call directly with
  // fixed test incomes and facts.
  function computeWithFacts(higherAnnual, lowerAnnual, facts) {
    var lowerWk = lowerAnnual / 52.0;
    var higherWk = higherAnnual / 52.0;
    var r = W.run(facts.box, lowerWk, higherWk,
      facts.kids, 0,
      { aHealth: facts.healthLow, bHealth: facts.healthHigh });
    // Parent A = lower earner, Parent B = higher earner (matches model/charts/_common.py's
    // order() convention). Map worksheet's A/B payor designation back onto actual gross incomes.
    var payorGross = r.payor === 'A' ? lowerAnnual : higherAnnual;
    var recipGross = r.payor === 'A' ? higherAnnual : lowerAnnual;
    // kids_under_13 fixed at 0 -- see the header comment and CONVENTIONS.md SS11: no control on
    // this tool for how many children are under 13, so the recipient household figures below run
    // slightly lower than this site's worked-example figures elsewhere (two of three under 13).
    var pos = N.analyze(payorGross, recipGross, facts.kids, r['7d'], 0.0, 0.0, undefined, 0);
    return {
      order_wk: r['7d'],
      line_7e: r['7e'],
      true_pct_net: pos.support_pct_of_payor_net,
      payor_after: pos.payor_after,
      recip_after: pos.recip_after,
      recip_per_person: pos.recip_per_person,
      payor_is: r.payor === 'A' ? 'lower' : 'higher'
    };
  }

  function compute(higherAnnual, lowerAnnual) {
    return computeWithFacts(higherAnnual, lowerAnnual, MCSGCalculatorFacts);
  }

  // Sanity guard: the worked example ($201,000 higher earner, $29,640 lower earner) at the
  // DEFAULT facts (three children, Box 1) must reproduce the site's own tested figure, $1,013/wk
  // (see calculator.test.js PART 3) -- checked against MCSGCalculatorDefaults, not against
  // whatever the radios currently show, so this guard means the same thing regardless of what a
  // reader has selected. If a future edit to either lib/ file, or a bad load, changes that
  // answer, showing a wrong number silently is worse than showing nothing -- render a visible
  // "calculator unavailable" note instead of numbers rather than trust an unverified result.
  function sanityCheckPasses() {
    try {
      var r = computeWithFacts(201000, 29640, MCSGCalculatorDefaults);
      return Math.round(r.order_wk) === 1013;
    } catch (e) {
      if (window.console) console.error('calculator.js: sanity check threw', e);
      return false;
    }
  }

  function showUnavailable(root, inputs, radios, cells, flags) {
    root.setAttribute('data-calc-unavailable', 'true');
    Object.keys(inputs).forEach(function (key) { inputs[key].disabled = true; });
    radios.forEach(function (el) { el.disabled = true; });
    Object.keys(cells).forEach(function (key) { cells[key].textContent = 'not available'; });
    flags.forEach(function (flag) {
      if (!flag) return;
      flag.textContent = 'This calculator is temporarily unavailable: its self-check against ' +
        'the worked example did not match. Method: ' +
        'model/worksheet.py and model/net_position.py, ported in assets/js/lib/worksheet.js.';
      flag.classList.add('visible');
    });
    if (window.console) console.error('calculator.js: sanity check failed, worked example did not reproduce $1,013/wk');
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
    var radios = Array.prototype.slice.call(root.querySelectorAll('[data-calc-radio]'));
    var cells = {};
    Array.prototype.slice.call(root.querySelectorAll('[data-calc-cell]')).forEach(function (el) {
      cells[el.getAttribute('data-calc-cell')] = el;
    });
    var notes = {};
    Array.prototype.slice.call(root.querySelectorAll('[data-calc-note]')).forEach(function (el) {
      notes[el.getAttribute('data-calc-note')] = el;
    });
    var flag = root.querySelector('[data-calc-flag]');
    var flagHousehold = root.querySelector('[data-calc-flag-household]');

    if (!sanityCheckPasses()) {
      showUnavailable(root, inputs, radios, cells, [flag, flagHousehold]);
      return;
    }

    function outputFor(input) {
      return document.getElementById(input.id + '-output') || root.querySelector('output[for="' + input.id + '"]');
    }

    function setNote(key, text) {
      var el = notes[key];
      if (!el) return;
      if (text) {
        el.textContent = text;
        el.classList.add('visible');
      } else {
        el.textContent = ' ';
        el.classList.remove('visible');
      }
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

      // True share of the payor's net income: warning colour + bold text label only past 40%
      // (WCAG 1.4.1 -- colour is never the only channel). Below 40% the value renders in the
      // ordinary text colour, matching Line 7e's own 40% substantial-hardship threshold.
      if (cells.true_pct_net) {
        cells.true_pct_net.textContent = pct1(result.true_pct_net);
        var overHardship = result.true_pct_net > 0.40;
        cells.true_pct_net.classList.toggle('is-warning', overHardship);
        setNote('true_pct_net', overHardship ? 'Above 40% of net' : '');
      }

      if (cells.payor_after) cells.payor_after.textContent = money(result.payor_after);
      if (cells.recip_after) {
        cells.recip_after.textContent = money(result.recip_after);
        var recipAhead = result.recip_after > result.payor_after;
        cells.recip_after.classList.toggle('is-warning', recipAhead);
        setNote('recip_after', recipAhead ? 'Above the payor' : '');
      }
      if (cells.recip_per_person) cells.recip_per_person.textContent = money(result.recip_per_person);

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

      if (flagHousehold) {
        if (result.recip_after > result.payor_after) {
          flagHousehold.textContent = 'The recipient household holds more than the payor keeps: ' +
            money(result.recip_after) + ' against ' + money(result.payor_after) + '. Per person, the ' +
            'household has ' + money(result.recip_per_person) + ' against the payor\'s ' + money(result.payor_after) + '.';
          flagHousehold.classList.add('visible');
        } else {
          flagHousehold.textContent = '';
          flagHousehold.classList.remove('visible');
        }
      }
    }

    inputs.higher && inputs.higher.addEventListener('input', render);
    inputs.lower && inputs.lower.addEventListener('input', render);
    radios.forEach(function (el) {
      el.addEventListener('change', function () {
        var group = el.getAttribute('data-calc-radio');
        MCSGCalculatorFacts[group] = Number(el.value);
        render();
      });
    });
    render();
  }

  // Exposed for a manual browser-console spot check (e.g. MCSGCalculatorCompute(201000, 29640)).
  // calculator.test.js runs in Node, where `window` does not exist, so it re-derives this same
  // arithmetic against lib/worksheet.js and lib/net-position.js directly rather than calling this.
  window.MCSGCalculatorCompute = compute;
  window.MCSGCalculatorComputeWithFacts = computeWithFacts;
  document.querySelectorAll('[data-calculator]').forEach(initCalculator);
})();
