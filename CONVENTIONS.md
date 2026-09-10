# Site conventions — checktheworksheet.org (2026-09-06 redesign, "Paper & Claret")

For every agent writing a content page in this repository. Follow this file exactly; it is written
so you do not have to ask. It documents the foundation built in `_config.yml`, `_layouts/`,
`_includes/`, `assets/css/site.css`, and `assets/js/`. **Do not edit those files** without updating
this one to match — they are what every content page depends on.

**Source of truth for the design itself:** `2026-09-06-DESIGN-BRIEF.md` in the private research
repo (`docs/research/website/redesign/`), and the owner's exhibit direction,
`docs/plans/2026-09-06-exhibit-direction.md`, which overrides the brief where they differ (the
exhibit set is now single-chart-per-file, and the lead exhibit is the cross-state pair E12/E17).
This file is the local, buildable application of both — it does not restate their reasoning, and
where this file and the brief disagree, re-read the brief; this file may be behind it.

Required skills before writing a page: `web-design-system`, `web-page-anatomy`, `web-figures`,
`web-static-build`, `write-natural`. **Where the design brief departs from a skill's default
(JavaScript, layout width, a persistent sidebar), the brief wins** — this is true for the
interactive exhibits (§3.7) and the sortable table (web-figures says "never JS for a table
filter/sort"; the brief specifically wants it here, with a no-JS fallback that is a complete
table).

---

## 0. What changed in this pass, and what did not

This pass rebuilt the **foundation only**: `_config.yml`, all four layouts, all five includes,
`assets/css/site.css`, `assets/js/*.js`, and this file. It did **not** write any content page.
Two things follow from that:

1. **The header/footer nav point at pages that don't exist yet.** Per the brief's file list
   (§3.12), the top bar and footer link to `/findings/`, `/findings/fifty-jurisdictions.html`,
   `/documents.html`, `/exhibits.html`, `/about.html` — the **new**, flat-`.html` URLs. The
   **old** content (see below) still lives at `/documents/`, `/exhibits/`, `/about/`,
   `/findings/fifty-one-jurisdictions/`. Until the new pages are written, those nav links 404.
   This is expected mid-migration, not a foundation defect — confirmed by building the site
   locally and diffing every internal link against the built output (see §9).
2. **Old content pages still render, unchanged, through the new layouts** (`findings/child-care.md`,
   `findings/hardship-test.md`, `findings/parenting-time/index.md`,
   `findings/fifty-one-jurisdictions/index.md`, `exhibits/index.md`, `documents/index.md`,
   `the-model/index.md`, `the-data/index.md`, `about/index.md`, `sitemap/index.md`) because
   `layout: page` / `layout: finding` still resolve, and the classes they use
   (`.doc-list`, `.finding-list`, `.exhibit`/`.exhibit-facts`, `.stat-callout`, `.table-scroll`,
   `.visually-hidden`, `.ask`, `.disclosure`) are all still defined in `site.css` for exactly this
   reason. **They are old-design pages, not yet migrated to the brief's pattern** (no numeral
   pair, no `sections:`-driven rail, no interactive exhibit, some at the wrong URL for the brief's
   file list). Whoever writes `index.html` and the four `findings/*.html` pages per §3.12 should
   treat these as source material to rewrite into the new pattern, not as finished pages to leave
   standing at two URLs. **`index.md` at the repo root has no front matter at all** — Jekyll
   copies it byte-for-byte to `/index.md` rather than converting it, so **there is currently no
   working homepage at `/`** until an `index.html` with `layout: home` front matter replaces it
   (per the hard rule against destroying content, `index.md`'s prose has not been touched or
   deleted here — read it for material worth carrying into the new hero/disclosure/finding-card
   copy before it is superseded).

---

## 1. Build route

Route (a) from `web-static-build`: plain Jekyll, no theme, hand-written CSS, GitHub's default
runner builds on every push. `_config.yml` carries no `theme:`/`remote_theme:` key — one was
briefly and accidentally reintroduced on this branch (a commit reduced the whole file to
`theme: minima`); if you ever see a `theme:` key here again, something regressed, restore this
file's structure instead of building on top of it.

