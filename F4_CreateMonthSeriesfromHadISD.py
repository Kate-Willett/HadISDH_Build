#!/usr/local/sci/bin/python
# PYTHON3
# 
# Author: Kate Willett
# Created: 24 January 2018 (based on IDL create_monthseriesJAN2015.pro 1 Feb 2013)
# Last update: 4 September 2020
# Location: home/h04/hadkw/HadISDH_Code/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# Reads in hourly HadISD data, converts to humidity variables, caluclates monthly means and monthly mean anomalies, saves to ascii and netCDF.
# Outputs station files to: 
#	PHA folder: /scratch/hadkw/pha52jgo/data/hadisdh/
# Depending on PHA switch it will output anomalies or absolurtes to PHA 
# Still need to test PHA with anomalies which would allow me to produce absolutes from anomaly + climatology which is better
# 	/scratch/hadkwUPDATE<YYYY>/MONTHLIES/NETCDF/
# 	/scratch/hadkw/UPDATE<YYYY>/MONTHLIES/ASCII/
#
# Outputs list files to:
# 	/scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/
#
# this program reads in every QC'd HadISD netcdf file and outputs a monthly mean anomaly, abs, clim and sd version
# this uses T, Tdew and SLP from the netCDF but also needs to know elevation in order to calculate SLP if necessary.
# this outputs T, Tdew, DPD, Twetbulb, vapour pressure, specific humidity and relative humidity using calc_evap.pro
# Also outputs SLP and windspeed
# May add heat indices in the future
#
# This previously also read in source data and output a station history file
# /data/local/hadkw/HADCRUH2/UPDATE2017/MONTHLIES/HISTORY/ of the format:
# /data/local/hadkw/HADCRUH2/PROGS/USHCN_v52d/src_codes/documentation/SHF_tob_inst.txt
# some amendments:
# SOURCE CODE 3=history created from raw data using: 
#	- change in station source (composited stations) - uses IDs listed for each time point within netCDF file
# 	- change in ISD within file lat/lon (2012 onwards)
#	- change in observing frequency 
#	- change in observing times
#	- change in recording resolution (2012 onwards?)
# REMEMBER to convert lat/lon to degrees, minutes and seconds and elevation to feet (?)
# This functionality hasn't been brought through from IDL to python yet.
#
# Initial kick ouf if fewer than 1344 obs for a calendar month over the 1981-2010 climatology period - 80% of days in month with at least 4 obs and 15 years (15*4*(28*0.8))
# Initial kick out if fewer than 24000 total obs - 20 years with 4 obs on at least 300 days

# First, month hour averages are taken for each hour of the day 
# - there must be at least 15 days present for each hour within the month
# Then the month average is made from the month hour averages
# - there must be at least 4 month hour averages with at least 1 in each tercile 00 to 07, 08 to 15, 16 to 23
# There must also be at least one year in each decade of climatology 81-90, 91-00, 01-10 
# There must be at least (>=) 15 years of T and Td (tests RH) within the 1981-2010 climatology period 
# for each month present for the station to be kept

#1) Makes hr means for each month where >=15 obs for each hour over the month
#2) ABS and St Devs: Makes month means from month hr means where >= 4 hrs within month and 1 in each tercile 0-7, 8-15, 16-23
#3) Makes month hr clims where >= 15 years of data for each month hr and one in each decade
#4) CLIMS and CLIM ST DEVS: Makes month CLIMS and Clim Std Devs if >= 4 clim hr means and one in each tercile
#5) Makes month hr mean anomalies if >= 15 hr anomalies (hr - month hr climatology)
#6) ANOMS: Make month mean anomalies if >= 4 month hr mean anomalies in each month and one in each hr tercile
#7) Add a final check that if the station is still good (has all 12 months of climatology) 

#
# <references to related published material, e.g. that describes data set>
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# inbuilt:
# import datetime as dt
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.dates import date2num,num2date
# import sys, os
# from scipy.optimize import curve_fit,fsolve,leastsq
# from scipy import pi,sqrt,exp
# from scipy.special import erf
# import scipy.stats
# from math import sqrt,pi
# import struct
# import pdb
# import netCDF4 as nc4
# from subprocess import check_output
#
# Kates:
# import CalcHums - written by kate Willett to calculate humidity variables
# import ReadNetCDF
# from GetNiceTimes import MakeDaysSince 
# 
# -----------------------
# DATA
# -----------------------
# reads in netCDF hourly station data from HadISD 
# - /scratch/hadkw/UPDATE<YYYY>/HADISDTMP/
# New list of potential HadISD stations to include
# inlists='/scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/HadISD.<Version>_candidate_stations_details.txt'
# inCIDs='/scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/isd-history_downloaded18JAN2018_1230.txt'
# 20CR SLP data for making climatological SLP for humidity calculation
# inSLP='/scratch/hadkw/UPDATE<YYYY>/OTHERDATA/'	#20CR*7605MSLP_yycompos.151.170.240.10.37.8.8.59.nc
#
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# First make sure the HadISD and 20CR source data are in the right place.
# Make sure this year's directories are set up: makeHadISDHdirectories.sh
# Make sure this year's PHA directories are set up: makePHAdirectories.sh
# Go through everything in the 'Start' section to make sure dates, versions and filepaths are up to date
# This can take an hour or so to run through ~3800 stations so consider using screen, screen -d, screen -r
# python3 CreateMonthSeriesfromHadISD.py
#
# Run from desktop:
# module load scitools/default-current # to load python 3
# python CreateMonthSeriesfromHadISD.py 
#
# Run from spice:
# ./F4_submit_spice.bash
#
# -----------------------
# OUTPUT
# -----------------------
# ASCII monthly means and anomalies
# outdirASC='/scratch/hadkw/UPDATE<YYYY>/MONTHLIES/ASCII/'
# GHCNM style ASCII monthly means for PHA
# outdirRAW<var>='/scratch/hadkw/UPDATE<YYYY>/pha52jgo/data/hadisdh/<var>/monthly/raw/'
# outdirHIST='scratch/hadkw/UPDATE<YYYY>/MONTHLIES/HISTORY/'
# outdirNCF='scratch/hadkw/UPDATE<YYYY>/MONTHLIES/NETCDF/'
# A list of stations that are not carried forward because they do not contain enough months of data
# ditchfile='scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/tooshortforHadISDH.'+version+'.txt'
# A list of stations that have enough months to be carried forward
# keepfile='scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/goodforHadISDH.'+version+'.txt'
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
#
# Version 6 (22 October 2020)
# ---------
#  
# Enhancements
# Updated headers and processes to work in a fully automated manner from /scratch/hadkw/
# Can now output anomalies or absolutes to the PHA file structure
# Now outputs the number of 'good' and 'bad' stations to an output file.
#  
# Changes
#  
# Bug fixes
#
#
# Version 5 (3 February 2020)
# ---------
#  
# Enhancements
# Now python 3
#  
# Changes
# Now month climatology catch kicks out if there are fewer than 1344 obs - 80% of days with at least 4 obs per day and 15 years of climatology (Feb has 28 days so ((28*4)*0.8) * 15
# Its also kicked out if there are fewer than 20 years of data with 4 obs on at least 300 days (24000) - these would have been caught anyway but this is more efficient to catch here early
# Climatology can be calculated where there are >= 15 years of data rather than > 15 years
#  
# Bug fixes
# 1) reshaping of 20CR SLP arrays has been corrected - this created very small errors within the monthly values
# 2) RH was being calculated with respect to water in all cases rather than with respect to ice when Tw <= 0
# 3) Climatology maker checked that there was at least 1 year of data in each decade but this wasn't working properly so more stations passed than should have
#
#
#Version 4 (24 January 2018)
# ---------
#  
# Enhancements
# Now python
#  
# Changes
# Can work with any climatology period BUT check that 20CR data is there for that clim period.
# Changed 20CRMMM7605 filenames to match the 19812010 formats
#  
# Bug fixes
#
# IDL VERSIONS PREVIOUSLY
# Version 3 (18 January 2017)
# ---------
#  
# Enhancements
# Updated to deal with HadISD.2.0.1 - now 8000 stations plus, data from 1900 onwards and new station list
# Sticking with 1976-2005 clim for now so that I don't have to redo 20CR stuff yet - next year I should do this
#  
# Changes
# Now requires an ish-history...txt file to find the CID (2 digit country code ID) to match up to the station WMO-WBAN numbers
# These are saved and then put in the output station list file at the end for continuity with previous versions and the hope
# that one day this CID will be corrected and usable - we know of many errors in it e.g., CI meaning China or Chile in some cases.
#  
# Bug fixes

#
# Version 2 (22 January 2016)
# ---------
#  
# Enhancements
# Updated to deal with 2016
# Added more detail to the header for code legacy
#  
# Changes
#  
# Bug fixes

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
# COULD CHANGE TO RUN EACH STATION INDEPENDENTLY SO IT CAN BE SPAT OUT TO SPICE AND RUN VERY VERY QUICKLY
# WOULD REQUIRE A SORT ON THE STATION OUTPUT LISTS AT THE END THOUGH TO CHECK THEY ARE IN ORDER

