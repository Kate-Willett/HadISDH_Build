# PYTHON 3
# >module load scitools/default-current
#
# Author: Kate Willett
# Created: 1 February 2013 (IDL)
# Last update: 1 December 2020 (Python 3 from 1st Dec 2020)
# Location: /home/h04/hadkw/HadISDH_Code/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# This code finds the missed adjustment uncertainty for each variable by looking at a gaussian fit to the distribution of adjustments
# and the actual distribution. The missed adjustment uncertainty is the standard deviation of the difference.
#
# This code looks at all of the adjustments allocated to all stations for a variable
# It plots a distribution of adjustment magnitude and a time series of adjustment frequency.(optional plot output)
# It also assesses the mean and standard deviation of the adjustments in absolute and actual space (also median)
# It also fits a gaussian to the distribution, adjusts it to include the 'fatter tails' and then 
# takes the difference between the two to identify the 'missing adjustments / missing middle' 
# The standard deviation of the missed adjustment distribution is taken as the 1 sigma uncertainty
# remaining in the data from missed adjustments
#
# Mean number of changepoints and distribution stats are output to file for read in by other programs
#
# Plots are output and a list of stations and adjustments from largest to smallest.
# 
# <references to related published material, e.g. that describes data set>
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# <List of program modules required to run the code, or link to compiler/batch file>
# 
# -----------------------
# DATA
# -----------------------
# inlist: list of stations to work through 
# /scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/goodforHadISDH.'+version+'_PHAdpd.txt'
# NB - IF YOU RERUN LATER YOU WILL HAVE TO SWAP TO USING _KeptLarge.txt!!!
# inlog: list of adjustment locations and magnitudes for each station    
# /scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/HadISDH.landDPD.'+version+'_PHA.log' 
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# Go through everything in the 'Start' section to make sure dates, versions and filepaths are up to date
# If we're using the Config file (F1_HadISDHBuildConfig.txt) then make sure that is correct.
#>./F10_submit_spice.bash - this will run all variables so you will have to comment out any you do not wish to run
#or 
#>module load scitools/default-current # for Python 3
#>python F10_MissingAdjUncPlots.py --var <var>
#
# <var> can be q, rh, t, td, tw, e, dpd
# 
# -----------------------
# OUTPUT
# -----------------------
# outplots: 
# /scratch/hadkw/UPDATE<YYYY>/IMAGES/BUILD/HadISDH.landDPD.'+versiondots+'_adjspread_PHA.eps'
# outadjs: list of stations and adjustments from largest to smallest
# /scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/Largest_Adjs_landDPD.'+versiondots+'_PHA.txt'  
# outstats: for each variable/homogtype a list of stats is output
# /scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/Adjs_Stats.'+versiondots+.txt'  
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
# 
# Version 4 (1 December 2020)
# ---------
#  
# Enhancements
#  
# Changes
# This is now Python 3 rather than IDL
#  
# Bug fixes
#
#
# Version 3 (6 February 2018)
# ---------
#  
# Enhancements
# This program now finds the number of stations in the candidate variable station
# list so that it does not need to be put in manually before running.
# Next I should pull out the variable and homogtype so that it is stated
# at the command line rather than changed within the file before running.
#
# Now has param (variable) and homogtype called at the command line so you only need to edit the file once per year
#
# This now outputs a list of stats for each variable/homogtype to file (appends) so that other programs can read in
#
# This now has a 'KeptLarge' true/false switch to easily switch when running after the first inital run where you need
# to use the _KeptLarge.txt station lists
#  
# Changes
#  
# Bug fixes
#
# Version 2 (27 January 2017)
# ---------
#  
# Enhancements
# General tidy up and move of all editables to the top
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
#
#************************************************************************
#                                 START
#************************************************************************
# USE python3
# module load scitools/default-current
# python F10_MissingAdjUnc_AdjPlots.py --var <var> 
#
# For debugging
# ipython
# %pdb
# %run F10_MissingAdjUnc_AdjPlots.py <var>
#
# REQUIRES
# ReadNetCDF.py
#
#************************************************************************
# Set up python imports
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num,num2date
import sys, os, getopt
from scipy.optimize import curve_fit,fsolve,leastsq
#from lmfit import Model
from scipy import pi,sqrt,exp
from scipy.special import erf
import scipy.stats
from math import sqrt,pi
import struct
import pdb
#import netCDF4 as nc4
from subprocess import check_output
from subprocess import call

