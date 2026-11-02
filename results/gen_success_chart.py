import os

# (task, difficulty, m0_m1, m2)
tasks = [
    ("door-close-v3", "easy", 100, 0),
    ("button-press-topdown-v3", "easy", 80, 0),
    ("reach-v3", "easy", 30, 20),
    ("basketball-v3", "medium", 20, 40),
    ("bin-picking-v3", "medium", 20, 60),
    ("sweep-v3", "medium", 10, 0),
    ("coffee-push-v3", "medium", 0, 0),
    ("pick-place-v3", "hard", 20, 10),
    ("push-v3", "hard", 20, 70),
    ("assembly-v3", "hard", 0, 0),
    ("shelf-place-v3", "very-hard", 10, 0),
    ("disassemble-v3", "very-hard", 10, 0),
]

W, H = 960, 700
left = 235
plot_right = 900
top = 70
bar_h = 14
bar_gap = 4
row_gap = 14
x_scale = (plot_right - left) / 100.0

n = len(tasks)
row_h = 2 * bar_h + bar_gap
plot_height = n * row_h + (n - 1) * row_gap
bottom = top + plot_height

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Arial, sans-serif">')
svg.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
svg.append(f'<text x="{left}" y="38" font-size="19" font-weight="bold" fill="#111111">Success rate by task: M0/M1 (multi-task) vs M2 (specialized on 4 tasks)</text>')

svg.append(f'<rect x="{left}" y="46" width="14" height="10" fill="#9e9e9e" rx="2"/>')
svg.append(f'<text x="{left + 18}" y="55" font-size="11" fill="#555555">M0 / M1</text>')
svg.append(f'<rect x="{left + 90}" y="46" width="14" height="10" fill="#1565c0" rx="2"/>')
svg.append(f'<text x="{left + 108}" y="55" font-size="11" fill="#555555">M2 (specialized)</text>')

for v in [0, 25, 50, 75, 100]:
    x = left + v * x_scale
    svg.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" stroke="#e0e0e0" stroke-width="1"/>')
    svg.append(f'<text x="{x}" y="{bottom + 18}" font-size="11" fill="#666666" text-anchor="middle">{v}%</text>')

for i, (name, diff, m01, m2) in enumerate(tasks):
    y = top + i * (row_h + row_gap)
    svg.append(f'<text x="{left - 10}" y="{y + row_h/2 + 4}" font-size="12" fill="#333333" text-anchor="end">{name}</text>')
    w1 = m01 * x_scale
    svg.append(f'<rect x="{left}" y="{y}" width="{plot_right - left}" height="{bar_h}" fill="#f2f2f2" rx="2"/>')
    if w1 > 0.5:
        svg.append(f'<rect x="{left}" y="{y}" width="{w1:.1f}" height="{bar_h}" fill="#9e9e9e" rx="2"/>')
    svg.append(f'<text x="{left + w1 + 5}" y="{y + bar_h - 2}" font-size="10" fill="#555555">{m01}%</text>')
    y2 = y + bar_h + bar_gap
    w2 = m2 * x_scale
    svg.append(f'<rect x="{left}" y="{y2}" width="{plot_right - left}" height="{bar_h}" fill="#f2f2f2" rx="2"/>')
    if w2 > 0.5:
        svg.append(f'<rect x="{left}" y="{y2}" width="{w2:.1f}" height="{bar_h}" fill="#1565c0" rx="2"/>')
    svg.append(f'<text x="{left + w2 + 5}" y="{y2 + bar_h - 2}" font-size="10" fill="#333333">{m2}%</text>')

svg.append('</svg>')

out = os.path.join("ros-vla-manip", "results", "success_rate.svg")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("written:", out)
