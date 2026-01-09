# Simulation code: When bubbles bounce or stick

This repository contains the simulation templates and automation scripts required to reproduce the numerical results reported in the manuscript **“When bubbles bounce or stick”**.

The numerical workflow is split into two parts:

1. **Axisymmetric dynamics (2D, r–z):** simulated in **COMSOL Multiphysics 6.x**, controlled via Python using `mph` for automated parameter sweeps and data export.
2. **3D dynamics:** simulated using **Basilisk** (C-based adaptive CFD solver) with MPI support.

---

## Part 1: Axisymmetric simulations by COMSOL

Axisymmetric (r–z) simulations are run in **COMSOL Multiphysics 6.x** and controlled via Python using the `mph` library. The scripts automate:

- loading a pre-configured template model
- updating physical parameters (e.g., `Ga`, `Bo`, `Lrise`) and numerical settings (mesh level, timestep)
- running the solver
- exporting selected results for plotting/analysis

### Requirements

#### Software

- **COMSOL Multiphysics 6.x**
  - a valid license is required
  - the COMSOL backend must be accessible in your execution environment (local workstation or HPC)
- **Python 3.x**

#### Python dependencies

- `mph` (COMSOL–Python interface)
- `pandas` (data handling/export)
- `numpy`, `matplotlib` for post-processing/plotting

### Installation and setup

1. **Verify COMSOL works**
   - make sure you can open and solve `Axi_bubble_basic_model.mph` in the COMSOL GUI.

2. **Install python packages**
   ```bash
   pip install mph pandas numpy matplotlib
   ```

3. **Ensure `mph` can locate COMSOL**
   - if COMSOL is installed in a non-standard location, you may need to configure environment variables.

### How to run

#### Run on HPC via slurm (linux)

```bash
sbatch job.sh
```

#### Run locally (windows/linux)

```bash
python job.py
# or
bash job.sh
```

#### Quick test

A minimal test case is provided to validate that COMSOL + `mph` is functioning.

**Test parameters (example)**

- `Lrise = 1`
- `Ga = 20`
- `Bo = 1e-1`
- mesh refinement level: `7`

Run:

```bash
python test.py
```

#### Outputs

- A csv file `results_L_rise1_Ga20_Bo1e-1_Level7.csv`  is exported. 

---

## Part 2: 3D simulations by Basilisk

Full 3D bubble rising and impacting dynamics are simulated with **Basilisk**, using an adaptive grid solver and MPI parallelization. The implementation follows the methodology described in "Tripathi, M., Sahu, K. & Govindarajan, R. *Dynamics of an initially spherical bubble rising in quiescent liquid.* **Nat Commun** 6, 6268 (2015). https://doi.org/10.1038/ncomms7268"

### Requirements

- Basilisk installed following https://basilisk.fr/src/INSTALL.
- Python 3.x for post-processing scripts
- (optional) ParaView5.6.2 for `.vtu` visualization

### How to compile

Go to the compilation directory and build the solver:

```bash
# option 1: direct compile (example)
CC99='mpicc -std=c99' qcc -Wall -O2 -D_MPI=1 -disable-dimensions bubble.c -o bubble -lm

# option 2: use the provided script
bash compile.sh
```

### How to run

#### Local execution (MPI)

```bash
bash hpc-script.sh
```

#### HPC submission (slurm)

```bash
sbatch hpc-script.sh
```

### Visualization

#### Basilisk C Snapshot Visualization Script

```bash
qcc -w -Wall -O2 -disable-dimensions getFacets3D.c -o getFacets3D -lm
qcc -w -Wall -O2 -disable-dimensions getCells_bottomPlate.c -o getCells_bottomPlate -lm
python Video3D.py
```

#### Paraview export

```bash
python run_vtu.py
```

Open the generated `.vtu` sequence in ParaView5.6.2 for 3D rendering.

### Test run

To verify your Basilisk environment:

**Test parameters**

- `Ga = 100`
- `Bo = 0.1`
- `MAXLEVEL = 9`

Run:

```bash
bash test_3D.sh
```

---

## Citation

If you use this repository in academic work, please cite the associated manuscript.

```bibtex
@article{when_bubbles_bounce_or_stick,
  title   = {When bubbles bounce or stick},
  author  = {<authors>},
  journal = {<journal>},
  year    = {<year>},
  volume  = {<volume>},
  pages   = {<pages>},
  doi     = {<doi>}
}
```

---

## Contact

For questions, issues, or reproduction help, please open an issue in the repository or contact:

- Xiangyu Zhang (<zhangxiangyu911@gmail.com>)