#import ReadNetCDF
#from GetNiceTimes import MakeDaysSince

# Start and end years if HardWire = 1
styear       = 1973
edyear       = 2019

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

# Do you want to run for plots only - not output stats?
PlotOnly = False # False = plots and output stats, True = plots only

# Growth Factor for Pseudomax of Gaussian Fitting
GrowthFactor = 1.5 # Tried 1.2, bit small

# Do you want to run for a second time (e.g., for PlotOnly = True) where station lists have already been saved as _KeptLarge.txt?
KeptLarge = False	# TRUE (run with _KeptLarge station lists or FALSE (normal, first time run)
if (KeptLarge):

    KL = '_KeptLarge' 

else: 

    KL = ''
    
# Set up directories locations
updateyy  = str(edyear)[2:4]
updateyyyy  = str(edyear)
#workingdir  = '/scratch/hadkw/UPDATE'+updateyyyy
workingdir  = '/data/users/hadkw/WORKING_HADISDH/UPDATE'+updateyyyy

OUTPLOTDIR   = workingdir+'/IMAGES/BUILD/'

# Set up filenames
INDIR = workingdir+'/LISTS_DOCS/'
OUTPUTLOG  = '/scratch/hadkw/OutputLogFile'+versiondots+'.txt'
#OUTSTATS   = workingdir+'/LISTS_DOCS/Adjs_Stats.'+versiondots+'.txt'  

# Set up variables
MDI = -1e+30
#*** at some point add all the header info from the new HadISD files***

# Dictionaries for param, units, homogtype, binsize
ParamDict = dict([('q',['q','g/kg','IDPHA','PHA', 0.05]),
	          ('rh',['RH','%rh','IDPHA','PHA', 0.5]),
	          ('t',['T','deg C','IDPHA','PHA', 0.05]), # Note this needs to be changed to IDPHAMG later
	          ('td',['Td','deg C','PHADPD','PHA', 0.1]),
	          ('tw',['Tw','deg C','IDPHA','PHA', 0.05]),
	          ('e',['e','hPa','IDPHA','PHA', 0.05]),
	          ('dpd',['DPD','deg C','PHA','PHA', 0.1])])

#************************************************************************
# Subroutines
#************************************************************************
# READDATA
def ReadData(FileName,typee,delimee):
    ''' Use numpy genfromtxt reading to read in all rows from a complex array '''
    ''' Need to specify format as it is complex '''
    ''' outputs an array of tuples that in turn need to be subscripted by their names defaults f0...f8 '''
    return np.genfromtxt(FileName, dtype=typee, delimiter=delimee, encoding='latin-1') # ReadData
#    return np.genfromtxt(FileName, dtype=typee, delimiter=delimee) # ReadData

#************************************************************************
# GAUSSIAN 
def Gaussian(x, amp, cen, wid):
    ' A Gaussian model for curve fitting '
    ' x is the x axis points '
    ' amp is the maximum amplitude '
    ' cen is the mean '
    ' wid is the standard deviation ' 
    
    return amp * exp(-(x-cen)**2 / (2*wid**2))

