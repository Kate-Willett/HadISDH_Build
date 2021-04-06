#********************************************
# Script to run PHA 
# Set up will be on /scratch/hadkw/
#********************************************
echo 'Running PHA'

# Configuration file to read in UPDATE INFORMATION WITHIN THIS FILE!!!
source F1_HadISDHBuildConfig.txt

echo $StartYear # This should be 1973
echo $EndYear # This should be 2019 or later

WorkDir="UPDATE"$EndYear
MyDir="/scratch/hadkw/"

cd $MyDir$WorkDir/pha52jgo/

echo 'Moved to '$MyDir$WorkDir'/pha52jgo/'

sbatch --mem=20000 --time=150 --ntasks=1 --output=/scratch/hadkw/slurm_logs/q.log ./testv52j-phaSPICE.sh q tavg raw 0 0 P > runlogs/q.log &
sbatch --mem=20000 --time=150 --ntasks=1 --output=/scratch/hadkw/slurm_logs/e.log ./testv52j-phaSPICE.sh e tavg raw 0 0 P > runlogs/e.log &
sbatch --mem=20000 --time=150 --ntasks=1 --output=/scratch/hadkw/slurm_logs/rh.log ./testv52j-phaSPICE.sh rh tavg raw 0 0 P > runlogs/rh.log &
sbatch --mem=20000 --time=150 --ntasks=1 --output=/scratch/hadkw/slurm_logs/t.log ./testv52j-phaSPICE.sh t tavg raw 0 0 P > runlogs/t.log &
sbatch --mem=20000 --time=150 --ntasks=1 --output=/scratch/hadkw/slurm_logs/td.log ./testv52j-phaSPICE.sh td tavg raw 0 0 P > runlogs/td.log &
sbatch --mem=20000 --time=150 --ntasks=1 --output=/scratch/hadkw/slurm_logs/tw.log ./testv52j-phaSPICE.sh tw tavg raw 0 0 P > runlogs/tw.log &
sbatch --mem=20000 --time=150 --ntasks=1 --output=/scratch/hadkw/slurm_logs/dpd.log ./testv52j-phaSPICE.sh dpd tavg raw 0 0 P > runlogs/dpd.log &
sbatch --mem=20000 --time=150 --ntasks=1 --output=/scratch/hadkw/slurm_logs/slp.log ./testv52j-phaSPICE.sh slp tavg raw 0 0 P > runlogs/slp.log &

#sbatch --mem=20000 --time=150 --ntasks=1 --output=/scratch/hadkw/slurm_logs/ws.log ./pha52jgo/testv52j-phaSPICE.sh 7319ws tavg raw 0 0 P > runlogs/ws.log &

cd /home/h04/hadkw/HadISDH_Code/HADISDH_BUILD/

echo 'Moved back again'
