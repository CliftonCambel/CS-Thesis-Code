#!/bin/bash
#SBATCH --job-name=run_two_python_programs
#SBATCH --output=output_%j.log
#SBATCH --error=error_%j.log
#SBATCH --nodes=1
#SBATCH --ntasks=3                # Request 3 tasks
#SBATCH --cpus-per-task=20         # 20 CPUs per task for multithreading
#SBATCH --time=08:00:00           # Time limit
#SBATCH --mem=16GB                # Memory limit
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=c.c.roozendal@student.vu.nl

# Load Python module
module load Python/3.10.4-GCCcore-11.3.0

# Navigate to the script directory
#cd /path/to/your/scripts

# Run pythonprogram1.py on one task
srun --ntasks=1 --cpus-per-task=20 python Hillclimber_hybride_approach.py > output1.log &

# Run pythonprogram2.py on another task
srun --ntasks=1 --cpus-per-task=20 python Hillclimber_TSP_swaping.py > output2.log &

# Run pythonprogram2.py on another task
srun --ntasks=1 --cpus-per-task=20 python Hillclimber_TSP_swaping.py > output2.log &

# Wait for both processes to finish
wait

echo "Both programs have completed."
