#!/usr/local/sci/bin/python

#***************************************
# 11 October 2013 KMW - v1
# Indirect homogenisation of RH and Tw using breakpoints found in T and Td
# Indirect homogenisation of e and q using breakpoints found in Td
# Works on monthly mean values from HadISD  
# 
# 1. Establish where to source breaks Td or Td and T
# 2. Find all break locations and homogeneous subperiods
# 3. Read in station, find the neighbour network, read in all neighbours, make anomalies, make
#    difference series for each pair
# 4. Loop through breaks
#	4.1 Get difference in medians between homogeneous subperiods for each
#           difference series
#       4.2 Get the mean, 1 st dev of differences
#       4.3 If +/- 1SD are both of the same sign then GOOD (establish criteria)
#       4.4 Apply mean adjustment, record alongside 1SD
# 5. record accumulative adjustments and uncertainties
# 6. add back climatology, save adjusted station to file 
# 
# 24 January 2014
# Apply IDPHA to T using DPD changepoints
# USE DPD changepoints instead of TD
# Apply both T and DPD to all variables because:
#	in most cases T will have been involved in calculation from original source
#	DPD does not contain changepoints that co-occur in T and Td
# Cope with new 2.0.0.2013p file structure
# 
#
#************************************************************************
#                                 START
#************************************************************************
# USE python2.7
# python2.7 IndirectPHA_JAN2015.py
#
# REQUIRES
# LinearTrends.py
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

from LinearTrends import MedianPairwise

# RESTART VALUE
Restarter='------'				#'------'		#'681040'

# Set up initial run choices
param='tw'	# tw, q, e, rh, t
param2='Tw'	# Tw, q, e, RH, T
unit='deg C'	# 'deg C','g/kg','hPa','%'
nowmon='JAN'
nowyear='2015'
version='2.0.1.2014p'

# Set up file locations
STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAall_'+nowmon+nowyear+'.txt'	# removed all 'bad' DPD and T stations (6)

# Break locations are taken from pha output
TBREAKFIL='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landT.'+version+'_PHA_JAN2015.log'
DPDBREAKFIL='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landDPD.'+version+'_PHA_JAN2015.log'

STATSUFFIXOUT='_IDPHAadj.txt'

if param == 'rh':
    CORRFIL='/data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/PHA_2014/pha_v52i/data/hadisdh/hadisdh7314r/corr/corr.hadisdh7314r.tavg.r00.1502071231'
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/ASCII/RHABS/'
    STATSUFFIXIN='_RHmonthQCabs.raw'
    OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHAASCII/RHDIR/'
    BREAKSINFO='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landRH.'+version+'_IDPHA_'+nowmon+nowyear+'.log'
    NONEIGHBOURSLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/noneighbours_landRH.'+version+'_IDPHA_'+nowmon+nowyear+'.txt'
    GOTNEIGHBOURSLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHArh_'+nowmon+nowyear+'.txt'
    OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/STAT_PLOTS/IDADJCOMP/RHDIR/'

elif param == 'q':
    CORRFIL='/data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/PHA_2014/pha_v52i/data/hadisdh/hadisdh7314q/corr/corr.hadisdh7314q.tavg.r00.1502071125' 
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/ASCII/QABS/'
    STATSUFFIXIN='_qmonthQCabs.raw'
    OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHAASCII/QDIR/'
    BREAKSINFO='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landq.'+version+'_IDPHA_'+nowmon+nowyear+'.log'
    NONEIGHBOURSLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/noneighbours_landq.'+version+'_IDPHA_'+nowmon+nowyear+'.txt'
    GOTNEIGHBOURSLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAq_'+nowmon+nowyear+'.txt'
    OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/STAT_PLOTS/IDADJCOMP/QDIR/'

elif param == 'tw':
    CORRFIL='/data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/PHA_2014/pha_v52i/data/hadisdh/hadisdh7314w/corr/corr.hadisdh7314w.tavg.r00.1502071306'
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/ASCII/TWABS/'
    STATSUFFIXIN='_TwmonthQCabs.raw'
    OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHAASCII/TWDIR/'
    BREAKSINFO='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landTw.'+version+'_IDPHA_'+nowmon+nowyear+'.log'
    NONEIGHBOURSLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/noneighbours_landTw.'+version+'_IDPHA_'+nowmon+nowyear+'.txt'
    GOTNEIGHBOURSLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAtw_'+nowmon+nowyear+'.txt'
    OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/STAT_PLOTS/IDADJCOMP/TWDIR/'

elif param == 'e':
    CORRFIL='/data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/PHA_2014/pha_v52i/data/hadisdh/hadisdh7314e/corr/corr.hadisdh7314e.tavg.r00.1502071159'
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/ASCII/EABS/'
    STATSUFFIXIN='_emonthQCabs.raw'
    OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHAASCII/EDIR/'
    BREAKSINFO='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.lande.'+version+'_IDPHA_'+nowmon+nowyear+'.log'
    NONEIGHBOURSLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/noneighbours_lande.'+version+'_IDPHA_'+nowmon+nowyear+'.txt'
    GOTNEIGHBOURSLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAe_'+nowmon+nowyear+'.txt'
    OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/STAT_PLOTS/IDADJCOMP/EDIR/'

elif param == 't':
    CORRFIL='/data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/PHA_2014/pha_v52i/data/hadisdh/hadisdh7314t/corr/corr.hadisdh7314t.tavg.r00.1502071016' 
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/ASCII/TABS/'	# a different file name and format to read in
    INPHA='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/PHAASCII/TDIR/'	# a different file name and format to read in
    STATSUFFIXIN='_TmonthQCabs.raw'
    OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHAASCII/TDIR/'
    BREAKSINFO='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landT.'+version+'_IDPHA_'+nowmon+nowyear+'.log'
    BREAKSINFOMERGE='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landT.'+version+'_IDPHAMG_'+nowmon+nowyear+'.log'
    NONEIGHBOURSLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/noneighbours_landT.'+version+'_IDPHA_'+nowmon+nowyear+'.txt'
    GOTNEIGHBOURSLIST='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAt_'+nowmon+nowyear+'.txt'
    OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/STAT_PLOTS/IDADJCOMP/TDIR/'

# Set up variables and arrays needed

mdi=-99.99

styr=1973
edyr=2014
DATASTART=dt.datetime(styr,1,1,0,0)
DATAEND=dt.datetime(edyr,12,1,0,0)
clmst=1976
clmed=2005
clmsty=(clmst-styr)
clmedy=(clmed-styr)
clmstm=(clmst-styr)*12
clmedm=((clmed-styr)*12)+11
CLIMSTART=dt.datetime(clmst,1,1,0,0)
CLIMEND=dt.datetime(clmed,12,1,0,0)
nmons=((edyr+1)-styr)*12
monarr=range(nmons)
nyrs=(edyr-styr)+1
yrarr=range(nyrs)

nstations=0	# defined after reading in station list
StationListWMO=[]	# nstations list filled after reading in station list
StationListWBAN=[]	# nstations list filled after reading in station list

nNstations=0	# defined after reading corr station list
NeighbourList=[] # nNstations list filled after reading in corr station list

nBreaks=0	# defined after finding and reading in break locs
BreakLocs=[]	# nBreaks list of locations filled after reading in break locs list
BreakSize=[]	# nBreaks list of sizes filled after reading in break locs list
BreakUncs=[]	# nBreaks list of uncertainties filled after reading in break locs list
NewBreakDist=[]	# filled each time a break size is found from all neighbour difference series
NewBreakList=[]	# nBreaks by 4 array for mean adjustment relative to next most recent HSP, 1.65sigma unc, total adjustment relative to most recent HSP, total 1.65sigma unc
MyBreakLocs=[]      # nBreaks+2 month locations for each break including month 1 if needed and last month

