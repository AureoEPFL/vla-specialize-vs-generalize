import os, csv

rows = []
with open(os.path.join("ros-vla-manip", "results", "loss.csv"), newline="") as f:
    for r in csv.DictReader(f):
        rows.append((int(r["step"]), float(r["loss"])))

W, H = 640, 360
left, right, top, bottom = 60, 620, 30, 300
xmin, xmax = min(s for s, _ in rows), max(s for s, _ in rows)
ymin, ymax = 0.0, 0.5

def X(s): return left + (s - xmin) / (xmax - xmin) * (right - left)
def Y(l): return bottom - (l - ymin) / (ymax - ymin) * (bottom - top)

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Arial, sans-serif">')
svg.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
svg.append(f'<text x="{left}" y="20" font-size="15" font-weight="bold" fill="#111111">Training loss (imitation learning)</text>')

svg.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#333333" stroke-width="1"/>')
svg.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#333333" stroke-width="1"/>')

for y in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]:
    yy = Y(y)
    svg.append(f'<line x1="{left}" y1="{yy}" x2="{right}" y2="{yy}" stroke="#e0e0e0" stroke-width="1"/>')
    svg.append(f'<text x="{left - 8}" y="{yy + 4}" font-size="10" fill="#666666" text-anchor="end">{y:.1f}</text>')

for s in range(0, 501, 100):
    xx = X(s)
    svg.append(f'<line x1="{xx}" y1="{top}" x2="{xx}" y2="{bottom}" stroke="#f0f0f0" stroke-width="1"/>')
    svg.append(f'<text x="{xx}" y="{bottom + 16}" font-size="10" fill="#666666" text-anchor="middle">{s}</text>')

svg.append(f'<text x="{right}" y="{bottom + 34}" font-size="10" fill="#666666" text-anchor="end">step</text>')

pts = " ".join(f"{X(s):.1f},{Y(l):.1f}" for s, l in rows)
svg.append(f'<polyline points="{pts}" fill="none" stroke="#1565c0" stroke-width="2"/>')
for s, l in rows:
    svg.append(f'<circle cx="{X(s):.1f}" cy="{Y(l):.1f}" r="2.5" fill="#1565c0"/>')

svg.append('</svg>')

out = os.path.join("ros-vla-manip", "results", "loss_curve.svg")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("written:", out)
