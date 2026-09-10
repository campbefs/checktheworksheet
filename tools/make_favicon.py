#!/usr/bin/env python3
"""Generate the site favicon set.

The mark is a checkmark on the site's one accent colour, which is the site's
name ("Check the Worksheet") and nothing more. Single-accent discipline, per
the design system: --accent #7A1330 on --surface #FBF3EA.

Run from anywhere:

    .venv/bin/python tools/make_favicon.py

Writes, relative to the repo root:

    favicon.ico              16/32/48, what a browser requests by default
    assets/favicon.svg       scalable, preferred by modern browsers
    assets/favicon-32.png    explicit 32 for browsers that skip the SVG
    assets/apple-touch-icon.png   180, iOS home screen (opaque, no rounding —
                                  iOS applies its own mask)

The PNGs are drawn at 8x and downsampled, because PIL has no antialiased
polygon fill. The SVG is hand-written to the same geometry, so the two marks
are the same drawing at different resolutions rather than a conversion.
"""

from pathlib import Path

from PIL import Image, ImageDraw

ACCENT = "#7A1330"  # --accent
PAPER = "#FBF3EA"  # --surface

# Geometry, in fractions of the icon box. Shared by the PNG and the SVG so the
# two cannot drift.
CORNER_R = 0.18
CHECK = [(0.245, 0.525), (0.425, 0.700), (0.760, 0.320)]
CHECK_W = 0.125

ROOT = Path(__file__).resolve().parent.parent
SUPERSAMPLE = 8


def _draw(size: int, rounded: bool) -> Image.Image:
    s = size * SUPERSAMPLE
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if rounded:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(CORNER_R * s), fill=ACCENT)
    else:
        d.rectangle([0, 0, s - 1, s - 1], fill=ACCENT)

    pts = [(x * s, y * s) for x, y in CHECK]
    d.line(pts, fill=PAPER, width=int(CHECK_W * s), joint="curve")
    # `joint="curve"` rounds the elbow but leaves the two ends square; caps the
    # stroke by hand so the mark reads as one drawn stroke at 16px.
    r = CHECK_W * s / 2
    for x, y in (pts[0], pts[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=PAPER)

    return img.resize((size, size), Image.LANCZOS)


def _svg() -> str:
    d = "M {:.4g} {:.4g} L {:.4g} {:.4g} L {:.4g} {:.4g}".format(
        *[c for pt in CHECK for c in pt]
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1" '
        'width="64" height="64" role="img" aria-label="Check the Worksheet">\n'
        f'  <rect width="1" height="1" rx="{CORNER_R}" fill="{ACCENT}"/>\n'
        f'  <path d="{d}" fill="none" stroke="{PAPER}" stroke-width="{CHECK_W}" '
        'stroke-linecap="round" stroke-linejoin="round"/>\n'
        "</svg>\n"
    )


def main() -> None:
    written = []

    ico = ROOT / "favicon.ico"
    _draw(48, rounded=True).save(ico, sizes=[(16, 16), (32, 32), (48, 48)])
    written.append(ico)

    png32 = ROOT / "assets" / "favicon-32.png"
    _draw(32, rounded=True).save(png32)
    written.append(png32)

    touch = ROOT / "assets" / "apple-touch-icon.png"
    _draw(180, rounded=False).convert("RGB").save(touch)
    written.append(touch)

    svg = ROOT / "assets" / "favicon.svg"
    svg.write_text(_svg())
    written.append(svg)

    for p in written:
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size} bytes")


if __name__ == "__main__":
    main()
