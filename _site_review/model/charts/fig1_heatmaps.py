"""Figure 1: Massachusetts net-position heatmaps, 1/2/3 children, Box 1 (main) and Box 2 (appendix).

Panels: (a) recipient household net minus payor net after the order; (b) the same per person;
(c) order as % of payor net; (d) the units lag, true % of net minus Line 7e's reading.
Also writes fig1_headline: panel (a) for 1, 2 and 3 children side by side."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from _common import grid, write_csv, out, theme, EXAMPLE, SOURCE_SRC, NOTE_CONV, NOTE_MASK, facts, top_header, bottom_footer

theme.apply("light")
P = theme.P if hasattr(theme, "P") else theme.LIGHT
DIV = plt.matplotlib.colors.LinearSegmentedColormap.from_list("div", [P["div_low"], P["div_mid"], P["div_high"]])
SEQ = plt.matplotlib.colors.LinearSegmentedColormap.from_list("seq", P["seq"])


def _ax_money(ax):
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))
    ax.set_xlabel("Higher earner, gross per year")
    ax.set_ylabel("Lower earner, gross per year")


def _mark(ax, kids):
    if kids == EXAMPLE["kids"]:
        ax.plot(EXAMPLE["payor"], EXAMPLE["recip"], marker="o", ms=7, mfc="none", mec=P["text"], mew=1.6)
        ax.annotate("worked example", (EXAMPLE["payor"], EXAMPLE["recip"]), xytext=(8, 8),
                    textcoords="offset points", fontsize=8.5, color=P["text"])


def panel(ax, g, key, title, diverging=True, contour=0.0, fmt="${:,.0f}", pct=False, kids=3, vmax=None):
    Z = g[key]
    if diverging:
        lim = np.nanmax(np.abs(Z))
        im = ax.pcolormesh(g["H"], g["L"], Z, cmap=DIV, norm=TwoSlopeNorm(0, -lim, lim), shading="nearest")
    else:
        im = ax.pcolormesh(g["H"], g["L"], Z, cmap=SEQ, shading="nearest", vmin=0, vmax=vmax)
    cs = ax.contour(g["H"], g["L"], Z, levels=[contour], colors=[P["text"]], linewidths=1.4)
    ax.clabel(cs, fmt=(lambda v: f"{v:.0%}") if pct else (lambda v: "even"), fontsize=8.5)
    cb = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.02)
    cb.ax.yaxis.set_major_formatter(plt.FuncFormatter((lambda v, _: f"{v:.0%}") if pct else (lambda v, _: f"-${abs(v)/1000:,.0f}k" if v < 0 else f"${v/1000:,.0f}k")))
    cb.outline.set_visible(False)
    _ax_money(ax)
    _mark(ax, kids)
    ax.set_title(title, loc="left", fontsize=10.5, color=P["text"], pad=6)
    ax.grid(False)


def main():
    headline = {}
    for box in (1, 2):
        for kids in (1, 2, 3):
            g = grid(kids, box)
            fig, axs = plt.subplots(2, 2, figsize=(13, 10.5))
            fig.subplots_adjust(hspace=0.42, wspace=0.28, top=0.83, bottom=0.10)
            panel(axs[0, 0], g, "gap_h", "(a) Recipient household net minus payor net, per year", kids=kids)
            panel(axs[0, 1], g, "gap_pp", "(b) The same per person (recipient household ÷ (1 + children))", kids=kids)
            panel(axs[1, 0], g, "pct_net", "(c) Order as a share of payor NET income (line: 40%)",
                  diverging=False, contour=0.40, pct=True, kids=kids, vmax=0.60)
            # panel (d): sequential lag with the 7e = 40% contour drawn from e7
            Z = g["lag"]
            im = axs[1, 1].pcolormesh(g["H"], g["L"], Z, cmap=SEQ, shading="nearest", vmin=0, vmax=0.15)
            cs = axs[1, 1].contour(g["H"], g["L"], g["e7"], levels=[0.40], colors=[P["text"]], linewidths=1.4)
            axs[1, 1].clabel(cs, fmt=lambda v: "7e reads 40%", fontsize=8.5)
            cb = plt.colorbar(im, ax=axs[1, 1], fraction=0.046, pad=0.02)
            cb.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
            cb.outline.set_visible(False)
            _ax_money(axs[1, 1]); _mark(axs[1, 1], kids); axs[1, 1].grid(False)
            axs[1, 1].set_title("(d) Units lag: true share of payor net minus Line 7e's gross-based reading",
                                loc="left", fontsize=10.5, color=P["text"], pad=6)
            boxname = "Box 1 (equal time)" if box == 1 else "Box 2 (primary with the lower earner)"
            fig.subplots_adjust(top=top_header(fig, f"Massachusetts 2025 Guidelines: {kids} child{'ren' if kids > 1 else ''}, {boxname}",
                "Who holds more after the order, and what Line 7e sees.",
                facts(box, kids), x=0.06))
            bottom_footer(fig, NOTE_MASK + "Panels (c) and (d): fixed scales across all six figures. " + NOTE_CONV, SOURCE_SRC)
            name = f"fig1_heatmap_{kids}child_box{box}"
            fig.savefig(out(name + ".png"), dpi=170); fig.savefig(out(name + ".svg")); plt.close(fig)
            rows = [(h, l, g["order"][i, j], g["gap_h"][i, j], g["gap_pp"][i, j], g["pct_net"][i, j], g["e7"][i, j], g["lag"][i, j])
                    for i, l in enumerate(g["lo"]) for j, h in enumerate(g["hi"]) if not np.isnan(g["order"][i, j])]
            write_csv(name + ".csv", ["higher_gross", "lower_gross", "order_wk", "gap_household", "gap_per_person",
                                      "order_pct_payor_net", "line_7e", "lag"], rows)
            if box == 1:
                headline[kids] = g
            print(name, "written")
    # headline: panel (a) for 1/2/3 children, Box 1
    fig, axs = plt.subplots(1, 3, figsize=(17, 6.2))
    fig.subplots_adjust(wspace=0.32, top=0.72, bottom=0.15)
    lim = 40_000.0   # shared, clipped: the one-child corner runs past -$100k and would wash out the rest
    for ax, kids in zip(axs, (1, 2, 3)):
        g = headline[kids]
        im = ax.pcolormesh(g["H"], g["L"], np.clip(g["gap_h"], -lim, lim), cmap=DIV,
                           norm=TwoSlopeNorm(0, -lim, lim), shading="nearest")
        cs = ax.contour(g["H"], g["L"], g["gap_h"], levels=[0], colors=[P["text"]], linewidths=1.4)
        ax.clabel(cs, fmt=lambda v: "even", fontsize=8.5)
        _ax_money(ax); _mark(ax, kids); ax.grid(False)
        ax.set_title(f"{kids} child{'ren' if kids > 1 else ''}", loc="left", fontsize=11, color=P["text"], pad=8)
    cb = fig.colorbar(im, ax=axs, fraction=0.02, pad=0.02, extend="both")
    cb.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v/1000:+,.0f}k"))
    cb.outline.set_visible(False); cb.set_label("recipient household minus payor, net per year", fontsize=9)
    fig.subplots_adjust(top=top_header(fig, "The number of children decides which household holds more after the order",
        "Recipient household net minus payor net. Red: recipient ahead; blue: payor ahead.",
        facts(1, "1, 2 and 3"), x=0.05))
    bottom_footer(fig, "Per person the payor leads throughout (E02). Colour capped at ±\\$40k. " + NOTE_MASK + NOTE_CONV,
                  SOURCE_SRC, x=0.05)
    fig.savefig(out("fig1_headline_household_gap.png"), dpi=170); fig.savefig(out("fig1_headline_household_gap.svg")); plt.close(fig)
    print("fig1_headline_household_gap written")


if __name__ == "__main__":
    main()