# AS of 7th Feb 2020 this runs and appears to output sensible values
# HOWEVER - these values to not match the IDL values either for anomalies or absolutes.
# They are close but not the same, sometimes even a few numbers out (whole numbers not just decimal precision)
# Could this be the humidity calculation?
# Could this be the month means - have I changed anything that might have altered the climatologies
# If it also affects T and Td then its not just the humidity calculations - IT DOES NOT - SO IT IS SOMETHING TO DO WITH CALCHUMS....precision? Method? Ice bulb method?
# I have cross-checked IDL calc_evap.pro and python 3 CalcHums.py and they produce identical values to at least 4 decimal places.
# Maybe its the pressure read in? - 20CR values for 010010-99999 are very slightly different
# HOwever, I've just tested tolerance and its very small, even for very low temperatures.
# Now check both codes at variable conversion and then again at monthly means
# SOOO - there were twobugs in IDL
# - the pull out and reformat of 20CR slp data was wrong because the shift() term did not have a 0 for the second axis.
#   all data were rolling through as a vector rather than an array
#   This is an error but would not have lead to very different values because sensitivity to pressure is small
# - the calculation of RH was done only with respect to water even when tw <= 0.
#   this only affected RH values but the difference could be large
#
# On complete run through Python kicks out 18 more stations than IDL
# Some stations kicked out by IDL are retained by python and vice versa and stations have slightly different numbers of months in some cases.
# I think this comes down to the make_months_oddtimes or MakeMonths functions
#
# In Python we calculate clims where there are >= 15 years over clim period but IDL is just > 15 so Python keeps more stations for this
# Still trying to find out why python kicks out others that make it in IDL
# Found ANOTHER bug in the IDL code in make_months_oddtimesJAN2015.pro
# - to create a climatology there must be at least 15 years of data AND at least 1 year in each decade
# - in IDL the decade counter was wrong  - rather than the decade goin 0-9 and 10-19 and 20-29 of the climatology it
# started at the start year 1973 so any year within the first 17 was counted even though a subarray of only the climatology years had been created
#
# SOOOO - my python code that kicks out more stations but keeps some that were kicked out in IDL is CORRECT!!!
#
#-------------------------------------------------------------------------
# JAN 2015
# updated to read in 2014
# now includes windpeed and sea level pressure
# moved 'BAD MONTHS' kick out to just below RH make_months and moved RH to be done first
# no point carrying on if there isn't enough humidity data - do not base on SLP which has lots of
# missing

# JAN 2014
# updated to read in 2013
# now creates hourly DPD and then monthly DPD AND monthly derived DPD (compare later)
# added a loop in make_months_oddtimesJAN2014.pro to remove all stations that have fewer 
# than 15 months for any one month within climatology period. This can occur in some cases 
# when the odd hour makes an hour_month clim possible but not a monthly..

# DEC 2013
# Adding dewpoint depression ready for 2013 update
# Need to check that T-DPD = Td as it may not.
# Not entirely sure whether its best to calculate monthly T and Td and then create DPD
# Or whether its best to calculate monthly DPD directly from the hourly data
# For playing (to see whether there is more S-N ratio in DPD compared to Td) just use monthly conversions

# FEB 2013
# CHANGED station P calculation
# i) use actual station T to convert to monthly - test
# ii) make climatological monthly mean T values and use those to calc station P
# iii) read in CR20 monthly MSLP climatologies 1976-2005 and use these instead of 1013.25 - use climatological monthly mean T

#"Support for the Twentieth Century Reanalysis Project dataset is provided by the U.S. Department of Energy, 
# Office of Science Innovative and Novel Computational Impact on Theory and Experiment (DOE INCITE) program, 
# and Office of Biological and Environmental Research (BER), and by the National Oceanic and Atmospheric 
# Administration Climate Program Office."
#"20th Century Reanalysis V2 data provided by the NOAA/OAR/ESRL PSD, Boulder, Colorado, USA, from their Web site at 
# http://www.esrl.noaa.gov/psd/"
# We would also appreciate receiving a copy of the relevant publications. 

# both use Eq. from Smithsonian Tables p268

#************************************************************************
#                                 START
#************************************************************************
# USE python3
# module load scitools/default-current
# python F4_CreateMonthSeriesfromHadISD.py
#
# For debugging
# ipython
# %pdb
# %run F4_CreateMonthSeriesfromHadISD.py
#
# REQUIRES
# CalcHums.py
# MakeMonths.py
# ReadNetCDF.py
#
#************************************************************************
# Set up python imports
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num,num2date
import sys, os
from scipy.optimize import curve_fit,fsolve,leastsq
from scipy import pi,sqrt,exp
from scipy.special import erf
import scipy.stats
from math import sqrt,pi
import struct
import pdb
import netCDF4 as nc4
from subprocess import check_output, call
import glob

import CalcHums 
import ReadNetCDF
from GetNiceTimes import MakeDaysSince

# RESTART VALUE
RestartValue = '-----------' #'-----------'				#'------'		#'681040'

# Anomalies or absolutes to PHA?
PHAActuals = True # True for outputting actuals to PHA, False to output Anomalies to PHA

# Start and end years if HardWire = 1
isdstyear = 1931 # start year of HadISD dataset
styear = 1973
edyear = 2019

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
        styear = int(ConfigDict['StartYear'])
        edyear = int(ConfigDict['EndYear'])
    
# Climatology start and end years
clims = [1981,2010]

# Set up directories locations
updateyy  = str(edyear)[2:4]
updateyyyy  = str(edyear)
workingdir  = '/scratch/hadkw/UPDATE'+updateyyyy

# Hope this stays teh same. May need to change this when we go to monthly updating
# Could use glob.glob with wildcard for the date bit...
#INDIR       = workingdir+'/HADISDTMP/hadisd.'+hadisdversiondots+'_19310101-'+str(edyear+1)+'0101_'
INDIR       = workingdir+'/HADISDTMP/hadisd.'+hadisdversiondots+'_19310101-'+str(edyear+1)+'0201_'

OUTASC      = workingdir+'/MONTHLIES/ASCII/'
OUTRAWq     = workingdir+'/pha52jgo/data/hadisdh/q/'
OUTRAWe     = workingdir+'/pha52jgo/data/hadisdh/e/'
OUTRAWt     = workingdir+'/pha52jgo/data/hadisdh/t/'
OUTRAWdpd   = workingdir+'/pha52jgo/data/hadisdh/dpd/'
OUTRAWtd    = workingdir+'/pha52jgo/data/hadisdh/td/'
OUTRAWtw    = workingdir+'/pha52jgo/data/hadisdh/tw/'
OUTRAWrh    = workingdir+'/pha52jgo/data/hadisdh/rh/'
OUTRAWws    = workingdir+'/pha52jgo/data/hadisdh/ws/'
OUTRAWslp   = workingdir+'/pha52jgo/data/hadisdh/slp/'
OUTHIST     = workingdir+'/MONTHLIES/HISTORY/'
OUTNCF      = workingdir+'/MONTHLIES/NETCDF/'

# Set up filenames
RAWSUFFIX   = '.raw.tavg'
HISSUFFIX   = '.his'
ANOMSUFFIX  = 'monthQCanoms.raw'
ABSSUFFIX   = 'monthQCabs.raw'
NCSUFFIX    = '_hummonthQC.nc' 

INSTATLIST  = workingdir+'/LISTS_DOCS/HadISD.'+hadisdversiondots+'_candidate_stations_details.txt'
INCIDs      = workingdir+'/LISTS_DOCS/isd-history-*.txt' # does wildcard work here?
INSLP       = workingdir+'/OTHERDATA/'	#20CRJan7605MSLP_yycompos.151.170.240.10.37.8.8.59.nc or 20CRv2cJan19812010_SLP_Jan2018.nc

OUTDITCH    = workingdir+'/LISTS_DOCS/tooshortforHadISDH.'+versiondots+'.txt'
OUTKEEP     = workingdir+'/LISTS_DOCS/goodforHadISDH.'+versiondots+'.txt'
OUTPUTLOG   = workingdir+'/LISTS_DOCS/OutputLogFile'+versiondots+'.txt'

# Set up variables
MDI = -1e+30
#*** at some point add all the header info from the new HadISD files***

# date and time stuff
MonArr   = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
stday    = 1
stmon    = 1
stjul    = dt.date(styear,stmon,stday).toordinal() # 00:00 hrs not set for hours just integer days + 1721424.5   #JULDAY(stmon,stday,styear,0)
edday    = 31
edmon    = 12
#edjul    = dt.date(edyear+1,edmon,edday).toordinal()  # 00:00 hrs not sure why this is year + 1 but still with Dec 31st
edjul    = dt.date(edyear+1,1,1).toordinal()  # 00:00 hrs not sure why this is year + 1 but still with Dec 31st
# Should it not be dt.date(edyear+1,1,1)
edactjul = dt.date(edyear,edmon,edday).toordinal() # should be 11pm 23:00
# Will have to *24 to get bours 

# Using JULIAN DAYS to get at number of hours - doesn't need to be Julian days!
ntims = (edjul - stjul) * 24 # time points in hours
nmons = ((edyear + 1) - styear) * 12 # time points in months
nyrs = (edyear + 1) - styear # time points in years
actyears = np.arange(styear, (edyear + 1)) # array of integer years
ndays = (edjul - stjul)
# ISD times are HOURS since 1931-01-01 00:00 rather than DAYS since 1973-01-01 00:00 so we need to extract
# this is a little complicated as they are provided as integers rather than decimals of a whole day (1./24.)
# set up an array of time pointers from 1973 onwards in HadISD time language (hours since 1931-01-01 00:00)
# 753887 hours since 1931 comes out as Dec 31st 2016 at 23:00 - which is correct!!!
# 24 * (JULDAY(12,31,2016,23) - JULDAY(1,1,1931,0) = 753887
# 24 * (JULDAY(1,1,1973,0) - JULDAY(1,1,1931,0) = 368184
isdstjul = dt.date(isdstyear,stmon,stday).toordinal()  # JULDAY(stmon,stday,isdstyear,0) ; this gives a number in days 2426342.5
hrssince1931 = (stjul - isdstjul) * 24 # hours since Jan 1st 1931 for Jan 1st 1973 00:00
isd_full_times = np.arange(ntims) + hrssince1931 # array for each hour from Jan 1st 1973 00:00 starting count at hours since jan 1st 1931 00:00
full_times = np.arange(0, ntims) # array for each hour from Jan 1st 1973 00:00 starting at 0

