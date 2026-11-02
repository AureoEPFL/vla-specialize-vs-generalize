import os

# (task, difficulty, m0, m1, m2)  M0 == M1 by construction (identical results)
tasks = [
    ("door-close-v3", "easy", 100, 100, 0),
    ("button-press-topdown-v3", "easy", 80, 80, 0),
    ("reach-v3", "easy", 30, 30, 20),
    ("basketball-v3", "medium", 20, 20, 40),
    ("bin-picking-v3", "medium", 20, 20, 60),
    ("sweep-v3", "medium", 10, 10, 0),
    ("coffee-push-v3", "medium", 0, 0, 0),
    ("pick-place-v3", "hard", 20, 20, 10),
    ("push-v3", "hard", 20, 20, 70),
    ("assembly-v3", "hard", 0, 0, 0),
    ("shelf-place-v3", "very-hard", 10, 10, 0),
    ("disassemble-v3", "very-hard", 10, 10, 0),
]

W, H = 980, 760
left = 240
plot_right = 920
top = 78
bar_h = 10
bar_gap = 2
row_gap = 12
x_scale = (plot_right - left) / 100.0

n = len(tasks)
row_h = 3 * bar_h + 2 * bar_gap
plot_height = n * row_h + (n - 1) * row_gap
bottom = top + plot_height

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Arial, sans-serif">')
svg.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
svg.append(f'<text x="{left}" y="34" font-size="19" font-weight="bold" fill="#111111">Success rate per task: M0 (base), M1 (MT50 fine-tune), M2 (specialized)</text>')

# legend
legend = [("#9e9e9e", "M0 (base)"), ("#ef6c00", "M1 (multi-task)"), ("#1565c0", "M2 (specialized)")]
lx = left
for color, label in legend:
    svg.append(f'<rect x="{lx}" y="48" width="14" height="10" fill="{color}" rx="2"/>')
    svg.append(f'<text x="{lx + 18}" y="57" font-size="11" fill="#555555">{label}</text>')
    lx += 120

for v in [0, 25, 50, 75, 100]:
    x = left + v * x_scale
    svg.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" stroke="#e0e0e0" stroke-width="1"/>')
    svg.append(f'<text x="{x}" y="{bottom + 18}" font-size="11" fill="#666666" text-anchor="middle">{v}%</text>')

colors = ["#9e9e9e", "#ef6c00", "#1565c0"]

for i, (name, diff, m0, m1, m2) in enumerate(tasks):
    y = top + i * (row_h + row_gap)
    svg.append(f'<text x="{left - 10}" y="{y + row_h/2 + 4}" font-size="12" fill="#333333" text-anchor="end">{name}</text>')
    for j, val in enumerate([m0, m1, m2]):
        by = y + j * (bar_h + bar_gap)
        w = val * x_scale
        svg.append(f'<rect x="{left}" y="{by}" width="{plot_right - left}" height="{bar_h}" fill="#f4f4f4" rx="2"/>')
        if w > 0.5:
            svg.append(f'<rect x="{left}" y="{by}" width="{w:.1f}" height="{bar_h}" fill="{colors[j]}" rx="2"/>')
        svg.append(f'<text x="{left + w + 4}" y="{by + bar_h - 1}" font-size="9" fill="#444444">{val}%</text>')

svg.append('</svg>')

out = os.path.join("ros-vla-manip", "results", "success_rate.svg")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("written:", out)
