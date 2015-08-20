#!/usr/local/sci/bin/python

#*********************************************
# 08 JUL 2015
# Read in log file of chosen variable
# Output No. Stations with 0, 1, 2, 3 etc IH
# Output No. Stations with absolute IH size 0-1, 1-2, 2-3, 3-4, 4-5, 5-6, 6-7. 7-8 etc
# Reduce list to stations with x maximum IH size and y maximum IH frequency
#	< 1 g/kg or 1 deg or 1 %rh or 1 hPa abosolute IH
#	<= 3 IH
# Output selected list of stations
# Output IH for selected list of stations
#*********************************************
#                START
#*********************************************
# USE python2.7
# python2.7 PullOutLowIHStations_JUL2015.py
#
# ipython
# %pdb
# %run PullOutLowIHStations_JUL2015.py
# u, d, 
#
# REQUIRES:
#
#*********************************************
# Set up python imports
import numpy as np
import itertools # this helps to work with lists
 
#*********************************************
# Set up variables and filenames

MyParam='T'	#'q','RH','e','T','Td','Tw','DPD

SelectSize=0.1 	# Maximum size of IH permitted
SelectFreq=3	# Maximum number of IHs permitted

#InList='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAq_goodsHadISDH.2.0.1.2014p_JAN2015.txt'
#InList='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHArh_goodsHadISDH.2.0.1.2014p_JAN2015.txt'
InList='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAe_goodsHadISDH.2.0.1.2014p_JAN2015.txt'
#InList='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAt_goodsHadISDH.2.0.1.2014p_JAN2015.txt'
#InList='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAtw_goodsHadISDH.2.0.1.2014p_JAN2015.txt'
#InList='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHADPDtd_goodsHadISDH.2.0.1.2014p_JAN2015.txt'
#InList='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAdpd_goodsHadISDH.2.0.1.2014p_JAN2015.txt'

#InLog='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landq.2.0.1.2014p_IDPHA_JAN2015.log'
#InLog='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landRH.2.0.1.2014p_IDPHA_JAN2015.log'
InLog='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.lande.2.0.1.2014p_IDPHA_JAN2015.log'
#InLog='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landT.2.0.1.2014p_IDPHAMG_JAN2015.log'
#InLog='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landTw.2.0.1.2014p_IDPHA_JAN2015.log'
#InLog='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landTd.2.0.1.2014p_PHADPD_JAN2015.log'
#InLog='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.landDPD.2.0.1.2014p_PHA_JAN2015.log'

OutList='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.land'+MyParam+'.2.0.1.2014p_SELECTmax'+str(SelectSize)+'_most'+str(SelectFreq)+'_JUL2015.txt'

OutLog='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/HadISDH.land'+MyParam+'.2.0.1.2014p_SELECTmax'+str(SelectSize)+'_most'+str(SelectFreq)+'_JUL2015.log'

# Create some structure to hold all of the IH info for each station
# Build on the fly to hold: StationID, Total number of IH, IHStartDates, IHEndDates, IHActualSize, IHActualUnc, IHCumSize, IHCumUnc
StationStatVar=[]
SubStationStatVar=[]

# Read in station lists
# create on fly from read in with all info: StationID, Latitude, Longitude, Elevation, CountryCode, StationName
StationList=[]
SubStationList=[]

#************************************************************************
# READDATA
def ReadData(FileName,typee,delimee):
    ''' Use numpy genfromtxt reading to read in all rows from a complex array '''
    ''' Need to specify format as it is complex '''
    ''' outputs an array of tuples that in turn need to be subscripted by their names defaults f0...f8 '''
    return np.genfromtxt(FileName, dtype=typee,delimiter=delimee) # ReadData

