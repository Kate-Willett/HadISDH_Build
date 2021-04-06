#!/usr/local/sci/bin/python
# PYTHON3
# 
# Author: Kate Willett
# Created: 24 February 2014
# Last update: 17 February 2020
# Location: /home/h04/hadkw/HadISDH_Code/HADISDH_BUILD	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# This codes reads in the homogenised monthly mean data from PHA, outputs to ASCII, infilling
# hte missing years with missing data indicators (entire missing years are not printed by PHA).
# This code also plots the raw and homogenised station series alongside its raw neighbours with
# the linear trend (median pairwise) shown, for abs and anomaly annual means. 
# It can cope with PHA, IDPHA and PHADPD homogenised modes. It doresn't need to be run for IDPHA 
# though, nor is it essential to run for q, e, RH or Tw as we don't use the PHA output.
# When run for Td in PHADPD mode it creates homogenised Td from IDPHAt minus PHAdpd and outputs
# a merged log file which attempts to acumulate the changepoints appropriately.
#
# NB: In a few cases Td will not have neighbours to plot so prog will fail. Restart.
# 
# Willett et al., 2014
# Willett, K. M., Dunn, R. J. H., Thorne, P. W., Bell, S., de Podesta, M., Parker, D. E., Jones, P. D., and Williams Jr., 
# C. N.: HadISDH land surface multi-variable humidity and temperature record for climate monitoring, Clim. Past, 10, 
# 1983-2006, doi:10.5194/cp-10-1983-2014, 2014. 
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# Inbuilt:
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
#
# Kates:
# from LinearTrends import MedianPairwise - fits linear trend using median pairwise
# 
# -----------------------
# DATA
# -----------------------
# Working Dir is either:
# /data/users/hadkw/WORKING_HADISDH/UPDATE<YYYY>/
# /scratch/hadkw/UPDATE<YYYY>/ 
#
# The 40 nearest correlating neighbours from PHA   
# CORRFIL='pha52jgo/data/hadisdh/<var>/corr/corr.log'	
# The raw monthly mean station data
# INRAW='MONTHLIES/ASCII/<VAR>ABS/'
# The PHA station list to work through
# STATLIST='LISTS_DOCS/goodforHadISDH.'+versiondots+'_PHAq.txt'	
# OR the IDPHA list to work through
# STATLIST='LISTS_DOCS/goodforHadISDH.'+versiondots+'_IDPHAq.txt'	
# Homogenised monthly mean station data from PHA
# INHOM='pha52jgo/data/hadisdh/q/monthly/WMs.r00/'
# Homogenised monthly mean station data from IDPHA
# INHOM='MONTHLIES/HOMOG/IDPHAASCII/<var>DIR/'
# For Td
# IDPHA homogenised monthly mean T for creating Td
# INHOMT='MONTHLIES/HOMOG/IDPHAASCII/TDIR/'
# PHA homogenised monthly mean DPD for creating Td
# INHOMDPD='MONTHLIES/HOMOG/PHAASCII/DPDDIR/'
# Log of changepoint locations and magnitudes and uncertainties for DPD to merge with T breaks
# DPDBREAKFIL='LISTS_DOCS/HadISDH.landDPD.'+versiondots+'_PHA.log'
# Log of changepoint locations and magnitudes and uncertainties for T to merge with DPD breaks
# TBREAKFIL='LISTS_DOCS/HadISDH.landT.'+versiondots+'_IDPHAMG.log'
#
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# Set HardWire = 0 to readddddddddddddddddddddddd from the F1_HadISDHBuildConfig.txt 
# OR
# Go through everything in the 'Start' section to make sure dates, versions and filepaths are up to date
# Choose param settings for the desired variable (also in 'Start' section)
# This can take an hour or so to run through ~3800 stations so consider using screen, screen -d, screen -r

# module load scitools/default-current
# python F7_9_OutputPHAASCIIPLOT.py
#
# or 
# >F7_submit_spice.bash for t and dpd (and the rest)
# >F9_submit_spice.bash for td (derived from homog DPD and T once IDPHA for t complete
#
# NB: In a few cases Td will not have neighbours to plot so prog will fail. Restart.
# 
# -----------------------
# OUTPUT
# -----------------------
# Working Dir is either:
# /data/users/hadkw/WORKING_HADISDH/UPDATE<YYYY>/
# /scratch/hadkw/UPDATE<YYYY>/ 

# # PHA Plot showing raw and homogenised candidate vs raw neighbours with linear trends for abs and anomly monthly means
# OUTPLOT='MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/<var>DIR/'
# or if IDPHA
# OUTPLOT='IDADJCOMP/<var>DIR/'
# PHA only: Output monthly mean homogenised ASCII with missing years infilled with missing data indicator
# OUTDAT='MONTHLIES/HOMOG/PHAASCII/<var>DIR/'
# For Derived Td mode (PHADPD)
# Output log of merged T and DPD changepoints, adjustments, uncertainties that essentially went into Td (indirectly as Td is 
# created from T - DPD
# TDBREAKFIL='LISTS_DOCS/HadISDH.landTd.'+versiondots+'_PHADPD.log'
# Derived Td is stored as for IDPHA:
# OUTDAT='MONTHLIES/HOMOG/IDPHAASCII/TDDIR/'
# OUTPLOT='MONTHLIES/HOMOG/STAT_PLOTS/IDADJCOMP/TDDIR/'
#
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
# 
# Version 3 (19 January 2021)
# ---------
#  
# Enhancements
# Now runs from command line (or spice) with variables and with config file so no internal code editing required
#  
# Changes
#  
# Bug fixes
#
#


