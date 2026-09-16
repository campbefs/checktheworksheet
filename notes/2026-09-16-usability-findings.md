# Usability findings on the homepage — 2026-09-16

**Origin.** These are findings about this site's own homepage, surfaced as a byproduct of
testing whether Claude's `design-usability` skill (built and tuned against Shopify app screens)
also works on a non-app, content-argument surface. The skill-fit question was the actual task;
this file exists so the four things noticed about the live page don't evaporate when that
session ends. **Not triaged, not fixed, and not a design-department deliverable** — just a
faithful record of what a Nielsen heuristic evaluation, run once, found and didn't find.

Method: source-only read of `index.html`, `_layouts/home.html` → `_layouts/default.html`,
`_includes/header.html`/`footer.html`/`disclosure.html`, `assets/js/calculator.js`, and
`assets/css/site.css`. No rendered browser pass — see Scope note at the end.

Surface reviewed: the homepage only, as the page a cold, possibly skeptical first-time visitor
lands on and decides within seconds whether to keep reading.

---

## Findings

Each finding: heuristic, file:line, evidence, severity (Nielsen 0-4: 0 not a problem, 1
cosmetic, 2 minor, 3 major, 4 catastrophe), and what fixing it would take.

### F1 — Numeral-pair orphaned from its context (Heuristic 6, Recognition rather than recall)

**Severity: 1 (cosmetic).**

