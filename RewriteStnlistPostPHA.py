#!/usr/local/sci/bin/python
# PYTHON3
# 
# Author: Kate Willett
# Created: 31 January 2018
# Last update: 17 February 2020
# Location: /data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# This code creates the new station lists after running PHA and removal of stations with which to run the 
# rest of the HadISDH build code. Stations are removed by PHA because there are too few neighbours. This occurs 
# differently for each variable. Then the station removals from DPD and T are then propogated through for IDPHA 
# for T, Tw, e, q and RH.
#
# This code also copies the corr* files for each variable to corr.log - this is in each variable's own PHA location
# /data/local/hadkw/HADCRUH2/UPDATE2017/PROGS/PHA2015/pha52jgo/data/hadisdh/73<yy><var>/corr/corr.log
# 
# This code also reformats the list of adjustments applied and saves as a new file in both the local PHA space and LISTS_DOCS,
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# inbuilt:
# import sys, os
# import struct
# import pdb
# from subprocess import call
#
# Kates:
#
# -----------------------
# DATA
# -----------------------
# 
# Post-PHA station lists are read in from:
# /data/local/hadkw/HADCRUH2/UPDATE<yyyy>/PROGS/PHA2015/pha52jgo/data/hadisdh/73<yy><var>/corr/meta.73<yy><var>.tavg.r00.<yymmddhhmm>
#
# PHA correlation files are read in from
# /data/local/hadkw/HADCRUH2/UPDATE<yyyy>/PROGS/PHA2015/pha52jgo/data/hadisdh/73<yy><var>/corr/corr.73<yy><var>.tavg.r00.<yymmddhhmm>
#
# PHA logs are read in from
# /data/local/hadkw/HADCRUH2/UPDATE<yyyy>/PROGS/PHA2015/pha52jgo/data/hadisdh/73<yy><var>/output/PHAv52j.FAST.MLY.TEST.<yymmddhhmm>.tavg.73<yy><var>.r00.out.gz
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# Go through everything in the 'Start' section to make sure dates, versions and filepaths are up to date
# python2.7 RewriteStnlistPostPHA.py
# 
# -----------------------
# OUTPUT
# -----------------------
# Output station lists are created for direct PHA:
# /data/local/hadkw/HADCRUH2/UPDATE<yyyy>/LISTS_DOCS/goodforHadISDH.<version>_PHA<var>_JAN<yyyy>.txt
# Output station lists are created for indirect IDPHA:
# /data/local/hadkw/HADCRUH2/UPDATE<yyyy>/LISTS_DOCS/goodforHadISDH.<version>_IDPHAall_JAN<yyyy>.txt
#
# Lists of all adjustments applied are created and saved:
# /data/local/hadkw/HADCRUH2/UPDATE<yyyy>/LISTS_DOCS/HadISDH.land<var>.<version>_PHA_JAN<yyyy>.log
# /data/local/hadkw/HADCRUH2/UPDATE<yyyy>/PROGS/PHA2015/pha52jgo/data/hadisdh/73<yy><var>/output/HadISDH.land<var>.<version>_PHA_JAN<yyyy>.log
#
# Correlations with all other station lists are copied to corr.log
# /data/local/hadkw/HADCRUH2/UPDATE<yyyy>/PROGS/PHA2015/pha52jgo/data/hadisdh/73<yy><var>/corr/corr.log
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
#
# Version 3 (22 October 2020)
# ---------
#  
# Enhancements
# Now can work without any annual update to the code - reads from F1_HadISDHBuildConfig.txt
#  
# Changes
#  
# Bug fixes
# 
# Version 2 (17 February 2020)
# ---------
#  
# Enhancements
#  
# Changes
# Now in Python 3 rather than Python 2.7
#  
# Bug fixes
#
# Version 1 (31 January 2018)
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
# Double check use of searchsorted because this gives the intersect, not the match
# Its ok as long as all elements exist in the other array. Use np.in1d instead.
#
#************************************************************************
#                                 START
#************************************************************************
# module load scitools/default-current # for Python 3
# python RewriteStnListPostPHA.py
#
# USE python2.7
# python2.7 RewriteStnListPostPHA.py
#
# For debugging mode:
# ipython
# %pdb
# %run RewriteStnListPostPHA.py
#
# REQUIRES
# 
#************************************************************************
# START
#************************************************************************
# Imports
import sys, os
import struct
import pdb
import numpy as np
from subprocess import call

