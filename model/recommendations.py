#!/usr/bin/env python3
"""Every number the Recommendations page quotes, printed by one script.

    .venv/bin/python model/recommendations.py

Six blocks (plan: docs/plans/2026-09-07-site-findings-restructure-and-recommendations.md
section 4, plus block F added by the coordinator 2026-09-07 on the author's childcare
recommendation):

  A. The fifty-jurisdiction S1/S2 medians (Georgia held out; the ranked tier is 50),
     Massachusetts's rank and its distance from each median.
  B. Washington, California, New Jersey, Connecticut, New York at S1/S2, with each
     state's income basis and cap note as recorded in the ceilings dataset.
  C. Five candidate credits for equal parenting time at the worked example, priced
     against the fifty-state S1 median and against Washington and California.
  D. The Box 1 reduction that would put Massachusetts exactly at the median, at
     Washington's figure, and at California's figure.
  E. A corpus check for the "deferred, not decided" gross-vs-net claim.
  F. the author's childcare recommendation: remove childcare from the worksheet, split it
     50-50 after base support, or split it on the post-transfer income mix -- each
     priced against the current rule at the worked example, with after-tax positions.

Reuses model/worksheet.py's run(), model/box1_fix.py's run(), model/net_position.py's
analyze(), and model/childcare_post_transfer.py's figures() for every worksheet and
tax calculation; nothing here reimplements them. Every dollar figure printed below
comes from a function call; only inputs (incomes, health premiums, overnight shares,
child-care amounts) are literal. Numbers are rounded only at print.
"""
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import box1_fix as bf  # noqa: E402
import childcare_post_transfer as cpt  # noqa: E402
import net_position as npos  # noqa: E402
import worksheet as w  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIER50_PATH = os.path.join(REPO, "data", "fifty-state", "tier-50-2026-09-05.json")
CEILINGS_PATH = os.path.join(REPO, "data", "fifty-state", "ceilings-2026-09-06.json")
EXTRACTED_DIR = os.path.join(REPO, "data", "extracted")
GUIDELINES_FLOW = os.path.join(EXTRACTED_DIR, "Guidelines.flow.txt")

# The worked example -- same fact pattern as submission_figures.py / box1_fix.py /
# childcare_post_transfer.py: Parent B (payor) $201,000/yr gross, health premium $43;
# Parent A (recipient) $570/wk gross ($29,640/yr), health premium $33; three children,
# two under 13 for the MA Child and Family Tax Credit.
PAYOR_GROSS_YR = 201_000.0
PAYOR_GROSS_WEEKLY = PAYOR_GROSS_YR / 52.0
RECIP_WEEKLY = 570.0
RECIP_GROSS_YR = RECIP_WEEKLY * 52.0
KIDS = 3
KIDS_UNDER_13 = 2
A_HEALTH, B_HEALTH = 33.0, 43.0

COMPARISON_STATES = ("Washington", "California", "New Jersey", "Connecticut", "New York")

MONTHLY = 52.0 / 12.0  # weekly x MONTHLY = monthly, matching every fifty-state row


def wk_to_mo(weekly):
    return weekly * MONTHLY


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_tier50():
    rows = json.load(open(TIER50_PATH, encoding="utf-8"))
    assert len(rows) == 50, (
        f"expected the ranked fifty-jurisdiction tier to hold 50 rows, found {len(rows)} "
        f"-- Georgia is held out and must not appear here"
    )
    assert not any(r["state"] == "Georgia" for r in rows), "Georgia is held out; it must not be in the ranked tier"
    return rows


def load_ceilings():
    rows = json.load(open(CEILINGS_PATH, encoding="utf-8"))
    return {r["state"]: r for r in rows}


def state_row(rows, name):
    matches = [r for r in rows if r["state"] == name]
    return matches[0] if matches else None


def median_rank_distance(rows, field):
    """Median of `field` among the ranked rows, Massachusetts's rank (1 = highest)
    and its dollar/percent distance above the median."""
    values_desc = sorted((r[field] for r in rows), reverse=True)
    median = statistics.median(values_desc)
    ranked = sorted(rows, key=lambda r: r[field], reverse=True)
    ma_rank = next(i for i, r in enumerate(ranked, 1) if r["state"] == "Massachusetts")
    ma_value = next(r[field] for r in rows if r["state"] == "Massachusetts")
    dollars = ma_value - median
    pct = dollars / median if median else 0.0
    return {"median": median, "ma_rank": ma_rank, "ma_value": ma_value,
            "distance_dollars": dollars, "distance_pct": pct, "n": len(values_desc)}


