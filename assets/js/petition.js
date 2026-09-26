// checktheworksheet.org — petition sign-up: header trigger, corner card, dialog, and the
// standalone /petition/ page's own inline form. Loaded on every page, but only when
// site.petition_endpoint is set (see _layouts/default.html) -- with it empty, this file is never
// requested at all, which is the whole of the OFF state.
//
// The site is static (GitHub Pages), so the form's `action` points at a small purpose-built
// server, not a third-party form backend -- see _config.yml's `petition_endpoint` comment for the
// full request/response contract. This script is progressive enhancement on the SUBMIT step only:
// with it disabled, or before it loads, the `<form action="..." method="POST">` still submits for
// real (browsers default an unadorned POST form to application/x-www-form-urlencoded, which is
// exactly what the server expects) and the server 303-redirects back to
// /petition/?signed=1, which this same script recognizes on the next page load and turns into a
// thank-you line -- see initPetitionPage() below. Everything else here (the header trigger
// opening a dialog instead of navigating, the corner card, the inline fetch submit) is enhancement
// on top of a page that already works without it.
//
// ---------------------------------------------------------------------------------------------
// MARKUP CONTRACT
// ---------------------------------------------------------------------------------------------
// Dialog (_includes/petition-modal.html), mounted on every page except /petition/ itself:
//   <dialog data-petition-dialog aria-labelledby="...">
//     <button data-petition-close>...</button>
//     <div data-petition-form-wrap> <form data-petition-form> ...fields..., name="_gotcha"
//       honeypot, <p data-petition-error role="alert" hidden> </form> </div>
//     <div data-petition-thankyou hidden> ... <p data-petition-thankyou-message></p> </div>
//   </dialog>
// A real <dialog>, opened with showModal() -- while open, the browser keeps focus inside it and
// makes the rest of the document inert, so unlike lightbox.js's plain <div role="dialog"> this
// needs no hand-rolled Tab trap. Escape fires the dialog's native "cancel" then "close" events;
// this script does not intercept "cancel", only listens to "close" to return focus to whichever
// element opened it.
//
// Corner card (_includes/petition-card.html), mounted the same way, also excluded on /petition/:
//   <div data-petition-card hidden aria-hidden="true">
//     <button data-petition-card-dismiss>...</button>
//     <p>...</p>
//     <button data-petition-card-open>...</button>
//   </div>
// Shown once per visitor, after ~25 seconds or 40% scroll depth, whichever comes first -- never
// on page load, and never blocking (it is a plain positioned div, not a dialog). Dismissing it is
// remembered 30 days in localStorage; signing anything, anywhere on the site, hides it for good.
//
// Standalone page (petition/index.md), only rendered there:
//   <div data-petition-form-wrap> <form data-petition-form> ... </form> </div>
//   <div data-petition-thankyou hidden> ... <p data-petition-thankyou-message></p> </div>
//   <p data-petition-count hidden></p>
// The same [data-petition-form-wrap]/[data-petition-thankyou] pair the dialog uses, which is what
// lets one submit handler serve both. At most one [data-petition-form] ever exists on a page --
// the dialog's, or the standalone page's, never both, because _includes/petition-modal.html
// excludes itself on /petition/ -- so this script queries for these elements globally (document-
// wide) rather than scoping each lookup to a particular container.
//
// Any element anywhere on the page with `data-petition-trigger` opens the dialog if one exists on
// that page (header.html's own button carries it); if none exists (e.g. already on /petition/, or
// the browser has no <dialog>/showModal support), the click is left alone and the element's own
// `href` does the navigating.

