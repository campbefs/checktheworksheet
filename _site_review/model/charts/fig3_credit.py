"""Figure 3: the equal-parenting credit collapses as the income gap widens (current, Variant A, Variant B),
and the overnight share the order implies under a cross-credit at factors 1.5 and 2.0. Three children."""
import numpy as np
import matplotlib.pyplot as plt
from _common import w, write_csv, out, theme, SOURCE_SRC, NOTE_CONV, EXAMPLE, HEALTH_LO, HEALTH_HI, facts, top_header, bottom_footer
import box1_fix as bf

theme.apply("light"); P = theme.P
HI = EXAMPLE["payor"]; KIDS = 3


def main():
    los = np.linspace(2_000, 150_000, 75)
    rows = []
    for lo in los:
        b2 = w.run(box=2, a_gross=lo / 52, b_gross=HI / 52, children_under18=KIDS, a_health=HEALTH_LO, b_health=HEALTH_HI)
        res = {v: bf.run(v, a_gross=lo / 52, b_gross=HI / 52, children_under18=KIDS, a_health=HEALTH_LO, b_health=HEALTH_HI)
               for v in ("current", "A", "B")}
        if b2["payor"] != "B" or any(r["payor"] != "B" for r in res.values()):
            continue
        share = res["current"]["B_3c"]
        red = {v: 1 - res[v]["7d"] / b2["7d"] for v in res}
        imp15 = bf.implied_overnight_share(res["current"], 1.5)
        imp20 = bf.implied_overnight_share(res["current"], 2.0)
        rows.append((lo, share, b2["7d"], res["current"]["7d"], res["A"]["7d"], res["B"]["7d"],
                     red["current"], red["A"], red["B"], imp15, imp20))
    rows.sort(key=lambda r: r[1])
    x = [r[1] for r in rows]
    fig, axs = plt.subplots(1, 2, figsize=(15, 5.6))
    fig.subplots_adjust(wspace=0.22, top=0.71, bottom=0.24)
    ax = axs[0]
    ax.plot(x, [r[6] for r in rows], color=P["series"][3], lw=2.2, label="Worksheet today (Box 1 vs Box 2)")
    ax.plot(x, [r[7] for r in rows], color=P["series"][0], lw=2.2, label="Variant A: 6e applied once")
    ax.plot(x, [r[8] for r in rows], color=P["series"][2], lw=2.2, label="Variant B: cross-credit, factor 1.5")
    ax.set_title("(a) Reduction in the order for equal time", loc="left", fontsize=10.5)
    ax.set_ylim(0, 1); ax.set_ylabel("Reduction")
    ax = axs[1]
    ax.plot(x, [r[9] for r in rows], color=P["series"][2], lw=2.2, label="Duplication factor 1.5 (as in Variant B)")
    ax.plot(x, [r[10] for r in rows], color=P["series"][1], lw=2.2, label="Duplication factor 2.0")
    ax.axhline(0.5, color=P["axis"], lw=1, ls="--"); ax.text(0.51, 0.51, "actual: 50% of overnights", fontsize=8.5, color=P["text_2"])
    ax.set_title("(b) Overnight share the order implies", loc="left", fontsize=10.5)
    ax.set_ylim(0, 0.6); ax.set_ylabel("Implied payor overnight share")
    for ax in axs:
        ax.set_xlim(0.5, 1.0)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.set_xlabel("Payor's share of combined available income")
        ax.axvline(0.877, color=P["text_mute"], lw=0.8); ax.text(0.879, ax.get_ylim()[1] * 0.93, "worked\nexample", fontsize=8, color=P["text_mute"])
        ax.legend(loc="upper left", bbox_to_anchor=(0, -0.16), ncols=3, frameon=False, fontsize=9)
    fig.subplots_adjust(top=top_header(fig, "The equal-time credit collapses with the income gap; a cross-credit only narrows",
        "Reduction in the order for equal time vs the one-third-time order, and the overnight share it implies.",
        facts("1v2", 3, "None (base support)", f"\\${HI:,.0f} / varies")))
    bottom_footer(fig, "Implied share blank below the Line 5c floor; sensitive to the factor. Variants: box1_fix.py. " + NOTE_CONV, SOURCE_SRC)
    fig.savefig(out("fig3_credit_collapse.png"), dpi=170); fig.savefig(out("fig3_credit_collapse.svg")); plt.close(fig)
    write_csv("fig3_credit_collapse.csv", ["lower_gross", "payor_3c", "box2_7d", "box1_7d", "variantA_7d", "variantB_7d",
                                           "reduction_current", "reduction_A", "reduction_B", "implied_share_1.5", "implied_share_2.0"], rows)
    print("fig3 written", len(rows))


if __name__ == "__main__":
    main()
