"""Shared harness for the paper's figures. Every figure writes its plotted values to CSV beside the PNG."""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))          # model/
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
import net_position as npos  # noqa: E402
import worksheet as w  # noqa: E402
import theme  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "output", "charts")
os.makedirs(OUT, exist_ok=True)

# The letter's worked example, marked on the three-child panels.
EXAMPLE = dict(payor=201_000.0, recip=570.0 * 52, kids=3)
HEALTH_LO, HEALTH_HI = 33.0, 43.0      # weekly premiums, as in the letter
# Tax credits for children under 13 (MA CFTC) are set to ZERO on the generic grids: it understates
# the recipient's position by $440/child/yr, the direction that weakens the paper's claim.
KIDS_UNDER_13 = 0
SOURCE = ("Source: model/worksheet.py (CJ-D 304, matches the form's own scripts), model/net_position.py "
          "(TY2026 federal + MA). MA under-13 credit set to zero. Health premiums \\$33/\\$43 per week.")


CUSTODY = {
    1: "Joint, equal time (Box 1)",
    2: "Primary with the lower earner (Box 2)",
    3: "Split, one child each (Box 3)",
    "1v2": "Joint (Box 1) vs primary (Box 2)",
    "1v3": "Joint (Box 1) vs split (Box 3)",
}
SOURCE_SRC = ("model/worksheet.py (CJ-D 304, matches the form's own scripts); "
              "model/net_position.py (TY2026 federal + MA tax)")
NOTE_CONV = "Premiums \\$43/\\$33 a week; MA under-13 credit set to zero."
NOTE_MASK = "Masked where the lower earner would out-earn the higher. "


def facts(custody, kids, childcare="None (base support)", incomes="Vary (axes)"):
    """The fact line every figure carries: custody, children, child care, incomes. Short values only;
    conventions go in the Notes footer."""
    kids_s = kids if isinstance(kids, str) else str(kids)
    return [("Custody", CUSTODY[custody]), ("Children", kids_s), ("Child care", childcare), ("Incomes", incomes)]


def top_header(fig, title="", subtitle="", pairs=None, x=0.06, right=0.97, top=0.975, panel_gap_pt=26.0):
    """Figure-level header wrapped to the figure width, stacked from the top. Returns the figure fraction the
    plot area must stay below; pass it to fig.subplots_adjust(top=...)."""
    dpi = fig.dpi
    W, H = fig.get_size_inches() * dpi
    bottom = theme.header(fig, title, subtitle, pairs, x_px=x * W, width_px=(right - x) * W,
                          anchor_px=top * H, anchor="top")
    return (bottom - panel_gap_pt * dpi / 72) / H


def bottom_footer(fig, notes="", source="", x=0.06, right=0.97, gap_pt=16.0):
    """Figure-level footer below everything the axes own (legends included). Call last, after all axes are drawn."""
    dpi = fig.dpi
    W, H = fig.get_size_inches() * dpi
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    y0 = min(ax.get_tightbbox(r).y0 for ax in fig.axes)
    theme.footer(fig, notes, source, x_px=x * W, width_px=(right - x) * W, top_px=y0 - gap_pt * dpi / 72)


def out(name):
    return os.path.join(OUT, name)


def write_csv(name, header, rows):
    with open(out(name), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(header)
        wr.writerows(rows)


def order(hi, lo, kids, box=1, cc_lo_total=0.0):
    """Weekly Box order with the higher earner as Parent B. Returns worksheet result."""
    per = cc_lo_total / kids if cc_lo_total else 0.0
    return w.run(box=box, a_gross=lo / 52.0, b_gross=hi / 52.0, children_under18=kids,
                 a_health=HEALTH_LO, b_health=HEALTH_HI,
                 a_childcare=(per,) * kids if cc_lo_total else (), b_childcare=())


def grid(kids, box=1, hi_range=(60_000, 300_000, 49), lo_range=(0, 120_000, 25)):
    """Arrays over higher-earner x lower-earner gross. Masked where lower > higher."""
    hi = np.linspace(*hi_range)
    lo = np.linspace(*lo_range)
    H, L = np.meshgrid(hi, lo)
    shape = H.shape
    gap_h = np.full(shape, np.nan)      # recipient household net - payor net
    gap_pp = np.full(shape, np.nan)     # per person
    pct_net = np.full(shape, np.nan)    # order / payor net
    lag = np.full(shape, np.nan)        # true % of net - Line 7e reading
    e7 = np.full(shape, np.nan)
    ordr = np.full(shape, np.nan)
    for i in range(shape[0]):
        for j in range(shape[1]):
            h, l = H[i, j], L[i, j]
            if l > h:
                continue
            r = order(h, l, kids, box)
            wk = r["7d"]
            # who pays: the worksheet says; with B the higher earner it is B except near-equal incomes
            payor_is_hi = r["payor"] == "B"
            pg, rg = (h, l) if payor_is_hi else (l, h)
            pos = npos.analyze(pg, rg, kids, wk, 0.0, 0.0, kids_under_13=KIDS_UNDER_13)
            sign = 1.0 if payor_is_hi else -1.0   # keep "higher earner" as the reference party
            gap_h[i, j] = sign * (pos["recip_after"] - pos["payor_after"])
            gap_pp[i, j] = sign * (pos["recip_after"] / (1 + kids) - pos["payor_after"])
            pct_net[i, j] = pos["support_pct_of_payor_net"]
            e7[i, j] = r["7e"]
            lag[i, j] = pos["support_pct_of_payor_net"] - r["7e"]
            ordr[i, j] = wk
    return dict(hi=hi, lo=lo, H=H, L=L, gap_h=gap_h, gap_pp=gap_pp, pct_net=pct_net, lag=lag, e7=e7, order=ordr)
