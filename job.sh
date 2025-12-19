#!/bin/bash
#SBATCH --partition=genoa
#SBATCH --nodes=1
#SBATCH --ntasks=192
#SBATCH --time=120:00:00
#SBATCH --job-name=Bubble_L_rise_5
#SBATCH --output=out-Bubble_L_rise_5.txt
#SBATCH --error=error-Bubble_L_rise_5.txt

L_rise=5
Bos=("1e-2")
Gas=("100" "80" "60" "50" "40" "35" "30" "25" "20" "15" "10" "8" "7" "6" "5" "4" "3")

refine_num=8
t_step=0.02
t_max=10
cores=24

###################
# Parallel settings
###################
NPARA=8         # Maximum number of concurrent tasks

############################################
# Function: Check tasks and remove finished
############################################
# This function iterates over the 'tasks' array,
# removes any PID that has exited, and returns
# how many are still running.
check_and_clean_tasks() {
  local still_running=()
  for pid in "${tasks[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then
      # PID is still alive
      still_running+=( "$pid" )
    fi
  done
  tasks=("${still_running[@]}")
  echo "${#tasks[@]}"  # Return how many remain
}

#################################
# Main loop over all parameters
#################################
declare -a tasks=()  # To store PIDs of launched jobs

for Bo in "${Bos[@]}"; do
    for Ga in "${Gas[@]}"; do
        FILENAME="L_rise${L_rise}_Ga${Ga}_Bo${Bo}_Level${refine_num}"
        # Skip if result already exists
        if [ -e "results_${FILENAME}.csv" ]; then
            echo "$FILENAME already exists."
            continue
        fi

        ##############################
        # Wait until concurrency < NPARA
        ##############################
        while true; do
            running_count=$(check_and_clean_tasks)
            if [ "$running_count" -lt "$NPARA" ]; then
            break
            fi
            sleep 1
        done

        ###################################
        # Launch job in background 
        ###################################
        (
          echo "$FILENAME starts."
          python run.py --Bo "$Bo" --Ga "$Ga" --Lrise "$L_rise" --refine_num "$refine_num" --t_step "$t_step" --t_max "$t_max" --cores "$cores" --name "$FILENAME"        
        ) &
        sleep 10
        # Record the PID of the background job
        tasks+=( "$!" )
    done
done

###############################
# Final wait for all tasks
###############################
# Check if any tasks still running, wait for them
while [ "${#tasks[@]}" -gt 0 ]; do
  # Wait for any job to finish
  wait -n 2>/dev/null || true
  # Clean up finished tasks from array
  check_and_clean_tasks >/dev/null
done

echo "All tasks have completed."