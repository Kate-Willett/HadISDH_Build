# PYTHON 3
# 
# Author: Kate Willett
# Created: 1 February 2013, IDL, Converted to Python 3 December 2020
# Last update: 12 January 2021
# Location:/home/h04/hadkw/HadISDH_Code/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# For one variable at a time, IN A SET ORDER!!! [T, RH, DPD, q, e, Td, Tw]
# Read in list of stations passing through PHA/IDPHA
# MUST HAVE INPUT ADJUSTMENT UNCERTAINTY FOR EACH VARIABLE - find #***MISSEDADJUNC***
# Loop through each station
# read in homogenised station (ASCII VERSION OF ABS)
# Find cases of subzeros (RH, q and e) or supersaturation (RH, DPD, Td and Tw indirectly q, e) and output to list (continue to process)
# WORKING WITH HOMOGENISED ACTUALS:
#   create station anomalies and climatologies using desired climatology period
# WORKING WITH HOMOGENISED ANOMALIES:
#   create station actuals from homogenised anomalies and non-homog climatologies (create these from ascii absolutes, could adjust by climatology of adjustments?)
# List stations with < 15 years present for each month of climatology as BADS - output to list and do not continue to process.
# Work out measurement uncertainty
# Work out adjustment uncertainties an dmissed adjustment uncertainty
# Output to netCDF (with 2 sigma uncertainties!!!)
# Make stationstats plot of all uncertainties

 
# <references to related published material, e.g. that describes data set>
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# import numpy as np # used
# import numpy.ma as npm # used
# from datetime import datetime # used
# import matplotlib.pyplot as plt
# import sys, os, getopt # used
# import struct
# import glob # used
# import pdb # used
# import netCDF4 as nc4
# from subprocess import call, check_output, run, PIPE # used

# Kate's Functions
# import CalcHums
# from RandomsRanges import LetterRange
# 
# -----------------------
# DATA
# -----------------------
# Input station lists, adjustment log lists
#  /scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/'
#    goodforHadISDH.'+versiondots+'_'+typee+var+'.txt'
#    HadISDH.land'+ParamDict[var][0]+'.'+versiondots+'_'+homogtype+'.log'
#    PosthomogIDPHArh_anoms'+CLMlab+'_satsHadISDH.'+versiondots+'.txt' CREATED AFTER RH RUN)
#    PosthomogPHAdpd_anoms'+CLMlab+'_satsHadISDH.'+versiondots+'.txt' CREATED AFTER DPD RUN)
# Input homogenised ascii data
#  /scratch/hadkw/UPDATE<YYYY>/MONTHLIES/HOMOG/<typee>ASCII/<VAR>DIR/' # this will then be PHAASCII or IDPHAASCII
#    <station>_'_'+typee+'adj.txt'
# Input SLPclims from 20CR in raw station files
#  /scratch/hadkw/UPDATE<YYYY>/MONTHLIES/NETCDF/'
#    StationListID[st][0:6]+'-'+StationListID[st][6:11]+'_hummonthQC.nc'
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# Ensure that you have updated the end year, version, clim period etc or switched HardWire = 0 and F1_HadISDHBuildConfig.txt is up to date
#
# The variables should be run in a specific order:
# T IDPHA first because homogenised t_abs are used to:
#  -> estimate uncertainties in RH, q, e, Td and dpd
# RH IDPHA second because homogenised rh_abs is used to:
#  -> find supersats in q, e
#  -> estimate uncertainties in q, e, Td, and DPD
# DPD PHA third because PosthomogPHAdpd_anoms8110_sats  are used for:
#  -> find supersats in Tw and Td
# homog Td is made up from homog T - homog DPD anyway
# q IDPHA fourth because all dependencies are now complete
# e IDPHA fifth because all dependencies are now complete
# td PHADPD sixth because all dependencies are now complete
# tw IDPHA zeventh because all dependencies are now complete
#
# > module load scitools/default-current
# > python F12_CreateHomogNCDFStUnc --var <var> --typee <type> --runtype <runtype>
#
## Which variable?
# var = 'dpd'	#'dpd','td','t','tw','e','q','rh'
#
## Which homog type?
# typee = 'PHA'	#'PHA' (for DPD only),'IDPHA' (for t, e, q, rh and tw),'PHADPD' (for Td) 
#
## What sort of run?
# runtype = 'all' # runs all stations within the station list
# runtype = '00000099999' # restarts from the given station ID then continues through all stations within the station list
#
#
# Or ./F12_submit_spice.sh
# 
# -----------------------
# OUTPUT
# -----------------------
# Output lists of good, bad, supersaturated and subzero stations
#  /scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/
#    Posthomog<typee><var>_anoms'+CLMlab+'_<goods,bads,sats,subs>HadISDH.'+versiondots+'.txt' 
# Output homogenised netCDF data
#  /scratch/hadkw/UPDATE<YYYY>/MONTHLIES/HOMOG/<typee>NETCDF/<VAR>DIR/' # this will then be PHANETCDF or IDPHANETCDF
#    <station>'_anoms<climLAB>_homog.nc'
# Output uncertainty plots
#  /scratch/hadkw/UPDATE<YYYY>/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/<VAR>DIR/' 
#    <station>'_anoms<climLAB>_stationstats.png'
# Output log info
#  /scratch/hadkw/OutputLogFile'+versiondots+'.txt'
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
#
# Version 5 (12 January 2021)
# ---------
#  
# Enhancements
# Now only outputs stations that are 'good' or do not have subzeros or supersaturated values. These stations are
# listed in seperate files with all being in the 'BAD' station list then repeated in the SATS and SUBS files
# THis doesn't change the final grids but means that we no longer need to faff around pulling out the sats and subs stations
#  
# Changes
# This is now python 3 rather than IDL
# Climatology now calculated where >= 15 years represented for each month, not > 15 - so a few more stations get through.
# Tw supersats set to when DPD has a supersat (station removed from further processing) so far fewer Tw supersats now found (was Tw > T)
# Now pulls through monthly standard deviations too
# Calculates the pseudo e, q, Td with correction to use ice bulb when Twet <= 0 .Twet calculated from T which is set to 5. in case of missing
# so will result in wet bulb (too high e) in some cases where it should be ice
# T values only differ due to missed adjustment error
# RH values only differ due to missed adjustment error
# DPD values differ due to missed adjustment error AND measurement error which is now lower when pseudoTwet is <= 0 and so the ice bulb calc for e is used
# q values only differ due to the missed adjustment error
# e as for q
# Tw very similar - values only differ due to missed adjustment error. Supersats are now those found from DPD not Tw>T - so far fewer supersats.
# Td now has own list of sats and bads assessed rather than copied from DPD and T and differs in adj error
#
#  
# Bug fixes
#
#
# Version 4 (8 February 2018)
# ---------
#  
# Enhancements
# Now reads in station counts and missed adjustment uncertainty automatically so no updating required.
# Now runs variable/homogtype from the command line so no updating beyond year required
### Which variable? T first, RH, DPD, q, e, td, tw
#param =      'tw'
## Which homog type?
#homogtype =  'ID'		#'ID','DPD' for Td, 'PHA' - req for DPD or PHA versions of all variables
#  
# Changes
#  
# Bug fixes
#
# Version 3 (31 January 2017)
# ---------
#  
# Enhancements
# General tidy up of code and input variable format
#  
# Changes
#  
# Bug fixes
# 
# Version 2 (12 August 2015)
# ---------
#  
# Enhancements
# Improved header
# Added capacity to output using different climatology period 1981-2010
# Rearranged file input structure to account for choices of climatolgoy period
# Tidied up code generally and tried to fix some oddities (changes)
#  
# Changes
# NOT SURE WHY BUT FOR UNCERTAINTY IN Td and DPD it tries to read in raw T and station_Pclim but
# as it was would fail and set statP_arr to standard pressure of 1013. I have changed so that it reads in 20CRstation_Pclim 
# and no raw T (homog T already read in)
# ALSO - not really sure why DPD has to come first so that it then needs to read in unhomogenised Td - need to go through code again really
#  
# Bug fixes
# RH subzeros not listed properly - were added to supersats and labelled as supersats
# This has resulted in 1 fewer sat and 1 new sub for RH (anoms8110)
# missed adjustment for e was 0.12 but should have been 0.2!!!
#
#
# Version 1 (15 January 2015)
# ---------
#  
# Enhancements
#  
# Changes
#  
# Bug fixes
#  
# -----------------------
# OTHER INFORMATION
# -----------------------
##measurement uncertainty for obs_error:
# For RH sensors this is approximatly 2% at 10% RH and 2.5% at 98% RH
# For psychormeters we can assume 0.3 deg C wetbulb depession
# This scales out as:
# -50 deg C = 30% 0 deg C = 5.8% RH, 50 deg = 1.2% RH	- 
# -50 = 30%
# -40 = 30%
# -30 = 30%
# -20 = 20%
# -10 = 10%
#   0 = 6%
#  10 = 4%
#  20 = 2.5%
#  30 = 1.8%
#  40 = 1.4%
#  50+ = 1.2% 

