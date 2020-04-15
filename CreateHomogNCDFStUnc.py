# PYTHON 3
# 
# Author: Kate Willett
# Created: 1 February 2013
# Last update: 18 February 2018
# Location: /data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# Read in list of stations passing through PHA/IDPHA
# MUST HAVE INPUT ADJUSTMENT UNCERTAINTY FOR EACH VARIABLE - find #***MISSEDADJUNC***
# Loop through each station
# read in homogenised station (ASCII VERSION OF ABS)
# Find cases of subzeros (RH, q and e) or supersaturation (RH, DPD, Td and Tw indirectly q, e) and output to list (continue to process)
# create station anomalies and climatologies using desired climatology period
# List stations with < 15 years present for each month of climatology as BADS - output to list and do not continue to process.
# Work out measurement uncertainty
# Work out adjustment uncertainties an dmissed adjustment uncertainty
# Output to netCDF (with 1 sigma uncertainties!!!)
# Make stationstats plot of all uncertainties

 
# <references to related published material, e.g. that describes data set>
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# .compile calc_evap.pro
# 
# -----------------------
# DATA
# -----------------------
#      inlist =	    dirlist+'goodforHadISDH.'+version+'_PHADPDtd_'+thenmon+thenyear+'.txt'
#      inlistS =	    dirlist+'PosthomogPHAdpd_anoms'+CLMlab+'_satsHadISDH.'+version+'_'+thenmon+thenyear+'.txt'	#need to use these to remove stations from 'goods' - and copy
#      inlistB =	    dirlist+'PosthomogPHAdpd_anoms'+CLMlab+'_badsHadISDH.'+version+'_'+thenmon+thenyear+'.txt'	#need to use these to remove stations from 'goods' - and copy
#      inhom =	    dirhomog+'IDPHAASCII/TDDIR/'	    #***
#      inlog =	    dirlist+'HadISDH.landTd.'+version+'_PHADPD_'+thenmon+thenyear+'.log'     #***
#      inmissadj =  dirlist+'Adjs_Stats.<version>_JAN<yyyy>.txt'
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# Ensure that you have updated the end year, version, clim period etc.
#
# The variables should be run in a specific order:
# T IDPHA first because homogenised t_abs is used to:
#  -> find supersats in Td and Tw
#  -> estimate uncertainties in RH, q, e, Td and dpd
# RH IDPHA second because homogenised rh_abs is used to:
#  -> find supersats in q, RH (obvs), e
#  -> find subzeros in RH (obvs)
#  -> estimate uncertainties in q, RH (obvs), e, Td, and DPD
# DPD PHA third because PosthomogPHAdpd_anoms7605_sats and bads are used for:
#  -> contributing to the sats and bads of Td
# NOTE: DPD requires Td for calculating uncertainty but can use homog T - homog DPD because
# homog Td is made up from homog T - homog DPD anyway
# q IDPHA fourth because all dependencies are now complete
# e IDPHA fifth because all dependencies are now complete
# td PHADPD sixth because all dependencies are now complete
# tw IDPHA zeventh because all dependencies are now complete
#
# > module load scitools/default-current
# > python CreateHomogNCDFStUnc --var <var> --typee <type>
#
## Which variable?
# var = 'dpd'	#'dpd','td','t','tw','e','q','rh'
#
## Which homog type?
# typee = 'PHA'	#'PHA' (for DPD only),'ID' (for t, e, q, rh and tw),'PHADPD' 
#
# See 'EDITABLES' for setting longer life things like version, dataset years etc.
#
#
#>tidl
#>.compile calc_evap
#>.compile create_homogNCDFall_stunc_JAN2015
#>create_homogNCDFall_stunc_JAN2015,'q','ID'
## Which variable? T first, RH, DPD, q, e, td, tw
#param =      'tw'
## Which homog type?
#homogtype =  'ID'		#'ID','DPD' for Td, 'PHA' - req for DPD or PHA versions of all variables
# 
# -----------------------
# OUTPUT
# -----------------------
# List of 'good' stations - outlist:
# /data/local/hadkw/HADCRUH2/UPDATE2016/LISTS_DOCS/PosthomogPHADPDtd_anoms'+CLMlab+'_goodsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
# List of supersaturated values (q, e, RH, Td, Tw, DPD) - outfunniesT: 
# /data/local/hadkw/HADCRUH2/UPDATE2016/LISTS_DOCS/PosthomogPHADPDtd_anoms'+CLMlab+'_satsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
# List of bad stations (not enough months after PHA) - outbads:
# /data/local/hadkw/HADCRUH2/UPDATE2016/LISTS_DOCS/PosthomogPHADPDtd_anoms'+CLMlab+'_badsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
# netCDF monthly station time series with uncertainty - outdat:
# /data/local/hadkw/HADCRUH2/UPDATE2016/MONTHLY/HOMOG/IDPHANETCDF/TDDIR/'
# uncertainty time series plots for each station - outplots:
# /data/local/hadkw/HADCRUH2/UPDATE2016/MONTHLY/HOMOG/STAT_PLOTS/UNCPLOTS/TDDIR/'
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
#
# Version 5 (17 February 2020)
# ---------
#  
# Enhancements
# Now only outputs stations that are 'good' or do not have subzeros or supersaturated values. These stations are
# listed in seperate files with all being in the 'BAD' station list then repeated in the SATS and SUBS files
# THis doesn't change the final grids but means that we no longer need to faff around pulling out the sats and subs stations
#  
# Changes
# This is now python 3 rather than IDL
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
import numpy as np
import matplotlib.pyplot as plt
import sys, os, getopt
import struct
import pdb
#import netCDF4 as nc4
from netCDF4 import Dataset
from subprocess import call
from subprocess import check_output

# Kate's Functions
from ReadNetCDF import GetGrid4

#******************************************************
# SUBROUTINES #
#******************************************************



#*******************************************************
# MAIN #
#*******************************************************
def main(argv):

    # INPUT PARAMETERS AS STRINGS!!!!
    var = 'q'	    # 'q','rh','e','td','tw','t','dpd'
    typee = 'IDPHA' # 'PHA','IDPHA','PHADPD'

    try:
        opts, args = getopt.getopt(argv, "hi:",
	                           ["var=","typee="])
    except getopt.GetoptError:
        print('Usage (as strings) MakeGridTrends.py --var <q> --typee <IDPHA>')
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
 
#    assert var != '' and typee != '', "Input values not specified."

    print(var,typee)
#    pdb.set_trace()

    #****************** LONGER LIFE EDITABLES****************
    # TWEAK ME!!!!

#*** UNCERTAINTY COMPONENT NEEDS SORTING FOR ALL ***

# program to read in homogenised data from PHA and raw, get adjustments and adjustment uncertainty
# calculate error in climatologies Eclims
# set up error in obs Eobs (this may be flat, or scale with temperature and over time)
# find adjustment uncertainty Eadj
# ignore computation errors at this stage Ecomp
# combine in quadrature - after Brohan et al. 2006
# output to NetCDF

    Restarter = '-----------' 	# set as a '0000009999' 11 digit station id to restart

    # Which year?
    MYstyr = 1973
    MYedyr = 2019

    # Which climatology?
    MYclst = 1981	# 1976, 1981
    MYcled = 2010	# 2005, 2010
    CLMlab = str(MYclst)[2:4]+str(MYcled)[2:4]

    # Which working file dates?
    nowmon =     'JAN'
    nowyear =    '2020'
    thenmon =    'JAN'
    thenyear =   '2020'

    # Which version?
    version =    '4.2.0.2019f'

    # files and directories
    updatedir =  'UPDATE20'+strmid(strcompress(MYedyr,/remove_all),2,2)
    workingdir = '/data/users/hadkw/WORKING_HADISDH/'+updatedir
    dirlist =    workingdir+'/LISTS_DOCS/'
    dirhomog =   workingdir+'/MONTHLIES/HOMOG/'
    dirraw =     workingdir+'/MONTHLIES/NETCDF/'

#*******************************************************
    # variable specific filepaths and directories
    # homogenised data file suffix
    datsuffix =   '_anoms'+CLMlab+'_homog'+nowmon+nowyear+'.nc'
    # homogenised temperature abs for working out uncertainties, calculating Td and super sat (T>Td)
    intmp =	      dirhomog+'IDPHANETCDF/TDIR/' # for calculating Td
    # For Td, Tw, q and e just use homogenised T if < Td (RH>100)
    # RH (derived from T and Td) cannot be < 0 or > 100 unless forced to be so by adjustment
    insat =       dirhomog+'IDPHANETCDF/RHDIR/' # SOME STATIONS WILL NOT BE THERE FOR RH

    # File with the missed adjustment uncertainty values in it
    inmissadj = dirlist+'Adjs_Stats.'+version+'_'+thenmon+thenyear+'.txt' 

