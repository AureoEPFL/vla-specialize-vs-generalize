import os, csv

base = os.path.dirname(os.path.abspath(__file__))

def load(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append((int(r["step"]), float(r["loss"])))
    return rows

m1 = load(os.path.join(base, "loss_m1.csv"))
m2 = load(os.path.join(base, "loss_m2.csv"))

all_steps = [s for s, _ in m1] + [s for s, _ in m2]
all_loss = [l for _, l in m1] + [l for _, l in m2]

W, H = 720, 400
left, right, top, bottom = 70, 690, 40, 330
xmin, xmax = 0, max(all_steps)
ymin, ymax = 0.0, 2.0

def X(s): return left + (s - xmin) / (xmax - xmin) * (right - left)
def Y(l): return bottom - (l - ymin) / (ymax - ymin) * (bottom - top)

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Arial, sans-serif">')
svg.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
svg.append(f'<text x="{left}" y="24" font-size="15" font-weight="bold" fill="#111111">Training loss: M1 (MT50, 2000 steps) vs M2 (4 tasks, 6000 steps)</text>')

svg.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#333333" stroke-width="1"/>')
svg.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#333333" stroke-width="1"/>')

for y in [0.0, 0.5, 1.0, 1.5, 2.0]:
    yy = Y(y)
    svg.append(f'<line x1="{left}" y1="{yy}" x2="{right}" y2="{yy}" stroke="#e8e8e8" stroke-width="1"/>')
    svg.append(f'<text x="{left - 8}" y="{yy + 4}" font-size="10" fill="#666666" text-anchor="end">{y:.1f}</text>')

for s in range(0, 6001, 1000):
    xx = X(s)
    svg.append(f'<line x1="{xx}" y1="{top}" x2="{xx}" y2="{bottom}" stroke="#f2f2f2" stroke-width="1"/>')
    svg.append(f'<text x="{xx}" y="{bottom + 16}" font-size="10" fill="#666666" text-anchor="middle">{s}</text>')
svg.append(f'<text x="{right}" y="{bottom + 34}" font-size="10" fill="#666666" text-anchor="end">training step</text>')

def poly(rows, color):
    pts = " ".join(f"{X(s):.1f},{Y(l):.1f}" for s, l in rows)
    svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"/>')
    for s, l in rows:
        svg.append(f'<circle cx="{X(s):.1f}" cy="{Y(l):.1f}" r="1.8" fill="{color}"/>')

poly(m1, "#ef6c00")
poly(m2, "#1565c0")

svg.append(f'<rect x="{left}" y="{top - 22}" width="14" height="10" fill="#ef6c00" rx="2"/>')
svg.append(f'<text x="{left + 18}" y="{top - 13}" font-size="11" fill="#444444">M1 (multi-task, 2000 steps)</text>')
svg.append(f'<rect x="{left + 190}" y="{top - 22}" width="14" height="10" fill="#1565c0" rx="2"/>')
svg.append(f'<text x="{left + 208}" y="{top - 13}" font-size="11" fill="#444444">M2 (specialized, 6000 steps)</text>')

svg.append(f'<text x="{left}" y="{H - 8}" font-size="10" fill="#777777">Values extracted from the Kaggle training logs (step, loss).</text>')
svg.append('</svg>')

out = os.path.join(base, "loss_curves.svg")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("written:", out)
