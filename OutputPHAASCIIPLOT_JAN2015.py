#!/usr/local/sci/bin/python
# PYTHON2.7
# 
# Author: Kate Willett
# Created: 24 February 2014
# Last update: 29 January 2016
# Location: /data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# This codes reads in the homogenised monthly mean data from PHA, outputs to ASCII, infilling
# hte missing years with missing data indicators (entire missing years are not printed by PHA).
# This code also plots the raw and homogenised station series alongside its raw neighbours with
# the linear trend (median pairwise) shown, for abs and anomaly annual means. 
# It can cope with PHA, IDPHA and PHADPD homogenised modes.
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
#
# Kates:
# from LinearTrends import MedianPairwise - fits linear trend using median pairwise
# 
# -----------------------
# DATA
# -----------------------
# # The 40 nearest correlating neighbours from PHA    
# CORRFIL='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315q/corr/corr.log'	
# The raw monthly mean station data
# INRAW='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/QABS/'
# The PHA station list to work through
# STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAq_'+thenmon+thenyear+'.txt'	
# OR the IDPHA list to work through
# STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAq_'+thenmon+thenyear+'.txt'	
# Homogenised monthly mean station data from PHA
# INHOM='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315q/monthly/WMs.r00/'
# Homogenised monthly mean station data from IDPHA
# INHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/IDPHAASCII/QDIR/'
# For TdL
# IDPHA homogenised monthly mean T for creating Td
# INHOMT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/IDPHAASCII/TDIR/'
# PHA homogenised monthly mean DPD for creating Td
# INHOMDPD='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/PHAASCII/DPDDIR/'
# Log of changepoint locations and magnitudes and uncertainties for DPD to merge with T breaks
# DPDBREAKFIL='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landDPD.'+version+'_PHA_'+thenmon+thenyear+'.log'
# Log of changepoint locations and magnitudes and uncertainties for T to merge with DPD breaks
# TBREAKFIL='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landT.'+version+'_IDPHAMG_'+thenmon+thenyear+'.log'
#
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# Go through everything in the 'Start' section to make sure dates, versions and filepaths are up to date
# Choose param settings for the desired variable (also in 'Start' section)
# This can take an hour or so to run through ~3800 stations so consider using screen, screen -d, screen -r
# python2.7 OutputPHAASCIIPLOT_JAN2015.py
#
# NB: In a few cases Td will not have neighbours to plot so prog will fail. Restart.
# 
# -----------------------
# OUTPUT
# -----------------------
# # PHA Plot showing raw and homogenised candidate vs raw neighbours with linear trends for abs and anomly monthly means
# OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/QDIR/'
# or if IDPHA
# OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/IDADJCOMP/QDIR/'
# PHA only: Output monthly mean homogenised ASCII with missing years infilled with missing data indicator
# OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/PHAASCII/QDIR/'
# For Derived Td mode (PHADPD)
# Output log of merged T and DPD changepoints, adjustments, uncertainties that essentially went into Td (indirectly as Td is 
# created from T - DPD
# TDBREAKFIL='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landTd.'+version+'_PHADPD_'+thenmon+thenyear+'.log'
# Derived Td is stored as for IDPHA:
# OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/IDPHAASCII/TDDIR/'
# OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/IDADJCOMP/TDDIR/'
#
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
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
Spin='TRUE'	#TRUE: loop through, FALSE: perform one stations only
Plotonly='FALSE'	#TRUE or FALSE
AddLetter='a)'		#'---'

# Set up initial run choices
param='td'	# tw, q, e, rh, t, td, dpd
param2='Td'	# Tw, q, e, RH, T, Td, DPD
unit='degrees C'	# 'deg C','g/kg','hPa', '%rh'
nowmon='JAN'
nowyear='2016'
thenmon='JAN'
thenyear='2016'
version='2.1.0.2015p'
homogtype='PHADPD'	#'PHA','IDPHA','PHADPD'

# Set up file locations

