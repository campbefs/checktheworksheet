#!/usr/bin/env python3
"""Generate the site favicon set.

The mark is a worksheet checkbox with a heart in it and three form rows beside
it: the thing being checked, and what it is about. Single-accent discipline,
per the design system: --accent #7A1330 on --surface #FBF3EA.

**Two tiers, and this is the point of the file.** At 16 pixels the box outline,
the heart and the rows merge into a smear -- measured, not assumed, on
2026-09-11. So the detailed mark is used at 32 and above, and a simplified one
(bigger box, heart only, no rows) is used at 16. Both are drawn from the
constants below, so they cannot drift apart.

Run from anywhere:

    .venv/bin/python tools/make_favicon.py

Writes, relative to the repo root:

    favicon.ico              16 (simple) + 32/48 (detailed), what a browser
                             requests by default
    assets/favicon.svg       scalable, preferred by modern browsers
    assets/favicon-32.png    explicit 32 for browsers that skip the SVG
    assets/apple-touch-icon.png   180, iOS home screen (opaque, no rounding --
                                  iOS applies its own mask)

The PNGs are drawn at 8x and downsampled, because PIL has no antialiased
polygon fill. The SVG is written from the same constants, so the two marks are
one drawing at different resolutions rather than a conversion.

The previous checkmark-only generator is kept beside this one as
`make_favicon.pre-logo-2026-09-11.py`.
"""

from pathlib import Path

from PIL import Image, ImageDraw

ACCENT = "#7A1330"  # --accent
PAPER = "#FBF3EA"  # --surface

# Geometry in a 0-100 box, shared by every renderer below.
CORNER_R = 18.0

# --- detailed mark, used at 32 and above -------------------------------------
BOX = (19.0, 31.0, 37.0, 37.0)  # x, y, w, h
BOX_R = 6.5
STROKE = 7.0
HEART = (37.5, 48.0, 23.0)  # cx, cy, width
ROWS = [(64.0, 35.5, 20.0), (64.0, 48.5, 26.0), (64.0, 61.5, 14.0)]  # x, y, w
ROW_H = 7.0

# --- simplified mark, used at 16 ---------------------------------------------
# At 16 pixels a box AND a heart is one shape too many: the box outline eats
# four of the sixteen rows and the heart inside it turns to porridge. Measured
# 2026-09-11. So the small mark is the heart alone, filled, at the size the box
# would have been -- one shape, full contrast, unmistakable at a tab's size.
HEART_S = (50.0, 50.0, 58.0)

# A heart drawn in a 6..94 x 10..88 box, scaled and centred on demand. Cubic
# segments as (control1, control2, end); the start point is the one before it.
_HEART_START = (50.0, 88.0)
_HEART_CURVES = [
    ((20, 66), (6, 50), (6, 34)),
    ((6, 20), (17, 10), (30, 10)),
    ((39, 10), (46, 15), (50, 22)),
    ((54, 15), (61, 10), (70, 10)),
    ((83, 10), (94, 20), (94, 34)),
    ((94, 50), (80, 66), (50, 88)),
]
_HEART_W = 88.0  # x extent of the raw path
_HEART_CX, _HEART_CY = 50.0, 49.0

ROOT = Path(__file__).resolve().parent.parent
SUPERSAMPLE = 8
FLATTEN = 24  # segments per cubic; 24 is smooth past 512px


def _heart_points(cx: float, cy: float, w: float) -> list[tuple[float, float]]:
    """The heart as a flat polygon, so PIL can fill it."""
    s = w / _HEART_W

    def m(p):
        return (cx + (p[0] - _HEART_CX) * s, cy + (p[1] - _HEART_CY) * s)

    pts = [m(_HEART_START)]
    cur = _HEART_START
    for c1, c2, end in _HEART_CURVES:
        for i in range(1, FLATTEN + 1):
            t = i / FLATTEN
            u = 1 - t
            x = (
                u**3 * cur[0]
                + 3 * u**2 * t * c1[0]
                + 3 * u * t**2 * c2[0]
                + t**3 * end[0]
            )
            y = (
                u**3 * cur[1]
                + 3 * u**2 * t * c1[1]
                + 3 * u * t**2 * c2[1]
                + t**3 * end[1]
            )
            pts.append(m((x, y)))
        cur = end
    return pts


