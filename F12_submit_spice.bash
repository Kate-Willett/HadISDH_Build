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

for var in t rh dpd q td e tw;
# NEED A SLEEP COMMAND FOR t, rh and dpd so that they are run in order and not simultaneously
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
        spice_script=spice_CreateHomogNCDF_${var}.bash
        
        echo "#!/bin/bash -l" > ${spice_script}
        echo "#SBATCH --mem=5G" >> ${spice_script}
        echo "#SBATCH --ntasks=1" >> ${spice_script}
        echo "#SBATCH --output=/scratch/hadkw/slurm_logs/F12_CreateHomogNCDFStUnc_${var}.txt" >> ${spice_script}
        echo "#SBATCH --time=120" >> ${spice_script}
        echo "#SBATCH --qos=normal" >> ${spice_script}

        echo "module load scitools/default-current" >> ${spice_script}
        echo "export MPLBACKEND='Agg'" >> ${spice_script}
        echo "python F12_CreateHomogNCDFStUnc.py --var ${var} --typee ${typee} --runtype all" >> ${spice_script}
        echo "unset MPLBACKEND" >> ${spice_script}        
        
        sbatch ${spice_script}       

    echo "Submitted ${var}"

    if [ "$var" == "t" ] || [ "$var" == "dpd" ] || [ "$var" == "rh" ];
    then
        echo "Sleeping for 90 minutes"
	sleep 90m
    fi

done
