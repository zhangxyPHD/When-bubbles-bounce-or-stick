#!/bin/bash

module load GCC/13.2.0
module load OpenMPI/4.1.6-GCC-13.2.0 
module load Python/3.9.5-GCCcore-10.3.0 

cd basicmodel
CC99='mpicc -std=c99' qcc -Wall -O2 -D_MPI=1 -disable-dimensions bubble.c -o bubble -lm
qcc -Wall -O2 -disable-dimensions getResults.c -o getResults -lm
rm -rf .*
cd ..