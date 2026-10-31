"""Draw the newsprint-style Central Asia map for the Kazakhstan post.

Usage: python scripts/make_central_asia_map.py ne_50m_admin_0_countries.geojson
Boundaries: Natural Earth 1:50m (public domain). GDP per capita from data/asia_gdp.json.
"""
import json
import math
import sys
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
out = repo / "content/not-cringe/kazakhstan/map.svg"

countries = json.load(open(sys.argv[1]))["features"]
gdp = {r["country"]: r["gdp_pc"] for r in json.load(open(repo / "data/asia_gdp.json"))["rows"]}

mentioned = {
    "KAZ": "Kazakhstan", "CHN": "China", "TKM": "Turkmenistan", "IRN": "Iran",
    "UZB": "Uzbekistan", "KGZ": "Kyrgyzstan", "TJK": "Tajikistan", "AFG": "Afghanistan",
}

lon_min, lon_max, lat_min, lat_max = 43, 112, 24, 56
width = 1000
k = math.cos(math.radians(40))
scale = width / ((lon_max - lon_min) * k)
height = round((lat_max - lat_min) * scale)


def xy(lon, lat):
    return (lon - lon_min) * k * scale, (lat_max - lat) * scale


def path(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    d = []
    for poly in polys:
        for ring in poly:
            lons = [p[0] for p in ring]
            lats = [p[1] for p in ring]
            if max(lons) < lon_min - 5 or min(lons) > lon_max + 5 or max(lats) < lat_min - 5 or min(lats) > lat_max + 5:
                continue
            pts = []
            for p in ring:
                x, y = xy(*p)
                # drop points under a pixel apart
                if not pts or abs(x - pts[-1][0]) + abs(y - pts[-1][1]) > 1:
                    pts.append((x, y))
            if len(pts) > 2:
                d.append("M" + "L".join(f"{x:.0f},{y:.0f}" for x, y in pts) + "Z")
    return "".join(d)


def fill(name):
    # deeper red = higher GDP per capita
    v = gdp[name]
    t = math.log(v / 400) / math.log(16000 / 400)
    a = 0.12 + 0.75 * max(0, min(1, t))
    paper_rgb, red_rgb = (244, 239, 228), (200, 16, 46)
    return "#" + "".join(f"{round(p + (r - p) * a):02x}" for p, r in zip(paper_rgb, red_rgb))


ink, paper, water = "#1b1a17", "#f4efe4", "#d5dcdc"
svg = [
    f'<svg class="nc-map" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" '
    f'aria-label="Map of Kazakhstan, its Central Asian neighbours, Iran, Afghanistan and western China">',
    f'<rect width="{width}" height="{height}" fill="{water}"/>',
]

for f in countries:
    iso = f["properties"]["ADM0_A3"]
    if iso in mentioned:
        continue
    d = path(f["geometry"])
    if d:
        svg.append(f'<path d="{d}" fill="{paper}" stroke="#b9b09d" stroke-width="0.8"/>')
for f in countries:
    iso = f["properties"]["ADM0_A3"]
    if iso in mentioned:
        svg.append(f'<path d="{path(f["geometry"])}" fill="{fill(mentioned[iso])}" stroke="{ink}" stroke-width="1.4"/>')

svg.append(f'<text x="{width - 14}" y="{height - 14}" text-anchor="end" class="nc-map-place">• oil and gas fields from the article</text>')

# Places from the article
places = [
    (53.4, 46.1, "Tengiz"),
    (51.6, 46.3, "Kashagan"),
    (53.3, 51.1, "Karachaganak"),
    (62.3, 37.3, "Galkynysh"),
]
for lon, lat, name in places:
    x, y = xy(lon, lat)
    left = name == "Kashagan"
    svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{ink}" stroke="{paper}" stroke-width="1.5"/>')
    svg.append(f'<text x="{x - 8 if left else x + 8:.1f}" y="{y + 4:.1f}" text-anchor="{"end" if left else "start"}" class="nc-map-place">{name}</text>')

x, y = xy(71.6, 40.8)
svg.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="26" ry="9" fill="none" stroke="{ink}" stroke-width="1.5" stroke-dasharray="4 3"/>')
svg.append(f'<text x="{x:.1f}" y="{y - 14:.1f}" text-anchor="middle" class="nc-map-place">Fergana Valley</text>')

x, y = xy(48.5, 42.5)
svg.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" class="nc-map-sea">Caspian</text>')
svg.append(f'<text x="{x:.1f}" y="{y + 16:.1f}" text-anchor="middle" class="nc-map-sea">Sea</text>')

# Country labels: (anchor lon, lat) and optional label offset for small countries
labels = {
    "Kazakhstan": (67, 48.3, None),
    "China": (96, 34.5, None),
    "Turkmenistan": (59, 39.3, None),
    "Iran": (54.5, 32.2, None),
    "Uzbekistan": (64, 42.3, None),
    "Afghanistan": (65.5, 33.6, None),
    "Kyrgyzstan": (75.5, 41.4, (79.5, 39.2)),
    "Tajikistan": (71, 38.6, (73.2, 35.4)),
}
for name, (lon, lat, off) in labels.items():
    ax, ay = xy(lon, lat)
    if off:
        lx, ly = xy(*off)
        svg.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{lx - 3:.1f}" y2="{ly - 5:.1f}" stroke="{ink}" stroke-width="1"/>')
        anchor = "start"
    else:
        lx, ly = ax, ay
        anchor = "middle"
    svg.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" class="nc-map-country">{name.upper()}</text>')
    svg.append(f'<text x="{lx:.1f}" y="{ly + 17:.1f}" text-anchor="{anchor}" class="nc-map-gdp">${gdp[name]:,}</text>')

svg.append(f'<rect width="{width}" height="{height}" fill="none" stroke="{ink}" stroke-width="3"/>')
svg.append("</svg>")
out.write_text("\n".join(svg))
print(out, width, height)
