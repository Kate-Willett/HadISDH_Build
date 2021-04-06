#!/usr/local/sci/bin/python
# PYTHON3
# 
# Author: Kate Willett
# Created: 31 January 2017
# Last update: 25 January 2021
# Location: /home/h04/hadkw/HadISDH_Code/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# This code: 
#   - takes the stations with large adjustments:
#	 > 5.0 deg from T (IDPHAMG)
#	 > 5.0 deg from Td (PHADPD) 
#	 > 3 g/kg from q (IDPHA)
# 	 >15 %rh from RH (IDPHA)
#	and saves to file
#   - uses the list of stations to remove from the key lists (IDPHA T, Tw, q, e, RH, PHA DPD and PHADPD Td
#	 because they have very large (as above) adjustments detected and applied to T, Td, RH and q
#   - copies the old goodstations... files to goodstations...KeptLarge.txt
#   - rewrites out the goodstations...txt with the bad stations removed
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# inbuilt:
# import numpy as np
# import sys, os
# import struct
# import pdb
# from subprocess import call # for calling unix commands
#
# -----------------------
# DATA
# -----------------------
# Working Dir is either:
# /data/users/hadkw/WORKING_HADISDH/UPDATE<YYYY>/
# /scratch/hadkw/UPDATE<YYYY>/ 
#
# List of largest adjustments for T (IDPHAMG)
# LARGETLIST = '/LISTS_DOCS/Largest_Adjs_landT.<version>_IDPHAMG.txt
# List of largest adjustments for Td (PHADPD)
# LARGETDLIST = '/LISTS_DOCS/Largest_Adjs_landTd.<version>_PHADPD.txt
# List of largest adjustments for q (IDPHA)
# LARGEQLIST = '/LISTS_DOCS/Largest_Adjs_landq.<version>_IDPHA.txt
# List of largest adjustments for RH (IDPHA)
# LARGERHLIST = '/LISTS_DOCS/Largest_Adjs_landRH.<version>_IDPHA.txt
#
# Station lists of all good stations for each variables (IDPHA, PHAdpd and PHADPDtd)
# STATLIST='/LISTS_DOCS/goodforHadISDH.'+version+'_*'.txt'	# removed all 'bad' DPD and T stations (6)
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# module load scitools/default-current
# python F11_UpdateGoodLists_LargeAdjRemovals.py
# 
# -----------------------
# OUTPUT
# -----------------------
# Working Dir is either:
# /data/users/hadkw/WORKING_HADISDH/UPDATE<YYYY>/
# /scratch/hadkw/UPDATE<YYYY>/ 
#
# Station list of those to remove
# BADSLIST = '/LISTS_DOCS/HadISDH.<version>_LargeAdj_removals.txt
# Copy of original goodstations... lists to goodstations...KeptLarge.txt
# New goodstations...txt with the bad stations removed
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
# 
# Version 4 (25 January 2021)
# ---------
#  
# Enhancements
#  
# Changes
# Now part of HadiSDH code suite running on scratch and from spice
#  
# Bug fixes
#

#
# Version 3 (23 February 2020)
# ---------
#  
# Enhancements
#  
# Changes
# This code is now python 3 from pyrhon 2.7
#  
# Bug fixes
#
# Version 2 (7 February 2018)
# ---------
#  
# Enhancements
#  
# Changes
# This code now creates the list of stations with large adjustments to remove from all station lists
# rather than it having to be created manually beforehand:
# /LISTS_DOCS/HadISDH.<version>_LargeAdj_removals_JAN<yyyy>.txt
# This lists all unique stations where adjustments in T and Td > 5deg, in q > 3g/kg and in RH > 15%rh
#  
# Bug fixes
#
# Version 1 (31 January 2017)
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
# Set up python imports
import numpy as np
import sys, os
import struct
import pdb
from subprocess import call, check_output

# Start and end years if HardWire = 1
styear = 1973
edyear = 2019

# Dataset version if HardWire = 1
versiondots = '4.2.0.2019f'

# HARDWIRED SET UP!!!
# If HardWire = 1 then program reads from the above run choices
# If HardWire = 0 then program reads in from F1_HadISDHBuildConfig.txt
HardWire = 0

if (HardWire == 0):
    
    #' Read in the config file to get all of the info
    with open('F1_HadISDHBuildConfig.txt') as f:
        
        ConfigDict = dict(x.rstrip().split('=', 1) for x in f)
    
    versiondots = ConfigDict['VersionDots']
    styear = ConfigDict['StartYear']
    edyear = ConfigDict['EndYear']