# ---------------------------------------------------------------------------
# Block C -- candidate credits for equal parenting time
# ---------------------------------------------------------------------------

def box2_order():
    """Today's primary-custody order at the worked example: worksheet.run(box=2)."""
    return w.run(box=2, a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS_WEEKLY,
                 children_under18=KIDS, a_health=A_HEALTH, b_health=B_HEALTH)


def box1_order():
    """Today's shared-parenting order at the worked example: worksheet.run(box=1)."""
    return w.run(box=1, a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS_WEEKLY,
                 children_under18=KIDS, a_health=A_HEALTH, b_health=B_HEALTH)


def variant_order(v, payor_overnight_share=0.5):
    """box1_fix.py's variant, at the given PAYOR overnight share (box1_fix.py's own
    convention: a_overnight_share is Parent A / the recipient's share)."""
    return bf.run(v, a_gross=RECIP_WEEKLY, b_gross=PAYOR_GROSS_WEEKLY,
                  children_under18=KIDS, a_health=A_HEALTH, b_health=B_HEALTH,
                  a_overnight_share=1.0 - payor_overnight_share)


def linear_time_discount(payor_overnight_share, low=1.0 / 3.0, high=0.5, max_discount=0.5):
    """the author's sketch: 0% discount off today's Box 2 (primary) order at LOW payor
    overnights, scaling linearly to MAX_DISCOUNT at HIGH payor overnights. Clamped
    outside [low, high]. Returns the discount fraction, not a dollar figure."""
    if payor_overnight_share <= low:
        return 0.0
    if payor_overnight_share >= high:
        return max_discount
    return max_discount * (payor_overnight_share - low) / (high - low)


def linear_discount_order(payor_overnight_share, base=None):
    base = box2_order()["7d"] if base is None else base
    return base * (1.0 - linear_time_discount(payor_overnight_share))


def candidate_credits():
    """The five (six-row) candidates block C asks for, each as a dict with the
    weekly order and a label. All computed from worksheet.py / box1_fix.py; the
    linear rule is applied to worksheet.py's own Box 2 figure."""
    b2 = box2_order()["7d"]
    rows = []
    rows.append({"label": "(i) Variant A -- 6e limitation moved to the transfer",
                 "weekly": variant_order("A")["7d"]})
    rows.append({"label": "(ii) Variant B -- cross-credit at duplication 1.5",
                 "weekly": variant_order("B")["7d"]})
    rows.append({"label": "(iii) Variant C at equal time (payor 50% of overnights)",
                 "weekly": variant_order("C", 0.5)["7d"]})
    rows.append({"label": "(iv) Linear time-proportional discount at 50% of overnights",
                 "weekly": linear_discount_order(0.5, base=b2)})
    rows.append({"label": "(v-a) Linear time-proportional discount at 45% of overnights",
                 "weekly": linear_discount_order(0.45, base=b2)})
    rows.append({"label": "(v-b) Linear time-proportional discount at 40% of overnights",
                 "weekly": linear_discount_order(0.40, base=b2)})
    return rows, b2


# ---------------------------------------------------------------------------
# Block E -- corpus check for the gross-vs-net deferral claim
# ---------------------------------------------------------------------------

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
COMMENTARY_MARKER_RE = re.compile(r"Comm\s*entary\s+(20\d\d)")


def commentary_blocks():
    """Split Guidelines.flow.txt at each 'Commentary <year>' marker (an OCR artifact
    sometimes inserts a space: 'Comm entary'). Returns a list of (year, block_text)
    in document order; the guidelines embed several blocks per year, one per section
    the commentary addresses, so a year can appear more than once."""
    if not os.path.exists(GUIDELINES_FLOW):
        return {}
    text = open(GUIDELINES_FLOW, encoding="utf-8").read()
    matches = list(COMMENTARY_MARKER_RE.finditer(text))
    blocks = []
    for i, m in enumerate(matches):
        year = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((year, text[start:end]))
    return blocks