# Version 3 (17 February 2020)
# ---------
#  
# Enhancements
#  
# Changes
# Now python 3
#  
# Bug fixes
#
#
# Version 2 (25 January 2017)
# ---------
#  
# Enhancements
# General tidy up and refinement of changable variables at the beginning
# Now it should be more straight forward to set up for each year/version/variable and
# clearer to read.
#  
# Changes
#  
# Bug fixes
# I had got the RAw and HOMOG anomalies the wrong way around for the plotter so homog was red and raw was blue
# Now corrected.
#
#
# Version 1 (29 January 2016)
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
#
#************************************************************************
#                                 START
#************************************************************************
# USE python2.7
# python2.7 OutputPHAASCIIPLOT_JAN2015.py
#
# REQUIRES
# LinearTrends.py
#************************************************************************
# Set up python imports
import datetime as dt
import matplotlib
#matplotlib.use('Agg') # For spice if not set within sbatch script
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num,num2date
import sys, os, getopt
from scipy.optimize import curve_fit,fsolve,leastsq
from scipy import pi,sqrt,exp
from scipy.special import erf
import scipy.stats
from math import sqrt,pi
import struct
import pdb

from LinearTrends import MedianPairwise

# Restarter station ID
RestartValue = '-----------' # '00000099999'

# Start and end years if HardWire = 1
styear       = 1973
edyear       = 2019

# Which climatology?
clmst = 1981	# 1976, 1981
clmed = 2010	# 2005, 2010
CLMlab = str(clmst)[2:4]+str(clmed)[2:4]

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

# Note that ConfigDict is still held in memory and contains all the Global Attribute Elements for the output NetCDF File

# NOT CODED THIS FUNCTIONALITY YET
## Are we working with homogenised actuals (True) or anomalies (False)?
#Actuals = True

# Other code choices
Spin=True	#TRUE: loop through, FALSE: perform one stations only
Plotonly=False	#TRUE or FALSE
AddLetter='a)'		#'---'

# Set up directories locations
updateyy  = str(edyear)[2:4]
updateyyyy  = str(edyear)
workingdir  = '/scratch/hadkw/UPDATE'+updateyyyy
#workingdir  = '/data/users/hadkw/WORKING_HADISDH/UPDATE'+updateyyyy

# Set up filenames
INDIRLIST = workingdir+'/LISTS_DOCS/'
INDIRPHA = '/scratch/hadkw/pha52jgo/data/hadisdh/' # for corr.log and homogenised series
INDIRRAW = workingdir+'/MONTHLIES/ASCII/' 
# For Td run (PHADPD) as F9_
INHOMT = workingdir+'/MONTHLIES/HOMOG/IDPHAASCII/TDIR/'
INHOMDPD = workingdir+'/MONTHLIES/HOMOG/PHAASCII/DPDDIR/'

#workingdir  = '/scratch/hadkw/UPDATE'+updateyyyy
OUTDIRDAT_7 = workingdir+'/MONTHLIES/HOMOG/PHAASCII/' 
OUTDIRPLOT_7 = workingdir+'/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/' 
# For Td run (PHADPD) as F9_
OUTDIRDAT_9 = workingdir+'/MONTHLIES/HOMOG/IDPHAASCII/' 
OUTDIRPLOT_9 = workingdir+'/MONTHLIES/HOMOG/STAT_PLOTS/IDPHAADJCOMP/' 
# File for output stats but also for reading in missed adjustment uncertainties
OUTPUTLOG = workingdir+'/LISTS_DOCS/OutputLogFile'+versiondots+'.txt'

# Set up variables
mdi = -99.99

# Dictionaries for param, units, homogdirprefix, STATION FILE PREFIX, standard name, long name, raw data suffix(only for test run)
ParamDict = dict([('q',['q','g/kg','IDPHA','Q','specific_humidity','monthly mean 2m specific humidity','qhum']),
	          ('rh',['RH','%rh','IDPHA','RH','relative_humidity','monthly mean 2m relative humidity','rhum']),
	          ('t',['T','deg C','IDPHA','T','drybulb_temperature','monthly mean 2m dry bulb temperature','temp']), # Note this needs to be changed to IDPHAMG later
	          ('td',['Td','deg C','IDPHA','TD','dewpoint_temperature','monthly mean 2m dew point temperature','dewp']),
	          ('tw',['Tw','deg C','IDPHA','TW','wetbulb_temperature','monthly mean 2m wetbulb temperature','twet']),
	          ('e',['e','hPa','IDPHA','E','vapour_pressure','monthly mean 2m vapour pressure','evap']),
	          ('dpd',['DPD','deg C','PHA','DPD','dewpoint depression','monthly mean 2m dew point depression','ddep'])])

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
# MERGEADJUSTMENTS
def MergeAdjustments(FileInDPD, FileInT, FileOutTd, StationID, TheMCount):
    ''' Reads in PHA DPD adjustments and IDPHA T Adjustments '''
    ''' Sorts them and merges shifts on top of each other '''
    ''' Outputs DPDPHA in same format as IDPHA '''

    nBreaks      = 0	# defined after finding and reading in break locs
    BreakLocsSt  = np.reshape(0,(1))	# nBreaks list of start locations filled after reading in break locs list
    BreakLocsEd  = np.reshape(0,(1))	# nBreaks list of end locations filled after reading in break locs list
    BreakSize    = np.reshape(0.,(1))	# nBreaks list of sizes filled after reading in break locs list
    BreakUncs    = np.reshape(0.,(1))	# nBreaks list of uncertainties filled after reading in break locs list
    BreakSources = np.reshape('x',(1))	# nBreaks list of uncertainties filled after reading in break locs list
    BreakList    = np.zeros((1,4))	# Build this on the fly to equal nBreaks(rows) by rel(adj,unc),act(adj,unc) including last HSP which will be zero	
    MyBreakLocs  = []	# nBreaks+2 month locations for each break including month 1 if needed and last month

    # read in the PHA log for DPD
    BreakSize,BreakLocsSt,BreakLocsEd,BreakSources,BreakUncs,nBreaks=PHAReadSimple(FileInDPD,StationID,BreakSize,BreakLocsSt,
                                                                                 BreakLocsEd,BreakSources,BreakUncs,nBreaks,
										 TheMCount)
     
    # read in the IDPHA log for T
    BreakSize,BreakLocsSt,BreakLocsEd,BreakSources,BreakUncs,nBreaks=IDPHAReadSimple(FileInT,StationID,BreakSize,BreakLocsSt,
                                                                                 BreakLocsEd,BreakSources,BreakUncs,nBreaks,
										   TheMCount)
   
    # sort and combine
    BreakLocsSt,BreakLocsEd,BreakList,BreakSources,nBreaks=SortBreaksMerge(BreakLocsSt,BreakSize,BreakUncs,
                                                                           BreakList,BreakSources,nBreaks,TheMCount)
        
    # write out to file
    LogBreakInfoMerge(FileOutTd,StationID,nBreaks,TheMCount,BreakLocsSt,BreakList,BreakSources)

    return # MergeAdjustments

