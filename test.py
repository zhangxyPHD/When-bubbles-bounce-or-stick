#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
#SBATCH --partition=genoa
#SBATCH --nodes=1
#SBATCH --ntasks=192
#SBATCH --time=120:00:00
#SBATCH --job-name=Bubble_L_rise_5
#SBATCH --output=out-Bubble_L_rise_5.txt
#SBATCH --error=error-Bubble_L_rise_5.txt

Description:
  This script replicates the logic of the original bash script to run multiple
  parameter sets of a Python program (run.py) with a simple concurrency limit
  on Windows or Linux, launching up to NPARA tasks simultaneously.
"""

import os
import time
import subprocess

# --------------------
# Define parameters
# --------------------
L_rise = 1
Bos = ["1e-1"]
Gas = ["20"]  # Correct list syntax

refine_num = 7
t_step = 0.01
t_max = 0.1
cores = 24

# Concurrency limit
NPARA = 1  # Maximum number of concurrent tasks

# List to store active subprocesses
tasks = []

def check_and_clean_tasks():
    """
    Check which subprocesses are still running.
    Remove finished ones from 'tasks' list.
    Return the count of running tasks.
    """
    global tasks
    still_running = []
    for proc in tasks:
        # If proc.poll() is None => still running
        if proc.poll() is None:
            still_running.append(proc)
    tasks = still_running
    return len(tasks)

def main():
    """
    Main driver logic to iterate over parameters and spawn jobs with concurrency control.
    """
    for Bo in Bos:
        for Ga in Gas:
            filename = f"L_rise{L_rise}_Ga{Ga}_Bo{Bo}_Level{refine_num}"
            result_file = f"results_{filename}.csv"

            # Skip if result already exists
            if os.path.exists(result_file):
                print(f"{filename} already exists.")
                continue

            # Wait until we have fewer than NPARA running tasks
            while True:
                running_count = check_and_clean_tasks()
                if running_count < NPARA:
                    break
                time.sleep(1)

            # Launch the job in background
            print(f"{filename} starts.")
            cmd = [
                "python", "run.py",
                "--Bo", Bo,
                "--Ga", Ga,
                "--Lrise", str(L_rise),
                "--refine_num", str(refine_num),
                "--t_step", str(t_step),
                "--t_max", str(t_max),
                "--cores", str(cores),
                "--name", filename
            ]
            proc = subprocess.Popen(cmd)
            tasks.append(proc)

            # Sleep briefly before launching the next job
            time.sleep(10)

    # -----------------------------
    # Final wait for all tasks
    # -----------------------------
    # On Windows, os.waitpid won't work the same as Linux/Unix, so just poll.
    while len(tasks) > 0:
        time.sleep(1)
        check_and_clean_tasks()

    print("All tasks have completed.")

if __name__ == "__main__":
    main()