# ConfigDict held in memory to probide global attribute text later

# NOT CODED THIS FUNCTIONALITY YET
## Are we working with homogenised actuals (True) or anomalies (False)?
#Actuals = True

# Set up directories locations
updateyy  = str(edyear)[2:4]
updateyyyy  = str(edyear)
workingdir  = '/scratch/hadkw/UPDATE'+updateyyyy
#workingdir  = '/data/users/hadkw/WORKING_HADISDH/UPDATE'+updateyyyy

# List of stations to remove
LARGETLIST  = workingdir+'/LISTS_DOCS/Largest_Adjs_landT.'+versiondots+'_IDPHAMG.txt'
LARGETDLIST = workingdir+'/LISTS_DOCS/Largest_Adjs_landTd.'+versiondots+'_PHADPD.txt'
LARGEQLIST = workingdir+'/LISTS_DOCS/Largest_Adjs_landq.'+versiondots+'_IDPHA.txt'
LARGERHLIST = workingdir+'/LISTS_DOCS/Largest_Adjs_landRH.'+versiondots+'_IDPHA.txt'
BADSLIST    = workingdir+'/LISTS_DOCS/HadISDH.'+versiondots+'_LargeAdj_removals.txt'
GOODLISTt   = workingdir+'/LISTS_DOCS/goodforHadISDH.'+versiondots+'_IDPHAt'
GOODLISTdpd = workingdir+'/LISTS_DOCS/goodforHadISDH.'+versiondots+'_PHAdpd'
GOODLISTtd  = workingdir+'/LISTS_DOCS/goodforHadISDH.'+versiondots+'_PHADPDtd'
GOODLISTq   = workingdir+'/LISTS_DOCS/goodforHadISDH.'+versiondots+'_IDPHAq'
GOODLISTrh  = workingdir+'/LISTS_DOCS/goodforHadISDH.'+versiondots+'_IDPHArh'
GOODLISTe   = workingdir+'/LISTS_DOCS/goodforHadISDH.'+versiondots+'_IDPHAe'
GOODLISTtw  = workingdir+'/LISTS_DOCS/goodforHadISDH.'+versiondots+'_IDPHAtw'

# File for output stats of number of large adjustment removals and resulting station counts
OUTPUTLOG = workingdir+'/LISTS_DOCS/OutputLogFile'+versiondots+'.txt'

nstations       = 0	# defined after reading in station list
StationListWMO  = []	# nstations list filled after reading in station list
StationListWBAN = []	# nstations list filled after reading in station list
nLadjs          = 0	# defined after reading in station list
LargeListWMO    = []	# nstations list filled after reading in station list
LargeListWBAN   = []	# nstations list filled after reading in station list
LargeListadj    = []	# nstations list filled after reading in station list
LargeListBLURB  = []	# nstations list filled after reading in station list
TmpLargeListWMO    = []	# nstations list filled after reading in station list
TmpLargeListWBAN   = []	# nstations list filled after reading in station list
TmpLargeListadj    = []	# nstations list filled after reading in station list
TmpLargeListBLURB  = []	# nstations list filled after reading in station list

#************************************************************************
# Subroutines
#************************************************************************
# READDATA
def ReadData(FileName,typee,delimee):
    ''' Use numpy genfromtxt reading to read in all rows from a complex array '''
    ''' Need to specify format as it is complex '''
    ''' outputs an array of tuples that in turn need to be subscripted by their names defaults f0...f8 '''

    return np.genfromtxt(FileName, dtype=typee,delimiter=delimee,encoding='latin-1') # ReadData

#***********************************************************************
# SIFTLIST
def SiftList(FileName,BadWMOWBANs):
    ''' Open and read list of good stations (now KeptLarge.txt) for variable '''
    ''' If good station doesn't match up with anything '''
    ''' in the bad station list then write out to new file '''

    MyTypes         = ("|U6","|U5","float","float","float","|U4","|U30","|U14")