MyStation=[]	# filled after reading in candidate station
MyClims=[]	# 12 element array of mean months 1976-2005
MyAnomalies=[]	# filled with anomalies after subtracting climatology
MyHomogAnoms=[] # filled with homogenised anomalies
MyHomogAbs=[]	# filled with climatology+homogenised anomalies
MyClimMeanShift=[] # flat value across complete climatology period that the homogenised values differ from zero by - to rezero anoms and adjust clims/abs

NeighbourStations=[]	# nNstations by nmons array filled after reading in all neighbour stations
NeighbourAnomsStations=[]	# nNstations by nmons array filled after anomalising all neighbour stations relative to climatology
NeighbourClimsStations=[]	# nNstations by nmons array filled after anomalising all neighbour stations relative to climatology
NeighbourDiffStations=[]	# nNstations by nmons array filled after creating candidate minus neighbour difference series

MyFile=' '	#string containing file name

#************************************************************************
# Subroutines
#************************************************************************
# READDATA
def ReadData(FileName,typee,delimee):
    ''' Use numpy genfromtxt reading to read in all rows from a complex array '''
    ''' Need to specify format as it is complex '''
    ''' outputs an array of tuples that in turn need to be subscripted by their names defaults f0...f8 '''
    return np.genfromtxt(FileName, dtype=typee,delimiter=delimee) # ReadData

#************************************************************************
# PHAREAD
def PHARead(FileName,StationID, all_adjust, all_starts, all_uncs, breakcount,TheMCount):
    '''
    Read in PHA results from Adjwrite.txt

    StationIDs - list of station IDs
    all_adjust - list of adjustment magnitudes
    all_starts - list of adjustment dates taken from END points in T and Td
    if first end point read in is not equal to total months in complete record (i.e. 480 for 1973-2012)
    then force it to equal total number of months - this is the most recent HSP
    '''
    
    all_firsts=np.reshape(0,(1))	# in function array to temporarily store start points of HSPs as opposed to the endpoints which are the break locs.
    infunccount=0	# in function counter so that if T and Td are considered there is still sensitivity to end of records.
    for line in open(FileName):
        if "Adj write:"+StationID in line:
	    print(line)
            moo=str.split(line)
            if breakcount == 0:
		# This is the first line read in so should be the last data present point but data may have been removed
		# - force end point to be nmonths IF it is not == nmonths and within 24 months of nmonths - just the end of data present as 
		# no changepoints can occurr within 2 years of end of record
		# - add end point of nmonths IF it is not == nmonths and more than 24 months earlier - could be data removed or
		# could be end of data, if end of data it won't matter as MDI will prevent any adjustment.
		# Only problem with adding extra end point is that an extra break will be counted, with zero adjustment.
		# Can try and remove this later in assign breaks?
		
		### ADD ALL FIRSTS!!! ###
		### SORT OUT ASSIGN AND APPLY SO THEY WORK ###
		### can use np.delete(array,row/column/pointers,axis)###
		
                if TheMCount-int(moo[7]) > 24:
		    all_firsts[0]=int(moo[7])+1
		    all_firsts=np.append(all_firsts,int(moo[4]))
		    all_starts[0]=TheMCount
		    all_starts=np.append(all_starts,int(moo[7]))
		    all_adjust[0]=0.0
		    all_adjust=np.append(all_adjust,moo[11])
		    all_uncs[0]=0.0
		    all_uncs=np.append(all_uncs,moo[12])
		    breakcount=breakcount+2
		    infunccount=infunccount+2
		elif TheMCount-int(moo[7]) <= 24:		    
		    all_firsts[0]=int(moo[4])
		    all_starts[0]=TheMCount
		    all_adjust[0]=moo[11]
                    all_uncs[0]=moo[12]
		    breakcount=breakcount+1
		    infunccount=infunccount+1
 
	    elif breakcount != 0 and infunccount == 0:
                if TheMCount-int(moo[7]) > 24:
		    all_firsts=np.append(all_firsts,(int(moo[7])+1,int(moo[4])))
		    all_starts=np.append(all_starts,(TheMCount,int(moo[7])))
		    all_adjust=np.append(all_adjust,(0.0,moo[11]))
		    all_uncs=np.append(all_uncs,(0.0,moo[12]))
		    breakcount=breakcount+2
		    infunccount=infunccount+2
		elif TheMCount-int(moo[7]) <= 24:		    
		    all_firsts=np.append(all_firsts,int(moo[4]))
                    all_starts=np.append(all_starts,TheMCount)		
                    all_adjust=np.append(all_adjust,moo[11])
                    all_uncs=np.append(all_uncs,moo[12])
                    breakcount=breakcount+1
		    infunccount=infunccount+1
		# This is the first line of a new variable (i.e., T after doing Td)	    	

            else:
		all_firsts=np.append(all_firsts,int(moo[4]))
                all_starts=np.append(all_starts,int(moo[7]))		#int(moo[4]))
                all_adjust=np.append(all_adjust,moo[11])
                all_uncs=np.append(all_uncs,moo[12])
                breakcount=breakcount+1
		infunccount=infunccount+1

    # Test the start point of the last element added - if it is not 1 then add 1 in case some data has been removed.
    if all_firsts[infunccount-1] > 24:
        all_starts=np.append(all_starts,all_firsts[infunccount-1]-1)		#int(moo[4]))
        all_adjust=np.append(all_adjust,0.0)
        all_uncs=np.append(all_uncs,0.0)
        breakcount=breakcount+1
        

    if breakcount == 1:	# then there are no breaks so reset everything to zero so 
        breakcount=0	# it doesn't double count with second iteration for RH and Tw
     
    return all_adjust, all_starts, all_uncs, breakcount # PHARead

#************************************************************************
# FINDNEIGHBOURS
def FindNeighbours(FileName,CandID,neighbourcount,neighbourlist):
    ''' open the corr file and find the line beginning with the candidate station '''
    ''' list all neighbouring stations up to 40'''
    ''' be sure not to count 0s'''
    ''' return neighbour count and neighbour list '''
    for line in open(FileName):
        neighbourlist=[]			# make sure its blank to start
        neighbourlist=str.split(line)		# makes a list
        if neighbourlist[0] == CandID:	# found the line
            neighbourcount=len(neighbourlist)		# this doesn't include the zeros but does include the candidate in the count.
            break				# don't waste time, exit the loop

    return neighbourcount,neighbourlist # FindNeighbours
  
#************************************************************************
# READINNETWORKS
def ReadInNetworks(TheCount,TheList,TheCStation,TheFilebitA,TheFilebitB,TheYears,TheData):
    ''' Loop through all neighbour station raw files '''
    ''' IGNORE FIRST FILE AS THIS IS THE CANDIDATE STATION '''
    ''' DOUBLE CHECK ALL OTHER STATIONS ARE NOT CANDIDATE AS THIS IS A KNOWN PROBLEM '''
    ''' read in using ReadStations and add to array '''    
    TheNewCount=0	# setting up new variables to output
    TheNewList=[]
    TheData=np.array(TheData)	# was an empty list
    for n,TheNStation in enumerate(TheList[1:]):	# 1: starts at second element
	if TheNStation == TheCStation:
	    continue
	    
        TheFile=TheFilebitA+TheNStation[0:6]+'-'+TheNStation[6:11]+TheFilebitB
        
	TempStation=[]
        TheTypes=np.append("|S12",["int"]*13)
        TheDelimiters=np.append([12,4,6],[9]*11)
        RawData=ReadData(TheFile,TheTypes,TheDelimiters)
        for yy in TheYears:
            moo=list(RawData[yy])
            if yy == 0: 
                TempStation=moo[2:14] 
            else:
                TempStation=np.append(TempStation,moo[2:14])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element
  
        if TheData.size:		# if empty array then use first element, otherwise append
	    TheData=np.append(TheData,np.reshape(TempStation/100.,(1,len(TempStation))),axis=0)	# now in proper units, fill the Neighbour array
	else:
	    TheData=np.reshape(TempStation/100.,(1,len(TempStation)))
        if any(TheNewList):		# if empty array then use first element, otherwise append
	    TheNewList=np.append(TheNewList,TheNStation)
	else:
	    TheNewList=[TheNStation]
    
    TheNewCount=len(TheNewList)		# Now this only includes the neighbours and not the candidate, as in FingNeighbours
    return TheData,TheNewList,TheNewCount #ReadInNetworks 	

