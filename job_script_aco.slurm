#!/bin/bash
#SBATCH -J aco
#SBATCH -N 1                        
#SBATCH --ntasks=1                       
#SBATCH --cpus-per-task=20               
#SBATCH -p rome                 
#SBATCH -t 119:00:00                  
#SBATCH --mail-type=BEGIN,END            
#SBATCH --mail-user=c.c.roozendal@student.vu.nl  



python3 $HOME/CS-Thesis-Code/ACO.py




echo "Finished"