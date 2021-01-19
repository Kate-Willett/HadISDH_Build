#!/bin/bash -l
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --output=/data/users/hadkw/WORKING_HADISDH/slurm_logs/MakeGridTrend_19792019_t.txt
#SBATCH --time=200
#SBATCH --qos=normal
python MakeGridTrends.py --var t --typee ERA5 --year1 1979 --year2 2019
