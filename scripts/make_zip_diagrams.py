"""Draw the newsprint-style diagrams for the file compression post.

Usage: python scripts/make_zip_diagrams.py
Writes huffman.svg, lz77.svg and archives.svg into content/caricature/zip.
Text classes match the .nc-map styles in assets/css/notcringe.css.
"""
from pathlib import Path

out = Path(__file__).resolve().parent.parent / "content/caricature/zip"
ink, paper, red, pink, grey, muted, water = "#1b1a17", "#f4efe4", "#c8102e", "#eab3ba", "#b9b09d", "#5d574c", "#d5dcdc"


def svg(w, h, label, body):
    return "\n".join([f'<svg class="nc-map" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">',
                      f'<rect width="{w}" height="{h}" fill="{paper}"/>', *body,
                      f'<rect width="{w}" height="{h}" fill="none" stroke="{ink}" stroke-width="3"/>', "</svg>"])


def text(x, y, s, cls, anchor="middle", extra=""):
    return f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" class="{cls}" {extra}>{s}</text>'


def node(x, y, label, sub, fill):
    return [f'<circle cx="{x}" cy="{y}" r="26" fill="{fill}" stroke="{ink}" stroke-width="2"/>',
            text(x, y + 6, label, "nc-map-country"),
            text(x, y + 46, sub, "nc-map-place")]


def edge(x1, y1, x2, y2, bit):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ink}" stroke-width="2"/>',
            f'<circle cx="{mx}" cy="{my}" r="12" fill="{paper}" stroke="{red}" stroke-width="1.5"/>',
            text(mx, my + 5, bit, "nc-map-gdp", extra=f'style="fill:{red}"')]


def bits(x, y, s, cell, color, label):
    b = [text(x, y - 10, label, "nc-map-place", "start")]
    for i, ch in enumerate(s):
        if ch == " ":
            continue
        b.append(f'<rect x="{x + i * cell:.1f}" y="{y}" width="{cell - 1:.1f}" height="22" fill="{color}" stroke="{ink}" stroke-width="0.6"/>')
        b.append(text(x + i * cell + cell / 2 - 0.5, y + 16, ch, "nc-map-place"))
    return b


# 1. Huffman tree for BANANA
b = [text(500, 36, "HUFFMAN CODING “BANANA”", "nc-map-country"),
     text(170, 92, "Count the letters", "nc-map-gdp")]
for i, (ch, n) in enumerate((("A", 3), ("N", 2), ("B", 1))):
    y = 130 + i * 44
    b.append(text(110, y, ch, "nc-map-country"))
    b.append(f'<rect x="135" y="{y - 18}" width="{n * 40}" height="24" fill="{pink}" stroke="{ink}" stroke-width="1"/>')
    b.append(text(150 + n * 40, y, f"× {n}", "nc-map-place", "start"))
b.append(text(170, 300, "Rare letters go deeper,", "nc-map-place"))
b.append(text(170, 318, "so they get longer codes", "nc-map-place"))
b += edge(560, 100, 470, 200, "0") + edge(560, 100, 650, 200, "1") + edge(650, 200, 590, 300, "0") + edge(650, 200, 710, 300, "1")
b += [f'<circle cx="560" cy="100" r="22" fill="{paper}" stroke="{ink}" stroke-width="2"/>', text(560, 106, "6", "nc-map-gdp")]
b += [f'<circle cx="650" cy="200" r="22" fill="{paper}" stroke="{ink}" stroke-width="2"/>', text(650, 206, "3", "nc-map-gdp")]
b += node(470, 200, "A", "code 0", pink) + node(590, 300, "N", "code 10", pink) + node(710, 300, "B", "code 11", pink)
b += bits(60, 392, "010000100100000101001110010000010100111001000001", 18.6, water, "Normal text: 6 letters × 8 bits = 48 bits")
b += bits(60, 462, "11 0 10 0 10 0", 18.6, pink, "Huffman: B A N A N A = 9 bits")
huffman = svg(1000, 510, "Huffman tree for the word banana, giving A the code 0, N the code 10 and B the code 11, shrinking 48 bits to 9", b)

# 2. LZ77 back-reference
phrase = "TO BE OR NOT TO BE"
x0, w = 50, 50
b = [f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="{red}"/></marker></defs>',
     text(500, 32, "LEMPEL\u2013ZIV \u201cTO BE OR NOT TO BE\u201d", "nc-map-country")]
