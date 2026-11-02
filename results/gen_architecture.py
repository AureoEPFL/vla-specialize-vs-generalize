import os

W, H = 960, 340
svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Arial, sans-serif">')
svg.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
svg.append(f'<text x="480" y="26" font-size="16" font-weight="bold" fill="#111111" text-anchor="middle">SmolVLA architecture</text>')

# legend
svg.append(f'<rect x="700" y="8" width="14" height="10" fill="#dbe7f6" stroke="#4a7bbd"/>')
svg.append(f'<text x="718" y="17" font-size="11" fill="#444444">frozen</text>')
svg.append(f'<rect x="780" y="8" width="14" height="10" fill="#fde8d0" stroke="#c47a1a"/>')
svg.append(f'<text x="798" y="17" font-size="11" fill="#444444">trained</text>')

def box(x, y, w, h, title, lines, fill, stroke):
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    ty = y + 20
    svg.append(f'<text x="{x + w/2}" y="{ty}" font-size="13" font-weight="bold" fill="#111111" text-anchor="middle">{title}</text>')
    ty += 16
    for ln in lines:
        svg.append(f'<text x="{x + w/2}" y="{ty}" font-size="10.5" fill="#444444" text-anchor="middle">{ln}</text>')
        ty += 14

def arrow(x1, y1, x2, y2, color="#888888"):
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.6"/>')
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    for d in (-150, 150):
        a = ang + math.radians(d)
        svg.append(f'<line x1="{x2}" y1="{y2}" x2="{x2 - 9*math.cos(a):.1f}" y2="{y2 - 9*math.sin(a):.1f}" stroke="{color}" stroke-width="1.6"/>')

# inputs (left)
inputs = [("RGB image", 60, "#333333"), ("language instruction", 170, "#333333"), ("robot state", 270, "#333333")]
for label, y, c in inputs:
    svg.append(f'<text x="30" y="{y+4}" font-size="12" fill="{c}" text-anchor="start">{label}</text>')

# vision encoder (frozen)
box(150, 40, 150, 60, "Vision encoder", ["SigLIP", "64 visual tokens"], "#dbe7f6", "#4a7bbd")
# language decoder (frozen)
box(360, 110, 180, 90, "Language decoder", ["SmolLM2 · 16 layers", "visual + text + state", "tokens merged"], "#dbe7f6", "#4a7bbd")
# action expert (trained)
box(610, 110, 180, 90, "Action expert", ["flow-matching", "transformer (~100M)", "interleaved CA / SA"], "#fde8d0", "#c47a1a")
# output
box(850, 125, 90, 60, "action chunk", ["[a_t … a_t+49]", "50 steps · 4-D"], "#eef7e8", "#4f8a3d")

# arrows
arrow(190, 100, 150+75, 100, "#4a7bbd")  # image -> vision encoder (approx)
arrow(185, 170, 360, 155, "#888888")      # vision -> decoder
arrow(540, 155, 610, 140, "#888888")      # decoder -> expert
arrow(790, 155, 850, 152, "#4f8a3d")      # expert -> output
arrow(150, 170, 360, 165, "#888888")      # instruction -> decoder
arrow(150, 270, 360, 175, "#888888")      # state -> decoder

svg.append(f'<text x="480" y="320" font-size="11" fill="#666666" text-anchor="middle">Only the action expert is trained; the vision encoder and language decoder are frozen.</text>')
svg.append('</svg>')

out = os.path.join("ros-vla-manip", "results", "architecture.svg")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("written:", out)