#    MyTypes         = ("|S6","|S5","float","float","float","|S4","|S30","|S14")
    MyDelimiters    = [6,5,8,10,7,4,30,14]
    RawData         = ReadData(FileName+'_KeptLarge.txt',MyTypes,MyDelimiters)
    StationListWMO  = np.array(RawData['f0'])
    StationListWBAN = np.array(RawData['f1'])
    StationListLat  = np.array(RawData['f2'])
    StationListLon  = np.array(RawData['f3'])
    StationListElev = np.array(RawData['f4'])
    StationListCID  = np.array(RawData['f5'])
    StationListName = np.array(RawData['f6'])
    Mush            = np.array(RawData['f7'])
    nstations       = len(StationListWMO)
    
#    pdb.set_trace()
    
    # loop through station by station
    for st in range(nstations):

    # Test to see if stationWMO and WBAN match anything in the BadWMOs/BadWBANS
        if (len(np.where(BadWMOWBANs == StationListWMO[st]+StationListWBAN[st])[0]) == 0):
    
    # if no match then list in good station list
            ListStation(FileName+'.txt',StationListWMO[st]+StationListWBAN[st],StationListLat[st],
	                StationListLon[st],StationListElev[st],StationListCID[st],StationListName[st],Mush[st])

    # end loop of stations
    return

#***********************************************************************
# LISTSTATION
def ListStation(TheFile,TheStationID,TheLat,TheLon,TheElev,TheCID,TheName,TheMush):
    ''' Write out the station WMO and WBAN and Location to file   '''
    ''' File is either list of good stations or bad stations '''
    ''' Bad stations are cases where there are fewer than 7 neighbours '''
    ''' This is based on listings compiled for this variable during direct PHA '''
    ''' First difference series of the monthly anomalies must correlate > 0.1 '''

    filee = open(TheFile,'a+')
    
    filee.write('%11s%8.4f%10.4f%7.1f%4s%30s%14s' % (TheStationID,TheLat,TheLon,
                TheElev,TheCID,TheName,TheMush)) # \n'
    
    filee.close()

    return #ListStation

#***********************************************************************
# WRITETEXT # no blurb
def WriteText(TheFile,TheStationWMO,TheStationWBAN):
    ''' Write out the station WMO and WBAN and Blurb to file   '''

    filee = open(TheFile,'w')
    
    for ll in range(len(TheStationWMO)):
    
        filee.write('%6s%5s\n' % (TheStationWMO[ll],TheStationWBAN[ll])) # \n'
    
    filee.close()

    return #WriteText

#***********************************************************************
# WRITETEXTBLURB # blurb to cover any notes (up to 60 char) on large adj for WMO ID
def WriteTextBlurb(TheFile,TheStationWMO,TheStationWBAN,TheBlurb):
    ''' Write out the station WMO and WBAN and Blurb to file   '''

    filee = open(TheFile,'w')
    
    for ll in range(len(TheStationWMO)):
    
        filee.write('%6s%5s%60s\n' % (TheStationWMO[ll],TheStationWBAN[ll],TheBlurb[ll])) # \n'
    
    filee.close()

    return #WriteText

#***********************************************************************
# MAIN PROGRAM
#***********************************************************************
# Read in the largest adj lists, merge, save only unique stations, output to file
MyTypes            = ("|U6","|U5","float")
#MyTypes            = ("|U6","|U5","float","|U60")
MyDelimiters       = [6,5,8]
#MyDelimiters       = [6,5,8,60]

# read in bad station list for T
RawData            = ReadData(LARGETLIST,MyTypes,MyDelimiters)
TmpLargeListWMO       = np.array(RawData['f0'])
TmpLargeListWBAN      = np.array(RawData['f1'])
TmpLargeListadj       = np.array(RawData['f2'])
#TmpLargeListBLURB     = np.array(RawData['f3'])

# Keep only those this adjustment values greater than 5 deg
LargeMask         = np.where(np.abs(TmpLargeListadj) > 5.0)[0]
TmpLargeListWMO   = TmpLargeListWMO[LargeMask]
TmpLargeListWBAN  = TmpLargeListWBAN[LargeMask]
#TmpLargeListBLURB = TmpLargeListBLURB[LargeMask]

# Log the number of larges for T
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('T_Larger_than_5_deg=',len(TmpLargeListWMO)))
filee.close()

LargeListWMO       = np.append(LargeListWMO,TmpLargeListWMO)
LargeListWBAN      = np.append(LargeListWBAN,TmpLargeListWBAN)
#LargeListBLURB     = np.append(LargeListBLURB,TmpLargeListBLURB)

TmpLargeListWMO    = []	# nstations list filled after reading in station list
TmpLargeListWBAN   = []	# nstations list filled after reading in station list
TmpLargeListadj    = []	# nstations list filled after reading in station list
#TmpLargeListBLURB  = []	# nstations list filled after reading in station list

