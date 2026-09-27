---
layout: page
title: Sign the petition
description: >-
  Sign the petition asking Massachusetts and the federal government to correct the child support
  guidelines now.
permalink: /petition/
---

# Sign the petition to fix the Massachusetts child support guidelines

To the Chief Justice of the Trial Court, the Governor of Massachusetts, and the U.S. Department of
Health and Human Services. We believe federal law requires every child support order to rest on what a parent can actually pay, and that Massachusetts has never been asked whether its guidelines do that. No court or federal agency has ruled on whether the guidelines meet this standard. Federal approval of the state's plan has not addressed it. We ask that they be corrected now, and that every parent whose order was set under them be allowed to apply for immediate relief.

{% if site.petition_endpoint != "" %}
<div class="petition-layout" markdown="0">

<aside class="petition-why">
  <h2>Why this matters</h2>
  <ul>
    <li>Massachusetts charges more for joint custody than 47 states charge when the recipient has
      primary custody. <a href="{{ '/findings/fifty-one-jurisdictions/' | relative_url }}">See the comparison &rarr;</a></li>
    <li>With $100 a week of child care claimed per child, 40 percent of three-child, primary-custody
      income pairs on a model grid have an order that takes more than half of take-home pay, and 10.6
      percent cross 60 percent, the actual federal limit on what can be withheld from wages. All of
      those also trip Massachusetts's own 40 percent hardship presumption, which helps only if the parent raises it and a judge agrees.
      <a href="{{ '/findings/federal-law/' | relative_url }}">See the finding &rarr;</a></li>
    <li>The Worksheet never computes what a parent keeps after tax.
      <a href="{{ '/findings/federal-law/' | relative_url }}">See the finding &rarr;</a></li>
  </ul>
</aside>

<div class="petition-main">

<p class="form-note petition-count" data-petition-count hidden></p>

<div data-petition-form-wrap>
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
  <input type="hidden" name="source" data-petition-source value="">
  <input type="text" name="_gotcha" class="form-field--honeypot" tabindex="-1" aria-hidden="true" autocomplete="off">
  <p class="petition-form-error" data-petition-error role="alert" hidden></p>
  <div class="form-actions">
    <button type="submit" class="btn">Sign the petition</button>
  </div>
  <p class="form-note">
    Your name, email and ZIP are used to count signatures and to show officials how many signers
    live in Massachusetts. They are never sold or shared for any other purpose. Your name is never
    shown publicly. There is no public list of signers on this site. You get no email unless you
    check the updates box. To remove your signature, write to
    <a href="mailto:checktheworksheet@gmail.com">checktheworksheet@gmail.com</a>.
  </p>
</form>
</div>

<div class="disclosure petition-thankyou" data-petition-thankyou hidden>
  <div class="box">
    <h2>Thank you for signing.</h2>
    <p data-petition-thankyou-message>Your name has been added to the petition.</p>
    <p class="petition-returning" data-petition-returning hidden>
      <button type="button" data-petition-signagain>Sign again from another address</button>
    </p>
    <div class="petition-share" data-petition-share hidden>
      <p>Ask two more Massachusetts parents to sign.</p>
      <button type="button" class="btn" data-petition-share-btn hidden>Share the petition</button>
      <button type="button" class="btn" data-petition-copy-btn hidden>Copy link</button>
      <p class="petition-share-links">
        <a data-petition-email-link href="#">Email it</a>
      </p>
    </div>
  </div>
</div>

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