# create array of half year counts taking into account leap years
# These are for analysing the station data for shifts in resolution or frequency
# i.e., 1973 June 30th = 181st day Dec 31st = 365th day (184)
# i.e., 1974 June 30th = 181st day Dec 31st = 365th day (184)
# i.e., 1975 June 30th = 181st day Dec 31st = 365th day (184)
# i.e., 1976 June 30th = 182nt day Dec 31st = 366th day (184)
# leaps are 1976,1980,1984,1988,1992,1996,2000,2004,2008,2012,2016
# leap if divisible by four by not 100, unless also divisible by 400 i.e. 1600, 2000

# IDentify the leap years
founds = np.where( ((actyears/4.) - np.floor(actyears/4.) == 0.0) & ( ((actyears/100.) - np.floor(actyears/100.) != 0.0) | ((actyears/400.) - np.floor(actyears/400.) == 0.0)))
leapsids = np.repeat(0,nyrs)
leapsids[founds] = 1  #1s identify leap years

HrDict = {'JanHrs':np.arange(744),
          'FebHrs':np.arange(696)+744, # THIS INCLUDES 29th FEB!!!
	  'MarHrs':np.arange(744)+1440,
          'AprHrs':np.arange(720)+2184,
          'MayHrs':np.arange(744)+2904,
          'JunHrs':np.arange(720)+3648,
          'JulHrs':np.arange(744)+4368,
          'AugHrs':np.arange(744)+5112,
          'SepHrs':np.arange(720)+5856,
          'OctHrs':np.arange(744)+6576,
          'NovHrs':np.arange(720)+7320,
          'DecHrs':np.arange(744)+8040}

dates = [stjul,edactjul] # this is Jan 1st 1973 to end-year, Dec 31st so the day counts will need +1 to be correct
stclim = clims[0] - styear
edclim = clims[1] - styear
climsum = (edclim + 1) - stclim
CLIMstjul = dt.date(clims[0],stmon,stday).toordinal()      #JULDAY(stmon,stday,clims(0),0)
# Can't understand why I did clims(1)+1, edmon,edday
CLIMedjul = dt.date(clims[1]+1,stmon,stday).toordinal()    #JULDAY(edmon,edday,clims(1)+1, 0)
CLIMtims = (CLIMedjul - CLIMstjul) * 24.
CLIMstpoint = (CLIMstjul - stjul) * 24.
clpointies = (np.arange(CLIMtims) + CLIMstpoint).astype(int)    
#print('check these clims')
#pdb.set_trace()

#************************************************************************
# Subroutines
#************************************************************************
# READDATA
def ReadData(FileName,typee,delimee):
    ''' Use numpy genfromtxt reading to read in all rows from a complex array '''
    ''' Need to specify format as it is complex '''
    ''' outputs an array of tuples that in turn need to be subscripted by their names defaults f0...f8 '''

    return np.genfromtxt(FileName, dtype=typee,delimiter=delimee,encoding='latin-1') # ReadData 

#************************************************************************
#ReadSLPdata
def ReadSLPdata(TheMDI):
    ''' REad in 1981-2010 climatological SLP from 20CRv2 data '''
    ''' REform lats and lons accordingly '''
    ''' Compile 12 month clim to one array '''
    ''' Data are 2 x 2 degrees '''
    
    TheData = np.empty((12,91,180))
    TheData.fill(TheMDI)
    
    LatInfo = ['lat']
    LonInfo = ['lon']
    ReadInfo = ['VAR']
    
    # Loop through each month to read in and append data into array
    MonArr = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    for mm,mon in enumerate(MonArr):
    
        TmpData,TmpLats,TmpLons = ReadNetCDF.GetGrid(INSLP+'20CRv2c'+mon+'19812010_SLP_Jan2018.nc',ReadInfo,LatInfo,LonInfo)
        # A time, lat, lon data numpy array
    
        # If this is January then sort out lats and lons
        if (mm == 0):
    
            # Make lats the northern-most boundary and reverse to go 91 to - 89
            TheLats = np.flip(np.copy(TmpLats))
            TheLats = TheLats + 1
        
	    # Make the lons the western-most boundary from -179 to 179 
            TheLons = np.roll(np.copy(TmpLons) - 1,89)
            TheLons[np.where(TheLons >= 180)] = -(360 - TheLons[np.where(TheLons >= 180)])
    
        TheData[mm,:,:] = np.flipud(np.roll(np.copy(TmpData),89,axis=1)) # lons were 0 to 358 and are now  to -179 to 179 (gridbox centres)
    
    #print('Check this reformatting')
    #pdb.set_trace()

    return TheData,TheLats,TheLons

#************************************************************************
# GetHadISD
def GetHadISD(TheFilee,TheHTimes,TheMDI):
    ''' THis reads in the data from netCDF and pulls out the correct time period '''
    
    # Build correct time arrays
    TheTempArr = np.repeat(TheMDI, len(TheHTimes)) 
    TheDewpArr = np.repeat(TheMDI, len(TheHTimes)) 
    TheWSArr = np.repeat(TheMDI, len(TheHTimes)) 
    TheSLPArr = np.repeat(TheMDI, len(TheHTimes)) 
    TheObsSource = np.empty((len(TheHTimes),12),dtype='|S1') 
    
    # Read the time, t, td, slp and ws (and obs source) data from the netcdf file
    ncf = nc4.Dataset(TheFilee,'r')
    tims = np.copy(ncf.variables['time'][:]).astype(int) # hours wince 1931, 1, 1, 00:00 - these are doubles so convert to integer
    # Now find the period we're interested and only copy that data
    # Note that we may be reading HadISD that has data after our period of interest (monthly updates) so need to be specific
    #StartPoint = np.where(tims >= TheHTimes[0])[0]
    StartPoint = np.where((tims >= TheHTimes[0]) & (tims <= TheHTimes[-1]) )[0]
#    pdb.set_trace()

    # Catch station if there is no data in desired period and return with empty arrays
    if (len(StartPoint) == 0):
    
        return TheTempArr,TheDewpArr,TheWSArr,TheSLPArr,tims,TheObsSource
	
    #StartPoint = np.where(tims >= TheHTimes[0])[0][0]
    tims = tims[StartPoint[0]:]
    
    temps = np.copy(ncf.variables['temperatures'][StartPoint[0]:])
    dewps = np.copy(ncf.variables['dewpoints'][StartPoint[0]:])
    slp = np.copy(ncf.variables['slp'][StartPoint[0]:])
    ws = np.copy(ncf.variables['windspeeds'][StartPoint[0]:])
    #tims = tims.astype(int)
    sourceids = np.copy(ncf.variables['input_station_id'][StartPoint[0]:,:]) # time,long_character_length (12) - comes out is byte array b'0' etc
    # needs to be converted to string and then concatenated
    #pdb.set_trace()
    # Trying to convert byte character array into a joined string array but FAR TOO SLOWWWW
    #sourceids = np.array([]) # a blank numpy array to append to
    #for row in range(len(tmp[:,0])):
    #    #print(row)
    #    #sourceids = np.append(sourceids,''.join([''.join(i) for i in tmp[row,:].astype('U')])) # TOOOOOOOO SLOW!!!!
    #    sourceids = np.append(sourceids,tmp[row,:].astype('U'))
    
    # pull out the HadISDH data period
    # Which points in the HadISD data match the desired times for HadISDH TheHTimes
    # np.isin gave IndexError when run from script but not from pdb - np.intersect1d seems more efficient anyway
    Mush,ISDMap,HISDMap = np.intersect1d(tims,TheHTimes,assume_unique=True,return_indices=True)
    TheTempArr[HISDMap] = np.copy(temps[ISDMap])
    TheDewpArr[HISDMap] = np.copy(dewps[ISDMap])
    TheWSArr[HISDMap] = np.copy(ws[ISDMap])
    TheSLPArr[HISDMap] = np.copy(slp[ISDMap])
    TheObsSource[HISDMap,:] = np.copy(sourceids[ISDMap,:])
    #print('Check mapping has worked: ISDcounts = ',len(ISDMap),' HISDCounts = ',len(HISDMap))
    #pdb.set_trace()
    
    # Convert all flagged -2e30 and missing -1e30 valuess to missing
    TheTempArr[np.where(TheTempArr <= TheMDI)] = TheMDI
    TheDewpArr[np.where(TheDewpArr <= TheMDI)] = TheMDI
    TheWSArr[np.where(TheWSArr <= TheMDI)] = TheMDI
    TheSLPArr[np.where(TheSLPArr <= TheMDI)] = TheMDI
    #print('check the mdi catching has worked') # may need [0] at end of np.where()
    #pdb.set_trace()

    return TheTempArr,TheDewpArr,TheWSArr,TheSLPArr,tims,TheObsSource

