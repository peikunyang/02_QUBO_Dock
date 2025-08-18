import sys

if len(sys.argv) != 6:
    print("用法: python translate_back.py input.pdbqt output.pdbqt dx dy dz")
    sys.exit(1)

inp, outp = sys.argv[1], sys.argv[2]
dx, dy, dz = map(float, sys.argv[3:6])

with open(inp) as fin, open(outp, "w") as fout:
    for line in fin:
        if line.startswith(("ATOM", "HETATM")):
            try:
                x = float(line[30:38]) - dx
                y = float(line[38:46]) - dy
                z = float(line[46:54]) - dz
                line = f"{line[:30]}{x:8.3f}{y:8.3f}{z:8.3f}{line[54:]}"
            except:
                parts = line.split()
                if len(parts) >= 9:
                    parts[6] = f"{float(parts[6]) - dx:.3f}"
                    parts[7] = f"{float(parts[7]) - dy:.3f}"
                    parts[8] = f"{float(parts[8]) - dz:.3f}"
                    line = " ".join(parts) + "\n"
        fout.write(line)

