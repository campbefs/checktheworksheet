// checktheworksheet.org — generic "slider(s) -> grid lookup -> readouts" engine.
// Vanilla JS, no dependencies, no CDN. Powers both interactive exhibits that share this shape
// (design brief §3.7): the home-page two-income calculator (two sliders, a 2-D grid) and the
// hardship-test child-care slider (one slider, a 1-D grid). One engine, so both tools behave
// identically and get fixed together if a bug turns up in one.
//
// NOTHING IS COMPUTED FREEHAND IN THE BROWSER. Every value shown is a row looked up (nearest
// match, snapped to the data's own grid) from a JSON file generated once, at build time, from the
// same CSV that produced the tool's static exhibit — see CONVENTIONS.md "Interactive exhibit
// data (CSV -> JSON)" for the conversion this expects and where the JSON files live.
//
// ---------------------------------------------------------------------------------------------
// MARKUP CONTRACT
// ---------------------------------------------------------------------------------------------
// <div class="tool" data-tool data-tool-src="/assets/data/valve-units-lag.json">
//   <div class="tool-slider-row">
//     <label for="childcare-slider">Child care claimed
//       <output id="childcare-slider-output" for="childcare-slider"></output>
//     </label>
//     <input type="range" id="childcare-slider" data-tool-input="childcare_wk"
//            data-tool-output-format="money-wk"                 (drives the paired <output>)
//            data-tool-valuetext="Child care claimed: {value} a week"
//            min="0" max="1290" step="10" value="300">
//   </div>
//   <div class="tool-readout" aria-live="polite">
//     <p class="cell-value" data-tool-cell="order_wk" data-tool-format="money-wk"></p>
//     <p class="cell-value" data-tool-cell="line_7e" data-tool-format="pct1"></p>
//   </div>
//   <p class="tool-flag" data-tool-flag data-tool-flag-rule="threshold"
//      data-tool-flag-key="order_pct_payor_net" data-tool-flag-op="gte" data-tool-flag-value="0.4"
//      data-tool-flag-text="The payor's true burden has already passed 40% of net income."></p>
// </div>
//
// - `data-tool-src`: path to the JSON grid (array of flat objects, one per row — the CSV's own
//   column names as keys).
// - `data-tool-input`: on each <input type="range">, the row-key it drives. One input = a 1-D
//   lookup; two or more (as on the calculator) = an N-D nearest-match lookup across all of them.
// - `data-tool-cell` / `data-tool-format`: on each readout element, which row-key to show and how
//   ("money-wk", "money-yr", "pct1" (one decimal, e.g. "33.4%"), "raw").
// - `data-tool-output-format` + a paired `<output for="...">`: same formats, for a slider's own
//   live value label.
// - `data-tool-valuetext`: a template with one `{value}` placeholder, formatted with
//   `data-tool-output-format`, set as the input's `aria-valuetext` on every change — a screen
//   reader hears a full sentence ("Higher earner: $200,000 a year"), never a bare number.
// - `data-tool-flag`: optional. See NO-JS FALLBACK note below — a page MUST also render the
//   worked-example baseline as static text/table so a no-JS visitor never sees a blank control.
//
// This script does not enable itself; a page opts in with
// `scripts: ["/assets/js/csv-slider.js"]` in its front matter (see CONVENTIONS.md).