#************************************************************************
# MAKEANOMALIES
def MakeAnomalies(TheData,TheAnomalies,TheClims,TheYCount,TheStClim,TheEdClim,TheMDI):
    ''' Working on both 1D and 2D (multiple station) arrays '''
    ''' Use given climatology period to create monthly clims and anomalies '''
    
    sizoo=TheData.shape			# returns a tuple of rows,columns
    TheClims=np.empty((sizoo[0],12))	# initialise clims array for nstations (rows) by 12 months (columns)
    TheClims.fill(TheMDI)
    TheAnomalies=np.empty(sizoo)
    TheAnomalies.fill(TheMDI)
    for t,TempStation in enumerate(TheData):	# row by row so ok as long as each station is a row
        #print(t,len(TempStation))
	Mooch=np.reshape(TempStation,(TheYCount,12))	# years(rows) by months(columns)
	Mooch2=np.empty_like(Mooch)		# To make sure I don't overwrite the absolute data
	Mooch2.fill(TheMDI)
	for mm in range(12):
	    subarr=Mooch[TheStClim:TheEdClim+1,mm]
	    #print(mm,subarr)
	    gots=(subarr > TheMDI)
	    if len(subarr[gots]) >= 15:		# more sophisticated checking has been done previously 
	        TheClims[t,mm]=np.mean(subarr[gots])
		gots2=(Mooch[:,mm] > TheMDI)
	        Mooch2[gots2,mm]=Mooch[gots2,mm]-TheClims[t,mm]
		#print " %6.2f"*40 % tuple(Mooch[:,mm])
	TheAnomalies[t,]=np.reshape(Mooch2,(1,12*TheYCount))    
    return TheAnomalies,TheClims #MakeAnomalies

#************************************************************************
# MAKEDIFFSERIES
def MakeDiffSeries(TheCandidate,TheNeighbours,TheDiffSeries,TheMDI,TheMCount):
    ''' Go through all neighbour anomaly series and subtract from candidate '''
    
    TheDiffSeries=np.empty_like(TheNeighbours)	# set up difference series array
    TheDiffSeries.fill(TheMDI)
    TheCandidate=np.reshape(TheCandidate,(len(TheCandidate[0,]),))
#    gotsC=TheCandidate > TheMDI		#True where values not MDI
#    print(gotsC)
    for t,TempStation in enumerate(TheNeighbours):
        for mm in range(0,TheMCount):
	    if TheCandidate[mm] > TheMDI and TempStation[mm] > TheMDI:
	        TheDiffSeries[t,mm]=TheCandidate[mm]-TempStation[mm]
	
#	gotsN=TempStation > TheMDI
#        subsample=np.where(gotsC == gotsN)
#	if len(subsample) > 0:		# check there are data present
#	    TheDiffSeries[t,subsample]=TheCandidate[subsample]-TempStation[subsample]
##	    print " %5.2f"*len(TheDiffSeries[t,]) % tuple(TheDiffSeries[t,])
    
    return TheDiffSeries #MakeDiffSeries

#************************************************************************
# SORTBREAKS
def SortBreaks(TheBreakLocs,TheActualBreakLocs,TheBCount,TheMCount):
    ''' Looks at list of potential breaks from T and Td '''
    ''' Sorts them from 1 to 480 (or total) months '''
    ''' Removes duplicates and those within 12 months of a preceding break '''
    ''' resets nBreaks appropriately and also assigns BreakLocs to 1st and last month '''
    TheBreakLocs.sort()		# sorts the list BreakLocs
    print(TheBreakLocs)

    TheActualBreakLocs=[1,TheBreakLocs[0]]	    # first break location should never be 1st month so no if/else needed here
    LastBreakLoc=TheBreakLocs[0]

    #if TheBreakLocs[0] != 1:
    #	TheActualBreakLocs=[1,TheBreakLocs[0]]	    # this is our first breaklocation, hopefully not silly close to 1st month
    #    LastBreakLoc=TheBreakLocs[0]
    #else:
    #	TheActualBreakLocs=TheBreakLocs[0]		
    #    LastBreakLoc=TheBreakLocs[0]

    for bb in range(1,TheBCount):
   	if TheBreakLocs[bb]-LastBreakLoc > 11:	    # keep it if its at least a year apart from any other break
    	    TheActualBreakLocs=np.append(TheActualBreakLocs,TheBreakLocs[bb])
    	    LastBreakLoc=TheBreakLocs[bb]

# I've added an artificial break location at 1 so that is an extra break
# therefore TheBCount should be len(TheActualBreakLocs)-1 and as the last
# one is always the last month there does not need to be an added last month+1
#    TheBCount=len(TheActualBreakLocs)
#    TheActualBreakLocs=np.append(TheActualBreakLocs,TheMCount+1)      # given the last time point plus one to work with for loop 

    TheBCount=len(TheActualBreakLocs)-1

    print(TheBCount,TheActualBreakLocs)
       
    return TheBreakLocs,TheActualBreakLocs,TheBCount #SortBreaks

#************************************************************************
# ASSIGNJUMPSIZEUNC
def AssignJumpSizeUnc(TheBreakList,TheBCount,TheActualBreakLocs,TheBreakDist,TheNeighbourDiffs,TheMDI):
    ''' Loop through each HSP '''
    ''' Call DetectJumpSizes to find size of adjustment in each difference series '''
    ''' Find the median and the mean of the 50th - 5th and 95th - 50th percentiles = ~1.65 sigma uncertainty/90% '''
    ''' 5th and 95th percentiles are not symmetric around the median hence slight fudge above '''
    ''' fill TheBreakList with relative (to next most recent HSP) adjustment and uncertainty '''
    ''' Loop through each break and calculate total change of HSP to most recent HSP and total uncertainty SQRT(sum(alluncs**2)) '''
    ''' There need to be at least 7 neighbour diffs to robustly estimate the adjustment '''
    ''' IF THERE ARE INSUFFICIENT NEIGHBOURS PRESENT FOR THE PERIOD (INCLUDING IF CANDIDATE IS MISSING) THEN ALLOCATE TheMDI 
        TO THE BREAKLIST - THIS WILL LATER BE TRANSLATED TO NO BREAK '''
    TheBreakList=np.zeros((1,4))	# Build this on the fly to equal nBreaks(rows) by rel(adj,unc),act(adj,unc) including last HSP which will be zero	
    TheModifiedBreakLocs=[1]	# build on the fly - there will always be a 1 and 480 though - add 480 at the end
    
    breakpointer=1	# local variable to deal with pointing when breaks are removed
    for bb in range(1,TheBCount):	# range(1,2) = [1] - therefore last element always stays as zero
	# set up the HSP pointers for each pair of HSPs
	HSP_1=range((TheActualBreakLocs[bb-1]-1),TheActualBreakLocs[bb])   # no minus 1 as indexing starts from a and moves to b-1              
	#HSP_2=range((TheActualBreakLocs[bb]-1),(TheActualBreakLocs[bb+1]-1)) 
	# HSP_2 should not include endpoint from HSP_1 - correction below
	# HSP_2 should not include start point from next HSP and no extra Nmonths+1 is then needed to make this work - Bcount already one fewer
	HSP_2=range(TheActualBreakLocs[bb],TheActualBreakLocs[bb+1]) # -1 as indexing starts from 0
	
