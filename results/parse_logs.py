import json, re, csv, os

def parse(path, out_csv, total):
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
                rows.append((int(steps[-1]), float(losses[-1])))
    d = {}
    for s, l in rows:
        d[s] = l
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["step", "loss"])
        for s in sorted(d):
            w.writerow([s, d[s]])
    print(out_csv, "->", len(d), "points, step range", (min(d), max(d)) if d else None)

base = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(base)
src = os.path.join(root, "..", "_losssrc")

parse(os.path.join(src, "m1", "ros-vla-manip-metaworld.log"), os.path.join(base, "loss_m1.csv"), 2000)
parse(os.path.join(src, "m2", "ros-vla-manip-m2-train.log"), os.path.join(base, "loss_m2.csv"), 6000)