# Find the missed adjustment uncertainty from the Adjs_Stats file for variable and homogtype
    GotMADJ = 0
    TheString = '%3s%7s     SDGSDFS:' % (param,homogtype)
    with open (inmissadj, 'rt') as myfile:
        
        for line in myfile:
	
            if line.find(TheString) != -1: # if there is a match with the variable, homogtype and sd of the gaussian distribution
    
                missadjerr = float(line[23:32]) # or if b'' float(foo.decode('utf-8')[23:33])
                GotMADJ = 1
                break
	    
    if (GotMADJ == 0):   # There should always be a CID!
	   
        print('No Missed Adjustment uncertainty found!')
        pdb.set_trace()
	    
    print('Check that the Missed ADjustment search is working: ',misadjerr)
    pdb.set_trace()

    # Dictionaries for filename and other things
    ParamDict = dict([('q',['q','Q','g/kg']),
	      ('rh',['RH','RH','%rh']),
	      ('t',['T','T','deg C']),
	      ('td',['Td','TD','deg C']),
	      ('tw',['Tw','TW','deg C']),
	      ('e',['e','E','hPa']),
	      ('dpd',['DPD','DPD','deg C'])])

    # Dictionary for looking up variable standard (not actually always standard!!!) names for netCDF output of variables
    NameDict = dict([('q',['specific_humidity',
                           'monthly mean 2m specific humidity']),
	             ('rh',['relative_humidity',
	                    'monthly mean 2m relative humidity anomaly']),
	             ('e',['vapour_pressure',
		           'monthly mean 2m vapour pressure anomaly']),
	             ('tw',['wetbulb_temperature',
		            'monthly mean 2m wetbulb temperature']),
	             ('t',['drybulb_temperature',
		           'monthly mean 2m dry bulb temperature']),
	             ('td',['dewpoint_temperature',
		            'monthly mean 2m dew point temperature']),
	             ('dpd',['dewpoint depression',
		            'monthly mean 2m dew point depression'])])

    inlist =	    dirlist+'goodforHadISDH.'+version+'_'+typee+var+'_'+thenmon+thenyear+'.txt'
    # just for Td PHADPD
    inlistS =	    dirlist+'PosthomogPHAdpd_anoms'+CLMlab+'_satsHadISDH.'+version+'_'+thenmon+thenyear+'.txt'	#need to use these to remove stations from 'goods' - and copy
    inlistB =	    dirlist+'PosthomogPHAdpd_anoms'+CLMlab+'_badsHadISDH.'+version+'_'+thenmon+thenyear+'.txt'	#need to use these to remove stations from 'goods' - and copy
    
    inhom =	    dirhomog+typee+'ASCII/'+ParamDict[var][1]+'DIR/'	    #***
    inlog =	    dirlist+'HadISDH.land'+ParamDict[var][0]+'.'+version+'_'+typee+'_'+thenmon+thenyear+'.log'     #***
    
    outlist =	    dirlist+'Posthomog'+typee+var+'_anoms'+CLMlab+'_goodsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
    outfunniesT =   dirlist+'Posthomog'+typee+var+'_anoms'+CLMlab+'_satsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
    outfunniesZ =   dirlist+'Posthomog'+typee+var+'_anoms'+CLMlab+'_subzerosHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
    outbads =	    dirlist+'Posthomog'+typee+var+'_anoms'+CLMlab+'_badsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'

    outdat =	    dirhomog+typee+'NETCDF/'+ParamDict[var][1]+'DIR/'
    outplots =    dirhomog+'STAT_PLOTS/UNCPLOTS/'+ParamDict[var][1]+'DIR/'

    homsuffix = '_'+typee+'adj.txt'
        
    if (typee == 'PHADPD'):

        inhom =	    dirhomog+'IDPHAASCII/TDDIR/'	    #***
        homsuffix = '_PHAadj.txt'
        outdat =    dirhomog+'IDPHANETCDF/TDDIR/'
        # DPD sats are identical to Td supersats because Td is built from T-DPD so no need to look at Td specifically
        call('cp '+inlistS+' '+outfunniesT,shell=True)
        #call(['cp', inlistS, outfunniesT] shell=False)
        # DPD bads should be identical to Td bads because homog Td is built from T-DPD (and DPD original from raw T-Td)
        # But - after creation of DPD some T stations will have had sections removed which would make Td have sections removed
        # relative to DPD - so a station could pass DPD but fail Td in terms of having enough months present over the climatology period
        # So we paste all DPD bads in and then append additional ones - there may be some duplicates!!!
        call('cp '+inlistB+' '+outbads,shell=True)
        #call(['cp', inlistB, outbads] shell=False)

GOT TO HERE
        filee = file.open(outbads,'a+')
        openw,99,outbads,/append
        filee.write('END OF DPD DERIVED FAILURES\n')
        filee.close()

    

    #--------------------------------------------------------
    # other variables and arrays 
    mdi = -999.      # FLOAT it was -1e+30 but netCDF files now save it as -999 because they are stored as integers to save space

    monarr =   ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    styr =     MYstyr
    edyr =     MYedyr
    clst =     MYclst - styr
    cled =     MYcled - styr
    nyrs =     (edyr + 1) - styr
    nmons =    nyrs * 12
    int_mons = np.arange(nmons) # if this is for netCDF times we're best of taking these from CreateMonthSeriesfromHadISD.py methods

    # UNCERTAINTIES IN MEASUREMENT
    rhbins = [-100,-40,-30,-20,-10,0,10,20,30,40,50,100]	# degrees C

    # 2 sigma
    ##rherr = [30,30,30,20,10,6,4,2.5,1.8,1.4,1.2] 
    #rherr = [30,30,30,20,10,5.5,3.6,2.7,2.2,1.9,1.6] 
    # 1 sigma
    rhunc =  [15,15,15,10,5,2.75,1.8,1.35,1.1,0.95,0.8] 

    t_unc =  0.2

    tw_unc = 0.15

    #---------------------------------------------------------
# Open and read in station list 
    MyTypes         = ("|U11","float","float","float","|U1","!U2","|U1","|U29","|U13")
    #MyTypes         = ("|S6","|S1","|S5","|S1","|S30","|S1","float","|S1","float","|S1","float","|S1","|S21")
    #MyTypes         = ("str","str","str","str","str","str","float","str","float","str","float","str","str")
    #MyTypes         = (str,str,str,str,str,str,float,str,float,str,float,str,str)
    MyDelimiters    = [11,8,10,7,1,2,1,29,13]
    RawData         = ReadData(inlist,MyTypes,MyDelimiters)
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
        if Restarter != '------' and Restarter != StationListID[st]:
            continue

        Restarter     = '------'
    
# find homog file and read in to array 
        infile = inhom+StationListID[st]+homsuffix
        MyTypes = np.append("|S12",["int"]*13)
        MyDelimiters = np.append([12,4,6],[9]*11)
        RawData      = ReadData(infile,MyTypes,MyDelimiters)
        
	stat_abs = np.array(()) # initiate empty array to append to
	for yy in range(nyrs):
            
	    moo = list(RawData[yy])
            
	    stat_abs = np.append(stat_abs,np.copy(moo[2:14]/100.)) 

        print('Check file read in: ',StationListID[st])
	pdb.set_trace()  
  
        stat_anoms = np.repeat(mdi,nmons)
        stat_clims = np.repeat(mdi,12)
        stat_sds =   np.repeat(mdi,12)
        stat_adjs =      np.repeat(0.,nmons)
        stat_adjs_err =  np.repeat(0.,nmons)
        stat_clims_err = np.repeat(mdi,nmons)
        stat_obs_err =   np.repeat(mdi,nmons)
        station_err =    np.repeat(mdi,nmons)

        bads = np.where(stat_abs == -99.99)
        if (len(bads[0]) > 0): 
	
            stat_abs[bads] = mdi # reset to -999 as this is what we'll need for putting in the netCDF files
    
        # Find subzeros and supersats (if relevant to variable), output to releavnt lists and then move on to next station
        # DO NOT PROCESS ANY FURTHER!!!
        # No relevance for T
        # subsats - RH, q, e should not be less than zero 
        # supersats - RH should not be greater than 100
        #             DPD should not be less than zero (derived Td then fine)
        #             Td should not be greater than 100% - using same listing as for DPD
        # COULD TRANSFER PROBLEMS IN RH or DPD TO ALL VARIABLES
        # FIND HOMOGENISED FILE IF IT EXISTS
    
    GOT TO THERE
    CASE param OF
      'dpd': BEGIN
        adjgoods = WHERE(tmparr NE mdi,countgadj)  
        countadj=0
        adjbads = WHERE(tmparr NE mdi AND tmparr LT 0.,countadj)
        IF (countadj GT 0) THEN BEGIN
          countfunnies = countfunnies+adjbads
          openw,98,outfunniesT,/append
          printf,98,wmo,'Funny supersats: ',countadj,countgadj,format='(a11,x,a16,i3,x,i3)'
          close,98
        ENDIF      
      END
      'td': BEGIN