STATSUFFIXOUT='_PHAadj.txt'

if param == 'rh':
    STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHArh_'+thenmon+thenyear+'.txt'	
    CORRFIL='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315rh/corr/corr.log'	
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/RHABS/'
    STATSUFFIXIN='_RHmonthQCabs.raw'
    INHOM='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315rh/monthly/WMs.r00/'
    OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/PHAASCII/RHDIR/'
    OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/RHDIR/'

elif param == 'q':
    CORRFIL='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315q/corr/corr.log'	
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/QABS/'
    STATSUFFIXIN='_qmonthQCabs.raw'
    if homogtype == 'PHA':
        STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAq_'+thenmon+thenyear+'.txt'	
        INHOM='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315q/monthly/WMs.r00/'
        OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/QDIR/'
        OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/PHAASCII/QDIR/'
    elif homogtype =='IDPHA':
        STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAq_'+thenmon+thenyear+'.txt'	
        INHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/IDPHAASCII/QDIR/'
        OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/IDADJCOMP/QDIR/'

elif param == 'tw':
    STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAtw_'+thenmon+thenyear+'.txt'	
    CORRFIL='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315tw/corr/corr.log'
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/TWABS/'
    STATSUFFIXIN='_TwmonthQCabs.raw'
    INHOM='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315tw/monthly/WMs.r00/'
    OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/PHAASCII/TWDIR/'
    OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/TWDIR/'

elif param == 'e':
    STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAe_'+thenmon+thenyear+'.txt'	
    CORRFIL='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315e/corr/corr.log'
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/EABS/'
    STATSUFFIXIN='_emonthQCabs.raw'
    INHOM='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315e/monthly/WMs.r00/'
    OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/PHAASCII/EDIR/'
    OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/EDIR/'

elif param == 't':
    STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAt_'+thenmon+thenyear+'.txt'	
    CORRFIL='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA2015/pha52jgo/data/hadisdh/7315t/corr/corr.log'	
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/TABS/'
    STATSUFFIXIN='_TmonthQCabs.raw'
    INHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA2015/pha52jgo/data/hadisdh/7315t/monthly/WMs.r00/'
    OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/PHAASCII/TDIR/'
    OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/TDIR/'

elif param == 'dpd':
    STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAdpd_'+thenmon+thenyear+'.txt'	
    CORRFIL='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA2015/pha52jgo/data/hadisdh/7315dpd/corr/corr.log'
    INRAW='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/DPDABS/'
    STATSUFFIXIN='_DPDmonthQCabs.raw'
    INHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA2015/pha52jgo/data/hadisdh/7315dpd/monthly/WMs.r00/'
    OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/PHAASCII/DPDDIR/'
    OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/DPDDIR/'

elif param == 'td':
    if homogtype == 'PHADPD':
        STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHADPDtd_'+thenmon+thenyear+'.txt'	
        CORRFIL='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA2015/pha52jgo/data/hadisdh/7315td/corr/corr.log'	
        INRAW='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/TDABS/'
        STATSUFFIXIN='_TdmonthQCabs.raw'
#    INHOM='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/hadisdh7313td/monthly/WMs.r00/'
        INHOMT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/IDPHAASCII/TDIR/'
        INHOMDPD='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/PHAASCII/DPDDIR/'
        DPDBREAKFIL='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landDPD.'+version+'_PHA_'+thenmon+thenyear+'.log'
        TBREAKFIL='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landT.'+version+'_IDPHAMG_'+thenmon+thenyear+'.log'
        TDBREAKFIL='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landTd.'+version+'_PHADPD_'+thenmon+thenyear+'.log'
        OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/IDPHAASCII/TDDIR/'
        OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/IDADJCOMP/TDDIR/'
    #NB: In a few cases Td will not have neighbours to plot so prog will fail. Restart.
    else:
        STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAtd_'+thenmon+thenyear+'.txt'	
        CORRFIL='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315td/corr/corr.log'	
        INRAW='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/derivedTDABS/'
        STATSUFFIXIN='_deTdmonthQCabs.raw'
        INHOM='/data/local/hadkw/HADCRUH2/PROGS/PHA2015/pha52jgo/data/hadisdh/7315td/monthly/WMs.r00/'
        OUTHOM='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/PHAASCII/TDDIR/'
        OUTPLOT='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HOMOG/STAT_PLOTS/PHAADJCOMP/TDDIR/'
        

