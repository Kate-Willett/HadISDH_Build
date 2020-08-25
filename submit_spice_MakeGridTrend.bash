#!/bin/bash
# set -x
# ************************************************************************
# Simple script to create and submit SPICE jobs to Slurm.
#
# Author: hadkw
# Date:3 April 2020
#
# Does each year combination as a separate script.  
#    Polls the queue to not overload the system or quotas (Thanks to JJK for this)
#
# ************************************************************************
# START

year=2000
end=2019

echo "Running trends between ${year} and ${end} inclusive"

#while [ $year -le $end ];
for var in q rh t td e tw dpd;
#for var in td;
#for var in t;
do

	typee='LAND'
	#typee='MARINE'
	#typee='MARINESHIP'
	#typee='BLEND'
	#typee='BLENDSHIP'

#	typee='IDPHA'
#	if [ $var = 'dpd' ]
#	then   
#	    typee='PHA'
#	    
#	fi
#	
#	if [ $var = 'td' ]
#	then
#	    typee='PHADPD'
#	    
#	fi

        echo $var $typee
	
	# separate file for each job
        spice_script=spice_MakeGridTrend_${var}.bash
        
        echo "#!/bin/bash -l" > ${spice_script}
        echo "#SBATCH --mem=10G" >> ${spice_script}
        echo "#SBATCH --ntasks=1" >> ${spice_script}
        echo "#SBATCH --output=/data/users/hadkw/WORKING_HADISDH/slurm_logs/MakeGridTrend_${year}${end}_${var}.txt" >> ${spice_script}
        echo "#SBATCH --time=200" >> ${spice_script}
        echo "#SBATCH --qos=normal" >> ${spice_script}

        echo module load scitools/default-current
        echo "python MakeGridTrends.py --var ${var} --typee ${typee} --year1 ${year} --year2 ${end}" >> ${spice_script}
        
        sbatch ${spice_script}       

    echo "Submitted ${var}"

done

# remove all job files on request
#rm -i ${cwd}/spice_hadisdh_grid_*

#  END
#************************************************************************
