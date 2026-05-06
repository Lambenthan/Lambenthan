#!/usr/bin/env python3
"""Render Chinese signature text as an SVG with LXGW WenKai glyphs as outlined paths.
The font is fully baked into geometry — works in any browser without external font loading."""

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

FONT_PATH = "/Users/han/Library/Fonts/LXGWWenKai-Medium.ttf"
TEXT = "在审计与大模型之间，记笔记的人"
COLOR = "#2C4768"           # navy, matches the typing animation
FONT_SIZE = 22              # rendered px height
PADDING_X = 16
PADDING_Y = 6
OUTPUT = "/Users/han/Desktop/AI_Plan/2026LLM/Media_Paper/github-profile/assets/signature.svg"


def main() -> None:
    font = TTFont(FONT_PATH)
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    units_per_em = font['head'].unitsPerEm
    ascent = font['hhea'].ascent
    descent = font['hhea'].descent  # negative
    scale = FONT_SIZE / units_per_em

    cursor = 0
    paths = []
    for ch in TEXT:
        glyph_name = cmap.get(ord(ch))
        if not glyph_name:
            cursor += units_per_em // 2
            continue
        glyph = glyph_set[glyph_name]
        pen = SVGPathPen(glyph_set)
        glyph.draw(pen)
        commands = pen.getCommands()
        if commands:
            paths.append((cursor, commands))
        cursor += glyph.width

    text_width_units = cursor
    text_height_units = ascent - descent

    svg_width = round(text_width_units * scale + PADDING_X * 2, 2)
    svg_height = round(text_height_units * scale + PADDING_Y * 2, 2)
    baseline_y = round(PADDING_Y + ascent * scale, 2)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {svg_width} {svg_height}" '
        f'width="{svg_width}" height="{svg_height}">',
        f'<g transform="translate({PADDING_X}, {baseline_y}) scale({scale}, -{scale})" fill="{COLOR}">'
    ]
    for x_offset, d in paths:
        parts.append(f'<path d="{d}" transform="translate({x_offset}, 0)"/>')
    parts.append('</g></svg>')

    svg = ''.join(parts)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f"wrote {OUTPUT}")
    print(f"  size: {svg_width:.0f} x {svg_height:.0f} px")
    print(f"  glyphs rendered: {len(paths)}")
    print(f"  file size: {len(svg.encode('utf-8'))} bytes")


if __name__ == "__main__":
    main()
