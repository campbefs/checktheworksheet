// checktheworksheet.org -- the fifty-jurisdiction table's jurisdiction finder (home page).
// Vanilla JS, no dependencies, no CDN. A separate control from sortable-table.js's filter input:
// this is a FINDER, not a filter -- it never hides a row. Choosing a jurisdiction highlights its
// row, scrolls it into view, and writes a one-line readout above the table comparing that
// jurisdiction's own two numbers (and its rank on each) against Massachusetts's.
//
// This tool does not compute anything -- it reads the numbers already rendered in
// <table id="fifty-table"> (the same 50 rows sortable-table.js sorts) and derives rank by sorting
// those numbers, client-side, from the table's own `data-sort-value` attributes. Single source of
// truth: the rendered table, same principle as sortable-table.js itself ("this script only
// reorders DOM rows already present, it does not fetch or invent data").
//
// Georgia is the 51st jurisdiction and has NO row in the table (held out -- see the page copy
// above the table): selecting it shows the held-out note instead of numbers, and clears any row
// highlight, since there is no row to point at.
//
// ---------------------------------------------------------------------------------------------
// MARKUP CONTRACT
// ---------------------------------------------------------------------------------------------
// <p class="jurisdiction-readout" id="jurisdiction-readout" aria-live="polite">
//   Massachusetts: $4,388/mo equal parenting (rank 1 of 50), $4,714/mo primary custody (rank 2 of 50).
// </p>
// <div class="table-finder">
//   <label for="jurisdiction-finder">Jump to a jurisdiction</label>
//   <select id="jurisdiction-finder" data-jurisdiction-finder
//           data-finder-table="fifty-table" data-finder-readout="jurisdiction-readout">
//     <option value="alabama">Alabama</option>
//     ...
//     <option value="massachusetts" selected>Massachusetts</option>
//     ...
//     <option value="georgia" data-held-out="true">Georgia (held out)</option>
//   </select>
// </div>
// <table class="exhibit-table" id="fifty-table" data-sortable> ... </table>
//
// - `<option value="...">` MUST equal the matching row's `data-filter-text` attribute exactly
//   (both already lowercase full names, e.g. "new york", "district of columbia") -- that is the
//   join key between the dropdown and the table. Georgia has no row and no `data-filter-text` to
//   match; mark its option with `data-held-out="true"` instead.
// - The readout's starting text is the no-JS fallback (design brief's own convention for
//   supplementary elements, matching calculator.js's `data-calc-flag`): a reader with JavaScript
//   off, or a page missing this script, still sees the correct default (Massachusetts's own two
//   numbers and ranks) as plain, real, static text. Only the ability to change it is lost.
// - Selecting a jurisdiction NEVER hides any other row -- this is a finder, not a filter (see
//   sortable-table.js's own filter input for that, a separate control). Only a highlight class
//   (`.is-selected-state`) and a scroll are applied.
// - Works with the existing sort: the highlight is a class on the `<tr>` itself, and
//   sortable-table.js only reappends existing `<tr>` elements when sorting (it does not recreate
//   them), so the highlight follows its row through any re-sort.
// - A page opts in with `scripts: ["/assets/js/jurisdiction-finder.js"]` (in addition to
//   `sortable-table.js`, which this script does not replace or require to be loaded first --
//   the two are independent listeners on the same table).