#*********************************************
# ReadLogs
def ReadLogs(FileName,TheStatList): 
    '''
    Read in IDPHA results from log
    
    Create a list of embedded lists containing:

    0: StationID - wmo+wban
    1: Total number of IH 0+
    2: NumIH - number of IH in order, counts go from 1973 to present
    3: IHStartMon - month count for start
    4: IHEndMon - month count for end
    5: rel_adjust - relative adjustment size to next HSP
    6: rel_unc - relative uncertainty in adj
    7: act_adjust - actual adjustment relative to reference 
    8: act_unc - actual uncertainty in adjustment
    
    '''
    
    # tempvars for searching through
    StationID='99999999999'
    Counter=-1
    for line in open(FileName):
        moo=str.split(line)	# split by gaps
	
	# Find out if this is a new station or if it belongs to previous line
	if StationID in line: # it is so carry on appending
	    TheStatList[Counter][2].append(int(moo[1]))
	    TheStatList[Counter][3].append(int(moo[2]))
	    TheStatList[Counter][4].append(int(moo[3]))
	    TheStatList[Counter][5].append(float(moo[4]))
	    TheStatList[Counter][6].append(float(moo[5]))
	    TheStatList[Counter][7].append(float(moo[6]))
	    TheStatList[Counter][8].append(float(moo[7]))	    
	
	else: # its not so start a new entry
	    Counter=Counter+1    
	    #print(Counter,moo[0])
	    TheStatList.append([])
	    StationID=str(moo[0])
	    TheStatList[Counter].append([StationID])
	    TheStatList[Counter].append([int(moo[1])-1])	# first entry is final count of IH so if = 1 then this will be 0
	    TheStatList[Counter].append([int(moo[1])])
	    TheStatList[Counter].append([int(moo[2])])
	    TheStatList[Counter].append([int(moo[3])])
	    TheStatList[Counter].append([float(moo[4])])
	    TheStatList[Counter].append([float(moo[5])])
	    TheStatList[Counter].append([float(moo[6])])
	    TheStatList[Counter].append([float(moo[7])])
	    	    	
    return TheStatList # ReadLogs

#*********************************************
# OutputStats
def OutputStats(TheStatList):
    '''
    Look through file and output simple stats to screen (maybe to file later?)
    Number of stations with 0, 1, 2, 3 etc IH
    Number of stations with absolute IH size of <1, <2, <3 etc
    '''

    StationCount=len(TheStatList)

    # Search through list to find Number of Stations with 1 to max of list IHs - using some list comprehension
    MaxNumIH=max([TheStatList[i][1] for i in range(StationCount)])
    for IHNum in range(MaxNumIH[0]+1):
        Totals=sum([(int(TheStatList[i][1][0]) == IHNum) for i in range(StationCount)])
	print(Totals,' Stations with ',IHNum,' IH number')

    # Search through list to find Total Number of Stations with IH max in ranges from 1 to max of list - using some list comprehension
    # Consider only cumulative/actual IH sizes - could change this
    MaxSizeIH=np.ceil(max(abs(np.array(list(itertools.chain.from_iterable([TheStatList[i][7] for i in range(StationCount)]))))))
    Totals=sum([(max(abs(np.array(TheStatList[i][7]))) == 0.0) for i in range(StationCount)])
    print(Totals,' Stations with 0.0 max IH Size')
    for IHSize in range(int(MaxSizeIH)):	# look at 0-1, 1-2, 2-3 etc
        Totals=sum([(max(abs(np.array(TheStatList[i][7]))) > IHSize) & (max(abs(np.array(TheStatList[i][7]))) <= IHSize+1.) for i in range(StationCount)])
	print(Totals,' Stations with ',IHSize,' to ',IHSize+1,' max IH Size')
 
    return   #OutputStats
#*********************************************
# StationSelection
def StationSelection(TheIDList,TheStatList,TheIHSize,TheIHFreq,TheSubIDList,TheSubStatList):
    '''
    Based on given Max IH size and frequency
    Select stations that fit criteria
    Subset station list of IDs and list of IHs
    Return sublists
    '''
    StationCount=len(TheStatList)

    # Search through list to find Number of Stations with 1 to max of list IHs - using some list comprehension
    FewIHs=[(int(TheStatList[i][1][0]) <= TheIHFreq) for i in range(StationCount)]
    print(sum(FewIHs),' Stations with <= ',TheIHFreq,' IH number')

    # Search through list to find Total Number of Stations with IH max in ranges from 1 to max of list - using some list comprehension
    # Consider only cumulative/actual IH sizes - could change this
    SmallIH=[(max(abs(np.array(TheStatList[i][7]))) < TheIHSize) for i in range(StationCount)]
    print(sum(SmallIH),' Stations with < ',TheIHSize,' max IH Size')
    
    Goodies=np.where((np.array(FewIHs)==True) & (np.array(SmallIH)==True))[0]
    
    for loo,pointie in enumerate(Goodies):
        #print(loo,pointie,FewIHs[pointie],SmallIH[pointie])
        # now test to make sure the kept station is actually in the goods list (could have been chucked out in post processing)
	#stop
	Foundit=np.where(TheIDList[0] == TheStatList[pointie][0][0][0:6])[0]
	if (len(Foundit) > 0):
	    #print('Got it!')
	    TheSubStatList.append(TheStatList[pointie])
	    TheSubIDList.append([TheIDList[0][Foundit[0]],TheIDList[1][Foundit[0]],TheIDList[2][Foundit[0]],TheIDList[3][Foundit[0]],TheIDList[4][Foundit[0]],TheIDList[5][Foundit[0]],TheIDList[6][Foundit[0]]])
    
    print(len(TheSubIDList),' Stations with fewer than ',TheIHFreq,' and less than ',TheIHSize,' max IH')
    
    return TheSubIDList,TheSubStatList # StationSelection