#************************************************************************
# PHAREADSIMPLE
def PHAReadSimple(FileName,StationID, all_adjust, all_starts, all_ends, all_sources, all_uncs, breakcount,TheMCount):
    '''
    Read in PHA results from Adjwrite.txt

    StationIDs - list of station IDs
    all_adjust - list of adjustment magnitudes
    all_starts - list of adjustment date starts
    all_ends - list of adjustment date ends
    all_sources - list of adjustment source (DPD) in this case

    '''
    
    for line in open(FileName):
        if "Adj write:"+StationID in line:
            print(line)
            moo        = str.split(line)
            tempstring = moo[12]
            tempunc    = tempstring[0:4]
            if breakcount == 0:
		### can use np.delete(array,row/column/pointers,axis)###
		
                all_starts[0]  = int(moo[4])
                all_ends[0]    = TheMCount
                all_adjust[0]  = float(moo[11])
                if float(tempunc) > 0. :
                    all_uncs[0] = float(tempunc)	# convert 1.65 sigma to 1 sigma
                else:
                    all_uncs[0] = 0.
                all_sources[0] = 'dd'
                breakcount     = breakcount+1 
            else:
                all_starts     = np.append(all_starts,int(moo[4]))
                all_ends       = np.append(all_ends,int(moo[7]))		#int(moo[4]))
                all_adjust     = np.append(all_adjust,float(moo[11]))		# positive adjustments to dewpoint t
                if float(tempunc) > 0.:
                    all_uncs = np.append(all_uncs,float(tempunc))
                else:
                    all_uncs = np.append(all_uncs,0.)
		     
                all_sources    = np.append(all_sources,'dd')
                breakcount     = breakcount+1        
    
    all_starts[len(all_starts)-1] = 1	#start at 1 because ID will (no intro extra CP)    

    return all_adjust, all_starts, all_ends, all_sources, all_uncs, breakcount # PHAReadSimple

#************************************************************************
# IDPHAREAD
def IDPHAReadSimple(FileName,StationID, all_adjust, all_starts, all_ends, all_sources, all_uncs, breakcount,TheMCount):
    '''
    Read in PHA results from Adjwrite.txt

    StationIDs - list of station IDs (wmo+wban)
    all_adjust - list of adjustment magnitudes
    all_starts - list of adjustment date starts
    all_ends - list of adjustment date ends
    all_sources - list of adjustment source (DPD) in this case

    '''
    
    for line in open(FileName):
        if StationID in line:
            print(line)
            moo = str.split(line)
            if breakcount == 0:
		### can use np.delete(array,row/column/pointers,axis)###
		
                all_starts[0]  = int(moo[2])
                all_ends[0]    = TheMCount
                all_adjust[0]  = -(float(moo[6]))		# negative adjustments to dewpoint t
                if float(moo[7]) > 0. :
                    all_uncs[0] = float(moo[7])	# convert 1.65 sigma to 1 sigma
                else:
                    all_uncs[0] = 0.
                all_sources[0] = 't'
                breakcount     = breakcount+1 
            else:
                all_starts     = np.append(all_starts,int(moo[2]))
                all_ends       = np.append(all_ends,int(moo[3]))		#int(moo[4]))
                all_adjust     = np.append(all_adjust,-(float(moo[6])))		# negative adjustments to dewpoint t
                if float(moo[7]) > 0.:
                    all_uncs = np.append(all_uncs,float(moo[7]))
                else:
                    all_uncs = np.append(all_uncs,0.)
		     
                all_sources    = np.append(all_sources,'t')
                breakcount     = breakcount+1        

    return all_adjust, all_starts, all_ends, all_sources, all_uncs, breakcount # IDPHAReadSimple

