// checktheworksheet.org — hand-rolled, dependency-free lightbox, SITE-WIDE as of the 2026-09-07
// pass (design brief §3.8, extended by owner direction the same day: every exhibit image on every
// page opens wider in a modal, not only the exhibits gallery). Real DOM (an <img> inside a
// positioned <div>), not a canvas widget, so it is reachable and readable exactly like the rest of
// the page. Vanilla JS, no dependencies, no CDN.
//
// Loaded unconditionally from `_layouts/default.html`, the same way `site.js` is — a page no
// longer needs `scripts: ["/assets/js/lightbox.js"]` in its own front matter (harmless if one
// still has it: `document.querySelectorAll` again finds the same trigger elements and rewires the
// same listeners). The one lightbox root is written once, in `default.html`, present on every
// page; this script no-ops (`if (!root) return`) only if that markup is ever missing.
//
// ---------------------------------------------------------------------------------------------
// MARKUP CONTRACT
// ---------------------------------------------------------------------------------------------
// Any trigger, anywhere on the page (an exhibits-gallery tile, a figure.html exhibit, a
// finding-card thumbnail, a hero image):
//   <a class="lightbox-trigger" href="/figures/exhibits/E01-who-holds-more-3-children.png"
//      data-lightbox
//      data-caption="With three children, the recipient household holds more after the order in
//      55 percent of the income combinations modelled."
//      data-csv-href="/figures/working/fig1_heatmap_3child_box1.csv"
//      data-csv-label="Data (CSV)">
//     <img src="/figures/exhibits/E01-who-holds-more-3-children.png" alt="...">
//   </a>
// `data-csv-href`/`data-csv-label` are optional — omit both if the image has no underlying data
// file (e.g. a decorative or non-chart image); the modal's source line is hidden when absent.
// The exhibits gallery's own tile caption (`.exhibit-tile-caption`) is unrelated markup outside
// the trigger and is untouched by this script.
//
// Exactly one lightbox root per page, written once in `_layouts/default.html`:
//   <div class="lightbox" data-lightbox-root aria-hidden="true">
//     <div class="lightbox-dialog" role="dialog" aria-modal="true" aria-label="Exhibit image" tabindex="-1">
//       <button type="button" class="lightbox-close" data-lightbox-close aria-label="Close">&times;</button>
//       <img data-lightbox-image src="" alt="">
//       <p class="lightbox-caption" data-lightbox-caption></p>
//       <p class="lightbox-source"><a data-lightbox-csv href="#"></a></p>
//     </div>
//   </div>
//
// Behaviour: Escape and a click outside the dialog both close it. Focus moves into the dialog
// (the close button) on open and returns to the triggering element on close. The image is shown
// at its full rendered size, capped to the viewport (`.lightbox-dialog`/`.lightbox-dialog img` in
// site.css: max 94vw wide, 90vh tall dialog, image itself capped to 78vh so the caption stays
// visible without scrolling on most screens). Without JavaScript every trigger is a plain working
// `<a>` straight to the full-size PNG — never a broken control; the trigger's own keyboard
// behaviour (Tab to focus, Enter to activate) needs no extra work because it already is a link.
//
// FOCUS TRAP (2026-09-11, QA swarm, device-access F1): while the dialog is open, Tab and
// Shift+Tab cycle only among the dialog's own focusable elements (the close button and, when
// present, the CSV link) instead of escaping to the page underneath, which is still fully
// present in the DOM and still covered by the modal on screen. Before this fix, two Tabs from
// open moved focus onto the header nav links with nothing on screen to show where it went — the
// modal looked the same, but the keyboard was now operating a page the visitor could not see.
// The trap is recomputed on every open() (the CSV link's `hidden` state changes per image, so
// the "last focusable element" is not always the same node), and Escape still closes the dialog
// from anywhere inside it, per the existing behaviour above.

(function () {
  'use strict';

  var root = document.querySelector('[data-lightbox-root]');
  if (!root) return;

  var dialog = root.querySelector('.lightbox-dialog');
  var img = root.querySelector('[data-lightbox-image]');
  var caption = root.querySelector('[data-lightbox-caption]');
  var csvLink = root.querySelector('[data-lightbox-csv]');
  var csvPara = csvLink ? csvLink.parentNode : null; // .lightbox-source, hidden when no CSV
  var closeBtn = root.querySelector('[data-lightbox-close]');
  var lastTrigger = null;

  function open(trigger) {
    lastTrigger = trigger;
    img.src = trigger.getAttribute('href');
    img.alt = trigger.querySelector('img') ? trigger.querySelector('img').alt : '';
    caption.textContent = trigger.getAttribute('data-caption') || '';
    var csvHref = trigger.getAttribute('data-csv-href');
    if (csvLink && csvPara) {
      if (csvHref) {
        csvLink.setAttribute('href', csvHref);
        csvLink.textContent = trigger.getAttribute('data-csv-label') || 'Data (CSV)';
        csvPara.hidden = false;
      } else {
        csvPara.hidden = true;
      }
    }
    root.classList.add('is-open');
    root.removeAttribute('aria-hidden');
    (closeBtn || dialog).focus();
    document.addEventListener('keydown', onKeydown);
  }

  function close() {
    root.classList.remove('is-open');
    root.setAttribute('aria-hidden', 'true');
    img.src = '';
    document.removeEventListener('keydown', onKeydown);
    if (lastTrigger) lastTrigger.focus();
  }

  // The dialog's own focusable elements, in DOM (= visual) order, recomputed on every open()
  // since csvPara's `hidden` state (and so whether csvLink is focusable) changes per image.
  function focusableInDialog() {
    return Array.prototype.slice.call(dialog.querySelectorAll('button, a[href]'))
      .filter(function (el) { return !el.hidden && el.offsetParent !== null; });
  }

  function onKeydown(e) {
    if (e.key === 'Escape') { close(); return; }
    if (e.key !== 'Tab') return;
    var focusable = focusableInDialog();
    if (!focusable.length) { e.preventDefault(); dialog.focus(); return; }
    var first = focusable[0];
    var last = focusable[focusable.length - 1];
    var active = document.activeElement;
    if (e.shiftKey) {
      if (active === first || !dialog.contains(active)) { e.preventDefault(); last.focus(); }
    } else {
      if (active === last || !dialog.contains(active)) { e.preventDefault(); first.focus(); }
    }
  }

  document.querySelectorAll('[data-lightbox]').forEach(function (trigger) {
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      open(trigger);
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', close);

  // Click outside the dialog (on the backdrop) closes it.
  root.addEventListener('click', function (e) {
    if (e.target === root) close();
  });

  root.setAttribute('aria-hidden', 'true');
})();