#	print("HSP POINTS: ",TheActualBreakLocs[bb-1]-1,TheActualBreakLocs[bb],TheActualBreakLocs[bb],TheActualBreakLocs[bb+1])
 	    
        TheBreakDist=[]
	TheBreakDist=DetectJumpSizes(HSP_1,HSP_2,TheNeighbourDiffs,TheBreakDist,TheMDI)
	#print " %5.2f"*len(NewBreakDist) % tuple(NewBreakDist)

	if len(TheBreakDist[np.where(abs(TheBreakDist) > 0.)]) > 0:	# THERE MUST BE AT LEAST 1 DIFF SERIES WITH DATA OR NO GO
	    print " %5.2f"*len(TheBreakDist[np.where(abs(TheBreakDist) > 0.)]) % tuple(TheBreakDist[np.where(abs(TheBreakDist) > 0.)])
	    print "PERCENTILES %5.2f %5.2f %5.2f %5.2f %5.2f " % tuple(np.percentile(TheBreakDist[np.where(abs(TheBreakDist) > 0.)],(5,25,50,75,95)))

	    TheBreakList=np.append(TheBreakList,np.zeros((1,4)),0)	# always add another row on the fly - first row remains zeros
	    TheBreakList[breakpointer-1,0]=(np.median(TheBreakDist[np.where(abs(TheBreakDist) > 0.)]))	# actual adj to next HSP 
	    TheBreakList[breakpointer-1,1]=np.mean(((np.median(TheBreakDist[np.where(abs(TheBreakDist) > 0.)]) - np.percentile(TheBreakDist[np.where(abs(TheBreakDist) > 0.)],5)),
		                              (np.percentile(TheBreakDist[np.where(abs(TheBreakDist) > 0.)],95) - np.median(TheBreakDist[np.where(abs(TheBreakDist) > 0.)]))))	#
	    print "MEDIAN AND 1.65SIGMA ",TheBreakList[breakpointer-1,0:2]
	    TheModifiedBreakLocs=np.append(TheModifiedBreakLocs,TheActualBreakLocs[bb])
	    breakpointer=breakpointer+1
        
	# IF there are no difference series then the candidate does not have data present for at least one of the HSPs
	# IF this is the first or last changepoint then it is most likely that we have added this to account for PHA_direct removed data
	# Therefore it is desireable to remove this changepoint from all relevant arrays. 
	# This has been done by building TheBreakList and TheModifiedBreakLocs on the fly only with Breaks that have adjustments
	# TheBCount is then changed to be the number of rows in the resulting TheBreakList

	
# after all breaks assessed reset TheBCount in case any brekas have been removed.
    TheModifiedBreakLocs=np.append(TheModifiedBreakLocs,TheActualBreakLocs[TheBCount])	#utilises the old TheBCount - should set nMonths
    TheBCount=len(TheBreakList[:,0])
    
    print(TheBCount,TheModifiedBreakLocs)
    	
# after all breaks assessed relatively calculated total adjustment and uncertainty
    for bb in range(0,TheBCount-1):
	 TheBreakList[bb,2]=sum(TheBreakList[bb:TheBCount-1,0])
	 TheBreakList[bb,3]=np.sqrt(sum(TheBreakList[bb:TheBCount-1,1]**2))

# plot histogram with median and 5th/95th percentiles to see if its sensible

    return TheBreakList,TheBCount,TheModifiedBreakLocs #ASSIGNJUMPSIZEUNC

#************************************************************************
# DETECTJUMPSIZES
def DetectJumpSizes(TheHSP_1,TheHSP_2,TheNeighbourDiffs,TheBreakDist,TheMDI):
    ''' Go through each difference series and calculate median of HSPs if there are at least 12 months of data '''
    ''' Store difference in medians before and after BreakLoc '''
    sizoo=TheNeighbourDiffs.shape
    TheBreakDist=np.zeros(sizoo[0])
    for d,Diff in enumerate(TheNeighbourDiffs):
        period1=Diff[TheHSP_1]
	period2=Diff[TheHSP_2]
	gots1=period1 > TheMDI
	gots2=period2 > TheMDI
#	print gots1
#	print gots2
        if sum(gots1) > 11 and sum(gots2) > 11:	# there are data present in both samples
	    TheBreakDist[d]=np.median(period2[gots2])-np.median(period1[gots1])
#	print TheBreakDist[d]    
    return TheBreakDist #DetectJumpSizes

#************************************************************************
# APPLYJUMPSREZERO
def ApplyJumpsReZero(TheAnomalies,TheHomogAnoms,TheBreakList,TheBCount,TheActualBreakLocs,TheStClim,TheEdClim,TheMDI,TheMean):
    ''' use the total adjustments calculated earlier to adjust the months in the candidate anomalies '''
    ''' rezero the homogenised anomaly series so that it still has a mean of zero '''
    ''' Save this time series mean over the climatology period so that it can be applied to climatology too - as a flat value '''
    ''' Also rezero the raw anomaly series so that it will be easy to compare where the shifts are on the plot'''
    AdjustmentFactor=np.zeros_like(TheAnomalies)
    TheHomogAnoms=np.zeros_like(TheAnomalies)
    TheHomogAnoms.fill(TheMDI)
    
    for bb in range(1,TheBCount):
	HSP=range((TheActualBreakLocs[bb-1]-1),TheActualBreakLocs[bb])   # does not need minus 1 as range starts from a and moves to b-1              
        AdjustmentFactor[0,HSP]=np.repeat(TheBreakList[bb-1,2],len(HSP))	# the total adjustment for that HSP   

    TheHomogAnoms[np.where(TheAnomalies > TheMDI)]=TheAnomalies[np.where(TheAnomalies > TheMDI)]+AdjustmentFactor[np.where(TheAnomalies > TheMDI)] 
    
    climpoints=range(clmstm,clmedm+1)	# range(0,9) only goes from 0 to 8 so need a,b+1
    # ADD IN NP.ARRAY TO MAKE SURE NOTHING ODD HAPPENING?
    Selection=TheHomogAnoms[0,climpoints]
    TheMean=np.mean(Selection[np.where(Selection > TheMDI)])
    TheHomogAnoms[np.where(TheHomogAnoms > TheMDI)]=TheHomogAnoms[np.where(TheHomogAnoms > TheMDI)]-TheMean
    TheAnomalies[np.where(TheAnomalies > TheMDI)]=TheAnomalies[np.where(TheAnomalies > TheMDI)]-TheMean  
    
    return TheAnomalies,TheHomogAnoms,TheMean #APPLYJUMPSREZERO

#************************************************************************
# MAKEABS
def MakeAbs(TheHomogAnoms,TheHomogAbs,TheClims,TheMDI,TheYCount,TheMean):
    ''' Add back the monthly climatology to each anomaly '''
    TheHomogAbs=np.empty_like(TheHomogAnoms)
    TheHomogAbs.fill(TheMDI)
    TheHomogAbs=np.reshape(TheHomogAbs,(TheYCount,12))
    TheHomogAnoms=np.reshape(TheHomogAnoms,(TheYCount,12))
    for mm in range(12):
        if TheClims[0,mm] > TheMDI:
	    TheHomogAbs[np.where(TheHomogAnoms[:,mm] > TheMDI),mm]=TheHomogAnoms[np.where(TheHomogAnoms[:,mm] > TheMDI),mm]+TheClims[0,mm]+TheMean
    
    TheHomogAbs=np.reshape(TheHomogAbs,(1,TheYCount*12))
    TheHomogAnoms=np.reshape(TheHomogAnoms,(1,TheYCount*12))
    
    return TheHomogAbs #MAKEABS