#**************************************************************************
# MakeMonths
def MakeMonths(TheDataArr,TheDates,TheMDI):
    ''' Code converted from IDL make_months_oddtimesJAN2015.pro '''
    ''' COMPLEX method makes month hour means, substracts month hour climatology, makes month hour anomaly'''
    ''' Importantly this removes the diurnal cycle before averaging so reduces biasing from uneven temporal sampling '''
    ''' 1) Makes hr means for each month where >=15 obs for each hour over the month
        2) ABS and St Devs: Makes month means from month hr means where >= 4 hrs within month and 1 in each tercile 0-7, 8-15, 16-23
	3) Makes month hr clims where >= 15 years of data for each month hr and one in each decade
	4) CLIMS and CLIM ST DEVS: Makes month CLIMS and Clim Std Devs if >= 4 clim hr means and one in each tercile
	5) Makes month hr mean anomalies if >= 15 hr anomalies (hr - month hr climatology)
	6) ANOMS: Make month mean anomalies if >= 4 month hr mean anomalies in each month and one in each hr tercile
	7) Add a final check that if the station is still good (has all 12 months of climatology) !!!'''

    # Set up the times
    nhhrs = len(TheDataArr) # number of hours in record - complete years of data including leap years
    nddys = (dates[1] - dates[0]) + 1 # number of days in the record - should be nhhrs / 24 so this is a check
    #print('Number of days/hours check: ',nhhrs/24, nddys)
    #pdb.set_trace()
    
    TheStYr = dt.date.fromordinal(dates[0]).year
    TheEdYr = dt.date.fromordinal(dates[1]).year
    nyyrs = (TheEdYr - TheStYr) + 1 # number of years of record
    nmms = nyyrs * 12 # number of months of record
    
    clim_points = [clims[0]-TheStYr,clims[1]-TheStYr] # remember in python that if we're getting a range the last value needs to be +1
    climlength = (clims[1] - clims[0]) + 1 # should be 30
    #print('Number of years in clim (30?) check: ',climlength)
    #pdb.set_trace()
    
    # Set up leap year stuff
    # This is already in the code above so may just be referencable but by putting it here this could be a stand alone function
    ActYears = np.arange(TheStYr, (TheEdYr + 1)) # array of integer years
    LeapIDs = np.repeat(0,nyyrs)
    LeapIDs[np.where( ((ActYears/4.) - np.floor(ActYears/4.) == 0.0) & ( ((ActYears/100.) - np.floor(ActYears/100.) != 0.0) | ((ActYears/400.) - np.floor(ActYears/400.) == 0.0)))] = 1  #1s identify leap years
    #print('Check the LeapIDs are correct')
    #pdb.set_trace()

    # SEt up the final arrays
    TheAnoms = np.repeat(MDI,nmms)
    TheAbs = np.repeat(MDI,nmms)
    TheSDs = np.repeat(MDI,nmms)
    TheClims = np.repeat(MDI,12)    
    TheClimSDs = np.repeat(MDI,12)    
    
    # Set up the working arrays
    mm_hr_abs   = np.empty((nmms,24)) # month mean for each hour
    mm_hr_abs.fill(MDI)
    mm_hr_anoms = np.empty((nmms,24)) # month mean anomaly for each hour
    mm_hr_anoms.fill(MDI)
    mm_hr_clims = np.empty((12,24))   # month climatological mean for each hour
    mm_hr_clims.fill(MDI)
    
    # 1) MAKE MONTH HOUR MEANS FOR ALL YEARS - OK WITH LEAP YEARS
    # chunk by years then work through each month - allows us to easily ID leap years
    MCount = 0 # counter for months
    stpoint = 0
    edpoint = 0
    for yy,year in enumerate(ActYears): # loops through with 0,1973 1,1974 etc
    
        if (LeapIDs[yy] == 0): # not a leap year
        
            MonDays = [31,28,31,30,31,30,31,31,30,31,30,31]

        else:
	    
            MonDays = [31,29,31,30,31,30,31,31,30,31,30,31]
	    
        #print('Check leap year ID')
        #pdb.set_trace()    
	
	# Now loop through each month    
        for mm in range(12):    
	
	    # Extract month of data and reform to hrs,days array
            edpoint = stpoint + (MonDays[mm]*24)
            HrDayArr = np.reshape(TheDataArr[stpoint:edpoint],(MonDays[mm],24)) # each row is a day, each column is an hour
	
            #print('Check stpoint and edpoint and extraction')
            #pdb.set_trace()
	        
	    # Loop through the hours in the day
            for hh in range(24):

                # *** Get month hour means where there are AT LEAST 15 days present within the month
                # THIS COULD HAVE BEEN 20 BUT THEN STATIONS WITH CHANGES TO GMT REPORTING WITHIN A MONTH i.e. Australia MAY 
                # HAVE EVERY e.g. MARCH and SEPTEMBER REMOVED.
                if (len(np.where(HrDayArr[:,hh] > TheMDI)[0]) >= 15):

                    mm_hr_abs[MCount,hh] = np.mean(HrDayArr[np.where(HrDayArr[:,hh] > TheMDI)[0],hh])
	
  	    # 2) Make Month Means from actuals
	    # *** If there are at least 4 hrs means within the day and one in each tercile [0-7,8-15,16-23] then Fill TheAbs and TheSDs[MCount]
            if ((len(np.where(mm_hr_abs[MCount,:] > TheMDI)[0]) >= 4) & 
                (len(np.where(mm_hr_abs[MCount,0:8] > TheMDI)[0]) > 0) & 
                (len(np.where(mm_hr_abs[MCount,8:16] > TheMDI)[0]) > 0) & 
                (len(np.where(mm_hr_abs[MCount,16:24] > TheMDI)[0]) > 0)):
	    
                TheSDs[MCount] = np.std(HrDayArr[np.where(HrDayArr > TheMDI)])
                TheAbs[MCount] = np.mean(mm_hr_abs[MCount,np.where(mm_hr_abs[MCount,:] > TheMDI)[0]])
		# potentially we could have a value for TheAbs but not TheAnoms so need to make sure the 15 days minimum is also applied there
		# Later, if one month fails for climatology the whole station is dumped
	    
            stpoint = edpoint
            MCount = MCount + 1
            
            #print('Check hour sampling and means')
            #pdb.set_trace()
	    	    
    # 3) MAKE MONTH HOUR CLIMS where >= 15 years of month hr data adn one in each decade
    # Firstextract clim years and reshape the mm_hr_abs from nmms,24 to climlength,12,24
    mm_hr_abs_clim = np.reshape(mm_hr_abs[(clim_points[0]*12):((clim_points[1]+1)*12),:],(climlength,12,24))
    #print('Check extraction of climatological months - 360')
    #pdb.set_trace()

    for mm in range(12):
    
        for hh in range(24):
	
            # *** There should be at least 15 years (50% of climlength) and one year in each decade
	    # NOTE THAT IN IDL THIS WAS JUST GT 15 NOT GE 15!!! SO WE KEEP MORE STATIONS HERE AT LEAST
            if ((len(mm_hr_abs_clim[np.where(mm_hr_abs_clim[:,mm,hh] > TheMDI)[0],mm,hh]) >= climlength*0.5) & 
                (len(mm_hr_abs_clim[np.where(mm_hr_abs_clim[0:10,mm,hh] > TheMDI)[0],mm,hh]) > 0) & 
                (len(mm_hr_abs_clim[np.where(mm_hr_abs_clim[10:20,mm,hh] > TheMDI)[0],mm,hh]) > 0) & 
                (len(mm_hr_abs_clim[np.where(mm_hr_abs_clim[20:30,mm,hh] > TheMDI)[0],mm,hh]) > 0)):
	    
                mm_hr_clims[mm,hh] = np.mean(mm_hr_abs_clim[np.where(mm_hr_abs_clim[:,mm,hh] > TheMDI)[0],mm,hh])	
                #print('Check the month hr clim')
                #pdb.set_trace()		    

        # 4) THEN MONTH CLIMS if >= 4 clim hr means and one in each tercile
	# NOTE FAIL IF: one month fails then this station will be ditched
	# *** If there are at least 4 hrs means within the day and one in each tercile [0-7,8-15,16-23] then Fill TheClims and TheClimSDs[MCount]
        if ((len(np.where(mm_hr_clims[mm,:] > TheMDI)[0]) >= 4) & 
	    (len(np.where(mm_hr_clims[mm,0:8] > TheMDI)[0]) > 0) & 
	    (len(np.where(mm_hr_clims[mm,8:16] > TheMDI)[0]) > 0) & 
	    (len(np.where(mm_hr_clims[mm,16:24] > TheMDI)[0]) > 0)):
 
            TheClims[mm] = np.mean(mm_hr_clims[mm,np.where(mm_hr_clims[mm,:] > TheMDI)])	
            monthstash = mm_hr_abs_clim[:,mm,:]    
            TheClimSDs[mm] = np.std(monthstash[np.where(monthstash > TheMDI)])	    

            #print('Check the month clim and sd')
            #pdb.set_trace()		    
     
        # This month does not have enough data so we need to ditch the station
        else:
	
            #print('Failed to produce climatology')
            #pdb.set_trace()
            return TheAnoms, TheAbs, TheSDs, TheClims, TheClimSDs # exit with empty / incomplete return arrays

    # 5) Make month hr mean anomalies if >= 15 hr anomalies (hr - month hr climatology)
    # NOW BUILD THE month hr anoms and TheAnoms
    # chunk by years then work through each month - allows us to easily ID leap years
    MCount = 0 # counter for months
    stpoint = 0
    edpoint = 0
    for yy,year in enumerate(ActYears): # loops through with 0,1973 1,1974 etc
    
        if (LeapIDs[yy] == 0): # not a leap year
        
            MonDays = [31,28,31,30,31,30,31,31,30,31,30,31]

        else:
	    
            MonDays = [31,29,31,30,31,30,31,31,30,31,30,31]
	    
	# Now loop through each month    
        for mm in range(12):    
	
	    # Extract month of data and reform to hrs,days array
            edpoint = stpoint + (MonDays[mm]*24)
            HrDayArr = np.reshape(TheDataArr[stpoint:edpoint],(MonDays[mm],24)) # each row is a day, each column is an hour
	
	    # Loop through the hours in the day
            for hh in range(24):

                # *** Get month hour mean anoms where there are AT LEAST 15 days present within the month
                # THIS COULD HAVE BEEN 20 BUT THEN STATIONS WITH CHANGES TO GMT REPORTING WITHIN A MONTH i.e. Australia MAY 
                # HAVE EVERY e.g. MARCH and SEPTEMBER REMOVED.
                if ((len(np.where(HrDayArr[:,hh] > TheMDI)[0]) >= 15) & (mm_hr_clims[mm,hh] > TheMDI)):

                    mm_hr_anoms[MCount,hh] = np.mean((HrDayArr[np.where(HrDayArr[:,hh] > TheMDI)[0],hh] - mm_hr_clims[mm,hh]))
	
	    # 6) Make month mean anomalies if >= 4 month hr mean anomalies in each month and one in each hr tercile
	    # *** If there are at least 4 hrs means within the day and one in each tercile [0-7,8-15,16-23] then Fill TheAnoms
            if ((len(np.where(mm_hr_anoms[MCount,:] > TheMDI)[0]) >= 4) & 
                (len(np.where(mm_hr_anoms[MCount,0:8] > TheMDI)[0]) > 0) & 
                (len(np.where(mm_hr_anoms[MCount,8:16] > TheMDI)[0]) > 0) & 
                (len(np.where(mm_hr_anoms[MCount,16:24] > TheMDI)[0]) > 0)):
	    
                TheAnoms[MCount] = np.mean(mm_hr_anoms[MCount,np.where(mm_hr_anoms[MCount,:] > TheMDI)[0]])
	    
            stpoint = edpoint
            MCount = MCount + 1

    # 7) Add a final check that if the station is still good (has all 12 months of climatology) 
    # there are sufficient numbers of absolute values to calculate a climatology
    TheAbsClims = np.reshape(TheAbs,(len(ActYears),12))[clim_points[0]:clim_points[1]+1,:]
    for mm in range(12):
    
        if (len(TheAbsClims[np.where(TheAbsClims[:,mm] > TheMDI)[0],mm]) < 15):
	
	# this is bad so fail everything
            TheClims[:] = TheMDI
            #print('Failed to produce enough absolute values')
            #pdb.set_trace()
            return TheAnoms, TheAbs, TheSDs, TheClims, TheClimSDs
            
    return TheAnoms, TheAbs, TheSDs, TheClims, TheClimSDs
    