# Variables
# Set up initial run choices
styr       = 1973
edyr       = 2019

# Dataset version if HardWire = 1
versiondots    = '4.2.0.2019f'
version    = 'v420_2019f'

if (HardWire == 0):
    
    #' Read in the config file to get all of the info
    with open('F1_HadISDHBuildConfig.txt') as f:
        
	ConfigDict = dict(x.rstrip().split('=', 1) for x in f)
	versiondots = ConfigDict['VersionDots']
	hadisdversiondots = ConfigDict['HadISDVersionDots']
	styr = ConfigDict['StartYear']
	edyr = ConfigDict['EndYear']
    

# Set up file locations
updateyear = str(edyr)[2:4]
workingdir = '/scratch/hadkw/UPDATE20'+updateyear
phadir     = workingdir+'/pha52jgo/data/hadisdh/'

varlist = ['dpd','t','q','e','rh','tw','td']

# PHA Run string - CHECK THE DATETIME STRING DPD, T, Q, E, RH, TW, TD
# from phav52jgo/data/hadisdh/
# > ls /out<var>put/P*
# This now searches for the string for each variable and appends to a list
PHAID = []
for var in varlist:
    
    # This should pull out the PHA... filename as a string
    WholeName = glob.glob(phadir+var+"/output/PHAv52j*")[0].split('/')[2]
    PHAID.append(WholeName[22:32])
    
# Should create something like this - number strings are YYMMDDHHMM and may differ if PHA is run at different times for each var
#PHAID = ['2002171753','2002171753','2002171753','2002171753','2002171753','2002171753','2002171753']

# In Filepaths - CHECK THE NUMBER OF input_not_stnlist IS CORRECT
# from PHA2015/phav52jgo/data/hadisdh/
# > ls <var>/corr/m*
# Each year there may be 1, 2 or more input_not_stnlist files and I'm not sure why
# glob.glob is a useful way of finding these
BadFiles = []
for var in varlist:

    # This appends a list to the BadFiles list so we have lists of lists in varlist order
    BadFiles.append(glob.glob(phadir+var+"/corr/meta*input_not_stnlist"))
# Should look something like this
BadFiles   = [[phadir+'dpd/corr/meta.dpd.tavg.r00.'+PHAID[0]+'.1.input_not_stnlist',
               phadir+'dpd/corr/meta.dpd.tavg.r00.'+PHAID[0]+'.2.input_not_stnlist'],
              [phadir+'t/corr/meta.t.tavg.r00.'+PHAID[1]+'.1.input_not_stnlist',
	      phadir+'t/corr/meta.t.tavg.r00.'+PHAID[1]+'.2.input_not_stnlist'],
              [phadir+'q/corr/meta.q.tavg.r00.'+PHAID[2]+'.1.input_not_stnlist'],
              [phadir+'e/corr/meta.e.tavg.r00.'+PHAID[3]+'.1.input_not_stnlist'],
              [phadir+'rh/corr/meta.rh.tavg.r00.'+PHAID[4]+'.1.input_not_stnlist',
               phadir+'rh/corr/meta.rh.tavg.r00.'+PHAID[4]+'.2.input_not_stnlist'],
	      [phadir+'tw/corr/meta.tw.tavg.r00.'+PHAID[5]+'.1.input_not_stnlist'],
              [phadir+'td/corr/meta.td.tavg.r00.'+PHAID[6]+'.1.input_not_stnlist']]#,
              # phadir+'td/corr/meta.td.tavg.r00.'+PHAID[6]+'.2.input_not_stnlist']]

