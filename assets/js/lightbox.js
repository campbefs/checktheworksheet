// checktheworksheet.org — hand-rolled, dependency-free lightbox for the exhibits gallery (design
// brief §3.8). Real DOM (an <img> inside a positioned <div>), not a canvas widget, so it is
// reachable and readable exactly like the rest of the page. Vanilla JS, no dependencies, no CDN.
//
// ---------------------------------------------------------------------------------------------
// MARKUP CONTRACT — exhibits.html builds one of these
// ---------------------------------------------------------------------------------------------
// Trigger tiles, anywhere on the page:
//   <a class="exhibit-tile" href="/figures/exhibits/E01-who-holds-more-3-children.png"
//      data-lightbox data-caption="E01 — With three children, the recipient household holds more
//      after the order in 55 percent of the income combinations modelled.">
//     <img src="/figures/exhibits/E01-who-holds-more-3-children.png" alt="...">
//     <span class="exhibit-tile-caption"><strong>E01</strong> One-line caption</span>
//   </a>
//
// Exactly one lightbox root per page, placed once, anywhere (e.g. right before </main>):
//   <div class="lightbox" data-lightbox-root>
//     <div class="lightbox-dialog" role="dialog" aria-modal="true" aria-label="Exhibit image" tabindex="-1">
//       <button type="button" class="lightbox-close" data-lightbox-close aria-label="Close">&times;</button>
//       <img data-lightbox-image src="" alt="">
//       <p class="lightbox-caption" data-lightbox-caption></p>
//     </div>
//   </div>
//
// Behaviour: Escape and a click outside the dialog both close it (design brief §3.8 — explorer's
// mockup skipped both; build them in). Focus moves into the dialog (the close button) on open and
// returns to the triggering tile on close. Without JavaScript every trigger is a plain working
// link straight to the full-size PNG — never a broken control.
//
// A page opts in with `scripts: ["/assets/js/lightbox.js"]` in front matter.

(function () {
  'use strict';

  var root = document.querySelector('[data-lightbox-root]');
  if (!root) return;

  var dialog = root.querySelector('.lightbox-dialog');
  var img = root.querySelector('[data-lightbox-image]');
  var caption = root.querySelector('[data-lightbox-caption]');
  var closeBtn = root.querySelector('[data-lightbox-close]');
  var lastTrigger = null;

  function open(trigger) {
    lastTrigger = trigger;
    img.src = trigger.getAttribute('href');
    img.alt = trigger.querySelector('img') ? trigger.querySelector('img').alt : '';
    caption.textContent = trigger.getAttribute('data-caption') || '';
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

  function onKeydown(e) {
    if (e.key === 'Escape') close();
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
