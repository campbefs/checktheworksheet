// checktheworksheet.org — contact form submit handling (contact/index.md only, loaded via that
// page's `scripts:` front matter, same opt-in pattern as csv-slider.js / lightbox.js).
//
// The site is static (GitHub Pages), so the form's `action` already points at a third-party form
// backend — see `_config.yml`'s `contact_form_endpoint` for the single place that URL lives, and
// `docs/plans/redteam/CONTACT-FORM.md` in the private repo for how the provider was chosen. This
// script is progressive enhancement ONLY: with it disabled, or before it loads, the `<form
// action="..." method="POST">` on the page still submits for real and lands on the provider's own
// confirmation page. This script's whole job is to intercept that same submit, send it with
// `fetch` instead so the reader never leaves the page, and show a toast in its place.
//
// ---------------------------------------------------------------------------------------------
// MARKUP CONTRACT
// ---------------------------------------------------------------------------------------------
//   <form class="contact-form" data-contact-form action="<provider endpoint>" method="POST">
//     ...real fields...
//     <input type="text" name="_gotcha" class="form-field--honeypot" tabindex="-1" aria-hidden="true">
//     <button type="submit">Send</button>
//   </form>
//   <div class="toast" data-contact-toast role="status" aria-live="polite" hidden>
//     <p data-contact-toast-message></p>
//     <button type="button" data-contact-toast-close aria-label="Dismiss">&times;</button>
//   </div>
// The toast is one shared element for both outcomes; `.is-error` plus a `role="alert"` swap (set
// only while an error is showing, so it interrupts a screen reader the way a status message
// should not) is how the two states differ — never colour alone (WCAG 1.4.1), so the wording
// itself always says success or failure in plain words, not only the rule colour along its edge.

(function () {
  'use strict';

  var form = document.querySelector('[data-contact-form]');
  if (!form) return;

  var toast = document.querySelector('[data-contact-toast]');
  var toastMessage = toast ? toast.querySelector('[data-contact-toast-message]') : null;
  var toastClose = toast ? toast.querySelector('[data-contact-toast-close]') : null;
  var submitButton = form.querySelector('button[type="submit"]');
  var honeypot = form.querySelector('input[name="_gotcha"]');
  var toastTimer = null;

  var hideToast = function () {
    if (!toast) return;
    toast.hidden = true;
    toast.classList.remove('is-error');
    toast.removeAttribute('role');
    if (toastTimer) {
      window.clearTimeout(toastTimer);
      toastTimer = null;
    }
  };

  var showToast = function (message, isError) {
    if (!toast || !toastMessage) return;
    toastMessage.textContent = message;
    toast.classList.toggle('is-error', !!isError);
    // A failure interrupts (role="alert" implies aria-live="assertive"); a success is announced
    // politely once the reader is free, via the aria-live="polite" already on the element in
    // markup. Only one of the two is present at a time.
    if (isError) {
      toast.setAttribute('role', 'alert');
    } else {
      toast.setAttribute('role', 'status');
    }
    toast.hidden = false;
    if (toastTimer) window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(hideToast, 10000);
  };

  if (toastClose) toastClose.addEventListener('click', hideToast);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && toast && !toast.hidden) hideToast();
  });

  form.addEventListener('submit', function (e) {
    // Honeypot: a real visitor never fills this in (it's visually hidden and out of the tab
    // order — see .form-field--honeypot in site.css). If it's filled, this is a bot filling every
    // field it can see in the DOM; drop the submission client-side rather than sending it, and
    // say nothing further. A human never reaches this branch.
    if (honeypot && honeypot.value) {
      e.preventDefault();
      return;
    }

    e.preventDefault();
    if (submitButton) submitButton.disabled = true;

    var formData = new FormData(form);
    fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: { Accept: 'application/json' }
    })
      .then(function (response) {
        if (response.ok) {
          form.reset();
          showToast('Sent. Please allow 48 hours for a reply.', false);
        } else {
          showToast(
            "That didn't go through. Nothing you typed was lost — try Send again in a moment.",
            true
          );
        }
      })
      .catch(function () {
        showToast(
          "That didn't go through, probably a connection problem. Nothing you typed was lost — try Send again.",
          true
        );
      })
      .then(function () {
        if (submitButton) submitButton.disabled = false;
      });
  });
})();
