"""Figure 5: the fifty-one jurisdictions at one fact pattern. (a)/(b) monthly orders S1/S2, MA highlighted,
tier-50 rows (Georgia held out). (c) tile map: formula credit at 122 overnights, 28 yes / 23 no."""
import json
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from _common import ROOT, write_csv, out, theme, facts

theme.apply("light"); P = theme.P
D = os.path.join(ROOT, "data", "fifty-state")
ABBR = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
        "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
        "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
        "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
        "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
        "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
        "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}
TILES = {"AK": (0, 0), "ME": (0, 10), "VT": (1, 9), "NH": (1, 10),
         "WA": (2, 0), "ID": (2, 1), "MT": (2, 2), "ND": (2, 3), "MN": (2, 4), "IL": (2, 5), "WI": (2, 6), "MI": (2, 7), "NY": (2, 8), "MA": (2, 9), "RI": (2, 10),
         "OR": (3, 0), "NV": (3, 1), "WY": (3, 2), "SD": (3, 3), "IA": (3, 4), "IN": (3, 5), "OH": (3, 6), "PA": (3, 7), "NJ": (3, 8), "CT": (3, 9),
         "CA": (4, 0), "UT": (4, 1), "CO": (4, 2), "NE": (4, 3), "MO": (4, 4), "KY": (4, 5), "WV": (4, 6), "VA": (4, 7), "MD": (4, 8), "DE": (4, 9),
         "AZ": (5, 1), "NM": (5, 2), "KS": (5, 3), "AR": (5, 4), "TN": (5, 5), "NC": (5, 6), "SC": (5, 7), "DC": (5, 8),
         "OK": (6, 3), "LA": (6, 4), "MS": (6, 5), "AL": (6, 6), "GA": (6, 7),
         "HI": (7, 0), "TX": (7, 3), "FL": (7, 7)}
assert len(TILES) == 51 and set(TILES) == set(ABBR.values())


def strip(rows, key, title, name, custody):
    rows = sorted(rows, key=lambda r: r[key])
    fig, ax = theme.figure(9, 10)
    fig.subplots_adjust(bottom=0.05, top=0.90)
    y = range(len(rows))
    colors = [P["series"][1] if r["state"] == "Massachusetts" else P["series"][0] for r in rows]
    ax.barh(list(y), [r[key] for r in rows], color=colors, height=0.62)
    ax.set_yticks(list(y)); ax.set_yticklabels([r["state"] for r in rows], fontsize=8.5)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.grid(axis="y", visible=False)
    theme.finish(ax, title=title,
                 subtitle="Monthly order at one fact pattern. Georgia held out.",
                 comma=False,
                 pairs=facts(custody, 3, "None (base support)", "\\$201,000 / \\$29,640"),
                 notes="Each row profiled from primary sources, computed twice blind, reconciled, attacked. Own premiums "
                       "(\\$43/\\$33) as each state treats them. One fact pattern only.",
                 source="data/fifty-state/tier-50-2026-09-05.json")
    theme.save(fig, out(name))


def main():
    tier = json.load(open(os.path.join(D, "tier-50-2026-09-05.json")))
    strip(tier, "s1", "Equal parenting time: Massachusetts orders the most of fifty jurisdictions", "fig5a_states_S1.png", 1)
    strip(tier, "s2", "Lower earner primary: only Hawaii's Melson formula orders more than Massachusetts", "fig5b_states_S2.png", 2)
    write_csv("fig5_states.csv", ["state", "s1", "s2"], [(r["state"], r["s1"], r["s2"]) for r in tier])

    cr = json.load(open(os.path.join(D, "credit-at-122-2026-09-05.json")))
    fig, ax = theme.figure(11, 7.4)
    for r in cr["rows"]:
        ab = ABBR[r["state"]]; row, col = TILES[ab]
        yes = r["credit_at_122"] == "Y"
        face = P["series"][0] if yes else P["div_mid"]
        ax.add_patch(Rectangle((col, -row), 0.94, 0.94, facecolor=face, edgecolor=P["surface"], lw=2))
        ax.text(col + 0.47, -row + 0.47, ab, ha="center", va="center", fontsize=10, weight="bold" if ab == "MA" else "normal",
                color=P["surface"] if yes else P["text"])
    ax.set_xlim(-0.2, 11.2); ax.set_ylim(-7.3, 1.2); ax.set_aspect("equal"); ax.axis("off")
    t = cr["tally"]
    theme.finish(ax, title=f"A parent with the children a third of the time gets a formula credit in {t['Y']} jurisdictions and none in {t['N']}",
                 subtitle="Blue: a formula credit at 122 overnights a year. Grey: none.",
                 pairs=[("Counted", "Any formula credit at 122 overnights"), ("Children", "3"),
                        ("Child care", "None"), ("Incomes", "\\$201,000 / \\$29,640")],
                 notes="A count, not a dollar amount. Massachusetts's Box 2 is the one-third case.",
                 source="data/fifty-state/credit-at-122-2026-09-05.json")
    theme.save(fig, out("fig5c_credit_at_122_tilemap.png"))
    print("fig5 written")


if __name__ == "__main__":
    main()
