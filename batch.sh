#!/bin/bash

#SBATCH --job-name=CS5350MatrixMult
#SBATCH --output=%x_%j.out 
#SBATCH --error=%x_%j.err
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=25
#SBATCH --mem=4G
#SBATCH --partition=compute


# Compile the program with g++
g++ -fopenmp -o open_mp open_mp.cpp

# Initialize the results file with column headers
echo "m,n,q,P,SerialTime,ParallelTime,ParallelSpeedup,ParallelCost,1-DParallelTime,1-DParallelSpeedup,1-DParallelCost,2-DParallelTime,2-DParallelSpeedup,2-DParallelCost" > results.csv

# Define the range for m, n, q, and P.
for m in 10 25 50 100 250 500; do
    for n in 10 25 50 100 250 500; do
        for q in 10 25 50 100 250 500; do
            # Iterate through perfect squares for P up to 25
            for P in 4 9 16 25; do
                # Run the program and append the output to results.csv
                echo "Running for m=${m}, n=${n}, q=${q}, P=${P}" # echo placed in .out file
                ./open_mp ${m} ${n} ${q} ${P} >> results.csv
            done
        done
    done
done

echo "All tasks completed." # echo placed in .out file
