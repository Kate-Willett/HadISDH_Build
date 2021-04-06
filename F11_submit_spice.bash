#!/bin/bash
# set -x
# ************************************************************************
# Simple script to create and submit SPICE jobs to Slurm.
#
# Author: hadkw
# Date:25 January 2021
#
# ************************************************************************
#
# separate file for each job
spice_script=spice_UpdateGoodLists_LargeAdjRemovals.bash

echo "#!/bin/bash -l" > ${spice_script}
echo "#SBATCH --mem=1G" >> ${spice_script}
echo "#SBATCH --ntasks=1" >> ${spice_script}
echo "#SBATCH --output=/scratch/hadkw/slurm_logs/F11_UpdateGoodLists_LargeAdjRemovals.txt" >> ${spice_script}
echo "#SBATCH --time=60" >> ${spice_script}
echo "#SBATCH --qos=normal" >> ${spice_script}

echo "module load scitools/default-current" >> ${spice_script}
echo "python F11_UpdateGoodLists_LargeAdjRemovals.py" >> ${spice_script}

sbatch ${spice_script}       

echo "Submitted"
