"""Embed a browser-tab icon (favicon) and a phone home-screen icon in a course page.

usage: python -I favicon.py <index.html> [emoji] [--font <emoji font file>] [--preview <out.png>]
The emoji defaults to the one in the page's <div class="brand"> (e.g. 🎲). It is drawn in colour, cropped,
centred on a transparent square, and embedded as two PNG data URIs right after <title>: a 32x32 icon and a
180x180 apple-touch-icon. The page stays one self-contained file. Re-running replaces the old icons.
Fonts: Segoe UI Emoji on Windows by default; elsewhere pass --font (e.g. NotoColorEmoji.ttf).
"""
import base64, io, re, sys
from PIL import Image, ImageDraw, ImageFont

args = sys.argv[1:]
opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or not args[i - 1].startswith("--"))]
path = pos[0]
html = open(path, encoding="utf-8", newline="").read()
emoji = pos[1] if len(pos) > 1 else None
if not emoji:
    m = re.search(r'<div class="brand">\s*(\S+)', html)
    if not m:
        sys.exit("no emoji given and no <div class=\"brand\"> found")
    emoji = m.group(1)
font = ImageFont.truetype(opt("--font", "C:/Windows/Fonts/seguiemj.ttf"), 400)


def render(size):
    big = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    bb = d.textbbox((0, 0), emoji, font=font, embedded_color=True)
    d.text(((512 - (bb[2] - bb[0])) / 2 - bb[0], (512 - (bb[3] - bb[1])) / 2 - bb[1]), emoji, font=font, embedded_color=True)
    box = big.getbbox()
    if not box:
        sys.exit(f"the font drew nothing for {emoji!r}; pass --font with a colour emoji font")
    im = big.crop(box)
    side = max(im.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    return sq.resize((size, size), Image.LANCZOS)


def data_uri(im):
    b = io.BytesIO()
    im.save(b, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


i32, i180 = render(32), render(180)
links = (f'<link rel="icon" type="image/png" sizes="32x32" href="{data_uri(i32)}">\n'
         f'<link rel="apple-touch-icon" sizes="180x180" href="{data_uri(i180)}">\n')
html = re.sub(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>\n', "", html)
m = re.search(r"</title>\n", html)
if not m:
    sys.exit("no </title> found")
html = html[:m.end()] + links + html[m.end():]
open(path, "w", encoding="utf-8", newline="").write(html)
if opt("--preview"):
    i180.save(opt("--preview"))
code = " ".join(f"U+{ord(ch):04X}" for ch in emoji)   # the Windows console can't always print emoji
print(f"{path}: icon {code} embedded (32px + 180px, {len(links) // 1024} KB)")
