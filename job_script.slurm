#!/bin/bash
#SBATCH -J Initial_test_run_hillclimber  
#SBATCH -N 1                        
#SBATCH --ntasks=1                       
#SBATCH --cpus-per-task=36               
#SBATCH -p rome                 
#SBATCH -t 24:00:00                  
#SBATCH --exclusive                      
#SBATCH --mail-type=BEGIN,END            
#SBATCH --mail-user=c.c.roozendal@student.vu.nl  



python3 $HOME/CS-Thesis-Code/Hillclimber_hybride_approach.py 




echo "Finished"