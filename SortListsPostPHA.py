#!/usr/local/sci/bin/python
# PYTHON2.7
# 
# Author: Kate Willett
# Created: 10 February 2018
# Last update: 10 February 2018
# Location: /data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# This code: 
#   - reads in the Posthomog... files for each called variable (T unnecessary)
#   - looks at subzeros and bads and removes any that are in bads (e and q only)
#   - looks at supersats and bads and removes any that are in bads (all)
#   - files are now ready to go for the rest of processing
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
# Post PHA list of bad stations - too few months remaining
# PHBADS = '/data/local/hadkw/HADCRUH2/UPDATE<yyyy>/LISTS_DOCS/Posthomog<homogtype><var>_anoms<clim>_badsHadISDH.<version>_JAN<yyyy>.txt
# Post PHA list of subzero stations - q and e values below zero
# PHSUBS = '/data/local/hadkw/HADCRUH2/UPDATE<yyyy>/LISTS_DOCS/Posthomog<homogtype><var>_anoms<clim>_subsHadISDH.<version>_JAN<yyyy>.txt
# Post PHA list of supersaturated stations - greater than 100%rh, Td>T, DPD<0
# PHSATS = '/data/local/hadkw/HADCRUH2/UPDATE<yyyy>/LISTS_DOCS/Posthomog<homogtype><var>_anoms<clim>_satsHadISDH.<version>_JAN<yyyy>.txt
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# python2.7 SortListsPostPHA.py
# Edit the VarSwitch internally from 'all' to 'q','e','rh','td','tw','sps if you only want a specific variable
# 
# -----------------------
# OUTPUT
# -----------------------
# Post PHA list of bad stations - too few months remaining
# PHBADS = '/data/local/hadkw/HADCRUH2/UPDATE<yyyy>/LISTS_DOCS/Posthomog<homogtype><var>_anoms<clim>_badsHadISDH.<version>_JAN<yyyy>.txt
# Post PHA list of subzero stations - q and e values below zero
# PHSUBS = '/data/local/hadkw/HADCRUH2/UPDATE<yyyy>/LISTS_DOCS/Posthomog<homogtype><var>_anoms<clim>_subsHadISDH.<version>_JAN<yyyy>.txt
# Post PHA list of supersaturated stations - greater than 100%rh, Td>T, DPD<0
# PHSATS = '/data/local/hadkw/HADCRUH2/UPDATE<yyyy>/LISTS_DOCS/Posthomog<homogtype><var>_anoms<clim>_satsHadISDH.<version>_JAN<yyyy>.txt
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
#
# Version 1 (10 February 2018)
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
# Next time I need to fix the SAT/SUB Annotation as it just writes 'S'
#
#************************************************************************
#                                 START
#************************************************************************
# USE python2.7
# python2.7 SortListsPostPHA.py
#
#************************************************************************
# Set up python imports
import numpy as np
import sys, os
import struct
import pdb
from subprocess import call

# Set up initial run choices
# Switch to choose between running all or just one variable
VarSwitch  = 'all' # 'all','q','e','rh','td','tw','dpd'

# Run type switch to choose the production run (IDPHA(q,e,RH.Tw), PHA(DPD) and PHADPD(Td) or other
RunType    = 'full' # 'full','IDPHA','PHA','PHADPD'

# End year
edyr       = 2017

# Working file month and year
nowmon     = 'JAN'
nowyear    = '2018'

# Climatology period
climstart  = 1981
climend    = 2010
climperiod = str(climstart)[2:4]+str(climend)[2:4]

# Dataset version
version    = '4.0.0.2017f'

# Set up file locations
updateyear = str(edyr)[2:4]
workingdir = '/data/local/hadkw/HADCRUH2/UPDATE20'+updateyear