# Td supersats are identical to DPD supersats so no need for separate search throuhg for the PHADPD version
# because we've already pasted the DPD supersats in.
        IF (homogtype EQ 'PHA') THEN BEGIN
	  fileeS = FILE_SEARCH(intmp+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count)
          IF (count GE 1) THEN BEGIN	#found the file, now open and search for sats and subsats
            inn=NCDF_OPEN(fileeS(0))
            satvar=NCDF_VARID(inn,'t_abs')
            NCDF_VARGET,inn,satvar,satstestees
            NCDF_CLOSE,inn
            adjgoods = WHERE(tmparr NE mdi,countgadj)  
            countadj = 0
            adjbads=WHERE(tmparr NE mdi AND satstestees NE mdi AND tmparr GT satstestees,countadj)
            IF (countadj GT 0) THEN BEGIN
              countfunnies = countfunnies+adjbads
              openw,98,outfunniesT,/append
              printf,98,wmo,'Funny supersats: ',countadj,countgadj,format='(a11,x,a16,i3,x,i3)'
              close,98
            ENDIF
          ENDIF
        ENDIF
      END
      'q': BEGIN
        fileeS = FILE_SEARCH(insat+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count)
	IF (count GE 1) THEN BEGIN	#found the file, now open and search for sats and subsats
          inn = NCDF_OPEN(fileeS(0))
          satvar = NCDF_VARID(inn,'rh_abs')
          NCDF_VARGET,inn,satvar,satstestees
          NCDF_CLOSE,inn
          adjgoods = WHERE(tmparr NE mdi,countgadj)  
          countadj = 0
          adjbads = WHERE(tmparr NE mdi AND satstestees NE mdi AND satstestees GT 100.,countadj)
          IF (countadj GT 0) THEN BEGIN
            countfunnies = countfunnies+adjbads
            openw,98,outfunniesT,/append
            printf,98,wmo,'Funny supersats: ',countadj,countgadj,format='(a11,x,a16,i3,x,i3)'
            close,98
          ENDIF
        ENDIF
	countadj = 0
        adjbads = WHERE(tmparr NE mdi AND tmparr LT 0.,countadj)
        IF (countadj GT 0) THEN BEGIN
          countfunnies = countfunnies+adjbads
          openw,98,outfunniesZ,/append
          printf,98,wmo,'Funny subzeros: ',countadj,countgadj,format='(a11,x,a16,i3,x,i3)'
          close,98
        ENDIF
      END
      'rh': BEGIN
        adjgoods = WHERE(tmparr NE mdi,countgadj)  
        countadj = 0
        adjbads = WHERE(tmparr NE mdi AND tmparr LT 0.,countadj)
        IF (countadj GT 0) THEN BEGIN
          countfunnies = countfunnies+adjbads
          openw,98,outfunniesZ,/append
          printf,98,wmo,'Funny subzeros: ',countadj,countgadj,format='(a11,x,a16,i3,x,i3)'
          close,98
        ENDIF      
        countadj = 0
        adjbads=WHERE(tmparr NE mdi AND tmparr GT 100.,countadj)
        IF (countadj GT 0) THEN BEGIN
          countfunnies = countfunnies+adjbads
          openw,98,outfunniesT,/append
          printf,98,wmo,'Funny supersats: ',countadj,countgadj,format='(a11,x,a16,i3,x,i3)'
          close,98
        ENDIF      
      END
      'e': BEGIN
        fileeS=FILE_SEARCH(insat+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count)
        IF (count GE 1) THEN BEGIN	#found the file, now open and search for sats and subsats
          inn = NCDF_OPEN(fileeS(0))
          satvar = NCDF_VARID(inn,'rh_abs')
          NCDF_VARGET,inn,satvar,satstestees
          NCDF_CLOSE,inn
          adjgoods = WHERE(tmparr NE mdi,countgadj)  
          countadj = 0
          adjbads = WHERE(tmparr NE mdi AND satstestees NE mdi AND satstestees GT 100.,countadj)
          IF (countadj GT 0) THEN BEGIN
            countfunnies = countfunnies+adjbads
            openw,98,outfunniesT,/append
            printf,98,wmo,'Funny supersats: ',countadj,countgadj,format='(a11,x,a16,i3,x,i3)'
            close,98
          ENDIF
        ENDIF      
        countadj=0
        adjbads = WHERE(tmparr NE mdi AND tmparr LT 0.,countadj)
        IF (countadj GT 0) THEN BEGIN
          countfunnies = countfunnies+adjbads
          openw,98,outfunniesZ,/append
          printf,98,wmo,'Funny subzeros: ',countadj,countgadj,format='(a11,x,a16,i3,x,i3)'
          close,98
        ENDIF
      END
      'tw': BEGIN
        fileeS = FILE_SEARCH(intmp+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count)
        IF (count GE 1) THEN BEGIN	#found the file, now open and search for sats and subsats
          inn = NCDF_OPEN(fileeS(0))
          satvar = NCDF_VARID(inn,'t_abs')
          NCDF_VARGET,inn,satvar,satstestees
          NCDF_CLOSE,inn
          adjgoods = WHERE(tmparr NE mdi,countgadj)  
          countadj = 0
          adjbads = WHERE(tmparr NE mdi AND satstestees NE mdi AND satstestees LT tmparr,countadj)
          IF (countadj GT 0) THEN BEGIN
            countfunnies = countfunnies+adjbads
            openw,98,outfunniesT,/append
            printf,98,wmo,'Funny supersats: ',countadj,countgadj,format='(a11,x,a16,i3,x,i3)'
            close,98
          ENDIF
        ENDIF      
      END
      't': BEGIN
      END
    ENDCASE
    
    stat_abs(*)=REFORM(tmparr,nmons)

#create stat anoms and clims from homogenised abs
    # derive and apply Eclims
    stat_clims_err = REFORM(stat_clims_err,12,nyrs)
    FOR mm=0,11 DO BEGIN
      subclm = tmparr(mm,clst:cled)
      clgots = WHERE(subclm NE mdi,countcl)
      gots =   WHERE(tmparr(mm,*) NE mdi,count)
      IF (countcl GE 15) THEN BEGIN
        stat_clims(mm) =       MEAN(subclm(clgots))
	stat_sds(mm) =         STDDEV(subclm(clgots))
	tmparr(mm,gots) =      tmparr(mm,gots)-stat_clims(mm)
	stat_clims_err(mm,*) = (stat_sds(mm)/SQRT(countcl))*2 # we want 2 sigma error!
      ENDIF ELSE BEGIN
        openw,99,outbads,/append
	printf,99,wmo,'TOO FEW FOR CLIM: ',countcl,format='(a11,x,a18,i2)'
	close,99
        goto,beginagain
      ENDELSE
    ENDFOR
    stat_anoms =     REFORM(tmparr,nmons)
    stat_clims_err = REFORM(stat_clims_err,nmons)

# Work out the relative measurement uncertainty
# NEW METHOD JAN2014
# ADD IN ERROR IN T SOMEHOW??? could just add to Tw error for a worst case scenario T err = 0.2 from Brohan et al 2006
#**********************************************
    CASE param OF
      't': BEGIN
# FOR T: easy - +/- 0.2deg
        gots = WHERE(stat_abs NE mdi,count)
        IF (count GT 0) THEN stat_obs_err(gots) = 2*(t_unc/SQRT(60.))	#now a 1 sigma error so multiply by 2
      END
# WET BULB ERROR pre 1980 (mostly)
# 0.15 degrees
# 15%rh at -50 deg C T, 0.8 %rh at 50 deg C T
# scale all error based on %rh at T
      'tw': BEGIN
