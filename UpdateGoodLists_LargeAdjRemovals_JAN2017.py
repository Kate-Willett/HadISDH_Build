#!/usr/local/sci/bin/python
# PYTHON2.7
# 
# Author: Kate Willett
# Created: 31 January 2017
# Last update: 31 January 2017
# Location: /data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# This code: 
#   - reads in a list of stations to remove from the key lists because they have very large (> 5deg) adjustments
#      detected and applied to T and Td
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
# Station list of those to remove
# BADSLIST = '/data/local/hadkw/HADCRUH2/UPDATE2016/LISTS_DOCS/HadISDH.3.0.0.2016p_LargeAdjT_Td_removals_JAN2017.txt
#
# Station lists of all good stations for each variables (IDPHA, PHAdpd and PHADPDtd)
# STATLIST='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_*_'+nowmon+nowyear+'.txt'	# removed all 'bad' DPD and T stations (6)
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# Make sure there is a text file listing the stations to be removed e.g.:
# BADSLIST = '/data/local/hadkw/HADCRUH2/UPDATE2016/LISTS_DOCS/HadISDH.3.0.0.2016p_LargeAdjT_Td_removals_JAN2017.txt
# 
# python2.7 UpdateGoodLists_LargeAdjRemovals_JAN2017.py
# 
# -----------------------
# OUTPUT
# -----------------------
# Copy of original goodstations... lists to goodstations...KeptLarge.txt
# New goodstations...txt with the bad stations removed
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
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
# USE python2.7
# python2.7 UpdateGoodLists_LargeAdjRemovals_JAN2017.py
#
#************************************************************************
# Set up python imports
import numpy as np
import sys, os
import struct
import pdb
from subprocess import call

# Set up initial run choices
# End year
edyr       = 2016

# Working file month and year
nowmon     = 'JAN'
nowyear    = '2017'

# Dataset version
version    = '3.0.0.2016p'

# Set up file locations
updateyear = str(edyr)[2:4]
workingdir = '/data/local/hadkw/HADCRUH2/UPDATE20'+updateyear

# List of stations to remove
BADSLIST    = workingdir+'/LISTS_DOCS/HadISDH.'+version+'_LargeAdjT_Td_removals_'+nowmon+nowyear+'.txt'
GOODLISTt   = workingdir+'/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAt_'+nowmon+nowyear
GOODLISTdpd = workingdir+'/LISTS_DOCS/goodforHadISDH.'+version+'_PHAdpd_'+nowmon+nowyear
GOODLISTtd  = workingdir+'/LISTS_DOCS/goodforHadISDH.'+version+'_PHADPDtd_'+nowmon+nowyear
GOODLISTq   = workingdir+'/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAq_'+nowmon+nowyear
GOODLISTrh  = workingdir+'/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHArh_'+nowmon+nowyear
GOODLISTe   = workingdir+'/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAe_'+nowmon+nowyear
GOODLISTtw  = workingdir+'/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAtw_'+nowmon+nowyear

nBADstations       = 0	# defined after reading in station list
BADStationListWMO  = []	# nstations list filled after reading in station list
BADStationListWBAN = []	# nstations list filled after reading in station list
nstations       = 0	# defined after reading in station list
StationListWMO  = []	# nstations list filled after reading in station list
StationListWBAN = []	# nstations list filled after reading in station list

#************************************************************************
# Subroutines
#************************************************************************
# READDATA
def ReadData(FileName,typee,delimee):
    ''' Use numpy genfromtxt reading to read in all rows from a complex array '''
    ''' Need to specify format as it is complex '''
    ''' outputs an array of tuples that in turn need to be subscripted by their names defaults f0...f8 '''

    return np.genfromtxt(FileName, dtype=typee,delimiter=delimee) # ReadData

#***********************************************************************
# SIFTLIST
def SiftList(FileName,BadWMOWBANs):
    ''' Open and read list of good stations (now KeptLarge.txt) for variable '''
    ''' If good station doesn't match up with anything '''
    ''' in the bad station list then write out to new file '''

    MyTypes         = ("|S6","|S5","float","float","float","|S4","|S30","|S14")
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
# MAIN PROGRAM
#***********************************************************************
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

# read in bad station list
MyTypes            = ("|S6","|S5","|S60")
MyDelimiters       = [6,5,60]
RawData            = ReadData(BADSLIST,MyTypes,MyDelimiters)
BADStationListWMO  = np.array(RawData['f0'])
BADStationListWBAN = np.array(RawData['f1'])
nBADstations       = len(StationListWMO)

# Concatenate the WMO and WBANS elementwise
BADWMOWBAN = np.array(["%s%s" % i for i in zip(BADStationListWMO,BADStationListWBAN)])

# read in good station lists for each variable and then output minus bads
SiftList(GOODLISTt,BADWMOWBAN)
#pdb.set_trace()
SiftList(GOODLISTdpd,BADWMOWBAN)
SiftList(GOODLISTtd,BADWMOWBAN)
SiftList(GOODLISTq,BADWMOWBAN)
SiftList(GOODLISTrh,BADWMOWBAN)
SiftList(GOODLISTe,BADWMOWBAN)
SiftList(GOODLISTtw,BADWMOWBAN)

print("And, we are done!")
