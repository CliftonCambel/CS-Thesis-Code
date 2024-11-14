#!/bin/bash
#SBATCH -J Initial_test_run_hillclimber
#SBATCH -t 1:30:00
#SBATCH -p thin
#SBATCH -N 1
#SBATCH --tasks-per-node 22
#SBATCH --mem=60G





python3 $HOME/CS-Thesis-Code/Hillclimber_hybride_approach.py 




echo "Finished"
