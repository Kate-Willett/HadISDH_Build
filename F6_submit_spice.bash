#!/bin/bash -l
#SBATCH --mem=1G
#SBATCH --ntasks=1
#SBATCH --output=/scratch/hadkw/slurm_logs/F6_RewriteStnlistPostPHA.txt
#SBATCH --time=200
#SBATCH --qos=normal
module load scitools/default-current
python F6_RewriteStnlistPostPHA.py
