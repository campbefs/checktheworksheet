---
layout: page
title: Contact
permalink: /contact/
description: >-
  Report an error in the arithmetic, a broken link, or a question, without an email address on
  the page. Goes to the site's owner. Allow 48 hours for a reply.
scripts:
  - "/assets/js/contact.js"
---

# Report an error, or ask a question, without an email address on the page

This site's whole pitch is that a reader can check the arithmetic. If a number, a link, or a
script doesn't hold up, this is the fastest way to say where.

<form class="contact-form" data-contact-form action="{{ site.contact_form_endpoint }}" method="POST">
  <div class="form-field">
    <label for="contact-subject">Subject</label>
    <input type="text" id="contact-subject" name="subject" required maxlength="200" autocomplete="off">
  </div>

  <div class="form-field">
    <label for="contact-message">Message</label>
    <textarea id="contact-message" name="message" rows="8" required></textarea>
  </div>

  <div class="form-field">
    <label for="contact-email">Your email <span class="field-optional">(optional, only if you want a reply)</span></label>
    <input type="email" id="contact-email" name="email" autocomplete="email">
  </div>

  <div class="form-field form-field--honeypot" aria-hidden="true">
    <label for="contact-company">Leave this field blank</label>
    <input type="text" id="contact-company" name="_gotcha" tabindex="-1" autocomplete="off">
  </div>

  <input type="hidden" name="_subject" value="checktheworksheet.org contact form">

  <div class="form-actions">
    <button type="submit" class="btn">Send</button>
    <p class="form-note">Goes to the site's owner, not posted anywhere. Allow 48 hours for a reply.</p>
  </div>
</form>

<div class="toast" data-contact-toast role="status" aria-live="polite" hidden>
  <p data-contact-toast-message></p>
  <button type="button" class="toast-close" data-contact-toast-close aria-label="Dismiss">&times;</button>
</div>

<div class="ask">
  <h2>Looking to check a figure instead?</h2>
  <ul>
    <li><a href="/the-model/">The model</a></li>
    <li><a href="/the-data/">The data</a></li>
    <li><a href="/findings/">The findings</a></li>
  </ul>
</div>
