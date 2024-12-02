#!/bin/bash
#SBATCH -J run_grid_aco
#SBATCH -N 1                        
#SBATCH --ntasks=1                       
#SBATCH --cpus-per-task=128               
#SBATCH -p rome                 
#SBATCH -t 119:00:00                  
#SBATCH --exclusive                   
#SBATCH --mail-type=BEGIN,END            
#SBATCH --mail-user=c.c.roozendal@student.vu.nl  



python3 $HOME/CS-Thesis-Code/Grid_search_ACO.py



echo "Finished"