# Set up variables and arrays needed

mdi=-99.99

styr=1973
edyr=2015
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

MyStation=[]	# filled after reading in candidate station
MyRAWStation=[]	# filled after reading in candidate station
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
		
		all_starts[0]=int(moo[4])
		all_ends[0]=TheMCount
		all_adjust[0]=float(moo[11])
                if float(tempunc) > 0. :
		    all_uncs[0]=float(tempunc)	# convert 1.65 sigma to 1 sigma
		else:
		    all_uncs[0]=0.
		all_sources[0]='dd'
		breakcount=breakcount+1 
            else:
		all_starts=np.append(all_starts,int(moo[4]))
                all_ends=np.append(all_ends,int(moo[7]))		#int(moo[4]))
                all_adjust=np.append(all_adjust,float(moo[11]))		# positive adjustments to dewpoint t
                if float(tempunc) > 0.:
		    all_uncs=np.append(all_uncs,float(tempunc))
		else:
		    all_uncs=np.append(all_uncs,0.)
		     
		all_sources=np.append(all_sources,'dd')
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
		all_adjust[0]=-(float(moo[6]))		# negative adjustments to dewpoint t
                if moo[7] > 0. :
		    all_uncs[0]=float(moo[7])	# convert 1.65 sigma to 1 sigma
		else:
		    all_uncs[0]=0.
		all_sources[0]='t'
		breakcount=breakcount+1 
            else:
		all_starts=np.append(all_starts,int(moo[2]))
                all_ends=np.append(all_ends,int(moo[3]))		#int(moo[4]))
                all_adjust=np.append(all_adjust,-(float(moo[6])))		# negative adjustments to dewpoint t
                if moo[7] > 0.:
		    all_uncs=np.append(all_uncs,float(moo[7]))
		else:
		    all_uncs=np.append(all_uncs,0.)
		     
		all_sources=np.append(all_sources,'t')
                breakcount=breakcount+1        

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
    derr=0.
    terr=0.
    dadj=0.
    tadj=0.
    if TheSources[0] =='t' : 
        terr=TheUncs[0]
	tadj=TheAdjs[0]
    else:
        derr=TheUncs[0]
	dadj=TheAdjs[0]
    
    realcounter=0
    for bb in range(1,TheBCount):
        if TheSources[bb] =='t' : 
            terr=TheUncs[bb]
	    tadj=TheAdjs[bb]
        else:
            derr=TheUncs[bb]
	    dadj=TheAdjs[bb]
   	if TheStarts[bb]-LastBreakLocSt > 11:	    # keep it if its at least a year apart from any other break
    	    NewStarts=np.append(NewStarts,TheStarts[bb])
    	    NewAdjs=np.append(NewAdjs,tadj+dadj)
    	    NewUncs=np.append(NewUncs,np.sqrt((terr**2) + (derr**2)))
    	    NewSources=np.append(NewSources,TheSources[bb])
    	    LastBreakLocSt=TheStarts[bb]
	    realcount=realcounter+1
	else:
    	    NewAdjs[realcounter-1]=tadj+dadj
    	    NewUncs[realcounter-1]=np.sqrt((terr**2) + (derr**2))
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
	    # sign swapping of adjustments for consistency with PHA logs
            filee.write('%11s %2s %3i %3i %6.2f %6.2f %6.2f %6.2f %2s\n' % (TheStationID,TheBCount-b,TheBreakLocsSt[b],
	            LocEnd,-(TheBreakList[b,0]),TheBreakList[b,1],-(TheBreakList[b,2]),TheBreakList[b,3],TheSources[b]))
            LocEnd=(TheBreakLocsSt[b]-1)
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
# PLOTHOMOGTS
def PlotHomogTS(TheFile,TheStation,TheNeighbours,TheHStation,TheNCount,TheMDI,TheStYr,TheYCount,unit,typee,Letteree):
    ''' Plot raw candidate and neighbours with homogenised candidate '''
    ''' Add medianpairwise trends - from code medianpairwise.py '''
    '''MAKE MEDIANPAIRWISE.PY and COMPLETE WHEN HOMOG SERIES IS DONE '''
 
    # create annual averages and years and titles
    TheStationAnn=np.empty(TheYCount)
    TheStationAnn.fill(TheMDI)
    TheHStationAnn=np.empty(TheYCount)
    TheHStationAnn.fill(TheMDI)
    if TheNCount > 1:
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
   
    if TheNCount > 1:
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
    if TheNCount > 1:
        PileItUp=np.append(TheNeighboursAnn,np.append(np.reshape(TheStationAnn,(1,TheYCount)),
             np.reshape(TheHStationAnn,(1,TheYCount)),axis=0),axis=0)
    else:
        PileItUp=np.append(np.reshape(TheStationAnn,(1,TheYCount)),
             np.reshape(TheHStationAnn,(1,TheYCount)),axis=0)
    
    plt.ylim([np.floor(min(PileItUp[PileItUp != TheMDI]))-2,
              np.ceil(max(PileItUp[PileItUp != TheMDI]))+2])
    plt.xlim([TheStYr,TheStYr+TheYCount])
    plt.tick_params(axis='both', which='major', labelsize=16)
   
    if TheNCount > 1:
        for n,Neighbour in enumerate(TheNeighboursAnn):
            line,=plt.plot(TheYears[np.where(Neighbour > TheMDI)],Neighbour[np.where(Neighbour > TheMDI)],color='black',linewidth=0.25)
 	
    line,=plt.plot(TheYears[np.where(TheStationAnn > TheMDI)],TheStationAnn[np.where(TheStationAnn > TheMDI)],'r',linewidth=2)	
    line,=plt.plot(TheYears[np.where(TheHStationAnn > TheMDI)],TheHStationAnn[np.where(TheHStationAnn > TheMDI)],'b',linewidth=2)
    if typee=='anomalies':
        line,=plt.plot(np.append(TheYears,TheStYr+TheYCount+1),np.zeros(TheYCount+1),'black',linewidth=1)        	
    
    plt.xlabel(xtitlee,size=16)
    plt.ylabel(ytitlee,size=16)
    
