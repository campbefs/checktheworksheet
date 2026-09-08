// checktheworksheet.org -- the home-page two-income calculator (design brief SS3.7, item 1).
// Vanilla JS, no dependencies, no CDN. Computes its answer for any two incomes, using a tested
// port of the worksheet and tax model -- assets/js/lib/worksheet.js and
// assets/js/lib/net-position.js -- checked to the dollar against the Commonwealth's own CJ-D 304
// XFA calculate-scripts. See assets/js/calculator.test.js.
//
// v5 (2026-09-07) adds two things to the Child care tab only, both from
// model/childcare_post_transfer.py (not a new computation -- see that file's own docstring for the
// five rules it prints and model/test_childcare_post_transfer.py for what pins them):
//   1. AN ALWAYS-VISIBLE READOUT (computeChildcareDistribution): the higher earner's Line 3c income
//      share (the pre-order share Line 6b already uses to allocate child care), and where that same
//      pair of incomes actually lands after the NO-CHILD-CARE order -- as a share of gross and, using
//      net-position.js, of net. Independent of the two child-care sliders; it is a property of income,
//      children and the custody box alone. Its net-share leg uses kidsUnder13 = min(2, kids) -- the
//      site's own worked example's fact (two of three children are under 13), NOT the zero used
//      everywhere else on this tab -- because the task was to reproduce childcare_post_transfer.py's
//      87.7/64.3/48.2 at that worked example, and that script uses kidsUnder13=2. Every OTHER figure on
//      this tab keeps the site-wide zero convention; only this one readout differs, and it says so.
//   2. A TOGGLE (computeFixedRuleOrder), "the comments' Line 6b-1": recomputes the child-care order by
//      running the worksheet ONCE with no child care to get the base order and the Payor/Recipient
//      designation Line 6f would give in that pass (avoids the circularity a 2026-09-05 review caught --
//      see childcare_post_transfer.py's own header), then allocates the combined child-care dollars on
//      that payor's post-transfer Line 3a share instead of the pre-order Line 3c share. A dedicated
//      sanity check (fixedRuleSanityPasses) gates the toggle alone: if it fails, the toggle disables
//      with a note instead of showing a wrong number, without taking down the rest of the calculator.
//
// v4 (2026-09-07) is an interface rebuild, not a new computation. Three changes:
//   1. TABS. "Base support" (no child care) and "Child care" (two sliders, one per parent) are
//      real tabs (role="tablist"/"tab"/"tabpanel", arrow-key navigation), not a third radio
//      group. Income, children, custody and the two premium inputs are SHARED state above the
//      tabs; each tab computes its own order from that shared state plus its own child-care
//      inputs (Base support always uses $0/$0 child care).
//   2. PREMIUMS became two number inputs (was a fixed $33/$43 constant), default $40/$40 each --
//      so the default reading no longer reproduces the site's own $1,013 worked example, which
//      uses $33/$43. Said plainly in the tool's one-line assumptions text.
//   3. STATUS BADGES. A two-badge strip sits above both tabs' readouts and updates for whichever
//      tab is active: which household is ahead after tax, and whether the order is at or above
//      40% of the payor's net income (the true share, INCLUDING the payor's own child care on the
//      Child care tab). This replaces the old data-calc-flag / data-calc-flag-household text
//      flags, which said the same two things in prose.
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
//   <div class="tool-tabs" role="tablist">
//     <button role="tab" data-calc-tab="base" aria-selected="true" ...>Base support</button>
//     <button role="tab" data-calc-tab="childcare" aria-selected="false" tabindex="-1" ...>Child care</button>
//   </div>
//   <input data-calc-input="higher"> <input data-calc-input="lower">   (income sliders, shared)
//   <input data-calc-radio="kids">   <input data-calc-radio="box">     (shared)
//   <input data-calc-input="healthHigh"> <input data-calc-input="healthLow">  (number inputs, shared)
//   <span data-calc-badge="household">  <span data-calc-badge="hardship">    (status strip, shared)
//   <div data-calc-panel="base">    ... data-calc-cell="order_wk" / "line_7e" / "true_pct_net" ...
//                                    ... data-calc-cell="payor_after" / "recip_after" / "recip_per_person" ...
//   <div data-calc-panel="childcare" hidden>
//     ... data-calc-cell="cc_dist_share3c" / "cc_dist_gross" / "cc_dist_net" (always visible) ...
//     <input data-calc-input="ccLower"> <input data-calc-input="ccHigher">  (child-care sliders)
//     ... data-calc-cell="cc_order_wk" / "cc_delta_wk" / "cc_share_pct" / "cc_share_wk" ...
//     ... data-calc-cell="cc_payor_after" / "cc_recip_after" / "cc_recip_per_person" ...
//     ... data-calc-cell="cc_combined_line" (only filled in when BOTH sliders > 0) ...
//     <input data-calc-input="ccFix" type="checkbox">  (the Line 6b-1 toggle)
//     ... data-calc-cell="cc_fix_compare_wrap" > "cc_fix_order" / "cc_fix_was" (shown when checked) ...
//     ... data-calc-note="cc_fix" (disable message if fixedRuleSanityPasses() fails) ...
// </div>
//
// - Every `data-calc-*` element MUST already contain the real, precomputed defaults as static
//   text (no-JS fallback) -- see index.html. A no-JS visitor sees the default reading stated
//   correctly and only loses the ability to change it or to reach the Child care tab (the tab
//   button is a plain <button>; without JS it does nothing, so the Child care tab's numbers are
//   simply unreachable without JavaScript -- an acceptable narrowing of the existing no-JS
//   fallback, since the Base support tab still renders a complete, correct, static reading).
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
  function moneyBare(v) { return '$' + Math.round(v).toLocaleString('en-US'); }
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
  // healthHigh, ccLower, ccHigher }. ccLower/ccHigher are the two child-care sliders' combined
  // weekly totals (Parent A = lower earner, Parent B = higher earner, always -- see header).
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
    // for how many children are under 13); see CONVENTIONS.md SS11.
    var pos = N.analyze(payorGross, recipGross, facts.kids, r['7d'], weeklyChildcare,
      payorChildcareShare, undefined, 0);

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

  // CHANGE 1 -- the always-visible Child care tab readout. Port of
  // model/childcare_post_transfer.py's rule1_share (Line 3c) / rule2_gross_share / rule3_share, at
  // the NO-CHILD-CARE order -- Chris: "have the base support calculated first and then figure out
  // what the net percentage mix is." Independent of facts.ccLower/facts.ccHigher; only
  // kids/box/healthLow/healthHigh matter. "Higher earner" is Parent B always (see header comment);
  // every fixture row this site has ever computed names B the payor, so this does not special-case
  // a flip.
  function computeChildcareDistribution(higherAnnual, lowerAnnual, facts) {
    var lowerWk = lowerAnnual / 52.0, higherWk = higherAnnual / 52.0;
    var r0 = W.run(facts.box, lowerWk, higherWk, facts.kids, 0,
      { aHealth: facts.healthLow, bHealth: facts.healthHigh });
    var baseOrderWk = r0['7d'];
    var combinedGross = higherAnnual + lowerAnnual;
    var grossShare = combinedGross ? (higherAnnual - baseOrderWk * 52) / combinedGross : 0.0;
    // Two of three children under 13 -- the site's own worked example's fact, not the zero
    // convention this tab's other cells use. See the header comment for why this one readout
    // differs. Capped at facts.kids so a 1- or 2-child selection never claims more under-13
    // children than the family has.
    var kidsUnder13 = Math.min(2, facts.kids);
    var pos = N.analyze(higherAnnual, lowerAnnual, facts.kids, baseOrderWk, 0.0, 0.0, undefined, kidsUnder13);
    return {
      base_order_wk: baseOrderWk,
      share3c: r0.B_3c,
      gross_share: grossShare,
      net_share: pos.payor_after_share
    };
  }

  // CHANGE 2 -- the "apply the proposed fix" toggle. Port of childcare_post_transfer.py's rule2b:
  // run the worksheet with NO child care to get the base order and the Payor/Recipient designation
  // Line 6f would give in that pass, then allocate the COMBINED weekly child care on that payor's
  // post-transfer Line 3a share (Line 3a moved by the base order, over Line 3b) instead of the
  // pre-order Line 3c share Line 6b uses today. This is the letter's Section 2 redline, new
  // Worksheet Line 6b-1. Uses r0.payor generically (not a hardcoded "B") to match the Python's own
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
  // incomes, no child care -- reproduces childcare_post_transfer.py's 87.7% / 64.3% / 48.2%
  // (rule1_share / rule2_gross_share / rule3_share). If this fails it is as serious as the order
  // itself being wrong, so it is folded into the main guard below, not the toggle-only one.
  function distributionSanityPasses() {
    try {
      var d = computeChildcareDistribution(SANITY_HIGHER, SANITY_LOWER, SANITY_NO_CC);
      return Math.round(d.share3c * 1000) === 877 &&
             Math.round(d.gross_share * 100) === 64 &&
             Math.round(d.net_share * 100) === 48;
    } catch (e) {
      if (window.console) console.error('calculator.js: distribution sanity check threw', e);
      return false;
    }
  }

  function sanityCheckPasses() {
    try {
      var noCc = computeWithFacts(SANITY_HIGHER, SANITY_LOWER, SANITY_NO_CC);
      var withCc = computeWithFacts(SANITY_HIGHER, SANITY_LOWER, SANITY_CC);
      return Math.round(noCc.order_wk) === 1013 && Math.round(withCc.order_wk) === 1276 &&
             distributionSanityPasses();
    } catch (e) {
      if (window.console) console.error('calculator.js: sanity check threw', e);
      return false;
    }
  }

  // The Change-2 toggle's OWN gate, separate from the main guard above: worked example, $300
  // lower-earner child care, fix on -> $1,206/wk (childcare_post_transfer.py's rule2b_7d). If this
  // fails, only the toggle disables (see initCalculator) -- the rest of the calculator keeps
  // working, per the brief: never show a wrong number, but don't take down the whole tool for one
  // figure either.
  function fixedRuleSanityPasses() {
    try {
      var f = computeFixedRuleOrder(SANITY_HIGHER, SANITY_LOWER, SANITY_CC);
      return Math.round(f.fixed_rule_order_wk) === 1206;
    } catch (e) {
      if (window.console) console.error('calculator.js: fixed-rule sanity check threw', e);
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
      el.className = 'tool-badge tool-badge--muted';
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
    var radios = Array.prototype.slice.call(root.querySelectorAll('[data-calc-radio]'));
    var allInputs = Object.keys(inputs).map(function (k) { return inputs[k]; });
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
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[data-calc-tab]'));
    var panels = {};
    Array.prototype.slice.call(root.querySelectorAll('[data-calc-panel]')).forEach(function (el) {
      panels[el.getAttribute('data-calc-panel')] = el;
    });

    if (!sanityCheckPasses()) {
      showUnavailable(root, allInputs, radios,
        Object.keys(cells).map(function (k) { return cells[k]; }),
        Object.keys(badges).map(function (k) { return badges[k]; }));
      return;
    }

    var activeTab = 'base';

    function outputFor(input) {
      return document.getElementById(input.id + '-output') || root.querySelector('output[for="' + input.id + '"]');
    }

    function setNote(key, text) {
      var el = notes[key];
      if (!el) return;
      if (text) { el.textContent = text; el.classList.add('visible'); }
      else { el.textContent = ' '; el.classList.remove('visible'); }
    }

    function setBadge(key, lit, litText, mutedText) {
      var el = badges[key];
      if (!el) return;
      el.textContent = lit ? litText : mutedText;
      el.className = 'tool-badge ' + (lit ? 'tool-badge--lit' : 'tool-badge--muted');
    }

    function currentFacts() {
      return {
        kids: Number(document.querySelector('[data-calc-radio="kids"]:checked').value),
        box: Number(document.querySelector('[data-calc-radio="box"]:checked').value),
        healthHigh: Number(inputs.healthHigh.value) || 0,
        healthLow: Number(inputs.healthLow.value) || 0,
        ccLower: inputs.ccLower ? Number(inputs.ccLower.value) || 0 : 0,
        ccHigher: inputs.ccHigher ? Number(inputs.ccHigher.value) || 0 : 0,
        ccFixOn: inputs.ccFix ? !!inputs.ccFix.checked : false
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
      if (out) out.textContent = money(higher);
      inputs.higher.setAttribute('aria-valuetext', 'Higher earner: ' + money(higher).replace('/yr', '') + ' a year');
      var outLo = outputFor(inputs.lower);
      if (outLo) outLo.textContent = money(lower);
      inputs.lower.setAttribute('aria-valuetext', 'Lower earner: ' + money(lower).replace('/yr', '') + ' a year');
    }

    function render() {
      var higherRaw = Number(inputs.higher.value);
      var lowerRaw = Number(inputs.lower.value);
      // Sliders are independent; normalise so labels stay honest regardless of which a reader
      // dragged past the other.
      var higher = Math.max(higherRaw, lowerRaw);
      var lower = Math.min(higherRaw, lowerRaw);
      renderIncomeOutputs(higher, lower);

      var facts = currentFacts();
      var noCcFacts = { kids: facts.kids, box: facts.box, healthHigh: facts.healthHigh, healthLow: facts.healthLow, ccLower: 0, ccHigher: 0 };
      var baseResult = computeWithFacts(higher, lower, noCcFacts);
      var ccResult = computeWithFacts(higher, lower, facts);

      // -- Child care tab: the always-visible pre/post-order distribution readout (Change 1). --
      var dist = computeChildcareDistribution(higher, lower, noCcFacts);
      if (cells.cc_dist_share3c) cells.cc_dist_share3c.textContent = pct1(dist.share3c);
      if (cells.cc_dist_gross) cells.cc_dist_gross.textContent = pct0(dist.gross_share);
      if (cells.cc_dist_net) cells.cc_dist_net.textContent = pct0(dist.net_share);

      if (inputs.ccLower) {
        var ccLowOut = outputFor(inputs.ccLower);
        if (ccLowOut) ccLowOut.textContent = moneyWk(facts.ccLower);
      }
      if (inputs.ccHigher) {
        var ccHighOut = outputFor(inputs.ccHigher);
        if (ccHighOut) ccHighOut.textContent = moneyWk(facts.ccHigher);
      }

      // -- Base support panel --
      if (cells.order_wk) cells.order_wk.textContent = moneyWk(baseResult.order_wk);
      if (cells.line_7e) cells.line_7e.textContent = pct1(baseResult.line_7e);
      if (cells.true_pct_net) {
        cells.true_pct_net.textContent = pct1(baseResult.true_pct_net);
        cells.true_pct_net.classList.toggle('is-warning', baseResult.true_pct_net >= 0.40);
      }
      if (cells.payor_after) cells.payor_after.textContent = money(baseResult.payor_after);
      if (cells.recip_after) {
        cells.recip_after.textContent = money(baseResult.recip_after);
        var baseAhead = baseResult.recip_after > baseResult.payor_after;
        cells.recip_after.classList.toggle('is-warning', baseAhead);
        setNote('recip_after', baseAhead ? 'Above the payor' : '');
      }
      if (cells.recip_per_person) cells.recip_per_person.textContent = money(baseResult.recip_per_person);

      // -- Child care panel --
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
      if (cells.cc_true_pct_net) {
        cells.cc_true_pct_net.textContent = pct1(ccResult.true_pct_net);
        cells.cc_true_pct_net.classList.toggle('is-warning', ccResult.true_pct_net >= 0.40);
      }
      if (cells.cc_payor_after) cells.cc_payor_after.textContent = money(ccResult.payor_after);
      if (cells.cc_recip_after) {
        cells.cc_recip_after.textContent = money(ccResult.recip_after);
        var ccAhead = ccResult.recip_after > ccResult.payor_after;
        cells.cc_recip_after.classList.toggle('is-warning', ccAhead);
        setNote('cc_recip_after', ccAhead ? 'Above the payor' : '');
      }
      if (cells.cc_recip_per_person) cells.cc_recip_per_person.textContent = money(ccResult.recip_per_person);

      // -- Child care tab: the "apply the proposed fix" toggle (Change 2). --
      if (inputs.ccFix) {
        if (fixedRuleSanityPasses()) {
          inputs.ccFix.disabled = false;
          setNote('cc_fix', '');
          var fixResult = computeFixedRuleOrder(higher, lower, facts);
          var showFix = facts.ccFixOn && (facts.ccLower > 0 || facts.ccHigher > 0);
          if (cells.cc_fix_order) cells.cc_fix_order.textContent = moneyWk(fixResult.fixed_rule_order_wk);
          if (cells.cc_fix_was) cells.cc_fix_was.textContent = moneyBare(ccResult.order_wk);
          if (cells.cc_fix_compare_wrap) cells.cc_fix_compare_wrap.classList.toggle('visible', showFix);
        } else {
          inputs.ccFix.disabled = true;
          inputs.ccFix.checked = false;
          if (cells.cc_fix_compare_wrap) cells.cc_fix_compare_wrap.classList.remove('visible');
          setNote('cc_fix', 'Proposed-fix figures unavailable.');
        }
      }

      // -- Status strip: reflects whichever tab is active. --
      var active = activeTab === 'childcare' ? ccResult : baseResult;
      setBadge('household', active.recip_after > active.payor_after,
        'Payee household ends up ahead', 'Payor ends up ahead');
      setBadge('hardship', active.true_pct_net >= 0.40,
        'Order above 40% of payor’s net (' + pct1(active.true_pct_net) + ')',
        'Order below 40% of payor’s net (' + pct1(active.true_pct_net) + ')');
    }

    function selectTab(name) {
      activeTab = name;
      tabs.forEach(function (btn) {
        var selected = btn.getAttribute('data-calc-tab') === name;
        btn.setAttribute('aria-selected', selected ? 'true' : 'false');
        btn.tabIndex = selected ? 0 : -1;
      });
      Object.keys(panels).forEach(function (key) {
        if (key === name) panels[key].removeAttribute('hidden');
        else panels[key].setAttribute('hidden', '');
      });
      render();
    }

    tabs.forEach(function (btn, i) {
      btn.addEventListener('click', function () { selectTab(btn.getAttribute('data-calc-tab')); });
      btn.addEventListener('keydown', function (e) {
        if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
        e.preventDefault();
        var next = e.key === 'ArrowRight' ? (i + 1) % tabs.length : (i - 1 + tabs.length) % tabs.length;
        tabs[next].focus();
        selectTab(tabs[next].getAttribute('data-calc-tab'));
      });
    });

    inputs.higher && inputs.higher.addEventListener('input', render);
    inputs.lower && inputs.lower.addEventListener('input', render);
    inputs.healthHigh && inputs.healthHigh.addEventListener('input', render);
    inputs.healthLow && inputs.healthLow.addEventListener('input', render);
    inputs.ccLower && inputs.ccLower.addEventListener('input', render);
    inputs.ccHigher && inputs.ccHigher.addEventListener('input', render);
    inputs.ccFix && inputs.ccFix.addEventListener('change', render);
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
  document.querySelectorAll('[data-calculator]').forEach(initCalculator);
})();