# FOR Tw - easy - +/- 0.15deg
        gots = WHERE(stat_abs NE mdi,count)
        IF (count GT 0) THEN stat_obs_err(gots) = 2*(tw_unc/SQRT(60.))	#now a 1 sigma error so multiply by 2
      END
      'rh': BEGIN
# FOR RH - easy - bin from -50 to 50 deg C and apply table of %rh errors
        filoo = FILE_SEARCH(intmp+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count)
        IF (count GT 0) THEN BEGIN
          inn = NCDF_OPEN(filoo(0))
          tmpid = NCDF_VARID(inn,'t_abs')
          NCDF_VARGET,inn,tmpid,abstmp
          NCDF_CLOSE,inn
	  bads = WHERE(abstmp EQ mdi,countB)
	  IF (countB GT 0) THEN abstmp(bads) = 0.	# assuming a 0 deg/3 %rh error if no data exist
          gots = WHERE(stat_abs NE mdi AND abstmp NE mdi,countboth)
          IF (countboth GT 0) THEN BEGIN
            FOR bins = 0,10 DO BEGIN
	      founds = WHERE(abstmp(gots) GE rhbins(bins) AND abstmp(gots) LT rhbins(bins+1),countf) #all vals within bin
	      IF (countf GT 0) THEN BEGIN
	        stat_obs_err(gots(founds)) = 2.*(rhunc(bins)/SQRT(60.))   
	      ENDIF
	    ENDFOR
	  ENDIF      
        ENDIF ELSE stat_obs_err(*) = 2*(3./SQRT(60.))	# NO TEMPERATURE DATA SO ASSUME MODERATE UNCERTAINTY OF 3%
      END      
      'q': BEGIN
# FOR q: (ASSUME RH=80% IF NO RH FILE/OB EXISTS, and 3%rh uncertainty IF NO TEMPERATURE FILE/OB EXIST)
#	qsat=(q/RH)*100
# 	q+err=((RH+err)/100)*qsat
#	qerr=(q+err)-q
        filoo = FILE_SEARCH(insat+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count)
        IF (count GT 0) THEN BEGIN		# IF RH file exists carry on if not assume 80% everywhere
          inn = NCDF_OPEN(filoo(0))
          tmpid = NCDF_VARID(inn,'rh_abs')
          NCDF_VARGET,inn,tmpid,absrh
          NCDF_CLOSE,inn
	  bads = WHERE(absrh EQ mdi,countB)
	  IF (countB GT 0) THEN absrh(bads) = 80.	# assuming 80%rh if no data exist
	ENDIF ELSE absrh=make_array(nmons,/float,value=80.)
        filoo = FILE_SEARCH(intmp+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count) # IF T DOES NOT EXIST ASSUME bin 0/3%rh uncertainty (moderate)
        IF (count GT 0) THEN BEGIN
          inn =   NCDF_OPEN(filoo(0))
          tmpid = NCDF_VARID(inn,'t_abs')
          NCDF_VARGET,inn,tmpid,abstmp
          NCDF_CLOSE,inn
	  bads =  WHERE(abstmp EQ mdi,countB)
	  IF (countB GT 0) THEN abstmp(bads) = 0.	# assuming a 0 deg/3 %rh error if no data exist
	ENDIF ELSE abstmp = make_array(nmons,/float,value=0.)
	monsathums =        make_array(nmons,/float,value=mdi)
	monhumerr =         make_array(nmons,/float,value=mdi)
        gots =              WHERE(stat_abs NE mdi AND absrh NE mdi and abstmp NE mdi,countboth)
	monsathums(gots) = (stat_abs(gots)/absrh(gots))*100.
        IF (countboth GT 0) THEN BEGIN
          FOR bins = 0,10 DO BEGIN
	    founds = WHERE(abstmp(gots) GE rhbins(bins) AND abstmp(gots) LT rhbins(bins+1),countf) #all vals within bin
	    IF (countf GT 0) THEN BEGIN
	      absrh(gots(founds)) = absrh(gots(founds))+rhunc(bins)
	    ENDIF
	  ENDFOR
	  monhumerr(gots) = (absrh(gots)/100.)*monsathums(gots)
	  stat_obs_err(gots) = 2.*((monhumerr(gots)-stat_abs(gots))/SQRT(60.))   
#	  stop,'check for silly values'	# No max RH so could go over 100 but would just result in a large q error - cannot go below 0 anyway
        ENDIF
      END

      'e': BEGIN
# FOR e: (ASSUME RH=80% IF NO RH FILE/OB EXISTS, and 3%rh uncertainty IF NO TEMPERATURE FILE/OB EXIST)
#	esat=(e/RH)*100
# 	e+err=((RH+err)/100)*esat
#	eerr=(e+err)-e
        filoo = FILE_SEARCH(insat+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count)
        IF (count GT 0) THEN BEGIN		# IF RH file exists carry on if not assume 80% everywhere
          inn = NCDF_OPEN(filoo(0))
          tmpid = NCDF_VARID(inn,'rh_abs')
          NCDF_VARGET,inn,tmpid,absrh
          NCDF_CLOSE,inn
	  bads = WHERE(absrh EQ mdi,countB)
	  IF (countB GT 0) THEN absrh(bads)=80.	# assuming 80%rh if no data exist
	ENDIF ELSE absrh=make_array(nmons,/float,value=80.)
        filoo = FILE_SEARCH(intmp+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count) # IF T DOES NOT EXIST ASSUME bin 0/3%rh uncertainty (moderate)
        IF (count GT 0) THEN BEGIN
          inn = NCDF_OPEN(filoo(0))
          tmpid = NCDF_VARID(inn,'t_abs')
          NCDF_VARGET,inn,tmpid,abstmp
          NCDF_CLOSE,inn
	  bads = WHERE(abstmp EQ mdi,countB)
	  IF (countB GT 0) THEN abstmp(bads)=0.	# assuming a 0 deg/3 %rh error if no data exist
	ENDIF ELSE abstmp = make_array(nmons,/float,value=0.)
	monsathums =       make_array(nmons,/float,value=mdi)
	monhumerr =        make_array(nmons,/float,value=mdi)
        gots =             WHERE(stat_abs NE mdi AND absrh NE mdi and abstmp NE mdi,countboth)
	monsathums(gots) = (stat_abs(gots)/absrh(gots))*100.
        IF (countboth GT 0) THEN BEGIN
          FOR bins = 0,10 DO BEGIN
	    founds = WHERE(abstmp(gots) GE rhbins(bins) AND abstmp(gots) LT rhbins(bins+1),countf) #all vals within bin
	    IF (countf GT 0) THEN BEGIN
	      absrh(gots(founds)) = absrh(gots(founds))+rhunc(bins)
	    ENDIF
	  ENDFOR
	  monhumerr(gots) = (absrh(gots)/100.)*monsathums(gots)
	  stat_obs_err(gots) = 2.*((monhumerr(gots)-stat_abs(gots))/SQRT(60.))   
#	  stop,'check for silly values'	# No max RH so could go over 100 but would just result in a large q error - cannot go below 0 anyway
        ENDIF
      END

      'td': BEGIN
# FOR Td: use error in e. (ASSUME RH=80% IF NO RH FILE/OB EXISTS, and 3%rh uncertainty IF NO TEMPERATURE FILE/OB EXIST)
# 	e=e(Td)
#	esat=(e/RH)*100
# 	e+err=((RH+err)/100)*esat
#	Td+err=Td+err(e+err)
#	Tderr=(Td+err)-Td
        filoo = FILE_SEARCH(insat+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count)
        IF (count GT 0) THEN BEGIN		# IF RH file exists carry on if not assume 80% everywhere
          inn = NCDF_OPEN(filoo(0))
          tmpid = NCDF_VARID(inn,'rh_abs')
          NCDF_VARGET,inn,tmpid,absrh
          NCDF_CLOSE,inn
	  bads = WHERE(absrh EQ mdi,countB)
	  IF (countB GT 0) THEN absrh(bads) = 80.	# assuming 80%rh if no data exist
	ENDIF ELSE absrh = make_array(nmons,/float,value=80.)
        filoo = FILE_SEARCH(intmp+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count) # IF T DOES NOT EXIST ASSUME bin 0/3%rh uncertainty (moderate)
        IF (count GT 0) THEN BEGIN
          inn = NCDF_OPEN(filoo(0))
          tmpid = NCDF_VARID(inn,'t_abs')
          NCDF_VARGET,inn,tmpid,abstmp
          NCDF_CLOSE,inn
	  bads = WHERE(abstmp EQ mdi,countB)
	  IF (countB GT 0) THEN abstmp(bads)=0.	# assuming a 0 deg/3 %rh error if no data exist
	ENDIF ELSE abstmp=make_array(nmons,/float,value=0.)
