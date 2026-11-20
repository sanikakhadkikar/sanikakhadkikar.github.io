"""Draw the newsprint-style world map of Mo-99 reactors for the Holy Moly post.

Usage: python scripts/make_mo99_map.py ne_110m_admin_0_countries.geojson
Boundaries: Natural Earth 1:110m (public domain).
Reactors: OECD NEA (2025), Current Trends in the Supply and Utilisation of Medical Radioisotopes, Tables 2 and 3.
"""
import json
import sys
from pathlib import Path

out = Path(__file__).resolve().parent.parent / "content/caricature/holy-moly/reactors.svg"
countries = json.load(open(sys.argv[1]))["features"]

ink, paper, red, pink, grey, water = "#1b1a17", "#f4efe4", "#c8102e", "#eab3ba", "#b9b09d", "#d5dcdc"
lon_min, lon_max, lat_min, lat_max = -170, 190, -56, 75
W = 1000
s = W / (lon_max - lon_min)
H = round((lat_max - lat_min) * s)


def xy(lon, lat):
    if lon < lon_min:
        lon += 360
    return (lon - lon_min) * s, (lat_max - lat) * s


def path(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    d = []
    for poly in polys:
        for ring in poly:
            pts = [xy(*p) for p in ring]
            d.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    return "".join(d)


producers = {"BEL", "NLD", "CZE", "POL", "ZAF", "AUS"}
current = [  # name, lon, lat
    ("BR2", 5.10, 51.19), ("HFR", 4.67, 52.79), ("LVR-15", 14.36, 50.18), ("MARIA", 21.36, 52.10),
    ("SAFARI-1", 27.92, -25.80), ("OPAL", 150.98, -34.05),
]
planned = [
    ("SHINE, USA (accelerator)", -89.02, 42.68, "end", -10, 4),
    ("Darlington, Canada", -78.72, 43.87, "start", 10, -6),
    ("RA-10, Argentina", -58.52, -34.85, "start", 10, 4),
    ("JHR, France", 5.76, 43.69, "end", -10, 14),
]

b = [f'<svg class="nc-map" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
     f'aria-label="World map of the six research reactors that make about 95 percent of the world\'s molybdenum-99">',
     f'<rect width="{W}" height="{H}" fill="{water}"/>']
for f in countries:
    iso = f["properties"]["ADM0_A3"]
    if iso == "ATA":
        continue
    fill = pink if iso in producers else paper
    b.append(f'<path d="{path(f["geometry"])}" fill="{fill}" stroke="{grey if fill == paper else ink}" stroke-width="{0.6 if fill == paper else 1}"/>')

for name, lon, lat, anchor, dx, dy in planned:
    x, y = xy(lon, lat)
    b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{paper}" stroke="{red}" stroke-width="2"/>')
    b.append(f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}" class="nc-map-place">{name}</text>')

for name, lon, lat in current:
    x, y = xy(lon, lat)
    b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{red}" stroke="{paper}" stroke-width="1.5"/>')

# labels: one callout for the European cluster, direct labels for the others
ex, ey = xy(21.36, 52.10)
tx, ty = xy(42, 63)
b.append(f'<line x1="{ex + 6:.1f}" y1="{ey - 4:.1f}" x2="{tx - 4:.1f}" y2="{ty + 2:.1f}" stroke="{ink}" stroke-width="1"/>')
b.append(f'<text x="{tx:.1f}" y="{ty:.1f}" class="nc-map-gdp">BR2, HFR, LVR-15, MARIA</text>')
b.append(f'<text x="{tx:.1f}" y="{ty + 15:.1f}" class="nc-map-place">Belgium, Netherlands, Czechia, Poland</text>')
x, y = xy(27.92, -25.80)
b.append(f'<text x="{x + 10:.1f}" y="{y + 4:.1f}" class="nc-map-gdp">SAFARI-1</text>')
b.append(f'<text x="{x + 10:.1f}" y="{y + 19:.1f}" class="nc-map-place">South Africa</text>')
x, y = xy(150.98, -34.05)
b.append(f'<text x="{x - 10:.1f}" y="{y - 8:.1f}" text-anchor="end" class="nc-map-gdp">OPAL</text>')
b.append(f'<text x="{x - 10:.1f}" y="{y + 7:.1f}" text-anchor="end" class="nc-map-place">Australia</text>')

# legend
lx, ly = 16, H - 108
b.append(f'<rect x="{lx - 6}" y="{ly - 16}" width="230" height="52" fill="{paper}" stroke="{ink}" stroke-width="1"/>')
b.append(f'<circle cx="{lx + 6}" cy="{ly}" r="6" fill="{red}"/>')
b.append(f'<text x="{lx + 18}" y="{ly + 4}" class="nc-map-place">Main reactors, about 95% of supply</text>')
b.append(f'<circle cx="{lx + 6}" cy="{ly + 22}" r="5" fill="{paper}" stroke="{red}" stroke-width="2"/>')
b.append(f'<text x="{lx + 18}" y="{ly + 26}" class="nc-map-place">Planned or starting up</text>')
b.append(f'<rect width="{W}" height="{H}" fill="none" stroke="{ink}" stroke-width="3"/>')
b.append("</svg>")
out.write_text("\n".join(b))
print(out, W, H)