InAll       = workingdir+'/LISTS_DOCS/goodforHadISDH.'+versiondots+'.txt' 

# Out Filepaths
OutIDPHAall = workingdir+'/LISTS_DOCS/goodforHadISDH.'+versiondots+'_IDPHAall.txt'
OutTdBad    = phadir+'td/corr/badlist.txt'

# Variables
MyFullTypes         = ("|U6","|U5","float","float","float","|U4","|U30","|U7","int")
#MyFullTypes         = ("|S6","|S5","float","float","float","|S4","|S30","|S7","int")
MyFullDelimiters    = [6,5,8,10,7,4,30,7,5]
MyBadTypes          = ("|U6","|U5","float","float","int","|U4","|U30")
#MyBadTypes          = ("|S6","|S5","float","float","int","|S4","|S30")
MyBadDelimiters     = [6,5,7,10,13,4,30]
nBADstations        = 0	# defined after reading in station list
BADStationListWMO   = []	# nstations list filled after reading in station list
BADStationListWBAN  = []	# nstations list filled after reading in station list
nALLBADstations        = 0	# defined after reading in station list
ALLBADStationListWMO   = []	# nstations list filled after reading in station list
ALLBADStationListWBAN  = []	# nstations list filled after reading in station list
nstations           = 0	# defined after reading in station list
StationListWMO      = []	# nstations list filled after reading in station list
StationListWBAN     = []	# nstations list filled after reading in station list
StationListLat      = []
StationListLon      = []
StationListElev     = []
StationListCID      = []
StationListName     = []
StationListMonths   = []
nGOODstations           = 0	# defined after reading in station list
GOODStationListWMO      = []	# nstations list filled after reading in station list
GOODStationListWBAN     = []	# nstations list filled after reading in station list
GOODStationListLat      = []
GOODStationListLon      = []
GOODStationListElev     = []
GOODStationListCID      = []
GOODStationListName     = []
GOODStationListMonths   = []

#*************************************************************************
# SUBROUTINES
#*************************************************************************
# READTEXT
def ReadText(FileName,typee,delimee):
    ''' Use numpy genfromtxt reading to read in all rows from a complex array '''
    ''' Need to specify format as it is complex '''
    ''' outputs an array of tuples that in turn need to be subscripted by their names defaults f0...f8 '''

    return np.genfromtxt(FileName, dtype=typee,delimiter=delimee,encoding='latin-1') # ReadData
    
#***************************************************************************
# WRITETEXT
def WriteText(TheFile,TheStationID,TheLat,TheLon,TheElev,TheCID,TheName,TheMonths):
    ''' Write out the station WMO and WBAN and Location to file   '''
    ''' File is either list of good stations or bad stations '''
    ''' Bad stations are cases where there are fewer than 7 neighbours '''
    ''' This is based on listings compiled for this variable during direct PHA '''
    ''' First difference series of the monthly anomalies must correlate > 0.1 '''

    filee = open(TheFile,'w')
    
    for ll in range(len(TheStationID)):
        filee.write('%11s%8.4f%10.4f%7.1f%4s%30s%7s%5d\n' % (TheStationID[ll],TheLat[ll],TheLon[ll],
                TheElev[ll],TheCID[ll],TheName[ll],'MONTHS:',TheMonths[ll])) # \n'
    
    filee.close()

    return #WriteText

#*************************************************************************
# MAIN
#*************************************************************************
# Open all station list
RawData         = ReadText(InAll,MyFullTypes,MyFullDelimiters)
StationListWMO    = np.array(RawData['f0'])
StationListWBAN   = np.array(RawData['f1'])
StationListLat    = np.array(RawData['f2'])
StationListLon    = np.array(RawData['f3'])
StationListElev   = np.array(RawData['f4'])
StationListCID    = np.array(RawData['f5'])
StationListName   = np.array(RawData['f6'])
StationListMonths = np.array(RawData['f8']) # f7 = MONTHS:
nstations         = len(StationListWMO)