#    watermarkstring="/".join(os.getcwd().split('/')[4:])+'/'+os.path.basename( __file__ )+"   "+dt.datetime.strftime(dt.datetime.now(), "%d-%b-%Y %H:%M")
#    plt.figtext(0.01,0.01,watermarkstring,size=6)
    
    rawstr="%5.2f +/- %5.2f to %5.2f %s /decade " % (rawtrend[0]*10,rawtrend[1]*10,rawtrend[2]*10,unit)
    homstr="%5.2f +/- %5.2f to %5.2f %s /decade " % (homtrend[0]*10,homtrend[1]*10,homtrend[2]*10,unit)

    plt.figtext(0.1,0.84,rawstr,color='r',size=16)
    plt.figtext(0.1,0.78,homstr,color='b',size=16)
    if Letteree != '---':
       plt.figtext(0.05,0.95,Letteree,color='Black',size=18)
       
    #plt.show()
    plt.savefig(TheFile+".eps")
    plt.savefig(TheFile+".png")
     
    return #PlotHomogTS
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

    MyStation=np.zeros((nyrs,12))	# filled after reading in candidate station
    MyStation[:,:]=(-9999)
    MyTStation=[]
    MyDPDStation=[]
    MyRAWStation=[]
    MyClims=[]	# 12 element array of mean months 1976-2005
    MyAnomalies=[] # filled with anomalies after subtracting climatology
    MyHomogAnoms=[] # filled with homogenised anomalies
    MyHomogAbs=[]  # filled with climatology+homogenised anomalies
    MyClimMeanShift=[] # flat value across complete climatology period that the homogenised values differ from zero by - to rezero anoms and adjust clims/abs

    NeighbourStations=[]	# nNstations by nmons array filled after reading in all neighbour stations
    NeighbourAnomsStations=[]	# nNstations by nmons array filled after anomalising all neighbour stations relative to climatology
    NeighbourClimsStations=[]	# nNstations by nmons array filled after anomalising all neighbour stations relative to climatology
    NeighbourDiffStations=[]	# nNstations by nmons array filled after creating candidate minus neighbour difference series