(function () {
  'use strict';

  var FORMATTERS = {
    'money-wk': function (v) { return '$' + Math.round(v).toLocaleString('en-US') + '/wk'; },
    'money-yr': function (v) { return '$' + Math.round(v).toLocaleString('en-US') + '/yr'; },
    'money': function (v) { return '$' + Math.round(v).toLocaleString('en-US'); },
    'pct1': function (v) { return (v * 100).toFixed(1) + '%'; },
    'pct0': function (v) { return Math.round(v * 100) + '%'; },
    'raw': function (v) { return String(v); }
  };

  function format(key, value) {
    return (FORMATTERS[key] || FORMATTERS.raw)(value);
  }

  // Nearest-match lookup across one or more numeric keys. Grids in this project are dense/regular
  // (a full step grid, or a full cartesian product for two keys), so an exact match is the common
  // case; the nearest-neighbour fallback keeps a slider from ever landing on "no data" if a
  // future grid has a gap.
  function nearestRow(rows, targets) {
    var best = null, bestDist = Infinity;
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i], dist = 0, ok = true;
      for (var key in targets) {
        if (typeof row[key] !== 'number') { ok = false; break; }
        dist += Math.abs(row[key] - targets[key]);
      }
      if (ok && dist < bestDist) { bestDist = dist; best = row; }
    }
    return best;
  }

  function evalFlag(el, row) {
    var rule = el.getAttribute('data-tool-flag-rule');
    var text = el.getAttribute('data-tool-flag-text') || '';
    var show = false;

    if (rule === 'threshold') {
      var key = el.getAttribute('data-tool-flag-key');
      var op = el.getAttribute('data-tool-flag-op') || 'gte';
      var value = parseFloat(el.getAttribute('data-tool-flag-value'));
      var v = row[key];
      show = (op === 'gte') ? v >= value : (op === 'lte') ? v <= value : (op === 'gt') ? v > value : v < value;
    } else if (rule === 'divergence') {
      var keys = (el.getAttribute('data-tool-flag-keys') || '').split(',');
      var threshold = parseFloat(el.getAttribute('data-tool-flag-threshold'));
      if (keys.length === 2 && typeof row[keys[0]] === 'number' && typeof row[keys[1]] === 'number') {
        show = Math.abs(row[keys[0]] - row[keys[1]]) >= threshold;
      }
    }

    el.textContent = text;
    el.classList.toggle('visible', !!show);
  }

  function initTool(root) {
    var src = root.getAttribute('data-tool-src');
    if (!src) return;

    fetch(src).then(function (r) { return r.json(); }).then(function (rows) {
      var inputs = Array.prototype.slice.call(root.querySelectorAll('[data-tool-input]'));
      var cells = Array.prototype.slice.call(root.querySelectorAll('[data-tool-cell]'));
      var flags = Array.prototype.slice.call(root.querySelectorAll('[data-tool-flag]'));

      var render = function () {
        var targets = {};
        inputs.forEach(function (input) {
          targets[input.getAttribute('data-tool-input')] = Number(input.value);
        });
        var row = nearestRow(rows, targets);
        if (!row) return;

        cells.forEach(function (cell) {
          var key = cell.getAttribute('data-tool-cell');
          var fmt = cell.getAttribute('data-tool-format') || 'raw';
          if (typeof row[key] === 'number') cell.textContent = format(fmt, row[key]);
        });

        inputs.forEach(function (input) {
          var fmt = input.getAttribute('data-tool-output-format');
          var out = document.getElementById(input.getAttribute('list-output-for') || '') ||
                    root.querySelector('output[for="' + input.id + '"]');
          if (out && fmt) out.textContent = format(fmt, Number(input.value));

          var template = input.getAttribute('data-tool-valuetext');
          if (template && fmt) {
            input.setAttribute('aria-valuetext', template.replace('{value}', format(fmt, Number(input.value))));
          }
        });

        flags.forEach(function (el) { evalFlag(el, row); });
      };

      inputs.forEach(function (input) { input.addEventListener('input', render); });
      render();
    }).catch(function (err) {
      // Leave the page's own no-JS-fallback markup (a static table or precomputed baseline
      // values, per design brief §3.7) visible and untouched — this tool degrades to that, it
      // never shows a broken control.
      root.setAttribute('data-tool-load-failed', 'true');
      if (window.console) console.error('csv-slider.js: could not load', src, err);
    });
  }

  document.querySelectorAll('[data-tool]').forEach(initTool);
})();
