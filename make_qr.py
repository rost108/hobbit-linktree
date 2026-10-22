"""Брендовий QR для лінк трі Hobbit House → qr-brand.svg (+ PNG через headless Chrome)."""
import re
import subprocess
import pathlib
import segno

URL = "https://hobbit-house.netlify.app/?utm_source=qr&utm_medium=print&utm_campaign=linktree"
HERE = pathlib.Path(__file__).parent
INK, BG, YELLOW, STEEL = "#16181A", "#F6F5F2", "#FCDE00", "#84969A"

# Шляхи логотипа беремо з index.html (джерело — design_extract/.../logo-mark.svg)
html = (HERE / "index.html").read_text(encoding="utf-8")
arch = re.search(r'class="mark-y" d="([^"]+)"', html).group(1)
mono, wordmark = re.findall(r'class="mark-s"(?: fill-rule="evenodd" clip-rule="evenodd")? d="([^"]+)"', html)[:2]

q = segno.make(URL, error="h")
m = [[bool(v) for v in row] for row in q.matrix]
n = len(m)

CELL = 24
GAP = CELL * 0.03          # зазор між модулями (більший ламає суворі декодери)
QUIET = 2                      # модулі поля навколо (решту дає картка)
PAD = 70                       # поля картки, px
qr_px = (n + QUIET * 2) * CELL
W = qr_px + PAD * 2
H = W + 230                    # місце під вордмарк і підпис
ox = oy = PAD + QUIET * CELL   # початок матриці

# Зона під логотип у центрі (непарна кількість модулів)
plate = round(n * 0.24)
if plate % 2 != n % 2:
    plate += 1
c0 = (n - plate) // 2
def in_plate(r, c):
    return c0 <= r < c0 + plate and c0 <= c < c0 + plate

def in_finder(r, c):
    return (r < 7 and c < 7) or (r < 7 and c >= n - 7) or (r >= n - 7 and c < 7)

parts = []
for r in range(n):
    for c in range(n):
        if m[r][c] and not in_finder(r, c) and not in_plate(r, c):
            x, y = ox + c * CELL, oy + r * CELL
            parts.append(f'<rect x="{x+GAP:.2f}" y="{y+GAP:.2f}" width="{CELL-2*GAP:.2f}" height="{CELL-2*GAP:.2f}" rx="{CELL*0.3:.1f}"/>')

def finder(r, c):
    x, y = ox + c * CELL, oy + r * CELL
    s = 7 * CELL
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{CELL*1.2}" fill="{INK}"/>'
            f'<rect x="{x+CELL}" y="{y+CELL}" width="{s-2*CELL}" height="{s-2*CELL}" rx="{CELL*0.4}" fill="{BG}"/>'
            f'<rect x="{x+2*CELL}" y="{y+2*CELL}" width="{3*CELL}" height="{3*CELL}" rx="{CELL*0.6}" fill="{INK}"/>')

finders = finder(0, 0) + finder(0, n - 7) + finder(n - 7, 0)

# Плита з логотипом
px, py = ox + c0 * CELL, oy + c0 * CELL
ps = plate * CELL
mark_w = ps * 0.72
scale = mark_w / 79
mark_h = 56 * scale
mx, my = px + (ps - mark_w) / 2, py + (ps - mark_h) / 2 + 4
logo = (f'<rect x="{px+4}" y="{py+4}" width="{ps-8}" height="{ps-8}" rx="{CELL*1.2}" fill="#FFFFFF"/>'
        f'<g transform="translate({mx:.1f} {my:.1f}) scale({scale:.4f})">'
        f'<path d="{arch}" fill="{YELLOW}"/><path fill-rule="evenodd" d="{mono}" fill="{STEEL}"/></g>')

# Вордмарк під кодом (вектор з лого, без залежності від шрифтів)
wm_scale = 5.6
wm_w = 79 * wm_scale
wm_x = (W - wm_w) / 2
wm_y = PAD + qr_px + 26 - 61 * wm_scale
wordmark_svg = (f'<g transform="translate({wm_x:.1f} {wm_y:.1f}) scale({wm_scale})">'
                f'<path d="{wordmark}" fill="{INK}"/></g>')
line_y = PAD + qr_px + 26 + 12.5 * wm_scale + 22
caption_y = line_y + 52

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}">
<style>@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&amp;display=swap');</style>
<rect width="{W}" height="{H:.0f}" rx="48" fill="{BG}"/>
<g fill="{INK}">{"".join(parts)}</g>
{finders}
{logo}
{wordmark_svg}
<rect x="{W/2-60}" y="{line_y:.0f}" width="120" height="8" rx="4" fill="{YELLOW}"/>
<text x="{W/2}" y="{caption_y:.0f}" text-anchor="middle" font-family="IBM Plex Mono, Menlo, monospace" font-weight="500"
 font-size="30" letter-spacing="4" fill="#5C6468">ВАША БЕЗПЕКА — ЦЕ НАША РОБОТА</text>
</svg>'''

svg_path = HERE / "qr-brand.svg"
svg_path.write_text(svg, encoding="utf-8")

# PNG 2× через headless Chrome
wrap = HERE / "_qr_render.html"
wrap.write_text(f'<!doctype html><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}'
                f'svg{{display:block}}</style>{svg}', encoding="utf-8")
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                "--default-background-color=00000000", f"--window-size={W},{int(H)}", "--virtual-time-budget=4000",
                f"--screenshot={HERE / 'qr-brand.png'}", wrap.as_uri()], check=True, capture_output=True)
wrap.unlink()
print(f"modules={n} version={q.version} -> {svg_path.name}, qr-brand.png ({W}x{int(H)} @2x)")