# read in bad station list for Td
RawData               = ReadData(LARGETDLIST,MyTypes,MyDelimiters)
TmpLargeListWMO       = np.array(RawData['f0'])
TmpLargeListWBAN      = np.array(RawData['f1'])
TmpLargeListadj       = np.array(RawData['f2'])
#TmpLargeListBLURB     = np.array(RawData['f3'])
#TmpLargeListWMO       = np.append(TmpLargeListWMO,np.array(RawData['f0']))
#TmpLargeListWBAN      = np.append(TmpLargeListWBAN,np.array(RawData['f1']))
#TmpLargeListadj       = np.append(TmpLargeListadj,np.array(RawData['f2']))
##TmpLargeListBLURB     = np.append(TmpLargeListBLURB,np.array(RawData['f3']))

# Keep only those this adjustment values greater than 5 deg
LargeMask         = np.where(np.abs(TmpLargeListadj) > 5.0)[0]
TmpLargeListWMO   = TmpLargeListWMO[LargeMask]
TmpLargeListWBAN  = TmpLargeListWBAN[LargeMask]
#TmpLargeListBLURB = TmpLargeListBLURB[LargeMask]

# Log the number of larges for Td
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('Td_Larger_than_5_deg=',len(TmpLargeListWMO)))
filee.close()

LargeListWMO       = np.append(LargeListWMO,TmpLargeListWMO)
LargeListWBAN      = np.append(LargeListWBAN,TmpLargeListWBAN)
#LargeListBLURB     = np.append(LargeListBLURB,TmpLargeListBLURB)

TmpLargeListWMO    = []	# nstations list filled after reading in station list
TmpLargeListWBAN   = []	# nstations list filled after reading in station list
TmpLargeListadj    = []	# nstations list filled after reading in station list
#TmpLargeListBLURB  = []	# nstations list filled after reading in station list

# read in bad station list for q
RawData               = ReadData(LARGEQLIST,MyTypes,MyDelimiters)
TmpLargeListWMO       = np.array(RawData['f0'])
TmpLargeListWBAN      = np.array(RawData['f1'])
TmpLargeListadj       = np.array(RawData['f2'])
#TmpLargeListBLURB     = np.array(RawData['f3'])

# Keep only those this adjustment values greater than 3 g/kg
LargeMask         = np.where(np.abs(TmpLargeListadj) > 3.0)[0]
TmpLargeListWMO   = TmpLargeListWMO[LargeMask]
TmpLargeListWBAN  = TmpLargeListWBAN[LargeMask]
#TmpLargeListBLURB = TmpLargeListBLURB[LargeMask]

# Log the number of larges for q
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('q_Larger_than_3_g/kg=',len(TmpLargeListWMO)))
filee.close()

LargeListWMO       = np.append(LargeListWMO,TmpLargeListWMO)
LargeListWBAN      = np.append(LargeListWBAN,TmpLargeListWBAN)
#LargeListBLURB     = np.append(LargeListBLURB,TmpLargeListBLURB)

TmpLargeListWMO    = []	# nstations list filled after reading in station list
TmpLargeListWBAN   = []	# nstations list filled after reading in station list
TmpLargeListadj    = []	# nstations list filled after reading in station list
#TmpLargeListBLURB  = []	# nstations list filled after reading in station list

# read in bad station list for RH
RawData               = ReadData(LARGERHLIST,MyTypes,MyDelimiters)
TmpLargeListWMO       = np.array(RawData['f0'])
TmpLargeListWBAN      = np.array(RawData['f1'])
TmpLargeListadj       = np.array(RawData['f2'])
#TmpLargeListBLURB     = np.array(RawData['f3'])

# Keep only those this adjustment values greater than 15 %rh
LargeMask         = np.where(np.abs(TmpLargeListadj) > 15.0)[0]
TmpLargeListWMO   = TmpLargeListWMO[LargeMask]
TmpLargeListWBAN  = TmpLargeListWBAN[LargeMask]
#TmpLargeListBLURB = TmpLargeListBLURB[LargeMask]

# Log the number of larges for RH
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('RH_Larger_than_15_%rh=',len(TmpLargeListWMO)))
filee.close()

