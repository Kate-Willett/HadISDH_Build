#********************************************
# Script to set up directory structure for this year's run
# Set up will be on /scratch/hadkw/
# After completion of run the structure will need to moved to /data/users/hadkw/WORKING_HADISDH/
# >scp -r UPDATE<YYYY> /data/users/hadkw/WORKING_HADISDH/
# Then clean up scratch using rm -r VERY VERY VERY CAREFULLY
#********************************************

# Configuration file to read in UPDATE INFORMATION WITHIN THIS FILE!!!
source F1_HadISDHBuildConfig.txt

echo $StartYear # This should be 1973
echo $EndYear # This should be 2019 or later
echo $Version # This should be v420_2019f or later
echo $VersionDots # This should be 4.2.0.2019f or later
echo $HadISDVersionDots # This should be 3.1.0.2019f or later
echo $HadISDVersion # This should be v310_2019f or later
echo $HadISDVersionMonth # This should be v310_201901p or later

WorkDir="UPDATE"$EndYear
MyDir="/scratch/hadkw/"

LastYear=$(( $EndYear - 1 ))
OldWorkDir="UPDATE"$LastYear

echo $OldWorkDir

mkdir $MyDir$WorkDir

mkdir $MyDir$WorkDir/LISTS_DOCS  

# Create file to store useful statistics for blog, update documents
touch $MyDir$WorkDir/LISTS_DOCS/OutputLogFile$VersionDots.txt

mkdir $MyDir$WorkDir/IMAGES
mkdir $MyDir$WorkDir/IMAGES/MAPS
mkdir $MyDir$WorkDir/IMAGES/TIMESERIES
mkdir $MyDir$WorkDir/IMAGES/BUILD
mkdir $MyDir$WorkDir/IMAGES/ANALYSIS
mkdir $MyDir$WorkDir/IMAGES/OTHER