#************************************************************************
# WRITEOUT
def WriteOut(TheData,TheFile,TheYears,TheStYr,TheStationID):
    ''' Use numpy array to reform to years by months (row/column)'''
    ''' Output lines to text of StationID, space, year, 12 months of data*100 (i6,x)'''
    TheData=np.reshape(TheData,(-1,12))	# an nyears by 12 months array 

    for outt in TheYears:
        for mm in range(12):
	    if mm == 0:  
	        moo=[np.char.mod("%6i",int(TheData[outt,mm]*100.))," "]
	    else:
	        moo=moo+[np.char.mod("%6i",int(TheData[outt,mm]*100.))," "]  # list of silly months with spaces between
	if outt == 0:
	    goo=[TheStationID," ",TheYears[outt]+TheStYr]+moo
	else:
	    goo=np.vstack((goo,[TheStationID," ",TheYears[outt]+TheStYr]+moo))

# NEED TO MAKE A 2D STRING ARRAY - seems very long winded to me!
    
    np.savetxt(TheFile,goo,fmt='%s',delimiter='')
    return #WriteOut

#************************************************************************
# LOGBREAKINFO
def LogBreakInfo(TheFile,TheStationID,TheBCount,TheMonthCount,TheBreakLocs,TheBreakList):
    ''' Print out a list of breaks found with their location, size and uncertainty '''
    ''' Append to file '''
    ''' IN ALL CASES ADJUSTMENTS ARE -(adj) TO MATCH PHA OUTPUT '''
    ''' IF THE DATA HAVE BEEN ADJUSTED DOWN THEN THE ADJUSTMENT GIVEN IS POSITIVE - WEIRD '''
    filee=open(TheFile,'a+')
    if TheBCount == 1:
        filee.write('%11s %2s %3i %3i %6.2f %6.2f %6.2f %6.2f \n' % (TheStationID,1,1,
	           TheMonthCount,-(TheBreakList[0,0]),TheBreakList[0,1],-(TheBreakList[0,2]),TheBreakList[0,3]))
    else:
        LocEnd=TheMonthCount
	# Force first location of TheBreakLocs to be 0 instead of 1 so that a single line of code works
	TheBreakLocs[0]=0
	for b,brev in enumerate(range(TheBCount,0,-1)):
	    print(TheBCount,b,brev)
            filee.write('%11s %2s %3i %3i %6.2f %6.2f %6.2f %6.2f \n' % (TheStationID,brev,TheBreakLocs[brev-1]+1,
	            LocEnd,-(TheBreakList[brev-1,0]),TheBreakList[brev-1,1],-(TheBreakList[brev-1,2]),TheBreakList[brev-1,3]))
            LocEnd=(TheBreakLocs[brev-1])
    filee.close()
    return #LogBreakInfo

#************************************************************************
# PLOTHOMOGTS
def PlotHomogTS(TheFile,TheStation,TheNeighbours,TheHStation,TheMDI,TheStYr,TheYCount,unit,typee):
    ''' Plot raw candidate and neighbours with homogenised candidate '''
    ''' Add medianpairwise trends - from code medianpairwise.py '''
    '''MAKE MEDIANPAIRWISE.PY and COMPLETE WHEN HOMOG SERIES IS DONE '''
 
    # create annual averages and years and titles
    TheStationAnn=np.empty(TheYCount)
    TheStationAnn.fill(TheMDI)
    TheHStationAnn=np.empty(TheYCount)
    TheHStationAnn.fill(TheMDI)
    TheNeighboursAnn=np.empty((len(TheNeighbours[:,0]),TheYCount))
    TheNeighboursAnn.fill(TheMDI)

    TheStation=np.reshape(TheStation,(TheYCount,12))
    TheHStation=np.reshape(TheHStation,(TheYCount,12))    
    
    for yy in range(TheYCount):
        if np.sum(TheStation[yy,] != TheMDI) >= 9:
	    TheStationAnn[yy]=np.mean(TheStation[yy,np.where(TheStation[yy,] != TheMDI)])
        if np.sum(TheHStation[yy,] != TheMDI) >= 9:
	    TheHStationAnn[yy]=np.mean(TheHStation[yy,np.where(TheHStation[yy,] != TheMDI)])
 
    TheStation=np.reshape(TheStation,(TheYCount*12))
    TheHStation=np.reshape(TheHStation,(TheYCount*12))    
   
    for n,Neighbour in enumerate(TheNeighbours):
        Neighbour=np.reshape(Neighbour,(TheYCount,12))
        for yy in range(TheYCount):
            if np.sum(Neighbour[yy,] != TheMDI) >= 9:
	        TheNeighboursAnn[n,yy]=np.mean(Neighbour[yy,np.where(Neighbour[yy,] != TheMDI)])
        
    
    TheYears=np.reshape(range(TheStYr,TheStYr+TheYCount),TheYCount)
    ytitlee=typee+' ('+unit+')'
    xtitlee='Years'
    
    # get decadal trends and 5th-9th conf
    rawtrend=[0.,0.,0.]
    homtrend=[0.,0.,0.]
    rawtrend=MedianPairwise(TheStationAnn,TheMDI,rawtrend)
    homtrend=MedianPairwise(TheHStationAnn,TheMDI,homtrend)
        
    # set up plot
 
    plt.clf()
    plt.figure(1,figsize=(8,4))
    plt.axes([0.1,0.1,0.85,0.80])
    PileItUp=np.append(TheNeighboursAnn,np.append(np.reshape(TheStationAnn,(1,TheYCount)),
             np.reshape(TheHStationAnn,(1,TheYCount)),axis=0),axis=0)
    plt.ylim([np.floor(min(PileItUp[PileItUp != TheMDI]))-2,
              np.ceil(max(PileItUp[PileItUp != TheMDI]))+2])
    plt.xlim([TheStYr,TheStYr+TheYCount])
   
    for n,Neighbour in enumerate(TheNeighboursAnn):
        line,=plt.plot(TheYears[np.where(Neighbour > TheMDI)],Neighbour[np.where(Neighbour > TheMDI)],color='black',linewidth=0.25)
 	
    line,=plt.plot(TheYears[np.where(TheStationAnn > TheMDI)],TheStationAnn[np.where(TheStationAnn > TheMDI)],'r',linewidth=2)	
    line,=plt.plot(TheYears[np.where(TheHStationAnn > TheMDI)],TheHStationAnn[np.where(TheHStationAnn > TheMDI)],'b',linewidth=2)
    if typee=='anomalies':
        line,=plt.plot(np.append(TheYears,TheStYr+TheYCount+1),np.zeros(TheYCount+1),'black',linewidth=1)        	
    
    plt.xlabel(xtitlee)
    plt.ylabel(ytitlee)
    
    watermarkstring="/".join(os.getcwd().split('/')[4:])+'/'+os.path.basename( __file__ )+"   "+dt.datetime.strftime(dt.datetime.now(), "%d-%b-%Y %H:%M")
    plt.figtext(0.01,0.01,watermarkstring,size=6)
    
    rawstr="%5.2f +/- %5.2f to %5.2f %s /decade " % (rawtrend[0]*10,rawtrend[1]*10,rawtrend[2]*10,unit)
    homstr="%5.2f +/- %5.2f to %5.2f %s /decade " % (homtrend[0]*10,homtrend[1]*10,homtrend[2]*10,unit)

    plt.figtext(0.1,0.86,rawstr,color='r')
    plt.figtext(0.1,0.82,homstr,color='b')

    #plt.show()
    plt.savefig(TheFile+".eps")
    plt.savefig(TheFile+".png")
     
    return #PlotHomogTS