# give all 40-50 1.4%
# give all 0-10 6%  (apply upwards bin)
# USED Michael de Podesta's spread sheet with eq. (ice and wet) from Buck 1981 (my thesis ch 2)
# so - read in temperature netcdfs for climatology - scale errors with climatology or raw values?
# scale with raw - may lead to change over time as temperatures change?
#  - may also lead to biases where adjustments have been made as T is not homog.
# scale with clim - continuous over time but a little coarse? Although pos and neg should balance out?
# penalise cold months - but that IS where we're least certain
# AT GRIDBOX level this could scale with time too - introduce some change to RH sensor uncertainty beginning in 1990s to
# be almost complete by 2011? Tricky and a bit arbitray - at least doing all using wetbulb uncertainty is a 'worst case'


#******************************************************
# Global variables and imports
# Inbuilt: (may not all be required actually)
import numpy as np # used
import numpy.ma as npm # used
from datetime import datetime # used
import matplotlib.pyplot as plt
import sys, os, getopt # used
import struct
import glob # used
import pdb # used
import netCDF4 as nc4
#from netCDF4 import Dataset # used
from subprocess import call, check_output, run, PIPE # used

# Kate's Functions
import CalcHums
from RandomsRanges import LetterRange

# Restarter station ID
RestartValue = '-----------' # '00000099999'

# Start and end years if HardWire = 1
styear       = 1973
edyear       = 2019

# Dataset version if HardWire = 1
versiondots    = '4.2.0.2019f'
version    = 'v420_2019f'
hadisdversiondots = '3.1.0.2019f'
hadisdversion = 'v310_2019f'

# HARDWIRED SET UP!!!
# If HardWire = 1 then program reads from the above run choices
# If HardWire = 0 then program reads in from F1_HadISDHBuildConfig.txt
HardWire = 0

if (HardWire == 0):
    
    #' Read in the config file to get all of the info
    with open('F1_HadISDHBuildConfig.txt') as f:
        
        ConfigDict = dict(x.rstrip().split('=', 1) for x in f)
    
    versiondots = ConfigDict['VersionDots']
    hadisdversiondots = ConfigDict['HadISDVersionDots']
    styear = ConfigDict['StartYear']
    edyear = ConfigDict['EndYear']

# AttribDict held in memory to probide global attribute text later
#' Read in the attribute file to get all of the info
with open('F1_HadISDHBuildAttributes.txt') as f:
    
    AttribDict = dict(x.rstrip().split('=', 1) for x in f)

# NOT CODED THIS FUNCTIONALITY YET
## Are we working with homogenised actuals (True) or anomalies (False)?
#Actuals = True

# Set up directories locations
updateyy  = str(edyear)[2:4]
updateyyyy  = str(edyear)
workingdir  = '/scratch/hadkw/UPDATE'+updateyyyy
#workingdir  = '/data/users/hadkw/WORKING_HADISDH/UPDATE'+updateyyyy

# Set up filenames
INDIRLIST = workingdir+'/LISTS_DOCS/'
INDIRHOM = workingdir+'/MONTHLIES/HOMOG/' # this will then be PHAASCII or IDPHAASCII
INDIRP = workingdir+'/MONTHLIES/NETCDF/'

#workingdir  = '/scratch/hadkw/UPDATE'+updateyyyy
OUTDIRLIST = workingdir+'/LISTS_DOCS/'
OUTDIRHOM = workingdir+'/MONTHLIES/HOMOG/' # this will then be PHANETCDF or IDPHANETCDF
OUTDIRPLOTS = workingdir+'/MONTHLIES/HOMOG/STAT_PLOTS/UNCPLOTS/' 
# File for output stats but also for reading in missed adjustment uncertainties
OUTPUTLOG = workingdir+'/LISTS_DOCS/OutputLogFile'+versiondots+'.txt'

# Set up variables
MDI = -1e+30
#*** at some point add all the header info from the new HadISD files***

# Dictionaries for param, units, homogdirprefix, STATION FILE PREFIX, standard name, long name, raw data suffix(only for test run)
ParamDict = dict([('q',['q','g/kg','IDPHA','Q','specific_humidity','monthly mean 2m specific humidity','qhum']),
	          ('rh',['RH','%rh','IDPHA','RH','relative_humidity','monthly mean 2m relative humidity','rhum']),
	          ('t',['T','deg C','IDPHA','T','drybulb_temperature','monthly mean 2m dry bulb temperature','temp']), # Note this needs to be changed to IDPHAMG later
	          ('td',['Td','deg C','IDPHA','TD','dewpoint_temperature','monthly mean 2m dew point temperature','dewp']),
	          ('tw',['Tw','deg C','IDPHA','TW','wetbulb_temperature','monthly mean 2m wetbulb temperature','twet']),
	          ('e',['e','hPa','IDPHA','E','vapour_pressure','monthly mean 2m vapour pressure','evap']),
	          ('dpd',['DPD','deg C','PHA','DPD','dewpoint depression','monthly mean 2m dew point depression','ddep'])])

#******************************************************
# SUBROUTINES #
#******************************************************
# READDATA
def ReadData(FileName,typee,delimee):
    ''' Use numpy genfromtxt reading to read in all rows from a complex array '''
    ''' Need to specify format as it is complex '''
    ''' outputs an array of tuples that in turn need to be subscripted by their names defaults f0...f8 '''
    return np.genfromtxt(FileName, dtype=typee, delimiter=delimee, encoding='latin-1') # ReadData
#    return np.genfromtxt(FileName, dtype=typee, delimiter=delimee) # ReadData

#****************************************************
# MakeDaysSince
def MakeDaysSince(TheStYr,TheStMon,TheEdYr,TheEdMon):
    ''' Take counts of months since styr, stmn (assume 15th day of month) '''
    ''' Work out counts of days since styr,stmn, January - incl leap days '''
    ''' Also work out time boundaries 1st and last day of month '''
    ''' This can cope with incomplete years or individual months '''
    
    # set up arrays for month month bounds
    BoundsArray = np.empty((((TheEdYr-TheStYr)+1)*((TheEdMon-TheStMon)+1),2))
    
    # make a date object for each time point and subtract start date
    StartDate = datetime(TheStYr,TheStMon,1,0,0,0)	# January
    
    DaysArray = list(np.array([[(datetime(j,i,1,0,0,0)-StartDate).days + 15 for i in np.arange(1,13)] for j in np.arange(TheStYr,TheEdYr+1)]).flat)
    BoundsArray[:,0] = list(np.array([[(datetime(j,i,1,0,0,0)-StartDate).days for i in np.arange(1,13)] for j in np.arange(TheStYr,TheEdYr+1)]).flat)
    BoundsArray[:,1] = np.append(BoundsArray[1:,0]-1,(datetime(TheEdYr,TheEdMon,31,23,59,59)-StartDate).days)
            
    return DaysArray,BoundsArray

#**************************************************************************************
# WriteNetCDF
def WriteNetCDF(FileName,TheStYr,TheEdYr,TheClims,TheDataList,DimObject,AttrObject,GlobAttrObject,TheMDI):
    ''' WRites NetCDF4 '''
    ''' Sort out the date/times to write out and time bounds '''
    ''' Write to file, set up given dimensions, looping through all potential variables and their attributes, and then the provided dictionary of global attributes '''

