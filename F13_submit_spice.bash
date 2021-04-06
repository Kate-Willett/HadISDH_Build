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
#for var in td;

do

       typee='IDPHA'
       if [ "$var" == "dpd" ];
       then   
	   typee='PHA'
	   
       fi
       
       if [ "$var" == "td" ];
       then
	   typee='PHADPD'
	   
       fi

        echo $var $typee
	
	# separate file for each job
        spice_script=spice_GridHadISDHFLAT_${var}.bash
        
        echo "#!/bin/bash -l" > ${spice_script}
        echo "#SBATCH --mem=2G" >> ${spice_script}
        echo "#SBATCH --ntasks=1" >> ${spice_script}
        echo "#SBATCH --output=/scratch/hadkw/slurm_logs/F13_GridHadISDHFLAT_${var}.txt" >> ${spice_script}
        echo "#SBATCH --time=120" >> ${spice_script}
        echo "#SBATCH --qos=normal" >> ${spice_script}

        echo "module load scitools/default-current" >> ${spice_script}
        echo "export MPLBACKEND='Agg'" >> ${spice_script}
        echo "python F13_GridHadISDHFLAT.py --var ${var} --typee ${typee}" >> ${spice_script}
        echo "unset MPLBACKEND" >> ${spice_script}        
        
        sbatch ${spice_script}       

    echo "Submitted ${var}"

done