#***********************************************************************
# LISTSTATION
def ListStation(TheFile,TheStationID,TheLat,TheLon,TheElev,TheCID,TheName,TheCount):
    ''' Write out the station WMO and WBAN and Location to file   '''
    ''' File is either list of good stations or bad stations '''
    ''' Bad stations are cases where there are fewer than 7 neighbours '''
    ''' This is based on listings compiled for this variable during direct PHA '''
    ''' First difference series of the monthly anomalies must correlate > 0.1 '''
    filee=open(TheFile,'a+')
    filee.write('%11s%8.4f%10.4f%7.1f%4s%29s%4i \n' % (TheStationID,TheLat,TheLon,
                TheElev,TheCID,TheName,TheCount))
    filee.close()

    return #ListNoNeighbours
#***********************************************************************
# MERGEADJUSTMENTS
def MergeAdjustments(FileInDPD, FileInT, FileOutTd, StationID, TheMCount):
    ''' Reads in PHA DPD adjustments and IDPHA T Adjustments '''
    ''' Sorts them and merges shifts on top of each other '''
    ''' Outputs DPDPHA in same format as IDPHA '''

    nBreaks=0	# defined after finding and reading in break locs
    BreakLocsSt=np.reshape(0,(1))	# nBreaks list of start locations filled after reading in break locs list
    BreakLocsEd=np.reshape(0,(1))	# nBreaks list of end locations filled after reading in break locs list
    BreakSize=np.reshape(0.,(1))	# nBreaks list of sizes filled after reading in break locs list
    BreakUncs=np.reshape(0.,(1))	# nBreaks list of uncertainties filled after reading in break locs list
    BreakSources=np.reshape('x',(1))	# nBreaks list of uncertainties filled after reading in break locs list
    BreakList=np.zeros((1,4))	# Build this on the fly to equal nBreaks(rows) by rel(adj,unc),act(adj,unc) including last HSP which will be zero	
    MyBreakLocs=[]	# nBreaks+2 month locations for each break including month 1 if needed and last month

    # read in the PHA log for T
    BreakSize,BreakLocsSt,BreakLocsEd,BreakSources,BreakUncs,nBreaks=PHAReadSimple(FileInDPD,StationID,BreakSize,BreakLocsSt,
                                                                                 BreakLocsEd,BreakSources,BreakUncs,nBreaks,
										 TheMCount)
     
    # read in the IDPHA log for T
    BreakSize,BreakLocsSt,BreakLocsEd,BreakSources,BreakUncs,nBreaks=IDPHAReadSimple(FileInT,StationID,BreakSize,BreakLocsSt,
                                                                                 BreakLocsEd,BreakSources,BreakUncs,nBreaks,
										   TheMCount)
   
    # sort and combine
    BreakLocsSt,BreakLocsEd,BreakList,BreakSources,nBreaks=SortBreaksMerge(BreakLocsSt,BreakSize,BreakUncs,
                                                                           BreakList,BreakSources,nBreaks,nmons)
    
    
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
            moo=str.split(line)
	    tempstring=moo[12]
	    tempunc=tempstring[0:4]
            if breakcount == 0:
		### can use np.delete(array,row/column/pointers,axis)###
		
		all_starts[0]= int(moo[4]) 
		all_ends[0]=TheMCount
		all_adjust[0]=float(moo[11])
                if float(tempunc) > 0. :
		    all_uncs[0]=float(tempunc)	# convert 1.65 sigma to 1 sigma
		else:
		    all_uncs[0]=0.
		all_sources[0]='p'
		breakcount=breakcount+1 
            else:
		all_starts=np.append(all_starts,int(moo[4]))
                all_ends=np.append(all_ends,int(moo[7]))		#int(moo[4]))
                all_adjust=np.append(all_adjust,float(moo[11]))		
                if float(tempunc) > 0.:
		    all_uncs=np.append(all_uncs,float(tempunc))
		else:
		    all_uncs=np.append(all_uncs,0.)
		     
		all_sources=np.append(all_sources,'p')
                breakcount=breakcount+1        

    all_starts[len(all_starts)-1]=1	#start at 1 because ID will (no intro extra CP)

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
            moo=str.split(line)
            if breakcount == 0:
		### can use np.delete(array,row/column/pointers,axis)###
		
		all_starts[0]=int(moo[2])
		all_ends[0]=TheMCount
		all_adjust[0]=float(moo[6])		
                if moo[7] > 0. :
		    all_uncs[0]=float(moo[7])	# convert 1.65 sigma to 1 sigma
		else:
		    all_uncs[0]=0.
		all_sources[0]='i'
		breakcount=breakcount+1 
            else:
		all_starts=np.append(all_starts,int(moo[2]))
                all_ends=np.append(all_ends,int(moo[3]))		#int(moo[4]))
                all_adjust=np.append(all_adjust,float(moo[6]))		
                if moo[7] > 0.:
		    all_uncs=np.append(all_uncs,float(moo[7]))
		else:
		    all_uncs=np.append(all_uncs,0.)
		     
		all_sources=np.append(all_sources,'i')
                breakcount=breakcount+1        

    return all_adjust, all_starts, all_ends, all_sources, all_uncs, breakcount # IDPHAReadSimple

#************************************************************************
# SORTBREAKSMERGE
def SortBreaksMerge(TheStarts,TheAdjs,TheUncs,TheBreakList,TheSources,TheBCount,TheMCount):
    ''' Looks at list of potential from TPHA and TID '''
    ''' Sorts them from 1 to 480 (or total) months '''
    ''' Merges duplicates and those within 12 months of a preceding break '''
    ''' Merges accumulated adjustment and uncertainty '''
    ''' Combines simultaneous adjustment/uncertainty across HSPs '''
    ''' resets nBreaks appropriately  '''
    ''' IF DPD inc and T stays the same, Td should dec and vice versa '''
    ''' IF T inc and DPD stays the same, Td should inc and vice versa '''
    ''' IF DPD inc and T inc, Td should stay about the same and vice versa '''
    ''' IF DPD inc and T dec, Td should decrease and vice versa '''
    ''' THIS WILL NOT ALWAYS WORK OUT PERFECTLY BUT ITS OWNLY FOR UNCERTAINTY ESTIMATION '''	

    
    SortedInd=np.argsort(TheStarts)	# sorts the list BreakLocs indexing from 0
    TheStarts=TheStarts[SortedInd]		
    TheAdjs=TheAdjs[SortedInd]		
    TheUncs=TheUncs[SortedInd]		
    TheSources=TheSources[SortedInd]	
    print(TheStarts)
 
    LastBreakLocSt=TheStarts[0]
    NewStarts=np.reshape(TheStarts[0],(1))
    NewAdjs=np.reshape(TheAdjs[0],(1))
    NewUncs=np.reshape(TheUncs[0],(1))
    NewSources=np.reshape(TheSources[0],(1))
    perr=0.
    ierr=0.
    padj=0.
    iadj=0.
    if TheSources[0] =='p' : 
        perr=TheUncs[0]
	padj=TheAdjs[0]
    else:
        ierr=TheUncs[0]
	iadj=TheAdjs[0]
        
    realcounter=1
    for bb in range(1,TheBCount):
        print(bb,TheSources[bb],realcounter,TheStarts[bb],LastBreakLocSt)
        if TheSources[bb] =='p' : 
            perr=TheUncs[bb]
	    padj=TheAdjs[bb]
        else:
            ierr=TheUncs[bb]
	    iadj=TheAdjs[bb]
   	if TheStarts[bb]-LastBreakLocSt> 11:	    # LastBreakLocSt-TheStarts[bb]  keep it if its at least a year apart from any other break
    	    print("NEW")
	    NewStarts=np.append(NewStarts,TheStarts[bb])
    	    NewAdjs=np.append(NewAdjs,padj+iadj)	#TheAdjs[bb])
    	    NewUncs=np.append(NewUncs,np.sqrt((perr**2) + (ierr**2)))	#TheUncs[bb])
    	    NewSources=np.append(NewSources,TheSources[bb])
    	    LastBreakLocSt=TheStarts[bb]
	    realcounter=realcounter+1
	else:
	    print("BOTH")
    	    NewAdjs[realcounter-1]=padj+iadj
    	    NewUncs[realcounter-1]=np.sqrt((perr**2) + (ierr**2))
    	    NewSources[realcounter-1]='b'

    TheBCount=len(NewStarts)

    # reverse all of the arrays, sort out ends and independent adjustment/uncertainties
    NewStarts=NewStarts[::-1]       	
    NewAdjs=s=NewAdjs[::-1]       	
    NewUncs=NewUncs[::-1]       	
    NewSources=NewSources[::-1]    
    NewEnds=np.empty_like(NewStarts)
    NewEnds[0]=TheMCount   	
    TheBreakList=np.zeros((TheBCount,4))	# Build this on the fly to equal nBreaks(rows) by rel(adj,unc),act(adj,unc) including last HSP which will be zero	
    for bb in range(1,TheBCount):
	NewEnds[bb]=(NewStarts[bb-1])-1
        TheBreakList[bb,0]=NewAdjs[bb]-NewAdjs[bb-1]		# this is this funny range thing again needs +1
        TheBreakList[bb,1]=np.sqrt((NewUncs[bb]**2)-(NewUncs[bb-1]**2))
        TheBreakList[bb,2]=NewAdjs[bb]		# minus or not minus?
        TheBreakList[bb,3]=NewUncs[bb]

    print(TheBCount,NewStarts)
       
    return NewStarts,NewEnds,TheBreakList,NewSources,TheBCount #SortBreaksMerge

