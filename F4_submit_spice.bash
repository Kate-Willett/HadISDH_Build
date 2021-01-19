#!/bin/bash -l
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --output=/scratch/hadkw/slurm_logs/F4_CreateMonthSeriesfromHadISD.txt
#SBATCH --time=200
#SBATCH --qos=normal
module load scitools/default-current
python F4_CreateMonthSeriesfromHadISD.py