#    # Attributes and things common to all vars
#    add_offset = -100.0 # storedval=int((var-offset)/scale)
#    scale_factor = 0.01
    
    # Sort out date/times to write out
    TimPoints,TimBounds = MakeDaysSince(int(TheStYr),1,int(TheEdYr),12)
    nTims = len(TimPoints)
    MonthName = ['January   ',
                 'February  ',
	         'March     ',
	         'April     ',
	         'May       ',
	         'June      ',
	         'July      ',
	         'August    ',
	         'September ',
	         'October   ',
	         'November  ',
	         'December  ']
	
    # Create a new netCDF file - have tried zlib=True,least_significant_digit=3 (and 1) - no difference
    ncfw = nc4.Dataset(FileName,'w',format='NETCDF4_CLASSIC') # need to try NETCDF4 and also play with compression but test this first
    
    # Write out the global attributes
    if ('description' in GlobAttrObject):
        ncfw.description = GlobAttrObject['description']
	#print(GlobAttrObject['description'])
	
    if ('File_created' in GlobAttrObject):
        ncfw.File_created = GlobAttrObject['File_created']

    if ('Title' in GlobAttrObject):
        ncfw.Title = GlobAttrObject['Title']

    if ('Institution' in GlobAttrObject):
        ncfw.Institution = GlobAttrObject['Institution']

    if ('History' in GlobAttrObject):
        ncfw.History = GlobAttrObject['History']

    if ('Licence' in GlobAttrObject):
        ncfw.Licence = GlobAttrObject['Licence']

    if ('Project' in GlobAttrObject):
        ncfw.Project = GlobAttrObject['Project']

    if ('Processing_level' in GlobAttrObject):
        ncfw.Processing_level = GlobAttrObject['Processing_level']

    if ('Acknowledgement' in GlobAttrObject):
        ncfw.Acknowledgement = GlobAttrObject['Acknowledgement']

    if ('Source' in GlobAttrObject):
        ncfw.Source = GlobAttrObject['Source']

    if ('Comment' in GlobAttrObject):
        ncfw.Comment = GlobAttrObject['Comment']

    if ('References' in GlobAttrObject):
        ncfw.References = GlobAttrObject['References']

    if ('Creator_name' in GlobAttrObject):
        ncfw.Creator_name = GlobAttrObject['Creator_name']

    if ('Creator_email' in GlobAttrObject):
        ncfw.Creator_email = GlobAttrObject['Creator_email']

    if ('Version' in GlobAttrObject):
        ncfw.Version = GlobAttrObject['Version']

    if ('doi' in GlobAttrObject):
        ncfw.doi = GlobAttrObject['doi']

    if ('Conventions' in GlobAttrObject):
        ncfw.Conventions = GlobAttrObject['Conventions']

    if ('netcdf_type' in GlobAttrObject):
        ncfw.netcdf_type = GlobAttrObject['netcdf_type']
	
    # Loop through and set up the dimension names and quantities
    for vv in range(len(DimObject[0])):
        ncfw.createDimension(DimObject[0][vv],DimObject[1][vv])
	
    # Go through each dimension and set up the variable and attributes for that dimension if needed
    for vv in range(len(DimObject)-2): # ignore first two elements of the list but count all other dictionaries
#        print(DimObject[vv+2]['var_name'])
	
	# NOt 100% sure this works in a loop with overwriting
	# initiate variable with name, type and dimensions
        MyVar = ncfw.createVariable(DimObject[vv+2]['var_name'],DimObject[vv+2]['var_type'],DimObject[vv+2]['var_dims'])
        
	# Apply any other attributes
        if ('standard_name' in DimObject[vv+2]):
            MyVar.standard_name = DimObject[vv+2]['standard_name']
	    
        if ('long_name' in DimObject[vv+2]):
            MyVar.long_name = DimObject[vv+2]['long_name']
	    
        if ('units' in DimObject[vv+2]):
            MyVar.units = DimObject[vv+2]['units']
		   	 
        if ('axis' in DimObject[vv+2]):
            MyVar.axis = DimObject[vv+2]['axis']

        if ('calendar' in DimObject[vv+2]):
            MyVar.calendar = DimObject[vv+2]['calendar']

        if ('start_year' in DimObject[vv+2]):
            MyVar.start_year = DimObject[vv+2]['start_year']

        if ('end_year' in DimObject[vv+2]):
            MyVar.end_year = DimObject[vv+2]['end_year']

        if ('start_month' in DimObject[vv+2]):
            MyVar.start_month = DimObject[vv+2]['start_month']

        if ('end_month' in DimObject[vv+2]):
            MyVar.end_month = DimObject[vv+2]['end_month']

        if ('bounds' in DimObject[vv+2]):
            MyVar.bounds = DimObject[vv+2]['bounds']
	
	# Provide the data to the variable
        if (DimObject[vv+2]['var_name'] == 'time'):
            MyVar[:] = TimPoints

        if (DimObject[vv+2]['var_name'] == 'bounds_time'):
            MyVar[:,:] = TimBounds

        if (DimObject[vv+2]['var_name'] == 'month'):
#            pdb.set_trace()
#            MyVar[mm,:] = [nc4.stringtochar(np.array(MonthName[mm],dtype='S10')) for mm in np.arange(1,13)] 
            MyVar[:,:] = [[MonthName[mm][cc] for cc in range(10)] for mm in range(12)] 

    # Go through each variable and set up the variable attributes
    for vv in range(len(AttrObject)): # ignore first two elements of the list but count all other dictionaries

#        print(AttrObject[vv]['var_name'])

        # initiate variable with name, type and dimensions
        MyVar = ncfw.createVariable(AttrObject[vv]['var_name'],AttrObject[vv]['var_type'],AttrObject[vv]['var_dims'],fill_value = TheMDI)
        
	# Apply any other attributes
        if ('long_name' in AttrObject[vv]):
            MyVar.long_name = AttrObject[vv]['long_name']
	    
        if ('units' in AttrObject[vv]):
            MyVar.units = AttrObject[vv]['units']

#        MyVar.add_offset = add_offset
#        MyVar.scale_factor = scale_factor

        MyVar.reference_period = str(TheClims[0])+', '+str(TheClims[1])

	# Provide the data to the variable - depending on howmany dimensions there are
	## First change masked array to normal array filled with MDI
        #TheDataList[vv][TheDataList[vv].mask] = TheMDI
        MyVar[:] = TheDataList[vv].filled()
	    
    ncfw.close()
   
    return # WriteNCCF

