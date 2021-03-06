#!/bin/bash -l
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --output=/data/users/hadkw/WORKING_HADISDH/slurm_logs/MakeGridTrend_20002019_tw.txt
#SBATCH --time=200
#SBATCH --qos=normal
python MakeGridTrends.py --var tw --typee LAND --year1 2000 --year2 2019
