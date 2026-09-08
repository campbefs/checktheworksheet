"""
House chart style.

Usage:
    import theme
    fig, ax = theme.figure()
    ax.plot(x, y)
    theme.finish(ax, title="...", subtitle="...", source="...")
    theme.save(fig, "figures/my_chart.png")

Everything is set here so charts come out consistent without per-chart fiddling.
To restyle every chart at once, change values in this file only.

Palette and mark specs follow the `dataviz` skill reference instance:
categorical hues are assigned in fixed order and never cycled; gridlines are
hairline and recessive; lines are 2px; a legend appears for >=2 series and never
for one; text never wears the series color.
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------

LIGHT = {
    "surface":   "#fcfcfb",
    "text":      "#0b0b0b",
    "text_2":    "#52514e",
    "text_mute": "#7a7975",
    "grid":      "#e6e5e1",
    "axis":      "#c9c8c3",
    # categorical, fixed order — never reorder, never cycle past 8
    "series": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
               "#e87ba4", "#008300", "#4a3aa7", "#e34948"],
    "seq":     ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5",
                "#256abf", "#184f95", "#0d366b"],
    "div_low": "#2a78d6",
    "div_mid": "#f0efec",
    "div_high": "#e34948",
}

DARK = {
    "surface":   "#1a1a19",
    "text":      "#ffffff",
    "text_2":    "#c3c2b7",
    "text_mute": "#8f8e86",
    "grid":      "#2e2e2c",
    "axis":      "#454541",
    "series": ["#3987e5", "#d95926", "#199e70", "#c98500",
               "#d55181", "#008300", "#9085e9", "#e66767"],
    "seq":     ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5",
                "#256abf", "#184f95", "#0d366b"],
    "div_low": "#3987e5",
    "div_mid": "#383835",
    "div_high": "#e66767",
}

P = LIGHT          # active palette; swapped by apply()
_MODE = "light"

FONT = ["Helvetica Neue", "Helvetica", "Avenir Next", "Arial", "DejaVu Sans"]

# Scatter / bubble / small-multiple charts compare ALL pairs, not just adjacent
# ones — the palette only validates all-pairs for the first three slots.
# Past three series in those forms, fold to "Other" or facet.
ALL_PAIRS_SAFE = 3


# --------------------------------------------------------------------------
# Setup
# --------------------------------------------------------------------------

def apply(mode: str = "light") -> None:
    """Set global rcParams. Call once at the top of a script."""
    global P, _MODE
    P = DARK if mode == "dark" else LIGHT
    _MODE = mode

    mpl.rcParams.update({
        "figure.facecolor":  P["surface"],
        "axes.facecolor":    P["surface"],
        "savefig.facecolor": P["surface"],
        "savefig.dpi":       200,
        "savefig.bbox":      "tight",
        "savefig.pad_inches": 0.3,
        "figure.dpi":        110,

        "font.family":     "sans-serif",
        "font.sans-serif": FONT,
        "font.size":       10,

        "text.color":       P["text"],
        "axes.labelcolor":  P["text_2"],
        "axes.labelsize":   10,
        "axes.titlesize":   13,
        "axes.titleweight": "semibold",
        "axes.titlecolor":  P["text"],
        "axes.titlelocation": "left",
        "axes.titlepad":    12,

        # recessive frame — bottom rule only
        "axes.edgecolor":   P["axis"],
        "axes.linewidth":   0.8,
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "axes.spines.left":   False,
        "axes.spines.bottom": True,

        # hairline solid grid, y only
        "axes.grid":       True,
        "axes.grid.axis":  "y",
        "grid.color":      P["grid"],
        "grid.linewidth":  0.8,
        "grid.linestyle":  "-",
        "axes.axisbelow":  True,

        "xtick.color":      P["text_2"],
        "ytick.color":      P["text_2"],
        "xtick.labelsize":  9.5,
        "ytick.labelsize":  9.5,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "xtick.major.pad":  7,
        "ytick.major.pad":  7,

        "lines.linewidth":       2.0,
        "lines.solid_capstyle":  "round",
        "lines.solid_joinstyle": "round",
        "lines.markersize":      6,

        "legend.frameon":     False,
        "legend.fontsize":    9.5,
        "legend.labelcolor":  P["text_2"],
        "legend.handlelength": 1.4,
        "legend.handletextpad": 0.6,
        "legend.columnspacing": 1.6,

        "axes.prop_cycle": mpl.cycler(color=P["series"]),
    })


def figure(w: float = 8.0, h: float = 4.5, **kw):
    """A correctly-sized figure. Defaults to a 16:9-ish single chart."""
    return plt.subplots(figsize=(w, h), **kw)


# --------------------------------------------------------------------------
# Finishing
# --------------------------------------------------------------------------

def wrap_to(fig, text: str, fontsize: float, width_px: float, weight: str = "normal") -> str:
    """Wrap `text` so no line renders wider than width_px at this fontsize. Measured, not guessed."""
    import textwrap
    r = fig.canvas.get_renderer()
    out = []
    for line in text.split("\n"):
        t = fig.text(0, 0, line, fontsize=fontsize, weight=weight)
        w = t.get_window_extent(renderer=r).width; t.remove()
        if w <= width_px or len(line) < 12:
            out.append(line); continue
        per = max(12, int(len(line) * width_px / w) - 1)
        wrapped = textwrap.fill(line, per, break_long_words=False, break_on_hyphens=False)
        for _ in range(40):
            t = fig.text(0, 0, wrapped, fontsize=fontsize, weight=weight)
            w2 = t.get_window_extent(renderer=r).width; t.remove()
            if w2 <= width_px or per <= 12:
                break
            per -= 2
            wrapped = textwrap.fill(line, per, break_long_words=False, break_on_hyphens=False)
        out.append(wrapped)
    return "\n".join(out)


def keyline(fig, pairs, *, x_px: float, width_px: float, top_px: float, draw: bool = True) -> float:
    """
    The fact line: small muted labels with dark values, separated by middle dots,
    wrapping at pair boundaries so it never runs past width_px. Returns the bottom
    edge (px). draw=False only measures.
    """
    dpi = fig.dpi
    W, H = fig.get_size_inches() * dpi
    r = fig.canvas.get_renderer()
    lab_fs, val_fs = 7.6, 9.2
    gap_lv = 4 * dpi / 72          # label to value
    gap_pair = 14 * dpi / 72       # value to next label (the dot sits in the middle)
    line_h = 15 * dpi / 72

    def measure(text, fs, weight="normal"):
        t = fig.text(0, 0, text, fontsize=fs, weight=weight)
        w = t.get_window_extent(renderer=r).width; t.remove(); return w

    x, y = x_px, top_px
    first_on_line = True
    for label, value in pairs:
        lab = label.upper()
        w_lab, w_val = measure(lab, lab_fs), measure(value, val_fs, "normal")
        w_pair = w_lab + gap_lv + w_val
        if not first_on_line and x + gap_pair + w_pair > x_px + width_px:
            x, y = x_px, y - line_h; first_on_line = True
        if not first_on_line:
            if draw:
                fig.text((x + gap_pair / 2) / W, y / H, "·", fontsize=val_fs, color=P["text_mute"], va="top", ha="center")
            x += gap_pair
        if draw:
            fig.text(x / W, (y - 1.6 * dpi / 72) / H, lab, fontsize=lab_fs, color=P["text_mute"], va="top", ha="left")
            fig.text((x + w_lab + gap_lv) / W, y / H, value, fontsize=val_fs, color=P["text"], va="top", ha="left")
        x += w_pair
        first_on_line = False
    return y - line_h


def header(fig, title: str = "", subtitle: str = "", pairs=None, *, x_px: float, width_px: float,
           anchor_px: float, anchor: str = "top", gap_pt: float = 6.0) -> float:
    """
    Title, subtitle and fact line, each wrapped to width_px and stacked from measured
    heights. anchor="top": stack downward from anchor_px and return the bottom edge (px).
    anchor="bottom": stack upward from anchor_px and return the top edge (px).
    """
    dpi = fig.dpi
    W, H = fig.get_size_inches() * dpi
    gap = gap_pt * dpi / 72
    r = fig.canvas.get_renderer()
    blocks = []                                   # ("text", txt, fs, wt, color) | ("pairs", pairs)
    if title:
        blocks.append(("text", wrap_to(fig, title, 13.0, width_px, "bold"), 13.0, "bold", P["text"]))
    if subtitle:
        blocks.append(("text", wrap_to(fig, subtitle, 10.5, width_px), 10.5, "normal", P["text_2"]))
    if pairs:
        blocks.append(("pairs", pairs))

    def height(b):
        if b[0] == "text":
            t = fig.text(0, 0, b[1], fontsize=b[2], weight=b[3], linespacing=1.25)
            h = t.get_window_extent(renderer=r).height; t.remove(); return h
        return top_px_dummy - keyline(fig, b[1], x_px=x_px, width_px=width_px, top_px=top_px_dummy, draw=False)

    top_px_dummy = H
    heights = [height(b) for b in blocks]
    total = sum(heights) + gap * (len(blocks) - 1) + (4 * dpi / 72 if pairs else 0)
    y = anchor_px if anchor == "top" else anchor_px + total
    for b, h in zip(blocks, heights):
        if b[0] == "text":
            fig.text(x_px / W, y / H, b[1], fontsize=b[2], weight=b[3], color=b[4], va="top", ha="left", linespacing=1.25)
        else:
            y -= 4 * dpi / 72
            keyline(fig, b[1], x_px=x_px, width_px=width_px, top_px=y)
        y -= h + gap
    return y if anchor == "top" else anchor_px + total


def footer(fig, notes: str = "", source: str = "", *, x_px: float, width_px: float, top_px: float,
           gap_pt: float = 5.0) -> float:
    """Hairline rule, then Notes (italic) and Source, wrapped to width_px, stacked downward from top_px."""
    dpi = fig.dpi
    W, H = fig.get_size_inches() * dpi
    gap = gap_pt * dpi / 72
    r = fig.canvas.get_renderer()
    y = top_px
    fig.add_artist(__import__("matplotlib").lines.Line2D([x_px / W, (x_px + width_px) / W], [y / H, y / H],
                                                          color=P["axis"], lw=0.8, transform=fig.transFigure))
    y -= 7 * dpi / 72
    for label, text, style in (("Notes", notes, "italic"), ("Source", source, "normal")):
        if not text:
            continue
        txt = wrap_to(fig, f"{label}: {text}", 8.2, width_px)
        t = fig.text(x_px / W, y / H, txt, fontsize=8.2, style=style, color=P["text_mute"], va="top", ha="left",
                     linespacing=1.3)
        y -= t.get_window_extent(renderer=r).height + gap
    return y


def finish(ax, title: str = "", subtitle: str = "", source: str = "",
           ylabel: str = "", xlabel: str = "", legend: bool | None = None,
           money: bool = False, pct: bool = False, comma: bool = True,
           pairs=None, notes: str = "") -> None:
    """
    Apply title block, axis formatting, legend rules, and the footer.

    Header (title, subtitle, fact line) is wrapped to the axes width and stacked
    upward from the top of the axes; the footer (rule, Notes, Source) sits below
    everything the axes owns, including its legend. `legend=None` auto-decides:
    shown for >=2 labelled series, hidden for one (the title already names it).
    """
    fig = ax.figure
    r = fig.canvas.get_renderer()
    bb = ax.get_window_extent(renderer=r)
    if title:
        ax.set_title("")
    header(fig, title, subtitle, pairs, x_px=bb.x0, width_px=bb.width,
           anchor_px=bb.y1 + 10 * fig.dpi / 72, anchor="bottom")

    if ylabel:
        ax.set_ylabel(ylabel, labelpad=10)
    if xlabel:
        ax.set_xlabel(xlabel, labelpad=10)

    if money:
        ax.yaxis.set_major_formatter(FuncFormatter(_money))
    elif pct:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
    elif comma:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))

    handles, labels = ax.get_legend_handles_labels()
    show = legend if legend is not None else len(labels) >= 2
    if show and labels:
        ax.legend(loc="upper left", bbox_to_anchor=(0, -0.14),
                  ncols=min(len(labels), 4))

    if notes or source:
        fig.canvas.draw()
        tb = ax.get_tightbbox(fig.canvas.get_renderer())
        footer(fig, notes, source, x_px=bb.x0, width_px=bb.width, top_px=tb.y0 - 16 * fig.dpi / 72)


ROOT = __import__("pathlib").Path(__file__).resolve().parent


def save(fig, path: str) -> str:
    """
    Write the figure and return the absolute path.

    Relative paths resolve against the project root (where theme.py lives), not
    the shell's cwd — so output lands in the same place no matter where the
    script is invoked from.
    """
    p = __import__("pathlib").Path(path)
    if not p.is_absolute():
        p = ROOT / p
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p)
    plt.close(fig)
    return str(p)


# --------------------------------------------------------------------------
# Marks
# --------------------------------------------------------------------------

MAX_BAR_PX = 24       # mark spec: bars never fill the slot
CORNER_PX = 4         # mark spec: 4px rounded data-end
MIN_BAR_FRAC = 0.40   # floor, as a share of the category slot


def bars(ax, x, heights, color=None, width: float = 0.62,
         horizontal: bool = False, max_px: float = MAX_BAR_PX,
         corner_px: float = CORNER_PX, **kw):
    """
    Bars with a rounded data-end and a SQUARE baseline, per the mark spec.

    matplotlib has no native rounded bar. A FancyBboxPatch rounds all four
    corners, which makes bars look like they float off the axis — so this
    builds an explicit path: square at the baseline, rounded only at the
    data-end.

    Thickness and corner radius are specified in pixels and converted to data
    units, so they stay constant regardless of the axis scale.
    """
    import numpy as np
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch

    color = color or P["series"][0]
    x = np.asarray(list(x), dtype=float)
    heights = np.asarray(list(heights), dtype=float)

    # establish limits first so the data<->pixel transform is meaningful
    if horizontal:
        ax.barh(x, heights, height=width, color="none", linewidth=0)
    else:
        ax.bar(x, heights, width=width, color="none", linewidth=0)
    ax.figure.canvas.draw()

    inv = ax.transData.inverted()
    o = inv.transform((0, 0))
    unit_x = abs(inv.transform((1, 0))[0] - o[0])   # data units per pixel, x
    unit_y = abs(inv.transform((0, 1))[1] - o[1])   # data units per pixel, y

    # The 24px cap keeps dense charts from filling their slots. On a low-
    # cardinality chart the slot is wide and a hard 24px cap reads spindly, so
    # floor the thickness at a share of the slot.
    thick_axis = unit_y if horizontal else unit_x
    thickness = min(width, max(max_px * thick_axis, MIN_BAR_FRAC * width))

    patches = []
    for xi, hi in zip(x, heights):
        if hi == 0:
            continue
        sign = 1.0 if hi >= 0 else -1.0
        # radius can't exceed half the bar in either direction
        r_len = min(corner_px * (unit_x if horizontal else unit_y),
                    abs(hi) / 2)
        r_thk = min(corner_px * thick_axis, thickness / 2)
        lo, hi_edge = xi - thickness / 2, xi + thickness / 2
        end = hi
        near = end - sign * r_len

        if horizontal:
            verts = [(0, lo), (near, lo), (end, lo), (end, lo + r_thk),
                     (end, hi_edge - r_thk), (end, hi_edge), (near, hi_edge),
                     (0, hi_edge), (0, lo)]
        else:
            verts = [(lo, 0), (lo, near), (lo, end), (lo + r_thk, end),
                     (hi_edge - r_thk, end), (hi_edge, end), (hi_edge, near),
                     (hi_edge, 0), (lo, 0)]
        codes = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3,
                 Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO,
                 Path.CLOSEPOLY]

        patch = PathPatch(Path(verts, codes), facecolor=color, linewidth=0, **kw)
        ax.add_patch(patch)
        patches.append(patch)

    return patches


def label_ends(ax, x, y, fmt="{:,.0f}", dy: float = 0.02, color=None):
    """
    Value labels at the mark tip. Use sparingly — the spec is to label the
    endpoint, the extreme, or the one series the story is about. Never every point.
    """
    color = color or P["text_2"]
    span = ax.get_ylim()[1] - ax.get_ylim()[0]
    for xi, yi in zip(x, y):
        ax.annotate(fmt.format(yi), (xi, yi + span * dy), ha="center",
                    va="bottom", fontsize=9.5, color=color)


def annotate(ax, text, xy, xytext, color=None):
    """A callout with a leader line, in text ink — never the series color."""
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=9.5,
                color=color or P["text_2"],
                arrowprops=dict(arrowstyle="-", color=P["axis"], linewidth=0.9,
                                shrinkA=0, shrinkB=4))


def _money(v, _=None):
    a = abs(v)
    if a >= 1e9:
        return f"${v/1e9:.1f}B"
    if a >= 1e6:
        return f"${v/1e6:.1f}M"
    if a >= 1e3:
        return f"${v/1e3:.0f}K"
    return f"${v:,.0f}"


def compact(v, _=None):
    a = abs(v)
    if a >= 1e9:
        return f"{v/1e9:.1f}B"
    if a >= 1e6:
        return f"{v/1e6:.1f}M"
    if a >= 1e3:
        return f"{v/1e3:.1f}K"
    return f"{v:,.0f}"


apply("light")
