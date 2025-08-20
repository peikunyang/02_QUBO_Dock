# QUBODock: A Pip-Installable QUBO Tool for Ligand Pose Generation

*A minimal, interoperable pose-generation tool that formulates ligand pose generation as a QUBO and runs on CPU or CUDA GPUs. QUBODock focuses on producing candidate poses; scoring/reranking is intentionally delegated to external software.*

- **PyPI**: `qubodock`
- **Scope**: pose generation only (no built-in scoring)
- **Paper**: *QUBODock: A Pip-Installable QUBO Tool for Ligand Pose Generation* (arXiv:2508.13014)

---

## Project layout

```
2_inp/
 ├─ 1_ori/
 │   └─ 1nc3.pdb                     # Original PDB from RCSB
 └─ 2_rec_lig/
     ├─ 1nc3_pro.pdb                 # Protein part split from 1nc3.pdb
     ├─ 1nc3_lig_exp.pdb             # Ligand part (experimental pose)
     ├─ cen                          # Helper: print ligand geometric center (cx cy cz)
     └─ shift                        # Helper: translate ligand to simulate unknown pocket

3_example/
 ├─ 1_gen_j_matrix/                  # Build sparse QUBO (J matrix) and grid points
 ├─ 2_qubo_solver/                   # Solve the QUBO
 ├─ 3_ligand_pose/                   # Enumerate rigid placements (rotation/translation)
 ├─ 4_rmsd/                          # RMSD vs. experimental ligand
 └─ 5_sel_poses/                     # Materialize a selected pose as PDB
```

---

## Installation (PyTorch already installed)

> QUBODock is on PyPI and requires Python ≥ 3.8. Since the built-in solvers use PyTorch, please install a CPU or CUDA build of **PyTorch** first. With PyTorch in place, install QUBODock with:

```bash
pip install -U qubodock
# (Recommended when multiple Python environments are present)
# python -m pip install -U qubodock
```

```bash
conda create -n qubodock python=3.10 -y
conda activate qubodock
python -m pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision
python -m pip install -U --no-deps "qubodock[gpu]"
```

Quick check:
```bash
qubodock-buildj --help
qubodock-solve  --help
qubodock-align --help
qubodock-rmsd  --help
qubodock-applyrt --help
```

---

## Minimal end-to-end example (`3_example/`)

> The commands below assume **bash** on Linux/macOS/WSL. On Windows PowerShell, remove the backslashes at line ends and use a single line or PowerShell backticks (`` ` ``). If you have a CUDA GPU, replace `--device auto` with `--device cuda`.

### 1) Build the J matrix and grid (`3_example/1_gen_j_matrix/`)

```bash
qubodock-buildj ../../2_inp/2_rec_lig/1nc3_pro.pdb \
  --center 55.743 39.264 20.669 \
  --radius 7.0 \
  --spacing 0.375 \
  --exclusion 1.5 \
  --dmin 0.7 --dmax 1.3 \
  --penalty 20.0 --reward -2.0 \
  --out j.txt \
  --points-out grid_points.txt
```

### 2) Solve the QUBO (`3_example/2_qubo_solver/`)

```bash
qubodock-solve ../1_gen_j_matrix/j.txt \
  --method sa --iters 2000000 --T0 1.0 --Tend 1e-3 \
  --device cuda \
  --density 0.5 --seed 0 \
  --out solution_bits.txt \
  --points ../1_gen_j_matrix/grid_points.txt \
  --active-out active_points.txt \
  --time-out my_solve_time.txt
```

### 3) Enumerate rigid placements (`3_example/3_ligand_pose/`)

```bash
qubodock-align ../../2_inp/2_rec_lig/shift/1nc3_lig_shi.pdb \
  ../2_qubo_solver/active_points.txt \
  ../../2_inp/2_rec_lig/1nc3_pro.pdb \
  --device cuda \
  --pair-tol 0.2 \
  --tri-tol 0.2 \
  --clash 1.0 \
  --placements-out ../3_ligand_pose/placements.txt \
  --time-out align_time.txt
```

### 4) Compute RMSD (`3_example/4_rmsd/`)

```bash
qubodock-rmsd ../3_ligand_pose/placements.txt \
  ../../2_inp/2_rec_lig/shift/1nc3_lig_shi.pdb \
  ../../2_inp/2_rec_lig/1nc3_lig_exp.pdb \
  --device cuda \
  --match-by name \
  --out placements_rmsd.txt
```

### 5) Materialize a selected pose (`3_example/5_sel_poses/`)

```bash
qubodock-applyrt ../../2_inp/2_rec_lig/shift/1nc3_lig_shi.pdb \
  ../4_rmsd/placements_rmsd.txt \
  --pose-index 0 \
  --device cpu \
  --out pose_0000.pdb
```

---

## Contact

**Pei-Kun Yang**  
E-mail: <peikun@isu.edu.tw>, <peikun6416@gmail.com>  
ORCID: <https://orcid.org/0000-0003-1840-6204>

---

## Citation

If this repository or QUBODock is useful in your research, please cite the following (at least the first paper):

1. **QUBODock: A Pip-Installable QUBO Tool for Ligand Pose Generation.** arXiv:2508.13014. DOI: 10.48550/arXiv.2508.13014.  
2. **Ligand Pose Generation via QUBO-Based Hotspot Sampling and Geometric Triplet Matching.** arXiv:2507.20304. DOI: 10.48550/arXiv.2507.20304.  
3. **Comparative Evaluation of PyTorch, JAX, SciPy, and Neal for Solving QUBO Problems at Scale.** arXiv:2507.17770. DOI: 10.48550/arXiv.2507.17770.

---

## License

This repository (examples and documentation) is released under the **MIT License** (see `LICENSE`).  
The QUBODock software itself is obtained from PyPI with `pip install qubodock`.
