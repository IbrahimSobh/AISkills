"""slide_kit — matplotlib helpers for one-image explainer slides.

All positions are FIGURE fractions (0..1, origin bottom-left), so cards can be
laid out on a 16:9 canvas without fighting axes. Charts and thumbnails go in
real axes created with `sub_axes(fig, rect)`.

Typical use:

    import sys; sys.path.insert(0, "<skill>/scripts")
    from slide_kit import *
    fig = new_slide()
    headline(fig, "36 of 128 neurons were doing nothing.", "So they got a job.")
    inner = card(fig, (0.01, 0.10, 0.20, 0.76), 1, "Which neurons are idle?",
                 "36 of 128 never fire.", data_label="18,000 training images (30%)")
    ax = sub_axes(fig, inner)   # draw a chart in the card body
    ...
    save(fig, "slide.png")      # writes slide.png and slide.jpg

Run `python slide_kit.py --demo out.png` to see every helper on one canvas.
"""
from __future__ import annotations

import textwrap
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

# Card accent colours (one per card, in story order) — separate from semantics.
ACCENTS = ["#3B6FB6", "#C0504D", "#7A5BA6", "#D08A1E", "#2E8B57", "#2A9D9F"]
# Semantic colours: keep the same meaning across the whole slide.
GOOD, BAD, NEUTRAL = "#2E8B57", "#C0392B", "#9AA0A6"
INK, MUTED, PAPER, CARD_BG = "#1F2328", "#5F6670", "#FAFAF7", "#FFFFFF"
WHY_BG = "#FFF6DB"
FONT_MIN = 7.5  # pt at 16x9 in — below this, text is unreadable on a phone


def wrap(text: str, chars: int) -> str:
    """Wrap each paragraph of `text` to `chars` characters per line."""
    return "\n".join(textwrap.fill(p, chars) if p else "" for p in text.split("\n"))


def chars_for(width_frac: float, size: float, fig_w_in: float = 16.0,
              bold: bool = False) -> int:
    """Conservative characters-per-line that fit a width (figure fraction).
    Bold glyphs are wider, so they get a larger per-character width."""
    width_pt = width_frac * fig_w_in * 72
    return max(8, int(width_pt / (size * (0.62 if bold else 0.55))))


def new_slide(w: float = 16, h: float = 9, dpi: int = 150, bg: str = PAPER):
    fig = plt.figure(figsize=(w, h), dpi=dpi, facecolor=bg)
    fig._sk_dpi = dpi
    return fig


def text(fig, x, y, s, size=9, color=INK, weight="normal", ha="left", va="top",
         width=None, **kw):
    """Place text at figure coords; if `width` (fraction) is given, auto-wrap."""
    size = max(size, FONT_MIN)
    if width:
        s = wrap(s, chars_for(width, size, fig.get_figwidth(), bold=(weight == "bold")))
    return fig.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                    ha=ha, va=va, linespacing=1.25, **kw)


def box(fig, rect, fc=CARD_BG, ec="#D0D4D9", lw=1.0, radius=0.006, z=0):
    x, y, w, h = rect
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                       transform=fig.transFigure, fc=fc, ec=ec, lw=lw, zorder=z)
    fig.add_artist(p)
    return p


def headline(fig, line1: str, line2: str = "", y: float = 0.975, size: float = 20):
    """Headline across the top. Start cards at or below 0.87 to leave room."""
    text(fig, 0.5, y, line1, size=size, weight="bold", ha="center")
    if line2:
        text(fig, 0.5, y - 0.048, line2, size=size * 0.75, color=MUTED, ha="center")


def card(fig, rect, num: int, title: str, takeaway: str, accent: str | None = None,
         data_label: str | None = None, footnote: str | None = None):
    """Draw a numbered card. Returns the free body rect (x, y, w, h) for the figure."""
    x, y, w, h = rect
    accent = accent or ACCENTS[(num - 1) % len(ACCENTS)]
    box(fig, rect, ec=accent, lw=1.6)
    # number badge + title
    fig.add_artist(FancyBboxPatch((x + 0.006, y + h - 0.052), 0.026, 0.042,
                                  boxstyle="round,pad=0,rounding_size=0.006",
                                  transform=fig.transFigure, fc=accent, ec="none"))
    text(fig, x + 0.019, y + h - 0.031, str(num), size=15, color="white",
         weight="bold", ha="center", va="center")
    t = text(fig, x + 0.038, y + h - 0.012, title, size=10.5, weight="bold",
             color=accent, width=w - 0.045)
    n_title = t.get_text().count("\n") + 1
    top = min(y + h - 0.012 - 0.024 * n_title - 0.006, y + h - 0.060)  # clear the badge
    k = text(fig, x + 0.008, top, takeaway, size=9.5, weight="bold", width=w - 0.016)
    top -= 0.022 * (k.get_text().count("\n") + 1) + 0.004
    if data_label:
        d = text(fig, x + 0.008, top, "Data: " + data_label, size=7.8, color=MUTED,
                 style="italic", width=w - 0.016)
        top -= 0.018 * (d.get_text().count("\n") + 1) + 0.006
    bottom = y + 0.008
    if footnote:
        f = text(fig, x + 0.008, y + 0.008, footnote, size=7.6, color=MUTED,
                 va="bottom", width=w - 0.016)
        bottom += 0.017 * (f.get_text().count("\n") + 1) + 0.006
    return (x + 0.008, bottom, w - 0.016, top - bottom)


