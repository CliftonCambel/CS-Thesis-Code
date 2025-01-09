#!/bin/bash
#SBATCH -J run_grid_aco
#SBATCH -N 1                        
#SBATCH --ntasks=1                       
#SBATCH --cpus-per-task=32               
#SBATCH -p rome                 
#SBATCH -t 1:00:00                  
#SBATCH --mail-type=BEGIN,END            
#SBATCH --mail-user=c.c.roozendal@student.vu.nl  



python3 $HOME/CS-Thesis-Code/ACO_100.py



echo "Finished"