# THIS WILL NEVER READ IN BECAUSE FILE HAS A HYPHEN SO WE'RE ALWAYS USING HOMOGENISED T and STANDARD P!!!
#	filoo=FILE_SEARCH(dirraw+strmid(wmo,0,6)+strmid(wmo,6,5)+'*',count=count)
#        IF (count GT 0) THEN BEGIN
#          inn=NCDF_OPEN(filoo(0))
#          tmpid=NCDF_VARID(inn,'temp_abs')
#          stP_id=NCDF_VARID(inn,'station_Pclim')
#          NCDF_VARGET,inn,tmpid,abstmp
#          NCDF_VARGET,inn,stP_id,statP_arr
#          NCDF_CLOSE,inn
#        ENDIF ELSE statP_arr=make_array(nmons,/float,value=1013) # IF P station DOES NOT EXIST ASSUME STANDARD PRESSURE
# MODIFIED AUGUST 2016 TO MAKE SURE IT READS IN 20CR Climatological P rather than using standard P
	filoo = FILE_SEARCH(dirraw+strmid(wmo,0,6)+'-'+strmid(wmo,6,5)+'*',count=count)
        IF (count GT 0) THEN BEGIN
          inn = NCDF_OPEN(filoo(0))
          #tmpid=NCDF_VARID(inn,'temp_abs') # already read in abstmp from homogenised T
          stP_id = NCDF_VARID(inn,'20CRstation_Pclim')
          #NCDF_VARGET,inn,tmpid,abstmp
          NCDF_VARGET,inn,stP_id,statP_arr
          NCDF_CLOSE,inn
        ENDIF ELSE statP_arr = make_array(nmons,/float,value=1013) # IF P station DOES NOT EXIST ASSUME STANDARD PRESSURE
	monhums =          make_array(nmons,/float,value=mdi)
	monsathums =       make_array(nmons,/float,value=mdi)
	monhumerr =        make_array(nmons,/float,value=mdi)
	montderr =         make_array(nmons,/float,value=mdi)
        gots =             WHERE(stat_abs NE mdi AND absrh NE mdi and abstmp NE mdi,countboth)
	monhums(gots) =    calc_evap(stat_abs(gots),statP_arr(gots))
	monsathums(gots) = (monhums(gots)/absrh(gots))*100.
        IF (countboth GT 0) THEN BEGIN
          FOR bins = 0,10 DO BEGIN
	    founds = WHERE(abstmp(gots) GE rhbins(bins) AND abstmp(gots) LT rhbins(bins+1),countf) #all vals within bin
	    IF (countf GT 0) THEN BEGIN
	      absrh(gots(founds)) = absrh(gots(founds))+rhunc(bins)
	    ENDIF
	  ENDFOR
	  monhumerr(gots) =    (absrh(gots)/100.)*monsathums(gots)
	  montderr(gots) =     calc_dewp(monhumerr(gots),statP_arr(gots))
	  stat_obs_err(gots) = 2.*((montderr(gots)-stat_abs(gots))/SQRT(60.))   
#	  stop,'check for silly values'	# No max RH so could go over 100 but would just result in a large q error - cannot go below 0 anyway
	ENDIF      
      END
      'dpd': BEGIN
      # add monthly Td error + 0.2 from T then div by SQRT(60.)
# 	e=e(Td)
#	esat=(e/RH)*100
# 	e+err=((RH+err)/100)*esat
#	Td+err=Td+err(e+err)
#	Tderr=(Td+err)-Td
#	add 0.2 from T
        # read in RH, make missing 80%
	filoo = FILE_SEARCH(insat+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count)
        IF (count GT 0) THEN BEGIN		# IF RH file exists carry on if not assume 80% everywhere
          inn = NCDF_OPEN(filoo(0))
          tmpid = NCDF_VARID(inn,'rh_abs')
          NCDF_VARGET,inn,tmpid,absrh
          NCDF_CLOSE,inn
	  bads = WHERE(absrh EQ mdi,countB)
	  IF (countB GT 0) THEN absrh(bads) = 80.	# assuming 80%rh if no data exist
	ENDIF ELSE absrh=make_array(nmons,/float,value=80.)
        # read in T, make missing 0 deg C adn missing Td T minus DPD
	filoo = FILE_SEARCH(intmp+strmid(wmo,0,6)+strmid(wmo,6,5)+datsuffix,count=count) # IF T DOES NOT EXIST ASSUME bin 0/3%rh uncertainty (moderate)
        IF (count GT 0) THEN BEGIN
          inn = NCDF_OPEN(filoo(0))
          tmpid = NCDF_VARID(inn,'t_abs')
          NCDF_VARGET,inn,tmpid,abstmp
          NCDF_CLOSE,inn
	  bads = WHERE(abstmp EQ mdi,countB)
	  IF (countB GT 0) THEN abstmp(bads) = 0.	# assuming a 0 deg/3 %rh error if no data exist
	ENDIF ELSE abstmp = make_array(nmons,/float,value=0.)
        # read in Td
# BUT WE'RE DOING DPD BEFORE TD SO THE NETCDF WON'T BE COMPLETED
# Td = homog T-DPD anyway SO CAN JUST USE homog T and DPD
#	filoo = FILE_SEARCH(intdp+strmid(wmo,0,6)+strmid(wmo,6,5)+'*',count=count)
#        IF (count GT 0) THEN BEGIN		# IF Td file exists carry on if not use T-DPD
#          inn = NCDF_OPEN(filoo(0))
#          tmpid = NCDF_VARID(inn,'td_abs')
#          NCDF_VARGET,inn,tmpid,abstd
#          NCDF_CLOSE,inn
#	  bads = WHERE(abstd EQ mdi AND stat_abs NE mdi,countB)
#	  IF (countB GT 0) THEN abstd(bads) = abstmp(bads)-stat_abs(bads)	# use T-DPD if no file exists (it should!)
#	ENDIF ELSE BEGIN
	  gots = WHERE(abstmp NE mdi AND stat_abs NE mdi,countB)
	  abstd = make_array(nmons,/float,value=mdi)
	  abstd(gots) = abstmp(gots)-stat_abs(gots)
#	ENDELSE
	# read in P
# THIS WILL NEVER READ IN BECAUSE FILE HAS A HYPHEN SO WE'RE ALWAYS USING HOMOGENISED T and STANDARD P!!!
#	filoo = FILE_SEARCH(dirraw+strmid(wmo,0,6)+strmid(wmo,6,5)+'*',count=count)
#        IF (count GT 0) THEN BEGIN
#          inn = NCDF_OPEN(filoo(0))
#          tmpid = NCDF_VARID(inn,'temp_abs')
#          stP_id = NCDF_VARID(inn,'station_Pclim')
#          NCDF_VARGET,inn,tmpid,abstmp
#          NCDF_VARGET,inn,stP_id,statP_arr
#          NCDF_CLOSE,inn
#        ENDIF ELSE statP_arr = make_array(nmons,/float,value=1013) # IF P station DOES NOT EXIST ASSUME STANDARD PRESSURE
# MODIFIED AUGUST 2016 TO MAKE SURE IT READS IN 20CR Climatological P rather than using standard P
	filoo = FILE_SEARCH(dirraw+strmid(wmo,0,6)+'-'+strmid(wmo,6,5)+'*',count=count)
        IF (count GT 0) THEN BEGIN
          inn = NCDF_OPEN(filoo(0))
          #tmpid=NCDF_VARID(inn,'temp_abs') # already read in abstmp from homogenised T
          stP_id = NCDF_VARID(inn,'20CRstation_Pclim')
          #NCDF_VARGET,inn,tmpid,abstmp
          NCDF_VARGET,inn,stP_id,statP_arr
          NCDF_CLOSE,inn
        ENDIF ELSE statP_arr = make_array(nmons,/float,value=1013) # IF P station DOES NOT EXIST ASSUME STANDARD PRESSURE
	monhums =          make_array(nmons,/float,value=mdi)
	monsathums =       make_array(nmons,/float,value=mdi)
	monhumerr =        make_array(nmons,/float,value=mdi)
	montderr =         make_array(nmons,/float,value=mdi)
        gots =             WHERE(stat_abs NE mdi,countboth)
	monhums(gots) =    calc_evap(abstd(gots),statP_arr(gots))
	monsathums(gots) = (monhums(gots)/absrh(gots))*100.
        IF (countboth GT 0) THEN BEGIN
          FOR bins=0,10 DO BEGIN
	    founds = WHERE(abstmp(gots) GE rhbins(bins) AND abstmp(gots) LT rhbins(bins+1),countf) #all vals within bin
	    IF (countf GT 0) THEN BEGIN
	      absrh(gots(founds)) = absrh(gots(founds))+rhunc(bins)
	    ENDIF
	  ENDFOR
	  monhumerr(gots) =    (absrh(gots)/100.)*monsathums(gots)
	  montderr(gots) =     calc_dewp(monhumerr(gots),statP_arr(gots))
	  stat_obs_err(gots) = 2.*(((montderr(gots)-abstd(gots))+0.2)/SQRT(60.))   
