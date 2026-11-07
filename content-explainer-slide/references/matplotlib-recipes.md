# matplotlib recipes (PNG output)

Use `scripts/slide_kit.py`; run `python scripts/slide_kit.py --demo out.png` once to see every helper. Needs `matplotlib`, `numpy`, `Pillow`.

## Script shape (data mode)

```python
import sys; sys.path.insert(0, r"<skill-dir>/scripts")
from slide_kit import *

# 1. LOAD real artefacts and COMPUTE every number (no literals in slide text)
before_acc, after_acc = evaluate(model_a, test), evaluate(model_b, test)
n_fixed, n_broken = ...

# 2. DRAW
fig = new_slide()                                   # 16x9 in, 150 dpi
headline(fig, f"{n_idle} of {n_total} neurons were doing nothing.", "So they got a job.")
body = card(fig, (x, y, w, h), 1, "Question?", f"Answer with {n_idle}.",
            data_label="which data, and why that data", footnote="caveat only")
ax = sub_axes(fig, body)                            # chart inside the card body
...
save(fig, "slide.png")                              # + slide.jpg
```

Print the key numbers to stdout as well, so the run log doubles as a check against the fact sheet.

## Layout grid that works for 5 cards

Figure fractions, headline above 0.87, two banners at the bottom:

| card | x | width | note |
|---|---|---|---|
| 1 discovery | 0.008 | 0.15 | one small chart |
| 2 problem | 0.164 | 0.17 | chart + problem→fix list |
| 3 method | 0.340 | 0.30 | 2×2 step cells — widest |
| 4 counts | 0.646 | 0.17 | bar chart + example box |
| 5 result | 0.822 | 0.17 | stats + change chart + "why" panel |

Cards: `y=0.17, h=0.69`. Banners: conclusion `(0.008, 0.088, 0.984, 0.068)`, lesson `(0.008, 0.012, 0.984, 0.066)`. Adjust widths to content; with 3–4 cards, widen the method card. Put the conclusion banner inside the result card instead if the bottom gets crowded.

## Step cells (2×2)

```python
cw, ch = body[2]/2 - 0.004, body[3]/2 - 0.004
for i, (what, why) in enumerate(steps):
    cx = body[0] + (i % 2) * (cw + 0.008)
    cy = body[1] + (1 - i // 2) * (ch + 0.008)
    pic = step_cell(fig, (cx, cy, cw, ch), i + 1, what, why, ACCENTS[2], why_h=0.075)
    # draw the real-data picture inside `pic`
```

Size `why_h` to the longest WHY text (≈0.018 per wrapped line + 0.012). Keep the same `why_h` for every cell so the grid looks even.

## Pictures that explain

- **Real examples:** `thumbs(fig, pic_rect, images)` — real inputs, 4–6 of them, plus a text "… N in total".
- **Difference / pattern images:** `imshow(diff, cmap="coolwarm", vmin=-m, vmax=m)` with a legend "red = only in X, blue = only in Y".
- **Mechanism before → after:** two `mini_scores(...)` panels with `arrow(..., note="the 2nd-highest wins")` between them. Use `side=True` only when the cell is wide and short.
- **Groups:** `group_box(fig, rect, accent)` around each group (e.g. each style of one mistake), with one averaged thumbnail per group.
- **Change chart:** bars of after − before per item, coloured `GOOD`/`BAD`/`NEUTRAL`, zero line visible, value labels on bars.
- **Source distinction:** same colour, dark vs. light (alpha 0.45) for e.g. labelled vs. mined; add a legend.

## Gotchas

- `fig.text` does not wrap — always pass `width=` to `text(...)` (it wraps by estimated characters) and re-check in the render.
- Glyphs ✓ ✗ → − render in DejaVu Sans (matplotlib default); avoid emoji (they render as boxes).
- Thumbnails with `aspect="equal"` may not fill their rect; that is fine, but check the gap does not look like an empty area.
- After every render, crop each card with Pillow (`Image.open(p).crop(box)`) and look at it — overlaps are invisible at full-slide zoom.
- `save()` writes a JPG from the PNG for LinkedIn (no transparency).
