// checktheworksheet.org — petition sign-up: corner/bottom bar and the standalone /petition/
// page's own inline form. Loaded on every page, but only when site.petition_endpoint is set (see
// _layouts/default.html) -- with it empty, this file is never requested at all, which is the
// whole of the OFF state.
//
// The site is static (GitHub Pages), so the form's `action` points at a small purpose-built
// server, not a third-party form backend -- see _config.yml's `petition_endpoint` comment for the
// full request/response contract. This script is progressive enhancement on the SUBMIT step only:
// with it disabled, or before it loads, the `<form action="..." method="POST">` still submits for
// real (browsers default an unadorned POST form to application/x-www-form-urlencoded, which is
// exactly what the server expects) and the server 303-redirects back to
// /petition/?signed=1, which this same script recognizes on the next page load and turns into a
// thank-you line -- see initPetitionPage() below. Everything else here (the bottom bar, the inline
// fetch submit, the share step, the returning-signer state) is enhancement on top of a page that
// already works without it.
//
// A <dialog>-based popup (_includes/petition-modal.html) existed here through 2026-09-26 and was
// replaced by the bar below, which links straight to /petition/ instead of opening a popup. The
// modal markup is kept on disk (not deleted) but is never mounted from _layouts/default.html, so
// no dialog-open/close/focus-trap code has anything to attach to; that code was removed from this
// file as dead, design review 2026-09-26.
//
// ---------------------------------------------------------------------------------------------
// MARKUP CONTRACT
// ---------------------------------------------------------------------------------------------
// Bottom bar (_includes/petition-card.html), excluded on /petition/:
//   <div data-petition-card hidden aria-hidden="true">
//     <a data-petition-card-open>...</a>
//     <button data-petition-card-toggle>...</button>
//   </div>
// Always present until a signature (not a timed toast); minimizable, state persisted in
// localStorage. Signing anything, anywhere on the site, retires it for good.
//
// Standalone page (petition/index.md), only rendered there:
//   <div data-petition-form-wrap> <form data-petition-form> ... </form> </div>
//   <div data-petition-thankyou hidden>
//     ... <p data-petition-thankyou-message></p>
//     <p data-petition-returning hidden> <button data-petition-signagain>...</button> </p>
//     <div data-petition-share hidden>
//       <button data-petition-share-btn hidden>...</button>  (navigator.share path)
//       <button data-petition-copy-btn hidden>...</button>   (clipboard fallback -- never both)
//       <a data-petition-email-link>...</a>                  (always present, mailto:)
//     </div>
//   </div>
//   <p data-petition-count hidden></p>

