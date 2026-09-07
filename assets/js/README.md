# `assets/js/` — interactive components

Everything a page needs to mount one of this site's four interactive tools, in one place. Each
tool's own file carries the same information as a header comment; this file exists so a page
author does not have to open four files to find it. **Read `CONVENTIONS.md` first** — it is the
overall contract for content pages (front matter, layouts, CSS class vocabulary); this file only
covers the JS/data layer underneath it.

Every script here is vanilla ES5, no build step, no CDN, no framework. A page opts into a script
with `scripts: [...]` in its front matter (see `CONVENTIONS.md` §4); `site.js` loads on every
page regardless and needs no opt-in.

## What's in this folder

```
assets/js/
  site.js                  -- always loaded (progress bar, chapter rail, nav toggle)
  csv-slider.js             -- generic "slider(s) -> grid lookup -> readouts" engine
                                (child-care valve slider, credit-collapse slider)
  sortable-table.js         -- generic sortable/filterable <table> engine (fifty-jurisdiction table)
  lightbox.js                -- exhibits-gallery lightbox
  calculator.js              -- the home-page two-income calculator (COMPUTES, does not look up)
  calculator.test.js         -- node assets/js/calculator.test.js -- fidelity tests, run this
                                before trusting any number the calculator shows
  lib/
    worksheet.js              -- ported model/worksheet.py (CJ-D 304)
    net-position.js           -- ported model/net_position.py (TY2026 tax model)
assets/data/
  valve-units-lag.json          -- figures/working/fig6_valve_units_lag.csv (130 rows)
  heatmap-3child-box1.json      -- figures/working/fig1_heatmap_3child_box1.csv (1,147 rows)
  parenting-time-credit.json    -- figures/working/fig3_credit_collapse.csv (75 rows)
  states-fifty-jurisdictions.json -- data/fifty-state/tier-50-2026-09-05.json (50 rows)
```

All four JSON files are flat arrays of objects, keys = the source CSV's/JSON's own column names,
generated once and checked in (there is no build-time conversion step in this Jekyll route — see
`CONVENTIONS.md` §10). If a source file is ever updated, regenerate the matching JSON by hand and
recommit it; nothing regenerates these automatically.

---

## 1. The two-income calculator (home page)

**This is the one tool on the site that computes rather than looks up a precomputed grid.** The
design brief's original spec called for a $5,000-step lookup grid
(`heatmap-3child-box1.json`, still generated and present, see note below); it cannot reproduce the
worked example ($201,000 / $29,640) to the dollar, and the project's own rule is that no number
ships unless it's tested against the Python it came from. So this tool instead ports
`model/worksheet.py` and `model/net_position.py` into `lib/worksheet.js` / `lib/net-position.js`
and computes the real answer for any two incomes, at any dollar value, not just the grid's steps.

**Run the test before trusting this tool**, and after any change to either `lib/` file:

```
node assets/js/calculator.test.js
```