#************************************************************************
# SORTBREAKSMERGE
def SortBreaksMerge(TheStarts,TheAdjs,TheUncs,TheBreakList,TheSources,TheBCount,TheMCount):
    ''' Looks at list of potential from T and DPD '''
    ''' Sorts them from 1 to 480 (or total) months '''
    ''' Merges duplicates and those within 12 months of a preceding break '''
    ''' Merges accumulated adjustment and uncertainty '''
    ''' resets nBreaks appropriately  '''
    ''' IF DPD inc and T stays the same, Td should dec and vice versa '''
    ''' IF T inc and DPD stays the same, Td should inc and vice versa '''
    ''' IF DPD inc and T inc, Td should stay about the same and vice versa '''
    ''' IF DPD inc and T dec, Td should decrease and vice versa '''
    ''' THIS WILL NOT ALWAYS WORK OUT PERFECTLY BUT ITS OWNLY FOR UNCERTAINTY ESTIMATION '''	
    
    SortedInd  = np.argsort(TheStarts)	# sorts the list BreakLocs indexing from 0
    TheStarts  = TheStarts[SortedInd]		
    TheAdjs    = TheAdjs[SortedInd]		
    TheUncs    = TheUncs[SortedInd]		
    TheSources = TheSources[SortedInd]	
    print(TheStarts)
 
    LastBreakLocSt = TheStarts[0]
    NewStarts      = np.reshape(TheStarts[0],(1))
    NewAdjs        = np.reshape(TheAdjs[0],(1))
    NewUncs        = np.reshape(TheUncs[0],(1))
    NewSources     = np.reshape(TheSources[0],(1))
    derr = 0.
    terr = 0.
    dadj = 0.
    tadj = 0.
    if TheSources[0] =='t' : 
        terr = TheUncs[0]
        tadj = TheAdjs[0]
    else:
        derr = TheUncs[0]
        dadj = TheAdjs[0]
    
    realcounter=0
    for bb in range(1,TheBCount):
        if TheSources[bb] =='t' : 
            terr = TheUncs[bb]
            tadj = TheAdjs[bb]
        else:
            derr = TheUncs[bb]
            dadj = TheAdjs[bb]
        if TheStarts[bb]-LastBreakLocSt > 11:	    # keep it if its at least a year apart from any other break
            NewStarts      = np.append(NewStarts,TheStarts[bb])
            NewAdjs        = np.append(NewAdjs,tadj+dadj)
            NewUncs        = np.append(NewUncs,np.sqrt((terr**2) + (derr**2)))
            NewSources     = np.append(NewSources,TheSources[bb])
            LastBreakLocSt = TheStarts[bb]
            realcount      = realcounter+1
        else:
            NewAdjs[realcounter-1]    = tadj+dadj
            NewUncs[realcounter-1]    = np.sqrt((terr**2) + (derr**2))
            NewSources[realcounter-1] = 'b'

    TheBCount = len(NewStarts)

    # reverse all of the arrays, sort out ends and independent adjustment/uncertainties
    NewStarts    = NewStarts[::-1]       	
    NewAdjs      = NewAdjs[::-1]       	
    NewUncs      = NewUncs[::-1]       	
    NewSources   = NewSources[::-1]    
    NewEnds      = np.empty_like(NewStarts)
    NewEnds[0]   = TheMCount   	
    TheBreakList = np.zeros((TheBCount,4))	# Build this on the fly to equal nBreaks(rows) by rel(adj,unc),act(adj,unc) including last HSP which will be zero	
    for bb in range(1,TheBCount):
        NewEnds[bb]        = (NewStarts[bb-1])-1
        TheBreakList[bb,0] = NewAdjs[bb]-NewAdjs[bb-1]		# this is this funny range thing again needs +1
        TheBreakList[bb,1] = np.sqrt((NewUncs[bb]**2)-(NewUncs[bb-1]**2))
        TheBreakList[bb,2] = NewAdjs[bb]		# minus or not minus?
        TheBreakList[bb,3] = NewUncs[bb]

    print(TheBCount,NewStarts)
       
    return NewStarts,NewEnds,TheBreakList,NewSources,TheBCount #SortBreaksMerge

#************************************************************************
# LOGBREAKINFOMERGE
def LogBreakInfoMerge(TheFile,TheStationID,TheBCount,TheMonthCount,TheBreakLocsSt,TheBreakList,TheSources):
    ''' Print out a list of breaks found with their location, size and uncertainty '''
    ''' Append to file '''
    ''' IN ALL CASES ADJUSTMENTS ARE -(adj) TO MATCH PHA OUTPUT '''
    ''' IF THE DATA HAVE BEEN ADJUSTED DOWN THEN THE ADJUSTMENT GIVEN IS POSITIVE - WEIRD '''

    filee = open(TheFile,'a+')

    if TheBCount == 1:
        filee.write('%11s %2s %3i %3i %6.2f %6.2f %6.2f %6.2f \n' % (TheStationID,1,1,
	           TheMonthCount,TheBreakList[0,0],TheBreakList[0,1],TheBreakList[0,2],TheBreakList[0,3]))
    else:
        LocEnd=TheMonthCount
	# Force first location of TheBreakLocs to be 0 instead of 1 so that a single line of code works
        for b in range(0,TheBCount):
            print(TheBCount,b)
            # sign swapping of adjustments for consistency with PHA logs
            filee.write('%11s %2s %3i %3i %6.2f %6.2f %6.2f %6.2f %2s\n' % (TheStationID,TheBCount-b,TheBreakLocsSt[b],
                    LocEnd,-(TheBreakList[b,0]),TheBreakList[b,1],-(TheBreakList[b,2]),TheBreakList[b,3],TheSources[b]))
            LocEnd = (TheBreakLocsSt[b]-1)

    filee.close()

    return #LogBreakInfoMerge

#************************************************************************
# FINDNEIGHBOURS
def FindNeighbours(FileName,CandID,neighbourcount,neighbourlist):
    ''' open the corr file and find the line beginning with the candidate station '''
    ''' list all neighbouring stations up to 40'''
    ''' be sure not to count 0s'''
    ''' return neighbour count and neighbour list '''

    for line in open(FileName):
        neighbourlist = []			# make sure its blank to start
        neighbourlist = str.split(line)		# makes a list
        if neighbourlist[0] == CandID:	# found the line
            neighbourcount = len(neighbourlist)		# this doesn't include the zeros but does include the candidate in the count.
            break				# don't waste time, exit the loop

    return neighbourcount,neighbourlist # FindNeighbours
  