#****************************************************************************
# GETADJUSTMENTARRAYS
def GetAdjustmentArrays(INFIL, MCount, SCount, HType, WMOList, WBANList):
    ' This opens the adjustment list, searches for the adjustments for each station, adds them to appropriate lists '
    ' Inputs: '
    ' INFIL = string filepath and name for list of adjustments '
    ' MCount = integer number of months in time series '
    ' SCount = integer number of stations in dataset '
    ' HType = string homogtype eg. PHA, IDPHA, PHADPD '
    ' WMOList = list of WMO IDs '
    ' WBANList = list of WBAN IDs '
    ' Returns: '
    ' Adj_Locs = MCount integer array counting number of changepoints at each time point across entire dataset '
    ' Adj_Mags_Accum = Float array of all adjustments as read from file - accumalated magnitudes '
    ' Adj_Mags_Act = Float array of all adjustments as actual individual magnitudes '
    ' Adj_WMOs = integer array of WMO IDs to match each adjustment listed in Adj_Mags_Act and Adj_Mags_Accum '
    
    GAdj_Locs       = np.repeat(0,MCount) # integer array for storing locations of changepoints
    GAdj_Mags_Accum = [] # grow this array on the fly
    GAdj_Mags_Act   = []
    GAdj_WMOs       = []

    # Gunzip PHA output file
    print(INFIL)
    call(['gunzip',INFIL+'.gz'])

    # loop through station by station to get all of the adjustments and locations
    for st in range(SCount):

        # find homog adj for this station and append to array 
        if (HType == 'PHA'):
	#PHA - 0=ID, 3=stmon,6=edmon, 8=ibreak, 9=cbreak, 10=adj, 11=eadj 
	
            edmonget = 6
            adjget = 10
	    
            moo = check_output(['grep','-a','^Adj write:'+WMOList[st]+WBANList[st],INFIL])
            # Now sort out this string which is a byte array
	    # This creates a list of strings for each adjustment with a blank string at the beginning
            moo = moo.decode("utf-8").split('Adj write:')	
	    # Remove the blank string
            moo.remove('')

        elif (HType == 'IDPHAMG') or (HType == 'PHADPD'):
	#IDPHAMG - 0=ID, 2=stmon, 3=edmon, 6=adj, 7=eadj, 8=adj source indicator 

            edmonget = 3
            adjget = 6
	    
            moo = check_output(['grep','-a','^'+WMOList[st]+WBANList[st],INFIL])
            # Now sort out this string which is a byte array
	    # This creates a list of strings for each adjustment with a blank string at the beginning
            moo = moo.decode("utf-8").split('\n') # no space	
	    # Remove the blank string at the end
            moo.remove('')

        else:
	#IDPHA - 0=ID, 2=stmon, 3=edmon, 6=adj, 7=eadj 

            edmonget = 3
            adjget = 6
	    
            moo = check_output(['grep','-a','^'+WMOList[st]+WBANList[st],INFIL])
            # Now sort out this string which is a byte array
	    # This creates a list of strings for each adjustment with a blank string at the beginning
            moo = moo.decode("utf-8").split(' \n')	
	    # Remove the blank string at the end
            moo.remove('')

	# Strip the \n newline characters, random letters and split the strings to make a list of lists
        # b, i, p in IDPHAMG 
        moo = [i.strip(' ABCDEFGHIJKLMNOPQRSTUVWXYZbip\n').split() for i in moo] 
	
#        print('Check adjustment read in')
#        pdb.set_trace()
# Good for IDPHA and PHA
		
	# Now loop through the adjustments to append to array
        AdjVals = []	
	
        # Ignore first line as this is most recent period so adjustment is 0
        for rec,adjstr in enumerate(moo[1:]):
	
            Adj = -(np.copy(np.float(adjstr[adjget])))
            #print(Adj)
	    
	    # Break location
            Loc = np.int(adjstr[edmonget]) - 1
            GAdj_Locs[Loc] += 1 # increment this location by 1
	    
            GAdj_Mags_Accum.append(Adj)
            AdjVals.append(Adj)
            GAdj_WMOs.append(WMOList[st])
	    
	    # Now get the actual adjustments from AdjVals
            if (rec == 0):
	    
                GAdj_Mags_Act.append(AdjVals[0])
	
            else:
	    
                GAdj_Mags_Act.append(AdjVals[rec] - AdjVals[rec-1])	    	

#        print('Check adjustment arrays')
#        pdb.set_trace()	
# Good for IDPHA

    # gzip PHA output file for tidiness
    call(['gzip',INFIL])

    return GAdj_Locs, GAdj_Mags_Accum, GAdj_Mags_Act, GAdj_WMOs

