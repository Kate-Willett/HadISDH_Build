#!/bin/bash
# set -x
# ************************************************************************
# Simple script to create and submit SPICE jobs to Slurm.
#
# Author: hadkw
# Date:10 December 2020
#
# ************************************************************************
# START

for var in q rh t td e tw dpd;
#for var in q rh t;

do

        echo $var #$typee
	
	# separate file for each job
        spice_script=spice_MissingAdjUnc_${var}.bash
        
        echo "#!/bin/bash -l" > ${spice_script}
        echo "#SBATCH --mem=1G" >> ${spice_script}
        echo "#SBATCH --ntasks=1" >> ${spice_script}
        echo "#SBATCH --output=/scratch/hadkw/slurm_logs/F10_MissingAdjInc_AdjPlots_${var}.txt" >> ${spice_script}
        echo "#SBATCH --time=10" >> ${spice_script}
        echo "#SBATCH --qos=normal" >> ${spice_script}

        echo module load scitools/default-current
        echo "python F10_MissingAdjUnc_AdjPlots.py --var ${var}" >> ${spice_script}
        
        sbatch ${spice_script}       

    echo "Submitted ${var}"

done
