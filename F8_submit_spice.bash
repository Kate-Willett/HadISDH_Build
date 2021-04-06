#!/bin/bash
# set -x
# ************************************************************************
# Simple script to create and submit SPICE jobs to Slurm.
#
# Author: hadkw
# Date:25 January 2021
#
# ************************************************************************
# START

# Essential run: 
for var in t q rh e tw 
#for var in q rh e tw 


do

        echo $var
	
	# separate file for each job
        spice_script=spice_IndirectPHA_${var}.bash
        
        echo "#!/bin/bash -l" > ${spice_script}
        echo "#SBATCH --mem=1G" >> ${spice_script}
        echo "#SBATCH --ntasks=1" >> ${spice_script}
        echo "#SBATCH --output=/scratch/hadkw/slurm_logs/F8_IndirectPHA_${var}.txt" >> ${spice_script}
        echo "#SBATCH --time=120" >> ${spice_script}
        echo "#SBATCH --qos=normal" >> ${spice_script}

        echo "module load scitools/default-current" >> ${spice_script}
        echo "export MPLBACKEND='Agg'" >> ${spice_script}
        echo "python F8_IndirectPHA.py --var ${var} --runtype all" >> ${spice_script}
        echo "unset MPLBACKEND" >> ${spice_script}        
        
        sbatch ${spice_script}       

done