#BUGFIX - WHEN T UNC MIXED WITH I UNC the accumulative uncertainties do not grow. HOw to cope with this?
#AGH - Need to add crossed periods together - so will only have the IDPHA number of breaks but they will change given PHA

#************************************************************************
# LOGBREAKINFOMERGE
def LogBreakInfoMerge(TheFile,TheStationID,TheBCount,TheMonthCount,TheBreakLocsSt,TheBreakList,TheSources):
    ''' Print out a list of breaks found with their location, size and uncertainty '''
    ''' Append to file '''
    ''' IN ALL CASES ADJUSTMENTS ARE -(adj) TO MATCH PHA OUTPUT '''
    ''' IF THE DATA HAVE BEEN ADJUSTED DOWN THEN THE ADJUSTMENT GIVEN IS POSITIVE - WEIRD '''
    filee=open(TheFile,'a+')
    if TheBCount == 1:
        filee.write('%11s %2s %3i %3i %6.2f %6.2f %6.2f %6.2f \n' % (TheStationID,1,1,
	           TheMonthCount,TheBreakList[0,0],TheBreakList[0,1],TheBreakList[0,2],TheBreakList[0,3]))
    else:
        LocEnd=TheMonthCount
	# Force first location of TheBreakLocs to be 0 instead of 1 so that a single line of code works
	for b in range(0,TheBCount):
	    print(TheBCount,b)
	    # no sign swapping of adjustments as this is a direct read in from the logs
            filee.write('%11s %2s %3i %3i %6.2f %6.2f %6.2f %6.2f %2s\n' % (TheStationID,TheBCount-b,TheBreakLocsSt[b],
	            LocEnd,TheBreakList[b,0],TheBreakList[b,1],TheBreakList[b,2],TheBreakList[b,3],TheSources[b]))
            LocEnd=(TheBreakLocsSt[b]-1)
    filee.close()
    return #LogBreakInfoMerge
    
#***********************************************************************
# MAIN PROGRAM
#***********************************************************************
# read in station list
MyTypes=("|S6","|S5","float","float","float","|S4","|S30","|S7","int")
MyDelimiters=[6,5,8,10,7,4,30,7,5]
RawData=ReadData(STATLIST,MyTypes,MyDelimiters)
StationListWMO=np.array(RawData['f0'])
StationListWBAN=np.array(RawData['f1'])
StationListLat=np.array(RawData['f2'])
StationListLon=np.array(RawData['f3'])
StationListElev=np.array(RawData['f4'])
StationListCID=np.array(RawData['f5'])
StationListName=np.array(RawData['f6'])
nstations=len(StationListWMO)

# loop through station by station
for st in range(nstations):

# check if restart necessary
    if Restarter != '------' and Restarter != StationListWMO[st]:
        continue

    Restarter='------'
# set up clean arrays and variables
    nNstations=0	# defined after reading corr station list
    NeighbourList=[] # nNstations list filled after reading in corr station list

    nBreaks=0	# defined after finding and reading in break locs
    BreakLocs=np.reshape(0,(1))	# nBreaks list of locations filled after reading in break locs list
    BreakSize=np.reshape(0.,(1))	# nBreaks list of sizes filled after reading in break locs list
    BreakUncs=np.reshape(0.,(1))	# nBreaks list of uncertainties filled after reading in break locs list
    NewBreakDist=[]	# filled each time a break size is found from all neighbour difference series
    NewBreakList=[]	# nBreaks by 4 array for mean adjustment relative to next most recent HSP, 1.65sigma unc, total adjustment relative to most recent HSP, total 1.65sigma unc
    MyBreakLocs=[]	# nBreaks+2 month locations for each break including month 1 if needed and last month

    MyStation=[]	# filled after reading in candidate station
    MyClims=[]	# 12 element array of mean months 1976-2005
    MyAnomalies=[] # filled with anomalies after subtracting climatology
    MyHomogAnoms=[] # filled with homogenised anomalies
    MyHomogAbs=[]  # filled with climatology+homogenised anomalies
    MyClimMeanShift=[] # flat value across complete climatology period that the homogenised values differ from zero by - to rezero anoms and adjust clims/abs

    NeighbourStations=[]	# nNstations by nmons array filled after reading in all neighbour stations
    NeighbourAnomsStations=[]	# nNstations by nmons array filled after anomalising all neighbour stations relative to climatology
    NeighbourClimsStations=[]	# nNstations by nmons array filled after anomalising all neighbour stations relative to climatology
    NeighbourDiffStations=[]	# nNstations by nmons array filled after creating candidate minus neighbour difference series


# read in the station file
    if param == 't':
        MyFile=INPHA+StationListWMO[st]+StationListWBAN[st]+'_PHAadj.txt'
        print(st,MyFile)  
        MyTypes=np.append("|S16",["int"]*12)
        MyDelimiters=np.append([16,6],[7]*11)
        RawData=ReadData(MyFile,MyTypes,MyDelimiters)
        for yy in yrarr:
            moo=list(RawData[yy])
            if yy == 0: 
                MyStation=moo[1:13] 
            else:
                MyStation=np.append(MyStation,moo[1:13])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element
    else:
        MyFile=INRAW+StationListWMO[st]+"-"+StationListWBAN[st]+STATSUFFIXIN  
        print(st,MyFile)  
        MyTypes=np.append("|S12",["int"]*13)
        MyDelimiters=np.append([12,4,6],[9]*11)
        RawData=ReadData(MyFile,MyTypes,MyDelimiters)
        for yy in yrarr:
            moo=list(RawData[yy])
            if yy == 0: 
                MyStation=moo[2:14] 
            else:
                MyStation=np.append(MyStation,moo[2:14])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element
  
    MyStation=np.reshape(MyStation/100.,(1,len(MyStation)))	# now in proper units and an array not list