# List of files to work with - but these are set up later depending on loop (var, homog)
#PHBADS    = workingdir+'/LISTS_DOCS/Posthomog_'+homogtype+param+'_anoms'+climperiod+'_badsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
#PHSUBS    = workingdir+'/LISTS_DOCS/Posthomog_'+homogtype+param+'_anoms'+climperiod+'_satsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
#PHSATS    = workingdir+'/LISTS_DOCS/Posthomog_'+homogtype+param+'_anoms'+climperiod+'_subsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'

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
# SIFTBADLIST
def SiftBadList(BADFile,SUBFile,SATFile):
    ''' Open BADFile and read list of bad stations for variable '''
    ''' If SUBFile not '' then open and read list of subsat stations for variable - RH, q, e'''
    ''' If SATFile not '' then open and read list of sat stations for variable - RH, DPD, Td, Tw'''
    ''' Search to see if there are any sats or subsats in bad '''
    ''' If there are then remove from sat/subsat list and annotate station in bad list '''
    ''' If there is a station in the sub and sat list then remove from sub list and annotate in sat list '''

    # Info for reading in - should work for all although bads is a slightly shorter string
    MyTypes         = ("|S6","|S5","|S24")
    MyDelimiters    = [6,5,24]

    # Set up empty arrays
    nstations       = 0	# defined after reading in station list
    StationListWMO  = []	# nstations list filled after reading in station list
    StationListWBAN = []	# nstations list filled after reading in station list
    StationMush     = []	# any text
    nSBstations       = 0	# defined after reading in station list
    SBStationListWMO  = []	# nstations list filled after reading in station list
    SBStationListWBAN = []	# nstations list filled after reading in station list
    SBStationMush     = []	# any text
    nSTstations       = 0	# defined after reading in station list
    STStationListWMO  = []	# nstations list filled after reading in station list
    STStationListWBAN = []	# nstations list filled after reading in station list
    STStationMush     = []	# any text

    # Open the list of bad stations
    RawData         = ReadData(BADFile,MyTypes,MyDelimiters)
    StationListWMO  = np.array(RawData['f0'])
    StationListWBAN = np.array(RawData['f1'])
    StationMush  = np.array(RawData['f2'])
    nstations       = len(StationListWMO)
    # make a blank string array nstations long
    StationAnnotate = np.empty(nstations,dtype=str)
    StationAnnotate[:] = ''

    # If there is a sat file name then open and read to array
    if (SATFile != ''):
        RawData         = ReadData(SATFile,MyTypes,MyDelimiters)
        STStationListWMO  = np.array(RawData['f0'])
        STStationListWBAN = np.array(RawData['f1'])
        STStationMush  = np.array(RawData['f2'])
        nSTstations       = len(STStationListWMO)
        # make a blank string array nstations long
        STStationAnnotate = np.empty(nSTstations,dtype=str)
        STStationAnnotate[:] = ''
	        
	# Find sats in bads and annotate
	BadLocs               = np.in1d(StationListWMO,STStationListWMO)
	if (len(StationListWMO[BadLocs]) > 0):
	    loopee = np.where(BadLocs == True)[0]
	    for i in range(len(loopee)):
	        StationAnnotate[loopee[i]] = StationAnnotate[loopee[i]]+'SAT'
	print('Supersats in bad',len(StationListWMO[BadLocs]))
	
	# Find bads in sats and delete
	SatLocs           = np.in1d(STStationListWMO,StationListWMO)
	if (len(STStationListWMO[SatLocs]) > 0):
	    STStationListWMO  = np.delete(STStationListWMO,np.where(SatLocs == True))
	    STStationListWBAN = np.delete(STStationListWBAN,np.where(SatLocs == True))
	    STStationMush     = np.delete(STStationMush,np.where(SatLocs == True))
	    STStationAnnotate = np.delete(STStationAnnotate,np.where(SatLocs == True))
	
    # If there is a sub file name then open and read to array
    if (SUBFile != ''):
        RawData         = ReadData(SUBFile,MyTypes,MyDelimiters)
        SBStationListWMO  = np.array(RawData['f0'])
        SBStationListWBAN = np.array(RawData['f1'])
        SBStationMush  = np.array(RawData['f2'])
        nSBstations       = len(SBStationListWMO)
        # make a blank string array nstations long
        SBStationAnnotate = np.empty(nSBstations,dtype=str)
        SBStationAnnotate[:] = ''	
        
	# Find subs in bads and annotate
	BadLocs               = np.in1d(StationListWMO,SBStationListWMO)
	if (len(StationListWMO[BadLocs]) > 0):
	    loopee = np.where(BadLocs == True)[0]
	    for i in range(len(loopee)):
	        StationAnnotate[loopee[i]] = StationAnnotate[loopee[i]]+'SUB'
	print('Subsats in bad',len(StationListWMO[BadLocs]))
	
	# Find bads in subs and delete
	SubLocs           = np.in1d(SBStationListWMO,StationListWMO)
	SBStationListWMO  = np.delete(SBStationListWMO,np.where(SubLocs == True))
	SBStationListWBAN = np.delete(SBStationListWBAN,np.where(SubLocs == True))
	SBStationMush     = np.delete(SBStationMush,np.where(SubLocs == True))
	SBStationAnnotate = np.delete(SBStationAnnotate,np.where(SubLocs == True))
	
    # If there is a sub and sat file name then find matches
    if (SUBFile != '') and (SATFile != ''):

	# Find subs in sats and annotate sats
	BadLocs               = np.in1d(STStationListWMO,SBStationListWMO)
	if (len(STStationListWMO[BadLocs]) > 0):
	    loopee = np.where(BadLocs == True)[0]
	    for i in range(len(loopee)):
	        STStationAnnotate[loopee[i]] = STStationAnnotate[loopee[i]]+'SUB'
	print('Subsats in sat',len(STStationAnnotate[BadLocs]))
	
	# Find sats in subs and delete
	SubLocs           = np.in1d(SBStationListWMO,STStationListWMO)
	SBStationListWMO  = np.delete(SBStationListWMO,np.where(SubLocs == True))
	SBStationListWBAN = np.delete(SBStationListWBAN,np.where(SubLocs == True))
	SBStationMush     = np.delete(SBStationMush,np.where(SubLocs == True))
	SBStationAnnotate = np.delete(SBStationAnnotate,np.where(SubLocs == True))
	