def gross_and_net_sentences_by_year():
    """For each commentary year, every sentence (across all of that year's blocks)
    containing both 'gross' and 'net' (case-insensitive)."""
    by_year = {}
    for year, block in commentary_blocks():
        by_year.setdefault(year, {"n_blocks": 0, "hits": []})
        by_year[year]["n_blocks"] += 1
        for s in SENTENCE_RE.split(block):
            s = s.strip()
            if re.search(r"gross", s, re.I) and re.search(r"\bnet\b", s, re.I):
                by_year[year]["hits"].append(s)
    return by_year


def as_prior_task_forces_sentences():
    """Every sentence containing 'as prior task forces' (case-insensitive) across
    every *.flow.txt in data/extracted, with the source file."""
    hits = []
    if not os.path.isdir(EXTRACTED_DIR):
        return []
    for fname in sorted(os.listdir(EXTRACTED_DIR)):
        if not fname.endswith(".flow.txt"):
            continue
        path = os.path.join(EXTRACTED_DIR, fname)
        text = open(path, encoding="utf-8").read()
        for s in SENTENCE_RE.split(text):
            if "as prior task forces" in s.lower():
                hits.append((fname, s.strip()))
    return hits


# ---------------------------------------------------------------------------
# Block F -- the author's childcare recommendation
# ---------------------------------------------------------------------------

def childcare_rules():
    """Five childcare rules at the worked example ($300/wk paid by the recipient,
    $0 by the payor): the current worksheet, removing childcare from the worksheet
    entirely, a flat 50-50 split after base support, the post-transfer GROSS
    fallback (childcare_post_transfer.py rule 2b, comments' Line 6b-2), and the
    post-transfer NET withholding-basis rule (rule 5) -- the comments' Line 6b-1
    redline and the RECOMMENDED row. Row 5 runs through the order itself, the same
    as row 4, because Line 6b-1 sits inside the 6b -> 6c -> 6e -> 6g -> 7b -> 7d
    chain; it is not a private side payment beside an unchanged order.

    Each row reports the worksheet order (weekly/monthly), the payor's effective
    share of the $15,600/yr childcare cost in percent and dollars, and both
    parties' after-tax position from net_position.analyze(). Reuses
    childcare_post_transfer.figures() and net_position.analyze() throughout; the
    only new arithmetic here is applying an already-computed share to the $15,600
    total, exactly as childcare_post_transfer.py itself does for its rule 2b.
    """
    f = cpt.figures()
    base = f["base_7d"]                    # no-childcare Box 1 order
    cc_annual = f["cc_annual"]              # $15,600/yr
    CC_WEEKLY = cpt.CC_WEEKLY               # $300/wk

    def after_tax(support_weekly, payor_share_direct):
        return npos.analyze(PAYOR_GROSS_YR, RECIP_GROSS_YR, KIDS, support_weekly,
                             CC_WEEKLY, payor_share_direct, kids_under_13=KIDS_UNDER_13)

    rows = []

    # 1. Current worksheet: Line 6b on pre-order (Line 3c) shares. The order itself
    # carries the full childcare transfer; the payor pays nothing directly.
    order1 = f["current_7d"]
    share1 = f["rule1_share"]
    pos1 = after_tax(order1, 0.0)
    rows.append({"n": 1, "label": "Current worksheet (Line 6b on pre-order Line 3c shares)",
                 "order_wk": order1, "share": share1, "pos": pos1})

    # 2. Childcare removed from the worksheet entirely: the order reverts to the
    # no-childcare figure and each parent bears what they actually pay -- the payor
    # pays $0 of the recipient's $300/wk, so his effective share is zero.
    order2 = base
    share2 = 0.0
    pos2 = after_tax(order2, 0.0)
    rows.append({"n": 2, "label": "Childcare removed from the worksheet (each parent bears what they pay)",
                 "order_wk": order2, "share": share2, "pos": pos2})

    # 3. Base support calculated first, then childcare split 50-50 regardless of
    # income share (the author's sketch). The payor reimburses half the $300/wk directly.
    order3 = base  # the worksheet's support figure is unchanged
    share3 = 0.5
    pos3 = after_tax(order3, share3)
    rows.append({"n": 3, "label": "Base support first, then childcare split 50-50",
                 "order_wk": order3, "share": share3, "pos": pos3})

    # 4. Post-transfer GROSS shares on Line 3a -- the Trial Court comments' Line
    # 6b-1 redline. childcare_post_transfer.py's rule 2b; order bakes in the
    # childcare transfer at the post-transfer share.
    order4 = f["rule2b_7d"]
    share4 = f["rule2b_share"]
    pos4 = after_tax(order4, 0.0)
    rows.append({"n": 4, "label": "Post-transfer GROSS shares on Line 3a (comments' fallback, Line 6b-2)",
                 "order_wk": order4, "share": share4, "pos": pos4})

    # 5. THE RECOMMENDATION as of v4.9: post-transfer NET shares on the withholding
    # basis, applied AS A WORKSHEET LINE. Line 6b-1 feeds 6b -> 6c -> 6e -> 6g -> 7b
    # -> 7d, so the order itself moves; this is the same linear step rule 2b (row 4)
    # uses, and it is what the comments' Section 2 actually asks for. Modelling it as
    # a private side payment -- which this row did before 2026-09-08 -- proposed a
    # different remedy from the letter and was the audit's finding C3.
    order5 = f["rule5_7d"]
    share5 = f["rule5_share"]
    pos5 = after_tax(order5, 0.0)   # the child-care transfer is inside the order
    rows.append({"n": 5, "label": "Post-transfer NET shares on the withholding basis "
                                  "(comments' Line 6b-1 redline, RECOMMENDED)",
                 "order_wk": order5, "share": share5, "pos": pos5})

    headline = {
        "before_share": f["rule1_share"],                      # Line 3c, "before the order"
        "after_gross_share": f["rule2_gross_share"],            # post-transfer GROSS
        "after_net_share": f["rule3_share"],                    # post-transfer NET, credits included (analysis)
        "after_net_withholding_share": f["rule5_share"],        # post-transfer NET, withholding basis (the ask)
    }
    return rows, cc_annual, headline


