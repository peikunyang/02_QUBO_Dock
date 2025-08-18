import sys

file = sys.argv[1]
xs, ys, zs = [], [], []

with open(file) as f:
    for line in f:
        if line.startswith(("ATOM", "HETATM")):
            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
            except:
                parts = line.split()
                try:
                    x, y, z = map(float, parts[6:9])
                except:
                    continue
            xs.append(x)
            ys.append(y)
            zs.append(z)

cx = sum(xs) / len(xs)
cy = sum(ys) / len(ys)
cz = sum(zs) / len(zs)

print(f"center_x = {cx:.3f}")
print(f"center_y = {cy:.3f}")
print(f"center_z = {cz:.3f}")