# find the breaks for that station from DPD and T
    BreakSize,BreakLocs,BreakUncs,nBreaks=PHARead(DPDBREAKFIL,StationListWMO[st]+StationListWBAN[st],
                                          BreakSize,BreakLocs,BreakUncs,nBreaks,nmons)

    if (param != 't'):	# no need to apply T breaks if working on T 
        BreakSize,BreakLocs,BreakUncs,nBreaks=PHARead(TBREAKFIL,StationListWMO[st]+StationListWBAN[st],
	                                      BreakSize,BreakLocs,BreakUncs,nBreaks,nmons)

# If there are breaks - find the neighbour network for that station
    if nBreaks > 0:
        nNstations,NeighbourList=FindNeighbours(CORRFIL,StationListWMO[st]+StationListWBAN[st],nNstations,
	                         NeighbourList)
        print("No. of Neighbours: ",nNstations-1)	# not including candidate but may have duplicate
        #print(NeighbourList)
        if (nNstations-1) < 7:	# TOO FEW NEIGHBOURS
	    if (nNstations > 0): nNstations=nNstations-1
	    ListStation(NONEIGHBOURSLIST,StationListWMO[st]+StationListWBAN[st],StationListLat[st],
	                StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st],nNstations)
	    continue

# read in the neighbour files - if insufficient then list in bad stations list
        NeighbourStations,NeighbourList,nNstations=ReadInNetworks(nNstations,NeighbourList,
	                                           StationListWMO[st]+StationListWBAN[st],INRAW,
						   STATSUFFIXIN,yrarr,NeighbourStations)
        print("Actual No. of Neighbours: ",nNstations)	# not including candidate but may have duplicate
        #print(NeighbourList)
        if nNstations < 7:
	    ListStation(NONEIGHBOURSLIST,StationListWMO[st]+StationListWBAN[st],StationListLat[st],
	                StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st],nNstations)
	    continue

# convert all to anomalies (storing station climatology)
        MyAnomalies,MyClims=MakeAnomalies(MyStation,MyAnomalies,MyClims,nyrs,clmsty,clmedy,mdi)
	
        NeighbourAnomsStations,NeighbourClimsStations=MakeAnomalies(NeighbourStations,NeighbourAnomsStations,
	                                              NeighbourClimsStations,nyrs,clmsty,clmedy,mdi)
        
# make neighbour difference series using the anomalies
        NeighbourDiffStations=MakeDiffSeries(MyAnomalies,NeighbourAnomsStations,NeighbourDiffStations,mdi,nmons)

# sort all breaks from last to most recent, remove duplicates (+- 6months), loop through HSPs (Homogeneous subperiods)
	BreakLocs,MyBreakLocs,nBreaks=SortBreaks(BreakLocs,MyBreakLocs,nBreaks,nmons)

# Loop through all break periods, get distribution of shifts from difference series, assign relative and total adjustment and uncertainty
        NewBreakList,nBreaks,MyBreakLocs=AssignJumpSizeUnc(NewBreakList,nBreaks,MyBreakLocs,NewBreakDist,NeighbourDiffStations,mdi)
	print NewBreakList    
	
# apply adjustments to station anomaly series and rezero homogenised 
# move raw to mean of homogenised so that when they are plotted they lie together for the most recent HSP (not saved so ok to do this to aid visual inspection)
	MyAnomalies,MyHomogAnoms,MyClimMeanShift=ApplyJumpsReZero(MyAnomalies,MyHomogAnoms,NewBreakList,nBreaks,MyBreakLocs,clmstm,clmedm,mdi,MyClimMeanShift)
        print "MEAN SHIFT ",MyClimMeanShift
	
# add back climatology to homogeneous station anomalies
        MyHomogAbs=MakeAbs(MyHomogAnoms,MyHomogAbs,MyClims,mdi,nyrs,MyClimMeanShift)

# PLOT CANDIDATE AND NEIGHBOURS UNHOMOG WITH HOMOG ON TOP - ABS, ANOMS with MedianPairwiseTrends
# REZEROD HOMOG MAY MEAN ITS NOW OFFSET COMPARED TO ORIGINAL
	if param != 't':
	    MyPlotFile=OUTPLOT+StationListWMO[st]+StationListWBAN[st]+'_trendcomp_7312OCT2013abs'
            PlotHomogTS(MyPlotFile,MyStation,NeighbourStations,MyHomogAbs,mdi,styr,nyrs,unit,'absolutes')
            MyPlotFile=OUTPLOT+StationListWMO[st]+StationListWBAN[st]+'_trendcomp_7312OCT2013anoms'
            PlotHomogTS(MyPlotFile,MyAnomalies,NeighbourAnomsStations,MyHomogAnoms,mdi,styr,nyrs,unit,'anomalies')
        else:
	    MyStation=[]	# filled after reading in candidate station
	    MyFile=INRAW+StationListWMO[st]+'-'+StationListWBAN[st]+STATSUFFIXIN
            print(st,MyFile)  
            MyTypes=np.append("|S12",["int"]*13)
            MyDelimiters=np.append([12,4,6],[9]*11)
            RawData=ReadData(MyFile,MyTypes,MyDelimiters)
            for yy in yrarr:
                moo=list(RawData[yy])
                if yy == 0: 
                    MyStation=moo[2:14] 
                else:
                    MyStation=np.append(MyStation,moo[2:14])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element
            MyStation=np.reshape(MyStation/100.,(1,len(MyStation)))	# now in proper units and an array not list
	    
	    MyPlotFile=OUTPLOT+StationListWMO[st]+StationListWBAN[st]+'_trendcomp_7312OCT2013abs'
            PlotHomogTS(MyPlotFile,MyStation,NeighbourStations,MyHomogAbs,mdi,styr,nyrs,unit,'absolutes')
            MyPlotFile=OUTPLOT+StationListWMO[st]+StationListWBAN[st]+'_trendcomp_7312OCT2013anoms'
            PlotHomogTS(MyPlotFile,MyAnomalies,NeighbourAnomsStations,MyHomogAnoms,mdi,styr,nyrs,unit,'anomalies')
	
# print out homogenised station anomalies
        MyFileOut=OUTHOM+StationListWMO[st]+StationListWBAN[st]+STATSUFFIXOUT  
        WriteOut(MyHomogAbs,MyFileOut,yrarr,styr,StationListWMO[st]+StationListWBAN[st])

# print out break stats (inc. accumulated breaks and uncs)
        LogBreakInfo(BREAKSINFO,StationListWMO[st]+StationListWBAN[st],nBreaks,nmons,MyBreakLocs[:-1],NewBreakList)
        # for 't' merge old PHA and new IDPHA breaks and log
	if param == 't':
	    MergeAdjustments(TBREAKFIL,BREAKSINFO,BREAKSINFOMERGE,StationListWMO[st]+StationListWBAN[st],nmons)
	    

# If no breaks - go to printing out the homogeneous station and zero breaks stats
    else:
        nBreaks=1	# so that LogBreakInfo works for all with the for loop
        MyFileOut=OUTHOM+StationListWMO[st]+StationListWBAN[st]+STATSUFFIXOUT  
        WriteOut(MyStation,MyFileOut,yrarr,styr,StationListWMO[st]+StationListWBAN[st])
	NewBreakList=np.reshape([0.,0.,0.,0.],(1,4))	# set up a row
        LogBreakInfo(BREAKSINFO,StationListWMO[st]+StationListWBAN[st],nBreaks,nmons,BreakLocs,NewBreakList)
	# catch the no breaks cases for T
	if param == 't':
            LogBreakInfo(BREAKSINFOMERGE,StationListWMO[st]+StationListWBAN[st],nBreaks,nmons,BreakLocs,NewBreakList)

# list in good station list
    ListStation(GOTNEIGHBOURSLIST,StationListWMO[st]+StationListWBAN[st],StationListLat[st],
	                StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st],nNstations)

# end loop of stations

#    stop()

print("And, we are done!")
