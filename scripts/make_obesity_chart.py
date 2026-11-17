"""Draw the newsprint-style adult obesity chart for the Nauru post.

Usage: python scripts/make_obesity_chart.py
Data: World Obesity Federation ranking of adult obesity (BMI 30 or more), men and women combined,
based on NCD-RisC estimates. https://data.worldobesity.org/tables/ranking-obesity-by-country-adults-1.pdf
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out = Path(__file__).resolve().parent.parent / "content/caricature/nauru/obesity.png"

ink, paper, red, pink, grey, muted = "#1b1a17", "#f4efe4", "#c8102e", "#eab3ba", "#b9b09d", "#5d574c"

pacific = [
    ("American Samoa*", 76.84), ("Tonga", 75.08), ("Cook Islands", 73.59), ("Nauru", 72.99),
    ("Tokelau*", 72.12), ("Niue", 68.13), ("Tuvalu", 66.43), ("Samoa", 65.90),
    ("French Polynesia*", 50.24), ("Micronesia", 49.96), ("Kiribati", 46.94),
    ("Marshall Islands", 43.43), ("Palau", 41.62), ("Fiji", 40.24),
]
others = [("United States", 41.73), ("New Zealand", 34.70), ("Australia", 31.36), ("India", 8.28), ("Japan", 5.92)]

rows = pacific + [("", None)] + others
plt.rcParams.update({"font.family": "DejaVu Serif"})
fig, ax = plt.subplots(figsize=(8, 7.2), dpi=200)
fig.patch.set_facecolor(paper)
ax.set_facecolor(paper)

for i, (name, v) in enumerate(rows):
    y = len(rows) - 1 - i
    if v is None:
        continue
    color = red if name == "Nauru" else (pink if (name, v) in pacific else grey)
    ax.barh(y, v, height=0.72, color=color, edgecolor=paper, linewidth=1)
    ax.text(v + 1, y, f"{v:.0f}%", va="center", ha="left", fontsize=9, color=ink,
            fontweight="bold" if name == "Nauru" else "normal")
    ax.text(-1.5, y, name, va="center", ha="right", fontsize=9.5, color=ink,
            fontweight="bold" if name == "Nauru" else "normal")

ax.set_xlim(0, 85)
ax.set_ylim(-0.7, len(rows) - 0.3)
ax.set_yticks([])
ax.set_xticks([0, 20, 40, 60, 80])
ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%"], fontsize=8.5, color=muted)
ax.tick_params(axis="x", length=0)
ax.xaxis.grid(True, color=grey, linewidth=0.5, alpha=0.6)
ax.set_axisbelow(True)
for s in ax.spines.values():
    s.set_visible(False)

fig.text(0.02, 0.965, "Share of adults living with obesity", fontsize=13, fontweight="bold", color=ink)
fig.text(0.02, 0.935, "Pacific island nations in pink, Nauru in red, other countries in grey", fontsize=9, color=muted)
fig.text(0.02, 0.015, "* Territories, not independent countries. Source: World Obesity Federation, based on NCD-RisC estimates.",
         fontsize=7.5, color=muted)
plt.subplots_adjust(left=0.22, right=0.96, top=0.91, bottom=0.07)
fig.savefig(out, facecolor=paper)
print(out)
