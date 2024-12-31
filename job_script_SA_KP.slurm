#!/bin/bash
#SBATCH -J SA_KP
#SBATCH -N 1                        
#SBATCH --ntasks=1                       
#SBATCH --cpus-per-task=20               
#SBATCH -p rome                 
#SBATCH -t 119:00:00                  
#SBATCH --mail-type=BEGIN,END            
#SBATCH --mail-user=c.c.roozendal@student.vu.nl  



python3 $HOME/CS-Thesis-Code/SA_KP.py




echo "Finished"