38 checks: all six fact patterns from `model/runs/official-xfa-vs-model-2026-09-05.txt` (the
Commonwealth's own CJ-D 304 XFA calculate-scripts), both in "round every line" mode (matches the
official scripts to the dollar on all six) and in the default unrounded mode (matches
`model/worksheet.py`'s own output to six decimal places — this is what the letter, the paper and
this site's own copy quote); plus the worked example's tax position from
`model/runs/submission-figures-run-2026-09-05.txt` to the cent. **All 38 pass as of 2026-09-06.**
If you change either `lib/` file and a check fails, the port has diverged from the Python — fix
the port, never the test.

### Markup a page must contain

```html
<div class="tool tool-two-up" data-calculator>
  <div class="tool-slider-row">
    <label for="calc-higher">Higher earner, gross per year
      <output id="calc-higher-output" for="calc-higher">$201,000/yr</output>
    </label>
    <input type="range" id="calc-higher" data-calc-input="higher"
           min="60000" max="300000" step="1000" value="201000">
  </div>
  <div class="tool-slider-row">
    <label for="calc-lower">Lower earner, gross per year
      <output id="calc-lower-output" for="calc-lower">$29,640/yr</output>
    </label>
    <input type="range" id="calc-lower" data-calc-input="lower"
           min="0" max="120000" step="1000" value="29640">
  </div>
  <div class="tool-readout" aria-live="polite">
    <div>
      <p class="cell-label">Weekly order (Line 7d)</p>
      <p class="cell-value" data-calc-cell="order_wk">$1,013/wk</p>
    </div>
    <div>
      <p class="cell-label">Line 7e's reading</p>
      <p class="cell-value payor-line" data-calc-cell="line_7e">26.5%</p>
    </div>
    <div>
      <p class="cell-label">True share of the payor's net income</p>
      <p class="cell-value true-burden" data-calc-cell="true_pct_net">37.7%</p>
    </div>
  </div>
  <p class="tool-flag" data-calc-flag>&nbsp;</p>
  <p>Three children, no child care, Box 1 (shared parenting), health premiums $33/$43 a week,
    the worked example's own facts, held fixed. Method:
    <a href="/model/worksheet.py"><code>model/worksheet.py</code></a> and
    <a href="/model/net_position.py"><code>model/net_position.py</code></a>, ported and tested in
    <a href="/assets/js/lib/worksheet.js"><code>assets/js/lib/worksheet.js</code></a> and
    <a href="/assets/js/calculator.test.js"><code>assets/js/calculator.test.js</code></a>.</p>
</div>
```

(No new CSS class is introduced by this pass. `.check-yourself`/`.ask` exist in
`assets/css/site.css` but are built for a whole section with an `<h2>` and a link grid — the
method line above is one plain paragraph inside `.tool` and needs no special class; a page
author who wants the full check-yourself treatment should put it in its own section outside the
tool, per `CONVENTIONS.md` §7, not force it onto this one line.)

Front matter: `scripts: ["/assets/js/lib/worksheet.js", "/assets/js/lib/net-position.js", "/assets/js/calculator.js"]`
— **in that order**; `calculator.js` reads `window.MCSGWorksheet` / `window.MCSGNetPosition` and
does nothing if either is missing (fails safe onto the static markup below, see next point).

**No-JS / load-failure fallback is REQUIRED and is not automatic**: the three `data-calc-cell`
spans and the two sliders' `value` attributes must already contain the real worked-example numbers
exactly as written above ($1,013/wk, 26.5%, 37.7%, $201,000/yr, $29,640/yr) — copy them verbatim,
they are tested. A reader with JavaScript off, or whose browser fails to load one of the two
`lib/` scripts, sees the worked example stated correctly and only loses the ability to change it.

**Fixed facts, not sliders** (per the design brief's word budget — two income inputs only): three
children, no child care, Box 1 (shared parenting), health premiums $33/wk to whichever slider is
currently lower and $43/wk to whichever is currently higher (matches the convention already used
by every heatmap exhibit in this project, `model/charts/_common.py`'s `order()`). The two sliders
are independent controls; if a reader drags "lower" past "higher" the script silently swaps which
value plays which role so the labels stay honest — it does not clamp or block the drag.

**`heatmap-3child-box1.json` is not used by this tool** and is not dead weight to remove — it is
the CSV `figures/working/fig1_heatmap_3child_box1.csv` already committed to the repo and cited
elsewhere (e.g. exhibits E01/E02/E04 are drawn from its 1/2-child siblings), converted to JSON
in case a future page wants a client-side grid lookup (a hover tooltip over the static heatmap
exhibit, for instance). Converted and checked in now so the conversion doesn't have to happen
twice; not wired to any control.

---

## 2. The child-care valve slider (hardship-test finding page)

Already fully built by `csv-slider.js` (a generic engine — read that file's own header comment
for the complete markup contract and every `data-tool-*` attribute it reads). Data file:
`valve-units-lag.json`. No-JS fallback: the shipped site's existing five-row table, in a
`<noscript>` block (design brief §3.7 item 2) — this script only enhances it, it does not
replace it.

Static-exhibit pairing: `figures/exhibits/E05-what-line-7e-sees-vs-true-burden-worked-example.png`.

---

## 3. The parenting-time credit-collapse tool (parenting-time finding page)

**Built on the same `csv-slider.js` engine as the valve slider — no new script, no vendored
charting library.** The design brief (§3.7 item 4) specified Observable Plot for this exhibit,
chosen for built-in per-mark ARIA labels on an SVG curve with a moving marker. That was not
built: vendoring, licensing and testing a 69KB third-party library for one exhibit was not
justified once a plain native-range-input slider (identical in kind to the valve slider, already
tested, already accessible with zero additional ARIA work because there is no SVG mark to label)
delivers the same reader-facing fact — the credit percentage at a given income disparity — from
the same CSV. **What's given up: the moving marker on a visible curve.** What's kept: every
number the brief's spec cared about, native keyboard support, and no new dependency. Flagged here
so a reviewer can decide this was the right trade, not discover it by accident.

Data file: `parenting-time-credit.json` (from `figures/working/fig3_credit_collapse.csv`, 75
rows spanning the lower earner's income from $2,000 to $150,000/yr against a fixed higher
earner, at which the payor's income share of the combined household, `payor_3c`, ranges
57.3%–99.9%). Markup:

```html
<div class="tool" data-tool data-tool-src="/assets/data/parenting-time-credit.json">
  <div class="tool-slider-row">
    <label for="credit-slider">Payor's share of the combined household income
      <output id="credit-slider-output" for="credit-slider"></output>
    </label>
    <input type="range" id="credit-slider" data-tool-input="payor_3c"
           data-tool-output-format="pct0"
           data-tool-valuetext="Payor holds {value} of the combined household income"
           min="0.573" max="0.999" step="0.001" value="0.877">
  </div>
  <div class="tool-readout" aria-live="polite">
    <div>
      <p class="cell-label">Box 2 order (primary custody)</p>
      <p class="cell-value" data-tool-cell="box2_7d" data-tool-format="money-wk"></p>
    </div>
    <div>
      <p class="cell-label">Box 1 order (shared parenting)</p>
      <p class="cell-value" data-tool-cell="box1_7d" data-tool-format="money-wk"></p>
    </div>
    <div>
      <p class="cell-label">The shared-parenting credit</p>
      <p class="cell-value true-burden" data-tool-cell="reduction_current" data-tool-format="pct1"></p>
    </div>
  </div>
</div>
```

Default `value="0.877"` is the worked example's own payor income share (87.7%), where
`reduction_current` = 6.9% — matches `model/runs/submission-figures-run-2026-09-05.txt`'s
"SECTION 5" table row `87.7% 1,088 1,013 6.9%`. Front matter:
`scripts: ["/assets/js/csv-slider.js"]` (same file as the valve slider — a page using both tools
loads it once). No-JS fallback: render the "SECTION 5" table from the same run file as a plain
Markdown table (it already exists as prose in the project's documents; this is not new content to
write, only to place before the slider).

Static-exhibit pairing:
`figures/exhibits/E08-credit-shrinks-as-gap-widens-3-children.png` (and E09, the implied-
overnight-share companion).

---

## 4. The fifty-jurisdiction sortable, searchable table (home page + its finding page)

Already fully built by `sortable-table.js` (generic engine — read that file's own header comment
for the complete markup contract: `<button data-sort-key="...">` headers with `aria-sort`, an
optional `<input data-table-filter="...">`). **This script does not fetch or render the table —
it only reorders `<tr>` elements already in the DOM** (design brief's own requirement: the table
must be complete and correctly pre-sorted with no JS at all). A page author renders the 50 rows
as real HTML, from `states-fifty-jurisdictions.json` (or straight from
`data/fifty-state/tier-50-2026-09-05.json`, which this file is a byte-for-byte copy of plus one
derived field), sorted descending by `s1` to match the brief's stated no-JS default order.

Each row needs: the jurisdiction name; `s1` (equal-parenting order) and `s2` (primary-custody
order), both shown — this project's finding is specifically about the GAP between a
jurisdiction's own two numbers, so a table that only showed one would misrepresent it; and, for
Massachusetts only, the `is_reader_state`/`.is-reader-state` class so it stays visually pinned
regardless of sort order (`is_massachusetts: true` in the JSON marks which row). Numeric columns
need `data-sort-value` set to the raw number (see `sortable-table.js`'s own comment for why:
`$4,388/mo` as text would sort lexicographically, not numerically).

```html
<table class="exhibit-table" id="fifty-table" data-sortable>
  <thead>
    <tr>
      <th><button data-sort-key="state" aria-sort="none">Jurisdiction</button></th>
      <th class="numeric"><button data-sort-key="s1" data-sort-type="number" aria-sort="descending">Equal parenting (S1)</button></th>
      <th class="numeric"><button data-sort-key="s2" data-sort-type="number" aria-sort="none">Primary custody (S2)</button></th>
    </tr>
  </thead>
  <tbody>
    <tr class="is-reader-state" data-filter-text="massachusetts">
      <td>Massachusetts</td>
      <td class="numeric" data-sort-value="4388.48">$4,388/mo</td>
      <td class="numeric" data-sort-value="4714.22">$4,714/mo</td>
    </tr>
    <!-- ... 49 more rows, from states-fifty-jurisdictions.json, s1 descending ... -->
  </tbody>
</table>
<label for="jurisdiction-filter">Filter by jurisdiction</label>
<input type="text" id="jurisdiction-filter" data-table-filter="fifty-table" aria-controls="fifty-table">
```

Front matter: `scripts: ["/assets/js/sortable-table.js"]`. **Tiering caveat is a page-copy
responsibility, not this script's** — per `CONVENTIONS.md`/the exhibit direction, this is a
single-fact-pattern, tiered comparison (see `data/fifty-state/tier-50-2026-09-05.json`'s own
per-row `note` field, present on Hawaii, for the one row needing one) and the surrounding prose
must say so; the table itself carries no confidence styling.

Static-exhibit pairing (the lead exhibit pair per the 2026-09-06 exhibit direction):
`figures/exhibits/E12-fifty-states-lower-earner-primary-one-fact-pattern.png` then
`figures/exhibits/E17-ma-equal-time-vs-others-primary-custody.png`.

---

## 5. The exhibits-gallery lightbox

Already fully built by `lightbox.js` — read that file's own header comment for the complete
markup contract. Not data-driven; no `assets/data/*.json` file involved.

---

## Read-back done on this pass

- `node assets/js/calculator.test.js` — 38/38 checks pass (see file for what each one proves).
- Every `assets/data/*.json` file spot-checked against its source CSV/JSON's first and last rows
  and against figures already quoted in `context/MEMORY.md` (Massachusetts $4,388.48/$4,714.22;
  the worked example's $1,012.7257303613252 unrounded 7d; the 87.7%-income-share row's 6.9%
  credit).
- No em dash in any reader-visible string this pass added (`calculator.js`'s flag text); the
  pre-existing em dashes in every file's own code comments are not reader-visible prose and were
  left as the foundation pass wrote them.
- Every script here is self-contained ES5 with no absolute local file path.
