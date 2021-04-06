#********************************************
# Script to set up PHA directory and file structure for this year's run
# Set up will be on /scratch/hadkw/
#********************************************
# Configuration file to read in UPDATE INFORMATION WITHIN THIS FILE!!!
source F1_HadISDHBuildConfig.txt

echo $StartYear # This should be 1973
echo $EndYear # This should be 2019 or later
echo $Version # This should be 4.2.0.2019f or later
echo $VersionDots # This should be 4.2.0.2019f or later

WorkDir="UPDATE"$EndYear
MyDir="/scratch/hadkw/"

LastYear=$(( $EndYear - 1 ))

# Copy over the generic empty file structure and code
scp -r ~hadkw/HadISDH_Code/HADISDH_BUILD/pha52jgo $MyDir$WorkDir/

# Now update the within file fields for this year
sed -i -e 's/2018/'$EndYear'/g' $MyDir$WorkDir/pha52jgo/data/rh.conf # static code will always be set for 2018
sed -i -e 's/2018/'$EndYear'/g' $MyDir$WorkDir/pha52jgo/data/q.conf # static code will always be set for 2018
sed -i -e 's/2018/'$EndYear'/g' $MyDir$WorkDir/pha52jgo/data/e.conf # static code will always be set for 2018
sed -i -e 's/2018/'$EndYear'/g' $MyDir$WorkDir/pha52jgo/data/t.conf # static code will always be set for 2018
sed -i -e 's/2018/'$EndYear'/g' $MyDir$WorkDir/pha52jgo/data/td.conf # static code will always be set for 2018
sed -i -e 's/2018/'$EndYear'/g' $MyDir$WorkDir/pha52jgo/data/tw.conf # static code will always be set for 2018
sed -i -e 's/2018/'$EndYear'/g' $MyDir$WorkDir/pha52jgo/data/dpd.conf # static code will always be set for 2018
sed -i -e 's/2018/'$EndYear'/g' $MyDir$WorkDir/pha52jgo/data/slp.conf # static code will always be set for 2018
sed -i -e 's/2018/'$EndYear'/g' $MyDir$WorkDir/pha52jgo/data/ws.conf # static code will always be set for 2018
 
# No need to reset StartYear - set to 1973
sed -i -e 's/2018/'$EndYear'/g' $MyDir$WorkDir/pha52jgo/all_code/source_expand/parm_includes/inhomog.parm.MTHLY.TEST.incl
# No need to reset MaxStations - set to 5000

# Now make compile the fortran code adn then copy over to /bin
cd $MyDir$WorkDir/pha52jgo/all_code/source_expand/
make compile
# I actually think that the make compile copies stuff into /code/bin but just to be sure...
cp PHAv52j.FAST.MLY.TEST ../../code/bin/PHAv52j.FAST.MLY.TEST
cd ~hadkw/HadISDH_Code/HADISDH_BUILD/ # Does this work? Do we need to copy the code to somewhere else?

# Station lists will need to be copied over and data populated within /raw
