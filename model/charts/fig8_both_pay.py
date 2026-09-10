"""Figure 8: when both parents pay child care during their own parenting time, the payor bears 93%.

Worked example, three children, equal parenting time. Each parent pays $300/wk (the ordinary case at
50-50; the $430-per-child benchmark does not bind). The Worksheet allocates the recipient's cost to
the payor by Line 3c and clips the payor's own credit at Line 6e. Letter § 2;
`submission_figures.py` section 2.1, pinned by tests in test_worksheet.py."""
import numpy as np
import matplotlib.pyplot as plt
from _common import w, npos, write_csv, out, theme, facts, top_header, bottom_footer
import submission_figures as sf

theme.apply("light"); P = theme.P


def scenarios():
    # CORRECTED 2026-09-08: routed through npos.analyze(box=1), same fix as
    # submission_figures.py section 2.1 -- this used to call net_income() directly with
    # the recipient hardcoded as "hoh" claiming all three children regardless of custody,
    # which is the recipient-claims-all default analyze() no longer uses for Box 1.
    kk = dict(a_gross=sf.RECIP_WEEKLY, b_gross=sf.PAYOR_GROSS / 52.0, children_under18=sf.KIDS, a_health=33.0, b_health=43.0)
    spec = [("Neither pays\nchild care", (0, 0, 0), (0, 0, 0)),
            ("Only the recipient\npays $300/wk", (100, 100, 100), (0, 0, 0)),
            ("Both pay\n$300/wk", (100, 100, 100), (100, 100, 100))]
    out_ = []
    pn = rn = None
    for label, a, b in spec:
        r = w.run(box=1, a_childcare=a, b_childcare=b, **kk)
        order_wk, his_cc_wk, her_cc_wk = r["7d"], sum(b), sum(a)
        total_cc_wk = his_cc_wk + her_cc_wk
        share = his_cc_wk / total_cc_wk if total_cc_wk else 0.0
        p = npos.analyze(sf.PAYOR_GROSS, sf.RECIP_GROSS, sf.KIDS, order_wk, total_cc_wk, share,
                          kids_under_13=sf.KIDS_UNDER_13, box=1)
        pn, rn = p["payor_net"], p["recip_net"]
        order, his_cc, her_cc = order_wk * 52, his_cc_wk * 52, her_cc_wk * 52
        out_.append(dict(label=label, order_wk=r["7d"], e7=r["7e"], him=p["payor_after"], her=p["recip_after"],
                         his_cc=his_cc, her_cc=her_cc, burden_net=(order + his_cc) / pn))
    return out_, pn, rn


def main():
    S, pn, rn = scenarios()
    none, hers, both = S
    total_cc = both["his_cc"] + both["her_cc"]
    his_extra = (both["order_wk"] * 52 + both["his_cc"]) - none["order_wk"] * 52
    her_extra = none["her"] - both["her"]
    income_share = (sf.PAYOR_GROSS / 52) / (sf.PAYOR_GROSS / 52 + sf.RECIP_WEEKLY)
    clip = (hers["order_wk"] - both["order_wk"]) * 52

    fig, axs = plt.subplots(1, 2, figsize=(14, 5.4), gridspec_kw=dict(width_ratios=[1.35, 1]))
    fig.subplots_adjust(wspace=0.30, top=0.68, bottom=0.24)

    # (a) who bears the combined $31,200
    ax = axs[0]
    cats = ["Share of combined\ngross income", "Share of the combined\nchild care bill"]
    payor_vals = [income_share, his_extra / total_cc]
    recip_vals = [1 - income_share, her_extra / total_cc]
    y = np.arange(2)[::-1]
    ax.barh(y, payor_vals, height=0.5, color=P["series"][0], label="Payor")
    ax.barh(y, recip_vals, left=[v + 0.004 for v in payor_vals], height=0.5, color=P["series"][1], label="Recipient")
    for yi, pv, rv in zip(y, payor_vals, recip_vals):
        ax.text(pv / 2, yi, f"{pv:.0%}", ha="center", va="center", fontsize=10, color="white")
        ax.text(pv + 0.004 + rv / 2, yi, f"{rv:.0%}", ha="center", va="center", fontsize=9, color=P["text"])
    ax.set_yticks(y); ax.set_yticklabels(cats)
    ax.set_xlim(0, 1.0); ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.set_title(f"(a) Who pays the \\${total_cc:,.0f}", loc="left", fontsize=10.5)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.18), ncols=2, frameon=False, fontsize=9)
    ax.grid(False)

    # (b) net position, three scenarios
    ax = axs[1]
    xs = np.arange(3); wd = 0.36
    ax.bar(xs - wd / 2, [s["him"] for s in S], width=wd, color=P["series"][0], label="Payor keeps (one person)")
    ax.bar(xs + wd / 2, [s["her"] for s in S], width=wd, color=P["series"][1], label="Recipient household holds (four people)")
    for i, s in enumerate(S):
        ax.text(i - wd / 2, s["him"] + 1500, f"${s['him'] / 1000:,.0f}k", ha="center", fontsize=8.5, color=P["text_2"])
        ax.text(i + wd / 2, s["her"] + 1500, f"${s['her'] / 1000:,.0f}k", ha="center", fontsize=8.5, color=P["text_2"])
    ax.set_xticks(xs); ax.set_xticklabels([s["label"] for s in S], fontsize=9)
    ax.set_ylim(0, 120_000); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v / 1000:,.0f}k"))
    ax.set_title("(b) Net position, three scenarios", loc="left", fontsize=10.5)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.18), ncols=1, frameon=False, fontsize=9)

    fig.subplots_adjust(top=top_header(fig, f"When both parents pay child care, the payor bears {his_extra / total_cc:.0%} of it on {income_share:.0%} of the income",
        f"Who pays a combined \\${total_cc:,.0f} of child care, and each parent's net position.",
        facts(1, 3, "\\$300/wk in each home", "\\$201,000 / \\$29,640")))
    bottom_footer(fig, f"The payor's own \\${both['his_cc']:,.0f} cuts the order by only \\${clip:,.0f}/yr (Line 6e clip). "
                  f"Order + own care = {both['burden_net']:.0%} of his net; 7e reads {both['e7']:.1%}. Per person he still leads "
                  f"(\\${both['him']:,.0f} vs \\${both['her'] / 4:,.0f}). Two of three under 13; premiums \\$43/\\$33.",
                  "model/submission_figures.py § 2.1")
    fig.savefig(out("fig8_both_pay.png"), dpi=170); fig.savefig(out("fig8_both_pay.svg")); plt.close(fig)
    write_csv("fig8_both_pay.csv", ["scenario", "order_wk", "line_7e", "payor_keeps", "recipient_holds", "his_childcare", "her_childcare", "order_plus_own_care_pct_net"],
              [(s["label"].replace("\n", " "), s["order_wk"], s["e7"], s["him"], s["her"], s["his_cc"], s["her_cc"], s["burden_net"]) for s in S]
              + [("combined childcare", total_cc, "", his_extra, her_extra, "", "", ""),
                 ("shares", "", "", his_extra / total_cc, her_extra / total_cc, income_share, clip, "")])
    print("fig8 written", f"payor bears {his_extra / total_cc:.3f}; income share {income_share:.4f}; clip ${clip:,.0f}")


if __name__ == "__main__":
    main()
