#!/bin/bash
#SBATCH -J jobname             # Job name which can be changed
#SBATCH -p batch        # partition name
#SBATCH -o out.txt    # Output file name
#SBATCH -e error.txt    # Error file name
#SBATCH -N 1            # Number of nodes
#SBATCH -n 120            # Number of tasks
#SBATCH -c 1          # Number of CPU cores per task
#SBATCH --mem=440G      # Memory allocation
#SBATCH -t 70:00:00    # Time limit (hh:mm:ss)
comsol batch -inputfile jobname-base.mph -outputfile jobname.mph -batchlog log-jobname