def why_box(fig, rect, why: str, size: float = 8.0):
    """Tinted, labelled WHY box — reasoning lives here, never in a footnote."""
    x, y, w, h = rect
    box(fig, rect, fc=WHY_BG, ec="#E8C766", lw=0.8, radius=0.004)
    text(fig, x + 0.005, y + h - 0.006, "WHY? ", size=size, weight="bold",
         color="#9A6B00")
    text(fig, x + 0.036, y + h - 0.006, why, size=size, width=w - 0.042)


def step_cell(fig, rect, num: int, what: str, why: str | None, accent: str,
              why_h: float = 0.075, what_size: float = 8.6):
    """Method step: caption (WHAT) on top, picture band, WHY box at the bottom.
    Returns the picture rect."""
    x, y, w, h = rect
    box(fig, rect, fc="#FBFCFD", ec=accent, lw=0.9, radius=0.005)
    text(fig, x + 0.006, y + h - 0.006, f"{num}", size=11, weight="bold", color=accent)
    c = text(fig, x + 0.022, y + h - 0.007, what, size=what_size, weight="bold",
             width=w - 0.028)
    cap_h = 0.020 * (c.get_text().count("\n") + 1) + 0.010
    pic_bottom = y + 0.005
    if why:
        why_box(fig, (x + 0.004, y + 0.004, w - 0.008, why_h), why)
        pic_bottom = y + why_h + 0.010
    return (x + 0.006, pic_bottom, w - 0.012, (y + h - cap_h) - pic_bottom)


def sub_axes(fig, rect, off: bool = False):
    ax = fig.add_axes(rect)
    ax.set_facecolor("none")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=FONT_MIN)
    if off:
        ax.axis("off")
    return ax


def thumbs(fig, rect, images: Sequence, cmap="gray_r", labels: Sequence[str] | None = None,
           gap: float = 0.004):
    """A row of image thumbnails filling `rect`."""
    x, y, w, h = rect
    n = len(images)
    tw = (w - gap * (n - 1)) / n
    axes = []
    for i, img in enumerate(images):
        ax = fig.add_axes((x + i * (tw + gap), y, tw, h))
        ax.imshow(img, cmap=cmap, aspect="auto" if cmap != "gray_r" else "equal")
        ax.set_xticks([]); ax.set_yticks([])
        if labels:
            ax.set_title(labels[i], fontsize=FONT_MIN, pad=2)
        axes.append(ax)
    return axes


def mini_scores(fig, rect, scores: dict, title: str = "", correct: str | None = None,
                side: bool = False):
    """Small horizontal score bars; the top score is marked ✓ (correct) or ✗.
    `side=True` puts the title to the right instead of below (saves height)."""
    x, y, w, h = rect
    bw = w * (0.62 if side else 1.0)
    lab_h = 0 if side else 0.040  # room for the two-line label under the bars
    ax = fig.add_axes((x, y + lab_h, bw, h - lab_h))
    names = list(scores)[::-1]
    vals = [scores[k] for k in names]
    win = max(scores, key=scores.get)
    cols = [(GOOD if win == correct else BAD) if k == win else NEUTRAL for k in names]
    ax.barh(names, vals, color=cols, height=0.65)
    ax.set_xticks([]); ax.tick_params(labelsize=FONT_MIN, length=0)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    mark = "✓" if win == correct else "✗"
    label = f"{title}\npredicts {win} {mark}" if title else f"predicts {win} {mark}"
    col = GOOD if win == correct else BAD
    if side:
        text(fig, x + bw + 0.006, y + h / 2, label, size=8, color=col, weight="bold",
             va="center")
    else:
        text(fig, x + w / 2, y + lab_h - 0.004, label, size=8, color=col, weight="bold",
             ha="center", va="top")
    return ax


def arrow(fig, start, end, note: str | None = None, color=MUTED):
    fig.add_artist(FancyArrowPatch(start, end, transform=fig.transFigure,
                                   arrowstyle="-|>", mutation_scale=14, color=color, lw=1.4))
    if note:
        span = abs(end[0] - start[0]) + 0.01
        text(fig, (start[0] + end[0]) / 2, max(start[1], end[1]) + 0.010, note,
             size=7.6, color=MUTED, ha="center", va="bottom", width=span,
             multialignment="center")