#************************************************************************
# READINNETWORKS
def ReadInNetworks(TheCount,TheList,TheCStation,TheFilebitA,TheFilebitB,TheYears,TheData):
    ''' Loop through all neighbour station raw files '''
    ''' IGNORE FIRST FILE AS THIS IS THE CANDIDATE STATION '''
    ''' DOUBLE CHECK ALL OTHER STATIONS ARE NOT CANDIDATE AS THIS IS A KNOWN PROBLEM '''
    ''' read in using ReadStations and add to array '''    

    TheNewCount = 0	# setting up new variables to output
    TheNewList  = []
    TheData     = np.array(TheData)	# was an empty list

    for n,TheNStation in enumerate(TheList[1:]):	# 1: starts at second element
        if TheNStation == TheCStation:
            continue
	    
        TheFile       = TheFilebitA+TheNStation[0:6]+'-'+TheNStation[6:11]+TheFilebitB
        TempStation   = []
        TheTypes      = np.append("|S12",["int"]*13)
        TheDelimiters = np.append([12,4,6],[9]*11)
        RawData       = ReadData(TheFile,TheTypes,TheDelimiters)

        for yy in TheYears:
            moo = list(RawData[yy])
            if yy == 0: 
                TempStation = moo[2:14] 
            else:
                TempStation = np.append(TempStation,moo[2:14])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element
  
        if TheData.size:		# if empty array then use first element, otherwise append
            TheData = np.append(TheData,np.reshape(TempStation/100.,(1,len(TempStation))),axis=0)	# now in proper units, fill the Neighbour array
        else:
            TheData = np.reshape(TempStation/100.,(1,len(TempStation)))

        if any(TheNewList):		# if empty array then use first element, otherwise append
            TheNewList = np.append(TheNewList,TheNStation)
        else:
            TheNewList = [TheNStation]
    
    TheNewCount = len(TheNewList)		# Now this only includes the neighbours and not the candidate, as in FingNeighbours

    return TheData,TheNewList,TheNewCount #ReadInNetworks 	

#************************************************************************
# MAKEANOMALIES
def MakeAnomalies(TheData,TheAnomalies,TheClims,TheYCount,TheStClim,TheEdClim,TheMDI):
    ''' Working on both 1D and 2D (multiple station) arrays '''
    ''' Use given climatology period to create monthly clims and anomalies '''
    
    sizoo        = TheData.shape			# returns a tuple of rows,columns
    TheClims     = np.empty((sizoo[0],12))	# initialise clims array for nstations (rows) by 12 months (columns)
    TheClims.fill(TheMDI)
    TheAnomalies = np.empty(sizoo)
    TheAnomalies.fill(TheMDI)

    for t,TempStation in enumerate(TheData):	# row by row so ok as long as each station is a row

        #print(t,len(TempStation))
        Mooch  = np.reshape(TempStation,(TheYCount,12))	# years(rows) by months(columns)
        Mooch2 = np.empty_like(Mooch)		# To make sure I don't overwrite the absolute data
        Mooch2.fill(TheMDI)

        for mm in range(12):
	    
            subarr = Mooch[TheStClim:TheEdClim+1,mm]
            #print(mm,subarr)
            gots   = (subarr > TheMDI)

            if len(subarr[gots]) >= 15:		# more sophisticated checking has been done previously 
                TheClims[t,mm]   = np.mean(subarr[gots])
                gots2            = (Mooch[:,mm] > TheMDI)
                Mooch2[gots2,mm] = Mooch[gots2,mm]-TheClims[t,mm]
                #print " %6.2f"*40 % tuple(Mooch[:,mm])

        TheAnomalies[t,] = np.reshape(Mooch2,(1,12*TheYCount))    

    return TheAnomalies,TheClims #MakeAnomalies

#************************************************************************
# WRITEOUT
def WriteOut(TheData,TheFile,TheYears,TheStYr,TheStationID):
    ''' Use numpy array to reform to years by months (row/column)'''
    ''' Output lines to text of StationID, space, year, 12 months of data*100 (i6,x)'''

    TheData = np.reshape(TheData,(-1,12))	# an nyears by 12 months array 

    for outt in TheYears:

        for mm in range(12):

            if mm == 0:  
                moo = [np.char.mod("%6i",int(TheData[outt,mm]*100.))," "]
            else:
                moo = moo+[np.char.mod("%6i",int(TheData[outt,mm]*100.))," "]  # list of silly months with spaces between

        if outt == 0:
            goo = [TheStationID," ",TheYears[outt]+TheStYr]+moo
        else:
            goo = np.vstack((goo,[TheStationID," ",TheYears[outt]+TheStYr]+moo))

# NEED TO MAKE A 2D STRING ARRAY - seems very long winded to me!
    
    np.savetxt(TheFile,goo,fmt='%s',delimiter='')

    return #WriteOut

