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
// 2026-09-08: ported net_position.py's fix for analyze() defaulting to "recipient claims every
// child and files head of household" in EVERY custody arrangement, including Box 1 (equal
// parenting time). analyze() and refundableCredits() now take a `box` argument (default 2, the
// unchanged pre-fix behaviour); Box 1 averages the payor-claims and recipient-claims years via
// the new householdNetIncomes(). This required the IRC s. 24(b) high-income Child Tax Credit
// taper (ctcEntitlementAfterPhaseout(), previously absent here) and decoupling the federal CTC
// from the 'hoh'-only gate in refundableCredits() -- see model/net_position.py's own docstring
// for why both were latent bugs.
//
// 2026-09-08 (later, same day): a second fix, ported from private commit 723a7bf. The FIRST Box 1
// fix above had the two parents swap EVERYTHING in alternating years -- filing status, the EITC,
// and the CTC. The statute (IRC ss. 2(b)(1)(A)(i), 32(c)(3)(A)) does not allow that: head of
// household and the EITC stay with the physical custodian regardless of a s. 152(e)/Form 8332
// release; only the CTC/ACTC family moves. Added payorNetClaimsCtc() and custodialNetNoCtc(),
// ports of net_position._payor_net_claims_ctc()/_custodial_net_no_ctc(), and householdNetIncomes()
// now uses them for Box 1's payor-claims year instead of swapping filing status outright. See
// docs/2026-09-08-filing-status-and-credit-allocation.md. See assets/js/calculator.test.js for the
// fidelity checks.
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
    // IRC s. 24(b): the Child Tax Credit phases out $50 per $1,000 (or fraction) of MAGI over
    // $200,000 for single/HoH filers ($400,000 MFJ -- not modelled, no filer in this project
    // files jointly). A TAPER, not a cliff.
    ctcPhaseoutThreshold: { single: 200000, hoh: 200000 },
    ctcPhaseoutPer1000: 50,
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

  // IRC s. 24(b): CTC entitlement before the tax-liability/refundability split, reduced $50 per
  // $1,000 (or fraction) of gross over the filer's threshold. A taper, not a cliff -- do not
  // round the excess down to the nearest $1,000.
  function ctcEntitlementAfterPhaseout(gross, kids, status, params) {
    params = params || TAX_PARAMS;
    var entitlement = params.ctcPerChild * kids;
    var threshold = (params.ctcPhaseoutThreshold && params.ctcPhaseoutThreshold[status] !== undefined)
      ? params.ctcPhaseoutThreshold[status] : params.ctcPhaseoutThreshold.single;
    if (gross <= threshold) return entitlement;
    var steps = Math.ceil((gross - threshold) / 1000.0);
    var reduction = params.ctcPhaseoutPer1000 * steps;
    return Math.max(0.0, entitlement - reduction);
  }

  // Federal CTC (any filing status) + EITC (custodial-parent proxy only). IRC s. 24(d): the
  // refundable Additional Child Tax Credit is the LEAST of the entitlement remaining after it
  // offsets tax liability, $1,700 per child, and 15% of earned income above $2,500.
  //
  // DECOUPLED FROM FILING STATUS 2026-09-08. The CTC no longer returns 0 for a non-'hoh' filer --
  // a parent who claims a qualifying child (via a custody order or a signed Form 8332) can claim
  // the Child Tax Credit filing single, which is exactly the case a Box 1 (equal-time) scenario
  // needs once the dependency claim alternates between the two parents by year. The EITC keeps
  // ITS OWN rule, unchanged: it requires the child to have lived with the claimant for more than
  // half the year, which is what 'hoh' stands in for in this simplified model, so it is not
  // extended to a 'single, claims the kids on paper only' filer.
  function refundableCredits(gross, kids, status, params) {
    params = params || TAX_PARAMS;
    if (kids === 0) return 0.0;
    var entitlement = ctcEntitlementAfterPhaseout(gross, kids, status, params);
    var taxOwed = federalTax(gross, status, params);
    var nonrefundable = Math.min(entitlement, taxOwed);
    var refundable = Math.min(
      entitlement - nonrefundable,
      params.ctcRefundableCap * kids,
      0.15 * Math.max(0.0, gross - 2500)
    );
    var eitc = status === 'hoh' ? federalEitc(gross, kids, params) : 0.0;
    return nonrefundable + refundable + eitc;
  }

  // Port of net_position._payor_net_claims_ctc(). The payor's net income in the year a s.
  // 152(e)/Form 8332 release moves the Child Tax Credit to him. He never gains head-of-household
  // status, the EITC, the MA EITC, or the MA Child and Family Tax Credit -- none of the four is
  // movable by a release (IRC ss. 2(b)(1)(A)(i), 32(c)(3)(A); the MA credits piggyback on the
  // federal EITC/HoH test). He files single. `kids` here drives ONLY the CTC computation; maTax
  // below is always called with 0 dependents for the payor, matching the Python.
  function payorNetClaimsCtc(gross, kids, params) {
    params = params || TAX_PARAMS;
    var tax = federalTax(gross, 'single', params) + fica(gross, params) + maTax(gross, 'single', params, 0);
    var entitlement = ctcEntitlementAfterPhaseout(gross, kids, 'single', params);
    var taxOwed = federalTax(gross, 'single', params);
    var nonrefundable = Math.min(entitlement, taxOwed);
    var refundable = Math.min(
      entitlement - nonrefundable,
      params.ctcRefundableCap * kids,
      0.15 * Math.max(0.0, gross - 2500)
    );
    return gross - tax + nonrefundable + refundable;
  }

  // Port of net_position._custodial_net_no_ctc(). The majority-nights parent's net income in a
  // year where the s. 152(e)/Form 8332 release moves the federal Child Tax Credit to the other
  // parent. Head of household, the federal EITC, the MA EITC (40% of federal), and the MA Child
  // and Family Tax Credit are all UNAFFECTED by the release. Only the federal CTC/ACTC family
  // drops out for this parent this year -- maTax below still carries the full dependent count.
  function custodialNetNoCtc(gross, kids, kidsUnder13, params) {
    params = params || TAX_PARAMS;
    var tax = federalTax(gross, 'hoh', params) + fica(gross, params) + maTax(gross, 'hoh', params, kids);
    var fedEitc = kids ? federalEitc(gross, kids, params) : 0.0;
    var maCredits = maRefundableCredits(gross, kids, 'hoh', params, kidsUnder13);
    return gross - tax + fedEitc + maCredits;
  }

  // After-tax income including federal AND Massachusetts refundable credits.
  function netIncome(gross, status, kids, params, kidsUnder13) {
    params = params || TAX_PARAMS;
    var tax = federalTax(gross, status, params) + fica(gross, params) + maTax(gross, status, params, kids);
    return gross - tax
      + refundableCredits(gross, kids, status, params)
      + maRefundableCredits(gross, kids, status, params, kidsUnder13);
  }

  // Port of net_position.net_income_withholding_basis. Tax and FICA only, single filer,
  // no exemptions, no refundable credits -- the basis Section 2 of the comments asks for
  // as of v4.9, because CJ-D 304 collects neither filing status nor who claims which child.
  function netIncomeWithholdingBasis(gross, params) {
    params = params || TAX_PARAMS;
    return gross - (federalTax(gross, 'single', params) + fica(gross, params) + maTax(gross, 'single', params, 0));
  }

  // Each party's annual net income, given who claims the children for tax purposes. Mirrors
  // net_position.py's household_net_incomes().
  //
  // Box 2 (primary custody, the DEFAULT -- matches every caller written before 2026-09-08): the
  // recipient is the physical custodian, claims every child, and files head of household.
  // Unchanged from the original hardcoded behaviour.
  //
  // Box 1 (equal parenting time): CORRECTED AGAIN 2026-09-08, same day, against
  // docs/2026-09-08-filing-status-and-credit-allocation.md, a primary-source read of IRC ss.
  // 2(b), 7703(b), 152(c)/(e), 21(e)(5), 24(b)/(h), 32(c)(3)(A), and the corresponding MA
  // statutes. The FIRST attempt at this fix (same day, superseded) had the two parents swap
  // EVERYTHING in alternating years -- filing status, the EITC, and the CTC. The statute does
  // not allow that: a s. 152(e)/Form 8332 release moves ONLY the dependency claim and the
  // federal CTC/ACTC family (s. 152(e)(1)-(2), s. 24(c)(1)). Head of household stays with the
  // physical custodian regardless of any release (s. 2(b)(1)(A)(i): the qualifying-child test is
  // "determined without regard to section 152(e)"). The EITC stays with the physical custodian
  // too, on the identical "without regard to ... section 152(e)" language in s. 32(c)(3)(A).
  // This project's own 182/183-overnight convention (recipient holds 183, the majority) makes
  // the RECIPIENT the physical custodian in every year; the PAYOR never receives head-of-
  // household status or the EITC in Box 1, in either claiming year.
  //
  // So this returns the expected value of alternating ONLY the CTC/dependency claim: the
  // payor-claims year (recipient keeps HoH/EITC/MA EITC/MA CFTC, payor gets only the CTC as a
  // single filer -- see payorNetClaimsCtc()) and the recipient-claims year (identical to Box 2
  // in every respect -- the recipient already had everything, so nothing changes when she also
  // claims the CTC), averaged for both parties. This is not approximated as "half the credit" --
  // computing both years separately is what makes the IRC s. 24(b) high-income taper apply
  // correctly in the payor's claiming year, which a flat 50% haircut would not reproduce.
  //
  // countRefundableCredits=false (added 2026-09-08 -- the credits-off switch) lets a reader
  // who does not accept any assumption about which parent claims which child -- an economist,
  // most pointedly -- validate the arithmetic anyway. In this mode BOTH parties' net income
  // comes from netIncomeWithholdingBasis() and box/kidsUnder13 are ignored entirely: filing
  // status and who claims which child matter ONLY because they gate the refundable credits, so
  // once the credits are off there is nothing left for either fact to change. Mirrors
  // net_position.py's household_net_incomes() -- see that function's docstring.
  function householdNetIncomes(payorGross, recipientGross, kids, params, kidsUnder13, box, countRefundableCredits) {
    params = params || TAX_PARAMS;
    box = box === undefined ? 2 : box;
    countRefundableCredits = countRefundableCredits === undefined ? true : countRefundableCredits;
    var payorNet, recipNet;
    if (!countRefundableCredits) {
      return {
        payorNet: netIncomeWithholdingBasis(payorGross, params),
        recipNet: netIncomeWithholdingBasis(recipientGross, params)
      };
    }
    if (box === 1) {
      // Year A: the recipient (majority-nights parent) claims the CTC too -- identical to Box 2
      // in every respect, since she already had HoH, the EITC, and the MA credits regardless of
      // the CTC claim.
      var payorNetRecipientClaims = netIncome(payorGross, 'single', 0, params);
      var recipNetRecipientClaims = netIncome(recipientGross, 'hoh', kids, params, kidsUnder13);
      // Year B: the s. 152(e)/Form 8332 release moves ONLY the CTC to the payor. He never
      // becomes HoH and never gets the EITC; she keeps both, plus the MA EITC and MA CFTC, and
      // simply loses the federal CTC for that year.
      var payorNetPayorClaims = payorNetClaimsCtc(payorGross, kids, params);
      var recipNetPayorClaims = custodialNetNoCtc(recipientGross, kids, kidsUnder13, params);
      payorNet = (payorNetRecipientClaims + payorNetPayorClaims) / 2.0;
      recipNet = (recipNetRecipientClaims + recipNetPayorClaims) / 2.0;
    } else {
      payorNet = netIncome(payorGross, 'single', 0, params);
      recipNet = netIncome(recipientGross, 'hoh', kids, params, kidsUnder13);
    }
    return { payorNet: payorNet, recipNet: recipNet };
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
   * @param {number} [box] which custody box the credits should follow (see
   *   householdNetIncomes()). Defaults to 2 (recipient claims all children, the unchanged
   *   pre-2026-09-08 behaviour) so a call site written before this parameter existed keeps
   *   producing the same number it always did. A Box 1 (equal-time) scenario must pass box=1
   *   explicitly to get the corrected alternating-year treatment.
   * @param {boolean} [countRefundableCredits] the credits-off switch (added 2026-09-08,
   *   defaults to true so every existing call site keeps producing the same number it always
   *   did). false removes every refundable credit from every figure this function returns:
   *   both parties' net income comes from netIncomeWithholdingBasis() alone, and box /
   *   kidsUnder13 stop mattering. See householdNetIncomes()'s comment.
   */
  function analyze(payorGross, recipientGross, kids, weeklySupport, weeklyChildcare,
                    payorChildcareShare, params, kidsUnder13, box, countRefundableCredits) {
    params = params || TAX_PARAMS;
    var annualSupport = weeklySupport * 52.0;
    var annualChildcare = weeklyChildcare * 52.0;
    var payorCc = annualChildcare * payorChildcareShare;

    var nets = householdNetIncomes(payorGross, recipientGross, kids, params, kidsUnder13, box, countRefundableCredits);
    var payorNet = nets.payorNet;
    var recipNet = nets.recipNet;

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
    ctcEntitlementAfterPhaseout: ctcEntitlementAfterPhaseout,
    refundableCredits: refundableCredits,
    payorNetClaimsCtc: payorNetClaimsCtc,
    custodialNetNoCtc: custodialNetNoCtc,
    netIncome: netIncome,
    netIncomeWithholdingBasis: netIncomeWithholdingBasis,
    householdNetIncomes: householdNetIncomes,
    analyze: analyze
  };
}));
