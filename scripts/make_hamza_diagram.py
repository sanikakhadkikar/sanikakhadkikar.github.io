"""Draw the newsprint-style cross-section of the Amazon and the Hamza "river" for the Amazon post.

Usage: python scripts/make_hamza_diagram.py
Numbers from https://en.wikipedia.org/wiki/Hamza_River. Not to scale.
Text classes match the .nc-map styles in assets/css/notcringe.css.
"""
import random
from pathlib import Path

out = Path(__file__).resolve().parent.parent / "content/caricature/amazon/hamza.svg"
ink, paper, red, pink, grey, muted, water = "#1b1a17", "#f4efe4", "#c8102e", "#eab3ba", "#b9b09d", "#5d574c", "#c9d6d8"
W, H = 1000, 660
ground = 150          # surface line
km = 85               # pixels per km of depth
rnd = random.Random(4)


def text(x, y, s, cls, anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{s}</text>'


b = [f'<svg class="nc-map" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
     f'aria-label="Cross-section showing the Amazon river at the surface and the much slower, wider Hamza underground flow about 4 kilometres below it">',
     f'<rect width="{W}" height="{H}" fill="{paper}"/>',
     '<defs><marker id="flow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
     f'<path d="M0,0 L10,5 L0,10 Z" fill="{red}"/></marker>'
     '<marker id="fast" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
     f'<path d="M0,0 L10,5 L0,10 Z" fill="{ink}"/></marker></defs>']

# rock layers between the surface and the bottom
layers = [ground, ground + 1.3 * km, ground + 2.4 * km, ground + 3.5 * km]
for i, top in enumerate(layers):
    bottom = layers[i + 1] if i + 1 < len(layers) else H
    b.append(f'<rect x="0" y="{top:.0f}" width="{W}" height="{bottom - top:.0f}" fill="{"#ebe3d2" if i % 2 else "#e2d9c6"}"/>')
    b.append(f'<line x1="0" y1="{top:.0f}" x2="{W}" y2="{top:.0f}" stroke="{grey}" stroke-width="1"/>')

# the Hamza flow: a broad band of porous rock about 4 km down
hz_top, hz_bot = ground + 3.8 * km, ground + 4.6 * km
b.append(f'<path d="M0,{hz_top:.0f} C250,{hz_top - 14:.0f} 600,{hz_top + 12:.0f} {W},{hz_top - 6:.0f} '
         f'L{W},{hz_bot + 4:.0f} C650,{hz_bot + 16:.0f} 300,{hz_bot - 10:.0f} 0,{hz_bot:.0f} Z" fill="{pink}" stroke="{red}" stroke-width="1.5"/>')
for _ in range(260):
    x, y = rnd.uniform(5, W - 5), rnd.uniform(hz_top + 6, hz_bot - 4)
    b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.2, 2.6):.1f}" fill="{paper}" stroke="{red}" stroke-width="0.6"/>')
for x in (120, 380, 640):
    y = (hz_top + hz_bot) / 2
    b.append(f'<line x1="{x}" y1="{y:.0f}" x2="{x + 60}" y2="{y:.0f}" stroke="{red}" stroke-width="2.5" marker-end="url(#flow)"/>')

# surface: forest on both banks, river channel in the middle
cx, half = 560, 110
b.append(f'<path d="M0,{ground} L{cx - half - 30},{ground} C{cx - half},{ground} {cx - half + 10},{ground + 38} {cx - half + 60},{ground + 40} '
         f'L{cx + half - 60},{ground + 40} C{cx + half - 10},{ground + 38} {cx + half},{ground} {cx + half + 30},{ground} L{W},{ground} '
         f'L{W},{ground + 1} L0,{ground + 1} Z" fill="{ink}"/>')
b.append(f'<path d="M{cx - half - 22},{ground} C{cx - half + 2},{ground + 2} {cx - half + 12},{ground + 36} {cx - half + 60},{ground + 38} '
         f'L{cx + half - 60},{ground + 38} C{cx + half - 12},{ground + 36} {cx + half - 2},{ground + 2} {cx + half + 22},{ground} Z" fill="{water}" stroke="{ink}" stroke-width="2"/>')
wells = (190, 320, 820)
for x0, x1 in ((95, cx - half - 30), (cx + half + 30, W - 10)):
    x = x0
    while x < x1 - 14:
        r = rnd.uniform(9, 15)
        if any(abs(x + r - w) < r + 14 for w in wells):
            x += 2 * r
            continue
        b.append(f'<line x1="{x + r:.0f}" y1="{ground}" x2="{x + r:.0f}" y2="{ground - r - 6:.0f}" stroke="{ink}" stroke-width="1.5"/>')
        b.append(f'<circle cx="{x + r:.0f}" cy="{ground - r - 12:.0f}" r="{r:.0f}" fill="{grey}" stroke="{ink}" stroke-width="1.2"/>')
        x += 2 * r + rnd.uniform(0, 6)
b.append(f'<line x1="{cx - 50}" y1="{ground + 20}" x2="{cx + 40}" y2="{ground + 20}" stroke="{ink}" stroke-width="2.5" marker-end="url(#fast)"/>')
b.append(text(cx, ground - 66, "AMAZON", "nc-map-country"))
b.append(text(cx, ground - 48, "about 2 metres per second", "nc-map-place"))

# old oil wells reaching below the flow, with temperature readings
for x in wells:
    b.append(f'<path d="M{x - 9},{ground - 2} L{x},{ground - 30} L{x + 9},{ground - 2}" fill="none" stroke="{ink}" stroke-width="1.6"/>')
    b.append(f'<line x1="{x}" y1="{ground}" x2="{x}" y2="{hz_bot + 30:.0f}" stroke="{ink}" stroke-width="1.6" stroke-dasharray="6 4"/>')
    for d in range(1, 5):
        y = ground + d * km
        b.append(f'<line x1="{x - 5}" y1="{y:.0f}" x2="{x + 5}" y2="{y:.0f}" stroke="{red}" stroke-width="2"/>')
b.append(text(332, ground + 0.6 * km + 4, "old oil wells, temperature", "nc-map-place", "start"))
b.append(text(332, ground + 0.6 * km + 20, "measured on the way down", "nc-map-place", "start"))

# depth scale on the left
b.append(f'<line x1="70" y1="{ground}" x2="70" y2="{ground + 4 * km:.0f}" stroke="{ink}" stroke-width="1.2"/>')
for d in range(0, 5):
    y = ground + d * km
    b.append(f'<line x1="64" y1="{y:.0f}" x2="76" y2="{y:.0f}" stroke="{ink}" stroke-width="1.2"/>')
    b.append(f'<rect x="6" y="{y - 11:.0f}" width="54" height="16" fill="{paper}" opacity="0.85"/>')
    b.append(text(58, y + 2, f"{d} km" if d else "surface", "nc-map-place", "end"))
b.append(text(500, hz_bot + 40, "THE HAMZA “RIVER”", "nc-map-country"))
b.append(text(500, hz_bot + 58, "water seeping through porous rock, under 1 millimetre per second, 200 to 400 km wide", "nc-map-place"))
b.append(text(18, 28, "WEST", "nc-map-place", "start"))
b.append(text(W - 18, 28, "EAST, towards the Atlantic", "nc-map-place", "end"))
b.append(text(18, H - 12, "Not to scale.", "nc-map-place", "start"))
b.append(f'<rect width="{W}" height="{H}" fill="none" stroke="{ink}" stroke-width="3"/>')
b.append("</svg>")
out.write_text("\n".join(b))
print(out)
