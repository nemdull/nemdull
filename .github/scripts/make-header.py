#!/usr/bin/env python3
"""README の上に出している assets/header.svg を作る。

使い方:
    pip install fonttools
    python3 .github/scripts/make-header.py <DelaGothicOne-Regular.ttf の場所>

書体は Dela Gothic One（SIL Open Font License 1.1）。GitHub の README では Web フォントを読み込めないので、
文字は輪郭（パス）にして埋め込んでいる。書体は https://github.com/google/fonts の ofl/delagothicone にある。
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

OUT = Path(__file__).resolve().parents[2] / "assets" / "header.svg"
WIDTH, HEIGHT = 1200, 400

# (文字列, 文字の大きさ, 左端 x, ベースライン y, 眠そうに垂れるか)
LINES = [
    ("ねむい。", 132, 64, 150, True),
    ("だるい。", 132, 64, 286, True),
    ("だから自動化する。", 58, 68, 358, False),
]

# 眠そうに傾く角度（度）と、ずり落ちる量（書体の単位）。行ごと・文字ごとに少しずつ違える
DROOP = [
    [(-3, 0), (5, 40), (10, 90), (16, 160)],
    [(-6, 30), (7, 80), (14, 150), (22, 250)],
]


def glyph_paths(font: TTFont, text: str, size: float, x: float, baseline: float):
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    cursor = x
    for char in text:
        name = cmap[ord(char)]
        pen = SVGPathPen(glyphs, lambda value: str(round(value)))
        glyphs[name].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
        yield char, cursor, baseline, scale, pen.getCommands()
        cursor += glyphs[name].width * scale * (0.97 if size > 100 else 1.03)


def stars(count: int, seed: int) -> str:
    rng = random.Random(seed)
    out = []
    for index in range(count):
        depth = 0.25 + rng.random() * 0.75
        cx, cy = rng.random() * WIDTH, rng.random() * HEIGHT
        radius = 0.5 + depth * 1.5 * rng.random()
        color = "#ffd896" if rng.random() < 0.12 else "#d6eaff"
        twinkle = ""
        if index % 3 == 0:
            twinkle = f' class="tw" style="animation-duration:{2.2 + rng.random() * 3:.1f}s;animation-delay:-{rng.random() * 4:.1f}s"'
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{radius:.2f}" fill="{color}" opacity="{0.25 + 0.75 * depth:.2f}"{twinkle}/>')
    return "".join(out)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    font = TTFont(sys.argv[1])

    letters = []
    for row, (text, size, x, baseline, sleepy) in enumerate(LINES):
        for index, (char, gx, gy, scale, d) in enumerate(glyph_paths(font, text, size, x, baseline)):
            if sleepy:
                rot, drop = DROOP[row][index]
                style = f"--rot:{rot}deg;--drop:{drop}px;animation-delay:{row * 0.25 + index * 0.07:.2f}s"
                cls = "ch sleepy"
            else:
                style = f"animation-delay:{index * 0.045:.3f}s"
                cls = "ch go"
            letters.append(
                f'<g transform="translate({gx:.1f} {gy}) scale({scale:.4f})"><path class="{cls}" style="{style}" d="{d}"/></g>'
            )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="t">
<title id="t">ねむい。だるい。だから自動化する。</title>
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06112a"/><stop offset="1" stop-color="#030a1c"/></linearGradient>
<radialGradient id="glow" cx="0.86" cy="-0.1" r="0.9"><stop offset="0" stop-color="#27498a" stop-opacity="0.85"/><stop offset="0.65" stop-color="#27498a" stop-opacity="0"/></radialGradient>
<radialGradient id="moon" cx="0.36" cy="0.32" r="0.8"><stop offset="0" stop-color="#fdfeff"/><stop offset="1" stop-color="#9fd6f5"/></radialGradient>
<linearGradient id="tail" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="0.35" stop-color="#ffc857"/><stop offset="1" stop-color="#ffc857" stop-opacity="0"/></linearGradient>
<clipPath id="frame"><rect width="{WIDTH}" height="{HEIGHT}" rx="28"/></clipPath>
</defs>
<style>
.ch{{fill:#eef5ff;transform-box:fill-box;transform-origin:center}}
.tw{{animation:tw 3s ease-in-out infinite}}
.sleepy{{animation:sleepy 14s cubic-bezier(.2,.9,.2,1) infinite both}}
.go{{animation:go 14s cubic-bezier(.2,1.5,.4,1) infinite both}}
.orbit{{transform-origin:968px 196px;animation:turn 40s linear infinite}}
.orbit2{{transform-origin:968px 196px;animation:turn 64s linear infinite reverse}}
.zzz text{{fill:#66bff0;font:700 30px monospace;opacity:0;animation:zzz 14s ease-out infinite}}
.meteor{{opacity:0;animation:meteor 14s cubic-bezier(.55,0,.9,.6) infinite}}
@keyframes tw{{50%{{opacity:.15}}}}
@keyframes sleepy{{0%{{opacity:0;transform:translateY(-160px)}}9%,17%{{opacity:.45;transform:translateY(var(--drop)) rotate(var(--rot))}}21%,90%{{opacity:1;transform:none}}100%{{opacity:0;transform:translateY(var(--drop)) rotate(var(--rot))}}}}
@keyframes go{{0%,18%{{opacity:0;transform:translateY(700px) scale(.5)}}22%,90%{{opacity:1;transform:none}}96%,100%{{opacity:0;transform:none}}}}
@keyframes turn{{to{{transform:rotate(360deg)}}}}
@keyframes zzz{{0%,3%{{opacity:0;transform:translate(0,0)}}7%{{opacity:.95}}15%{{opacity:0;transform:translate(26px,-40px)}}100%{{opacity:0;transform:translate(26px,-40px)}}}}
@keyframes meteor{{0%,16.5%{{opacity:0;transform:translate(1260px,-60px) rotate(-28deg)}}17%{{opacity:1;transform:translate(1260px,-60px) rotate(-28deg)}}21%{{opacity:1;transform:translate(560px,300px) rotate(-28deg)}}21.5%,100%{{opacity:0;transform:translate(560px,300px) rotate(-28deg)}}}}
@media (prefers-reduced-motion:reduce){{.ch,.tw,.orbit,.orbit2,.zzz text,.meteor{{animation:none}}.zzz,.meteor{{display:none}}}}
</style>
<g clip-path="url(#frame)">
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#sky)"/>
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#glow)"/>
{stars(120, 11)}
<circle cx="968" cy="196" r="232" fill="none" stroke="#a5bbdd" stroke-opacity="0.18"/>
<circle cx="968" cy="196" r="170" fill="none" stroke="#a5bbdd" stroke-opacity="0.5" stroke-dasharray="4 6"/>
<circle cx="968" cy="196" r="112" fill="url(#moon)"/>
<circle cx="968" cy="196" r="118" fill="none" stroke="#66bff0" stroke-opacity="0.55" stroke-width="5"/>
<circle cx="930" cy="160" r="20" fill="#66bff0" opacity="0.28"/><circle cx="1004" cy="232" r="30" fill="#66bff0" opacity="0.22"/><circle cx="1010" cy="150" r="11" fill="#66bff0" opacity="0.3"/><circle cx="930" cy="248" r="9" fill="#66bff0" opacity="0.3"/>
<g class="orbit"><circle cx="1138" cy="196" r="9" fill="#ffc857"/><circle cx="798" cy="196" r="6" fill="#66bff0"/></g>
<g class="orbit2"><circle cx="968" cy="-36" r="5" fill="#62e6a0"/><circle cx="968" cy="428" r="7" fill="#eef5ff"/></g>
<g class="zzz"><text x="1058" y="96">z</text><text x="1078" y="80" style="animation-delay:.5s;font-size:38px">z</text><text x="1104" y="60" style="animation-delay:1s;font-size:46px">z</text></g>
<rect class="meteor" width="260" height="5" rx="3" fill="url(#tail)"/>
{''.join(letters)}
</g>
</svg>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print(f"作成: {OUT}  {OUT.stat().st_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