# Start loop through the variables - DPD, T, q, e, RH, Tw, Td
VarLoop       = ['DPD','T','q','e','RH','Tw','Td']
LittleVarLoop = ['dpd','t','q','e','rh','tw','td']

for vv, var in enumerate(VarLoop): # vv is a number, var is the element of VarLoop
    print(vv,var)

    #if (var != 'Td'):
    #    continue
    
    # Loop through each of the input_not_station files, read in and concatenate to the BADStationList...
    for ff, filee in enumerate(BadFiles[vv]):
        #print(ff,filee)

        RawData         = ReadText(filee,MyBadTypes,MyBadDelimiters)
        BADStationListWMO    = np.append(BADStationListWMO,np.array(RawData['f0']))
        BADStationListWBAN   = np.append(BADStationListWBAN,np.array(RawData['f1']))
        
    nBADstations         = len(BADStationListWMO)
    print('BAD Stations for: ',var,nBADstations)
    
    # If var is DPD or T then add the BAD lists to ALLBAD - then sort for unique values
    if var == 'DPD' or var == 'T':
        ALLBADStationListWMO = np.append(ALLBADStationListWMO,BADStationListWMO)
        ALLBADStationListWBAN = np.append(ALLBADStationListWBAN,BADStationListWBAN)
	#pdb.set_trace()
	
	# Cut down to only unique values
        if var == 'T':
            UniqVals, UniqIndex   = np.unique(ALLBADStationListWMO,return_index=True)
            ALLBADStationListWMO  = ALLBADStationListWMO[UniqIndex]    
            ALLBADStationListWBAN = ALLBADStationListWBAN[UniqIndex]   
            nALLBADstations = len(UniqVals) 
            print('BAD DPD and T uniq stations: ',nALLBADstations)
	    
	    # Remove the ALLBAD stations from the list - find bad station locs and delete them
            BadLocs               = StationListWMO.searchsorted(ALLBADStationListWMO)
            GOODStationListWMO    = np.delete(StationListWMO,BadLocs)
            GOODStationListWBAN   = np.delete(StationListWBAN,BadLocs)
            GOODStationListLat    = np.delete(StationListLat,BadLocs)
            GOODStationListLon    = np.delete(StationListLon,BadLocs)
            GOODStationListElev   = np.delete(StationListElev,BadLocs)
            GOODStationListCID    = np.delete(StationListCID,BadLocs)
            GOODStationListName   = np.delete(StationListName,BadLocs)
            GOODStationListMonths = np.delete(StationListMonths,BadLocs)
            nGOODstations         = len(GOODStationListWMO) 
            print('GOOD DPD and T uniq stations: ',nGOODstations)
	
	    # Concatenate WMO and WBAN
            GOODStationListID = np.array(["%s%s" % i for i in zip(GOODStationListWMO,GOODStationListWBAN)])
	
	    # Write out the new Good list to file (IDPHAall)
            WriteText(OutIDPHAall,
	              GOODStationListID,
		      GOODStationListLat,
		      GOODStationListLon,
		      GOODStationListElev,
		      GOODStationListCID,
		      GOODStationListName,
		      GOODStationListMonths)
	    
	    # Clear the Good list of stations 
            nGOODstations           = 0	# defined after reading in station list
            GOODStationListWMO      = []	# nstations list filled after reading in station list
            GOODStationListWBAN     = []	# nstations list filled after reading in station list
            GOODStationListLat      = []
            GOODStationListLon      = []
            GOODStationListElev     = []
            GOODStationListCID      = []
            GOODStationListName     = []
            GOODStationListMonths   = []
    
    # Make a Good list of stations with the BAD stations removed
    BadLocs               = StationListWMO.searchsorted(BADStationListWMO)
    GOODStationListWMO    = np.delete(StationListWMO,BadLocs)
    GOODStationListWBAN   = np.delete(StationListWBAN,BadLocs)
    GOODStationListLat    = np.delete(StationListLat,BadLocs)
    GOODStationListLon    = np.delete(StationListLon,BadLocs)
    GOODStationListElev   = np.delete(StationListElev,BadLocs)
    GOODStationListCID    = np.delete(StationListCID,BadLocs)
    GOODStationListName   = np.delete(StationListName,BadLocs)
    GOODStationListMonths = np.delete(StationListMonths,BadLocs)
    nGOODstations         = len(GOODStationListWMO) 
    print('GOOD '+var+' uniq stations: ',nGOODstations)

    # Concatenate WMO and WBAN
    GOODStationListID = np.array(["%s%s" % i for i in zip(GOODStationListWMO,GOODStationListWBAN)])
	
    # Write out the good list to file
    OutFile = workingdir+'/LISTS_DOCS/goodforHadISDH.'+version+'_PHA'+LittleVarLoop[vv]+'_JAN'+nowyear+'.txt'
    WriteText(OutFile,
	      GOODStationListID,
 	      GOODStationListLat,
	      GOODStationListLon,
	      GOODStationListElev,
	      GOODStationListCID,
	      GOODStationListName,
	      GOODStationListMonths)
    
    # Clear the BAD lists to start on the next variable
    # But if var = Td then first copy the list to 73<yy>td/corr/badlist.txt
    if var == 'Td':
        f = open(OutTdBad,'w')
        for bb in range(nBADstations):
            f.write('%6s\n' % BADStationListWMO[bb])
        f.close()
    
    nBADstations        = 0	# defined after reading in station list
    BADStationListWMO   = []	# nstations list filled after reading in station list
    BADStationListWBAN  = []	# nstations list filled after reading in station list

    # Clear the GOOD lists to start on the next variable
    nGOODstations           = 0	# defined after reading in station list
    GOODStationListWMO      = []	# nstations list filled after reading in station list
    GOODStationListWBAN     = []	# nstations list filled after reading in station list
    GOODStationListLat      = []
    GOODStationListLon      = []
    GOODStationListElev     = []
    GOODStationListCID      = []
    GOODStationListName     = []
    GOODStationListMonths   = []
    
    # Copy corr files to corr.log within each directory
    InCorrFile  = phadir+LittleVarLoop[vv]+'/corr/corr.73'+updateyear+LittleVarLoop[vv]+'.tavg.r00.'+PHAID[vv]
    OutCorrFile = phadir+LittleVarLoop[vv]+'/corr/corr.log'
    call(['cp',InCorrFile,OutCorrFile])
    #pdb.set_trace()

    # Unzip PHA output file, grab all Adj text and spit out to file, copy also to LISTS_DOCS
    InAdjFile   = phadir+LittleVarLoop[vv]+'/output/PHAv52j.FAST.MLY.TEST.'+PHAID[vv]+'.tavg.73'+updateyear+LittleVarLoop[vv]+'.r00.out' # this is a .gz file
    OutAdjFile  = phadir+LittleVarLoop[vv]+'/output/HadISDH.land'+var+'.'+version+'_PHA_JAN'+nowyear+'.log'
    ListAdjFile = workingdir+'/LISTS_DOCS/HadISDH.land'+var+'.'+version+'_PHA_JAN'+nowyear+'.log'	
    call(['gunzip',InAdjFile+'.gz'])
    moo = open(OutAdjFile,'w')
    call(['grep', '-a', 'Adj write:',InAdjFile],stdout=moo)
    call(['gzip',InAdjFile])
    call(['cp',OutAdjFile,ListAdjFile])
    #pdb.set_trace()
