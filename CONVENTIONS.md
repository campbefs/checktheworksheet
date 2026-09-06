# Site conventions — checktheworksheet.org

For every agent writing a content page in this repository. Follow this file exactly; it is written
so you do not have to ask. It documents the foundation built in `_config.yml`, `_layouts/`,
`_includes/`, and `assets/css/site.css`. **Do not edit those files** without updating this one to
match — they are what every content page depends on.

Required skills before writing a page: `web-design-system`, `web-page-anatomy`, `web-figures`,
`web-static-build`. This file is the local application of those four to this repository; it does
not restate their reasoning.

## Build route

Route (a) from `web-static-build`: plain Jekyll, no theme, hand-written CSS, GitHub's default
runner builds on every push. No `Gemfile`, no GitHub Actions workflow, no JavaScript anywhere.

## Frozen paths — never touch

`model/`, `data/`, `figures/`, `paper/` are frozen: their exact paths are cited in a working paper
and in letters already sent. Never delete, move, or rename anything inside them. New content pages
must link to files at their existing paths (e.g. `/figures/exhibits/E05-....png`,
`/model/worksheet.py`) and never assume a different location.

## Page front matter — every content page needs this

```yaml
---
layout: page        # or: finding  (see "Layouts" below)
title: A short page title
description: >-
  One or two sentences. Becomes the meta description via jekyll-seo-tag.
---
```

A page with no `layout:` key will still get a layout — the default-on `jekyll-default-layout`
plugin assigns `page.html` automatically — but always set it explicitly. Don't rely on the fallback.

## URLs — one content file per directory, named `index.md`

To get a clean URL (`/findings/`, not `/findings.html`), put the file at `<name>/index.md`. Do not
use a global `permalink:` setting (it only reliably affects posts) and do not hand-set
`permalink:` in every file's front matter — the folder convention is simpler and is what the nav
in `_includes/header.html` and `_includes/footer.html` already assumes:

| Nav label | URL | File to create |
|---|---|---|
| Findings | `/findings/` | `findings/index.md` (listing) + `findings/<slug>/index.md` (one per finding) |
| Exhibits | `/exhibits/` | `exhibits/index.md` |
| The model | `/the-model/` | `the-model/index.md` |
| The data | `/the-data/` | `the-data/index.md` |
| Documents | `/documents/` | `documents/index.md` |
| About | `/about/` | `about/index.md` |

**Do not create `model/index.md`, `data/index.md`, `figures/index.md`, or `paper/index.md`.** Those
directories are frozen asset folders (see above); putting a Jekyll content page inside one mixes
site content into a path an external document cites and risks exactly the kind of change the freeze
rule exists to prevent. The content pages that describe the model/data/documents live at the
hyphenated top-level URLs above and link *into* the frozen folders (`/model/worksheet.py`,
`/data/fifty-state/tier-50-2026-09-05.json`, etc.) rather than living inside them.

**`/sitemap/` does not exist yet.** The footer already links to it (`_includes/footer.html`) because
`web-page-anatomy` requires a human-readable sitemap page as the independent second way to navigate
(WCAG 2.4.5) — a footer that repeats the header nav is not that second way. Whoever builds the
Documents or About page should also create `sitemap/index.md`: a flat list of every page on the
site, in one place, as plain links. (`jekyll-sitemap`, already in `_config.yml`, only generates the
machine-readable `/sitemap.xml` — that is a separate, additional thing, not a substitute.)

## Layouts

| Layout | File | For | Adds over `default` |
|---|---|---|---|
| `default` | `_layouts/default.html` | Never set directly on a content page | HTML skeleton: head (`{% seo %}`, stylesheet, viewport), skip link, header include, `<main id="main">`, footer include |
| `page` | `_layouts/page.html` | Findings index, Exhibits, The model, The data, Documents, About | Wraps content in `<article class="page">`. No auto-generated heading — write your own `#` H1 as the first line of the markdown body |
| `finding` | `_layouts/finding.html` | One individual finding's own page (`findings/<slug>/index.md`) | Same as `page`, plus a breadcrumb (`Findings › <page.title>`) above the content |

Both `page` and `finding` set `layout: default` in their own front matter — Jekyll chains them, so
a content file only ever sets `layout: page` or `layout: finding`, never `layout: default`.

**Do not auto-generate an H1 from `page.title` in a layout.** The homepage (`index.md`) already
writes its own `# ...` heading in the markdown body; a layout that also prints `page.title` as an
H1 would duplicate it there. Every content page follows the same rule: write the H1 yourself, in
markdown, as the first line.

If a future page shape genuinely needs something `page`/`finding` don't provide (a different article
structure, not just different CSS classes), add a new layout file and a new row to this table —
don't overload the two above with conditional logic for content that varies page to page.

## CSS class vocabulary

Every class below is defined in `assets/css/site.css`. Do not write new CSS for a content page —
if nothing below fits, say so instead of inventing a class, so the vocabulary stays reviewable in
one file.

### Page shell (from the layouts — you don't add these by hand)