#************************************************************************
# PLOTHOMOGTS
def PlotHomogTS(TheFile,TheStation,TheNeighbours,TheHStation,TheNCount,TheMDI,TheStYr,TheYCount,unit,vartypee,Letteree):
    ''' Plot raw candidate and neighbours with homogenised candidate '''
    ''' Add medianpairwise trends - from code medianpairwise.py '''
    '''MAKE MEDIANPAIRWISE.PY and COMPLETE WHEN HOMOG SERIES IS DONE '''
 
    # create annual averages and years and titles
    TheStationAnn  = np.empty(TheYCount)
    TheStationAnn.fill(TheMDI)
    TheHStationAnn = np.empty(TheYCount)
    TheHStationAnn.fill(TheMDI)
    
    if TheNCount > 1:
        TheNeighboursAnn = np.empty((len(TheNeighbours[:,0]),TheYCount))
        TheNeighboursAnn.fill(TheMDI)

    TheStation = np.reshape(TheStation,(TheYCount,12))
    TheHStation = np.reshape(TheHStation,(TheYCount,12))    
    
    for yy in range(TheYCount):
        if np.sum(TheStation[yy,] != TheMDI) >= 9:
            TheStationAnn[yy] = np.mean(TheStation[yy,np.where(TheStation[yy,] != TheMDI)])
        if np.sum(TheHStation[yy,] != TheMDI) >= 9:
            TheHStationAnn[yy] = np.mean(TheHStation[yy,np.where(TheHStation[yy,] != TheMDI)])
 
    TheStation  = np.reshape(TheStation,(TheYCount*12))
    TheHStation = np.reshape(TheHStation,(TheYCount*12))    
   
    if TheNCount > 1:
        for n,Neighbour in enumerate(TheNeighbours):
            Neighbour = np.reshape(Neighbour,(TheYCount,12))
            for yy in range(TheYCount):
                if np.sum(Neighbour[yy,] != TheMDI) >= 9:
                    TheNeighboursAnn[n,yy] = np.mean(Neighbour[yy,np.where(Neighbour[yy,] != TheMDI)])
        
    
    TheYears = np.reshape(range(TheStYr,TheStYr+TheYCount),TheYCount)
    ytitlee  = vartypee+' ('+unit+')'
    xtitlee  = 'Years'
    
    # get decadal trends and 5th-9th conf
    rawtrend = [0.,0.,0.]
    homtrend = [0.,0.,0.]
    rawtrend = MedianPairwise(TheStationAnn,TheMDI,rawtrend)
    homtrend = MedianPairwise(TheHStationAnn,TheMDI,homtrend)
        
    # set up plot
 
    plt.clf()
#    exit()
# CODE FAILING HERE WITH SPICE EVEN THOUGH RUNNING WITH AGG - THOUGHT IT MIGHT BE TO DO WITH WORKING WITHIOUT AN OBJECT
# Its to do with 'agg' - I tried to set this from the sbatch script but it didn't work so is now hard coded here.
    fig = plt.figure(1,figsize=(8,4))
    plt.axes([0.12,0.12,0.85,0.80])
    if TheNCount > 1:
        PileItUp = np.append(TheNeighboursAnn,np.append(np.reshape(TheStationAnn,(1,TheYCount)),
             np.reshape(TheHStationAnn,(1,TheYCount)),axis=0),axis=0)
    else:
        PileItUp = np.append(np.reshape(TheStationAnn,(1,TheYCount)),
             np.reshape(TheHStationAnn,(1,TheYCount)),axis=0)
    
    plt.ylim([np.floor(min(PileItUp[PileItUp != TheMDI]))-2,
              np.ceil(max(PileItUp[PileItUp != TheMDI]))+2])
    plt.xlim([TheStYr,TheStYr+TheYCount])
    plt.tick_params(axis='both', which='major', labelsize=14)
   
    if TheNCount > 1:
        for n,Neighbour in enumerate(TheNeighboursAnn):
            line, = plt.plot(TheYears[np.where(Neighbour > TheMDI)],Neighbour[np.where(Neighbour > TheMDI)],color='black',linewidth=0.25)
 	
    line, = plt.plot(TheYears[np.where(TheStationAnn > TheMDI)],TheStationAnn[np.where(TheStationAnn > TheMDI)],'r',linewidth=2)	
    line, = plt.plot(TheYears[np.where(TheHStationAnn > TheMDI)],TheHStationAnn[np.where(TheHStationAnn > TheMDI)],'b',linewidth=2)
    if vartypee=='anomalies':
        line, = plt.plot(np.append(TheYears,TheStYr+TheYCount+1),np.zeros(TheYCount+1),'black',linewidth=1)        	
    
    plt.xlabel(xtitlee,size=14)
    plt.ylabel(ytitlee,size=14)
    
#    watermarkstring="/".join(os.getcwd().split('/')[4:])+'/'+os.path.basename( __file__ )+"   "+dt.datetime.strftime(dt.datetime.now(), "%d-%b-%Y %H:%M")
#    plt.figtext(0.01,0.01,watermarkstring,size=6)
    
    rawstr = "%5.2f +/- %5.2f to %5.2f %s /decade " % (rawtrend[0]*10,rawtrend[1]*10,rawtrend[2]*10,unit)
    homstr = "%5.2f +/- %5.2f to %5.2f %s /decade " % (homtrend[0]*10,homtrend[1]*10,homtrend[2]*10,unit)

    plt.figtext(0.13,0.84,rawstr,color='r',size=16)
    plt.figtext(0.13,0.78,homstr,color='b',size=16)
    if Letteree != '---':
       plt.figtext(0.05,0.95,Letteree,color='Black',size=18)
       
    #plt.show()
    plt.savefig(TheFile+".eps")
    plt.savefig(TheFile+".png")
     
    return #PlotHomogTS