#	  stop,'check for silly values'	# No max RH so could go over 100 but would just result in a large q error - cannot go below 0 anyway
	ENDIF      
      END
    ENDCASE

#**********************************************

# RH SENSOR ERROR (post 1980 - progressively)

# read in log and find adjustment uncertainties - apply
    IF (homogtype EQ 'PHA') THEN findline = '^Adj write:'+strcompress(wmo,/remove_all) $
                            ELSE findline = '^'+strcompress(wmo,/remove_all)
    spawn,'grep "'+findline+'" '+inlog+' > tmp.arr'
    openr,4,'tmp.arr'
    WHILE NOT EOF(4) DO BEGIN
      stmon =  0 
      edmon =  0
      ibreak = 0
      cbreak = 0
      adj =    0.
      eadj =   0.
      IF (homogtype EQ 'PHA') THEN readf,4,stmon,edmon,ibreak,cbreak,adj,eadj,format='(32x,i4,16x,i4,12x,i1,4x,i1,2(x,f6.2),x)' $
                              ELSE readf,4,stmon,edmon,adj,eadj,format='(14x,i4,i4,14x,2(f7.2))'
      print,stmon,edmon,ibreak,cbreak,adj,eadj
      stat_adjs(stmon-1:edmon-1) = -(adj) # these go from 1+, not 0+, first in loop is most recent period - no adjustment here      
      # THIS IS A 5th-95th so 1.65 sigma
      # divide by 1.65 then multiply by 2 to get 2sigma error - consistent with everything else then.
      IF (eadj GT 0.0) THEN stat_adjs_err(stmon-1:edmon-1) = (eadj/1.65) # NOT NEEDED? -> ELSE stat_adjs_err(stmon-1:edmon-1)=0.   
    ENDWHILE
    close,4
    spawn,'rm tmp.arr'

# add in the flat adjustment error for missed adjustments derived from teh missing middle
# this is 0.16 at 1 sigma  
# combine in quadtrature 2 give a 2 sigma error
    stat_adjs_err(*) = 2*(SQRT((stat_adjs_err(*)^2)+(missadjerr^2))) 
