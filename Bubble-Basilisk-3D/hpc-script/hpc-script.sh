#!/bin/bash 
#SBATCH -p batch        # partition name
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH --mem=440G      # Memory allocation
#SBATCH -t 70:00:00    # Time limit (hh:mm:ss)
#SBATCH --job-name=bubble_Bo1
#SBATCH -o out-bubble_Bo1.txt
#SBATCH -e error-bubble_Bo1.txt

module load GCC/13.2.0
module load OpenMPI/4.1.6-GCC-13.2.0 
module load Python/3.9.5-GCCcore-10.3.0 
ulimit -u 1000
# Parameter arrays
tsnap=0.01
Ldomain=16
Bos=(1)
MAXlevels=(9)
Gas=(100 250 500 1000)
THREADS=32
tmax=100
Lrise=10

DT=1e-3
CFL=0.5

echo "Oh values:"
for Oh in "${Gas[@]}"; do
    printf "%.3e\n" $Oh
done

###################
# Parallel settings
###################
NPARA=4      # Maximum number of concurrent tasks

mkdir -p Results_Running
mkdir -p Snapshots

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

for MAXlevel in "${MAXlevels[@]}"; do
  for Ga in "${Gas[@]}"; do
    for Bo in "${Bos[@]}"; do
      FILENAME="Bo${Bo}-Ga${Ga}-Lrise${Lrise}-MAXlevel${MAXlevel}"
      # Skip if result already exists        
      if [ -e "./Results_Running/$FILENAME.csv" ]; then
        echo "$FILENAME already exists."
        continue
      fi

      # Create working directory
      if [ -d "$FILENAME" ]; then
        cp -rf basicmodel/* "$FILENAME"
      else
        cp -rf basicmodel "$FILENAME"
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
        cd "$FILENAME" || exit 1            
        echo "[$(date)] Start running $FILENAME"
        chmod +x *
        # # Run the bounce program
        mpirun -n $THREADS ./bubble "$MAXlevel" "$Ga" "$Bo" "$tmax" "$Ldomain" "$DT" "$CFL" "$Lrise" >log_error 2>&1        
        python3 getResults.py --tMAX=$tmax --tSNAP=$tsnap --CPUs=$THREADS  >log_results 2>&1
        cp $FILENAME.csv ../Results_Running/$FILENAME.csv
        LAST_FILE=$(ls -v intermediate | tail -n 1)
        cp "intermediate/$LAST_FILE" "../Snapshots/$FILENAME-$LAST_FILE"
        cd ..
        tar -czf ${FILENAME}.tar.gz ${FILENAME} > /dev/null 2>&1
        rm -rf ${FILENAME}
      ) &
      # Record the PID of the background job
      tasks+=( "$!" )
    done
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