#***********************************************************************
# MAIN PROGRAM
#***********************************************************************
def main(argv):

    # INPUT PARAMETERS AS STRINGS!!!!
    var = 'q'	    # 'q','rh','e','td','tw','t','dpd'
    typee = 'PHA' # 'PHA','IDPHA','PHADPD'
    runtype = 'all' # 'all','000000'

    try:
        opts, args = getopt.getopt(argv, "hi:",
	                           ["var=","typee=","runtype="])
    except getopt.GetoptError:
        print('Usage (as strings) F7_9_OutputPHAASCIIPLOT.py --var <q> --typee <IDPHA> --runtype <all>')
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
    
    # Set up initial run choices
    styr = int(styear)
    edyr = int(edyear)
    clmsty = (clmst-styr)
    clmedy = (clmed-styr)
    clmstm = (clmst-styr)*12
    clmedm = ((clmed-styr)*12)+11
    nmons = ((edyr+1)-styr)*12
    nyrs = (edyr-styr)+1
    yrarr = range(nyrs)

    # Set up file paths for var
    STATSUFFIXIN = '_'+ParamDict[var][0]+'monthQCabs.raw'
    STATSUFFIXOUT = '_PHAadj.txt'
 
    STATLIST = INDIRLIST+'goodforHadISDH.'+versiondots+'_'+typee+var+'.txt'
    CORRFIL = INDIRPHA+var+'/corr/corr.log'
    INRAW = INDIRRAW+ParamDict[var][3]+'ABS/'
    INHOM = INDIRPHA+var+'/monthly/WMs.r00/'
    
    OUTDIRDAT = OUTDIRDAT_7
    OUTDIRPLOT = OUTDIRPLOT_7
    # If we're running as F9_ for Td PHA DPD then special case
    if (var == 'td') & (typee == 'PHADPD'):
    
        OUTDIRDAT = OUTDIRDAT_9
        OUTDIRPLOT = OUTDIRPLOT_9	    
        DPDBREAKFIL  = workingdir+'/LISTS_DOCS/HadISDH.landDPD.'+versiondots+'_PHA.log'
        TBREAKFIL    = workingdir+'/LISTS_DOCS/HadISDH.landT.'+versiondots+'_IDPHAMG.log'
        TDBREAKFIL   = workingdir+'/LISTS_DOCS/HadISDH.landTd.'+versiondots+'_PHADPD.log'

    # if we're running as F7_ for Td PHA then need to use derivedTD for raw
    if (var == 'td') & (typee == 'PHA'):
        INRAW = INDIRRAW+'derivedTDABS/'
        STATSUFFIXIN = '_deTdmonthQCabs.raw'

    OUTDAT = OUTDIRDAT+ParamDict[var][3]+'DIR/'
    OUTPLOT = OUTDIRPLOT+ParamDict[var][3]+'DIR/'

#***************************************************
# read in station list
#**************************************************
    MyTypes          = ("|U6","|U5","float","float","float","|U4","|U30","|U7","int")
    #MyTypes          = ("|S6","|S5","float","float","float","|S4","|S30","|S7","int")
    MyDelimiters     = [6,5,8,10,7,4,30,7,5]
    RawData          = ReadData(STATLIST,MyTypes,MyDelimiters)
    StationListWMO   = np.array(RawData['f0'])
    StationListWBAN  = np.array(RawData['f1'])
    StationListLat   = np.array(RawData['f2'])
    StationListLon   = np.array(RawData['f3'])
    StationListElev  = np.array(RawData['f4'])
    StationListCID   = np.array(RawData['f5'])
    StationListName  = np.array(RawData['f6'])
    nstations        = len(StationListWMO)

#************************************************
# loop through station by station
#**********************************************    
    for st in range(nstations):

        # check if restart necessary
        if RestartID != '-----------' and RestartID != StationListWMO[st]+StationListWBAN[st]:
            continue

        RestartID = '-----------'

    # set up clean arrays and variables
        nNstations    = 0	# defined after reading corr station list
        NeighbourList = [] # nNstations list filled after reading in corr station list

        MyStation       = np.zeros((nyrs,12))	# filled after reading in candidate station
        MyStation[:,:]  = (-9999)
        MyTStation      = []
        MyDPDStation    = []
        MyRAWStation    = []
        MyClims         = []	# 12 element array of mean months 1981-2010
        MyAnomalies     = [] # filled with anomalies after subtracting climatology
        MyHomogAnoms    = [] # filled with homogenised anomalies
        MyHomogAbs      = []  # filled with climatology+homogenised anomalies
        MyClimMeanShift = [] # flat value across complete climatology period that the homogenised values differ from zero by - to rezero anoms and adjust clims/abs

        NeighbourStations      = []	# nNstations by nmons array filled after reading in all neighbour stations
        NeighbourAnomsStations = []	# nNstations by nmons array filled after anomalising all neighbour stations relative to climatology
        NeighbourClimsStations = []	# nNstations by nmons array filled after anomalising all neighbour stations relative to climatology
        NeighbourDiffStations  = []	# nNstations by nmons array filled after creating candidate minus neighbour difference series

#***************************************************
# read in the RAW station file
#***************************************************
        MyFile = INRAW+StationListWMO[st]+"-"+StationListWBAN[st]+STATSUFFIXIN  
        MyTypes = np.append("|S12",["int"]*13) # Does this still work? '|U'?
        MyDelimiters = np.append([12,4,6],[9]*11)
        RawData = ReadData(MyFile,MyTypes,MyDelimiters)
        for yy in yrarr:
            moo = list(RawData[yy])
            if yy == 0: 
                MyRAWStation = moo[2:14] 
            else:
                MyRAWStation = np.append(MyRAWStation,moo[2:14])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element

        print(st,MyFile)  
        
        MyRAWStation = np.reshape(MyRAWStation/100.,(1,nmons))	# now in proper units and an array not list

#*************************************
# read in the PHA HOMOGENISED station file
#*************************************
        if typee == 'PHA':
            MyFile = INHOM+StationListWMO[st]+StationListWBAN[st]+".WMs.r00.tavg"  
            MyTypes = np.append(["|S16","|S6"],["|S9"]*11)
            MyDelimiters = np.append([16,6],[9]*11)
            RawData = ReadData(MyFile,MyTypes,MyDelimiters)
            for yy in range(0,len(RawData)):
                # get the year
                moo = list(RawData[yy])
                mystring = moo[0]
                ypoint = int(mystring[12:16])-styr
                # get the non'd' bits of the strings
                newmoo = [int(a[-5:]) for a in moo[1:13]]