(function () {
  'use strict';

  var SIGNED_KEY = 'ctw-petition-signed';
  var DISMISSED_KEY = 'ctw-petition-dismissed-until';
  var DISMISS_DAYS = 30;
  var SHOW_DELAY_MS = 25000;
  var SHOW_SCROLL_FRACTION = 0.40;
  var COUNT_MIN_TO_SHOW = 25;

  var DEFAULT_ERROR = "That didn't go through. Nothing you typed was lost. Try again in a moment.";
  var CONNECTION_ERROR = "That didn't go through, probably a connection problem. Nothing you typed was lost. Try again.";

  // ---- localStorage, defensive: private-browsing Safari throws on access, not just on quota ----
  function safeGet(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }
  function safeSet(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) { /* ignore, not load-bearing */ }
  }
  function isSigned() { return safeGet(SIGNED_KEY) === '1'; }
  function markSigned() { safeSet(SIGNED_KEY, '1'); }
  function isDismissed() {
    var until = parseInt(safeGet(DISMISSED_KEY), 10);
    return !isNaN(until) && Date.now() < until;
  }
  function markDismissed() {
    safeSet(DISMISSED_KEY, String(Date.now() + DISMISS_DAYS * 24 * 60 * 60 * 1000));
  }

  // ---- hide the corner card for good, e.g. right after a signature -------------------------
  function retireCard() {
    var card = document.querySelector('[data-petition-card]');
    if (!card) return;
    card.classList.remove('is-visible');
    card.hidden = true;
    card.setAttribute('aria-hidden', 'true');
    document.documentElement.classList.remove('has-petition-bar');
  }

  // ---- dialog: open/close, focus management -------------------------------------------------
  var dialog = document.querySelector('[data-petition-dialog]');
  var lastTrigger = null;

  function openDialog(triggerEl) {
    if (!dialog || typeof dialog.showModal !== 'function') return;
    lastTrigger = triggerEl || null;
    dialog.showModal();
    var firstField = dialog.querySelector('input[name="name"]');
    var closeBtn = dialog.querySelector('[data-petition-close]');
    if (firstField && firstField.offsetParent !== null) {
      firstField.focus();
    } else if (closeBtn) {
      closeBtn.focus();
    }
  }

  if (dialog) {
    dialog.addEventListener('close', function () {
      if (lastTrigger && typeof lastTrigger.focus === 'function') lastTrigger.focus();
    });
    // A click on the ::backdrop registers with the dialog element itself as the target, since the
    // backdrop is not a separate node in the DOM -- a click on the dialog's own visible content
    // lands on one of its descendants instead, so this only fires for a true outside click.
    dialog.addEventListener('click', function (e) {
      if (e.target === dialog) dialog.close();
    });
    var closeBtn = dialog.querySelector('[data-petition-close]');
    if (closeBtn) closeBtn.addEventListener('click', function () { dialog.close(); });
  }

  document.querySelectorAll('[data-petition-trigger]').forEach(function (trigger) {
    trigger.addEventListener('click', function (e) {
      if (!dialog || typeof dialog.showModal !== 'function') return; // let the href navigate
      e.preventDefault();
      openDialog(trigger);
    });
  });

  // ---- petition bar: always present until a signature, minimizable (2026-09-26) ------------
  // Replaces the timed corner card. Shown on load, never over the text: the page reserves the
  // bar's measured height as bottom padding. Minimized state persists; a signature retires it.
  var card = document.querySelector('[data-petition-card]');
  var MIN_KEY = 'ctw-petition-bar-min';
  if (card && !isSigned()) {
    var toggle = card.querySelector('[data-petition-card-toggle]');
    var root = document.documentElement;
    var measure = function () { root.style.setProperty('--petition-bar-h', card.offsetHeight + 'px'); };
    var setMin = function (min) {
      card.classList.toggle('is-min', min);
      if (toggle) {
        toggle.setAttribute('aria-expanded', min ? 'false' : 'true');
        toggle.setAttribute('aria-label', min ? 'Show the petition bar' : 'Minimize the petition bar');
        toggle.innerHTML = min ? 'Petition &#9652;' : '<span aria-hidden="true">&ndash;</span>';
      }
      safeSet(MIN_KEY, min ? '1' : '0');
      measure();
    };
    card.hidden = false;
    card.removeAttribute('aria-hidden');
    root.classList.add('has-petition-bar');
    setMin(safeGet(MIN_KEY) === '1');
    if (toggle) toggle.addEventListener('click', function () { setMin(!card.classList.contains('is-min')); });
    if (window.ResizeObserver) new ResizeObserver(measure).observe(card);
    else window.addEventListener('resize', measure);
  } else if (card) {
    retireCard();
  }

  // ---- form submit: honeypot, fetch, thank-you state, error state ---------------------------
  function parseJsonSafe(response) {
    return response.json().then(function (data) { return data; }, function () { return {}; });
  }

  function onSigned(count) {
    markSigned();
    retireCard();
    var wrap = document.querySelector('[data-petition-form-wrap]');
    var thankYou = document.querySelector('[data-petition-thankyou]');
    if (wrap) wrap.hidden = true;
    if (thankYou) {
      var message = 'Your name has been added to the petition.';
      if (typeof count === 'number') {
        message += ' ' + count + (count === 1 ? ' person has' : ' people have') + ' signed so far.';
      }
      var messageEl = thankYou.querySelector('[data-petition-thankyou-message]');
      if (messageEl) messageEl.textContent = message;
      thankYou.hidden = false;
      thankYou.setAttribute('tabindex', '-1');
      thankYou.focus();
    }
  }

  function wireForm(form) {
    var honeypot = form.querySelector('input[name="_gotcha"]');
    var errorEl = form.querySelector('[data-petition-error]');
    var submitButton = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function (e) {
      // Honeypot: a real visitor never fills this in (it's visually hidden and out of the tab
      // order -- .form-field--honeypot in site.css). If it's filled, a bot filled every field it
      // could see in the DOM; drop the submission client-side and say nothing further, the same
      // way assets/js/contact.js does.
      if (honeypot && honeypot.value) {
        e.preventDefault();
        return;
      }

      e.preventDefault();
      if (errorEl) { errorEl.hidden = true; errorEl.textContent = ''; }
      if (submitButton) submitButton.disabled = true;

      var formData = new FormData(form);
      var params = new URLSearchParams();
      formData.forEach(function (value, key) { params.append(key, value); });

      fetch(form.action, {
        method: 'POST',
        body: params.toString(),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          Accept: 'application/json'
        }
      })
        .then(function (response) {
          return parseJsonSafe(response).then(function (data) {
            return { ok: response.ok, data: data };
          });
        })
        .then(function (result) {
          if (result.ok && result.data && result.data.ok) {
            onSigned(typeof result.data.count === 'number' ? result.data.count : null);
          } else if (errorEl) {
            errorEl.textContent = (result.data && result.data.error) || DEFAULT_ERROR;
            errorEl.hidden = false;
          }
        })
        .catch(function () {
          if (errorEl) {
            errorEl.textContent = CONNECTION_ERROR;
            errorEl.hidden = false;
          }
        })
        .then(function () {
          if (submitButton) submitButton.disabled = false;
        });
    });
  }

  document.querySelectorAll('[data-petition-form]').forEach(wireForm);

  // ---- the standalone /petition/ page: the no-JS-submit redirect, and the ambient count -----
  function initPetitionPage() {
    if (window.location.pathname !== '/petition/') return;

    // A visitor whose browser posted the form for real (JavaScript disabled, or loaded after the
    // submit already happened) lands back here at ?signed=1 -- turn that into the same thank-you
    // state a fetch-handled submit shows, rather than leaving a bare query string on the page.
    if (window.location.search.indexOf('signed=1') !== -1) {
      onSigned(null);
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, '', window.location.pathname);
      }
    }

    var countEl = document.querySelector('[data-petition-count]');
    var form = document.querySelector('[data-petition-form]');
    if (!countEl || !form || !form.action) return;
    var countUrl = form.action.replace(/\/sign\/?$/, '/count');
    if (countUrl === form.action) return; // action didn't end in /sign -- nothing to derive

    fetch(countUrl, { headers: { Accept: 'application/json' } })
      .then(function (response) { return response.ok ? response.json() : null; })
      .then(function (data) {
        if (data && typeof data.count === 'number' && data.count >= COUNT_MIN_TO_SHOW) {
          countEl.textContent = data.count + ' people have signed.';
          countEl.hidden = false;
        }
      })
      .catch(function () { /* leave it hidden -- an ambient count is a nicety, not a promise */ });
  }

  initPetitionPage();
})();
