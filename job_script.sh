#!/bin/bash
#SBATCH -J Initial_test_run_hillclimber
#SBATCH -N 1
#SBATCH --tasks-per-node 1
#SBATCH --cpus-per-task=20
#SBATCH --mem=60G
#SBATCH --partition=rome
#SBATCH -t 02:00:00



# Navigate to the script directory
#cd /path/to/your/scripts
module matplotlib
python3 $HOME/CS-Thesis-Code/Hillclimber_hybride_approach.py 

# Run pythonprogram2.py on another task
#$HOME/clif/CS-Thesis-Code/python Hillclimber_TSP_swaping.py 

# Run pythonprogram2.py on another task
#$HOME/clif/CS-Thesis-Code/python Hillclimber_TSP_swaping.py 

# Wait for both processes to finish


echo "Finished"