#******************************************************************
# GETHIST
def GetHist(BinSz, GAdj_Mags_Act):
    ' Works out the things needed for creating a histogram of adjustments and returns histogram and stats '
    ' Inputs: '
    ' BinSz = float size of bins '
    ' GAdj_Mags_Act = Float array of actual adjustment magnitudes '
    ' Returns: '
    ' GHistAdjsMagsAct = Histogram of adjustments - Int array of counts for each point of histogram '
    ' GXarr = Float array of bin midpoints '
    ' GBinArr = Float array of bin points from leftmost to include final rightmost '
    ' GMeanAdj = float mean of all adjustment magnitudes '
    ' GStdAdj = float standard deviation of all adjustment magnitudes '
    ' GMaxFreq = int maximum count for a bin within the histogram '
    
    # Set up the bins for the histogram
    minX = np.floor(np.min(GAdj_Mags_Act)) - (BinSz/2.)
    maxX = np.ceil(np.max(GAdj_Mags_Act)) + (BinSz/2.)
    # Make the bins symmetrical - not quite sure why - its nice?
    if (abs(minX) > maxX): 
   
        maxX = abs(minX) 

    else:
    
        minX = -(maxX)
  
    # np.linspace better for floats than np.arange which gives inconsistent results for some reason
    GBinArr = np.linspace(minX,maxX,np.round(((maxX - minX) / BinSz)) + 1)
  
    GXarr = GBinArr[0:-1] + (BinSz/2.) 

    # Get the histogram of the Actual Adjustment Magnitudes Adj_Mags_Act  
    HistRes = plt.hist(GAdj_Mags_Act,bins=GBinArr) # [0] = histogram, [1] = bins
    GHistAdjMagsAct = HistRes[0]
    
    # Find the mean and standard deviation of adjustments
    GMeanAdj = np.mean(GAdj_Mags_Act)
    GStdAdj = np.std(GAdj_Mags_Act)
    
    # Find the max value in the histogram
    GMaxFreq = np.max(GHistAdjMagsAct)

#    # CHECK THIS!!!
#    print('Check Bins')
#    pdb.set_trace()
    
    return GHistAdjMagsAct, GXarr, GBinArr, GMeanAdj, GStdAdj, GMaxFreq

#*****************************************************************
# GETNEWMIDDLE
def GetNewMiddle(GHistAdjMagsAct, GXarr, BinSz, GMeanAdj, GMaxFreq):
    ' Find out if there is a dip or plateau in the middle '
    ' This depends on well behaved histograms that do not ahve any unusual peaks other than a missing middle. '
    ' 1. Split histogram below and =/above the mean '
    ' 2. Find local max of lower half and upper half '
    ' 3. Set all lower values (if any) after local max in lower half to max of histogram '
    '    - if there are lower values then set FixLow = True '
    ' 4. Set all lower values (if any) before local max in upper half to max of histogram '
    '    - if there are lower values then set FixHigh = True '
    '    - if there are lower values then set first point of upper value (closest to mean) to GrowthFactor * max of histogram (pseudomax) '
    ' 5. If there is no dip in upper values, so no pseudomax set, then if there is a dip in the lower half: '
    '    - set last point of lower half (closest to mean) to GrowthFactor * max of histogram (pseudomax) '
    ' 6. Merge new low and high values and return '
    ' Inputs: '
    ' GHistAdjMagsAct = Int array of histogram of adjustment magnitudes '
    ' GXarr = float array of bin midpoints '
    ' BinSz = float bin size '
    ' GMeanAdj = float mean of adjustment magnitudes '
    ' GMaxFreq = int max of histogram '
    ' Returns: '
    ' GNewHistAdjMagsAct = float array of adjustment magnitudes with missing middle set to max values '
    ' FixLow = True if a dip is found, False if not '
    ' FixHigh = True if a dip is found, False if not '
    
    FixLow = False
    FixHigh = False
    
    # Search for max in everything below the mean 
    LowHalf = GHistAdjMagsAct[np.where((GXarr + (BinSz / 2.)) < GMeanAdj)]
    LowHalfMax = np.max(LowHalf)
    GotMax = np.where(LowHalf == LowHalfMax)[0]