#    stop,'check missed adj'
  #calc station error
    errs = WHERE(stat_obs_err NE mdi AND stat_clims_err NE mdi AND stat_adjs_err NE mdi,counte)
    IF (counte GT 0) THEN station_err(errs) = $
    (SQRT(((stat_obs_err(errs)/2.)^2)+((stat_clims_err(errs)/2.)^2)+((stat_adjs_err(errs)/2.)^2)))*2
    # this gives a 2 sigma uncertainty

  # now output all of this to a netCDF file
    valid = WHERE(stat_anoms NE mdi,c)
    IF (c GE 1) THEN BEGIN
      min_anm = MIN(stat_anoms(valid))
      max_anm = MAX(stat_anoms(valid))
      min_abs = MIN(stat_abs(valid))
      max_abs = MAX(stat_abs(valid))
      min_unc = MIN(station_err(valid))
      max_unc = MAX(station_err(valid))
    ENDIF

    #write to netCDF file
    wilma = NCDF_CREATE(outdat+wmo+datsuffix,/clobber)
  
    tid =    NCDF_DIMDEF(wilma,'time',nmons)
    clmid =  NCDF_DIMDEF(wilma,'month',12)
    charid = NCDF_DIMDEF(wilma, 'Character', 3)
  
    timesvar = NCDF_VARDEF(wilma,'times',[tid],/SHORT)

    CASE param OF 
      'dpd': BEGIN
        tanomvar = NCDF_VARDEF(wilma,'dpd_anoms',[tid],/FLOAT)
        tabsvar =  NCDF_VARDEF(wilma,'dpd_abs',[tid],/FLOAT)
        tadj =     NCDF_VARDEF(wilma,'dpd_adjustments',[tid],/FLOAT)
        tunc =     NCDF_VARDEF(wilma,'dpd_uncertainty',[tid],/FLOAT)
        tobserr =  NCDF_VARDEF(wilma,'dpd_obserr',[tid],/FLOAT)
        tadjerr =  NCDF_VARDEF(wilma,'dpd_adjerr',[tid],/FLOAT)
        tclmerr =  NCDF_VARDEF(wilma,'dpd_clmerr',[tid],/FLOAT)
        tsdvar =   NCDF_VARDEF(wilma,'dpd_stds',[clmid],/FLOAT)
        tclmvar =  NCDF_VARDEF(wilma,'dpd_clims',[clmid],/FLOAT)
      END
      'td': BEGIN
        tanomvar = NCDF_VARDEF(wilma,'td_anoms',[tid],/FLOAT)
        tabsvar =  NCDF_VARDEF(wilma,'td_abs',[tid],/FLOAT)
        tadj =     NCDF_VARDEF(wilma,'td_adjustments',[tid],/FLOAT)
        tunc =     NCDF_VARDEF(wilma,'td_uncertainty',[tid],/FLOAT)
        tobserr =  NCDF_VARDEF(wilma,'td_obserr',[tid],/FLOAT)
        tadjerr =  NCDF_VARDEF(wilma,'td_adjerr',[tid],/FLOAT)
        tclmerr =  NCDF_VARDEF(wilma,'td_clmerr',[tid],/FLOAT)
        tsdvar =   NCDF_VARDEF(wilma,'td_stds',[clmid],/FLOAT)
        tclmvar =  NCDF_VARDEF(wilma,'td_clims',[clmid],/FLOAT)
      END
      't': BEGIN
        tanomvar = NCDF_VARDEF(wilma,'t_anoms',[tid],/FLOAT)
        tabsvar =  NCDF_VARDEF(wilma,'t_abs',[tid],/FLOAT)
        tadj =     NCDF_VARDEF(wilma,'t_adjustments',[tid],/FLOAT)
        tunc =     NCDF_VARDEF(wilma,'t_uncertainty',[tid],/FLOAT)
        tobserr =  NCDF_VARDEF(wilma,'t_obserr',[tid],/FLOAT)
        tadjerr =  NCDF_VARDEF(wilma,'t_adjerr',[tid],/FLOAT)
        tclmerr =  NCDF_VARDEF(wilma,'t_clmerr',[tid],/FLOAT)
        tsdvar =   NCDF_VARDEF(wilma,'t_stds',[clmid],/FLOAT)
        tclmvar =  NCDF_VARDEF(wilma,'t_clims',[clmid],/FLOAT)
      END
      'tw': BEGIN
        tanomvar = NCDF_VARDEF(wilma,'tw_anoms',[tid],/FLOAT)
        tabsvar =  NCDF_VARDEF(wilma,'tw_abs',[tid],/FLOAT)
        tadj =     NCDF_VARDEF(wilma,'tw_adjustments',[tid],/FLOAT)
        tunc =     NCDF_VARDEF(wilma,'tw_uncertainty',[tid],/FLOAT)
        tobserr =  NCDF_VARDEF(wilma,'tw_obserr',[tid],/FLOAT)
        tadjerr =  NCDF_VARDEF(wilma,'tw_adjerr',[tid],/FLOAT)
        tclmerr =  NCDF_VARDEF(wilma,'tw_clmerr',[tid],/FLOAT)
        tsdvar =   NCDF_VARDEF(wilma,'tw_stds',[clmid],/FLOAT)
        tclmvar =  NCDF_VARDEF(wilma,'tw_clims',[clmid],/FLOAT)
      END
      'q': BEGIN
        tanomvar = NCDF_VARDEF(wilma,'q_anoms',[tid],/FLOAT)
        tabsvar =  NCDF_VARDEF(wilma,'q_abs',[tid],/FLOAT)
        tadj =     NCDF_VARDEF(wilma,'q_adjustments',[tid],/FLOAT)
        tunc =     NCDF_VARDEF(wilma,'q_uncertainty',[tid],/FLOAT)
        tobserr =  NCDF_VARDEF(wilma,'q_obserr',[tid],/FLOAT)
        tadjerr =  NCDF_VARDEF(wilma,'q_adjerr',[tid],/FLOAT)
        tclmerr =  NCDF_VARDEF(wilma,'q_clmerr',[tid],/FLOAT)
        tsdvar =   NCDF_VARDEF(wilma,'q_stds',[clmid],/FLOAT)
        tclmvar =  NCDF_VARDEF(wilma,'q_clims',[clmid],/FLOAT)
      END
      'e': BEGIN
        tanomvar = NCDF_VARDEF(wilma,'e_anoms',[tid],/FLOAT)
        tabsvar =  NCDF_VARDEF(wilma,'e_abs',[tid],/FLOAT)
        tadj =     NCDF_VARDEF(wilma,'e_adjustments',[tid],/FLOAT)
        tunc =     NCDF_VARDEF(wilma,'e_uncertainty',[tid],/FLOAT)
        tobserr =  NCDF_VARDEF(wilma,'e_obserr',[tid],/FLOAT)
        tadjerr =  NCDF_VARDEF(wilma,'e_adjerr',[tid],/FLOAT)
        tclmerr =  NCDF_VARDEF(wilma,'e_clmerr',[tid],/FLOAT)
        tsdvar =   NCDF_VARDEF(wilma,'e_stds',[clmid],/FLOAT)
        tclmvar =  NCDF_VARDEF(wilma,'e_clims',[clmid],/FLOAT)
      END
      'rh': BEGIN
        tanomvar = NCDF_VARDEF(wilma,'rh_anoms',[tid],/FLOAT)
        tabsvar =  NCDF_VARDEF(wilma,'rh_abs',[tid],/FLOAT)
        tadj =     NCDF_VARDEF(wilma,'rh_adjustments',[tid],/FLOAT)
        tunc =     NCDF_VARDEF(wilma,'rh_uncertainty',[tid],/FLOAT)
        tobserr =  NCDF_VARDEF(wilma,'rh_obserr',[tid],/FLOAT)
        tadjerr =  NCDF_VARDEF(wilma,'rh_adjerr',[tid],/FLOAT)
        tclmerr =  NCDF_VARDEF(wilma,'rh_clmerr',[tid],/FLOAT)
        tsdvar =   NCDF_VARDEF(wilma,'rh_stds',[clmid],/FLOAT)
        tclmvar =  NCDF_VARDEF(wilma,'rh_clims',[clmid],/FLOAT)
      END  
    ENDCASE

    climsvar = NCDF_VARDEF(wilma,'months',[charid,clmid],/CHAR)

    NCDF_ATTPUT,wilma,'times','long_name','time'
    NCDF_ATTPUT,wilma,'times','units','months beginning Jan 1973'
    NCDF_ATTPUT,wilma,'times','axis','T'
    NCDF_ATTPUT,wilma,'times','calendar','gregorian'
    NCDF_ATTPUT,wilma,'times','valid_min',0.
    NCDF_ATTPUT,wilma,'months','long_name','month'
    NCDF_ATTPUT,wilma,'months','units','months of the year'

    NCDF_ATTPUT,wilma,tanomvar,'long_name','Monthly mean anomaly'
    NCDF_ATTPUT,wilma,tanomvar,'units',unitees
    NCDF_ATTPUT,wilma,tanomvar,'axis','T'
    NCDF_ATTPUT,wilma,tanomvar,'valid_min',min_anm
    NCDF_ATTPUT,wilma,tanomvar,'valid_max',max_anm
    NCDF_ATTPUT,wilma,tanomvar,'missing_value',mdi
    NCDF_ATTPUT,wilma,tabsvar,'long_name','Monthly mean absolutes'
    NCDF_ATTPUT,wilma,tabsvar,'units',unitees
    NCDF_ATTPUT,wilma,tabsvar,'axis','T'
    NCDF_ATTPUT,wilma,tabsvar,'valid_min',min_abs
    NCDF_ATTPUT,wilma,tabsvar,'valid_max',max_abs
    NCDF_ATTPUT,wilma,tabsvar,'missing_value',mdi
    NCDF_ATTPUT,wilma,tunc,'long_name','Monthly mean uncertainties'
    NCDF_ATTPUT,wilma,tunc,'units',unitees
    NCDF_ATTPUT,wilma,tunc,'axis','T'
    NCDF_ATTPUT,wilma,tunc,'valid_min',min_unc
    NCDF_ATTPUT,wilma,tunc,'valid_max',max_unc
    NCDF_ATTPUT,wilma,tunc,'missing_value',mdi
    NCDF_ATTPUT,wilma,tadj,'long_name','Monthly mean absjustments from NCDCs Pairwise'
    NCDF_ATTPUT,wilma,tadj,'units',unitees
    NCDF_ATTPUT,wilma,tadj,'axis','T'
    NCDF_ATTPUT,wilma,tadj,'missing_value',mdi
    NCDF_ATTPUT,wilma,tobserr,'long_name','Measurement error estimate'
    NCDF_ATTPUT,wilma,tobserr,'units',unitees
    NCDF_ATTPUT,wilma,tobserr,'axis','T'
    NCDF_ATTPUT,wilma,tobserr,'missing_value',mdi
    NCDF_ATTPUT,wilma,tadjerr,'long_name','Adjustment error estimate'
    NCDF_ATTPUT,wilma,tadjerr,'units',unitees
    NCDF_ATTPUT,wilma,tadjerr,'axis','T'
    NCDF_ATTPUT,wilma,tadjerr,'missing_value',mdi
    NCDF_ATTPUT,wilma,tclmerr,'long_name','Climatology error estimate'
    NCDF_ATTPUT,wilma,tclmerr,'units',unitees
    NCDF_ATTPUT,wilma,tclmerr,'axis','T'
    NCDF_ATTPUT,wilma,tclmerr,'missing_value',mdi
    NCDF_ATTPUT,wilma,tsdvar,'long_name','Monthly climatological st dev'
    NCDF_ATTPUT,wilma,tsdvar,'units',unitees
    NCDF_ATTPUT,wilma,tsdvar,'missing_value',mdi
    NCDF_ATTPUT,wilma,tclmvar,'long_name','Monthly climatology'
    NCDF_ATTPUT,wilma,tclmvar,'units',unitees
    NCDF_ATTPUT,wilma,tclmvar,'missing_value',mdi

    NCDF_ATTPUT,wilma,/GLOBAL,'station_information','Where station is a composite the station id refers to the primary source used in the timestep and may not apply to all elements'
    current_time = SYSTIME()
#PRINT,current_time
    NCDF_ATTPUT,wilma,/GLOBAL,'file_created',STRING(current_time)
    NCDF_CONTROL,wilma,/ENDEF

    NCDF_VARPUT, wilma,timesvar, int_mons
    NCDF_VARPUT, wilma,tanomvar,stat_anoms
    NCDF_VARPUT, wilma,tabsvar,stat_abs
    NCDF_VARPUT, wilma,tadj,stat_adjs
    NCDF_VARPUT, wilma,tunc,station_err
    NCDF_VARPUT, wilma,tadjerr,stat_adjs_err
    NCDF_VARPUT, wilma,tclmerr,stat_clims_err
    NCDF_VARPUT, wilma,tobserr,stat_obs_err
    NCDF_VARPUT, wilma,tabsvar,stat_abs
    NCDF_VARPUT, wilma,tsdvar,stat_sds
    NCDF_VARPUT, wilma,tclmvar,stat_clims

    NCDF_VARPUT, wilma,climsvar,monarr

    NCDF_CLOSE,wilma

    set_plot,'PS'
    device,filename=outplots+wmo+'_anoms'+CLMlab+'_stationstats'+nowmon+nowyear+'.eps',/color,/ENCAPSUL,xsize=20,ysize=26,/portrait,/helvetica,/bold
    !P.Font =  0
    !P.Thick = 4
    !X.Thick = 4
    !Y.thick = 4
    x1pos =    0.08
    x2pos =    0.98
    y1pos =    [0.83,0.67,0.51,0.35,0.19,0.03]
    y2pos =    [0.95,0.79,0.63,0.47,0.31,0.15]
    
    tvlct,100,100,100,1
  
