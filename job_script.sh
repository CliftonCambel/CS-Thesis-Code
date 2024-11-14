#!/bin/bash
#SBATCH -J Initial_test_run_hillclimber
#SBATCH -N 1
#SBATCH --tasks-per-node 3
#SBATCH --cpus-per-task=20
#SBATCH --mem=60G
#SBATCH --partition=rome
#SBATCH -t 01:00:00

module load 2022

module load Python/3.10.4-GCCcore-11.3.0

# Navigate to the script directory
#cd /path/to/your/scripts

# Run pythonprogram1.py on one task
$HOME/clif/CS-Thesis-Code/python Hillclimber_hybride_approach.py 

# Run pythonprogram2.py on another task
$HOME/clif/CS-Thesis-Code/python Hillclimber_TSP_swaping.py 

# Run pythonprogram2.py on another task
$HOME/clif/CS-Thesis-Code/python Hillclimber_TSP_swaping.py 

# Wait for both processes to finish
wait

echo "Both programs have completed."