#    pdb.set_trace()
    
    # If the max is before the end of the array then set all after max to max
    if (GotMax[0] < (len(LowHalf)-1)):
    
        LowHalf[GotMax[0]+1:] = GMaxFreq
        FixLow = True
#        print('Found dip in low half')
    
    # Search for max in everything above the mean
    HighHalf = GHistAdjMagsAct[np.where((GXarr + (BinSz / 2.)) >= GMeanAdj)]
    HighHalfMax = np.max(HighHalf)
    GotMax = np.where(HighHalf == HighHalfMax)[0]
#    pdb.set_trace()

    # If the max is after the beginning of the array then set all before max to max and first value (closest to mean) to max*GrowthFactor
    if (GotMax[0] > 0):
    
        HighHalf[:GotMax[0]] = GMaxFreq # do not need + 1 here because I don't want to reset the local maximum
        HighHalf[0] = GMaxFreq * GrowthFactor
        FixHigh = True
#        print('Found dip in high half - setting pseudomax')

    # Run a check that if no pseudomax value has been set in HighHalf because there is no dip then one shoudl be set in LowHalf if there is a dip there
    elif (FixLow):
    
        LowHalf[-1] = GMaxFreq * GrowthFactor
#        print('Set pseudomax in low half')

    # Merge Low and High half to create new histogram with completed middle
    GNewHistAdjMagsAct = np.append(LowHalf,HighHalf)
    
#    print('Check LowHalf and HighHalf')
#    pdb.set_trace()
    
    # Might need some threshold to detect the dip - if just one or two values is it really?
    # For q IDPHA only one value in dip but fit is better with pseudomax set.
    
    return GNewHistAdjMagsAct, FixLow, FixHigh 

#***********************************************************
# OUTPUTSTATS
def OutPutStats(OUTLOG, OUTADJS, GAdj_Mags_Act, GDiffValsArr, GAdj_WMOs, GVar, HType, SCount):
    ' Write out statistics to OUTPUTLOG and OUTADJS '
    ' Inputs: '
    ' OUTLOG = string filepath and name for OUTPUTLOG '
    ' OUTLIST = string filepath and name for OUTADJS '
    ' GAdj_Mags_Act = float array of all adjustment magnitudes ' 
    ' GDiffValsArr = float array of missing adjustments '
    ' GAdj_WMOs = string array of WMO IDs for each of GAdj_Mags_Act '
    ' GVar = string varname '
    ' HType = string homogtype '
    ' SCount = integer number of stations '
    ' Returns: '
    ' Nothing '

    # Get the sorted absolute adjustments
    Abs_Adj_Mags_Act = np.sort(abs(np.array(GAdj_Mags_Act)))  

    filee = open(OUTLOG,'a+')

    filee.write('%s%s%s%s%.3f\n' % (GVar,'_',HType,'_ABS_MEAN=',np.mean(Abs_Adj_Mags_Act)))
    filee.write('%s%s%s%s%.3f\n' % (GVar,'_',HType,'_ABS_MEDIAN=',np.median(Abs_Adj_Mags_Act)))
    filee.write('%s%s%s%s%.3f\n' % (GVar,'_',HType,'_ABS_STD=',np.std(Abs_Adj_Mags_Act)))
    filee.write('%s%s%s%s%.3f\n' % (GVar,'_',HType,'_MEAN=',np.mean(GAdj_Mags_Act)))
    filee.write('%s%s%s%s%.3f\n' % (GVar,'_',HType,'_MEDIAN=',np.median(GAdj_Mags_Act)))
    filee.write('%s%s%s%s%.3f\n' % (GVar,'_',HType,'_STD=',np.std(GAdj_Mags_Act)))
    filee.write('%s%s%s%s%.3f\n' % (GVar,'_',HType,'_MEAN_GAUSSDIFFS=',np.mean(GDiffValsArr)))
    filee.write('%s%s%s%s%.3f\n' % (GVar,'_',HType,'_STD_GAUSSDIFFS=',np.std(GDiffValsArr)))
    filee.write('%s%s%s%s%.3f\n' % (GVar,'_',HType,'_MEAN_ADJ_NO=',len(GAdj_Mags_Act) / float(SCount)))
    
    filee.close()

    # Get sorted array of adjustments for kicking out largest
    GAdj_Mags_Act = np.array(GAdj_Mags_Act)
    OrderAdj = np.flip(np.argsort(abs(GAdj_Mags_Act))) # gives the index of the sorted values, largest to smallest
