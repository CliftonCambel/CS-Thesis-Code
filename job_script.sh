#!/bin/bash
#SBATCH -J Initial_test_run_hillclimber  
#SBATCH --nodes=1                        
#SBATCH --ntasks=1                       
#SBATCH --cpus-per-task=64               
#SBATCH --partition=rome                 
#SBATCH --time=24:00:00                  
#SBATCH --mem=120G                       
#SBATCH --exclusive                      
#SBATCH --mail-type=BEGIN,END            
#SBATCH --mail-user=c.c.roozendal@student.vu.nl  


module load python                    

#Copy input file to scratch
cp $HOME/big_input_file "$TMPDIR"
 
#Create output directory on scratch
mkdir "$TMPDIR"/output_d

srun python $HOME/CS-Thesis-Code/Hillclimber_hybride_approach.py "$TMPDIR"/big_input_file "$TMPDIR"/output_dir




echo "Finished"