#************************************************************************
# WriteNetCDF
def WriteNetCDF(FileName,TheStYr,TheEdYr,TheClims,TheDataList,DimObject,AttrObject,GlobAttrObject,OLDMDI):
    ''' WRites NetCDF4 '''
    ''' Sort out the date/times to write out and time bounds '''
    ''' Convert variables using the obtained scale_factor and add_offset: stored_var=int((var-offset)/scale) '''
    ''' Write to file, set up given dimensions, looping through all potential variables and their attributes, and then the provided dictionary of global attributes '''

#    # Attributes and things common to all vars
#    add_offset = -100.0 # storedval=int((var-offset)/scale)
#    scale_factor = 0.01
    
    # Sort out date/times to write out
    TimPoints,TimBounds = MakeDaysSince(TheStYr,1,TheEdYr,12,'month',Return_Boundaries = True)
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
	
    # No need to convert float data using given scale_factor and add_offset to integers - done within writing program (packV = (V-offset)/scale
    # Not sure what this does to float precision though...
#    # Change mdi into an integer -999 because these are stored as integers
#    # NOTE THAT THIS CHANGES THE ACTUAL DATA ARRAYS IN THE LIST BECAUSE THE LIST IS JUST A POINTER!!!
#    NEWMDI = -999
#    for vv in range(len(TheDataList)):
#        TheDataList[vv][np.where(TheDataList[vv] == OLDMDI)] = NEWMDI

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
        print(DimObject[vv+2]['var_name'])
	
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

            for mm in range(12):
                MyVar[mm,:] = nc4.stringtochar(np.array(MonthName[mm],dtype='S10'))

    # Go through each variable and set up the variable attributes
    for vv in range(len(AttrObject)): # ignore first two elements of the list but count all other dictionaries

        print(AttrObject[vv]['var_name'])

        # NOt 100% sure this works in a loop with overwriting
	# initiate variable with name, type and dimensions
#        MyVar = ncfw.createVariable(AttrObject[vv]['var_name'],AttrObject[vv]['var_type'],AttrObject[vv]['var_dims'],fill_value = NEWMDI)
        MyVar = ncfw.createVariable(AttrObject[vv]['var_name'],AttrObject[vv]['var_type'],AttrObject[vv]['var_dims'],fill_value = OLDMDI)
        
	# Apply any other attributes
        if ('long_name' in AttrObject[vv]):
            MyVar.long_name = AttrObject[vv]['long_name']
	    
        if ('units' in AttrObject[vv]):
            MyVar.units = AttrObject[vv]['units']

#        MyVar.add_offset = add_offset
#        MyVar.scale_factor = scale_factor

        if ('valid_min' in AttrObject[vv]):
            MyVar.valid_min = AttrObject[vv]['valid_min']

        if ('valid_max' in AttrObject[vv]):
            MyVar.valid_max = AttrObject[vv]['valid_max']

        MyVar.reference_period = str(TheClims[0])+', '+str(TheClims[1])

	# Provide the data to the variable - depending on howmany dimensions there are
        MyVar[:] = TheDataList[vv]
	    
    ncfw.close()
   
    return # WriteNCCF

#************************************************************************
# WriteASCII
def WriteAscii(TheFilee,TheData,TheID,TheStYr,TheEdYr):
    ''' Write out to text file '''
    
    nyrs = (TheEdYr - TheStYr) + 1
    
    filee = open(TheFilee,'a+')
    
    for y,yy in enumerate(np.arange(TheStYr,TheEdYr+1)):

        #DataString = '   '.join(['%6i' % (i) for i in TheData[y,:]])
        #pdb.set_trace()
        filee.write('%11s %4s%105s\n' % (TheID,str(yy),'   '.join(['%6i' % (i) for i in TheData[y,:]]))) # 105 is 12 * 6 + 11 * 3

    filee.close()

    return

#************************************************************************
# FailureMode
def FailureMode(FailType,Message,Counter,StationID):
    '''This function prints out the failure mode, stationID and Counter to 
       screen and to relevant file then returns '''
    '''TheMessage should be a string of maximum 30 characters '''
    '''Counter should be max of 999999 '''

    if (FailType == 'TooFewHours'):
        print('Too few hours in month climatology')
    
        filee = open(OUTDITCH,'a+')
        filee.write('%12s %32s %6i \n' % (StationID,Message+': ',Counter))
        filee.close()

    elif (FailType == 'SubzeroDPD'):
        print('Subzero values in DPD data')
    
        filee = open(OUTDITCH,'a+')
        filee.write('%12s %32s %6i \n' % (StationID,Message+': ',Counter))
        filee.close()

    elif (FailType == 'EarlyRecord'):
        print('No data in desired time period')
    
        filee = open(OUTDITCH,'a+')
        filee.write('%12s %32s %6i \n' % (StationID,Message+': ',Counter))
        filee.close()

    elif (FailType == 'TooFewMonths'):
        print('Too few months with enough data for climatology')
    
        filee = open(OUTDITCH,'a+')
        filee.write('%12s %32s %6i \n' % (StationID,Message+': ',Counter))
        filee.close()

    elif (FailType == 'TooFewClims'):
        print('Too few climatological months')
    
        filee = open(OUTDITCH,'a+')
        filee.write('%12s %32s %6i \n' % (StationID,Message+': ',Counter))
        filee.close()

    elif (FailType == 'ShortStation'):
        print('Too few months in record')
    
        filee = open(OUTDITCH,'a+')
        filee.write('%12s %32s %6i \n' % (StationID,Message+': ',Counter))
        filee.close()

    return

#************************************************************************
# MAIN
#************************************************************************
# Read in the SLP data from netCDF
CR20arr,CR20lats,CR20lons = ReadSLPdata(MDI)

# Open and read in station list 
#MyTypes = str
MyTypes         = ("|U6","|U1","|U5","|U1","|U30","|U1","float","|U1","float","|U1","float","|U1","|U21")
#MyTypes         = ("|S6","|S1","|S5","|S1","|S30","|S1","float","|S1","float","|S1","float","|S1","|S21")
#MyTypes         = ("str","str","str","str","str","str","float","str","float","str","float","str","str")
#MyTypes         = (str,str,str,str,str,str,float,str,float,str,float,str,str)
#MyTypes         = "|U5"
# Could try:
#MyTypes         = ("|S6","x","|S5","x","|S30","x","float","x","float","x","float","x","|S21")
MyDelimiters    = [6,1,5,1,30,1,7,1,8,1,7,1,21]
RawData         = ReadData(INSTATLIST,MyTypes,MyDelimiters)
StationListWMO  = np.array(RawData['f0'])
StationListWBAN = np.array(RawData['f2'])
StationListLat  = np.array(RawData['f6'])
StationListLon  = np.array(RawData['f8'])
StationListElev = np.array(RawData['f10'])
StationListCID  = np.repeat('XX',len(StationListWMO)) # added later
StationListName = np.array(RawData['f4'])
nstations       = len(StationListWMO)
#print('Test to see if station read in has worked correctly and whether there is a more efficient method')
#pdb.set_trace()

# loop through station by station
for st in range(nstations):

# check if restart necessary
    if RestartValue != '-----------' and RestartValue != StationListWMO[st]+StationListWBAN[st]:
        continue

    RestartValue     = '-----------'

    stationid = StationListWMO[st]+'-'+StationListWBAN[st]	# New ISD will have different filenames
    outstationid = StationListWMO[st]+StationListWBAN[st]	# New ISD will have different filenames

    print('Working on ',stationid)

# Find the CID from the ish-history file
# INCIDs is a wildcard file path as the date of download changes each time.
    GotCID = 0
    FilNameWild = glob.glob(INCIDs)
#    with open (FilNameWild[0], 'rt') as myfile:
    with open (FilNameWild[0], 'r', errors='ignore') as myfile: # ignore to cope with umlaut : found for 999999-27516 Jan 2021
        
        for line in myfile:
	
            if line.find(StationListWMO[st]+' '+StationListWBAN[st]) != -1: # if there is a match with the WMO ID?
    
                StationListCID[st] = str(line[43:45])
                GotCID = 1
                break
	    
    if (GotCID == 0):   # There should always be a CID!
	   
        StationListCID[st] = '**'
        print('No CID found!')
        pdb.set_trace()
	    
    #print('Check that the CID search is working')
    #pdb.set_trace()

