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

Quick check:
```bash
qubodock-buildj --help
qubodock-solve  --help
```

---

## Minimal end-to-end example (`3_example/`)

> The commands below assume **bash** on Linux/macOS/WSL. On Windows PowerShell, remove the backslashes at line ends and use a single line or PowerShell backticks (`` ` ``). If you have a CUDA GPU, replace `--device auto` with `--device cuda`.

### 1) Build the J matrix and grid (`3_example/1_gen_j_matrix/`)

Option A — compute the ligand center with the helper and feed it into `qubodock-buildj`:
```bash
2_inp/2_rec_lig/cen 2_inp/2_rec_lig/1nc3_lig_exp.pdb > center.txt
CX=$(awk '{print $1}' center.txt); CY=$(awk '{print $2}' center.txt); CZ=$(awk '{print $3}' center.txt)

qubodock-buildj 2_inp/2_rec_lig/1nc3_pro.pdb   --center $CX $CY $CZ --radius 8.0 --spacing 0.4   --exclusion 1.6 --dmin 0.7 --dmax 1.3   --out 3_example/1_gen_j_matrix/j.txt   --points-out 3_example/1_gen_j_matrix/grid_points.txt
```

Option B — if you already know a pocket center, specify it directly:
```bash
qubodock-buildj 2_inp/2_rec_lig/1nc3_pro.pdb   --center 11.0 28.5 17.2 --radius 8.0 --spacing 0.4   --exclusion 1.6 --dmin 0.7 --dmax 1.3   --out 3_example/1_gen_j_matrix/j.txt   --points-out 3_example/1_gen_j_matrix/grid_points.txt
```

**Notes.** `--spacing` controls the initial grid density. `--exclusion` prunes points too close to protein atoms. The distance window `[d_min, d_max]` shapes the near-uniform selection encouraged by the QUBO.

### 2) Solve the QUBO (`3_example/2_qubo_solver/`)

```bash
qubodock-solve 3_example/1_gen_j_matrix/j.txt   --method sa --iters 200000 --T0 1.0 --Tend 1e-3   --device auto --seed 0   --out 3_example/2_qubo_solver/solution_bits.txt   --points 3_example/1_gen_j_matrix/grid_points.txt   --active-out 3_example/2_qubo_solver/active_points.txt   --time-out 3_example/2_qubo_solver/solve_time.txt
```

Tip: start with a smaller `--iters` to validate parameters, then increase for quality.

### 3) Enumerate rigid placements (`3_example/3_ligand_pose/`)

```bash
qubodock-align 2_inp/2_rec_lig/1nc3_lig_exp.pdb   3_example/2_qubo_solver/active_points.txt   2_inp/2_rec_lig/1nc3_pro.pdb   --pair-tol 0.3 --tri-tol 0.3 --clash 1.6   --device auto   --placements-out 3_example/3_ligand_pose/placements.txt   --save-poses 3_example/3_ligand_pose/poses.pdb
```

### 4) Compute RMSD (`3_example/4_rmsd/`)

```bash
qubodock-rmsd 3_example/3_ligand_pose/placements.txt   2_inp/2_rec_lig/1nc3_lig_exp.pdb   2_inp/2_rec_lig/1nc3_lig_exp.pdb   --out 3_example/4_rmsd/placements_rmsd.txt
```

> If you used the `shift` helper to move the ligand, replace the second path with the shifted ligand PDB.

### 5) Materialize a selected pose (`3_example/5_sel_poses/`)

```bash
# Example: export the first candidate pose (index 0)
qubodock-applyrt 2_inp/2_rec_lig/1nc3_lig_exp.pdb   3_example/3_ligand_pose/placements.txt   --pose-index 0   --out 3_example/5_sel_poses/pose_0.pdb
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

**BibTeX**
```bibtex
@misc{yang_qubodock_2025,
  title={QUBODock: A Pip-Installable QUBO Tool for Ligand Pose Generation},
  author={Pei-Kun Yang},
  year={2025},
  eprint={2508.13014},
  archivePrefix={arXiv},
  primaryClass={q-bio.BM},
  doi={10.48550/arXiv.2508.13014}
}

@misc{yang_hotspot_triplet_2025,
  title={Ligand Pose Generation via QUBO-Based Hotspot Sampling and Geometric Triplet Matching},
  author={Pei-Kun Yang},
  year={2025},
  eprint={2507.20304},
  archivePrefix={arXiv},
  primaryClass={q-bio.BM},
  doi={10.48550/arXiv.2507.20304}
}

@misc{yang_qubo_solvers_eval_2025,
  title={Comparative Evaluation of PyTorch, JAX, SciPy, and Neal for Solving QUBO Problems at Scale},
  author={Pei-Kun Yang},
  year={2025},
  eprint={2507.17770},
  archivePrefix={arXiv},
  primaryClass={cs.DC},
  doi={10.48550/arXiv.2507.17770}
}
```

---

## License

This repository (examples and documentation) is released under the **MIT License** (see `LICENSE`).  
The QUBODock software itself is obtained from PyPI with `pip install qubodock`.
