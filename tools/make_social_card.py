#!/usr/bin/env python3
"""Generate the social preview card served as og:image / twitter:image.

Without one, every share of this link -- to a legislative staffer, in a message,
on any social platform -- renders as a blank grey box. This is the card that
appears instead.

It reuses the mark's geometry from `make_favicon.py`, so the card and the favicon
cannot drift apart. Run either script after changing the mark.

Run from anywhere:

    .venv/bin/python tools/make_social_card.py

Writes `assets/social-card.png`, 1200x630, the size every major platform crops
from. Text sits inside a 100px margin so a platform cropping to 1.91:1 or to a
square never cuts a word.

The headline is the site's own h1, not a slogan written for this card. If the h1
changes, change HEADLINE and rerun -- and the assertion below fails loudly if the
headline no longer fits the box rather than rendering it clipped.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import make_favicon as mark  # same directory; shares ACCENT, PAPER and the geometry

W, H = 1200, 630
MARGIN = 100
MARK_PX = 96

# The site's own <h1>, verbatim. Not a slogan invented for the card.
HEADLINE = (
    "Massachusetts charges the most child support of any state "
    "when the parents split time equally."
)
WORDMARK = "checktheworksheet.org"
FOOTLINE = "The same two incomes and three children, run through fifty states."

# Georgia stands in for Charter, the site's first-choice serif, which is not a
# system font. Same genre: a transitional serif with a large x-height.
SERIF_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
MONO = "/System/Library/Fonts/Menlo.ttc"

ROOT = Path(__file__).resolve().parent.parent


def _wrap(draw, text, font, max_width):
    """Greedy wrap, measured with the real renderer rather than by character count."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main() -> None:
    img = Image.new("RGB", (W, H), mark.PAPER)
    d = ImageDraw.Draw(img)

    head = ImageFont.truetype(SERIF_BOLD, 54)
    foot = ImageFont.truetype(SERIF, 26)
    word = ImageFont.truetype(MONO, 30)

    # Mark and wordmark, top left.
    m = mark._draw(MARK_PX, rounded=True, simple=False).convert("RGBA")
    img.paste(m, (MARGIN, MARGIN), m)
    d.text(
        (MARGIN + MARK_PX + 24, MARGIN + MARK_PX // 2),
        WORDMARK,
        font=word,
        fill=mark.ACCENT,
        anchor="lm",
    )

    # Headline.
    box = W - 2 * MARGIN
    lines = _wrap(d, HEADLINE, head, box)
    assert len(lines) <= 4, f"headline wraps to {len(lines)} lines; it will not fit"
    y = MARGIN + MARK_PX + 70
    for ln in lines:
        d.text((MARGIN, y), ln, font=head, fill="#1A1614")
        y += 68

    # Foot line, wrapped and bottom-anchored.
    fl = _wrap(d, FOOTLINE, foot, box)
    fy = H - MARGIN - 34 * len(fl)
    assert fy > y + 20, "headline and foot line overlap; shorten one"
    for ln in fl:
        d.text((MARGIN, fy), ln, font=foot, fill="#5C5350")
        fy += 34

    # A single accent rule, the one piece of non-text ink on the card.
    d.rectangle([0, H - 12, W, H], fill=mark.ACCENT)

    out = ROOT / "assets" / "social-card.png"
    img.save(out, optimize=True)
    print(f"{out.relative_to(ROOT)}  {out.stat().st_size} bytes  {img.size}")


if __name__ == "__main__":
    main()