`index.html:342-352`. The "40 → 57" numeral-pair (captioned "What Line 7e reports, in percent
of income" → "The payor's true share of net income when it finally does") sits directly after
the "What the Worksheet does that its text doesn't say" heading and its one-line intro
(`index.html:336-339`), but *before* the four finding cards. The card that actually explains
these two numbers — `f-hardship`, "The hardship test reads a different income than the order
pays from" — is the *second* of the four cards below it (`index.html:377-396`).

A first-time reader hits two bare percentages with only a caption, no link or heading tying them
to the hardship finding, and has to keep scrolling to get the "why" — a brief, self-resolving
disorientation rather than a real barrier.

**Cheap fix:** either move the numeral-pair to sit directly above/inside the `f-hardship` card,
or add one clause to its wrapping context (e.g. an eyebrow line "the hardship test:") so the pair
reads as already-labeled rather than a preview a reader has to hold in mind.

### F2 — No reset control on the calculator (Heuristic 3, User control and freedom)

**Severity: 2 (minor).**

`index.html:58-292`, the "Try it: compute your own two incomes" calculator. The entire page's
narrative and every stat claim on it are pinned to one worked example — $201,000 / $29,640 / 3
children, no child care. The calculator's sliders default to those values, but nothing on
screen restores them once a reader drags a slider away. The only paths back are (a) manually
retyping all of higher-earner income, lower-earner income, children, custody box, and child
care to their exact original values, or (b) a full page reload, which also loses scroll
position.

Checked `calculator.js` for a reset/restore/default-value handler — none exists
(`grep -n "reset\|restore" assets/js/calculator.js` returns nothing relevant).

Not severe — reload is a full, low-cost recovery path, and nothing is destroyed — but it's a
real gap on a tool whose whole point is *comparing against* a specific reference example.

**Cheap fix:** one small "Reset to the worked example" link/button next to the sliders that
re-applies the six default values and re-renders.

### F3 — Worksheet line numbers unglossed on first use (Heuristic 2, Match between system and the real world)

**Severity: 2 (minor) — and see the caveat below.**

`index.html:126-131`. The calculator's readout labels a reader's very first result as "Weekly
order (Line 7d)" and "Line 7e's reading," with no inline explanation of what Line 7d or Line 7e
*is* structurally, the first time either appears. A visitor who has never seen Massachusetts
form CJ-D 304 meets a worksheet-internal citation before any plain-language gloss of what it
means. Heuristically this is the same failure shape as a raw enum or internal exception name
surfacing as UI copy — jargon presented as if the audience already has it.

**This is not an oversight to fix on sight.** The site's stated method — see the disclosure at
`_includes/disclosure.html` and its worked example ("The model behind every number here is
`model/worksheet.py`... checked against the form's own calculation scripts") — is built entirely
on *traceability*: every figure cites its exact line on the actual government form so a skeptical
reader (or the form's own author) can go check it. Citing "Line 7e" by name is that traceability
promise being kept, not a leak. Removing or hiding the citation would undercut the site's central
credibility mechanism.

**This is a judgment call for the site's author, not a defect:** the options are (a) leave it
as-is, on the reasoning that the target reader for a policy-verification site is expected to
either already know the form or be willing to look it up — traceability outranks approachability
here; or (b) add a one-time inline gloss the first time "Line 7d"/"Line 7e" appears (e.g. a
`<dfn>`/tooltip: "Line 7d — the worksheet's own line for the weekly order amount"), which would
help a genuinely cold reader without weakening the citation. Either is defensible; this note
exists so the trade-off is visible, not to argue for either side.

### F4 — The same qualifier repeated three times in the first screen (Heuristic 8, Aesthetic and minimalist design)

**Severity: 1 (cosmetic).**

The phrase "the same two incomes and three children" (or a close variant: "one set of incomes,"
"one worked example") appears three times before a reader has scrolled past the first exhibit
pair:

- the lede, `index.html:28-32`: "The same two incomes and three children in every state..."
- the confidence-tag directly under it, `index.html:37`: "The same two incomes and three
  children, in every state."
- the caption/`confidence` field on the E12/E17 exhibit pair immediately below,
  `index.html:316` and `index.html:327`: "The same two incomes and three children, in every
  state." (verbatim, twice more)

Each instance is individually load-bearing — it's the site's key methodological caveat and the
`web-page-anatomy`/disclosure convention calls for it to travel with every figure — but reading
top-to-bottom it lands as the same sentence four times in one screen's worth of content. Not a
correctness problem, and arguably intentional given the disclosure convention; flagged because a
first-time skim is exactly the moment repetition costs the most attention.

**Cheap fix, if the author wants one:** vary the wording on at least one of the four instances,
or drop the exhibit-pair `confidence` caption where the lede/tag directly above the same section
already said it seconds earlier.

---

## Heuristics and checks with no violation found

Stated explicitly, per the evaluation method, so nobody re-audits this ground later:

- **H1 Visibility of system status** — the calculator's status-strip badges (`range`,
  `impossible`, `household`, `hardship`) update live with every slider/toggle change and name
  their own cause in the same breath (`assets/js/calculator.js:845-880`).
- **H5 Error prevention** — sliders are constrained to declared min/max; a typed value outside a
  field's own range (e.g. a health-insurance premium) is clamped before it reaches the model,
  and the substitution is visibly flagged rather than silently computed
  (`assets/js/calculator.js:845-853`).
- **H9 Help users recognize, diagnose, recover from errors** — every status badge names the
  cause and, where relevant, the exact control that would change it (e.g. "Switch them off above
  to see the difference," `assets/js/calculator.js:872-876`).
- **H10 Help and documentation** — the "Assumptions and method" `<details>` sits directly under
  the calculator it explains; the "Check it yourself" section sits at the point in the page a
  verification-minded reader would actually want it.
- **Icon-only controls** — the only icon-only control on the page is the mobile hamburger nav
  toggle, which carries a visually-hidden "Menu" label and is a real, keyboard-operable
  `<label for>` bound to a checkbox — the collapsed panel is never `display:none`, so nothing
  drops out of the tab order (`_includes/header.html`).
- **Progressive disclosure** — never exceeds 1 level (the child-care toggle, the "Assumptions
  and method" `<details>`), inside NN/g's ≤2-level guidance.
- **Navigation depth vs. frequency** — the three tasks a first-time visitor is likely to want
  (read a finding, try the calculator, verify a number against source) are all 0-1 clicks from
  the homepage.
- **H4 Consistency and standards** — Home/nav behavior, the shared `.stat`/`.stat-callout`
  styling between finding cards and the hero, and heading hierarchy (one `h1`, ordered `h2`/`h3`,
  no skipped levels) are consistent across the page.

## A deliberate trade-off that was checked and NOT flagged

The site's own wordmark (`_includes/header.html`, styled at `assets/css/site.css:142-146`) is a
link to `/` with no visible link affordance — no underline, and its `:hover` only shifts text
color. Read in isolation, the discoverability "signifiers, not affordances" check would flag
this: it's clickable but doesn't look clickable.

It isn't flagged as a finding here because `header.html`'s own comment already reasons through
exactly this and mitigates it deliberately: "Home is a deliberate repeat of the wordmark. The
wordmark is a link but does not look like one, so a reader has no obvious way back. Duplicated
affordance beats a hidden one." The nav bar carries an explicit "Home" text link right beside the
wordmark for this reason. Checked that the mitigation is real (the "Home" link is present, styled
as a normal nav link, and marked `aria-current="page"` on `/`) — this is a decision already made
and defended in the code, not a gap to re-litigate.

## Scope note

This was a source-only read: HTML, CSS, and JS files, no rendered browser, no screenshot, no
Playwright pass. That's enough to find structural, copy, and logic problems that are true
regardless of how the browser paints them (all four findings above are of that kind), but it
cannot confirm:

- **Actual computed spacing** — whether the CSS's declared `--space-*` values produce the
  visual rhythm the source implies at real widths.
- **Breakpoint behavior** — how the layout actually reflows below the ~640px collapse point
  named in `header.html`'s comments, or at the `.hero`/`.numeral-pair` breakpoints in
  `site.css`.
- **The reading-progress bar** (`_layouts/default.html`, `.progress-bar`) — present in markup
  and described as animated by `site.js`, but not confirmed to render or track scroll correctly
  in a real browser.
- **The hamburger nav collapse** — confirmed keyboard-reachable and non-`display:none` from the
  markup/CSS alone, but not confirmed to visually open/close correctly.

A rendered pass (Playwright screenshot or a live load) would be needed to close those four, and
none of the four findings above depend on it — they're all readable from source alone.
