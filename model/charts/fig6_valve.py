"""Figure 6: the 40% hardship valve reads gross-derived income while the burden is paid from net.
As child care claimed by the recipient rises, Line 7e (order / payor 3a) and the true burden (order / payor net)
diverge; the valve fires where 7e reaches 40%. Worked example: $201,000 / $29,640, three children, Box 1."""
import numpy as np
import matplotlib.pyplot as plt
from _common import write_csv, out, theme, facts
import submission_figures as sf

theme.apply("light"); P = theme.P


def main():
    ccs = np.arange(0, 1291, 10.0)          # up to the $430 x 3 ceiling
    rows = []
    for cc in ccs:
        r = sf.sheet(cc)
        pos = sf.position(r, cc)
        rows.append((cc, r["7d"], r["7e"], pos["support_pct_of_payor_net"]))
    e7 = np.array([r[2] for r in rows]); tru = np.array([r[3] for r in rows])
    fire = ccs[np.argmax(e7 >= 0.40)] if (e7 >= 0.40).any() else None
    true40 = ccs[np.argmax(tru >= 0.40)] if (tru >= 0.40).any() else None
    fig, ax = theme.figure(9.5, 5.2)
    ax.plot(ccs, tru, color=P["series"][1], lw=2.2, label="Order as a share of the payor's NET income")
    ax.plot(ccs, e7, color=P["series"][0], lw=2.2, label="Line 7e: order as a share of Line 3a (gross-derived)")
    ax.axhline(0.40, color=P["axis"], lw=1, ls="--")
    ax.text(300, 0.405, "Section IV.C threshold, 40%", fontsize=8.5, color=P["text_2"])
    if true40 is not None:
        ax.axvline(true40, color=P["series"][1], lw=0.8, ls=":")
        ax.text(true40 + 8, 0.08, f"true burden reaches 40%\nat \\${true40:,.0f}/wk", fontsize=8.5, color=P["text"])
    if fire is not None:
        ax.axvline(fire, color=P["series"][0], lw=0.8, ls=":")
        ax.text(fire + 8, 0.16, f"Line 7e reaches 40%\nat \\${fire:,.0f}/wk; true burden {tru[np.argmax(e7 >= 0.40)]:.0%}", fontsize=8.5, color=P["text"])
    ax.set_xlim(0, 1290); ax.set_ylim(0, 0.8)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    theme.finish(ax, title="The hardship valve fires late because it reads the wrong income",
                 subtitle="Line 7e's reading vs the true share of net income as claimed child care rises.",
                 xlabel="Child care claimed, per week", pct=True,
                 pairs=facts(1, 3, "Rises to the \\$430/child ceiling (recipient)", "\\$201,000 / \\$29,640"),
                 notes="Child care is included in the order. 7e is what the form computes; net is what is paid. "
                       "Two of three children under 13 (MA credit); premiums \\$43/\\$33.",
                 source="model/submission_figures.py")
    theme.save(fig, out("fig6_valve_units_lag.png"))
    write_csv("fig6_valve_units_lag.csv", ["childcare_wk", "order_wk", "line_7e", "order_pct_payor_net"], rows)
    print("fig6 written", fire, true40)


if __name__ == "__main__":
    main()