#*******************************************************
# MAIN #
#*******************************************************
def main(argv):

    # INPUT PARAMETERS AS STRINGS!!!!
    var = 'q'	    # 'q','rh','e','td','tw','t','dpd'
    typee = 'IDPHA' # 'PHA','IDPHA','PHADPD'
    runtype = 'all' # 'all','00000099999'

    try:
        opts, args = getopt.getopt(argv, "hi:",
	                           ["var=","typee=","runtype="])
    except getopt.GetoptError:
        print('Usage (as strings) F12_CreateHomogNCDFStUnc.py --var <q> --typee <IDPHA> --runtype <all>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--var":
            try:
                var = arg
            except:
                sys.exit("Failed: var not a string")
        elif opt == "--typee":
            try:
                typee = arg
            except:
                sys.exit("Failed: typee not a string")
        elif opt == "--runtype":
            try:
                runtype = arg
            except:
                sys.exit("Failed: typee not a string")
 
#    assert var != '' and typee != '', "Input values not specified."

    print(var,typee,runtype)
    
    # Check to see if we're starting from the beginning?
    if (RestartValue == '-----------') & (runtype != 'all'):
 
        # Restarter set from run command line variables
        RestartID = runtype   

    else:
    
        RestartID = RestartValue
	
    # Which climatology?
    MYclst = 1981	# 1976, 1981
    MYcled = 2010	# 2005, 2010
    CLMlab = str(MYclst)[2:4]+str(MYcled)[2:4]

#*******************************************************
    # variable specific filepaths and directories
    # homogenised data file suffix
    DatSuffix = '_anoms'+CLMlab+'_homog.nc'

    # Needs to be IDPHAMG for T for the log of adjustments and MissedAdjErr
    homogtype = typee
    if (var == 't'):
        homogtype = 'IDPHAMG'

    # Set up files for read in and write out
    
#    InList = INDIRLIST+'goodforHadISDH.'+versiondots+'_'+typee+var+'_JAN2020.txt'
    InList = INDIRLIST+'goodforHadISDH.'+versiondots+'_'+typee+var+'.txt'
    
    InHom = INDIRHOM+ParamDict[var][2]+'ASCII/'+ParamDict[var][3]+'DIR/'	    #***
    # Diretories to read in homog T and RH for finding measurement uncertainty
    InHomT = INDIRHOM+'IDPHAASCII/TDIR/'	    #***
    InHomRH = INDIRHOM+'IDPHAASCII/RHDIR/'	    #***
    # Note that homogtype is set to IDPHAMG for T (see above)
#    InLog = INDIRLIST+'HadISDH.land'+ParamDict[var][0]+'.'+versiondots+'_'+homogtype+'_JAN2020.log'     #***
    InLog = INDIRLIST+'HadISDH.land'+ParamDict[var][0]+'.'+versiondots+'_'+homogtype+'.log'     #***
    
    OutList = OUTDIRLIST+'Posthomog'+typee+var+'_anoms'+CLMlab+'_goodsHadISDH.'+versiondots+'.txt'
    OutFunniesT = OUTDIRLIST+'Posthomog'+typee+var+'_anoms'+CLMlab+'_satsHadISDH.'+versiondots+'.txt'
    OutFunniesZ = OUTDIRLIST+'Posthomog'+typee+var+'_anoms'+CLMlab+'_subzerosHadISDH.'+versiondots+'.txt'
    INRHSATS = OUTDIRLIST+'PosthomogIDPHArh_anoms'+CLMlab+'_satsHadISDH.'+versiondots+'.txt'
    INDPDSATS = OUTDIRLIST+'PosthomogPHAdpd_anoms'+CLMlab+'_satsHadISDH.'+versiondots+'.txt'
    OutBads = OUTDIRLIST+'Posthomog'+typee+var+'_anoms'+CLMlab+'_badsHadISDH.'+versiondots+'.txt'

    #OutDat = OUTDIRHOM+typee+'NETCDF/'+ParamDict[var][3]+'DIR/'
    # I think this works for Td and DPD so not need to Td special case loop below (Td read and write from to IDPHAASCII IDPHANETCDF...
    OutDat = OUTDIRHOM+ParamDict[var][2]+'NETCDF/'+ParamDict[var][3]+'DIR/'
    OutPlots = OUTDIRPLOTS+ParamDict[var][3]+'DIR/'

    homsuffix = '_'+typee+'adj.txt'

    # Special case for Td    
    if (typee == 'PHADPD'):

        homsuffix = '_PHAadj.txt'
#        OutDat = OUTDIRHOM+'IDPHANETCDF/'+ParamDict[var][3]+'DIR/'
#        # I'm not copying over from DPD anymote

#--------------------------------------------------------
    # other variables and arrays 
    clst =     MYclst - int(styear)
    cled =     MYcled - int(styear)
    nyrs =     (int(edyear) + 1) - int(styear)
    nmons =    nyrs * 12
    # Save netCDF file as days since 01-01-1973 DD-MM-YYYY

    # UNCERTAINTIES IN MEASUREMENT
    RHBins = [-100,-40,-30,-20,-10,0,10,20,30,40,50,100]	# degrees C

    # 1 sigma (THIS IS LATER *2 TO PROVIDE 2 SIGMA UNCS)
    RHUnc =  [15,15,15,10,5,2.75,1.8,1.35,1.1,0.95,0.8] 
    t_unc =  0.2
    tw_unc = 0.15

# Find the missed adjustment uncertainty from the Adjs_Stats file for variable and homogtype
    moo = check_output(['grep','-a','^'+var+'_'+homogtype+'_STD_GAUSSDIFFS=',OUTPUTLOG])
    # Now sort out this string which is a byte array, remove newline and split
    moo = moo.decode("utf-8").strip('\n').split('=')	
#    print('Check read in of missed adjustment')
#    pdb.set_trace()
    
    MissedAdjErr = float(moo[1]) # THIS IS 1 SIGMA AND LATER * 2 TO PROVIDE 2 SIGMA UNCS
    
#*************************************************************
# Work through station by station
#*************************************************************
    
    # Open and read in station list 
    MyTypes         = ("|U11","float","float","float","|U1","|U2","|U1","|U29","|U13")
    MyDelimiters    = [11,8,10,7,1,2,1,29,13]
    RawData         = ReadData(InList,MyTypes,MyDelimiters)
    StationListID  = np.array(RawData['f0'])
    StationListLat  = np.array(RawData['f1'])
    StationListLon  = np.array(RawData['f2'])
    StationListElev = np.array(RawData['f3'])
    StationListCID  = np.array(RawData['f5'])
    StationListName = np.array(RawData['f7'])
    nstations       = len(StationListID)
    #print('Test to see if station read in has worked correctly and whether there is a more efficient method')
    #pdb.set_trace()

    # loop through station by station
    for st in range(nstations):

        # check if restart necessary
        if RestartID != '-----------' and RestartID != StationListID[st]:
            continue

        RestartID = '-----------'
    
        # find homog file for selected variable and read in to array 
        InFile = InHom+StationListID[st]+homsuffix
        MyTypes = np.append("|U12",["int"]*13)
        MyDelimiters = np.append([12,4,6],[7]*11)
        RawData      = ReadData(InFile,MyTypes,MyDelimiters)
        
        stat_abs = npm.array(()) # initiate empty masked array to append to
        for yy in range(nyrs):
            
            moo = list(RawData[yy])
            stat_abs = npm.append(stat_abs,np.copy(npm.array(moo[2:14])/100.)) 

#        print('Check file read in: ',StationListID[st])
#        pdb.set_trace()  
  
        # Initiate other masked arrays
        stat_anoms = npm.repeat(MDI,nmons)
        stat_sds = npm.repeat(MDI,nmons) # to be filled at end
        stat_clims = npm.repeat(MDI,12)
        stat_clim_sds = npm.repeat(MDI,12)
        stat_adjs = npm.repeat(0.,nmons)
        stat_adjs_err = npm.repeat(0.,nmons)
        stat_clims_err = npm.repeat(MDI,nmons)
        stat_obs_err = npm.repeat(MDI,nmons)
        station_err = npm.repeat(MDI,nmons)

        # Use masked arrays  so set the old MDI which is now -99.99 to the new MDI which is -1e30 then convert to masked
        stat_abs[stat_abs == -99.99] = MDI
        stat_abs = npm.masked_equal(stat_abs, MDI) # should not fall over if there are no missing values
#        print('Check masking of stat_abs array')
#        pdb.set_trace()
	    
#*******************************************************************************
# Find subzeros and supersats (if relevant to variable), output to releavnt lists and then move on to next station
#*******************************************************************************
        
	# DO NOT PROCESS THE STATION ANY FURTHER AS ITS NOW CONSIDERED A BAD!!!
        # No relevance for T
        # subsats - RH, q, e should not be less than zero 
        # supersats - RH should not be greater than 100
        #             DPD should not be less than zero (derived Td then fine)
        #             Td should not be greater than T - using same listing as for DPD
        #             Tw should not be greater than T
	# COULD TRANSFER PROBLEMS IN RH or DPD TO ALL VARIABLES
        # FIND HOMOGENISED FILE IF IT EXISTS
  
        # No need to look for subs and sats if its T
        if (var != 't'):   
	    
            GotSats = False
            GotSubs = False
	    
            # for rh sats where RH > 100. and subs where RH < 0.
            if (var == 'rh'):
	        
                if (len(np.where(stat_abs.compressed() > 100.)[0]) > 0):
		#if (len(stat_abs[(stat_abs > MDI) & (stat_abs > 100.)]) > 0):

                    print('Found supersats!')
                    #GotSats = len(stat_abs[(stat_abs > MDI) & (stat_abs > 100.)])
                    GotSats = len(np.where(stat_abs.compressed() > 100.)[0])
		    		
                if (len(np.where(stat_abs.compressed() < 0.)[0]) > 0):
                #if (len(stat_abs[(stat_abs > MDI) & (stat_abs < 0.)]) > 0):

                    print('Found subzeros!')
                    GotSubs = len(np.where(stat_abs.compressed() < 0.)[0])
                    #GotSubs = len(stat_abs[(stat_abs > MDI) & (stat_abs < 0.)])
	    	
	    # For dpd sats where dpd < 0
            elif (var == 'dpd'):	
              
                if (len(np.where(stat_abs.compressed() < 0.)[0]) > 0):
                #if (len(stat_abs[(stat_abs > MDI) & (stat_abs < 0.)]) > 0):

                    print('Found supersats!')
                    GotSats = len(np.where(stat_abs.compressed() < 0.)[0])
                    #GotSats = len(stat_abs[(stat_abs > MDI) & (stat_abs < 0.)])
	    		
	    # for q or e subs if q or e < 0 and if RH station listed as sat
            elif (var == 'q') or (var == 'e'):

                if (len(np.where(stat_abs.compressed() < 0.)[0]) > 0):
                #if (len(stat_abs[(stat_abs > MDI) & (stat_abs < 0.)]) > 0):

                    print('Found subzeros!')
                    GotSubs = len(np.where(stat_abs.compressed() < 0.)[0])  	
                    #GotSubs = len(stat_abs[(stat_abs > MDI) & (stat_abs < 0.)])    	

                # Look for the station string in the RH list? - NOTE CHECK_OUTPUT WILL FAIL IF IT CAN@T FIND ANYTHING
                moo = run(['grep','-a','^'+StationListID[st],INRHSATS],stdout=PIPE)
                if (moo.returncode == 0): # then we've found the station
                  
                    print('Found supersats!')
                    GotSats = 'RH supersats found '+moo.stdout.decode('utf-8').split()[1]
#                    pdb.set_trace()
	    	
            # for td sats if DPD station listed as sat
            elif (var == 'td'):

                # Look for the station string in the RH list? - NOTE CHECK_OUTPUT WILL FAIL IF IT CAN@T FIND ANYTHING
                moo = run(['grep','-a','^'+StationListID[st],INDPDSATS],stdout=PIPE)
                if (moo.returncode == 0): # then we've found the station
                  
                    print('Found supersats!')
                    GotSats = 'DPD supersats found '+moo.stdout.decode('utf-8').split()[1]
#                    pdb.set_trace()
	    
	    # for tw sats if tw > t so need to read in t or just use dpd? Tw is very sensitive to this so it kicks out A LOT of stations
            elif (var == 'tw'):	
	
                # Look for the station string in the RH list? - NOTE CHECK_OUTPUT WILL FAIL IF IT CAN@T FIND ANYTHING
                moo = run(['grep','-a','^'+StationListID[st],INDPDSATS],stdout=PIPE)
                if (moo.returncode == 0): # then we've found the station
                  
                    print('Found supersats!')
                    GotSats = 'DPD supersats found '+moo.stdout.decode('utf-8').split()[1]
#                    pdb.set_trace()	    

            # If we've got a supersat - write out station to list of supersats
            if (GotSats):
                filee = open(OutFunniesT,'a+')
                filee.write('%s %s\n' % (StationListID[st],GotSats))
                filee.close()
	        # Do we need to list as bads too?
                filee = open(OutBads,'a+')
                filee.write('%s %s\n' % (StationListID[st], 'Supersaturation found'))
                filee.close()

            # If we've got a subzero - write out station to list of subzeros
            if (GotSubs):
                filee = open(OutFunniesZ,'a+')
                filee.write('%s %s\n' % (StationListID[st],GotSubs))
                filee.close()
	        # Do we need to list as bads too?
                filee = open(OutBads,'a+')
                filee.write('%s %s\n' % (StationListID[st], 'Subzero found'))
                filee.close()

            # Now stop processing this station if we've found a sat or sub
            if (GotSats) or (GotSubs):
                print('Stopping processing station: ',StationListID[st])
                continue	 
	    
#******************************************************************
# create station anomalies and climatologies from homogenised abs
#******************************************************************
        
	# reshape the array to be a row for each year
        stat_abs = np.reshape(stat_abs,(nyrs,12)) 
        # subset the values to just the climatology period
        subclm = stat_abs[clst:cled+1,:] 
        
	# Are there enough years (>= 15) for each month? There must be a climatology value for each month to continue processing station
        if (npm.sum(npm.count(subclm,0) >= 15) < 12): # counts for each valid month over the 30 year period, sums these counts and enters loop if at least 1 count is less than 15

            # No there are not for at least one month so write out to bad station file and cease processeing
            print('At least one month has too few values to calculate a climatology')
            filee = open(OutBads,'a+')
            filee.write('%s %s %i\n' % (StationListID[st], 'Too few months for a climatology', np.sum(npm.count(subclm,0) >= 15)))
            filee.close()
            #pdb.set_trace()
            continue
	     	
	# Calculate climatology, climatological standard deviation and anomalies
        stat_clims = npm.mean(subclm,0) # compute the mean over each 30 year slice for each month, ignoring missing data 
        # Note that np.std assumes we're calculating st dev from whole population where as IDL assumes sample of population so deg_of_freedom = n-1
	# To match with previous IDL code, and because very often we have missing data, set ddof = 1 to use n-1
        stat_clim_sds = npm.std(subclm,0,ddof=1) # compute the stdeviation over each 30 year slice for each month, ignoring missing data 
        stat_anoms = stat_abs - stat_clims # this substracts the right month clim from the right month actual, ignoring missing data

#**# CALCULATE CLIMATOLOGY UNCERTAINTY - ***2-SIGMA***    
        stat_clims_err = np.tile((stat_clim_sds / np.sqrt(npm.count(subclm,0))) * 2, [nyrs,1])
	# Mask the uncertainty array with the same missing values
        stat_clims_err[stat_abs.mask] = MDI
        stat_clims_err = npm.masked_equal(stat_clims_err, MDI) # should not fall over if there are no missing values
	
	# Reshape the arrays ready to write to file
        stat_abs = np.reshape(stat_abs, 12 * nyrs)
        stat_anoms = np.reshape(stat_anoms, 12 * nyrs)
        stat_clims_err = np.reshape(stat_clims_err, 12 * nyrs)
	
#        print('Completed anomalies and climatology error - check')
#        pdb.set_trace()
	
#********************************************************************	
# Work out the relative measurement uncertainty - ***2 SIGMA***
#********************************************************************
        
	# Find right variable to process
        if (var == 't'):
	
            # Easy for T - +/- 0.2 deg - this is 1 sigma so multiply by 2
            stat_obs_err[:] = (t_unc / np.sqrt(60.)) * 2 	#  minimum number of obs per month is 15 days * 4 obs per day = 60 for single station within gridbox 

        elif (var == 'tw'):
	
            # Easy for Tw - +/- 0.15 deg - this is 1 sigma so multiply by 2 - WET BULB ERROR pre 1980 (mostly)
            # 15%rh at -50 deg C T, 0.8 %rh at 50 deg C T
            # scale all error based on %rh at T
            stat_obs_err[:] = (tw_unc / np.sqrt(60.)) * 2 	#  minimum number of obs per month is 15 days * 4 obs per day = 60 for single station within gridbox 

        elif (var == 'rh'):
	
            # FOR RH - easy - bin from -50 to 50 deg C and apply table of %rh errors based on 0.15 deg C error in Tw - multiply by 2 to give 2 sigma unc
	    # If T file exists then read in T_abs homogenise
            if (len(glob.glob(InHomT+StationListID[st]+'_IDPHAadj.txt')) == 1):
               
                InFile = InHomT+StationListID[st]+'_IDPHAadj.txt'
                RawData = ReadData(InFile,MyTypes,MyDelimiters)
                stat_absT = npm.array(()) # initiate empty masked array to append to
                for yy in range(nyrs):
            
                    moo = list(RawData[yy])
                    stat_absT = npm.append(stat_absT,np.copy(npm.array(moo[2:14])/100.)) 

                # Set all missing values to 5. degrees which will map to a 2.75% RH uncertainty (>= 0. and < 10. deg) - may be months where T was removed by PHA so still present in RH
                stat_absT[stat_absT == -99.99] = 5. 

                # Loop through RH bins start to penultimate bin
                for b,binn in enumerate(RHBins[:-1]):
		
                    # Set T to the RH Uncertainty for the associated level of T in RHBins and compute uncertainty
                    stat_obs_err[(stat_absT >= binn) & (stat_absT < RHBins[b+1])] = (RHUnc[b] / np.sqrt(60.)) * 2. #  minimum number of obs per month is 15 days * 4 obs per day = 60 for single station within gridbox 		

#                print('Check the RH unc aligns with T bins')
#                pdb.set_trace()
		            
	    # No T file exists - # NO TEMPERATURE DATA SO ASSUME MODERATE UNCERTAINTY OF 3%
            else:
	    
                stat_obs_err[:] = (2.75 / np.sqrt(60.)) * 2 	#  minimum number of obs per month is 15 days * 4 obs per day = 60 for single station within gridbox 

        else: # var is q, e, td or dpd
	
            # FOR q or e or Td: (ASSUME RH=80% IF NO RH FILE/OB EXISTS, and 2.75%rh uncertainty IF NO TEMPERATURE FILE/OB EXIST - set T = 5. to get that [>=0.<10 deg]) - *2 to get 2sigma
	    # If T file exists then read in T_abs homogenise
            if (len(glob.glob(InHomT+StationListID[st]+'_IDPHAadj.txt')) == 1):
               
                InFile = InHomT+StationListID[st]+'_IDPHAadj.txt'
                RawData = ReadData(InFile,MyTypes,MyDelimiters)
                stat_absT = npm.array(()) # initiate empty masked array to append to
                for yy in range(nyrs):
            
                    moo = list(RawData[yy])
                    stat_absT = npm.append(stat_absT,np.copy(np.array(moo[2:14])/100.)) 

                # Set all missing values to 0 degrees which will map to a 3% RH uncertainty - may be months where T was removed by PHA so still present in RH
                stat_absT[stat_absT == -99.99] = 5. 
		    
            # If no T file then set T values to 0. degrees
            else:

                 stat_absT = npm.repeat(5.,nmons)
		 
	    # If RH file exists then read in RH_abs homogenise
            if (len(glob.glob(InHomRH+StationListID[st]+'_IDPHAadj.txt')) == 1):
               
                InFile = InHomRH+StationListID[st]+'_IDPHAadj.txt'
                RawData = ReadData(InFile,MyTypes,MyDelimiters)
                stat_absRH = npm.array(()) # initiate empty masked array to append to
                for yy in range(nyrs):
            
                    moo = list(RawData[yy])
                    stat_absRH = npm.append(stat_absRH,np.copy(npm.array(moo[2:14])/100.)) 

                # Set all missing values to 80. %rh - may be months where RH was removed by PHA so still present in q
                stat_absRH[stat_absRH == -99.99] = 80. 
		    
            # If no RH file then set RH values to 80. %rh
            else:

                 stat_absRH = npm.repeat(80.,nmons)
		 
            # Get uncertainty for q or e
            # qsat=(q/RH)*100
            # q+err=((RH+err)/100)*qsat
            # qerr=(q+err)-q
            if ((var == 'q') or (var == 'e')):
     	        
		# Set up a pseudo qsat or esat masked array
                sat_array = (stat_abs / stat_absRH) * 100.
	        # Loop through RH bins start to penultimate bin
                for b,binn in enumerate(RHBins[:-1]):
		
                    # Set T to the RH Uncertainty for the associated level of T in RHBins and compute uncertainty
		    # straight RHUnc not /sqrt(60.) because we're pretending this is an individual ob
                    stat_obs_err[(stat_absT >= binn) & (stat_absT < RHBins[b+1])] =  (((((stat_absRH[(stat_absT >= binn) & (stat_absT < RHBins[b+1])] + RHUnc[b]) / 100.) \
		                                                                         * sat_array[(stat_absT >= binn) & (stat_absT < RHBins[b+1])]) \
										          - stat_abs[(stat_absT >= binn) & (stat_absT < RHBins[b+1])]) / npm.sqrt(60.)) * 2.
		    #  minimum number of obs per month is 15 days * 4 obs per day = 60 for single station within gridbox 		

#                print('Check the q / e unc aligns with RH and T bins - masking of stat_abs???')
#                pdb.set_trace()
		
	    # If its Td or DPD then
            # FOR Td: use error in e. (ASSUME RH=80% IF NO RH FILE/OB EXISTS, and 2.75%rh uncertainty IF NO TEMPERATURE FILE/OB EXIST)
            # e=e(Td)
            # esat=(e/RH)*100
            # e+err=((RH+err)/100)*esat
            # Td+err=Td+err(e+err)
            # Tderr=(Td+err)-Td
            else:

                # Need to read in station P from 20CR - that's a pain! - its in the raw station netCDF files
                if (len(glob.glob(INDIRP+StationListID[st][0:6]+'-'+StationListID[st][6:11]+'_hummonthQC.nc')) == 1):
       
                    ncf = nc4.Dataset(INDIRP+StationListID[st][0:6]+'-'+StationListID[st][6:11]+'_hummonthQC.nc','r')
                    # Climatological station level P from 20CR - repeated for each year giving an nmons array
                    P_arr = npm.array(ncf.variables['20CRstation_Pclim'][:]) # do we need to release the pointer?
                    ncf.close()
#                    print('Read in Station P - check')
#                    pdb.set_trace()

                # If the station file doesn't exist then assume standard P of 1013
                else:

                    P_arr = npm.repeat(1013.,nmons)		

                # Now compute the uncertainty in Td
		# Set up a pseudo esat masked array - 
                if (var == 'td'):

		    # We're working with Td so calculating e fairly easy		
		    # we can use T so that the ice bulb equation can be used - if T is set to 5. when it should be < 0. then its going to be wrong
		    # Using wet bulb instead of ice bulb will give slightly higher values of e 
                    # Calculate esat
                    sat_array = (CalcHums.vap(stat_abs, stat_absT, P_arr,roundit=False) / stat_absRH) * 100.

                else: 
	
		    # we're working with DPD so must get Td from T-DPD
		    # Problem when we have set T to 5. and DPD exists because Td could be very wrong - VERY LOW or possibly too high for cold stations/months - can't do much about this
                    # For consistency (its all wrong anyway) we use T here too to choose ice or wet bulb calc
                    # Calculate esat
                    sat_array = (CalcHums.vap((stat_absT-stat_abs), stat_absT, P_arr,roundit=False) / stat_absRH) * 100.
		
		# Loop through RH bins start to penultimate bin
                for b,binn in enumerate(RHBins[:-1]):
		
                    # Set T to the RH Uncertainty for the associated level of T in RHBins and compute e+err
		    # straight RHUnc not /sqrt(60.) because we're pretending this is an individual ob
                    # Calculate e+err=((RH+err)/100)*esat
                    stat_obs_err[(stat_absT >= binn) & (stat_absT < RHBins[b+1])] =  (((stat_absRH[(stat_absT >= binn) & (stat_absT < RHBins[b+1])] + RHUnc[b]) / 100.) \
		                                                                         * sat_array[(stat_absT >= binn) & (stat_absT < RHBins[b+1])])
		    #  minimum number of obs per month is 15 days * 4 obs per day = 60 for single station within gridbox 		

#                print('Check the e+err aligns with RH and T bins')
#                pdb.set_trace()
	
		# Compute Td+err from Td+err(e+err) and then substract Td to get Tderr adn then divide by 60 and * 2 to get 2sigma
                if (var == 'td'):
                    
		    # Working with Td so straightforward 
		    # Again using T to get pseudowetbulb to detect ice bulb - will be a little too high in erroneous wet bulb cases	
                    # Td+err=Td+err(e+err)
                    # Tderr=(Td+err)-Td
                    stat_obs_err = (((CalcHums.td_from_vap(stat_obs_err,P_arr,stat_absT,roundit=False)) - stat_abs) / npm.sqrt(60.) ) * 2.	
		    #  minimum number of obs per month is 15 days * 4 obs per day = 60 for single station within gridbox 		
                
                else:
		
		    # Working with DPD so need to get pseudo Td
                    # Td+err=Td+err(e+err)
                    # Tderr=(Td+err)-Td
                    stat_obs_err = ((CalcHums.td_from_vap(stat_obs_err,P_arr,stat_absT,roundit=False)) - (stat_absT - stat_abs)) # Again using Td instead of T to get pseudowetbulb to detect ice bulb - will be a little too low in erroneous ice cases		
		    # DPD = add 0.2 deg C unc from T on to DPD then *2 to get 2sigma
                    stat_obs_err = ((stat_obs_err + 0.2) / npm.sqrt(60.)) * 2.
		    #  minimum number of obs per month is 15 days * 4 obs per day = 60 for single station within gridbox 		
		    
#                print('Check the Tderr or DPDerr aligns with RH and T bins')
#                pdb.set_trace()
		# This give DPD obs error slightly smaller than the IDL version when T is < or very close to 0. because the ice bulb calculation is used here to convert to vapour pressure

        # Now mask in the missing data
        stat_obs_err[stat_abs.mask] = MDI
        stat_obs_err = npm.masked_equal(stat_obs_err, MDI) # should not fall over if there are no missing values
#	stat_obs_err.mask = stat_abs.mask	    

#*******************************************************************
# RH SENSOR ERROR (post 1980 - progressively) - NOT ADDED YET
#*******************************************************************

#*******************************************************************
# Work on adjustment uncertainties
#*******************************************************************
        
	# read in log and find adjustment uncertainties - apply
#        # Gunzip PHA output file
#        call(['gunzip',InLog+'.gz'])

        # find homog adj for this station and append to array 
        if (homogtype == 'PHA'):
	#PHA - 0=ID, 3=stmon,6=edmon, 8=ibreak, 9=cbreak, 10=adj, 11=eadj 
	
            stmonget = 3
            edmonget = 6
            adjget = 10
            eadj = 11
	    
            moo = check_output(['grep','-a','^Adj write:'+StationListID[st],InLog])
            # Now sort out this string which is a byte array
	    # This creates a list of strings for each adjustment with a blank string at the beginning
            moo = moo.decode("utf-8").split('Adj write:')	

        elif (homogtype == 'IDPHAMG') or (homogtype == 'PHADPD'):
	#IDPHAMG - 0=ID, 2=stmon, 3=edmon, 6=adj, 7=eadj, 8=adj source indicator 

            stmonget = 2
            edmonget = 3
            adjget = 6
            eadj = 7
	    
            moo = check_output(['grep','-a','^'+StationListID[st],InLog])
            # Now sort out this string which is a byte array
	    # This creates a list of strings for each adjustment with a blank string at the beginning
            moo = moo.decode("utf-8").split('\n') # no space	

        else:
	#IDPHA - 0=ID, 2=stmon, 3=edmon, 6=adj, 7=eadj 

            stmonget = 2
            edmonget = 3
            adjget = 6
            eadj = 7
	    	    
            moo = check_output(['grep','-a','^'+StationListID[st],InLog])
            # Now sort out this string which is a byte array
	    # This creates a list of strings for each adjustment with a blank string at the beginning
            moo = moo.decode("utf-8").split(' \n')	

        # Remove the blank string
        moo.remove('')
	# Strip the \n newline characters, random letters and split the strings to make a list of lists
        # b, i, p in IDPHAMG 
        moo = [i.strip(' ABCDEFGHIJKLMNOPQRSTUVWXYZbip\n').split() for i in moo] 
			
	# Now loop through the adjustments to append to array
        # Ignore first line as this is most recent period so adjustment is 0
        for rec,adjstr in enumerate(moo[1:]):
	
            Adj = -(np.copy(np.float(adjstr[adjget])))
            #print(Adj)
	    # these go from 1+, not 0+, first in loop is most recent period - no adjustment here 
            stat_adjs[int(adjstr[stmonget])-1:int(adjstr[edmonget])] = Adj
            # THIS IS A 5th-95th so 1.65 sigma
            # divide by 1.65 then multiply by 2 to get 2sigma error - consistent with everything else then.
            stat_adjs_err[int(adjstr[stmonget])-1:int(adjstr[edmonget])] = np.float(adjstr[eadj]) / 1.65

#        print('Check read in and processing of adjustment and error')
#        pdb.set_trace()
	
#	# gzip PHA output file for tidiness
#        call(['gzip',InLog])

        # add in the flat adjustment error for missed adjustments derived from teh missing middle
        # combine in quadtrature and multiply by 2 to give a 2 sigma error
        stat_adjs_err = (npm.sqrt((stat_adjs_err**2) + (MissedAdjErr**2))) * 2.
	 
        # Now mask in the missing data
        #stat_adjs_err.mask = stat_abs.mask
        #stat_adjs.mask = stat_abs.mask	    
        stat_adjs_err[stat_abs.mask] = MDI
        stat_adjs_err = npm.masked_equal(stat_adjs_err, MDI) # should not fall over if there are no missing values
        stat_adjs[stat_abs.mask] = MDI
        stat_adjs = npm.masked_equal(stat_adjs, MDI) # should not fall over if there are no missing values

#        print('Completed adjustment + MissedAdjErr - check')
#        pdb.set_trace()

#***********************************************************************
# Calc combined station error - ***2 SIGMA***
#***********************************************************************  
        
	# Combine errors in quadrature - should have same mask as obs
        station_err = npm.sqrt(stat_obs_err**2 + stat_clims_err**2 + stat_adjs_err**2) # NOT * 2 as these are already * 2 !!!!! WORKS OUT SAME AS DOIGN 1 SIGMA COMBINED * 2
	
#*******************************************************************************
# Read in monthly standard deviations from unhomogenised NetCDF files and mask to homogenised
#*********************************************************************************

        # File has to be present or we wouldn't be working on it
        ncf = nc4.Dataset(INDIRP+StationListID[st][0:6]+'-'+StationListID[st][6:11]+'_hummonthQC.nc','r')
        # Monthly standard deviation of all hourly values going into the monthly actual value
#        stat_sds = npm.array(ncf.variables[ParamDict[var][6]+'_std'][:]) # do we need to release the pointer?
        stat_sds = npm.array(ncf.variables[var+'_std'][:]) # do we need to release the pointer?
        ncf.close()

        # Use masked arrays with new MDI
        stat_sds[stat_abs.mask] = MDI
        stat_sds = npm.masked_equal(stat_sds, MDI) # should not fall over if there are no missing values
        # Actually because these are the raw (not homogenised!) standard deviations across all hourly data going into the monthly mean
	# the missing data may be less than the homogenised version where periods of ambiguous adjustment are removed
	# So need to mask using stat_abs too - having first ensured that stat_sds is a masked array which I think it was anyway from the netCDF file.
	
	# Check whether masked values that were previously -999 are in fact set to -1e30?
	# Yes - this is done in WriteNetCDF
        
#        print('Check read in of monthly Std values and masking')
#        pdb.set_trace()

#**********************************************************************************
# Write out to good list
#**********************************************************************************

#        pdb.set_trace()
        filee = open(OutList,'a+')
        filee.write('%11s% 9.4f% 10.4f% 7.1f %2s %-29s\n' % (StationListID[st],StationListLat[st], StationListLon[st], StationListElev[st],StationListCID[st],StationListName[st]))
        filee.close()
    	
#*********************************************************************************
# Write out to netCDF file
#************************************************************************************
        
	# NOTE THAT ITS JUST ONE VARIABLE!!!
        # List data together to pass to NetCDF writer
        DataList = [stat_anoms, stat_abs, stat_sds, stat_clims, stat_clim_sds, stat_adjs, stat_adjs_err, stat_clims_err, stat_obs_err, station_err]

        DimList = [['time','month','characters','bound_pairs'],
	           [nmons,12,10,2],
    	           dict([('var_type','f4'),
    		         ('var_name','time'),
    		         ('var_dims',('time',)),
    		         ('standard_name','time'),
    		         ('long_name','time'),
    		         ('units','days since 1973-1-1 00:00:00'),
    		         ('axis','T'),
    		         ('calendar','gregorian'),
    		         ('start_year',int(styear)),
    		         ('end_year',int(edyear)),
    		         ('start_month',1),
    		         ('end_month',12),
    		         ('bounds','bounds_time')]),
    	           dict([('var_type','i4'),
    		         ('var_name','bounds_time'),
    		         ('var_dims',('time','bound_pairs',)), 
    		         ('standard_name','time'),
    		         ('long_name','time period boundaries')]),
    	           dict([('var_type','S1'),
    		         ('var_name','month'),
    		         ('var_dims',('month','characters',)), 
    		         ('long_name','month of year')])]

        # Attribute list for variables
        AttrList = [dict([('var_type','f4'),
	                  ('var_name',var+'_anoms'),
		          ('var_dims',('time',)), 
	                  ('long_name',ParamDict[var][5]+' anomaly'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_abs'),
		          ('var_dims',('time',)), 
	                  ('long_name',ParamDict[var][5]),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_stds'),
		          ('var_dims',('time',)), 
	                  ('long_name',ParamDict[var][5]+' standard deviations'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_clims'),
		          ('var_dims',('month',)), 
	                  ('long_name',ParamDict[var][5]+' climatology '+str(MYclst)+'-'+str(MYcled)),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_clim_stds'),
		          ('var_dims',('month',)), 
	                  ('long_name',ParamDict[var][5]+' climatological standard deviation '+str(MYclst)+'-'+str(MYcled)),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_adjustments'),
		          ('var_dims',('time',)), 
	                  ('long_name',ParamDict[var][5]+' homogenisation adjustments from NCEIs PHA algorithm'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_adjerr'),
		          ('var_dims',('time',)), 
	                  ('long_name',ParamDict[var][5]+' adjustment uncertainty estimate including missed adjustment (2 sigma)'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_climerr'),
		          ('var_dims',('time',)), 
	                  ('long_name',ParamDict[var][5]+' climatology uncertainty estimate (2 sigma)'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_obserr'),
		          ('var_dims',('time',)), 
	                  ('long_name',ParamDict[var][5]+' measurement uncertainty estimate (2 sigma)'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_uncertainty'),
		          ('var_dims',('time',)), 
	                  ('long_name',ParamDict[var][5]+' combined station uncertainty estimate (2 sigma)'),
	                  ('units',ParamDict[var][1])])]  

        GlobAttrObjectList = dict([['File_created',datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')], # Is there a call for time stamping?
			          ['Description','HadISDH monthly mean land surface homogenised data'],
			          ['Title','HadISDH monthly mean land surface climate monitoring product'], 
			          ['Institution', AttribDict['Institution']],
			          ['History', AttribDict['History']], 
			          ['Licence', AttribDict['NCLicence']],
			          ['Project', AttribDict['Project']],
			          ['Processing_level', AttribDict['Processing_level']],
			          ['Acknowledgement', AttribDict['Acknowledgement']],
			          ['Source', 'HadISD '+hadisdversiondots+' '+AttribDict['Source']],
			          ['Comment',''],
			          ['References', AttribDict['References']],
			          ['Creator_name', AttribDict['Creator_name']],
			          ['Creator_email', AttribDict['Creator_email']],
			          ['Version', versiondots],
			          ['doi',''], # This needs to be filled in
			          ['Conventions', AttribDict['Conventions']],
			          ['netCDF_type', AttribDict['netCDF_type']]]) 

        # Write out monthly data to netCDH
        WriteNetCDF(OutDat+StationListID[st]+DatSuffix,styear,edyear,[MYclst,MYcled],DataList,DimList,AttrList,GlobAttrObjectList,MDI)

#**********************************************************************************
# Plot homogenisation plots
#**********************************************************************************
# Plot the time series of the anomalies, adjustments and individual and combined uncertainty components
#**********************************************************************************
        
	# Set up lists for looping through plot panels
        PlotTitles = [StationListID[st]+' Anomalies (Homogenised)', 
	              'PHA Adjustments', 
		      'Adjustment Uncertainty (2sigma)', 
		      'Measurement Uncertainty (2sigma)', 
		      'Climatology Uncertainty (2sigma)', 
		      'Total Station Uncertainty (2sigma)']
		      
        PlotVars = [stat_anoms, stat_adjs, stat_adjs_err, stat_obs_err, stat_clims_err, station_err]
	
        NPlots = len(PlotVars)
	
	# letters for plotting
        Letteree = LetterRange(0,NPlots)
	
	# Positioning
        xpos = []
        ypos = []
        xfat = []
        ytall = []
        totalyspace = 0.90	# start 0.08 end 0.98
        totalxspace = 0.85	# start 0.12 end 0.98
     
        for n in range(NPlots):
            xpos.append(0.12)
            ypos.append(0.98-((n+1)*(totalyspace/NPlots)))
            xfat.append(totalxspace)
            ytall.append(totalyspace/NPlots)
			      
        # Xarray of months
        DateArr = np.array(list(np.array([[datetime(j,i,1,0,0,0) for i in np.arange(1,13)] for j in np.arange(int(styear),int(edyear)+1)]).flat))
        xtitlee = 'Years'
            
	# Make the plot        
        plt.clf()
        f,axarr = plt.subplots(NPlots, figsize=(7,10), sharex=False)	#6,18
    
        for pp in range(NPlots):
        
            axarr[pp].set_position([xpos[pp],ypos[pp],xfat[pp],ytall[pp]])
            axarr[pp].set_xlim([DateArr[0],DateArr[-1]])
        
            # If its not the last plot then suppress year tick labels on x axis
            if pp < NPlots-1:
                
                axarr[pp].set_xticklabels([])    
		
            # If its not the first or second plot then ensure y axis goes down to zero.		
            if (pp > 1):
	    
                if (np.max(PlotVars[pp]) > 0.):

                    axarr[pp].set_ylim(0.,np.max(PlotVars[pp])*1.05)	    		

                else:
		 
                    axarr[pp].set_ylim(0.,1.)		 
     
            #pdb.set_trace()
#            axarr[pp].plot(DateArr[PlotVars[pp] > MDI],PlotVars[pp][PlotVars[pp] > MDI],c='black',linewidth=0.5)
            axarr[pp].plot(DateArr,PlotVars[pp],c='black',linewidth=0.5)
	
            axarr[pp].annotate(Letteree[pp]+') '+PlotTitles[pp],xy=(0.03,0.03), xycoords='axes fraction',size=12)

            axarr[pp].set_ylabel(ParamDict[var][1],fontsize=12)
            #axarr[pp].hlines(0,DataArr[0],DataArr[-1],color='black',linewidth=0.5)
	
        
        axarr[NPlots-1].set_xlabel(xtitlee,fontsize=12)
         
        #plt.show()
        plt.savefig(OutPlots+StationListID[st]+'_anoms'+CLMlab+'_stationstats'+'.eps')
        plt.savefig(OutPlots+StationListID[st]+'_anoms'+CLMlab+'_stationstats'+'.png')
        plt.close()

#***************************************************************************************
# If this is the last station in the list then output counts to OUTPUTLOGFILE - shouldn't matter if we've had a restart as long as we haven't double written to the list files???
#**************************************************************************************

    # Write out number of good, bad and (if they exist) supersat and subzero stations
    filee = open(OUTPUTLOG,'a+')
    moo = check_output(['wc','-l',OutList])
    filee.write('%s%s%i\n' % (var, '_GOOD_STATIONS_AFTER_HOMOG_CONVERSION=', int(moo.decode('utf-8').split()[0])))
    moo = check_output(['wc','-l',OutBads])
    filee.write('%s%s%i\n' % (var, '_BAD_STATIONS_AFTER_HOMOG_CONVERSION=', int(moo.decode('utf-8').split()[0])))
    if (len(glob.glob(OutFunniesT)) > 0):

        moo = check_output(['wc','-l',OutFunniesT])
        filee.write('%s%s%i\n' % (var, '_SUPERSAT_STATIONS_AFTER_HOMOG_CONVERSION=',int(moo.decode('utf-8').split()[0])))

    if (len(glob.glob(OutFunniesZ)) > 0):

        moo = check_output(['wc','-l',OutFunniesZ])
        filee.write('%s%s%i\n' % (var, '_SUBZERO_STATIONS_AFTER_HOMOG_CONVERSION=',int(moo.decode('utf-8').split()[0])))

    filee.close()
    
    print('And we are done!')
    
if __name__ == '__main__':
    
    main(sys.argv[1:])

#************************************************************************
    
