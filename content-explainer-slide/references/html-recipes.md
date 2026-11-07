# HTML/SVG recipes (rendered to PNG)

A fixed 1600×900 px canvas laid out with CSS grid, charts as inline SVG, rendered to PNG by headless Chrome or Edge. Start from `assets/slide_template.html` (it already has the headline, 5 cards, 2×2 step cells with WHY boxes, before→after score panels, banners and the colour tokens).

## Rules specific to HTML

- **Fixed canvas:** `body { width:1600px; height:900px; overflow:hidden }`. Never responsive — this is an image, not a web page.
- **Numbers:** in source mode, keep the fact sheet as a JS object at the top of the file (`const F = {...}`) and fill every number into the page from it (`data-f="acc_after"` + a small script). Then text and facts cannot disagree.
- **Charts:** hand-written inline SVG for small charts (bars, before/after scores, change charts). Compute bar lengths from the fact values in the script, never by eye.
- **Pictures from a paper:** if the source has figures you may not reproduce, redraw the idea schematically and say so in the footnote ("redrawn from Fig. 2").
- **Fonts:** system stack (`Inter, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`) so the render needs no network. Minimum 13 px at 1600 px width.
- **Overflow check:** before screenshotting, run the template's `checkOverflow()` (it outlines in red any element whose content overflows its box) — or eyeball the render for clipped text.

## Render to PNG

Windows (Chrome or Edge):
```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu \
  --hide-scrollbars --force-device-scale-factor=1.5 --window-size=1600,900 \
  --screenshot="C:/path/slide.png" "file:///C:/path/slide.html"
```
(Edge: `"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"` with the same flags.)

Linux: `google-chrome --headless=new ...` or `chromium --headless=new ...` with the same flags.

`--force-device-scale-factor=1.5` gives a 2400×1350 PNG (sharp on LinkedIn). Then make the JPG copy:
```bash
python -c "from PIL import Image; Image.open('slide.png').convert('RGB').save('slide.jpg', quality=95)"
```

If no browser is available, say so and fall back to the matplotlib route rather than delivering an un-rendered HTML file.
