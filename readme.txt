# SIMULATION CODE FOR: When Bubbles Bounce or Stick.

This archive contains the source code, simulation templates, and scripts required to reproduce the numerical results presented in the manuscript. The simulations utilize COMSOL Multiphysics 6.2 interactively controlled via Python using the 'mph' library.

-------------------------------------------------------------------------
1. SYSTEM REQUIREMENTS
-------------------------------------------------------------------------

SOFTWARE:
1. COMSOL Multiphysics 6.x
   - A valid license is required.

2. Python 3.x environment

3. Python Libraries:
   - mph (Interface for COMSOL)
   - pandas

OPERATING SYSTEM:
- The code is compatible with both Windows and Linux (HPC environments).
- Specific execution scripts are provided for both platforms.

-------------------------------------------------------------------------
2. INSTALLATION
-------------------------------------------------------------------------

1. Ensure COMSOL Multiphysics 6.x is installed and functional.

2. Install the required Python interface 'mph'. 
   Detailed documentation and installation guide: https://mph.readthedocs.io/en/1.3/index.html

   Installation command:
   $ pip install mph

3. Configuration:
   Ensure that the 'mph' library can locate your COMSOL installation.

-------------------------------------------------------------------------
3. FILE DESCRIPTION
-------------------------------------------------------------------------

CORE FILES:
A. Axi Model:
- Axi_bubble_basic_model.mph : The encapsulated basic case file. Contains the pre-set physics, geometry, and study settings used as the template.
- run.py                 : The main interface script. It uses 'mph' to:
                           1. Load 'Axi_bubble_basic_model.mph'
                           2. Modify parameters (e.g., Ga, Bo, Lrise, refine_num, t_step, t_max, cores)
                           3. Run the solver
                           4. Perform post-processing
                           5. Export results

EXECUTION SCRIPTS:
- job.sh                 : Shell script for submitting jobs in a HPC or Linux environment.
- job.py                 : Python script for running cases locally on Windows or Linux.
- test.py                : A simplified script for testing the environment setup and running a single instance.

RESULTS:
- [Output Files]         : Generated .mph files, .csv data files and .webm video file.

B. 3D Model:
- 3D_bubble_basic_model.mph
- run_3D.py             

EXECUTION SCRIPTS:
- job_3D.py                 : Python script for running cases locally on Windows or Linux.

-------------------------------------------------------------------------
4. USAGE INSTRUCTIONS
-------------------------------------------------------------------------

A. Running on HPC (Linux):
   1. Ensure permissions are set for the shell script.
   2. Submit the job using your scheduler (e.g., Slurm, PBS) or run directly:
      $ sbatch job.sh
      $ bash job.sh

B. Running on Windows (Local Machine):
   1. Open a terminal or command prompt.
   2. Navigate to the directory containing the files.
   3. Run the job script:
      $ python job.py

C. Customizing Parameters:
   To simulate different physical conditions, modify the parameter lists defined in 'job.sh' or 'job.py'.

-------------------------------------------------------------------------
5. EXAMPLE CASE & EXPECTED OUTPUT
-------------------------------------------------------------------------

Included in this archive is a test configuration to verify the installation.

Parameters:
- Rise Length (L_rise): 1
- Galileo Number (Ga): 20
- Bond Number (Bo): 1e-2
- Mesh Refinement Level: 7

To run this specific example, execute:
$ python test.py

EXPECTED OUTPUTS:
Upon successful completion, the script will generate:

1. Simulation File: 
   "bubble_L_rise1_Ga20_Bo1e-2_Level7.mph" 
   (Contains the solved model with full physics history).

2. Numerical Results Data: 
   "results_L_rise1_Ga20_Bo1e-2_Level7.csv"
   (Contains the exported physical quantities extracted during post-processing).

3. Numerical Video: 
   "video_L_rise1_Ga20_Bo1e-2_Level7.webm"

-------------------------------------------------------------------------
CONTACT
-------------------------------------------------------------------------
For questions regarding the code usage, please contact: 
[Xiangyu Zhang] at [zxiangyu2-c@my.cityu.edu.hk]