#	    print("NEWMOO",newmoo)
                MyStation[ypoint] = newmoo

            print(st,MyFile)  
            MyStation = np.reshape(MyStation/100.,(1,nmons))	# now in proper units and an array not list
    
        elif typee == 'PHADPD':
            MyFile = INHOMT+StationListWMO[st]+StationListWBAN[st]+'_IDPHAadj.txt'
            MyTypes = np.append("|S16",["int"]*12)
            MyDelimiters = np.append([16,6],[7]*11)
            RawData = ReadData(MyFile,MyTypes,MyDelimiters)
            for yy in yrarr:
                moo = list(RawData[yy])
                if yy == 0: 
                    MyTStation = moo[1:13] 
                else:
                    MyTStation = np.append(MyTStation,moo[1:13])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element
            print(st,MyFile)    
            MyTStation = np.reshape(MyTStation/100.,(1,nmons))	# now in proper units and an array not list
        
            MyFile = INHOMDPD+StationListWMO[st]+StationListWBAN[st]+'_PHAadj.txt'
            MyTypes = np.append("|S16",["int"]*12)
            MyDelimiters = np.append([16,6],[7]*11)
            RawData = ReadData(MyFile,MyTypes,MyDelimiters)
            for yy in yrarr:
                moo = list(RawData[yy])
                if yy == 0: 
                    MyDPDStation = moo[1:13] 
                else:
                    MyDPDStation = np.append(MyDPDStation,moo[1:13])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element
            print(st,MyFile)  
  
            MyDPDStation = np.reshape(MyDPDStation/100.,(1,nmons))	# now in proper units and an array not list
	
	    # create Td from T-DPD where data exist
            MyStation = np.empty_like(MyTStation)
            MyStation[:,:] = (-99.99)
            for mm in range(len(MyStation[0,:])):
                if MyTStation[0,mm] > mdi and MyDPDStation[0,mm] > mdi: 
                    MyStation[0,mm] = MyTStation[0,mm]-MyDPDStation[0,mm]
	    # ALSO FAFF AROND READING IN ADJUSTMENT FILES AND MERGING
            MergeAdjustments(DPDBREAKFIL,TBREAKFIL,TDBREAKFIL,StationListWMO[st]+StationListWBAN[st],nmons)
                
#*******************************************
# Find the neighbours that were used to homogenise
#*******************************************************
        nNstations,NeighbourList = FindNeighbours(CORRFIL,StationListWMO[st]+StationListWBAN[st],nNstations,
                                 NeighbourList)
        print("No. of Neighbours: ",nNstations-1)	# not including candidate but may have duplicate

#**********************************************
# read in the neighbour files - if insufficient then list in bad stations list
#*********************************************
        if nNstations > 1:

            NeighbourStations,NeighbourList,nNstations=ReadInNetworks(nNstations,NeighbourList,
	                                           StationListWMO[st]+StationListWBAN[st],INRAW,
						   STATSUFFIXIN,yrarr,NeighbourStations)
            print("Actual No. of Neighbours: ",nNstations)	# not including candidate but may have duplicate

#*********************************************
# convert all to anomalies (storing station climatology)
#************************************************

        MyAnomalies,MyClims = MakeAnomalies(MyRAWStation,MyAnomalies,MyClims,nyrs,clmsty,clmedy,mdi)
        MyHomogAnoms,MyClims = MakeAnomalies(MyStation,MyHomogAnoms,MyClims,nyrs,clmsty,clmedy,mdi)
	
        NeighbourAnomsStations,NeighbourClimsStations = MakeAnomalies(NeighbourStations,NeighbourAnomsStations,
	                                              NeighbourClimsStations,nyrs,clmsty,clmedy,mdi)
        
#**************************************************
# Make comparison plot
#**************************************************
    # PLOT CANDIDATE AND NEIGHBOURS UNHOMOG WITH HOMOG ON TOP - ABS, ANOMS with MedianPairwiseTrends
    # REZEROD HOMOG MAY MEAN ITS NOW OFFSET COMPARED TO ORIGINAL
        MyPlotFile = OUTPLOT+StationListWMO[st]+StationListWBAN[st]+'_trendcomp_'+var+'_abs'
        PlotHomogTS(MyPlotFile,MyRAWStation,NeighbourStations,MyStation,nNstations,mdi,styr,nyrs,ParamDict[var][1],'absolutes',AddLetter)
        MyPlotFile = OUTPLOT+StationListWMO[st]+StationListWBAN[st]+'_trendcomp_'+var+'_anoms'
        PlotHomogTS(MyPlotFile,MyAnomalies,NeighbourAnomsStations,MyHomogAnoms,nNstations,mdi,styr,nyrs,ParamDict[var][1],'anomalies',AddLetter)

#**************************************************
# print out homogenised station anomalies
#*************************************************
        if (not Plotonly):
            MyFileOut = OUTDAT+StationListWMO[st]+StationListWBAN[st]+STATSUFFIXOUT  
            WriteOut(MyStation,MyFileOut,yrarr,styr,StationListWMO[st]+StationListWBAN[st])
        if (not Spin):
            break
            # end loop of stations

#    pdb.set_trace()

    filee = open(OUTPUTLOG,'a+')
    filee.write('%s%s%s%s\n' % (var,'_OutputPHA_',typee,'=DONE'))
    filee.close()
    
    print('And we are done!')
    
if __name__ == '__main__':
    
    main(sys.argv[1:])

#************************************************************************