mkdir $MyDir$WorkDir/OTHERDATA  
mkdir $MyDir$WorkDir/OTHERDATA/ERA5  
cp /data/users/hadkw/WORKING_HADISDH/$OldWorkDir/OTHERDATA/new_coverpercentjul08.nc $MyDir$WorkDir/OTHERDATA/
cp /data/users/hadkw/WORKING_HADISDH/$OldWorkDir/OTHERDATA/HadCRUT.4.3.0.0.land_fraction.nc $MyDir$WorkDir/OTHERDATA/
cp /data/users/hadkw/WORKING_HADISDH/$OldWorkDir/OTHERDATA/197901_hourly_land_sea_mask_ERA5.nc $MyDir$WorkDir/OTHERDATA/
cp /data/users/hadkw/WORKING_HADISDH/$OldWorkDir/OTHERDATA/20CR* $MyDir$WorkDir/OTHERDATA/
cp /data/users/hadkw/WORKING_HADISDH/$OldWorkDir/OTHERDATA/*2m*ERA5* $MyDir$WorkDir/OTHERDATA/

mkdir $MyDir$WorkDir/STATISTICS 
mkdir $MyDir$WorkDir/STATISTICS/GRIDS
mkdir $MyDir$WorkDir/STATISTICS/TIMESERIES
mkdir $MyDir$WorkDir/STATISTICS/OTHER
mkdir $MyDir$WorkDir/STATISTICS/TRENDS

mkdir $MyDir$WorkDir/MONTHLIES  
mkdir $MyDir$WorkDir/MONTHLIES/NETCDF
mkdir $MyDir$WorkDir/MONTHLIES/HISTORY

mkdir $MyDir$WorkDir/MONTHLIES/ASCII
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/DPDABS    
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/EABS    
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/QABS    
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/RHABS    
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/TABS
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/TDABS    
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/TWABS    
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/derivedDPDABS
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/WSABS
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/SLPABS
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/DPDANOMS  
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/EANOMS  
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/QANOMS  
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/RHANOMS  
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/TANOMS  
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/TDANOMS  
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/TWANOMS  
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/derivedTDABS
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/WSANOMS
mkdir $MyDir$WorkDir/MONTHLIES/ASCII/SLPANOMS

mkdir $MyDir$WorkDir/MONTHLIES/HOMOG
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHAASCII  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHANETCDF  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHAASCII  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHANETCDF  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS

mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHAASCII/EDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHAASCII/QDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHAASCII/RHDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHAASCII/TDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHAASCII/TDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHAASCII/TWDIR

mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHANETCDF/EDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHANETCDF/QDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHANETCDF/RHDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHANETCDF/TDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHANETCDF/TDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/IDPHANETCDF/TWDIR 

mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHAASCII/DPDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHAASCII/EDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHAASCII/QDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHAASCII/RHDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHAASCII/TDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHAASCII/TDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHAASCII/TWDIR
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHAASCII/WSDIR
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHAASCII/SLPDIR

mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHANETCDF/DPDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHANETCDF/EDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHANETCDF/QDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHANETCDF/RHDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHANETCDF/TDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHANETCDF/TDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHANETCDF/TWDIR
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHANETCDF/WSDIR
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/PHANETCDF/SLPDIR

mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/IDPHAADJCOMP  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS

mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/IDPHAADJCOMP/EDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/IDPHAADJCOMP/QDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/IDPHAADJCOMP/RHDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/IDPHAADJCOMP/TDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/IDPHAADJCOMP/TDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/IDPHAADJCOMP/TWDIR

mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/DPDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/EDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/QDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/RHDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/TDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/TDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/TWDIR
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/WSDIR
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/SLPDIR

mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/DPDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/EDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/QDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/QPHADIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/RHDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/RHPHADIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/TDDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/TDIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/TDPHADIR  
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/TWDIR
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/WSDIR
mkdir $MyDir$WorkDir/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/SLPDIR

#exit 1 # to exit while debugging

# Make a temporary directory for storing HadISD data which will be deleted after processing and BEFORE copying processed data to /data/users/hadkw!!!
mkdir $MyDir$WorkDir"/HADISDTMP"
mkdir $MyDir$WorkDir"/HADISDTMP/LOGS" # for output logfiles from wget

# Download HadISD files from HadOBS server and unpack -o logfile, -t number of tries (default = 20)
# Get the station file listing and the final mergers files
#wget -P $MyDir$WorkDir/LISTS_DOCS/HadISD.$HadISDVersionDots"_candidate_stations_details.txt" https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/files/hadisd_station_fullinfo_$HadISDVersion.txt 
#wget -P $MyDir$WorkDir/LISTS_DOCS/HadISD.$HadISDVersionDots"_candidate_stations_details.txt" https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/files/hadisd_station_fullinfo_$HadISDVersionMonth.txt 
# Maybe a better way to change the file name while copying over?
wget -P $MyDir$WorkDir/LISTS_DOCS/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/files/hadisd_station_fullinfo_$HadISDVersionMonth.txt 
mv $MyDir$WorkDir/LISTS_DOCS/hadisd_station_fullinfo_$HadISDVersionMonth.txt $MyDir$WorkDir/LISTS_DOCS/HadISD.$HadISDVersionDots"_candidate_stations_details.txt"
#wget -P $MyDir$WorkDir/LISTS_DOCS/HadISD.$HadISDVersionDots"_final_mergers.txt" https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/files/final_mergers.txt 
#wget -P $MyDir$WorkDir/LISTS_DOCS/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/files/final_mergers.txt 
wget -P $MyDir$WorkDir/LISTS_DOCS/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/files/final_mergers.txt 
mv $MyDir$WorkDir/LISTS_DOCS/final_mergers.txt $MyDir$WorkDir/LISTS_DOCS/HadISD.$HadISDVersionDots"_final_mergers.txt"

# Download the latest isd-history.txt file to LISTS_DOCS with the date in the file name
#wget -P $MyDir$WorkDir/LISTS_DOCS/isd-history-$(date +"%Y-%m-%d").txt https://www1.ncdc.noaa.gov/pub/data/noaa/isd-history.txt
wget -P $MyDir$WorkDir/LISTS_DOCS/ https://www1.ncdc.noaa.gov/pub/data/noaa/isd-history.txt
mv $MyDir$WorkDir/LISTS_DOCS/isd-history.txt $MyDir$WorkDir/LISTS_DOCS/isd-history-$(date +"%Y-%m-%d").txt

#000000-029999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile0s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_000000-029999.tar.gz 
# Check Loggile0s for success?
# Unpack the tarball - these come out as .gz
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_000000-029999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
## For now this spits out into /scratch/rdunn/hadisd/v310_2019f/hadobs_copy_v310_2019f/data/ so we need to deal with that!!!
## Move after each copy/unpack to avoid 'Argument list too long' errors.
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#030000-049999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile03s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_030000-049999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_030000-049999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#050000-079999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile05s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_050000-079999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_050000-079999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#080000-099999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile08s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_080000-099999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_080000-099999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#100000-149999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile1s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_100000-149999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_100000-149999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#150000-199999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile15s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_150000-199999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_150000-199999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#200000-249999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile2s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_200000-249999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_200000-249999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#250000-299999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile25s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_250000-299999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_250000-299999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#300000-349999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile3s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_300000-349999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_300000-349999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#350000-399999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile35s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_350000-399999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_350000-399999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#400000-449999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile4s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_400000-449999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_400000-449999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#450000-499999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile45s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_450000-499999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_450000-499999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#500000-549999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile5s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_500000-549999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_500000-549999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#550000-599999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile55s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_550000-599999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_550000-599999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#600000-649999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile6s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_600000-649999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_600000-649999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#650000-699999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile65s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_650000-699999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_650000-699999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#700000-709999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile70s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_700000-709999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_700000-709999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#710000-719999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile71s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_710000-719999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_710000-719999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#720000-722999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile72s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_720000-722999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_720000-722999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#723000-723999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile723s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_723000-723999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_723000-723999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#724000-724999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile724s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_724000-724999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_724000-724999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#725000-725999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile725s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_725000-725999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_725000-725999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#726000-726999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile726s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_726000-726999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_726000-726999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#727000-729999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile727s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_727000-729999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_727000-729999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#730000-799999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile73s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_730000-799999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_730000-799999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#800000-849999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile8s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_800000-849999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_800000-849999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#850000-899999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile85s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_850000-899999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_850000-899999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#900000-949999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile9s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_900000-949999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_900000-949999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

#950000-999999
wget -o $MyDir$WorkDir/HADISDTMP/LOGS/Logfile95s -P $MyDir$WorkDir/HADISDTMP/ https://www.metoffice.gov.uk/hadobs/hadisd/$HadISDVersion/data/WMO_950000-999999.tar.gz 
tar -xzf $MyDir$WorkDir/HADISDTMP/WMO_950000-999999.tar.gz -C $MyDir$WorkDir/HADISDTMP/
#mv $MyDir$WorkDir/HADISDTMP/scratch/rdunn/hadisd/$HadISDVersion/hadobs_copy_$HadISDVersion/data/* $MyDir$WorkDir/HADISDTMP/

# There should be 29 Logfiles with '100%' in them if successful
moo=$( grep '100%' $MyDir$WorkDir/HADISDTMP/LOGS/Logfile* | wc -l)
echo $moo
if [ $moo -ge 29 ]; then
    echo Successful HadISD retrieve
    # get the number of stations in the HadISD station list, check against number of stations in file and output to log
    # this gives just the number of lines and not the filename as part of the output
    ISDStats=`wc -l < $MyDir$WorkDir/LISTS_DOCS/HadISD.$HadISDVersionDots"_candidate_stations_details.txt"`
    echo "ISD_Initial_Station_Count="$ISDStats >> $MyDir/LISTS_DOCS/OutputLogFile$VersionDots.txt
    #wc -l $MyDir$WorkDir/LISTS_DOCS/HadISD.$HadISDVersionDots"_candidate_stations_details.txt" >> $MyDir$WorkDir/OutputLogFile$Version.txt
    # If we find that this check on 29 files with '100%' in isn't working then could add a test for number  of stations copied vs station count
    # but I'm concerned that ls doesn't work well when counting LOTS of files - its slow.
else
    echo Failed HadISD retrieve
    exit 1
fi