# open the file, extract HadISDH time period data for times, t, td, slp and ws and station sources----------------------------------------------------------

    filee = INDIR+stationid+'.nc'
    # Need to gunzip then gzip
    call(['gunzip',filee+'.gz'])
    fulltemp_arr,fulldewp_arr,fullws_arr,fullslp_arr,tims,obssource = GetHadISD(filee,isd_full_times,MDI)
    call(['gzip',filee])
    
    # Catch failure from no data in desired time period
    if (len(fulltemp_arr[np.where(fulltemp_arr > MDI)[0]]) == 0):
    
        FailureMode('EarlyRecord','No data in period',0,stationid)
        continue

    #print('TOTAL TEMPS and DEWPS: ',len(np.where(fulltemp_arr > MDI)[0]),' ',len(np.where(fulldewp_arr > MDI)[0]))
    #pdb.set_trace()
# Convert to other variables        
    statP_arr = np.repeat(MDI, ntims)
    fullddep_arr = np.repeat(MDI, ntims) 
    fulltwet_arr = np.repeat(MDI, ntims) 
    fullevap_arr = np.repeat(MDI, ntims) 
    fullqhum_arr = np.repeat(MDI, ntims) 
    fullrhum_arr = np.repeat(MDI, ntims) 

# Double check there are vaguely enough data in the climatology period
    if (len(np.where((fulltemp_arr[clpointies] > MDI) & (fulldewp_arr[clpointies] > MDI))[0]) > 24000):	# 300 days for 20 years with 4 obs per day.

        #There are provisionally enough data - yippee!

# Get the climatological station P    
        #  FEB2013 use CR20 climatological MSLP and climatological temperature (from HadISD) to get a climatological station P for each time point (duplicated year to year for ease)
        # so we need all January hours over the climatology period etc.
        tempyearsarr = np.empty((8784,climsum))
        tempyearsarr.fill(MDI)                  # 30 year by all hours (including leaps) array - containing the years within the climatology period
        tempclimsarr = np.empty((8784,nyrs))
        tempclimsarr.fill(MDI)                  # all years by all hours (including leaps) array - to fill with climatological daily means 
        slpclimsarr = np.empty((8784,nyrs))
        slpclimsarr.fill(MDI)                   # array with all hours including leaps present for each year
        temppointer = 0
    
        # Pull out the climatological data
        for yrfill in range(nyrs):
        
            if ((yrfill >= stclim) & (yrfill <= edclim)):
                if (leapsids[yrfill] != 1):   # not a leap year so fill to Feb 28th and from Mar 1st
                    tempyearsarr[0:1416,yrfill-stclim] = fulltemp_arr[temppointer:temppointer+1416]
                    tempyearsarr[1440:8784,yrfill-stclim] = fulltemp_arr[temppointer+1416:temppointer+8760]
                    temppointer = temppointer+8760	

                else:
                    tempyearsarr[:,yrfill-stclim] = fulltemp_arr[temppointer:temppointer+8784]
                    temppointer = temppointer+8784	    

            else:
                if (leapsids[yrfill] != 1):   # not a leap year so fill to Feb 28th and from Mar 1st
                    temppointer = temppointer+8760	

                else:
                    temppointer = temppointer+8784	    
    
        # now subset to get clims for each month, fill tempclimsarr with those clims, slpclimsarr with CR20 MSLP for closestgridbox

        matchlats = np.where(CR20lats < StationListLat[st])
        thelat = matchlats[0][0] - 1 
 
        # Need a catch in case the longitude is < -179 or > 179
        if ((StationListLon[st] > 179.) | (StationListLon[st] < -179.)):
            
            thelon = 179	
	
        else:	
        
            matchlons = np.where(CR20lons > StationListLon[st])
            thelon = matchlons[0][0] - 1

        #print('Check the lat and lon matching bit')
        #pdb.set_trace()

        # Annoyingly we need a catch in here to check if any of the months do not have data over the climatology period just in case
        # THERE MUST BE AT LEAST 15 years of data over the climatology with 4 hours a day and 80% of days
        # For February that's ((28*4)*0.8)*15 = 1344 observations THIS IS DIFFERENT TO EARLIER CODE (Feb 2020) SO MAY KICK OUT MORE STATIONS
        BadMonth = 0 # Counter for months with too few data for climatology to catch failure
        for mm,Mon in enumerate(MonArr):

            lotsofhours = tempyearsarr[HrDict[Mon+'Hrs'],:]   # calculate T clims over clim period 1981-2010
            if (len(lotsofhours[np.where(lotsofhours > MDI)]) >= 1344):  
            
                tempclimsarr[HrDict[Mon+'Hrs'],:] = np.median(lotsofhours[np.where(lotsofhours > MDI)])
                slpclimsarr[HrDict[Mon+'Hrs'],:] = CR20arr[mm,thelat,thelon]
	
	    # if there isn't enough data then fail
            else:
        
                BadMonth = BadMonth + 1		
  	    
        if (BadMonth > 0):
    
            FailureMode('TooFewMonths','Months with no climatology',BadMonth,stationid)
            continue

        #print('Are you happy with how the climatology is being done?')
        #pdb.set_trace()
    
        # now convert back to fulltemp_arr space without fake leap years - converting standard P too
        temppointer = 0
        for yrfill in range(nyrs):
            
            if (leapsids[yrfill] != 1):    # not a leap year so fill to Feb 28th and from Mar 1st
                #pdb.set_trace()
	    # AS WE'RE USING STATION T NOT SEA LEVEL T, TO GET RATIO OF SEA LEVEL T TO STATION T NEEDS A REARRANGMENT OF THE (slT-HeightConv)/slT to stT/(stT+HeighConv)
                statP_arr[temppointer:temppointer+1416] = slpclimsarr[0:1416,yrfill] * (( (273.15 + tempclimsarr[0:1416,yrfill]) / 
		                                                                          ((273.15 + tempclimsarr[0:1416,yrfill]) + (0.0065 * StationListElev[st])) ) **5.256)   
                statP_arr[temppointer+1416:temppointer+8760] = slpclimsarr[1440:8784,yrfill] * (( (273.15 + tempclimsarr[1440:8784,yrfill]) / 
		                                                                                 ((273.15 + tempclimsarr[1440:8784,yrfill]) + (0.0065*StationListElev[st])) )**5.256)   
                temppointer = temppointer + 8760	
            else:

                statP_arr[temppointer:temppointer+8784] = slpclimsarr[:,yrfill] * (( (273.15 + tempclimsarr[:,yrfill]) / 
		                                                                    ((273.15 + tempclimsarr[:,yrfill]) + (0.0065 * StationListElev[st])) )**5.256)	
                temppointer = temppointer + 8784	    

        #print('Check the station pressures')
        #pdb.set_trace()

# Calculate Dew point depression
        gots = np.where((fulltemp_arr > MDI) & (fulldewp_arr > MDI)) 
        fullddep_arr[gots[0]] = fulltemp_arr[gots[0]] - fulldewp_arr[gots[0]]
        
	# Check DPD for subzeros - there really shouldn't be any as QC should have picked this up
        if (len(np.where(fullddep_arr[gots[0]] < 0.)[0]) > 0):
    
            FailureMode('SubzeroDPD','No. of subzero DPDs',len(np.where(fullddep_arr[gots[0]] < 0.)[0]),stationid)
            continue
	
# Calculate vapour pressure - over ice if twet <= 0.0        
        fullevap_arr[gots[0]] = CalcHums.vap(fulldewp_arr[gots[0]],fulltemp_arr[gots[0]],statP_arr[gots[0]],roundit=False) #station_P

# Calculate relative humidity - over ice if twet <= 0.0        
        fullrhum_arr[gots[0]] = CalcHums.rh(fulldewp_arr[gots[0]],fulltemp_arr[gots[0]],statP_arr[gots[0]],roundit=False) #station_P

# Calculate specific humidity - over ice if twet <= 0.0        
        fullqhum_arr[gots[0]] = CalcHums.sh(fulldewp_arr[gots[0]],fulltemp_arr[gots[0]],statP_arr[gots[0]],roundit=False) #station_P

# Calculate wetbulb temperature - over ice if twet <= 0.0        
        fulltwet_arr[gots[0]] = CalcHums.wb(fulldewp_arr[gots[0]],fulltemp_arr[gots[0]],statP_arr[gots[0]],roundit=False) #station_P

    else: # too few hours for climatology
    
        FailureMode('TooFewHours','Hours of good data',len(np.where((fulltemp_arr[clpointies] > MDI) & (fulldewp_arr[clpointies] > MDI))[0]),stationid)
        continue

