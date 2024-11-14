#!/bin/bash
#SBATCH --job-name=Initial_test_run_hillclimber
#SBATCH --output=output_%j.log
#SBATCH --error=error_%j.log
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
#SBATCH --partition=rome
#SBATCH --time=01:00:00



# Navigate to the script directory
#cd /path/to/your/scripts

# Run pythonprogram1.py on one task
srun $HOME/clif/CS-Thesis-Code/python Hillclimber_hybride_approach.py 

# Run pythonprogram2.py on another task
srun  $HOME/clif/CS-Thesis-Code/python Hillclimber_TSP_swaping.py 

# Run pythonprogram2.py on another task
srun $HOME/clif/CS-Thesis-Code/python Hillclimber_TSP_swaping.py 

# Wait for both processes to finish
wait

echo "Both programs have completed."