**Local build confirmed working, with a caveat.** `Gemfile` (repo root) does **not** use the full
`github-pages` meta-gem — on this machine's Ruby (system 2.6.10, no rbenv/rvm/asdf, so no newer
Ruby available), `github-pages ~> 232` cannot resolve: it hard-depends on `nokogiri >= 1.16.2`,
which itself requires Ruby `>= 3.0`. The `Gemfile` instead pins the individual gems this site
actually uses (`jekyll 3.10.0`, `jekyll-seo-tag`, `jekyll-sitemap`, plus `kramdown-parser-gfm`,
and version-pinned `ffi`/`webrick` to keep the transitive chain on Ruby 2.6), which is the exact
toolchain `web-static-build` says GitHub Pages itself runs. **GitHub Pages' own build is
unaffected by any of this** — it always uses the real meta-gem in GitHub's own environment; this
substitution is local-only, to make `bundle exec jekyll build` possible on this machine. If a
newer local Ruby (>=3.0, <3.2) ever becomes available, switch back to the full `github-pages`
gem — the comment at the top of `Gemfile` has the exact commands.

```
bundle config path vendor/bundle   # NOT `bundle config set --local path ...` — this Bundler
                                    # (1.17.2) doesn't have the `set`/`--local` subcommand syntax;
                                    # `bundle config path vendor/bundle` is the equivalent
BUNDLE_PATH=vendor/bundle bundle install
BUNDLE_PATH=vendor/bundle bundle exec jekyll build
```

`vendor/`, `_site/`, `.bundle/`, and `Gemfile.lock` are gitignored — never commit them.