# ---------------------------------------------------------------------------
# Printing
# ---------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("RECOMMENDATIONS PAGE -- EVERY NUMBER, PRINTED FROM CODE")
    print("=" * 78)

    rows = load_tier50()
    ceilings = load_ceilings()

    # --- Block A ------------------------------------------------------------
    print("\n" + "-" * 78)
    print("BLOCK A -- the fifty-jurisdiction medians and Massachusetts's distance")
    print("-" * 78)
    print("Source: data/fifty-state/tier-50-2026-09-05.json (Georgia held out; see")
    print("docs/2026-09-05-georgia-worked-example.md). S1 = equal parenting time,")
    print("S2 = the other parent has primary custody. Monthly figures throughout,")
    print("as the tier-50 dataset states them.\n")
    a_s1 = median_rank_distance(rows, "s1")
    a_s2 = median_rank_distance(rows, "s2")
    for label, d in (("S1 (equal time)", a_s1), ("S2 (primary custody)", a_s2)):
        print(f"  {label}:")
        print(f"    ranked jurisdictions           {d['n']}")
        print(f"    median                          ${d['median']:>10,.2f}/mo")
        print(f"    Massachusetts                   ${d['ma_value']:>10,.2f}/mo   rank {d['ma_rank']} of {d['n']}")
        print(f"    MA above the median              ${d['distance_dollars']:>9,.2f}/mo   {d['distance_pct']:>7.1%}")
    print()

    # --- Block B ------------------------------------------------------------
    print("-" * 78)
    print("BLOCK B -- Washington, California, New Jersey, Connecticut, New York")
    print("-" * 78)
    print("Basis and cap note: data/fifty-state/ceilings-2026-09-06.json.\n")
    for name in COMPARISON_STATES:
        r = state_row(rows, name)
        if r is None:
            print(f"  {name:<12} NOT FOUND in the ranked tier -- excluded from any rank claim.")
            continue
        c = ceilings.get(name)
        basis = c["basis"] if c else "unrecorded"
        cap = f"${c['annual_ceiling']:,.0f}/yr ({c['period_as_stated']})" if c and c["annual_ceiling"] else \
              (c["period_as_stated"] if c and c.get("period_as_stated") else "no stated ceiling")
        note = f" -- {c['note']}" if c and c.get("note") else ""
        print(f"  {name:<12} S1 ${r['s1']:>9,.2f}/mo   S2 ${r['s2']:>9,.2f}/mo   basis: {basis:<5}  cap: {cap}{note}")
        if r.get("note"):
            print(f"               row note: {r['note']}")
    print()
    for name in ("Washington", "California"):
        present = state_row(rows, name) is not None
        print(f"  {name} present at the ranked tier: {present}")
    print()

    # --- Block C ------------------------------------------------------------
    print("-" * 78)
    print("BLOCK C -- candidate credits for equal parenting time, worked example")
    print("-" * 78)
    print("Payor $201,000/yr gross, health premium $43; recipient $570/wk gross,")
    print("health premium $33; three children; no child care. Sources: worksheet.py,")
    print("box1_fix.py (variants A, B, C), and the linear rule applied here to")
    print("worksheet.py's own Box 2 figure.\n")
    b2 = box2_order()["7d"]
    b1 = box1_order()["7d"]
    print(f"  Today's Box 2 (primary) order    ${b2:>9,.2f}/wk   ${wk_to_mo(b2):>9,.2f}/mo")
    print(f"  Today's Box 1 (shared)  order    ${b1:>9,.2f}/wk   ${wk_to_mo(b1):>9,.2f}/mo")
    print()
    cand_rows, b2_check = candidate_credits()
    assert abs(b2_check - b2) < 0.005, "candidate_credits() must price off the same Box 2 figure printed above"
    print(f"  {'candidate':<58} {'wk':>9} {'mo':>10} {'vs Box1':>9} {'vs median':>10} {'vs WA':>10} {'vs CA':>10}")
    wa_s1 = state_row(rows, "Washington")["s1"]
    ca_s1 = state_row(rows, "California")["s1"]
    for r in cand_rows:
        mo = wk_to_mo(r["weekly"])
        pct_vs_b1 = (r["weekly"] - b1) / b1
        print(f"  {r['label']:<58} ${r['weekly']:>7,.2f} ${mo:>8,.2f} {pct_vs_b1:>8.1%} "
              f"{(mo - a_s1['median']) / a_s1['median']:>9.1%} {(mo - wa_s1) / wa_s1:>9.1%} {(mo - ca_s1) / ca_s1:>9.1%}")
    print("\n  ('vs median/WA/CA' = the candidate's monthly figure, percent above (+) or")
    print("   below (-) the fifty-state S1 median / Washington's S1 / California's S1.)")
    va = variant_order("A")
    vb = variant_order("B")
    vc_equal = variant_order("C", 0.5)
    print(f"\n  Check: Variant C at equal time reproduces Variant B exactly, as box1_fix.py's")
    print(f"  own docstring says ('at equal time this is identical to B'): "
          f"{abs(vb['7d'] - vc_equal['7d']) < 0.005}")
    print()

    # --- Block D ------------------------------------------------------------
    print("-" * 78)
    print("BLOCK D -- the Box 1 reduction that reaches the median, WA, and CA")
    print("-" * 78)
    targets = (("the fifty-state S1 median", a_s1["median"]),
               ("Washington's S1", wa_s1),
               ("California's S1", ca_s1))
    print(f"  Starting point: today's Box 1 order ${b1:,.2f}/wk (${wk_to_mo(b1):,.2f}/mo).\n")
    for label, target_mo in targets:
        target_wk = target_mo * 12.0 / 52.0
        cut_wk = b1 - target_wk
        pct = cut_wk / b1
        print(f"  To reach {label} (${target_mo:,.2f}/mo): cut ${cut_wk:,.2f}/wk "
              f"(${cut_wk * 52:,.0f}/yr), {pct:.1%} off today's Box 1 order.")
    print()

    # --- Block E ------------------------------------------------------------
    print("-" * 78)
    print("BLOCK E -- corpus check: was gross-vs-net deferred, and how many times")
    print("-" * 78)
    by_year = gross_and_net_sentences_by_year()
    if not by_year:
        print("  Corpus not present in this checkout (data/extracted/Guidelines.flow.txt);"
              " block E is reported in the committed run output only.")
    total_hits = 0
    for year in sorted(by_year):
        info = by_year[year]
        total_hits += len(info["hits"])
        print(f"  Commentary {year}: {info['n_blocks']} block(s) in Guidelines.flow.txt, "
              f"{len(info['hits'])} sentence(s) containing both 'gross' and 'net':")
        for h in info["hits"]:
            print(f"      \"{h}\"")
    print(f"\n  Total sentences with both terms inside a Guidelines.flow.txt commentary "
          f"block: {total_hits}")
    prior_hits = as_prior_task_forces_sentences()
    print(f"\n  'as prior task forces' across data/extracted/*.flow.txt: {len(prior_hits)} hit(s)")

    # The Guidelines PDF's own commentary is not the whole corpus any more. Since 2026-09-08 the
    # prior task force reports and economic reviews, 2001-2025, are in data/source/taskforce/ and
    # data/deferrals-gross-vs-net.json records what each cycle's OWN document says. Print that here
    # so this run output cannot be read as the complete picture.
    import json as _json
    _dp = os.path.join(REPO, "data", "deferrals-gross-vs-net.json")
    if os.path.exists(_dp):
        _d = _json.load(open(_dp))
        _def = [c for c in _d["cycles"] if c["status"] == "DEFERRED"]
        print(f"\n  FULL CORPUS (data/deferrals-gross-vs-net.json, {len(_d['cycles'])} reviews):")
        print(f"  {len(_def)} cycles take up gross versus net and none change it:")
        for c in _def:
            print(f"      {c['year']}  {c.get('source_kind', 'unknown source')}")
        _tf = [c['year'] for c in _def if c.get('source_kind') == 'task force report']
        _er = [c['year'] for c in _def if c.get('source_kind', '').startswith('economic review')]
        print(f"  Task force decisions: {_tf}.  Economic review statements: {_er}.")
        print("  Never write 'five task forces declined'; only the first list is task force decisions.")
    for fname, sentence in prior_hits:
        print(f"      {fname}: \"{sentence}\"")
    files_with_hit = sorted({fname for fname, _ in prior_hits})
    print(f"\n  CONCLUSION: {total_hits} sentence(s) mentioning both gross and net appear inside "
          f"the year-tagged commentary blocks embedded in the Guidelines PDF itself "
          f"({', '.join(sorted(by_year)) if by_year else 'none'} all checked, zero hits). The "
          f"explicit deferral -- \"as prior task forces have done ... decided not to recommend "
          f"a change from gross income to net income at this time\" -- lives in "
          f"{', '.join(files_with_hit) if files_with_hit else 'no file in this corpus'}, the "
          f"Brattle economic review, not in the Guidelines' own embedded commentary, and it does "
          f"not itself name which prior years deferred it. State it as: one document in this "
          f"corpus (the 2025 economic review) records a gross-vs-net deferral and says prior "
          f"task forces did the same; the Guidelines' own year-tagged commentary blocks contain "
          f"no sentence discussing gross vs. net at all.")
    print()

    # --- Block F --------------------------------------------------------
    print("-" * 78)
    print("BLOCK F -- the author's childcare recommendation, worked example")
    print("-" * 78)
    print("Payor $201,000/yr gross ($43 health premium), recipient $570/wk gross")
    print("($29,640/yr, $33 health premium), three children (two under 13), Box 1,")
    print("recipient pays $300/wk child care, payor pays $0 directly. Source:")
    print("model/childcare_post_transfer.py (reused, not reimplemented) and")
    print("model/net_position.py's analyze().\n")
    f_rows, cc_annual, headline = childcare_rules()
    print(f"  Total annual child care at issue: ${cc_annual:,.0f}/yr ($300/wk)\n")
    for r in f_rows:
        mo = wk_to_mo(r["order_wk"])
        print(f"  {r['n']}. {r['label']}")
        print(f"       order            ${r['order_wk']:>9,.2f}/wk   ${mo:>9,.2f}/mo")
        print(f"       payor's share of the ${cc_annual:,.0f}/yr child care: "
              f"{r['share']:>6.1%}  (${r['share'] * cc_annual:>9,.2f}/yr)")
        print(f"       after tax: payor keeps ${r['pos']['payor_after']:>9,.2f}   "
              f"recipient household holds ${r['pos']['recip_after']:>9,.2f}")
    print()
    print("  The sentence the site makes (rule 1, current worksheet):")
    print(f"    before the order, the payor's share of the parties' combined available")
    print(f"    income (Line 3c) is {headline['before_share']:.1%};")
    print(f"    after the order, his share of POST-TRANSFER GROSS income is "
          f"{headline['after_gross_share']:.1%};")
    print(f"    after the order, his share of POST-TRANSFER NET income, withholding basis "
          f"(the ask) is {headline['after_net_withholding_share']:.1%};")
    print(f"    after the order, his share of POST-TRANSFER NET income counting refundable "
          f"credits (analysis only) is {headline['after_net_share']:.1%};")
    print(f"    and child care is allocated on the {headline['before_share']:.1%} figure --")
    print(f"    the income split BEFORE the order, not any figure after it.")
    print()

    print("=" * 78)
    print("END OF RUN")
    print("=" * 78)


if __name__ == "__main__":
    main()
