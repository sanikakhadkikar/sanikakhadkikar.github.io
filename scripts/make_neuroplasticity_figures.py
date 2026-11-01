"""Draw the newsprint-style schematic figures for the neuroplasticity post.

Usage: python scripts/make_neuroplasticity_figures.py
Writes synapse.svg, spines.svg, stress-brain.svg and naming.svg into the post folder.
Text classes match the .nc-map styles in assets/css/notcringe.css.
"""
import random
from pathlib import Path

out = Path(__file__).resolve().parent.parent / "content/not-cringe/neuroplasticity"

ink, paper, red, pink, grey, muted = "#1b1a17", "#f4efe4", "#c8102e", "#eab3ba", "#b9b09d", "#5d574c"


def svg(width, height, label, body):
    return "\n".join([
        f'<svg class="nc-map" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">',
        f'<rect width="{width}" height="{height}" fill="{paper}"/>',
        *body,
        f'<rect width="{width}" height="{height}" fill="none" stroke="{ink}" stroke-width="3"/>',
        "</svg>",
    ])


def text(x, y, s, cls, anchor="middle", extra=""):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}" {extra}>{s}</text>'


def synapse(cx, vesicles, released, receptors, title, sub):
    rnd = random.Random(cx)
    b = [text(cx, 52, title, "nc-map-country"), text(cx, 72, sub, "nc-map-place")]
    # axon and presynaptic terminal
    b.append(f'<path d="M{cx-28},90 L{cx-28},130 Q{cx-120},140 {cx-120},200 Q{cx-120},262 {cx},262 '
             f'Q{cx+120},262 {cx+120},200 Q{cx+120},140 {cx+28},130 L{cx+28},90 Z" fill="{paper}" stroke="{ink}" stroke-width="2.5"/>')
    for _ in range(vesicles):
        x, y = cx + rnd.uniform(-80, 80), rnd.uniform(165, 240)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{pink}" stroke="{ink}" stroke-width="1.5"/>')
    # neurotransmitter in the cleft
    for _ in range(released):
        x, y = cx + rnd.uniform(-100, 100), rnd.uniform(272, 298)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="{red}"/>')
    # postsynaptic side
    b.append(f'<path d="M{cx-150},420 L{cx-150},322 Q{cx},300 {cx+150},322 L{cx+150},420" fill="{paper}" stroke="{ink}" stroke-width="2.5"/>')
    xs = [cx - 110 + i * 220 / max(1, receptors - 1) for i in range(receptors)] if receptors > 1 else [cx]
    for x in xs:
        y = 312 + abs(x - cx) * 0.07
        b.append(f'<rect x="{x-6:.0f}" y="{y-8:.0f}" width="12" height="16" rx="3" fill="{red}" stroke="{ink}" stroke-width="1.2"/>')
    return b


# Lateral view of a left hemisphere, front facing left, in a 400 x 310 box
cerebrum = ("M28,150 C22,82 92,24 190,20 C292,16 378,60 393,140 C398,170 392,192 376,202 "
            "C352,214 322,214 300,212 C280,216 262,226 248,236 C224,250 186,254 160,244 "
            "C132,234 112,218 104,198 C90,198 64,196 48,186 C36,178 30,166 28,150 Z")
cerebellum = "M292,206 C320,200 362,200 382,212 C398,228 388,260 356,266 C322,272 292,260 282,244 C278,228 282,212 292,206 Z"
brainstem = "M232,232 C242,256 248,284 250,306 L230,306 C226,284 220,262 210,244 Z"
# Sylvian fissure, central sulcus and a few others
sulci = [
    ("M108,196 C140,184 186,174 228,166 C250,162 268,154 280,142", 2.4),  # lateral (Sylvian) fissure
    ("M222,22 C214,58 200,96 190,132 C186,146 184,156 186,166", 2.4),     # central sulcus
    ("M196,24 C188,60 176,98 166,140 C164,150 164,160 166,170", 1.6),     # precentral sulcus
    ("M248,26 C240,62 228,100 220,138", 1.6),                             # postcentral sulcus
    ("M70,82 C100,72 130,68 160,70", 1.6),                                # superior frontal sulcus
    ("M52,120 C84,110 118,106 152,110", 1.6),                             # inferior frontal sulcus
    ("M150,226 C188,216 232,206 276,196 C298,191 318,190 340,193", 1.6),  # superior temporal sulcus
    ("M262,90 C292,82 320,86 346,100", 1.6),                              # intraparietal sulcus
    ("M352,62 C346,90 352,116 368,140", 1.6),                             # parieto-occipital
]
# Prefrontal cortex: front of the frontal lobe, ahead of the premotor strip, above the Sylvian fissure
pfc = ("M28,150 C22,82 92,24 150,21 C140,60 130,104 124,150 C120,172 114,186 108,196 "
       "C90,198 64,196 48,186 C36,178 30,166 28,150 Z")