(function () {
  'use strict';

  var SIGNED_KEY = 'ctw-petition-signed';
  var DISMISSED_KEY = 'ctw-petition-dismissed-until';
  var DISMISS_DAYS = 30;
  var SHOW_DELAY_MS = 25000;
  var SHOW_SCROLL_FRACTION = 0.40;
  var COUNT_MIN_TO_SHOW = 25;

  var DEFAULT_ERROR = "That didn't go through. Nothing you typed was lost. Try again in a moment.";
  var CONNECTION_ERROR = "That didn't go through. It looks like a connection problem. Nothing you typed was lost. Try again.";

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
        // "Sign", not "Petition" (design review 2026-09-26): the minimized label named the
        // topic rather than the action tapping it performs.
        toggle.innerHTML = min ? 'Sign &#9652;' : '<span aria-hidden="true">&ndash;</span>';
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

  // ---- share step, after a signature (2026-09-26) ------------------------------------------
  // A signer had no way to forward the petition -- a persona read of this page (a father who
  // came specifically to sign and send it to his brother) confirmed it as a task-blocking gap,
  // not a nicety: a petition's value compounds through forwarding. Feature-detected at render
  // time, never both buttons at once. No third-party embeds; nothing here calls the Fly server.
  var PETITION_URL = 'https://checktheworksheet.org/petition/';
  var SHARE_TEXT = 'Massachusetts child support is among the highest in the nation, and the guidelines do not comply with federal law.';
  var shareWired = false;

  function wireShare() {
    if (shareWired) return;
    shareWired = true;
    var shareBlock = document.querySelector('[data-petition-share]');
    if (!shareBlock) return;
    var shareBtn = shareBlock.querySelector('[data-petition-share-btn]');
    var copyBtn = shareBlock.querySelector('[data-petition-copy-btn]');
    var emailLink = shareBlock.querySelector('[data-petition-email-link]');

    if (typeof navigator.share === 'function' && shareBtn) {
      shareBtn.hidden = false;
      shareBtn.addEventListener('click', function () {
        navigator.share({ title: document.title, text: SHARE_TEXT, url: PETITION_URL }).catch(function () {
          /* user cancelled the share sheet, or the browser refused -- nothing to recover, the
             copy-link and email routes are still on screen */
        });
      });
    } else if (copyBtn) {
      copyBtn.hidden = false;
      var copyOriginalText = copyBtn.textContent;
      copyBtn.addEventListener('click', function () {
        var done = function () {
          copyBtn.textContent = 'Link copied';
          setTimeout(function () { copyBtn.textContent = copyOriginalText; }, 2000);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(PETITION_URL).then(done, done);
        } else {
          done(); // clipboard API unavailable -- nothing better to fall back to here
        }
      });
    }

    if (emailLink) {
      var subject = encodeURIComponent('Sign the Massachusetts child support petition');
      var body = encodeURIComponent(SHARE_TEXT + ' Sign the petition: ' + PETITION_URL);
      emailLink.setAttribute('href', 'mailto:?subject=' + subject + '&body=' + body);
    }
  }

  function revealShare() {
    var shareBlock = document.querySelector('[data-petition-share]');
    if (shareBlock) { wireShare(); shareBlock.hidden = false; }
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
    revealShare();
  }

  // ---- returning signer (2026-09-26) --------------------------------------------------------
  // A signer who comes back to /petition/ directly (bookmark, the footer link, a second visit)
  // saw the identical blank form a first-time visitor sees, with nothing acknowledging they'd
  // already signed. isSigned() is the same localStorage flag the bar itself already reads.
  function showAlreadySigned() {
    retireCard();
    var wrap = document.querySelector('[data-petition-form-wrap]');
    var thankYou = document.querySelector('[data-petition-thankyou]');
    if (wrap) wrap.hidden = true;
    if (thankYou) {
      var messageEl = thankYou.querySelector('[data-petition-thankyou-message]');
      if (messageEl) messageEl.textContent = "You've already signed this petition from this device.";
      var returning = thankYou.querySelector('[data-petition-returning]');
      if (returning) returning.hidden = false;
      thankYou.hidden = false;
      thankYou.setAttribute('tabindex', '-1');
      thankYou.focus();
    }
    revealShare();
    var again = document.querySelector('[data-petition-signagain]');
    if (again) {
      again.addEventListener('click', function () {
        if (wrap) wrap.hidden = false;
        if (thankYou) thankYou.hidden = true;
        var nameField = document.querySelector('#petition-name');
        if (nameField) nameField.focus();
      });
    }
  }

  // ---- source page: which page's bar or link led here (2026-09-26) -------------------------
  // The server records this on every signature for the admin dashboard's provenance column. A
  // referrer from THIS SITE names the page the signer came from (its path, not the full URL --
  // no query string, no host, nothing that could carry a visitor's own data); a referrer from
  // elsewhere, or none at all (direct link, a saved bookmark, a browser that blocks referrers),
  // falls back to the current page's own path so the field is never empty on this site's own
  // standalone /petition/ page.
  function sourcePath() {
    try {
      var ref = document.referrer;
      if (ref) {
        var refUrl = new URL(ref);
        if (refUrl.host === window.location.host) return refUrl.pathname;
      }
    } catch (e) { /* malformed or inaccessible referrer -- fall through */ }
    return window.location.pathname;
  }

  function wireForm(form) {
    var honeypot = form.querySelector('input[name="_gotcha"]');
    var errorEl = form.querySelector('[data-petition-error]');
    var submitButton = form.querySelector('button[type="submit"]');
    var sourceField = form.querySelector('[data-petition-source]');
    if (sourceField) sourceField.value = sourcePath();

    // ZIP field: the browser's own validation message ("Please match the requested format.")
    // says nothing about what format is expected once the 02108 placeholder is covered by a
    // typed value. A custom message, worded the same way a server error reads. Design review
    // 2026-09-26.
    var zipField = form.querySelector('input[name="zip"]');
    if (zipField) {
      zipField.addEventListener('invalid', function () {
        zipField.setCustomValidity('Enter a five-digit ZIP code.');
      });
      zipField.addEventListener('input', function () { zipField.setCustomValidity(''); });
    }

    function resetButton() {
      if (!submitButton) return;
      submitButton.textContent = submitButton.dataset.originalText || 'Sign the petition';
      submitButton.removeAttribute('aria-busy');
      submitButton.disabled = false;
    }

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
      if (submitButton) {
        // The Fly server sleeps when idle; the first submit after idle takes ~1-2s with no other
        // on-screen change. "Signing…" is the one thing that tells a visitor on a slow
        // connection the click registered, rather than nothing happening. Re-enabled only on
        // error -- on success the form itself is hidden by onSigned(), so there is nothing left
        // to re-enable. Design review 2026-09-26.
        submitButton.dataset.originalText = submitButton.dataset.originalText || submitButton.textContent;
        submitButton.textContent = 'Signing…';
        submitButton.setAttribute('aria-busy', 'true');
        submitButton.disabled = true;
      }

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
          } else {
            resetButton();
            if (errorEl) {
              errorEl.textContent = (result.data && result.data.error) || DEFAULT_ERROR;
              errorEl.hidden = false;
            }
          }
        })
        .catch(function () {
          resetButton();
          if (errorEl) {
            errorEl.textContent = CONNECTION_ERROR;
            errorEl.hidden = false;
          }
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
    } else if (isSigned()) {
      // A returning signer (bookmark, footer link, second visit) landing directly on /petition/,
      // outside the post-submit redirect above. Design review 2026-09-26.
      showAlreadySigned();
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
