// checktheworksheet.org -- faithful JavaScript port of model/net_position.py's TY2026 tax
// constants and functions, for the "true share of net income" readout on the home-page
// two-income calculator.
//
// THIS IS A PORT, NOT A REIMPLEMENTATION. Every constant and function below corresponds to the
// same-named constant/function in model/net_position.py (read that file's own docstring and
// comments for what each one means and where it was verified -- not repeated here). Do not
// change a number here without making the identical change there.
//
// TESTED FIDELITY (assets/js/calculator.test.js, run with `node assets/js/calculator.test.js`):
// reproduces the worked example's tax position from model/runs/submission-figures-run-2026-09-05.txt
// (payor effective rate +30.4%, recipient effective rate -38.9%, payor keeps $87,172 with no
// child care) to the cent.
//
// Usage (browser): <script src="/assets/js/lib/net-position.js"></script> attaches
// `window.MCSGNetPosition` (requires nothing else). Usage (Node, for tests):
// `require('./lib/net-position.js')`.

(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.MCSGNetPosition = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // TY2026 federal constants verified against Tax Foundation tables; MA constants verified
  // 2026-09-02 against malegislature.gov and the Commonwealth's FY26 tax expenditure budget
  // (budget.digital.mass.gov item 1.628). See model/net_position.py's TAX_PARAMS for citations.
  var TAX_PARAMS = {
    stdDeduction: { single: 16100, hoh: 24150 },
    brackets: {
      single: [
        [0.10, 12400], [0.12, 50400], [0.22, 105700], [0.24, 201775],
        [0.32, 256225], [0.35, 640600], [0.37, Infinity]
      ],
      hoh: [
        [0.10, 17700], [0.12, 67450], [0.22, 105700], [0.24, 201775],
        [0.32, 256200], [0.35, 640600], [0.37, Infinity]
      ]
    },
    ssRate: 0.062,
    ssWageBase: 184500,
    medicareRate: 0.0145,
    addlMedicareRate: 0.009,
    addlMedicareThreshold: 200000,
    maRate: 0.05,
    maPersonalExemption: { single: 4400, hoh: 6800 },
    maDependentExemption: 1000,
    maEitcPct: 0.40,
    maCftcPerDependent: 440,
    ctcPerChild: 2200,
    ctcRefundableCap: 1700,
    // EITC by number of qualifying children (TY2026): [max credit, phaseout start, phaseout end]
    eitc: {
      0: [664, 10860, 19540],
      1: [4427, 23890, 51593],
      2: [7316, 23890, 58629],
      3: [8231, 23890, 62974]
    }
  };

  function federalTax(gross, status, params) {
    params = params || TAX_PARAMS;
    var taxable = Math.max(0.0, gross - params.stdDeduction[status]);
    var tax = 0.0, last = 0.0;
    var brackets = params.brackets[status];
    for (var i = 0; i < brackets.length; i++) {
      var rate = brackets[i][0], upper = brackets[i][1];
      if (taxable <= last) break;
      tax += rate * (Math.min(taxable, upper) - last);
      last = upper;
    }
    return tax;
  }

  function fica(gross, params) {
    params = params || TAX_PARAMS;
    var ss = params.ssRate * Math.min(gross, params.ssWageBase);
    var med = params.medicareRate * gross;
    var addl = params.addlMedicareRate * Math.max(0.0, gross - params.addlMedicareThreshold);
    return ss + med + addl;
  }

  // Dependents reduce taxable income by $1,000 each on top of the filing-status exemption. The
  // 4% MA surtax on income over $1,000,000 is not modelled -- no scenario in this project
  // approaches it (same limitation as the Python).
  function maTax(gross, status, params, kids) {
    params = params || TAX_PARAMS;
    kids = kids || 0;
    var exempt = params.maPersonalExemption[status] + params.maDependentExemption * kids;
    return params.maRate * Math.max(0.0, gross - exempt);
  }

  function federalEitc(gross, kids, params) {
    params = params || TAX_PARAMS;
    var e = params.eitc[Math.min(kids, 3)];
    var mx = e[0], start = e[1], end = e[2];
    if (gross <= start) return mx;
    if (gross >= end) return 0.0;
    return mx * (end - gross) / (end - start);
  }

  // MA EITC (40% of the federal credit) plus the Child and Family Tax Credit. Both refundable.
  // kidsUnder13 defaults to all children; the CFTC is limited to dependents under 13 (or
  // disabled, or 65+).
  function maRefundableCredits(gross, kids, status, params, kidsUnder13) {
    params = params || TAX_PARAMS;
    if (status !== 'hoh' || kids === 0) return 0.0;
    if (kidsUnder13 === undefined || kidsUnder13 === null) kidsUnder13 = kids;
    var fedEitc = federalEitc(gross, kids, params);
    return params.maEitcPct * fedEitc + params.maCftcPerDependent * kidsUnder13;
  }

  // Federal CTC + EITC for the parent claiming the children. IRC s. 24(d): the refundable
  // Additional Child Tax Credit is the LEAST of the entitlement remaining after it offsets tax
  // liability, $1,700 per child, and 15% of earned income above $2,500.
  function refundableCredits(gross, kids, status, params) {
    params = params || TAX_PARAMS;
    if (status !== 'hoh' || kids === 0) return 0.0;
    var entitlement = params.ctcPerChild * kids;
    var taxOwed = federalTax(gross, status, params);
    var nonrefundable = Math.min(entitlement, taxOwed);
    var refundable = Math.min(
      entitlement - nonrefundable,
      params.ctcRefundableCap * kids,
      0.15 * Math.max(0.0, gross - 2500)
    );
    return nonrefundable + refundable + federalEitc(gross, kids, params);
  }

  // After-tax income including federal AND Massachusetts refundable credits.
  function netIncome(gross, status, kids, params, kidsUnder13) {
    params = params || TAX_PARAMS;
    var tax = federalTax(gross, status, params) + fica(gross, params) + maTax(gross, status, params, kids);
    return gross - tax
      + refundableCredits(gross, kids, status, params)
      + maRefundableCredits(gross, kids, status, params, kidsUnder13);
  }

  /**
   * Post-transfer spendable-income comparison. Mirrors net_position.py's analyze().
   * @param {number} payorGross annual
   * @param {number} recipientGross annual
   * @param {number} kids
   * @param {number} weeklySupport
   * @param {number} weeklyChildcare
   * @param {number} payorChildcareShare fraction of weeklyChildcare the payor bears directly
   * @param {object} [params]
   * @param {number} [kidsUnder13]
   */
  function analyze(payorGross, recipientGross, kids, weeklySupport, weeklyChildcare,
                    payorChildcareShare, params, kidsUnder13) {
    params = params || TAX_PARAMS;
    var annualSupport = weeklySupport * 52.0;
    var annualChildcare = weeklyChildcare * 52.0;
    var payorCc = annualChildcare * payorChildcareShare;

    var payorNet = netIncome(payorGross, 'single', 0, params);
    var recipNet = netIncome(recipientGross, 'hoh', kids, params, kidsUnder13);

    var payorAfter = payorNet - annualSupport - payorCc;
    // Support is received tax-free; recipient bears the remaining childcare cost.
    var recipAfter = recipNet + annualSupport - (annualChildcare - payorCc);

    var combinedGross = payorGross + recipientGross;
    return {
      payor_gross: payorGross,
      recipient_gross: recipientGross,
      payor_gross_share: payorGross / combinedGross,
      payor_net: payorNet,
      recip_net: recipNet,
      payor_eff_rate: 1 - payorNet / payorGross,
      recip_eff_rate: recipientGross ? 1 - recipNet / recipientGross : 0.0,
      annual_support: annualSupport,
      payor_childcare: payorCc,
      support_pct_of_payor_gross: annualSupport / payorGross,
      support_pct_of_payor_net: annualSupport / payorNet,
      burden_pct_of_payor_net: (annualSupport + payorCc) / payorNet,
      payor_after: payorAfter,
      recip_after: recipAfter,
      payor_after_share: payorAfter / (payorAfter + recipAfter),
      recip_per_person: recipAfter / (1 + kids),
      payor_per_person: payorAfter,
      gap: payorAfter - recipAfter
    };
  }

  return {
    TAX_PARAMS: TAX_PARAMS,
    federalTax: federalTax,
    fica: fica,
    maTax: maTax,
    federalEitc: federalEitc,
    maRefundableCredits: maRefundableCredits,
    refundableCredits: refundableCredits,
    netIncome: netIncome,
    analyze: analyze
  };
}));