def legend(fig, x, y, items: Iterable[tuple[str, str]], size=7.8, step=0.018):
    """Vertical legend: items = [(colour, label), ...]."""
    for i, (c, lab) in enumerate(items):
        yy = y - i * step
        box(fig, (x, yy - 0.010, 0.010, 0.010), fc=c, ec="none", radius=0.001)
        text(fig, x + 0.014, yy, lab, size=size, color=INK)


def group_box(fig, rect, accent):
    """White box with an accent edge to separate a group of items."""
    return box(fig, rect, fc="white", ec=accent, lw=1.0, radius=0.004)


def banner(fig, rect, msg: str, kind: str = "conclusion", size: float = 10):
    fc, ec = (("#E6F4EA", GOOD) if kind == "conclusion" else ("#EEF1F6", "#3B6FB6"))
    box(fig, rect, fc=fc, ec=ec, lw=1.2)
    x, y, w, h = rect
    prefix = "Conclusion: " if kind == "conclusion" else "Lesson: "
    text(fig, x + w / 2, y + h / 2, prefix + msg, size=size, weight="bold",
         ha="center", va="center", width=w - 0.02, multialignment="center")


def save(fig, path: str, jpg: bool = True, quality: int = 95):
    """Save PNG and (optionally) a transparency-free JPG copy for social media."""
    fig.savefig(path, dpi=getattr(fig, "_sk_dpi", 150), facecolor=fig.get_facecolor())
    out = [path]
    if jpg:
        from PIL import Image
        j = path.rsplit(".", 1)[0] + ".jpg"
        Image.open(path).convert("RGB").save(j, quality=quality)
        out.append(j)
    plt.close(fig)
    return out


def _demo(path):
    import numpy as np
    rng = np.random.default_rng(0)
    fig = new_slide()
    headline(fig, "Demo headline: a surprising fact.", "So we did something about it.")
    b1 = card(fig, (0.010, 0.17, 0.22, 0.70), 1, "What did we notice?",
              "36 of 128 units never activate.", data_label="18,000 images (30%), why: fair test",
              footnote="Footnote: caveats only.")
    ax = sub_axes(fig, (b1[0] + 0.02, b1[1] + 0.07, b1[2] - 0.03, b1[3] - 0.10))
    v = np.sort(rng.random(128))[::-1]; v[-36:] = 0.01
    ax.bar(range(128), v, color=[NEUTRAL] * 92 + [BAD] * 36, width=1)
    legend(fig, b1[0] + 0.01, b1[1] + 0.04, [(NEUTRAL, "active"), (BAD, "idle (0%)")])
    b3 = card(fig, (0.240, 0.17, 0.50, 0.70), 3, "How does one fix work?",
              "Four steps, each with its reason.", accent=ACCENTS[2],
              footnote="Example: shown for one case. Same recipe for all 30.")
    cw, ch = b3[2] / 2 - 0.004, b3[3] / 2 - 0.004
    for i in range(4):
        cx = b3[0] + (i % 2) * (cw + 0.008)
        cy = b3[1] + (1 - i // 2) * (ch + 0.008)
        pic = step_cell(fig, (cx, cy, cw, ch), i + 1, f"WHAT: step {i+1} compares A with B",
                        "Because the reason sits next to the step, readers never have to ask.",
                        ACCENTS[2])
        if i == 3:
            pw = pic[2] * 0.34
            mini_scores(fig, (pic[0] + 0.01, pic[1], pw, pic[3] - 0.005),
                        {"3": 0.7, "8": 0.5, "5": 0.1}, "before", correct="8")
            arrow(fig, (pic[0] + pic[2] * 0.42, pic[1] + pic[3] / 2),
                  (pic[0] + pic[2] * 0.58, pic[1] + pic[3] / 2), "8, the 2nd-highest, wins")
            mini_scores(fig, (pic[0] + pic[2] * 0.64, pic[1], pw, pic[3] - 0.005),
                        {"3": 0.3, "8": 0.5, "5": 0.1}, "after", correct="8")
        else:
            thumbs(fig, pic, [rng.random((8, 8)) for _ in range(4)])
    b5 = card(fig, (0.750, 0.17, 0.24, 0.70), 5, "Did it work on new data?",
              "96.74% → 96.99% (34 fixed, 9 broken).", data_label="10,000 test images, never used")
    ax = sub_axes(fig, (b5[0] + 0.02, b5[1] + 0.02, b5[2] - 0.03, b5[3] - 0.05))
    d = [2, -1, 0, -2, 1, -1, 0, 3, 4, -1]
    ax.bar(range(10), d, color=[GOOD if x > 0 else BAD if x < 0 else NEUTRAL for x in d])
    ax.set_xticks(range(10))
    banner(fig, (0.010, 0.085, 0.98, 0.065), "the fix works on new data; small but real gain.")
    banner(fig, (0.010, 0.012, 0.98, 0.060), "edits remove obstacles; new skills need training.",
           kind="lesson")
    return save(fig, path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "--demo":
        print(_demo(sys.argv[2]))
    else:
        print(__doc__)