LargeListWMO       = np.append(LargeListWMO,TmpLargeListWMO)
LargeListWBAN      = np.append(LargeListWBAN,TmpLargeListWBAN)
#LargeListBLURB     = np.append(LargeListBLURB,TmpLargeListBLURB)

TmpLargeListWMO    = []	# nstations list filled after reading in station list
TmpLargeListWBAN   = []	# nstations list filled after reading in station list
TmpLargeListadj    = []	# nstations list filled after reading in station list
#TmpLargeListBLURB  = []	# nstations list filled after reading in station list

# Keep only uniq stations
UniqVals, UniqIndex   = np.unique(LargeListWMO,return_index=True)
LargeListWMO          = LargeListWMO[UniqIndex]    
LargeListWBAN         = LargeListWBAN[UniqIndex]   
#LargeListBLURB        = LargeListBLURB[UniqIndex]   
nLadjs                = len(UniqVals) 
print('Large Adj T, Td, q and RH uniq stations: ',nLadjs)

# Log the number of unique larges
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('Uniq_Larges_removed=',len(LargeListWMO)))
filee.close()

# Save the list of large T and Td (>5) and q adn RH to file
WriteText(BADSLIST,LargeListWMO,LargeListWBAN)
#WriteTextBlurb(BADSLIST,LargeListWMO,LargeListWBAN,LargeListBLURB)

# MOVE original station lists to goodstations*KeptLarge.txt
print(GOODLISTt+'.txt')
#call('ls')
#call(['ls',GOODLISTt+'.txt'])
#call(['wc', '-l', GOODLISTt+'.txt'])
call(['mv', GOODLISTt+'.txt', GOODLISTt+'_KeptLarge.txt'])
#pdb.set_trace()
call(['mv', GOODLISTdpd+'.txt', GOODLISTdpd+'_KeptLarge.txt'])
call(['mv', GOODLISTtd+'.txt', GOODLISTtd+'_KeptLarge.txt'])
call(['mv', GOODLISTq+'.txt', GOODLISTq+'_KeptLarge.txt'])
call(['mv', GOODLISTrh+'.txt', GOODLISTrh+'_KeptLarge.txt'])
call(['mv', GOODLISTe+'.txt', GOODLISTe+'_KeptLarge.txt'])
call(['mv', GOODLISTtw+'.txt', GOODLISTtw+'_KeptLarge.txt'])

# Concatenate the WMO and WBANS elementwise
BADWMOWBAN = np.array(["%s%s" % i for i in zip(LargeListWMO,LargeListWBAN)])

# read in good station lists for each variable and then output minus bads
SiftList(GOODLISTt,BADWMOWBAN)
CountG = int(check_output(["wc","-l",GOODLISTt+'.txt']).decode('utf-8').split()[0])
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('T_Station_Count_After_Large_Removals=',CountG))
filee.close()

#pdb.set_trace()
SiftList(GOODLISTdpd,BADWMOWBAN)
CountG = int(check_output(["wc","-l",GOODLISTdpd+'.txt']).decode('utf-8').split()[0])
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('DPD_Station_Count_After_Large_Removals=',CountG))
filee.close()

SiftList(GOODLISTtd,BADWMOWBAN)
CountG = int(check_output(["wc","-l",GOODLISTtd+'.txt']).decode('utf-8').split()[0])
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('Td_Station_Count_After_Large_Removals=',CountG))
filee.close()

SiftList(GOODLISTq,BADWMOWBAN)
CountG = int(check_output(["wc","-l",GOODLISTq+'.txt']).decode('utf-8').split()[0])
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('q_Station_Count_After_Large_Removals=',CountG))
filee.close()

SiftList(GOODLISTrh,BADWMOWBAN)
CountG = int(check_output(["wc","-l",GOODLISTrh+'.txt']).decode('utf-8').split()[0])
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('RH_Station_Count_After_Large_Removals=',CountG))
filee.close()

SiftList(GOODLISTe,BADWMOWBAN)
CountG = int(check_output(["wc","-l",GOODLISTe+'.txt']).decode('utf-8').split()[0])
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('e_Station_Count_After_Large_Removals=',CountG))
filee.close()

SiftList(GOODLISTtw,BADWMOWBAN)
CountG = int(check_output(["wc","-l",GOODLISTtw+'.txt']).decode('utf-8').split()[0])
filee = open(OUTPUTLOG,'a+')
filee.write('%s%i\n' % ('Tw_Station_Count_After_Large_Removals=',CountG))
filee.close()

print("And, we are done!")