#    pdb.set_trace()
#    Sorted_Adj_Mags_Act  = np.flip(np.sort(GAdj_Mags_Act)) # now sorted and largest to smallest
    Sorted_Adj_Mags_Act  = GAdj_Mags_Act[OrderAdj] # now sorted and largest to smallest
    
    # Print out these in order
    filee = open(OUTADJS,'a+')
    
    for i, AdjVal in enumerate(Sorted_Adj_Mags_Act):

        stradj = '% 7.2f' % AdjVal
        filee.write('%s%s%s\n' % (GAdj_WMOs[OrderAdj[i]],' ', stradj))

    filee.close()

    return

#********************************************************************************
def PlotAdjs(OutFile, GHistAdjMagsAct, GGaussCurve, GMergeFit, GDiffArr, GDiffValsArr, GXarr, GAdj_Locs, MCount, StYr, EdYr, Unit):
    ''' Plot histogram of adjustments and estimates for missing middle '''
    ''' Plot time series of location of changepoints '''

    # Set up for 2 panel plot
    plt.clf()
    f,axarr=plt.subplots(2,figsize=(7,10),sharex=False)	#6,18
    
    # Set up the historgram
    axarr[0].set_position([0.1,0.6,0.85,0.35])
    axarr[0].set_xlim([GXarr[0],GXarr[-1]])
    axarr[0].plot(GXarr,GHistAdjMagsAct,'.',c='black') #linewidth=0.25)
    axarr[0].plot(GXarr,GGaussCurve,c='lightgrey') #,linewidth=0.25)
    axarr[0].plot(GXarr,GMergeFit,c='red') #, linewidth=0.25)
    axarr[0].plot(GXarr,GDiffArr,':',c='blue') #,linewidth=0.25)

    axarr[0].annotate('a)',xy=(0.03,0.9), xycoords='axes fraction',size=12)
    MnDfs = '%7.3f' % np.mean(GDiffValsArr)
    axarr[0].annotate('Mean of Diffs: '+MnDfs,xy=(0.03,0.8), xycoords='axes fraction',size=14)
    StdDfs = '%7.3f' % np.std(GDiffValsArr)
    axarr[0].annotate('Std of Diffs: '+StdDfs,xy=(0.03,0.7), xycoords='axes fraction',size=14)

    axarr[0].set_xlabel('Adjustment Magnitude '+Unit,size=16)
    axarr[0].set_ylabel('Frequency',size=16)

    # Set up the time series
    TheMonths = []
    yr = int(StYr)
    mon = 1
    for m in range(MCount):
        TheMonths.append(dt.date(yr,mon,1))
        mon=mon+1
        if mon == 13:
            mon = 1
            yr = yr + 1   

    axarr[1].set_position([0.1,0.1,0.85,0.35])
    axarr[1].set_xlim([TheMonths[0],TheMonths[-1]])
    axarr[1].plot(TheMonths,GAdj_Locs,c='black') #, linewidth=0.25)

    axarr[1].annotate('b)',xy=(0.03,0.9), xycoords='axes fraction',size=12)

    axarr[1].set_xlabel('Time',size=16)
    axarr[1].set_ylabel('Frequency',size=16)

    #plt.show()
    plt.savefig(OutFile+".eps")
    plt.savefig(OutFile+".png")

    return #PlotHomogTS

