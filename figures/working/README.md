# Figures for the working paper

Built 2026-09-05 by `model/charts/*.py`; rebuild everything with `.venv/bin/python model/charts/make_all.py`.
Every PNG has a CSV beside it holding the plotted values, so any number on a chart can be checked
without re-running anything. House style: `model/charts/theme.py`. None of these figures is in the
Trial Court letter; they are for the SSRN working paper and the op-ed, after the letter is sent.

Conventions that apply to every figure and must travel with any of them:
- **Every figure has the same anatomy (2026-09-05): a bold sentence title; a one-line deck; a small
  label/value fact line (CUSTODY · CHILDREN · CHILD CARE · INCOMES, with the Worksheet box in parentheses); the chart;
  a hairline rule; italic Notes carrying the conventions and caveats; Source.** `_common.facts()` builds the fact line
  so its wording cannot drift; `theme.header()`, `theme.keyline()` and `theme.footer()` draw the anatomy.
- **Nothing runs past the plot.** `theme.wrap_to()` measures every text element and wraps it to the plot's width;
  header and footer are stacked from measured heights (`finish(pairs=, notes=, source=)` for one-axes charts,
  `_common.top_header()` and `bottom_footer()` for multi-panel figures).

| File | What it shows | Source script / data |
|---|---|---|
| `fig1_headline_household_gap` | Panel (a) for 1, 2, 3 children side by side: recipient household net minus payor net after the order, Box 1 | `fig1_heatmaps.py`; `worksheet.py`, `net_position.py` |
| `fig1_heatmap_{1,2,3}child_box{1,2}` | Four panels each: (a) household gap, (b) per-person gap, (c) order as % of payor net with the 40% contour, (d) units lag with the "7e reads 40%" contour | same |
| `fig2_childcare_rules` | Payor's funded share of child care under three rules (Line 3c; post-transfer gross; post-transfer net) by income share, 1/2/3 children | `fig2_childcare.py` |
| `fig2_childcare_worked_example` | The 87.7% / 64.5% / 53.0% / 52.0% bars at the letter's worked example (64.5% is the § 2 fallback, new Line 6b-2; 53.0% is what the comments ask for, new Lines 6b-1a and 6b-1, withholding basis; 52.0% is the credits-inclusive share, after the 2026-09-08 fix to who claims the children at equal time) | `childcare_post_transfer.py` |
| `fig3_credit_collapse` | (a) equal-time reduction vs the ⅓-time order: Worksheet today, Variant A, Variant B; (b) implied overnight share at factors 1.5 and 2.0 | `fig3_credit.py`; `box1_fix.py` |
| `fig4_marginal_retention` | Cents of the next dollar the payor keeps, $100k–$400k, with and without $300/wk child care | `fig4_retention.py`; `marginal_retention.py` |
| `fig5a_states_S1`, `fig5b_states_S2` | Monthly orders in fifty jurisdictions at the fact pattern, MA highlighted; Georgia held out | `fig5_states.py`; `data/fifty-state/tier-50-2026-09-05.json` |
| `fig5c_credit_at_122_tilemap` | 28 jurisdictions give a formula credit at 122 overnights, 23 do not; MA among the 23 | `data/fifty-state/credit-at-122-2026-09-05.json` |
| `fig6_valve_units_lag` | Line 7e's reading vs the true share of net as child care rises; 7e reaches 40% at $590/wk when the true burden is 57%; the true burden passes 40% at $80/wk | `fig6_valve.py`; `submission_figures.py` |
| `fig7_box3_inversion` | Two children: Box 1 shared vs Box 3 one-child-each order across the income-share range ($835 vs $581/wk at the worked-example incomes, 30.4% lower) beside Table B's 1.40 vs 2.00; cuts against the lower earner | `fig7_box3_split.py`; `submission_figures.py` § 5.1 |
| `fig8_both_pay` | Both parents pay $300/wk of child care: payor bears 93% of the combined $31,200 while earning 87% of gross; net position under three scenarios; the $270/yr Line 6e clip | `fig8_both_pay.py`; `submission_figures.py` § 2.1 |
| `fig9_schedule_ceilings` | Where each state's presumptive schedule stops: 41 combined-income ceilings ranked, MA 13th at $450,000, median $360,000; ten unranked | `fig9_ceilings.py`; `data/fifty-state/ceilings-2026-09-06.json` |
| `fig11_deferral_timeline` | How many times the gross-versus-net income question was deferred in the Massachusetts guidelines corpus: 1 of 5 documented cycles (2025 only; 2017/2018/2021/2023 marked no record, never inferred) | `fig11_deferral_timeline.py`; `data/deferrals-gross-vs-net.json` |

**Exhibit set (one chart per file, `E01`–`E27`, 23 files, no exhibit with more than one set of axes): `output/charts/exhibits/`, built by `exhibits.py` from the CSVs above and copies of the single-panel figures; naming and ratings in `docs/2026-09-05-chart-exhibit-guide.md`.** Measured on the 3-child Box 1 grid (1,147 cells): recipient household ahead in 55% (96% below $150k higher-earner income, none above $230k); payor ahead per person in 99%; order above 40% of payor net in 15%, all at lower-earner income of $25k or less.

**2026-09-06 ("one exhibit, one graph"): the multi-panel figures `fig1_headline_household_gap`, `fig2_childcare_rules`, `fig7_box3_inversion` and `fig8_both_pay` are no longer copied into the exhibit set** (they stay here, unchanged, for the paper). Each panel became its own single-chart exhibit, E18–E26, drawn from the same CSVs. E01's title now states its own measured percentage instead of describing the axes. E12 and E17 were restyled as a deliberate pair (shared axis range, ordering rule, colours).

The presumptive-ceiling chart (plan item 7) was built 2026-09-06 as `fig9_schedule_ceilings` / E16, from a ceilings file completed
against the local primary documents (39 high / 12 medium confidence; no figure guessed).

Every chart was rendered and read back by eye before being committed. External review of the set ran
2026-09-05: every spot-checked value reproduced; fixes applied were disclosure and colour (fixed scales on
heatmap panels (c)/(d), the ±$40k cap stated, the under-13 convention stated on the worked-example charts,
factor-1.5 series in one colour). Suggested next figures: the Box 3 sibling-split inversion and the
both-parents-pay 93% scenario.

**E17 (2026-09-06):** `fig10_ma_shared_vs_primary` puts Massachusetts's Box 1 equal-time order ($4,388) on the same
bar chart as every other ranked jurisdiction's primary-custody order. It beats 47 of 49; only Hawaii and Wisconsin order more at
primary custody than Massachusetts does at equal time. CSV beside it. One fact pattern.
