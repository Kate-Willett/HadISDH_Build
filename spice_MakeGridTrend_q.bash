#!/bin/bash -l
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --output=/data/users/hadkw/WORKING_HADISDH/slurm_logs/MakeGridTrend_19792019_q.txt
#SBATCH --time=200
#SBATCH --qos=normal
python MakeGridTrends.py --var q --typee ERA5 --year1 1979 --year2 2019