#*********************************************
# WriteStationList
def WriteStationList(FileName,TheIDList):
    ''' Write out the station WMO and WBAN and Location to file   '''
    ''' File is either list of good stations or bad stations '''
    ''' Bad stations are cases where there are fewer than 7 neighbours '''
    ''' This is based on listings compiled for this variable during direct PHA '''
    ''' First difference series of the monthly anomalies must correlate > 0.1 '''
    filee=open(FileName,'a+')
    for loo in range(len(TheIDList)):
        filee.write('%6s%5s%9s%10s%7s%4s%30s\n' % (TheIDList[loo][0],TheIDList[loo][1],TheIDList[loo][2],TheIDList[loo][3],TheIDList[loo][4],TheIDList[loo][5],TheIDList[loo][6],))
    
    filee.close()

    return
#*********************************************
# WriteStationLogs
def WriteStationLogs(FileName,TheStatList):
    ''' Print out a list of breaks found with their location, size and uncertainty '''
    ''' Append to file '''
    ''' IN ALL CASES ADJUSTMENTS ARE -(adj) TO MATCH PHA OUTPUT '''
    ''' IF THE DATA HAVE BEEN ADJUSTED DOWN THEN THE ADJUSTMENT GIVEN IS POSITIVE - WEIRD '''
    filee=open(FileName,'a+')
    for loo in range(len(TheStatList)):
        for ih in range(TheStatList[loo][1][0]+1):
            filee.write('%11s %2s %3i %3i %6.2f %6.2f %6.2f %6.2f \n' % (TheStatList[loo][0][0],TheStatList[loo][2][ih],
	        TheStatList[loo][3][ih],TheStatList[loo][4][ih],TheStatList[loo][5][ih],TheStatList[loo][6][ih],TheStatList[loo][7][ih],TheStatList[loo][8][ih]))

    filee.close()

    return #WriteStationLogs
#*********************************************
# MAIN PROGRAM
#********************************************* 
# read in station list
MyTypes=("|S6","|S5","|S9","|S10","|S7","|S4","|S30","|S7")
MyDelimiters=[6,5,9,10,7,4,30,7]
RawData=ReadData(InList,MyTypes,MyDelimiters)
StationList.append(np.array(RawData['f0'])) # ID 6s
StationList.append(np.array(RawData['f1'])) # WBAN 5s
StationList.append(np.array(RawData['f2'])) # Latitude f9.4
StationList.append(np.array(RawData['f3'])) # Longitude f10.4
StationList.append(np.array(RawData['f4'])) # Elevation f7.1
StationList.append(np.array(RawData['f5'])) # CountryCode 4s 
StationList.append(np.array(RawData['f6'])) # StationName 30s
nstations=len(StationList[0])

# read in IDPHA log list and populate output var
StationStatVar=ReadLogs(InLog,StationStatVar)

# Get simple stats and output to screen
OutputStats(StationStatVar)

# Subset station list and log to only those fitting criteria
SubStationList,SubStationStatVar=StationSelection(StationList,StationStatVar,SelectSize,SelectFreq,SubStationList,SubStationStatVar)

# Print new station list to file
WriteStationList(OutList,SubStationList)

# Print new station log list to file
WriteStationLogs(OutLog,SubStationStatVar)

#stop

print("And, we are done!")