`html-proofer` was **not** installed (it pulls in the same nokogiri floor). In its place, a plain
Python link-checker was run against the built `_site/` (grep every `href`/`src` starting with `/`,
confirm the target file exists) — 294 internal links checked; the only misses were the expected
not-yet-built pages in §0. Re-run something equivalent after adding content pages; do not assume
GitHub's own build catching a 404 is good enough, since Jekyll's build succeeds even with a dead
link (Jekyll doesn't check them; only `htmlproofer` does).

---

## 2. Frozen paths — never touch

`model/`, `data/`, `figures/`, `paper/` are frozen: their exact paths are cited in a working paper
and in letters already sent. Never delete, move, or rename anything inside them — including the
retired multi-panel exhibits (`E03`/`E07`/`E14`/`E15`), which the exhibit-direction pass already
moved to `figures/exhibits/_retired-2026-09-06-multi-panel/` rather than deleting. **Never
reference E03/E07/E14/E15 from any new page** — the live exhibit set is E01, E02, E04, E05, E06,
E08, E09, E10, E11, E12, E13, E16, E17, E18–E27 (23 files; see
`figures/exhibits/README.md` for exactly which working CSV/script drew each one). New content
pages link to files at their existing paths (e.g. `/figures/exhibits/E05-....png`,
`/model/worksheet.py`) and never assume a different location.

---

## 3. URLs — this design uses flat `.html` files, not the old `<name>/index.md` folders

The brief's file list (§3.12) is authoritative:

```
index.html                          — home page
findings/hardship-test.html         — finding page 1
findings/child-care.html            — finding page 2
findings/parenting-time.html        — finding page 3
findings/fifty-jurisdictions.html   — finding page 4 (the full table + method lives HERE —
                                       do not also build comparison.html; §3.12 explicitly
                                       says pick one, and folding it into the finding page
                                       is the choice this repo has made)
findings/index.html                 — findings index
exhibits.html                       — gallery of all 23 exhibits + lightbox
documents.html                      — working paper PDF, Attachment E, document list
about.html                          — method, disclosure, test suite pointer
```

A page in this scheme has a clean URL by its filename directly (`documents.html` → `/documents.html`),
**not** by the old `<name>/index.md` folder convention. Jekyll serves both `.md` and `.html` files
with front matter through the same layout system — pick `.html` for a page whose body is mostly
hand-written markup (interactive exhibits, tables with ARIA attributes, the numeral pair) where
fighting kramdown would cost more than it saves, and reserve `.md` for prose-only sections inside a
larger page. **This is a deliberate change from the previous design's folder-per-page convention**
(`findings/child-care.md` at the top level, `findings/parenting-time/index.md` as a folder — the
previous pass was inconsistent about this even within itself). Do not create a new page using the
old folder-with-`index.md` pattern; do not build both a flat file and a folder for the same page.

`/sitemap/` (`sitemap/index.md`) is unchanged and still required — see §8.

---

## 4. Layouts

| Layout | File | For | Adds over `default` |
|---|---|---|---|
| `default` | `_layouts/default.html` | Never set directly on a content page | `<head>` (`{% seo %}`, stylesheet, viewport), skip link, reading-progress bar, header include, `<main id="main">`, footer include, the `site.js` script tag (always) and a `page.scripts` loop (opt-in, per page) |
| `home` | `_layouts/home.html` | `index.html` only | A `.home` wrapper `<div>` for CSS scoping. No persistent sidebar (brief §3.3) — the hero, disclosure, calculator, finding cards, and fifty-jurisdiction table are all written directly in `index.html`'s own body |
| `finding` | `_layouts/finding.html` | The four finding pages | An `<article class="finding">` wrapper. The page's own body supplies, in order, the disclosure → eyebrow/headline/numeral-pair → mechanism paragraph → interactive exhibit → static exhibit → two standing caveats → check-it-yourself (brief §3.6) |
| `page` | `_layouts/page.html` | `findings/index.html`, `findings/fifty-jurisdictions.html`, `exhibits.html`, `documents.html`, `about.html`, and every not-yet-migrated old page | An `<article class="page">` wrapper. No chapter rail by default — opt in with the same `.page-shell` markup a finding page uses (§5) if the page is long enough to want one |

All three non-`default` layouts set `layout: default` in their own front matter — Jekyll chains
them, so a content file only ever sets `layout: home` / `finding` / `page`, never `layout: default`.

**Do not auto-generate an H1 from `page.title` in a layout.** Every content page writes its own
`<h1>` — a complete-sentence assertion (web-page-anatomy) — as the first real content in its body.
A layout that also prints `page.title` as a heading duplicates it.

**Front-matter contract, common keys:**

| Key | Used by | Notes |
|---|---|---|
| `layout` | every page | `home` \| `finding` \| `page` |
| `title` | every page | `<title>` tag and OG/meta via jekyll-seo-tag |
| `description` | every page | Meta description via jekyll-seo-tag. One or two sentences |
| `permalink` | optional | Only if the flat-filename URL isn't already what you want |
| `disclosure` | home + finding pages | Array of paragraph strings (may contain inline HTML) — see §6 |
| `rail_label`, `rail_aria_label`, `sections` | finding pages, optionally other long pages | Drives `_includes/chapter-rail.html` — see §5 |
| `scripts` | any page using an interactive exhibit | Array of root-relative paths, e.g. `["/assets/js/csv-slider.js"]` — appended after `site.js`, which every page already loads |
| `body_class` | rarely, hand-set | Already set by `home`/`finding` layouts; only override for a genuinely new page archetype |

---

## 5. The chapter rail — data source and exact markup

`_includes/chapter-rail.html` renders from **front matter**, not from a scan of the rendered
headings (this is plain Jekyll, no plugin does that here). Set `sections:` on the content page to
match its own `<h2 id="...">` elements exactly:

```yaml
---
layout: finding
rail_label: "On this page"                 # optional, defaults to this
rail_aria_label: "Sections of this page"   # optional, defaults to this
sections:
  - id: mechanism
    label: "The mechanism"
  - id: tool
    label: "Try it: the slider"
  - id: grid
    label: "Across the income range"
  - id: caveats
    label: "What this isn't"
  - id: check
    label: "Check it yourself"
---
```

Placement inside the page body — the rail sits beside the content column, **below** the full-width
hero/disclosure/numeral-pair, which are not part of the rail's grid:

```html
<div class="page-shell">
  {% include chapter-rail.html %}
  <div class="content-col">
    <section id="mechanism">
      <h2>...</h2>
      ...
    </section>
    <section id="tool">...</section>
  </div>
</div>
```

**Read-back rule, every time:** every `id` in `sections:` has a matching `<h2 id="...">` (or
section id) in the body, and vice versa. A rail link with no target is a silent dead anchor;
`chapter-rail.js`'s `IntersectionObserver` only re-points `aria-current="location"` at links that
are already real, working `href="#id"` anchors — with JavaScript off, the rail is already a
complete, correct static list (design brief §3.4).

Never give the chapter rail and the top-bar nav (`_includes/header.html`) the same
`aria-label` — they are `"Primary"` and `"Sections of this page"` respectively; two different navs
sharing a label is indistinguishable to a screen reader.

The **home page has no chapter rail** (brief §3.3) — do not call `chapter-rail.html` from
`index.html`.

---

## 6. The disclosure

`_includes/disclosure.html` also reads from front matter — an array, each item becomes one `<p>`:

```yaml
---
layout: finding
disclosure:
  - >-
    The worked example throughout — the payor, the $201,000 income, the child care figures — is
    my own child support order: three children, my income and my children's mother's income
    entered as the Worksheet requires. I disclose it because a reader should be able to check
    whether the arithmetic changes when the numbers are real, not hypothetical. It doesn't: the
    same 17-point gap holds across the income and child-care ranges charted below, not only at
    my own figures.
  - >-
    The model behind every number here is <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>,
    checked by <a href="/model/test_worksheet.py"><code>model/test_worksheet.py</code></a>
    against the form's own calculation scripts.
---
```

Call it right after the hero, before the first finding, figure, or interactive exhibit:
`{% include disclosure.html %}`. web-page-anatomy's budget: fact + why it's told + a verification
link, all in the same disclosure block (one or two paragraphs), ≤3 sentences — the link must be
**inside** this block, never moved to the About page instead. The include does not escape the
paragraph strings (same convention as this repo's existing `description: >-` front matter) — content
authors are trusted, there is no user input here.

---

## 7. CSS class vocabulary

Every class below is in `assets/css/site.css`. Do not write new CSS for a content page — if
nothing below fits, say so instead of inventing a class.

### Header / top bar

`.topbar` (the `<header>` landmark) / `.topbar-inner` (flex row) / `.wordmark` / `.site-nav`
(shared by header and footer; `a[aria-current="page"]` styles itself, driven by the Liquid
`{% if page.url contains ... %}` checks already in `header.html` — don't add an "active" class by
hand) / `.nav-toggle-input` + `.nav-toggle-label` + `.nav-toggle-bars` (the ≤640px hamburger — a
real checkbox+label, functional with **zero** JavaScript; `site.js` only adds `aria-expanded`
bookkeeping and an Escape-to-close on top).

### Hero + display-tier numeral pair (home page, and once per finding page)

```html
<section class="hero">
  <p class="eyebrow">Massachusetts Child Support Guidelines Worksheet, verified in code</p>
  <h1>Massachusetts's hardship presumption does not kick in until the payor is at
    <span class="figure">55 percent</span> of net income.</h1>
  <p class="lede">One or two sentences restating that number with its reference class...</p>
</section>

<div class="numeral-pair">
  <div class="numeral">
    <span class="numeral-value">40</span>
    <p class="numeral-caption">Line 7e's reading, percent of income</p>
  </div>
  <span class="numeral-arrow" aria-hidden="true">&rarr;</span>
  <div class="numeral">
    <span class="numeral-value">55</span>
    <p class="numeral-caption">True share of net income, percent</p>
  </div>
</div>
```

On a finding page, one numeral only — add `numeral-pair--solo` to the wrapper and drop the arrow
and the second `.numeral`. **Never use `.numeral-value` for a number that is not the page's own
tested figure** (brief §3.2) — it is not a decorative stat treatment, it is the finding.

### Disclosure

`.disclosure` (outer, full-width) → `.box` (the bordered callout) — see §6 for the front-matter
pattern; don't hand-write the `<p>` tags in the body, they come from `page.disclosure`.

### Page shell / chapter rail

`.page-shell` (grid: rail + content, collapses to one column <960px) / `.chapter-rail` (`<nav>`,
built by the include in §5) / `.content-col` (max `var(--content-width)`, prose capped at
`var(--measure)` = 68ch).

### Findings grid (home page) and finding cards

```html
<div class="finding-grid">
  <article class="finding-card">
    <div class="thumb"><img src="/figures/exhibits/E05-....png" alt="..."></div>
    <div class="body">
      <p class="tag">Verified against the form's own scripts <span class="interactive-badge">&rarr; live tool</span></p>
      <h3><a href="/findings/hardship-test.html">The hardship test reads a different income than the order pays from</a></h3>
      <p>One mechanism sentence.</p>
      <div class="stat">
        <span class="stat-value">55%</span>
        <span class="stat-label">of the payor's net income, at the worked example, the point where the hardship presumption finally kicks in</span>
      </div>
    </div>
  </article>
  <!-- one .finding-card per finding; the fifth "card" the old mockup had (a ranking hover-strip)
       is GONE — replaced by the full sortable table in its own full-width section below the
       grid (brief §2.2/§3.5). Do not add a ranking-card/rank-bars mini chart back in; it isn't
       in this build's CSS on purpose. -->
</div>
```

**Do not duplicate a chart or its caption between a home-page card and its finding page** (a
red-team finding against the previous mockup, brief §4) — the card states only the headline stat
and one mechanism sentence; the full exhibit and its argument live exclusively on the finding page.

`.confidence-tag` doubles as `.finding-card .tag` — one consistent style, text stated in words
("Verified against the form's own scripts", "Tiered — see method", "Working paper, not yet
reviewed"), never color alone (SC 1.4.1). Place it at the point of listing, next to the title.

### Exhibit figures

Use the `_includes/figure.html` include (full parameter list is documented in that file's own
comment block) rather than hand-writing the `<figure>` markup:

```liquid
{% include figure.html
   id="e05"
   img="/figures/exhibits/E05-what-line-7e-sees-vs-true-burden-worked-example.png"
   alt="Line chart of Line 7e's reported percentage versus the true share of the payor's net
        income, against child care claimed from $0 to $600 a week, at the worked example."
   title="The hardship valve fires late because it reads the wrong income."
   notes="The true burden passes 40% of net at $130/week of child care; Line 7e reports 40% at
          $590/week, by which point the true burden is 55%."
   source_script="model/charts/fig6_valve.py"
   csv_href="/figures/working/fig6_valve_units_lag.csv" %}
```

Copy `title`/`notes` wording **verbatim** from the exhibit's own reviewed caption in the private
repository's `output/DRAFT-attachment-E-figures.md`
(read-only reference outside this repo — copy the wording in, never link that file from the site).
Drop `lazy="false"` on the first figure on a page (never lazy-load an above-the-fold image).

Two separate PNGs that are one comparison (a household + per-person pair): wrap two `figure.html`
calls in `<div class="exhibit-pair">`. **A single baked-together multi-panel PNG should not exist
in this exhibit set at all** — the 2026-09-06 exhibit direction retired every one of those
(E03/E07/E14/E15 → replaced by single-chart exhibits). If a future chart request produces one,
split it before adding it here.

`.exhibit-facts` (a `<dl>` of label/value pairs) is kept for backward compatibility with pages
built before this pass (`exhibits/index.md`) — a **new** figure normally does not need one, because
every chart in this project already bakes its own fact strip into the PNG (the
`analysis-chart-anatomy` skill's `fact_strip()`), so it would duplicate what's already in the image.

### Fifty-jurisdiction sortable table

Full markup contract and behaviour: comment block at the top of `assets/js/sortable-table.js`.
Classes: `.exhibit-table` (the `<table>`), `.exhibit-table-wrap` / `.table-scroll` (either name
works — the second is the old pages' name for the same overflow-x rule) for the ≤700px horizontal
scroll, `.table-filter` for the filter input's wrapper, `.is-reader-state` for Massachusetts's row.
A page using it must add `scripts: ["/assets/js/sortable-table.js"]` to its front matter, and the
table must render **complete and correctly pre-sorted with no JS at all** — the script only
reorders DOM rows already present, it does not fetch or invent data for this exhibit (unlike the
sliders below, whose whole point is a live lookup).

**Jurisdiction finder (2026-09-07), a separate control next to the filter:** full markup contract
in `assets/js/jurisdiction-finder.js`'s header comment. Classes: `.table-tools` (wraps the finder
and the filter in one row, stacking <700px), `.table-finder` (the `<select>`'s own wrapper, styled
like `.table-filter`), `.jurisdiction-readout` (the one-line comparison above the table), and
`.is-selected-state` on the found `<tr>` — a blue outline (`--hue-recipient`) kept visually
distinct from `.is-reader-state`'s permanent claret tint, since Massachusetts (the finder's default)
can carry both classes at once. **This is a finder, not a filter — it never hides a row**; adds
`scripts: ["/assets/js/jurisdiction-finder.js"]` alongside `sortable-table.js`.

### The live tools (calculator, valve slider, credit-collapse slider)

Full markup contract: comment block at the top of `assets/js/csv-slider.js`. Classes: `.tool` /
`.tool-deck` / `.tool-slider-row` / `.tool-two-up` (two sliders side by side, stacking <700px) /
`.tool-readout` / `.cell-label` / `.cell-value` (`.payor-line`, `.true-burden` modifiers) /
`.tool-flag`. A page using one adds `scripts: ["/assets/js/csv-slider.js"]` **and** must render the
no-JS fallback described in brief §3.7 (a static table, or the worked example's real baseline
values as plain text) — never a slider with nothing behind it when JavaScript is off.

**Calculator v2 (2026-09-07) added four classes**, all still inside this same `.tool` vocabulary
and documented in full in `assets/js/README.md` §1 and the header comment of `assets/js/calculator.js`:
`.tool-controls-row` (a real-radio segmented-control row — children count, custody box — that
spans the full `.tool-two-up` grid via `grid-column: 1 / -1`, since the two-up grid's implicit
2-column auto-placement would otherwise split it across a row), `.segmented`/`.segmented-option`
(the segmented controls themselves — a `<fieldset>`/`<legend>` with real `<input type="radio">`
options; the checked-option highlight is `:has()`, progressive enhancement only — the native radio
dot is the non-color channel that still works everywhere), `.tool-detail` (the `<details open>`
wrapper around the "after tax and the order" row, also `grid-column: 1 / -1`; open by default per
the restraint budget below), and `.cell-note`/`.cell-sub` (a bold short text label paired with a
warning colour per WCAG 1.4.1, and a per-person figure set beside a household one).

**Warning colour: `--accent` (the claret, #7A1330), verified 9.73:1 against `--surface` — well
past the 4.5:1 AA floor for text, per the ratio table in `assets/css/site.css` §1.** No separate
warning/danger token exists in this palette (brief §3.1's discipline: `--accent` is the only
saturated colour, used nowhere decoratively) — reusing it for "this figure crossed a threshold" is
the same colour already load-bearing for stat numbers, display numerals and the pinned
Massachusetts row, so it does not introduce a second meaning for red. **Colour is never the only
channel**: every element that gets `.is-warning` (`.tool-readout .cell-value.is-warning`) is paired
with a `.cell-note` sibling that fills in with bold text ("Above 40% of net", "Above the payor")
only when the warning is on, and is otherwise present but empty (`visibility: hidden`, height
reserved so nothing jumps). This differs from the pre-existing `.true-burden` modifier, which
colours a cell unconditionally (used by the credit-collapse slider, §3 below, for a figure that is
always the tool's headline number regardless of its value) — the calculator's true-share-of-net
cell deliberately does NOT carry `.true-burden`, since v2 needs that one cell's colour to be
conditional on the 40% threshold rather than permanent; do not re-add `.true-burden` to it.

### Exhibits gallery + lightbox

Full markup contract: comment block at the top of `assets/js/lightbox.js`. Classes:
`.exhibit-gallery` / `.exhibit-tile` / `.exhibit-tile-caption`, and the once-per-page lightbox root
(`.lightbox` / `.lightbox-dialog` / `.lightbox-close` / `.lightbox-caption`). `exhibits.html` adds
`scripts: ["/assets/js/lightbox.js"]`. Every tile is a real, working link to the full-size PNG with
no JavaScript — the lightbox is progressive enhancement on top of that, not a replacement for it.

### Caveats, check-it-yourself, documents, ask

`.caveat` (the two standing caveats every finding page carries — per-person counter-argument, and
"this is a tested extreme, not a typical case" — brief §3.6 step 6, never collapsed/hidden).
`.check-yourself` / `.ask` (interchangeable; verification-oriented section, never support-oriented
— no "donate," no "join"). `.doc-list` / `.doc-item` / `.doc-title` / `.doc-context` (Documents
page). `.stat-callout` / `.stat-value` / `.stat-label` (a single number in running prose, per
web-figures — not a chart, unless a curve's *shape* is the argument).

### Tables (plain Markdown)

Kramdown output for a table without the `.exhibit-table` class gets the base rules automatically:
header rule, row hairlines, no vertical rules, no zebra stripe (`web-design-system`: a zebra tint
computes to ~1.1:1, not a real distinction). For numeric columns needing right-alignment, write
raw HTML with `class="numeric"` on the relevant `<th>`/`<td>` — kramdown has no column-alignment
syntax for this.

---

## 8. Navigation

Two navs, deliberately different in length, per web-page-anatomy's "flat, ≤8 items" and this
brief's explicit four-item top bar:

- **Top bar** (`_includes/header.html`, `aria-label="Primary"`): Findings, Fifty jurisdictions,
  Documents, Repository. Exactly the brief's §3.3 list.
- **Footer** (`_includes/footer.html`, `aria-label="Footer"`): the same four, plus Exhibits, About
  & method, and Sitemap — the fuller list web-page-anatomy's Footer slot wants, and the
  `/sitemap/` link that satisfies WCAG 2.4.5's "independent second way to navigate" (a footer that
  only repeats the header nav is not that second way on its own).

`sitemap/index.md` is unchanged from the previous design and still needs its list of pages kept in
sync as new pages land — see that file for the current entries; it still names some old-design
URLs (`/exhibits/`, `/the-model/`, `/the-data/`) that a migration to the brief's file list should
update in the same pass that moves the content.

---

## 9. Read-back (do this before calling a page done)

Run `web-page-anatomy`'s eight-point read-back against the rendered page, plus, specific to this
design:

1. **Headings alone carry the argument** — extract every H1–H3 with no body text.
2. **The hero's first sentence contains a number and its reference class.**
3. **The disclosure's verification link is inside the disclosure block**, not moved elsewhere.
4. **Every number traces to a file** — the CSV beside a chart in `figures/working/`, a printed run
   in `model/runs/`, or a dataset in `data/fifty-state/`. If it isn't in one of those, leave it out.
5. **Confidence tags** appear on every item sitting next to one of a different tier.
6. **Chapter rail**: every `sections:` id has a matching heading id and vice versa (§5).
7. **No `/Users/` or other absolute local path** anywhere in the built output —
   `grep -rl "/Users/" _site` (excluding the frozen asset folders, which legitimately contain
   filesystem-looking strings in code/data files, not in page markup) must return nothing.
8. **An interactive exhibit has a real no-JS fallback** that shows correct, real numbers — not a
   blank control and not an empty table.
9. **390px screenshot**, taken with `Emulation.setDeviceMetricsOverride` or a real device, not
   `--window-size` alone — the brief's own red-team notes this sandbox's headless Chrome silently
   clamps to 500px.
10. **A local build still succeeds**: `BUNDLE_PATH=vendor/bundle bundle exec jekyll build`, then
    re-run a link check against `_site/` (see §1) — Jekyll's own build does not catch a dead link.

---

## 10. What's still missing (not built by this pass)

- Every page in the brief's file list (§3.12): `index.html`, the four `findings/*.html` pages,
  `findings/index.html`, `exhibits.html`, `documents.html`, `about.html`. This pass built only the
  foundation they render inside — see §0 for exactly what already exists at the old URLs and can
  be rewritten into the new pattern.
- Interactive exhibit #4 (parenting-time credit-collapse, brief §3.7 item 4) needs Observable Plot
  vendored at `assets/vendor/observable-plot/` with its licence file (brief: chosen for built-in
  per-mark ARIA labels; ~69KB gzip) — **not fetched or vendored by this pass**. `figures/working/fig3_credit_collapse.csv`
  already has the underlying data (columns include `implied_share_1.5` / `implied_share_2.0` —
  this is the export the brief's §3.12 file list calls `parenting-time-credit.json`; convert it,
  don't regenerate it from `box1_fix.py` a second time).
- The CSV→JSON conversion for the other three interactive exhibits' data files
  (`figures/working/fig1_heatmap_3child_box1.csv` → the calculator's grid, 1,147 rows;
  `figures/working/fig6_valve_units_lag.csv` → the child-care slider, 130 rows;
  `figures/working/fig5_states.csv` → the sortable table, 50 rows) into `assets/data/*.json` as
  flat arrays-of-objects (keys = the CSV's own header row) is not done by this pass — do it once,
  at authoring time, and check the resulting JSON into the repo next to the page that uses it; it
  is not regenerated by the Jekyll build (there is no build step in route (a) that could run a
  conversion script — GitHub's runner only runs Jekyll itself).
- `assets/vendor/` does not exist yet — create it only when the Observable Plot exhibit is built,
  with the library's own LICENSE file alongside it (brief: "no CDN at runtime").

---

## 11. Calculator v2 (2026-09-07) — the under-13 discrepancy, and the jurisdiction finder

**As of 2026-09-09 the calculator's "after tax and the order" row matches this site's own
worked-example figures elsewhere exactly ($87,172/$77,395), because the published model's default
excludes refundable tax credits everywhere.** The calculator fixes `kids_under_13 = 0` for every
combination (same generic-grid convention as `model/charts/_common.py`'s `KIDS_UNDER_13 = 0`, since
there is no third slider for how many children are under 13), and the worked example quoted in
`model/runs/submission-figures-run-2026-09-09.txt` and repeated around the rest of the site is
computed on the same credits-off, withholding basis. Under that basis `kids_under_13` does not
change any figure the site prints, because the MA Child and Family Tax Credit it would otherwise
affect is a refundable credit, and refundable credits are not counted. The convention only matters
if a reader switches the credits toggle on, where it still governs the labelled analysis view (the
credits-inclusive figures move by up to $880/yr per qualifying child, and depend on which parent
claims which child, which is why they are analysis rather than the ask). The method paragraph next
to the calculator should keep saying this in one sentence; do not remove it if the copy is edited,
and do not give the calculator a fourth slider for how many children are under 13, since that would
change every combination it can compute to a fact pattern that stops making sense once the
children slider leaves 3, for a control that presently affects nothing under the default basis.

**Warning-colour thresholds added by v2** (see §7 for the colour itself): the true-share-of-net
cell warns above 40% of the payor's net income (Line 7e's own substantial-hardship threshold); the
recipient-household cell warns whenever it exceeds the payor's own after-tax, after-order figure.
Both are computed live from the ported worksheet/tax model, not hardcoded — see
`assets/js/calculator.test.js` PART 5, which checks the threshold comparison agrees with the
Python-generated fixture on all 36 grid combinations, not only the worked example.

**Restraint budget**: the two new controls add one full-width row; the new output row is inside
`<details open>` specifically so the block's apparent height stays close to its pre-v2 size when
collapsed, while still rendering all of its content (open by default) with no JavaScript at all.

**The fifty-jurisdiction table's jurisdiction finder is a separate control from the calculator and
models nothing itself** — it is a `<select>` over the same 51 rows already in the table (50 ranked
plus Georgia, held out), used only to highlight and scroll to a row and to read out that
jurisdiction's own two numbers next to Massachusetts's. It does not compute; the calculator above
it is the only tool on this page that does, and remains Massachusetts-only for that reason — its
method paragraph says so in one clause so a reader does not assume the sliders can model another
state's worksheet.