amygdala = (152, 214)  # deep in the front of the temporal lobe, drawn dashed because it is hidden from view


def brain(dx, dy, pfc_fill, amy_rx, amy_fill, arrow_w):
    ax, ay = amygdala
    g = [f'<g transform="translate({dx},{dy})">',
         f'<path d="{cerebellum}" fill="{paper}" stroke="{ink}" stroke-width="2.2"/>',
         f'<path d="M292,226 C320,222 352,222 380,228 M286,240 C316,236 352,236 384,242 M292,254 C318,252 346,252 372,256" fill="none" stroke="{grey}" stroke-width="1.4"/>',
         f'<path d="{brainstem}" fill="{paper}" stroke="{ink}" stroke-width="2.2"/>',
         f'<path d="{cerebrum}" fill="{paper}" stroke="{ink}" stroke-width="2.5"/>',
         f'<path d="{pfc}" fill="{pfc_fill}" stroke="{ink}" stroke-width="1.6"/>',
         *[f'<path d="{d}" fill="none" stroke="{ink if w > 2 else grey}" stroke-width="{w}" stroke-linecap="round"/>' for d, w in sulci],
         f'<ellipse cx="{ax}" cy="{ay}" rx="{amy_rx}" ry="{amy_rx * 0.72:.1f}" fill="{amy_fill}" stroke="{ink}" stroke-width="2" stroke-dasharray="5 3"/>',
         f'<path d="M96,140 C112,168 122,182 {ax - amy_rx * 0.7:.0f},{ay - amy_rx * 0.72 - 2:.0f}" fill="none" stroke="{ink}" stroke-width="{arrow_w}" marker-end="url(#arrow)"/>',
         "</g>"]
    return g


defs = (f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 Z" fill="{ink}"/></marker></defs>')


def labels(dx, dy, pfc_text, amy_text, amy_rx):
    ax, ay = amygdala
    return [
        f'<line x1="{dx + 70}" y1="{dy - 8}" x2="{dx + 72}" y2="{dy + 60}" stroke="{ink}" stroke-width="1"/>',
        text(dx + 70, dy - 14, pfc_text, "nc-map-gdp"),
        f'<line x1="{dx + ax}" y1="{dy + ay + amy_rx * 0.72:.0f}" x2="{dx + ax - 20}" y2="{dy + 330}" stroke="{ink}" stroke-width="1"/>',
        text(dx + ax - 20, dy + 346, amy_text, "nc-map-gdp"),
    ]


figures = {
    "synapse.svg": svg(1000, 470, "A strengthened synapse with many receptors next to a weakened synapse with few", [
        *synapse(260, 9, 22, 6, "USED A LOT", "long-term potentiation"),
        *synapse(740, 3, 4, 2, "RARELY USED", "long-term depression"),
        text(500, 205, "sending neuron", "nc-map-place"),
        text(500, 292, "signal crosses the gap", "nc-map-place"),
        text(500, 372, "receiving neuron", "nc-map-place"),
        text(260, 448, "more receptors, stronger signal", "nc-map-gdp"),
        text(740, 448, "fewer receptors, weaker signal", "nc-map-gdp"),
    ]),
    "stress-brain.svg": svg(1000, 520, "Calm brain versus chronically stressed brain, showing a larger amygdala and weaker prefrontal cortex under stress", [
        defs,
        text(250, 40, "CALM", "nc-map-country"),
        text(750, 40, "CHRONIC STRESS", "nc-map-country"),
        *brain(50, 105, pfc_fill=red, amy_rx=13, amy_fill=pink, arrow_w=6),
        *brain(550, 105, pfc_fill=pink, amy_rx=24, amy_fill=red, arrow_w=2),
        *labels(50, 105, "prefrontal cortex", "amygdala (deep inside)", 13),
        *labels(550, 105, "prefrontal cortex shrinks", "amygdala grows", 24),
        text(500, 500, "Schematic based on chronic stress studies in rats, drawn on a human brain. Arrow thickness shows how well the prefrontal cortex calms the amygdala.", "nc-map-place"),
    ]),
}

for name, content in figures.items():
    (out / name).write_text(content)
    print(out / name)
