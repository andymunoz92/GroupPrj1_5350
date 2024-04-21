#!/bin/bash

# following flags tell the batch system to set the environment variables

#SBATCH --job-name=CS5350_GP1
#SBATCH --output=%x_%j.out 

#SBATCH --cpus-per-task=25

#SBATCH --mem=4G 
#SBATCH --partition=compute 


# Compile the program with g++
g++ -fopenmp -o open_mp open_mp.cpp

# Initialize the results file with column headers
echo "..." >> .csv # between the quotations put the headers for your csv file,  echo >> .csv means to output to your .csv file'

echo "Running for m=${m}, n=${n}, q=${q}, P=${P}" # echo will write to .out file
./open_mp ${m} ${n} ${q} ${P} >> results.csv

echo "All tasks completed." # echo will write to .out file 