def _heart_path(cx: float, cy: float, w: float) -> str:
    """The same heart as an SVG path, from the same constants."""
    s = w / _HEART_W

    def m(p):
        return f"{cx + (p[0] - _HEART_CX) * s:.4g} {cy + (p[1] - _HEART_CY) * s:.4g}"

    out = [f"M {m(_HEART_START)}"]
    for c1, c2, end in _HEART_CURVES:
        out.append(f"C {m(c1)} {m(c2)} {m(end)}")
    out.append("Z")
    return " ".join(out)


def _draw(size: int, rounded: bool, simple: bool) -> Image.Image:
    s = size * SUPERSAMPLE
    k = s / 100.0  # one unit of the 0-100 box, in supersampled pixels
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if rounded:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(CORNER_R * k), fill=ACCENT)
    else:
        d.rectangle([0, 0, s - 1, s - 1], fill=ACCENT)

    if simple:
        d.polygon([(px * k, py * k) for px, py in _heart_points(*HEART_S)], fill=PAPER)
        return img.resize((size, size), Image.LANCZOS)

    box, box_r, stroke, heart = BOX, BOX_R, STROKE, HEART

    # PIL strokes a rectangle INWARD from its bounding box; SVG straddles the
    # path, half in and half out. Expanding by half the stroke makes the two
    # agree, so the box interior is the same width in both and the heart is not
    # squeezed by a full stroke on each side.
    x, y, w, h = box
    half = stroke / 2.0
    d.rounded_rectangle(
        [(x - half) * k, (y - half) * k, (x + w + half) * k, (y + h + half) * k],
        radius=(box_r + half) * k,
        outline=PAPER,
        width=max(1, round(stroke * k)),
    )

    d.polygon(
        [(px * k, py * k) for px, py in _heart_points(*heart)],
        fill=PAPER,
    )

    for rx, ry, rw in ROWS:
        d.rounded_rectangle(
            [rx * k, ry * k, (rx + rw) * k, (ry + ROW_H) * k],
            radius=ROW_H * k / 2,
            fill=PAPER,
        )

    return img.resize((size, size), Image.LANCZOS)


def _svg() -> str:
    x, y, w, h = BOX
    rows = "\n".join(
        f'  <rect x="{rx:.4g}" y="{ry:.4g}" width="{rw:.4g}" height="{ROW_H:.4g}" '
        f'rx="{ROW_H / 2:.4g}" fill="{PAPER}"/>'
        for rx, ry, rw in ROWS
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
        'width="64" height="64" role="img" aria-label="Check the Worksheet">\n'
        f'  <rect width="100" height="100" rx="{CORNER_R:.4g}" fill="{ACCENT}"/>\n'
        f'  <rect x="{x:.4g}" y="{y:.4g}" width="{w:.4g}" height="{h:.4g}" '
        f'rx="{BOX_R:.4g}" fill="none" stroke="{PAPER}" stroke-width="{STROKE:.4g}"/>\n'
        f'  <path d="{_heart_path(*HEART)}" fill="{PAPER}"/>\n'
        f"{rows}\n"
        "</svg>\n"
    )


def main() -> None:
    written = []

    # The .ico carries the simple mark at 16 and the detailed one at 32/48.
    # Pillow matches `append_images` to `sizes` by the image's own size, so each
    # entry must be drawn at its final size -- passing one image and letting
    # Pillow resize it would put the detailed mark in the 16px slot, where it is
    # unreadable. Asserted below, because a silently dropped size looks fine.
    ico = ROOT / "favicon.ico"
    ico_imgs = {
        16: _draw(16, rounded=True, simple=True),
        32: _draw(32, rounded=True, simple=False),
        48: _draw(48, rounded=True, simple=False),
    }
    ico_imgs[48].save(
        ico,
        sizes=[(16, 16), (32, 32), (48, 48)],
        append_images=[ico_imgs[16], ico_imgs[32]],
    )
    with Image.open(ico) as check:
        got = sorted(check.ico.sizes())
    assert got == [(16, 16), (32, 32), (48, 48)], f"favicon.ico holds {got}"
    written.append(ico)

    png32 = ROOT / "assets" / "favicon-32.png"
    _draw(32, rounded=True, simple=False).save(png32)
    written.append(png32)

    png16 = ROOT / "assets" / "favicon-16.png"
    _draw(16, rounded=True, simple=True).save(png16)
    written.append(png16)

    touch = ROOT / "assets" / "apple-touch-icon.png"
    _draw(180, rounded=False, simple=False).convert("RGB").save(touch)
    written.append(touch)

    svg = ROOT / "assets" / "favicon.svg"
    svg.write_text(_svg())
    written.append(svg)

    for p in written:
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size} bytes")


if __name__ == "__main__":
    main()
