# QUBODock Documentation

QUBODock is a pip-installable QUBO tool for ligand pose generation (pose generation only). It builds a sparse QUBO from a protein pocket region, solves it on CPU or CUDA GPUs, and decodes the selected points into rigid ligand placements. Scoring/reranking is intentionally delegated to external software.

## Install

```bash
pip install -U qubodock
```
> Requires Python ≥ 3.8 and a CPU or CUDA build of PyTorch already installed.

## Quick start

```bash
# 1) Build J and grid points (example center/radius/spacing)
qubodock-buildj protein.pdb --center 0 0 0 --radius 8 --spacing 0.4   --exclusion 1.6 --dmin 0.7 --dmax 1.3   --out j.txt --points-out grid_points.txt

# 2) Solve the QUBO (sa or greedy)
qubodock-solve j.txt --method greedy --device auto   --points grid_points.txt --active-out active_points.txt

# 3) Decode placements and optionally save poses
qubodock-align ligand.pdb active_points.txt protein.pdb   --pair-tol 0.3 --tri-tol 0.3 --clash 1.6   --placements-out placements.txt --save-poses poses.pdb
```

## Inputs and outputs

- **Inputs**: protein PDB, ligand PDB, region parameters (center, radius, spacing).  
- **Outputs**: `j.txt` (QUBO), `grid_points.txt`, `solution_bits.txt`, `active_points.txt`, `placements.txt`, and optional pose PDBs.

## Links

- PyPI: `qubodock`
- Repository & examples: https://github.com/peikunyang/02_QUBO_Dock
- Paper: QUBODock: A Pip-Installable QUBO Tool for Ligand Pose Generation (arXiv:2508.13014)