# read in the RAW station file
    MyFile=INRAW+StationListWMO[st]+"-"+StationListWBAN[st]+STATSUFFIXIN  
    MyTypes=np.append("|S12",["int"]*13)
    MyDelimiters=np.append([12,4,6],[9]*11)
    RawData=ReadData(MyFile,MyTypes,MyDelimiters)
    for yy in yrarr:
        moo=list(RawData[yy])
        if yy == 0: 
            MyRAWStation=moo[2:14] 
        else:
            MyRAWStation=np.append(MyRAWStation,moo[2:14])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element

    print(st,MyFile)  
  
    MyRAWStation=np.reshape(MyRAWStation/100.,(1,nmons))	# now in proper units and an array not list

# read in the PHA HOMOGENISED station file
    if homogtype == 'PHA':
        MyFile=INHOM+StationListWMO[st]+StationListWBAN[st]+".WMs.r00.tavg"  
        MyTypes=np.append(["|S16","|S6"],["|S9"]*11)
        MyDelimiters=np.append([16,6],[9]*11)
        RawData=ReadData(MyFile,MyTypes,MyDelimiters)
        for yy in range(0,len(RawData)):
            # get the year
	    moo=list(RawData[yy])
	    mystring=moo[0]
	    ypoint=int(mystring[12:16])-styr
	    # get the non'd' bits of the strings
	    newmoo=[int(a[-5:]) for a in moo[1:13]]
#	    print("NEWMOO",newmoo)
            MyStation[ypoint]=newmoo

        print(st,MyFile)  
        MyStation=np.reshape(MyStation/100.,(1,nmons))	# now in proper units and an array not list
    elif homogtype == 'PHADPD':
        MyFile=INHOMT+StationListWMO[st]+StationListWBAN[st]+'_IDPHAadj.txt'
        MyTypes=np.append("|S16",["int"]*12)
        MyDelimiters=np.append([16,6],[7]*11)
        RawData=ReadData(MyFile,MyTypes,MyDelimiters)
        for yy in yrarr:
            moo=list(RawData[yy])
            if yy == 0: 
                MyTStation=moo[1:13] 
            else:
                MyTStation=np.append(MyTStation,moo[1:13])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element
        print(st,MyFile)    
        MyTStation=np.reshape(MyTStation/100.,(1,nmons))	# now in proper units and an array not list
        
        MyFile=INHOMDPD+StationListWMO[st]+StationListWBAN[st]+'_PHAadj.txt'
        MyTypes=np.append("|S16",["int"]*12)
        MyDelimiters=np.append([16,6],[7]*11)
        RawData=ReadData(MyFile,MyTypes,MyDelimiters)
        for yy in yrarr:
            moo=list(RawData[yy])
            if yy == 0: 
                MyDPDStation=moo[1:13] 
            else:
                MyDPDStation=np.append(MyDPDStation,moo[1:13])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element
        print(st,MyFile)  
  
        MyDPDStation=np.reshape(MyDPDStation/100.,(1,nmons))	# now in proper units and an array not list
	
	# create Td from T-DPD where data exist
	MyStation=np.empty_like(MyTStation)
        MyStation[:,:]=(-99.99)
	for mm in range(len(MyStation[0,:])):
	    if MyTStation[0,mm] > mdi and MyDPDStation[0,mm] > mdi: 
	        MyStation[0,mm]=MyTStation[0,mm]-MyDPDStation[0,mm]
	# ALSO FAFF AROND READING IN ADJUSTMENT FILES AND MERGING
	MergeAdjustments(DPDBREAKFIL,TBREAKFIL,TDBREAKFIL,StationListWMO[st]+StationListWBAN[st],nmons)

    elif homogtype == 'IDPHA':
        MyFile=INHOM+StationListWMO[st]+StationListWBAN[st]+'_IDPHAadj.txt'
        MyTypes=np.append("|S16",["int"]*12)
        MyDelimiters=np.append([16,6],[7]*11)
        RawData=ReadData(MyFile,MyTypes,MyDelimiters)
        for yy in yrarr:
            moo=list(RawData[yy])
            if yy == 0: 
                MyStation=moo[1:13] 
            else:
                MyStation=np.append(MyStation,moo[1:13])	# for some silly reason you subscript starting from 0th element to the nth rather than n-1th element
        print(st,MyFile)    
        MyStation=np.reshape(MyStation/100.,(1,nmons))	# now in proper units and an array not list
                
    nNstations,NeighbourList=FindNeighbours(CORRFIL,StationListWMO[st]+StationListWBAN[st],nNstations,
	                         NeighbourList)
    print("No. of Neighbours: ",nNstations-1)	# not including candidate but may have duplicate
    if nNstations > 1:
# read in the neighbour files - if insufficient then list in bad stations list
        NeighbourStations,NeighbourList,nNstations=ReadInNetworks(nNstations,NeighbourList,
	                                           StationListWMO[st]+StationListWBAN[st],INRAW,
						   STATSUFFIXIN,yrarr,NeighbourStations)
        print("Actual No. of Neighbours: ",nNstations)	# not including candidate but may have duplicate

# convert all to anomalies (storing station climatology)
    MyAnomalies,MyClims=MakeAnomalies(MyStation,MyAnomalies,MyClims,nyrs,clmsty,clmedy,mdi)
    MyHomogAnoms,MyClims=MakeAnomalies(MyRAWStation,MyHomogAnoms,MyClims,nyrs,clmsty,clmedy,mdi)
	
    NeighbourAnomsStations,NeighbourClimsStations=MakeAnomalies(NeighbourStations,NeighbourAnomsStations,
	                                              NeighbourClimsStations,nyrs,clmsty,clmedy,mdi)
        
# PLOT CANDIDATE AND NEIGHBOURS UNHOMOG WITH HOMOG ON TOP - ABS, ANOMS with MedianPairwiseTrends
# REZEROD HOMOG MAY MEAN ITS NOW OFFSET COMPARED TO ORIGINAL
    MyPlotFile=OUTPLOT+StationListWMO[st]+StationListWBAN[st]+'_trendcomp_'+param+'_'+nowmon+nowyear+'abs'
    PlotHomogTS(MyPlotFile,MyRAWStation,NeighbourStations,MyStation,nNstations,mdi,styr,nyrs,unit,'absolutes',AddLetter)
    MyPlotFile=OUTPLOT+StationListWMO[st]+StationListWBAN[st]+'_trendcomp_'+param+'_'+nowmon+nowyear+'anoms'
    PlotHomogTS(MyPlotFile,MyAnomalies,NeighbourAnomsStations,MyHomogAnoms,nNstations,mdi,styr,nyrs,unit,'anomalies',AddLetter)

# print out homogenised station anomalies
    if Plotonly == 'FALSE':
        MyFileOut=OUTHOM+StationListWMO[st]+StationListWBAN[st]+STATSUFFIXOUT  
        WriteOut(MyStation,MyFileOut,yrarr,styr,StationListWMO[st]+StationListWBAN[st])
    if Spin == 'FALSE':
        break
# end loop of stations

#    stop()

print("And, we are done!")
