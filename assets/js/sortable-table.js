// checktheworksheet.org — generic sortable/filterable table engine.
// Vanilla JS, no dependencies, no CDN. Built for the fifty-jurisdiction comparison (design brief
// §3.7.3) but not specific to it — any `<table data-sortable>` on the site gets the same
// behaviour. Plain HTML table, JS sort, in the ProPublica Nonprofit Explorer pattern the brief
// names: no framework, and the table is a complete, correct, pre-sorted document with no JS at
// all (this script only reorders DOM nodes already present).
//
// ---------------------------------------------------------------------------------------------
// MARKUP CONTRACT
// ---------------------------------------------------------------------------------------------
// <table class="exhibit-table" id="fifty-table" data-sortable>
//   <thead>
//     <tr>
//       <th><button data-sort-key="state" aria-sort="none">Jurisdiction</button></th>
//       <th class="numeric">
//         <button data-sort-key="s1" data-sort-type="number" aria-sort="descending">S1 (equal parenting)</button>
//       </th>
//     </tr>
//   </thead>
//   <tbody>
//     <tr class="is-reader-state" data-filter-text="massachusetts">
//       <td>Massachusetts</td>
//       <td class="numeric" data-sort-value="4388.48">$4,388/mo</td>
//     </tr>
//     ...
//   </tbody>
// </table>
//
// - Exactly one `<button>` may carry `aria-sort="ascending"` or `"descending"` at a time — that is
//   the table's pre-sorted state, written by hand to match the no-JS order the page ships. This
//   script reads that starting state, it does not assume descending-by-default.
// - `data-sort-type="number"`: sort numerically (parsing `data-sort-value`, falling back to the
//   cell's own text with non-digit characters stripped). Omit for a plain string column.
// - `data-filter-text` (optional, on `<tr>`): what the filter input matches against, lowercased.
//   Falls back to the row's first cell text if absent.
//
// A page enables the filter input separately:
//   <input type="text" id="jurisdiction-filter" data-table-filter="fifty-table"
//          aria-controls="fifty-table">
// with its own visible <label for="jurisdiction-filter"> (design brief §3.7.3).
//
// A page opts into this file with `scripts: ["/assets/js/sortable-table.js"]` in front matter.

(function () {
  'use strict';

  function cellSortValue(td, type) {
    var explicit = td.getAttribute('data-sort-value');
    if (type === 'number') {
      var n = explicit !== null ? parseFloat(explicit) : parseFloat((td.textContent || '').replace(/[^0-9.-]/g, ''));
      return isNaN(n) ? -Infinity : n;
    }
    return (explicit !== null ? explicit : td.textContent || '').trim().toLowerCase();
  }

  function initTable(table) {
    var headers = Array.prototype.slice.call(table.querySelectorAll('thead button[data-sort-key]'));
    var tbody = table.querySelector('tbody');

    headers.forEach(function (btn, colIndex) {
      btn.addEventListener('click', function () {
        var current = btn.getAttribute('aria-sort');
        var next = current === 'descending' ? 'ascending' : 'descending';
        headers.forEach(function (b) { b.setAttribute('aria-sort', 'none'); });
        btn.setAttribute('aria-sort', next);

        var type = btn.getAttribute('data-sort-type');
        var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
        rows.sort(function (a, b) {
          var av = cellSortValue(a.cells[colIndex], type);
          var bv = cellSortValue(b.cells[colIndex], type);
          if (av < bv) return next === 'ascending' ? -1 : 1;
          if (av > bv) return next === 'ascending' ? 1 : -1;
          return 0;
        });
        rows.forEach(function (row) { tbody.appendChild(row); });
      });
    });
  }

  function initFilter(input) {
    var table = document.getElementById(input.getAttribute('data-table-filter'));
    if (!table) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));

    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      rows.forEach(function (row) {
        var text = row.getAttribute('data-filter-text') || (row.cells[0] ? row.cells[0].textContent : '');
        row.hidden = q.length > 0 && text.toLowerCase().indexOf(q) === -1;
      });
    });
  }

  document.querySelectorAll('table[data-sortable]').forEach(initTable);
  document.querySelectorAll('[data-table-filter]').forEach(initFilter);
})();