for i, ch in enumerate(phrase):
    copy = i >= 13
    first = i < 5
    fill = pink if copy else (water if first else paper)
    b.append(f'<rect x="{x0 + i * w}" y="90" width="{w - 4}" height="56" fill="{fill}" stroke="{ink}" stroke-width="1.5"/>')
    b.append(text(x0 + i * w + (w - 4) / 2, 127, ch if ch != " " else "\u00b7", "nc-map-country", extra='style="font-size:24px"'))
b.append(f'<path d="M{x0 + 15.5 * w},150 C{x0 + 15.5 * w},230 {x0 + 2.5 * w},230 {x0 + 2.5 * w},150" fill="none" stroke="{red}" stroke-width="2.5" marker-end="url(#ah)"/>')
b.append(text(x0 + 2.5 * w, 76, "first time: written out", "nc-map-place"))
b.append(text(x0 + 15.5 * w, 76, "second time: \u201cgo back 13, copy 5\u201d", "nc-map-gdp", extra=f'style="fill:{red}"'))
b.append(text(500, 268, "Stored as: TO BE OR NOT (go back 13, copy 5)", "nc-map-gdp"))
b.append(text(500, 290, "Two small numbers replace five letters. The dots are spaces, which count as characters too.", "nc-map-place"))
lz = svg(1000, 310, "Lempel-Ziv compression of to be or not to be: the second to be is replaced by an instruction to go back 13 characters and copy 5", b)

# 3. tar.gz vs zip vs h5
b = [text(170, 36, ".TAR.GZ", "nc-map-country"), text(500, 36, ".ZIP", "nc-map-country"), text(830, 36, ".H5", "nc-map-country")]
# tar.gz: files glued, one compressed wrapper
b.append(f'<rect x="40" y="62" width="260" height="210" fill="{pink}" stroke="{ink}" stroke-width="2" stroke-dasharray="6 4"/>')
for i in range(4):
    b.append(f'<rect x="70" y="{82 + i * 44}" width="200" height="36" fill="{paper}" stroke="{ink}" stroke-width="1.5"/>')
    b.append(text(170, 106 + i * 44, f"file {i + 1}", "nc-map-place"))
b.append(text(170, 296, "Bundle everything, then compress", "nc-map-place"))
b.append(text(170, 314, "the whole bundle at once", "nc-map-place"))
# zip: each file compressed, index at end
for i in range(4):
    y = 70 + i * 44
    b.append(f'<rect x="380" y="{y}" width="240" height="36" fill="{paper}" stroke="{ink}" stroke-width="1.5"/>')
    b.append(f'<rect x="388" y="{y + 6}" width="120" height="24" fill="{pink}" stroke="{ink}" stroke-width="1" stroke-dasharray="4 3"/>')
    b.append(text(448, y + 23, f"file {i + 1}", "nc-map-place"))
b.append(f'<rect x="380" y="246" width="240" height="30" fill="{ink}"/>')
b.append(text(500, 266, "index: where each file is", "nc-map-place", extra=f'style="fill:{paper};stroke:{ink}"'))
b.append(text(500, 296, "Compress each file on its own,", "nc-map-place"))
b.append(text(500, 314, "with a map at the end", "nc-map-place"))
# h5: folders and arrays inside one file
b.append(f'<rect x="700" y="62" width="260" height="210" fill="{paper}" stroke="{ink}" stroke-width="2"/>')
tree = [(0, "/ (one file)", False), (1, "H1/", False), (2, "strain  [array]", True), (2, "quality  [array]", True), (1, "L1/", False), (2, "strain  [array]", True)]
for i, (d, name, arr) in enumerate(tree):
    y = 92 + i * 30
    x = 720 + d * 28
    if d:
        b.append(f'<path d="M{x - 18},{y - 22} L{x - 18},{y - 5} L{x - 6},{y - 5}" fill="none" stroke="{grey}" stroke-width="1.5"/>')
    if arr:
        b.append(f'<rect x="{x - 2}" y="{y - 16}" width="150" height="20" fill="{pink}" stroke="{ink}" stroke-width="0.8"/>')
    b.append(text(x + 2, y, name, "nc-map-place", "start"))
b.append(text(830, 296, "A file system inside a file,", "nc-map-place"))
b.append(text(830, 314, "built for big scientific arrays", "nc-map-place"))
archives = svg(1000, 340, "Comparison of tar.gz, zip and HDF5 file layouts", b)

for name, content in (("huffman.svg", huffman), ("lz77.svg", lz), ("archives.svg", archives)):
    (out / name).write_text(content)
    print(out / name)
