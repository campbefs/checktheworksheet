"""Figure 4: of the payor's next dollar, how much is kept. Recipient $570/wk, three children, Box 1."""
import numpy as np
import matplotlib.pyplot as plt
from _common import write_csv, out, theme, facts
import marginal_retention as mr

theme.apply("light"); P = theme.P


def main():
    xs = np.arange(100_000, 400_001, 5_000)
    rows = []
    fig, ax = theme.figure(9, 5)
    for cc, color, label in ((0.0, P["series"][0], "No child care"), (300.0, P["series"][1], "\\$300/week child care claimed")):
        after = np.array([mr.keep(x, cc)[1] for x in xs])
        kept = np.diff(after) / np.diff(xs)
        mid = (xs[1:] + xs[:-1]) / 2
        ax.plot(mid, kept, color=color, lw=2.2, label=label)
        rows += [(cc, m, k) for m, k in zip(mid, kept)]
    ax.axhline(0.5, color=P["axis"], lw=1, ls="--")
    ax.set_ylim(0, 0.7); ax.set_xlim(100_000, 400_000)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))
    theme.finish(ax, title="Of the next dollar, the payor keeps between a third and a half",
                 subtitle="After federal and state tax and the change in the order.",
                 xlabel="Payor gross income", pct=True,
                 pairs=facts(1, 3, "None vs \\$300/wk (recipient)", "Varies / \\$29,640"),
                 notes="\\$5,000 steps. Dashed: 50 cents. Two of three children under 13 (MA credit); premiums \\$43/\\$33.",
                 source="model/marginal_retention.py")
    theme.save(fig, out("fig4_marginal_retention.png"))
    write_csv("fig4_marginal_retention.csv", ["childcare_wk", "payor_gross_mid", "kept_of_next_dollar"], rows)
    print("fig4 written")


if __name__ == "__main__":
    main()
