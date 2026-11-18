#!/usr/bin/env python3
"""README の上に出している assets/header.svg を作る。

使い方:
    pip install fonttools pillow
    python3 .github/scripts/make-header.py <DelaGothicOne-Regular.ttf の場所> <DotGothic16-Regular.ttf の場所>

見た目は https://www.nemdull.com/ に合わせている。人の声（ベタ塗りの色面と大きな見出し）と、
機械の声（ドットの電光掲示板と、文字でできた星）の 2 つでできている。

書体は Dela Gothic One と DotGothic16（どちらも SIL Open Font License 1.1）。GitHub の README では
Web フォントを読み込めないので、文字は輪郭（パス）か点にして埋め込んでいる。
書体は https://github.com/google/fonts の ofl/delagothicone と ofl/dotgothic16 にある。
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[2] / "assets" / "header.svg"
WIDTH, HEIGHT = 1200, 440

# 色は nemdull.com と同じ
NIGHT, NAVY, MOON, LEMON, LAVENDER = "#1b2fd6", "#0a0f3c", "#f3f2ec", "#ffd91a", "#c4b5ff"
GO, AMBER, UNLIT = "#3ee08f", "#ffb224", "#19226b"

# (文字列, 文字の大きさ, 左端 x, ベースライン y, 眠そうに垂れるか)
LINES = [
    ("ねむい。", 132, 64, 142, True),
    ("だるい。", 132, 64, 278, True),
    ("だから自動化する。", 58, 68, 348, False),
]

# 眠そうに傾く角度（度）と、ずり落ちる量（書体の単位）。行ごと・文字ごとに少しずつ違える
DROOP = [
    [(-3, 0), (5, 40), (10, 90), (16, 160)],
    [(-6, 30), (7, 80), (14, 150), (22, 250)],
]

# 「。」は字の形を使わず、輪で描く。大きさは文字の大きさに対する割合
MARU_SIZE, MARU_STROKE, MARU_GAP, MARU_SINK = 0.272, 0.067, 0.03, 0.035

# 右上の黄色い円（サイトでは、最後の「。」の明かりから広がる自己紹介の部屋）
PORTAL = (1040, 150, 205)

# 下の電光掲示板。1 文字は 16 × 16 の点
SEAM_TOP, BAND_TOP = 372, 384
LED_ROWS, LED_PITCH, LED_DOT = 16, 3.5, 2.5
LED_TEXT = [
    ("nemdull.com", GO),
    ("　", None),
    ("テストを書いて、機械に任せる。", AMBER),
    ("　　", None),
]
LED_DOTS_PER_SECOND = 30


def outline(font: TTFont, char: str) -> tuple[str, float]:
    """1 文字の輪郭（上下を SVG の向きに直したもの）と、送り幅を返す。"""
    glyphs = font.getGlyphSet()
    name = font.getBestCmap()[ord(char)]
    pen = SVGPathPen(glyphs, lambda value: str(round(value)))
    glyphs[name].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
    return pen.getCommands(), glyphs[name].width


def plain_text(font: TTFont, text: str, size: float, x: float, baseline: float, fill: str, tracking: float = 1.0) -> str:
    """動かさない文字。"""
    scale = size / font["head"].unitsPerEm
    out, cursor = [], x
    for char in text:
        d, advance = outline(font, char)
        if d:
            out.append(f'<path transform="translate({cursor:.1f} {baseline}) scale({scale:.4f})" fill="{fill}" d="{d}"/>')
        cursor += advance * scale * tracking
    return "".join(out)


def headline(font: TTFont) -> str:
    out = []
    for row, (text, size, x, baseline, sleepy) in enumerate(LINES):
        scale = size / font["head"].unitsPerEm
        cursor = x
        last_line = row == len(LINES) - 1
        for index, char in enumerate(text):
            if sleepy:
                rot, drop = DROOP[row][index]
                cls = "ch sleepy"
                style = f"--rot:{rot}deg;--drop:{drop}px;animation-delay:{row * 0.25 + index * 0.07:.2f}s"
            else:
                cls = "ch go"
                style = f"animation-delay:{index * 0.045:.3f}s"

            if char == "。":
                radius = size * MARU_SIZE / 2
                cx = cursor + size * MARU_GAP + radius
                cy = baseline + size * MARU_SINK - radius
                if last_line:
                    # 最後の「。」だけは、黄色い明かり
                    out.append(f'<circle class="lamp" cx="{cx:.1f}" cy="{cy:.1f}" r="{radius:.1f}" fill="{LEMON}"/>')
                else:
                    # 文字と同じ動きを当てるので、文字と同じ座標系（書体の単位）で描く
                    stroke = size * MARU_STROKE
                    out.append(
                        f'<g transform="translate({cx:.1f} {cy:.1f}) scale({scale:.4f})"><circle class="{cls}" style="{style}" '
                        f'r="{(radius - stroke / 2) / scale:.0f}" stroke="{MOON}" stroke-width="{stroke / scale:.0f}"/></g>'
                    )
                cursor += size * (MARU_SIZE + MARU_GAP * 2)
                continue

            d, advance = outline(font, char)
            out.append(
                f'<g transform="translate({cursor:.1f} {baseline}) scale({scale:.4f})"><path class="{cls}" style="{style}" d="{d}"/></g>'
            )
            cursor += advance * scale * (0.97 if size > 100 else 1.03)
    return "".join(out)


def stars(count: int, seed: int) -> str:
    """文字でできた星（+ と * と ·）。見出し・黄色い円・掲示板には重ねない。"""
    rng = random.Random(seed)
    px, py, pr = PORTAL
    out, placed = [], []
    while len(out) < count:
        x, y = rng.uniform(14, WIDTH - 14), rng.uniform(12, SEAM_TOP - 12)
        if x < 610 and y > 28:
            continue  # 見出し
        if (x - px) ** 2 + (y - py) ** 2 < (pr + 16) ** 2:
            continue  # 黄色い円
        if any((x - sx) ** 2 + (y - sy) ** 2 < 34 ** 2 for sx, sy in placed):
            continue  # ほかの星に近すぎる
        placed.append((x, y))
        color = rng.choice([MOON, MOON, LAVENDER, LAVENDER, LEMON])
        opacity = rng.uniform(0.45, 0.95)
        kind = rng.choice("++*··")
        twinkle = ""
        if len(out) % 3 == 0:
            twinkle = f' class="tw" style="animation-duration:{rng.uniform(2.2, 5.2):.1f}s;animation-delay:-{rng.uniform(0, 4):.1f}s"'
        if kind == "·":
            body = f'<rect x="-1.5" y="-1.5" width="3" height="3"/>'
        else:
            arm = rng.choice([4, 5, 6])
            body = f'<path d="M-{arm} 0H{arm}M0 -{arm}V{arm}' + (f'M-{arm - 1} -{arm - 1}L{arm - 1} {arm - 1}M-{arm - 1} {arm - 1}L{arm - 1} -{arm - 1}' if kind == "*" else "") + '"/>'
        out.append(f'<g transform="translate({x:.0f} {y:.0f})" fill="{color}" stroke="{color}" stroke-width="1.6" opacity="{opacity:.2f}"{twinkle}>{body}</g>')
    return "".join(out)


def led(font_path: str) -> str:
    """電光掲示板に流す文を、点の並びにする。"""
    cell = 4  # 1 点を 4 × 4 の画素で描いてから、まん中を拾う
    font = ImageFont.truetype(font_path, LED_ROWS * cell)
    text = "".join(part for part, _color in LED_TEXT)
    columns = round(font.getlength(text) / cell)

    pad = LED_ROWS * cell
    image = Image.new("L", (columns * cell + cell, pad * 3), 0)
    ImageDraw.Draw(image).text((0, pad), text, font=font, fill=255)
    left, top, _right, bottom = image.getbbox()

    # 字の点と、拾う位置の刻みを合わせる（いちばんはっきり拾える位置を選ぶ）
    def sharpness(ox: int, oy: int) -> int:
        return sum(
            abs(image.getpixel((col * cell + ox, top + row * cell + oy)) - 127)
            for row in range(LED_ROWS)
            for col in range(columns)
            if top + row * cell + oy < image.height
        )

    ox, oy = max(((x, y) for x in range(cell) for y in range(cell)), key=lambda offset: sharpness(*offset))
    used_rows = -(-(bottom - top) // cell)
    first_row = (LED_ROWS - used_rows) // 2  # 上下のまん中に置く

    paths, column = [], 0
    for part, color in LED_TEXT:
        width = round(font.getlength(part) / cell)
        if color:
            rows = []
            for row in range(used_rows):
                y = top + row * cell + oy
                lit = [col for col in range(column, column + width) if y < image.height and image.getpixel((col * cell + ox, y)) > 127]
                if not lit:
                    continue
                # 1 行ぶんを、相対移動でつなげて書く（字数を減らすため）
                d, previous = f"M{lit[0]} {first_row + row}h0", lit[0]
                for col in lit[1:]:
                    d += f"m{col - previous} 0h0"
                    previous = col
                rows.append(d)
            paths.append(f'<path stroke="{color}" d="{"".join(rows)}"/>')
        column += width

    lap = columns * LED_PITCH
    ticker = (
        f'<g id="ticker" fill="none" stroke-width="{LED_DOT / LED_PITCH:.3f}" stroke-linecap="round" '
        f'transform="translate({LED_PITCH / 2} {BAND_TOP + LED_PITCH / 2}) scale({LED_PITCH})">{"".join(paths)}</g>'
    )
    return (
        f'<rect y="{BAND_TOP}" width="{WIDTH}" height="{HEIGHT - BAND_TOP}" fill="{NAVY}"/>'
        f'<rect y="{BAND_TOP}" width="{WIDTH}" height="{HEIGHT - BAND_TOP}" fill="url(#unlit)"/>'
        f'<g class="ticker" style="--lap:-{lap:.1f}px;animation-duration:{columns / LED_DOTS_PER_SECOND:.1f}s;'
        f'animation-timing-function:steps({columns})">{ticker}<use href="#ticker" x="{lap:.1f}"/></g>'
    )


def seam() -> str:
    """色の境目。上の色（群青）から下の色（紺）へ、3 段の点描でつなぐ。"""
    size = (BAND_TOP - SEAM_TOP) / 3
    return (
        f'<rect y="{SEAM_TOP}" width="{WIDTH}" height="{BAND_TOP - SEAM_TOP}" fill="{NIGHT}"/>'
        f'<rect y="{SEAM_TOP}" width="{WIDTH}" height="{BAND_TOP - SEAM_TOP}" fill="url(#dither)"/>'
    ), size


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    dela, dot_path = TTFont(sys.argv[1]), sys.argv[2]
    dot = TTFont(dot_path)

    px, py, pr = PORTAL
    seam_svg, cell = seam()
    led_svg = led(dot_path)

    portal = (
        f'<g class="portal"><circle cx="{px}" cy="{py}" r="{pr}" fill="{LEMON}"/>'
        f'<g class="inside">{plain_text(dela, "nemdull.com", 40, 860, 166, NAVY, 1.0)}'
        f'{plain_text(dot, "自分で自分を点検するページ", 22, 861, 204, NAVY, 1.0)}</g></g>'
    )
    zzz = "".join(
        f'<g class="zzz" style="animation-delay:{delay}s">{plain_text(dot, "z", size, x, y, LEMON)}</g>'
        for size, x, y, delay in [(28, 520, 96, 0), (36, 546, 76, 0.5), (46, 580, 52, 1)]
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="t">
<title id="t">ねむい。だるい。だから自動化する。</title>
<defs>
<linearGradient id="tail" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{MOON}"/><stop offset="0.35" stop-color="{LEMON}"/><stop offset="1" stop-color="{LEMON}" stop-opacity="0"/></linearGradient>
<clipPath id="frame"><rect width="{WIDTH}" height="{HEIGHT}" rx="28"/></clipPath>
<pattern id="unlit" width="{LED_PITCH}" height="{LED_PITCH}" y="{BAND_TOP}" patternUnits="userSpaceOnUse"><circle cx="{LED_PITCH / 2}" cy="{LED_PITCH / 2}" r="{LED_DOT / 2 - 0.2:.2f}" fill="{UNLIT}"/></pattern>
<pattern id="dither" width="{cell * 4}" height="{cell * 3}" y="{SEAM_TOP}" patternUnits="userSpaceOnUse" fill="{NAVY}"><rect width="{cell}" height="{cell}"/><rect y="{cell}" width="{cell}" height="{cell}"/><rect x="{cell * 2}" y="{cell}" width="{cell}" height="{cell}"/><rect y="{cell * 2}" width="{cell * 4}" height="{cell}"/><rect x="{cell * 2}" y="{cell * 2}" width="{cell}" height="{cell}" fill="{NIGHT}"/></pattern>
</defs>
<style>
.ch{{fill:{MOON};transform-box:fill-box;transform-origin:center}}
circle.ch{{fill:none}}
.tw{{animation:tw 3s ease-in-out infinite}}
.sleepy{{animation:sleepy 14s cubic-bezier(.2,.9,.2,1) infinite both}}
.go{{animation:go 14s cubic-bezier(.2,1.5,.4,1) infinite both}}
.lamp{{transform-box:fill-box;transform-origin:center;animation:lamp 14s ease-out infinite both}}
.portal{{transform-origin:{px}px {py}px;animation:portal 14s cubic-bezier(.2,1.3,.4,1) infinite both}}
.inside{{animation:inside 14s ease-out infinite both}}
.zzz{{opacity:0;animation:zzz 14s ease-out infinite}}
.meteor{{opacity:0;animation:meteor 14s cubic-bezier(.55,0,.9,.6) infinite}}
.ticker{{animation:ticker linear infinite}}
@keyframes tw{{50%{{opacity:.15}}}}
@keyframes sleepy{{0%{{opacity:0;transform:translateY(-160px)}}9%,17%{{opacity:.45;transform:translateY(var(--drop)) rotate(var(--rot))}}21%,90%{{opacity:1;transform:none}}100%{{opacity:0;transform:translateY(var(--drop)) rotate(var(--rot))}}}}
@keyframes go{{0%,18%{{opacity:0;transform:translateY(700px) scale(.5)}}22%,90%{{opacity:1;transform:none}}96%,100%{{opacity:0;transform:none}}}}
@keyframes lamp{{0%,23%{{opacity:0;transform:scale(0)}}26%{{opacity:1;transform:scale(1.9)}}29%,90%{{opacity:1;transform:none}}96%,100%{{opacity:0;transform:none}}}}
@keyframes portal{{0%,27%{{opacity:0;transform:scale(0)}}28%{{opacity:1;transform:scale(0)}}35%,90%{{opacity:1;transform:none}}96%,100%{{opacity:0;transform:none}}}}
@keyframes inside{{0%,34%{{opacity:0}}38%,100%{{opacity:1}}}}
@keyframes zzz{{0%,3%{{opacity:0;transform:translate(0,0)}}7%{{opacity:.95}}15%{{opacity:0;transform:translate(26px,-40px)}}100%{{opacity:0;transform:translate(26px,-40px)}}}}
@keyframes meteor{{0%,16.5%{{opacity:0;transform:translate(1260px,-60px) rotate(-28deg)}}17%{{opacity:1;transform:translate(1260px,-60px) rotate(-28deg)}}21%{{opacity:1;transform:translate(560px,300px) rotate(-28deg)}}21.5%,100%{{opacity:0;transform:translate(560px,300px) rotate(-28deg)}}}}
@keyframes ticker{{to{{transform:translateX(var(--lap))}}}}
@media (prefers-reduced-motion:reduce){{.ch,.tw,.lamp,.portal,.inside,.zzz,.meteor,.ticker{{animation:none}}.zzz,.meteor{{display:none}}}}
</style>
<g clip-path="url(#frame)">
<rect width="{WIDTH}" height="{HEIGHT}" fill="{NIGHT}"/>
{stars(40, 7)}
{portal}
{zzz}
<rect class="meteor" width="260" height="5" rx="3" fill="url(#tail)"/>
{headline(dela)}
{seam_svg}
{led_svg}
</g>
</svg>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print(f"作成: {OUT}  {OUT.stat().st_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
