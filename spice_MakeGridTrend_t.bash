#!/bin/bash -l
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --output=/data/users/hadkw/WORKING_HADISDH/slurm_logs/MakeGridTrend_20002019_t.txt
#SBATCH --time=200
#SBATCH --qos=normal
python MakeGridTrends.py --var t --typee LAND --year1 2000 --year2 2019
