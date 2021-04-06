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

# Essential run:
for var in t dpd 
# Addition if of interest
#for var in q rh td e tw;


do

        typee='PHA'

        echo $var $typee
	
	# separate file for each job
        spice_script=spice_F7OutputPHAASCIIPLOT_${var}.bash
        
        echo "#!/bin/bash -l" > ${spice_script}
        echo "#SBATCH --mem=5G" >> ${spice_script}
        echo "#SBATCH --ntasks=1" >> ${spice_script}
        echo "#SBATCH --output=/scratch/hadkw/slurm_logs/F7_OutputPHAASCIIPLOT_${var}.txt" >> ${spice_script}
        echo "#SBATCH --time=120" >> ${spice_script}
        echo "#SBATCH --qos=normal" >> ${spice_script}

        echo "module load scitools/default-current" >> ${spice_script}
        echo "export MPLBACKEND='Agg'" >> ${spice_script}
        echo "python F7_9_OutputPHAASCIIPLOT.py --var ${var} --typee ${typee} --runtype all" >> ${spice_script}
        echo "unset MPLBACKEND" >> ${spice_script}        
	
        sbatch ${spice_script}       

    echo "Submitted ${var}"

    if [ "${var}" == "t" ];
    then
        echo "Sleeping for 75 minutes"
        sleep 75m

    fi 
 
done
