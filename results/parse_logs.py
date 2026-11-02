import json, re, csv, os

def parse(path, total, offset=0):
    rows = []
    with open(path, "r", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(","):
                line = line[1:]
            try:
                obj = json.loads(line)
            except Exception:
                continue
            data = obj.get("data", "")
            if "loss:" not in data:
                continue
            steps = re.findall(r"(\d+)/" + str(total), data)
            losses = re.findall(r"loss:([0-9]*\.?[0-9]+)", data)
            if steps and losses:
                rows.append((int(steps[-1]) + offset, float(losses[-1])))
    return rows

def write(rows, out_csv):
    d = {}
    for s, l in rows:
        d[s] = l
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["step", "loss"])
        for s in sorted(d):
            w.writerow([s, d[s]])
    print(out_csv, "->", len(d), "points, range", (min(d), max(d)) if d else None)

base = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(base)
src = os.path.join(root, "..", "_pickplace")

part1 = parse(os.path.join(src, "ros-vla-manip-pickplace", "ros-vla-manip-pickplace.log"), 10000, 0)
part2 = parse(os.path.join(src, "ros-vla-manip-pickplace-resume", "ros-vla-manip-pickplace-resume.log"), 2000, 8000)
print("part1", len(part1), "part2", len(part2))
write(part1 + part2, os.path.join(base, "loss_m1.csv"))