| Class | Where | What |
|---|---|---|
| `.skip-link` | `default.html` | Visually hidden until focused; jumps to `#main` |
| `.site-header` / `.header-inner` | `default.html` / `header.html` | Header landmark and its measure-constrained inner wrapper |
| `.site-title` | `header.html` | The site name, links home |
| `.site-nav` | `header.html`, `footer.html` | The flat nav list; `a[aria-current="page"]` is styled automatically — don't add a class for "active," the layout sets the attribute |
| `.site-footer` / `.footer-inner` | `default.html` / `footer.html` | Footer landmark and wrapper |
| `.footer-meta` | `footer.html` | The one line of attribution/license/date text |
| `.page` | `page.html` | Article wrapper for a plain content page |
| `.finding` | `finding.html` | Article wrapper for one finding's page |
| `.breadcrumb` | `finding.html` | The `Findings › Title` line; only used on two-levels-deep pages |

### Hero (homepage only — `web-page-anatomy`'s Hero slot)

| Class | What | Notes |
|---|---|---|
| `.hero` | Wraps the eyebrow + H1 + lede block | Homepage only |
| `.eyebrow` | Small caps label above the H1 | ≤ 10 words (skill budget) |
| `.lede` | The intro paragraph after the H1 | 40–80 words (skill budget), must state the H1's number with its reference class |

`index.md` is off-limits to every agent unless specifically assigned it. If you are that agent: the
homepage currently has no `layout:` front matter key, so it is picking up `page.html` by default
(no hero markup, no chrome beyond what `jekyll-default-layout` + `page.html` already gives it).
Restructuring it to use `.hero`/`.eyebrow`/`.lede` is exactly what those classes are for — add
`layout: page` explicitly at that point (or a dedicated `home.html` layout, and a new row in the
Layouts table above) rather than leaving the fallback implicit.

### Disclosure (`web-page-anatomy`'s Disclosure slot)

| Class | What |
|---|---|
| `.disclosure` | Boxed callout: personal-stake fact, why it's told, and the verification link, all in the same `<p>` or two adjacent `<p>` inside it. ≤ 3 sentences total. Place right after the hero/lede, before the first finding, figure, or ask. |

```html
<div class="disclosure">
  <p>The worked example throughout is my own child support order, disclosed here because a reader
  should be able to check whether the arithmetic changes when the numbers are real. The model that
  produced it is at <a href="/model/worksheet.py"><code>model/worksheet.py</code></a>, with the test
  suite that pins it to the form's own calculation scripts.</p>
</div>
```

### Findings list (Findings index page)

| Class | What |
|---|---|
| `.finding-list` | `<ul>` wrapper for the finding cards |
| `.finding-card` | `<li>` per finding: heading (≤ 12 words, asserts), ≤ 2-sentence summary, one stat |

```html
<ul class="finding-list">
  <li class="finding-card">
    <h3><a href="/findings/hardship-test-reads-the-wrong-income/">The hardship test reads the wrong income</a></h3>
    <p>Section IV.C presumes hardship at 40 percent of gross-derived available income, but the order
    is paid from net. At the worked example the form reports 40 percent when the payor is at 57
    percent of net.</p>
    <p class="stat-callout">
      <span class="stat-value">57%</span>
      <span class="stat-label">of the payor's net income, at the point the form itself reads 40%</span>
    </p>
  </li>
  <!-- one <li class="finding-card"> per finding -->
</ul>
```

### Confidence tag (`web-page-anatomy`: "Marking mixed confidence")

| Class | What |
|---|---|
| `.confidence-tag` | One consistent visual style, text-only — the tier is stated in words, never by color alone (SC 1.4.1). Place next to the title of the item being tagged, at the point of listing (a documents list, a findings card) and again on the item's own page if it has one. |

```html
<p class="confidence-tag">Verified against the form's own calculation scripts</p>
<p class="confidence-tag">Tiered — see method</p>
<p class="confidence-tag">Working paper, not yet reviewed</p>
```

### Stat callout (`web-figures`: "a single number... a text callout, not a chart")

| Class | What |
|---|---|
| `.stat-callout` | Wraps one `.stat-value` (the number) and one `.stat-label` (its reference class, spelled out — not a bare percentage) |

```html
<p class="stat-callout">
  <span class="stat-value">88 cents</span>
  <span class="stat-label">of every dollar of claimed child care, funded by the payor at the worked example</span>
</p>
```

### Ask / verify-it-yourself (`web-page-anatomy`'s slot of the same name)

| Class | What |
|---|---|
| `.ask` | One bordered, separated section — never mid-argument. Verification-oriented ("check the model," "read the data"), never support-oriented ("donate," "join"). |

```html
<div class="ask">
  <h2>Check it yourself</h2>
  <p>One paragraph on how, then direct links:</p>
  <ul>
    <li><a href="/the-model/">The model</a></li>
    <li><a href="/the-data/">The data</a></li>
    <li><a href="https://github.com/campbefs/checktheworksheet">The repository</a></li>
  </ul>
</div>
```

### Document list (Documents page)

