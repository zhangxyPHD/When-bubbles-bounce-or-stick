#!/bin/bash
tsnap=0.01
Ldomain=16
Bo=0.1
MAXlevel=9
Ga=100
THREADS=32
tmax=100
Lrise=10
FILENAME="Bo${Bo}-Ga${Ga}-Lrise${Lrise}-MAXlevel${MAXlevel}"
cp -rf basicmodel "$FILENAME"
cd "$FILENAME" || exit 1      
CC99='mpicc -std=c99' qcc -Wall -O2 -D_MPI=1 -disable-dimensions bubble.c -o bubble -lm
qcc -Wall -O2 -disable-dimensions getResults.c -o getResults -lm      
mpirun -n $THREADS ./bubble "$MAXlevel" "$Ga" "$Bo" "$tmax" "$Ldomain" "$DT" "$CFL" "$Lrise" >log_error 2>&1        
python3 getResults.py --tMAX=$tmax --tSNAP=$tsnap --CPUs=$THREADS  >log_results 2>&1