#create monthly means/anoms/clims/sds------------------------------------

    RHanoms_mm, RHabs_mm, RHsd_mm, RHclims_mm,RHclimSD_mm = MakeMonths(fullrhum_arr,dates,MDI) # will return MDI for RHclims_mm if a month fails a climatology count

    #print('Check the monthly means - are the anoms and abs present identically?')
    #pdb.set_trace()
    
    # Test RH clims to see if they have been calculated because RH requires both T and Td to be present
    if (len(np.where(RHclims_mm > MDI)[0]) < 12):
    
        FailureMode('TooFewClims','No of Months Clim',len(np.where(RHclims_mm > MDI)[0]),stationid)
        continue

    # Check number of months in station and if < 200 then ditch
    if (len(np.where(RHanoms_mm > MDI)[0]) < 200):
    
        FailureMode('ShortStation','Months present',len(np.where(RHanoms_mm > MDI)[0]),stationid)
        continue   

    Panoms_mm, Pabs_mm, Psd_mm, Pclims_mm, PclimSD_mm = MakeMonths(statP_arr,dates,MDI)
    Tanoms_mm, Tabs_mm, Tsd_mm, Tclims_mm, TclimSD_mm = MakeMonths(fulltemp_arr,dates,MDI)
    Tdanoms_mm, Tdabs_mm, Tdsd_mm, Tdclims_mm, TdclimSD_mm = MakeMonths(fulldewp_arr,dates,MDI)
    DPDanoms_mm, DPDabs_mm, DPDsd_mm, DPDclims_mm, DPDclimSD_mm = MakeMonths(fullddep_arr,dates,MDI)

    # Derive Td and DPD at the monthly resolution for comparison
    derivedDPDabs_mm = np.repeat(MDI,nmons)
    derivedTdabs_mm = np.repeat(MDI,nmons)
    gots = np.where(DPDabs_mm > MDI)
    if (len(gots[0]) > 0):
        derivedDPDabs_mm[gots[0]] = Tabs_mm[gots[0]] - Tdabs_mm[gots[0]]
        derivedTdabs_mm[gots[0]] = Tabs_mm[gots[0]] - DPDabs_mm[gots[0]]

    Twanoms_mm, Twabs_mm, Twsd_mm, Twclims_mm, TwclimSD_mm = MakeMonths(fulltwet_arr,dates,MDI)
    eanoms_mm, eabs_mm, esd_mm, eclims_mm, eclimSD_mm = MakeMonths(fullevap_arr,dates,MDI)
    qanoms_mm, qabs_mm, qsd_mm, qclims_mm, qclimSD_mm = MakeMonths(fullqhum_arr,dates,MDI)
    WSanoms_mm, WSabs_mm, WSsd_mm, WSclims_mm, WSclimSD_mm = MakeMonths(fullws_arr,dates,MDI)
    SLPanoms_mm, SLPabs_mm, SLPsd_mm, SLPclims_mm, SLPclimSD_mm = MakeMonths(fullslp_arr,dates,MDI)

    #print('Check the monthly means')
    #pdb.set_trace()
 
    # List data together to pass to NetCDF writer
    DataList = [RHanoms_mm, RHabs_mm, RHsd_mm, RHclims_mm, RHclimSD_mm, Tanoms_mm, Tabs_mm, Tsd_mm, Tclims_mm, TclimSD_mm,
                Tdanoms_mm, Tdabs_mm, Tdsd_mm, Tdclims_mm, TdclimSD_mm, DPDanoms_mm, DPDabs_mm, DPDsd_mm, DPDclims_mm, DPDclimSD_mm,
                Twanoms_mm, Twabs_mm, Twsd_mm, Twclims_mm, TwclimSD_mm, eanoms_mm, eabs_mm, esd_mm, eclims_mm, eclimSD_mm,
                qanoms_mm, qabs_mm, qsd_mm, qclims_mm, qclimSD_mm, WSanoms_mm, WSabs_mm, WSsd_mm, WSclims_mm, WSclimSD_mm,
                SLPanoms_mm, SLPabs_mm, SLPsd_mm, SLPclims_mm, SLPclimSD_mm, Pabs_mm,derivedDPDabs_mm,derivedTdabs_mm]

    DimList=[['time','month','characters','bound_pairs'],
	       [nmons,12,10,2],
    	       dict([('var_type','f4'),
    		     ('var_name','time'),
    		     ('var_dims',('time',)),
    		     ('standard_name','time'),
    		     ('long_name','time'),
    		     ('units','days since 1973-1-1 00:00:00'),
    		     ('axis','T'),
    		     ('calendar','gregorian'),
    		     ('start_year',styear),
    		     ('end_year',edyear),
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
    AttrList=[dict([('var_type','f4'),
	            ('var_name','rh_anoms'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) relative humidity monthly mean anomaly'),
	            ('units','%rh')]),
              dict([('var_type','f4'),
	            ('var_name','rh_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) relative humidity monthly mean'),
	            ('units','%rh')]),
              dict([('var_type','f4'),
	            ('var_name','rh_std'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) relative humidity monthly standard deviations'),
	            ('units','%rh')]),
              dict([('var_type','f4'),
	            ('var_name','rh_clims'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) relative humidity monthly climatology '+str(clims[0])+'-'+str(clims[1])),
	            ('units','%rh')]),
              dict([('var_type','f4'),
	            ('var_name','rh_climSDs'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) relative humidity monthly climatological standard deviation '+str(clims[0])+'-'+str(clims[1])),
	            ('units','%rh')]),
              dict([('var_type','f4'),
	            ('var_name','t_anoms'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) air temperature monthly mean anomaly'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','t_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) air temperature monthly mean'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','t_std'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) air temperature monthly standard deviations'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','t_clims'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) air temperature monthly climatology '+str(clims[0])+'-'+str(clims[1])),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','t_climSDs'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) air temperature monthly climatological standard deviation '+str(clims[0])+'-'+str(clims[1])),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','td_anoms'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) dewpoint temperature monthly mean anomaly'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','td_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) dewpoint temperature monthly mean'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','td_std'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) dewpoint temperature monthly standard deviations'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','td_clims'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) dewpoint temperature monthly climatology '+str(clims[0])+'-'+str(clims[1])),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','td_climSDs'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) dewpoint temperature monthly climatological standard deviation '+str(clims[0])+'-'+str(clims[1])),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','dpd_anoms'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) dewpoint depression monthly mean anomaly'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','dpd_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) dewpoint depression monthly mean'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','dpd_std'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) dewpoint depression monthly standard deviations'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','dpd_clims'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) dewpoint depression monthly climatology '+str(clims[0])+'-'+str(clims[1])),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','dpd_climSDs'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) dewpoint depression monthly climatological standard deviation '+str(clims[0])+'-'+str(clims[1])),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','tw_anoms'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) wetbulb temperature monthly mean anomaly'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','tw_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) wetbulb temperature monthly mean'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','tw_std'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) wetbulb temperature monthly standard deviations'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','tw_clims'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) wetbulb temperature monthly climatology '+str(clims[0])+'-'+str(clims[1])),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','tw_climSDs'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) wetbulb temperature monthly climatological standard deviation '+str(clims[0])+'-'+str(clims[1])),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','e_anoms'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) vapour pressure monthly mean anomaly'),
	            ('units','hPa')]),
              dict([('var_type','f4'),
	            ('var_name','e_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) vapour pressure monthly mean'),
	            ('units','hPa')]),
              dict([('var_type','f4'),
	            ('var_name','e_std'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) vapour pressure monthly standard deviations'),
	            ('units','hPa')]),
              dict([('var_type','f4'),
	            ('var_name','e_clims'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) vapour pressure monthly climatology '+str(clims[0])+'-'+str(clims[1])),
	            ('units','hPa')]),
              dict([('var_type','f4'),
	            ('var_name','e_climSDs'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) vapour pressure monthly climatological standard deviation '+str(clims[0])+'-'+str(clims[1])),
	            ('units','hPa')]),
              dict([('var_type','f4'),
	            ('var_name','q_anoms'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) specific humidity monthly mean anomaly'),
	            ('units','g/kg')]),
              dict([('var_type','f4'),
	            ('var_name','q_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) specific humidity monthly mean'),
	            ('units','g/kg')]),
              dict([('var_type','f4'),
	            ('var_name','q_std'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) specific humidity monthly standard deviations'),
	            ('units','g/kg')]),
              dict([('var_type','f4'),
	            ('var_name','q_clims'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) specific humidity monthly climatology '+str(clims[0])+'-'+str(clims[1])),
	            ('units','g/kg')]),
              dict([('var_type','f4'),
	            ('var_name','q_climSDs'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) specific humidity monthly climatological standard deviation '+str(clims[0])+'-'+str(clims[1])),
	            ('units','g/kg')]),
              dict([('var_type','f4'),
	            ('var_name','ws_anoms'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~10m) wind speed monthly mean anomaly'),
	            ('units','m/s')]),
              dict([('var_type','f4'),
	            ('var_name','ws_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~10m) wind speed monthly mean'),
	            ('units','m/s')]),
              dict([('var_type','f4'),
	            ('var_name','ws_std'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~10m) wind speed monthly standard deviations'),
	            ('units','m/s')]),
              dict([('var_type','f4'),
	            ('var_name','ws_clims'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~10m) wind speed monthly climatology '+str(clims[0])+'-'+str(clims[1])),
	            ('units','m/s')]),
              dict([('var_type','f4'),
	            ('var_name','ws_climSDs'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~10m) wind speed monthly climatological standard deviation '+str(clims[0])+'-'+str(clims[1])),
	            ('units','m/s')]),
              dict([('var_type','f4'),
	            ('var_name','slp_anoms'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) station level pressure monthly mean anomaly'),
	            ('units','hPa')]),
              dict([('var_type','f4'),
	            ('var_name','slp_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) station level pressure monthly mean'),
	            ('units','hPa')]),
              dict([('var_type','f4'),
	            ('var_name','slp_std'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) station level pressure monthly standard deviations'),
	            ('units','hPa')]),
              dict([('var_type','f4'),
	            ('var_name','slp_clims'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) station level pressure monthly climatology '+str(clims[0])+'-'+str(clims[1])),
	            ('units','hPa')]),
              dict([('var_type','f4'),
	            ('var_name','slp_climSDs'),
		    ('var_dims',('month',)), 
	            ('long_name','near surface (~2m) station level pressure monthly climatological standard deviation '+str(clims[0])+'-'+str(clims[1])),
	            ('units','hPa')]), 
              dict([('var_type','f4'),
	            ('var_name','20CRstation_Pclim'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) 20CRv2c station level pressure monthly climatological mean '+str(clims[0])+'-'+str(clims[1])),
	            ('units','hPa')]),
              dict([('var_type','f4'),
	            ('var_name','de_dpd_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) derived (T-Td) dewpoint depression monthly mean'),
	            ('units','deg C')]),
              dict([('var_type','f4'),
	            ('var_name','de_td_abs'),
		    ('var_dims',('time',)), 
	            ('long_name','near surface (~2m) derived dewpoint temperature (T-DPD) monthly mean'),
	            ('units','deg C')])]  

    GlobAttrObjectList = dict([['File_created',dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S')], # Is there a call for time stamping?
			          ['Description','HadISDH monthly mean land surface raw data'],
			          ['Title','HadISDH monthly mean land surface raw climate monitoring product'], 
			          ['Institution', ConfigDict['Institution']],
			          ['History', ConfigDict['History']], 
			          ['Licence', ConfigDict['NCLicence']],
			          ['Project', ConfigDict['Project']],
			          ['Processing_level', ConfigDict['Processing_level']],
			          ['Acknowledgement', ConfigDict['Acknowledgement']],
			          ['Source', 'HadISD '+hadisdversiondots+' '+ConfigDict['Source']],
			          ['Comment',''],
			          ['References', ConfigDict['References']],
			          ['Creator_name', ConfigDict['Creator_name']],
			          ['Creator_email', ConfigDict['Creator_email']],
			          ['Version', versiondots],
			          ['doi',''], # This needs to be filled in
			          ['Conventions', ConfigDict['Conventions']],
			          ['netCDF_type', ConfigDict['netCDF_type']]]) 


# Write out monthly data to netCDH
    WriteNetCDF(OUTNCF+stationid+NCSUFFIX,styear,edyear,clims,DataList,DimList,AttrList,GlobAttrObjectList,MDI)

# Write out anoms and abs for PHA and just for ascii versions
    # First reform the data arrays

    # Now convert missing to -9999 and cross-check abs and anoms (should match but maybe they don't)
    # Do this within list which should also change the master

    # ReList data together to pass to ASCII writer
    DataList = [RHanoms_mm, RHabs_mm, 
                Tanoms_mm, Tabs_mm, 
                Tdanoms_mm, Tdabs_mm, 
                DPDanoms_mm, DPDabs_mm,
                Twanoms_mm, Twabs_mm, 
                eanoms_mm, eabs_mm, 
                qanoms_mm, qabs_mm, 
                WSanoms_mm, WSabs_mm, 
                SLPanoms_mm, SLPabs_mm, 
		derivedDPDabs_mm,derivedTdabs_mm]

    # If PHAActuals = True then push actuals to PHA else push anomalies
    if (PHAActuals):
    
        OutListRAW = dict([('1', OUTRAWrh+'monthly/raw/'+outstationid+RAWSUFFIX),
                  ('3',OUTRAWt+'monthly/raw/'+outstationid+RAWSUFFIX),
                  ('5',OUTRAWtd+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('9',OUTRAWtw+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('11',OUTRAWe+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('13',OUTRAWq+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('15',OUTRAWws+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('17',OUTRAWslp+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('18',OUTRAWdpd+'monthly/raw/'+outstationid+RAWSUFFIX)])

    else:
    # If PHAActuals = False then push anomalies to PHA
        OutListRAW = dict([('0', OUTRAWrh+'monthly/raw/'+outstationid+RAWSUFFIX),
                  ('2',OUTRAWt+'monthly/raw/'+outstationid+RAWSUFFIX),
                  ('4',OUTRAWtd+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('8',OUTRAWtw+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('10',OUTRAWe+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('12',OUTRAWq+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('14',OUTRAWws+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('16',OUTRAWslp+'monthly/raw/'+outstationid+RAWSUFFIX),
		  ('6',OUTRAWdpd+'monthly/raw/'+outstationid+RAWSUFFIX)]) # NOTE WITH ANOMALIES WE@RE NOT USING DERIVED DPD (T - TD)!!!
    
    OutListAll = dict([('0',OUTASC+'RHANOMS/'+stationid+'_RH'+ANOMSUFFIX),
                       ('1',OUTASC+'RHABS/'+stationid+'_RH'+ABSSUFFIX),
		       ('2',OUTASC+'TANOMS/'+stationid+'_T'+ANOMSUFFIX),
		       ('3',OUTASC+'TABS/'+stationid+'_T'+ABSSUFFIX),
		       ('4',OUTASC+'TDANOMS/'+stationid+'_Td'+ANOMSUFFIX),
		       ('5',OUTASC+'TDABS/'+stationid+'_Td'+ABSSUFFIX),
		       ('6',OUTASC+'DPDANOMS/'+stationid+'_DPD'+ANOMSUFFIX),
		       ('7',OUTASC+'DPDABS/'+stationid+'_DPD'+ABSSUFFIX),
		       ('8',OUTASC+'TWANOMS/'+stationid+'_Tw'+ANOMSUFFIX),
		       ('9',OUTASC+'TWABS/'+stationid+'_Tw'+ABSSUFFIX),
		       ('10',OUTASC+'EANOMS/'+stationid+'_e'+ANOMSUFFIX),
		       ('11',OUTASC+'EABS/'+stationid+'_e'+ABSSUFFIX),
		       ('12',OUTASC+'QANOMS/'+stationid+'_q'+ANOMSUFFIX),
		       ('13',OUTASC+'QABS/'+stationid+'_q'+ABSSUFFIX),
		       ('14',OUTASC+'WSANOMS/'+stationid+'_WS'+ANOMSUFFIX),
		       ('15',OUTASC+'WSABS/'+stationid+'_WS'+ABSSUFFIX),
		       ('16',OUTASC+'SLPANOMS/'+stationid+'_SLP'+ANOMSUFFIX),
		       ('17',OUTASC+'SLPABS/'+stationid+'_SLP'+ABSSUFFIX),
		       ('18',OUTASC+'derivedDPDABS/'+stationid+'_deDPD'+ABSSUFFIX),
		       ('19',OUTASC+'derivedTDABS/'+stationid+'_deTd'+ABSSUFFIX)])

    # get mask of qanoms_mm to mask out other variables NOT 100% SURE WE NEED/WANT TO DO THIS
    # NOTE THAT NOW THE MDI IS -999 BECAUSE THIS WAS SET WITHIN WriteNetCDF FOR NetCDF output as integers	
#    NEWMDI = -999.
#    qmask = np.where(qanoms_mm == NEWMDI)
    qmask = np.where(qanoms_mm == MDI)
    for v,vv in enumerate(DataList):

	# mask to qanoma
        vv[qmask] = -99.99
  
        #pdb.set_trace()
        # change MDI to -9999 and multiply values by 10 - round whole number
#        vv[np.where(vv == NEWMDI)] = -99.99
        vv[np.where(vv == MDI)] = -99.99

        # reshape to print out a row of 12 months for each year
        vv = np.reshape(vv,(nyrs,12))
  
        vv = np.round(vv * 100).astype(int)

    # Write to ascii

        WriteAscii(OutListAll[str(v)],vv,outstationid,styear,edyear)
           
        if (str(v) in OutListRAW):
	    
            WriteAscii(OutListRAW[str(v)],vv,outstationid,styear,edyear)	      	    
        
    #print('Check writing to file has worked')
    #pdb.set_trace()

# Print out station listing in keep file    
    filee = open(OUTKEEP,'a+')
    filee.write('%11s%8.4f %9.4f %6.1f %2s %29s%8s%4i\n' % (outstationid,StationListLat[st],StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st],'MONTHS: ',len(np.where(qanoms_mm > -99.99)[0])))
# NOTE usihng -99.99 here. The above loop changes MDI to -99.99 within the DataList so qanoms_mm now has MDI=-99.99 but for some reason the reshape and *100 doesn't happen in place?
    filee.close()

# Out put stnlist to each PHA directory
    filee = open(OUTRAWq+'meta/q_stnlist.tavg','a+')
    filee.write('%11s%7.2f%10.2f        %5i %2s %29s\n' % (outstationid,StationListLat[st],StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st]))
    filee.close()

    filee = open(OUTRAWe+'meta/e_stnlist.tavg','a+')
    filee.write('%11s%7.2f%10.2f        %5i %2s %29s\n' % (outstationid,StationListLat[st],StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st]))
    filee.close()

    filee = open(OUTRAWt+'meta/t_stnlist.tavg','a+')
    filee.write('%11s%7.2f%10.2f        %5i %2s %29s\n' % (outstationid,StationListLat[st],StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st]))
    filee.close()

    filee = open(OUTRAWdpd+'meta/dpd_stnlist.tavg','a+')
    filee.write('%11s%7.2f%10.2f        %5i %2s %29s\n' % (outstationid,StationListLat[st],StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st]))
    filee.close()

    filee = open(OUTRAWtd+'meta/td_stnlist.tavg','a+')
    filee.write('%11s%7.2f%10.2f        %5i %2s %29s\n' % (outstationid,StationListLat[st],StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st]))
    filee.close()

    filee = open(OUTRAWtw+'meta/tw_stnlist.tavg','a+')
    filee.write('%11s%7.2f%10.2f        %5i %2s %29s\n' % (outstationid,StationListLat[st],StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st]))
    filee.close()

    filee = open(OUTRAWrh+'meta/rh_stnlist.tavg','a+')
    filee.write('%11s%7.2f%10.2f        %5i %2s %29s\n' % (outstationid,StationListLat[st],StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st]))
    filee.close()

    filee = open(OUTRAWws+'meta/ws_stnlist.tavg','a+')
    filee.write('%11s%7.2f%10.2f        %5i %2s %29s\n' % (outstationid,StationListLat[st],StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st]))
    filee.close()

    filee = open(OUTRAWslp+'meta/slp_stnlist.tavg','a+')
    filee.write('%11s%7.2f%10.2f        %5i %2s %29s\n' % (outstationid,StationListLat[st],StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st]))
    filee.close()


CountG = int(check_output(["wc","-l",OUTKEEP]).decode('utf-8').split()[0])
CountB = int(check_output(["wc","-l",OUTDITCH]).decode('utf-8').split()[0])
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('HadISDH_Enough_Months_Station_Count=',CountG))
filee.write('%s%i\n' % ('HadISDH_NotEnough_Months_Station_Count=',CountB))
filee.close()

print('And we are done!')