| Class | What |
|---|---|
| `.doc-list` | `<ul>` wrapper |
| `.doc-item` | `<li>` per document: `.doc-title`, then a `.confidence-tag`, then a `.doc-context` line |

```html
<ul class="doc-list">
  <li class="doc-item">
    <span class="doc-title">Comments to the Trial Court, with Attachments A and D</span>
    <span class="confidence-tag">Prepared for submission — not yet sent</span>
    <span class="doc-context">The full submission as it will go to the Chief Justice.
      <a href="/paper/Comments-to-the-Trial-Court-with-Attachments-A-and-D.pdf">PDF</a></span>
  </li>
</ul>
```

### Tables

Plain Markdown tables (kramdown) get the base styling in `site.css` §9 automatically: header rule,
row hairlines, no vertical rules, no zebra stripe. Kramdown does not support column alignment for
numeric columns out of the box — for a table with numeric columns, write it as raw HTML and add
`class="numeric"` to the numeric `<th>`/`<td>` cells so they right-align with tabular figures.

### Figures

See `web-figures`'s `figure.html`/`ranked-table.html` for the full pattern and rationale (multi-panel,
dark-mode, alt-text formula). The classes (`.exhibit`, `.exhibit-title`, `.exhibit-deck`,
`.exhibit-facts`, `.exhibit-notes`, `.exhibit-source`, `.exhibit-pair`, `.exhibit-table`) are already
in `site.css` §10. Concretely, for this repo:

- `{{TITLE}}` / `{{DECK}}` / fact pairs / `{{NOTES}}` — copy verbatim from the figure's own in-image
  text and from `/Users/christophercampbell/Desktop/src/projects/child-support-reform/output/DRAFT-attachment-E-figures.md`
  (read-only reference outside this repo — do not copy that file in, just its wording for the
  figures it already describes, E01–E17).
- `{{IMG_SRC}}` — `/figures/exhibits/E0X-....png` (one file per exhibit; no 2x variant exists, so
  omit `srcset`).
- `{{CSV_HREF}}` — the matching file in `/figures/working/*.csv` per the table in
  `figures/working/README.md` (that file is excluded from the built site but still readable in the
  repo for this mapping).
- `{{SOURCE_SCRIPT}}` — the `.py` in `/model/charts/` named in the same README table.

```html
<figure class="exhibit" id="e05">
  <img src="/figures/exhibits/E05-what-line-7e-sees-vs-true-burden-worked-example.png"
       loading="lazy"
       alt="Line chart of Line 7e's reported percentage versus the true share of the payor's net
            income, against child care claimed from $0 to $600 a week, at the worked example.">
  <figcaption>
    <h3 class="exhibit-title">The hardship valve fires late because it reads the wrong income.</h3>
    <p class="exhibit-deck">Line 7e's reading vs. the true burden as claimed child care rises, worked example.</p>
    <p class="exhibit-notes">The true burden passes 40% of net at $80/week of child care; Line 7e reports 40% at $590/week, by which point the true burden is 57%.</p>
    <p class="exhibit-source">Source: <code>model/charts/fig6_valve.py</code> ·
      <a href="/figures/working/fig6_valve_units_lag.csv">data (CSV)</a></p>
  </figcaption>
</figure>
```

Drop `loading="lazy"` on the first figure on a page (never lazy-load an above-the-fold image); keep
it on every subsequent one.

For a ranked list of fifty-plus rows (the fifty-state comparisons), add the `<table class="exhibit-table">`
alternative from `ranked-table.html` beside the chart, built from the same CSV, with the reader's own
row (Massachusetts) marked `class="is-reader-state"`. Never present fifty rows as one long image with
no table.

## Numeracy (`web-page-anatomy`: "Numeracy in prose")

State a statistic as a concrete count with its reference class, not a bare ratio: "88 cents of every
dollar," not "87.68%." For a ranked claim, start from the exact count and denominator the source
states — "50 of 51 jurisdictions modelled" — and build the sentence from that; don't round it to
"most states." Every number must trace to a file in this repository: the CSV beside a chart in
`figures/working/`, a printed run in `model/runs/`, or a dataset in `data/fifty-state/`. If a number
isn't in one of those, leave it out.

## Read-back (do this before calling a page done)

Run the eight checks in `web-page-anatomy`'s "Read-back" section against the rendered page. In
particular for this site: headings alone must carry the argument; every number must be traced to its
source file; confidence tags must appear on every unverified item sitting next to a verified one;
the nav must show the current page marked and the skip link must be the first focusable element.

## What's still missing (not built by this pass)

- `sitemap/index.md` — required by the footer link and by `web-page-anatomy`'s navigation
  requirement (WCAG 2.4.5). Not yet created.
- Every content page under Nav/URLs above (`findings/`, `exhibits/`, `the-model/`, `the-data/`,
  `documents/`, `about/`) — this pass built only the shell they render inside.
- `index.md`'s own front matter and hero markup — untouched, out of scope for this pass; currently
  renders through `page.html` via Jekyll's default-layout fallback (see "Hero" above).
