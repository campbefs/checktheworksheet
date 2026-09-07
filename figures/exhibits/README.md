# Exhibit set — one chart per file

Built by `model/charts/exhibits.py` from the working figures in `output/charts/` (never edit these by hand; rebuild). Naming and ratings: `docs/2026-09-05-chart-exhibit-guide.md`. No exhibit has more than one set of axes (2026-09-06: "I told you ONE EXHIBIT, ONE GRAPH").

Heatmap exhibits E01/E02/E04/E18/E19 are drawn from `fig1_heatmap_{1,2,3}child_box1.csv`; E20-E22 from `fig2_childcare_rules.csv`; E08/E09 from `fig3_credit_collapse.csv`; E23/E24 from `fig7_box3_inversion*.csv`; E25/E26 from `fig8_both_pay.csv`; E27 from `data/deferrals-gross-vs-net.json`. The rest are copies of single-panel figures.

**Retired from the exhibit set (multi-panel; kept as working figures for the paper only):** `fig1_headline_household_gap.png` (was E03; its three panels are now E18/E19/E01), `fig2_childcare_rules.png` (was E07; now E20/E21/E22), `fig7_box3_inversion.png` (was E14; now E23/E24), `fig8_both_pay.png` (was E15; now E25/E26). The old E03/E07/E14/E15 exhibit PNGs are not included in this repository at all; they remain in the private working repository's `_retired-2026-09-06-multi-panel/` folder, so nothing globbing this folder for the live set picks them up.

The per-person exhibit (E02) travels with E01/E18/E19. The lead pair is E12 then E17 (same states, same axis range, same colours, same ordering rule): E12 ranks every jurisdiction's primary-custody order with Massachusetts marked; E17 replaces Massachusetts's bar with its equal-time order. Generic grids set the MA under-13 credit to zero.

- `E01-who-holds-more-3-children.png`
- `E02-who-holds-more-per-person-3-children.png`
- `E04-order-as-share-of-payor-net-3-children.png`
- `E05-what-line-7e-sees-vs-true-burden-worked-example.png`
- `E06-child-care-share-three-rules-worked-example.png`
- `E08-credit-shrinks-as-gap-widens-3-children.png`
- `E09-implied-overnight-share-by-factor-3-children.png`
- `E10-cents-kept-of-next-dollar-worked-example.png`
- `E11-fifty-states-equal-parenting-one-fact-pattern.png`
- `E12-fifty-states-lower-earner-primary-one-fact-pattern.png`
- `E13-credit-at-122-overnights-28-of-51.png`
- `E16-where-each-presumptive-schedule-stops-51.png`
- `E17-ma-equal-time-vs-others-primary-custody.png`
- `E18-who-holds-more-1-child.png`
- `E19-who-holds-more-2-children.png`
- `E20-child-care-funding-gap-1-child.png`
- `E21-child-care-funding-gap-2-children.png`
- `E22-child-care-funding-gap-3-children.png`
- `E23-split-siblings-weekly-order-2-children.png`
- `E24-split-siblings-schedule-cost-2-children.png`
- `E25-both-pay-child-care-who-pays-3-children.png`
- `E26-both-pay-child-care-net-position-3-children.png`
- `E27-gross-vs-net-deferred-1-of-5-cycles.png`
