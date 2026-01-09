#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess

# --------------------
# Define parameters
# --------------------
L_rise = 10
Bos = ["1e0", "1e-1", "1e-2", "1e-3"]
Gas = ["100"]
# Bos = ["1e1"]
# Gas = ["40"]
refine_num = 5
t_step = 0.05
t_max = 20
cores = 128

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
        if proc.poll() is None:  # None => still running
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
            # Command to run (adjust path to python if necessary)
            cmd = [
                "python", "run_3D.py",
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

            # Sleep briefly before launching next job
            time.sleep(10)

    # -----------------------------
    # Final wait for all tasks
    # -----------------------------
    while len(tasks) > 0:
        # Wait for at least one process to finish
        # If no process finishes quickly, wait will raise an exception after
        # the first to exit. We ignore that with try/except or poll approach.
        try:
            # 'wait' for any one child process
            os.waitpid(-1, 0)
        except ChildProcessError:
            # No more child processes
            break
        # Clean up finished tasks
        check_and_clean_tasks()

    print("All tasks have completed.")

if __name__ == "__main__":
    main()