(function () {
  'use strict';

  function moneyMo(v) { return '$' + Math.round(v).toLocaleString('en-US') + '/mo'; }

  function rankInfo(rows, key) {
    // rows: array of {name, s1, s2, tr}. Returns { byName: { name: {rank, total} } } for `key`.
    var sorted = rows.slice().sort(function (a, b) { return b[key] - a[key]; });
    var out = {};
    sorted.forEach(function (r, i) { out[r.name] = { rank: i + 1, total: sorted.length }; });
    return out;
  }

  function initFinder(select) {
    var tableId = select.getAttribute('data-finder-table');
    var readoutId = select.getAttribute('data-finder-readout');
    var table = document.getElementById(tableId);
    var readout = document.getElementById(readoutId);
    if (!table) return;
    var tbody = table.querySelector('tbody');

    function readRows() {
      return Array.prototype.slice.call(tbody.querySelectorAll('tr')).map(function (tr) {
        var name = tr.getAttribute('data-filter-text') || (tr.cells[0] ? tr.cells[0].textContent.trim().toLowerCase() : '');
        var s1 = parseFloat(tr.cells[1].getAttribute('data-sort-value'));
        var s2 = parseFloat(tr.cells[2].getAttribute('data-sort-value'));
        return { name: name, label: tr.cells[0] ? tr.cells[0].textContent.replace(/[†‡]/g, '').trim() : name, s1: s1, s2: s2, tr: tr };
      });
    }

    function clearHighlight() {
      Array.prototype.slice.call(tbody.querySelectorAll('tr.is-selected-state')).forEach(function (tr) {
        tr.classList.remove('is-selected-state');
      });
    }

    function render(userAction) {
      var value = select.value;
      var heldOut = select.selectedOptions && select.selectedOptions[0] &&
        select.selectedOptions[0].getAttribute('data-held-out') === 'true';
      var rows = readRows();

      if (heldOut) {
        clearHighlight();
        if (readout) {
          readout.textContent = 'Georgia is held out: its enacted formula orders less at equal ' +
            'parenting time than at primary custody, so it has no row in this comparison.';
        }
        return;
      }

      var found = null;
      for (var i = 0; i < rows.length; i++) {
        if (rows[i].name === value) { found = rows[i]; break; }
      }
      if (!found) return; // markup/data mismatch -- fail safe, leave the previous readout in place

      var byS1 = rankInfo(rows, 's1');
      var byS2 = rankInfo(rows, 's2');
      var ma = null;
      for (var j = 0; j < rows.length; j++) { if (rows[j].name === 'massachusetts') { ma = rows[j]; break; } }

      clearHighlight();
      found.tr.classList.add('is-selected-state');
      if (userAction && found.tr.scrollIntoView) {
        found.tr.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }

      if (readout) {
        var r1 = byS1[found.name], r2 = byS2[found.name];
        var text;
        if (found.name === 'massachusetts') {
          text = 'Massachusetts: ' + moneyMo(found.s1) + ' equal parenting (rank ' + r1.rank +
            ' of ' + r1.total + '), ' + moneyMo(found.s2) + ' primary custody (rank ' + r2.rank +
            ' of ' + r2.total + ').';
        } else if (ma) {
          var maR1 = byS1['massachusetts'], maR2 = byS2['massachusetts'];
          text = found.label + ': ' + moneyMo(found.s1) + ' equal parenting (rank ' + r1.rank +
            ' of ' + r1.total + '), ' + moneyMo(found.s2) + ' primary custody (rank ' + r2.rank +
            ' of ' + r2.total + ') — Massachusetts: ' + moneyMo(ma.s1) + ' (rank ' + maR1.rank +
            '), ' + moneyMo(ma.s2) + ' (rank ' + maR2.rank + ').';
        } else {
          text = found.label + ': ' + moneyMo(found.s1) + ' equal parenting (rank ' + r1.rank +
            ' of ' + r1.total + '), ' + moneyMo(found.s2) + ' primary custody (rank ' + r2.rank +
            ' of ' + r2.total + ').';
        }
        readout.textContent = text;
      }
    }

    select.addEventListener('change', function () { render(true); });
    // Reflect the markup's own preselected option (Massachusetts) without scrolling on load --
    // the readout's static starting text already matches this, so this is a no-op unless the
    // browser restored a different selection (e.g. back/forward cache).
    render(false);
  }

  document.querySelectorAll('[data-jurisdiction-finder]').forEach(initFinder);
})();
