# Simulation Code: When Bubbles Bounce or Stick

This archive contains the source code, simulation templates, and scripts required to reproduce the numerical results presented in the manuscript **"When Bubbles Bounce or Stick"**. The simulations utilize COMSOL Multiphysics 6.x interactively controlled via Python using the `mph` library.

---

## 1. System Requirements

### Software
* **COMSOL Multiphysics 6.x**
    * A valid license is required.
    * The software must be installed and the COMSOL backend must be accessible.
* **Python 3.x environment**

### Python Libraries
* `mph` (Interface for COMSOL)
* `pandas` (Data handling)

### Operating System
* The code is compatible with both Windows and Linux (HPC environments).
* Specific execution scripts are provided for both platforms.

---

## 2. Installation

1.  **COMSOL Setup:**
    Ensure COMSOL Multiphysics 6.x is installed and functional on your machine.

2.  **Python Interface Setup:**
    Install the required Python interface `mph`.
    * Detailed documentation: [https://mph.readthedocs.io/en/1.3/index.html](https://mph.readthedocs.io/en/1.3/index.html)
    * Installation command:
        ```bash
        pip install mph
        ```

3.  **Configuration:**
    Ensure that the `mph` library can locate your COMSOL installation. You may need to verify your system path environment variables if COMSOL is installed in a non-standard location.

---

## 3. File Description

### A. Axi-Symmetric Model
**Core Files:**
* `Axi_bubble_basic_model.mph`: The encapsulated basic case file. Contains the pre-set physics, geometry, and study settings used as the template.
* `run.py`: The main interface script. It uses `mph` to:
    1.  Load `Axi_bubble_basic_model.mph`
    2.  Modify parameters (e.g., Ga, Bo, Lrise, refine_num, t_step, t_max, cores)
    3.  Run the solver
    4.  Perform post-processing
    5.  Export results

**Execution Scripts:**
* `job.sh`: Shell script for submitting jobs in an HPC or Linux environment.
* `job.py`: Python script for running cases locally on Windows or Linux.
* `test.py`: A simplified script for testing the environment setup and running a single instance.

**Results:**
* Output Files: Generated `.mph` files, `.csv` data files, and `.webm` video files.

### B. 3D Model
**Core Files:**
* `3D_bubble_basic_model.mph`: The encapsulated 3D template.
* `run_3D.py`: The main interface script for 3D simulations.

**Execution Scripts:**
* `job_3D.py`: Python script for running 3D cases locally on Windows or Linux.

---

## 4. Usage Instructions

### A. Running on HPC (Linux)
1.  Ensure permissions are set for the shell script (e.g., `chmod +x job.sh`).
2.  Submit the job using your scheduler (e.g., Slurm, PBS) or run directly:

    ```bash
    # Using Slurm
    sbatch job.sh
    
    # OR running directly via bash
    bash job.sh
    ```

### B. Running on Windows (Local Machine)
1.  Open a terminal or command prompt (CMD/PowerShell/Anaconda Prompt).
2.  Navigate to the directory containing the files.
3.  Run the job script:
    ```bash
    python job.py
    ```

### C. Customizing Parameters
To simulate different physical conditions, modify the parameter lists defined inside `job.sh` (for HPC) or `job.py` (for local execution).

---

## 5. Example Case & Expected Output

Included in this archive is a test configuration to verify the installation and workflow.

**Test Parameters:**
* **Rise Length (L_rise):** 1
* **Galileo Number (Ga):** 20
* **Bond Number (Bo):** 1e-2
* **Mesh Refinement Level:** 7

**Execution:**
To run this specific example, execute:
```bash
python test.py