#  restore_colours,'shortbow'
  
    xarr =        indgen(nmons)
    zeros =       intarr(nmons)

    ymax =        max_anm*1.1
    ymin =        min_anm*1.1
    yrange =      ymax-ymin
    !P.Position = [x1pos,y1pos(0),x2pos,y2pos(0)]
    plot,xarr,stat_anoms,min_value=-100,yrange=[ymin,ymax],ystyle=1,xstyle=5,psym=-5,symsize=0.3,$
         title=wmo+' Monthly Anomalies (homogenised)',ytitle=unitees,charsize=0.9,/nodata,/noerase
    oplot,xarr,stat_anoms,min_value=-100,color=1,psym=-5,symsize=0.3,thick=4
    oplot,xarr,zeros,color=0,thick=1
    PLOTS,[xarr(0),xarr(nmons-1)],[ymin,ymin],color=0
    PLOTS,[xarr(0),xarr(nmons-1)],[ymax,ymax],color=0
    FOR yy = 1,nyrs-1 DO BEGIN
      mm = yy*12
      IF ((((yy+styr)/5.)-FIX((yy+styr)/5.)) GT 0.) THEN BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.03*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.03*yrange)],color=0
      ENDIF ELSE BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.05*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.05*yrange)],color=0    
        XYOUTS,xarr(mm),ymin-(0.12*yrange),strcompress(string(yy+styr),/remove_all),alignment=0.5,color=0,charsize=0.8
      ENDELSE
    ENDFOR

    ymax =        MAX(stat_adjs)*1.1
    ymin =        MIN(stat_adjs)*1.1
    IF (ymin EQ 0.) AND (ymax EQ 0.) THEN ymax = 1.
    yrange =      ymax-ymin  
    !P.Position = [x1pos,y1pos(1),x2pos,y2pos(1)]
    plot,xarr,stat_adjs,min_value=-100,yrange=[ymin,ymax],ystyle=1,xstyle=5,psym=-5,symsize=0.3,$
         title=' Monthly Adjustments',ytitle=unitees,charsize=0.9,/nodata,/noerase
    oplot,xarr,stat_adjs,min_value=-100,color=1,psym=-5,symsize=0.3,thick=4
    oplot,xarr,zeros,color=0,thick=1
    PLOTS,[xarr(0),xarr(nmons-1)],[ymin,ymin],color=0
    PLOTS,[xarr(0),xarr(nmons-1)],[ymax,ymax],color=0
    FOR yy = 1,nyrs-1 DO BEGIN
      mm = yy*12
      IF ((((yy+styr)/5.)-FIX((yy+styr)/5.)) GT 0.) THEN BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.03*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.03*yrange)],color=0
      ENDIF ELSE BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.05*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.05*yrange)],color=0    
        XYOUTS,xarr(mm),ymin-(0.12*yrange),strcompress(string(yy+styr),/remove_all),alignment=0.5,color=0,charsize=0.8
      ENDELSE
    ENDFOR

    ymax =        MAX(stat_adjs_err)*1.1
    ymin =        0.
    yrange =      ymax-ymin
    !P.Position = [x1pos,y1pos(2),x2pos,y2pos(2)]
    plot,xarr,stat_adjs_err,min_value=-100,yrange=[ymin,ymax],ystyle=1,xstyle=5,psym=-5,symsize=0.3,$
         title=' Monthly Adjustment Uncertainty',ytitle=unitees,charsize=0.9,/nodata,/noerase
    oplot,xarr,stat_adjs_err,min_value=-100,color=1,psym=-5,symsize=0.3,thick=4
    PLOTS,[xarr(0),xarr(nmons-1)],[ymin,ymin],color=0
    PLOTS,[xarr(0),xarr(nmons-1)],[ymax,ymax],color=0
    FOR yy = 1,nyrs-1 DO BEGIN
      mm = yy*12
      IF ((((yy+styr)/5.)-FIX((yy+styr)/5.)) GT 0.) THEN BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.03*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.03*yrange)],color=0
      ENDIF ELSE BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.05*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.05*yrange)],color=0    
        XYOUTS,xarr(mm),ymin-(0.12*yrange),strcompress(string(yy+styr),/remove_all),alignment=0.5,color=0,charsize=0.8
      ENDELSE
    ENDFOR

    ymax =        MAX(stat_obs_err)*1.1
    ymin =        0.
    yrange =      ymax-ymin  
    !P.Position = [x1pos,y1pos(3),x2pos,y2pos(3)]
    plot,xarr,stat_obs_err,min_value=-100,yrange=[ymin,ymax],ystyle=1,xstyle=5,psym=-5,symsize=0.3,$
         title=' Monthly Observation Uncertainty',ytitle=unitees,charsize=0.9,/nodata,/noerase
    oplot,xarr,stat_obs_err,min_value=-100,color=1,psym=-5,symsize=0.3,thick=4
    PLOTS,[xarr(0),xarr(nmons-1)],[ymin,ymin],color=0
    PLOTS,[xarr(0),xarr(nmons-1)],[ymax,ymax],color=0
    FOR yy = 1,nyrs-1 DO BEGIN
      mm = yy*12
      IF ((((yy+styr)/5.)-FIX((yy+styr)/5.)) GT 0.) THEN BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.03*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.03*yrange)],color=0
      ENDIF ELSE BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.05*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.05*yrange)],color=0    
        XYOUTS,xarr(mm),ymin-(0.12*yrange),strcompress(string(yy+styr),/remove_all),alignment=0.5,color=0,charsize=0.8
      ENDELSE
    ENDFOR

    ymax =        MAX(stat_clims_err)*1.1
    ymin =        0.
    yrange =      ymax-ymin
    !P.Position = [x1pos,y1pos(4),x2pos,y2pos(4)]
    plot,xarr,stat_clims_err,min_value=-100,yrange=[ymin,ymax],ystyle=1,xstyle=5,psym=-5,symsize=0.3,$
         title=' Monthly Climatology Uncertainty',ytitle=unitees,charsize=0.9,/nodata,/noerase
    oplot,xarr,stat_clims_err,min_value=-100,color=1,psym=-5,symsize=0.3,thick=4
    PLOTS,[xarr(0),xarr(nmons-1)],[ymin,ymin],color=0
    PLOTS,[xarr(0),xarr(nmons-1)],[ymax,ymax],color=0
    FOR yy = 1,nyrs-1 DO BEGIN
      mm = yy*12
      IF ((((yy+styr)/5.)-FIX((yy+styr)/5.)) GT 0.) THEN BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.03*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.03*yrange)],color=0
      ENDIF ELSE BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.05*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.05*yrange)],color=0    
        XYOUTS,xarr(mm),ymin-(0.12*yrange),strcompress(string(yy+styr),/remove_all),alignment=0.5,color=0,charsize=0.8
      ENDELSE
    ENDFOR

    ymax =        MAX(station_err)*1.1
    ymin =        0.
    yrange =      ymax-ymin
    !P.Position = [x1pos,y1pos(5),x2pos,y2pos(5)]
    plot,xarr,station_err,min_value=-100,yrange=[ymin,ymax],ystyle=1,xstyle=5,psym=-5,symsize=0.3,$
         title=' Monthly Station Uncertainty',ytitle=unitees,charsize=0.9,/nodata,/noerase
    oplot,xarr,station_err,min_value=-100,color=1,psym=-5,symsize=0.3,thick=4
    PLOTS,[xarr(0),xarr(nmons-1)],[ymin,ymin],color=0
    PLOTS,[xarr(0),xarr(nmons-1)],[ymax,ymax],color=0
    FOR yy = 1,nyrs-1 DO BEGIN
      mm = yy*12
      IF ((((yy+styr)/5.)-FIX((yy+styr)/5.)) GT 0.) THEN BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.03*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.03*yrange)],color=0
      ENDIF ELSE BEGIN
        PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.05*yrange)],color=0
        PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.05*yrange)],color=0    
        XYOUTS,xarr(mm),ymin-(0.12*yrange),strcompress(string(yy+styr),/remove_all),alignment=0.5,color=0,charsize=0.8
      ENDELSE
    ENDFOR
  
    device,/close
 # open output list for good stations
    printf,55,wmo,lat,lon,elv,cid,namoo,mush,format='(a11,x,f8.4,x,f9.4,x,f6.1,x,a2,x,a29,x,a7)'  

  ENDIF ELSE BEGIN
    openw,99,outbads,/append
    printf,99,wmo,'NO HOMOG FILE: ',countcl,format='(a11,x,a18,i2)'
    close,99
  ENDELSE

  beginagain:
  counter=counter+1
  
#  stop


ENDWHILE
close,5
close,55

stop

end


    print('And we are done!')
    
if __name__ == '__main__':
    
    main(sys.argv[1:])

#************************************************************************
    
