---
layout: page
title: Sign the petition
description: >-
  Sign the petition asking Massachusetts and the federal government to correct the child support
  guidelines now.
permalink: /petition/
---

# Sign the petition: the Massachusetts child support guidelines need immediate reform.

To the Chief Justice of the Trial Court, the Governor of Massachusetts, and the U.S. Department of
Health and Human Services. The Massachusetts child support guidelines do not comply with federal
law. We ask that they be corrected now, and that every parent whose order was set under them be
allowed to apply for immediate relief.

{% if site.petition_endpoint != "" %}
<p class="form-note petition-count" data-petition-count hidden></p>

<div data-petition-form-wrap markdown="0">
<form class="petition-form contact-form" data-petition-form action="{{ site.petition_endpoint }}" method="POST">
  <div class="form-field">
    <label for="petition-name">Full name</label>
    <input type="text" id="petition-name" name="name" required autocomplete="name">
  </div>
  <div class="form-field">
    <label for="petition-email">Email</label>
    <input type="email" id="petition-email" name="email" required autocomplete="email">
  </div>
  <div class="form-field">
    <label for="petition-zip">ZIP code</label>
    <input type="text" id="petition-zip" name="zip" required inputmode="numeric"
           pattern="^\d{5}(-\d{4})?$" placeholder="02108" autocomplete="postal-code">
  </div>
  <div class="form-field">
    <label class="form-checkbox" for="petition-updates">
      <input type="checkbox" id="petition-updates" name="updates">
      <span>Email me updates about this petition</span>
    </label>
  </div>
  <div class="form-field">
    <label class="form-checkbox" for="petition-public">
      <input type="checkbox" id="petition-public" name="public">
      <span>Show my name publicly as a signer</span>
    </label>
  </div>
  <input type="text" name="_gotcha" class="form-field--honeypot" tabindex="-1" aria-hidden="true" autocomplete="off">
  <p class="petition-form-error" data-petition-error role="alert" hidden></p>
  <div class="form-actions">
    <button type="submit" class="btn">Sign the petition</button>
  </div>
  <p class="form-note">
    Your name, email and ZIP are used to count signatures and to show officials how many signers
    live in Massachusetts. They are never sold or shared for any other purpose. Your name is shown
    publicly only if you check the box. You get no email unless you check the updates box. To
    remove your signature, write to
    <a href="mailto:checktheworksheet@gmail.com">checktheworksheet@gmail.com</a>.
  </p>
</form>
</div>

<div class="disclosure petition-thankyou" data-petition-thankyou hidden markdown="0">
  <div class="box">
    <h2>Thank you for signing.</h2>
    <p data-petition-thankyou-message>Your name has been added to the petition.</p>
  </div>
</div>
{% else %}
<div class="disclosure" markdown="0">
  <div class="box">
    <p><strong>Signing opens soon.</strong> The form is not live yet. Write to
    <a href="mailto:checktheworksheet@gmail.com">checktheworksheet@gmail.com</a> with any
    questions in the meantime.</p>
  </div>
</div>
{% endif %}