#    pdb.set_trace()
    
    # Write out bad list
    WriteText(BADFile,StationListWMO,StationListWBAN,StationMush,StationAnnotate)

    # If there is a SATFile then write out list
    if (SATFile != ''):
        WriteText(SATFile,STStationListWMO,STStationListWBAN,STStationMush,STStationAnnotate)

    # If there is a SUBFile then write out list
    if (SUBFile != ''):
        WriteText(SUBFile,SBStationListWMO,SBStationListWBAN,SBStationMush,SBStationAnnotate)

    return

#***********************************************************************
# WRITETEXT
def WriteText(TheFile,TheStationWMO,TheStationWBAN,TheBlurb,TheAnnotation):
    ''' Write out the station WMO and WBAN and Blurb and SAT/SUB Annotations to file   '''
    ''' OVERWRITES ORIGINAL!!! '''

    filee = open(TheFile,'w')
    
    for ll in range(len(TheStationWMO)):
    
        filee.write('%6s%5s%24s%7s\n' % (TheStationWMO[ll],TheStationWBAN[ll],TheBlurb[ll].rstrip('\n'),TheAnnotation[ll])) # \n'
    
    filee.close()

    return #WriteText

#***********************************************************************
# MAIN PROGRAM
#***********************************************************************
# Which variable?
if (VarSwitch == 'all'):
    VarArray = ['q','e','rh','td','tw','dpd']
else:
    VarArray = [VarSwitch]    

# Run type switch to choose the production run (IDPHA(q,e,RH.Tw), PHA(DPD) and PHADPD(Td) or other
RunType    = 'full' # 'full','IDPHA','PHA','PHADPD'

# Which homogtype?
if (RunType == 'full'):
    RunArray = ['IDPHA','IDPHA','IDPHA','PHADPD','IDPHA','PHA']
else:
    RunArray = [RunType]
 
# Loop through the variables
for i in range(len(VarArray)):    

    # Set up Filenames
    if (VarArray[i] == 'q') or (VarArray[i] == 'e'):
        PHSUBS = workingdir+'/LISTS_DOCS/Posthomog'+RunArray[i]+VarArray[i]+'_anoms'+climperiod+'_subzerosHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
    else:
        PHSUBS = ''
	
    PHBADS = workingdir+'/LISTS_DOCS/Posthomog'+RunArray[i]+VarArray[i]+'_anoms'+climperiod+'_badsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
    PHSATS = workingdir+'/LISTS_DOCS/Posthomog'+RunArray[i]+VarArray[i]+'_anoms'+climperiod+'_satsHadISDH.'+version+'_'+nowmon+nowyear+'.txt'

    # Sift through the bad, sub and sat lists and output
    SiftBadList(PHBADS,PHSUBS,PHSATS)

print("And, we are done!")
