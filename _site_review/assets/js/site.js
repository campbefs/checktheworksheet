// checktheworksheet.org — site-wide scaffolding, loaded on every page (see _layouts/default.html).
// Vanilla JS, no dependencies, no CDN, no build step. Everything here is defensive: it checks for
// its target elements before doing anything, so it is harmless on a page that has none of them
// (e.g. the reading-progress bar and chapter-rail tracking do nothing on the home page, which has
// no `.chapter-rail`; the nav-toggle bookkeeping does nothing if the checkbox isn't present).
//
// Heavier, page-specific interactive exhibits (the two-income calculator, the child-care and
// credit-collapse sliders, the sortable fifty-jurisdiction table, the exhibit lightbox) are
// separate opt-in files — csv-slider.js, sortable-table.js, lightbox.js — loaded only by the
// pages that use them via that page's `scripts:` front matter. Keeping them out of this file
// means a page that doesn't need them doesn't pay for them.

(function () {
  'use strict';

  // ---- reading progress bar (the <960px chapter-rail replacement, design brief §3.3) ----
  var bar = document.querySelector('.progress-bar');
  if (bar) {
    var updateProgress = function () {
      var scrolled = window.scrollY;
      var height = document.documentElement.scrollHeight - window.innerHeight;
      var pct = height > 0 ? (scrolled / height) * 100 : 0;
      bar.style.width = pct.toFixed(1) + '%';
    };
    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress);
    updateProgress();
  }

  // ---- chapter rail: tracks scroll position via IntersectionObserver ----
  // Progressive enhancement only. Without this script the rail (built in
  // _includes/chapter-rail.html from a page's own `sections:` front matter) is already a
  // complete, working list of `href="#id"` anchor links — this only adds the scroll-tracked
  // `aria-current="location"` marker on top (design brief §3.4).
  var railLinks = document.querySelectorAll('.chapter-rail a[href^="#"]');
  if (railLinks.length && 'IntersectionObserver' in window) {
    var sections = [];
    railLinks.forEach(function (link) {
      var id = link.getAttribute('href').slice(1);
      var el = document.getElementById(id);
      if (el) sections.push(el);
    });

    var setActive = function (id) {
      railLinks.forEach(function (l) {
        if (l.getAttribute('href') === '#' + id) {
          l.setAttribute('aria-current', 'location');
        } else {
          l.removeAttribute('aria-current');
        }
      });
    };

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) setActive(entry.target.id);
        });
      },
      { rootMargin: '-15% 0px -70% 0px', threshold: 0 }
    );
    sections.forEach(function (el) { observer.observe(el); });
  }

  // ---- top-bar nav toggle: aria-expanded bookkeeping only ----
  // The checkbox + label in _includes/header.html is the entire functional mechanism (CSS
  // :checked selector, no JS needed for the toggle itself to work, and it degrades to "always
  // visible, wraps normally" above 640px). This just keeps `aria-expanded` on the label in sync
  // for assistive tech, and closes the panel on Escape.
  var navToggle = document.getElementById('nav-toggle');
  if (navToggle) {
    var navLabel = document.querySelector('label[for="nav-toggle"]');
    var syncExpanded = function () {
      if (navLabel) navLabel.setAttribute('aria-expanded', navToggle.checked ? 'true' : 'false');
    };
    navToggle.addEventListener('change', syncExpanded);
    syncExpanded();
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && navToggle.checked) {
        navToggle.checked = false;
        syncExpanded();
      }
    });
  }
})();