#******************************************
# MAIN
#************************************************
def main(argv):
    # INPUT PARAMETERS AS STRINGS!!!!
    var = 'q'	    # 'q','rh','e','td','tw','t','dpd'
    
    try:
        opts, args = getopt.getopt(argv, "hi:",
	                           ["var="])
    except getopt.GetoptError:
        print('Usage (as strings) F10_MissingAdjUnc_AdjPlots.py --var <q>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--var":
            try:
                var = arg
            except:
                sys.exit("Failed: var not a string")

    # HARDWIRE THIS IF YOU WANT TO ONLY LOOK AT PHA!!!
    homogtype = ParamDict[var][2] # THIS IS THE OPERATIONAL RUN (IDPHA, IDPHAMG, PHA, PHADPD)
 
    print('WORKING ON: ',var, homogtype)
#    pdb.set_trace()

# Collect all of the adjustment information
    
    # Now set up files 
    var2   = ParamDict[var][0]	#'DPD','RH','Td','T','Tw','e','q
#    INSTATLIST   = INDIR+'goodforHadISDH.'+versiondots+'_'+homogtype+var+KL+'.txt'
    INSTATLIST   = INDIR+'goodforHadISDH.'+versiondots+'_'+homogtype+var+'_JAN2020'+KL+'.txt'
#    INADJLIST    = INDIR+'HadISDH.land'+var2+'.'+versiondots+'_'+homogtype+'.log' 
    # T IDPHA is Merged with PHA so homogtype is now IDPHAMG
    if (var == 't'):
 
        homogtype = homogtype+'MG'    
    
    INADJLIST    = INDIR+'HadISDH.land'+var2+'.'+versiondots+'_'+homogtype+'_JAN2020.log' 
    OUTPLOTS = OUTPLOTDIR+'HadISDH.land'+var2+'.'+versiondots+'_adjspread_'+homogtype+'_test'
    OUTADJS  = INDIR+'Largest_Adjs_land'+var2+'.'+versiondots+'_'+homogtype+'_test.txt'  

    # read in station list
    MyTypes          = ["|U6","|U5","float","float","float","|U4","|U30","|U7","int"]
    #MyTypes          = ("|S6","|S5","float","float","float","|S4","|S30","|S7","int")
    MyDelimiters     = [6,5,8,10,7,4,30,7,5]
    RawData          = ReadData(INSTATLIST,MyTypes,MyDelimiters)
    StationListWMO   = np.array(RawData['f0'])
    StationListWBAN  = np.array(RawData['f1'])
    StationListLat   = np.array(RawData['f2'])
    StationListLon   = np.array(RawData['f3'])
    StationListElev  = np.array(RawData['f4'])
    StationListCID   = np.array(RawData['f5'])
    StationListName  = np.array(RawData['f6'])
    nstations        = len(StationListWMO)

    # Set up arrays
    nyrs     = (int(edyear)+1)-int(styear)
    nmons    = nyrs*12
#    int_mons = indgen(nmons)

    # Read in adjustments into arrays
    Adj_Locs, Adj_Mags_Accum, Adj_Mags_Act, Adj_WMOs = GetAdjustmentArrays(INADJLIST, nmons, nstations, homogtype, StationListWMO, StationListWBAN)


# Calculate the required statistics
    # Very difficult to get a best fit gaussian to data with a missing middle as we have to assume something about the middle
    # Missing middle doesn't appear to be an issue for all - IDPHA for q and T appears to fill in, less so for RH
    # Get histogram of adjustments
    # Find middle - if there is a dip select all values between local peaks
    # Set these to the maximum of the other remaining values
    # Set the middle of the dip to GrowthFactor*max of remaining values to improve the amplitude gaussian fit. 
    # Find the max of the full histogram and mean and standard deviation of all adjustments
    # Find the best fit curve for the nanned version - set amp=np.max, cen=mean(adj), wid=sd(adj), set bounds to max+max*GrowthFactor (20%), mean+-0.1,st+/-0.2
    # It will likely fit to given lower bound
    # Get the curve using gaussian model
    # CHECK THE CURVE!!!
    # This sounds like a fudge but I set the middle value in IDL to ~4000 so its the same thing.
    
    # Get the histogram of adjustments for dataset
    BinSize = ParamDict[var][4]
    HistAdjMagsAct, Xarr, BinArray, MeanAdj, StdAdj, MaxFreq = GetHist(BinSize, Adj_Mags_Act)
#    print('Hist stats: ',MaxFreq, MeanAdj, StdAdj)
    
    # Find out if there is a dip or plateau in the middle
    # This depends on well behaved histograms that don't ahve any unusual peaks other than a missing middle.
    NewHistAdjMagsAct, FixingLow, FixingHigh = GetNewMiddle(HistAdjMagsAct, Xarr, BinSize, MeanAdj, MaxFreq) 
#    print('Did we need to fix middle? L? H?',FixingLow, FixingHigh)
        
    # If there is no dip or plateau just fit a gaussian anyway?
    
    # Get a best fit gaussian curve, with bounds if FixingLow or FixingHigh is True
    if (FixingLow) or (FixingHigh):

        # Add dip info to log file
        if (PlotOnly == False): # then we're getting all the stats
            
            filee = open(OUTPUTLOG,'a+')
            filee.write('%s%s%s%s\n' % (var,'_',homogtype,'_DIP_FOUND=True'))
            filee.close()

        bv, covar = curve_fit(Gaussian,Xarr,NewHistAdjMagsAct,p0=[MaxFreq,MeanAdj,StdAdj],bounds=([MaxFreq,MeanAdj-1.,StdAdj-1.],[MaxFreq*GrowthFactor,MeanAdj+1,StdAdj+1],))
        bvo, covaro = curve_fit(Gaussian,Xarr,HistAdjMagsAct,p0=[MaxFreq,MeanAdj,StdAdj])
#        print('Running with bounds because we found a dip')
        GaussCurve = Gaussian(Xarr,bv[0],bv[1],bv[2])
        GaussCurveOLD = Gaussian(Xarr,bvo[0],bvo[1],bvo[2])
	
    else:
    
        bv, covar = curve_fit(Gaussian,Xarr,NewHistAdjMagsAct,p0=[MaxFreq,MeanAdj,StdAdj])
        GaussCurve = Gaussian(Xarr,bv[0],bv[1],bv[2])
    
#    print('Check bv output for amp, mean, std and the best fit curve')
#    pdb.set_trace()
#    plt.clf()
#    plt.plot(Xarr,NewHistAdjMagsAct,'+')
#    plt.plot(Xarr,HistAdjMagsAct,'.')
#    plt.plot(Xarr,GaussCurve,'red')
#    if (FixingLow) or (FixingHigh):
#        plt.plot(Xarr,GaussCurveOLD,'grey')
#    plt.show()
#    pdb.set_trace()
    
    # Merge the GaussCurve and HistAdjMagsAct to pick up the maximum values in each case - the fatter tails of HistAdjMagsAct and the Missing Middle?
    MergeFit = np.maximum(HistAdjMagsAct,GaussCurve)

    # Get the difference between the MergeFit and HistAdjMagsAct
    DiffArr = MergeFit - HistAdjMagsAct
    
#    print('Check what happens when HistAdjMagsAct = 0 and the DiffArr')
#    plt.clf()
#    plt.plot(Xarr,NewHistAdjMagsAct,'+')
#    plt.plot(Xarr,HistAdjMagsAct,'.')
#    plt.plot(Xarr,GaussCurve,'red')
#    plt.plot(Xarr,MergeFit,'blue')
#    plt.plot(Xarr,DiffArr,'orange')
#    plt.show()
#    pdb.set_trace()
    
    # Convert the differences into values using the BinArray locations and numbers in DiffArr
    # DiffArr should not be less that 0 in any place
    DiffValsArr=[]
    for i,Num in enumerate(DiffArr):
        print(i,Num)
        
        if (np.round(Num) > 0):
	
            DiffValsArr = np.append(DiffValsArr,np.repeat((BinArray[i] + (BinSize / 2.)),np.round(Num)))
#            print('Check setting diff vals')
#            pdb.set_trace()
	      
# OUtput these stats if PlotOnly = False
    if (PlotOnly == False):
    
        OutPutStats(OUTPUTLOG, OUTADJS, Adj_Mags_Act, DiffValsArr, Adj_WMOs, var, homogtype, nstations)

# Make the Plots

    PlotAdjs(OUTPLOTS, HistAdjMagsAct, GaussCurve, MergeFit, DiffArr, DiffValsArr, Xarr, Adj_Locs, nmons, styear, edyear, ParamDict[var][1])

# Finish

if __name__ == '__main__':
    
    main(sys.argv[1:])

