#!/usr/local/sci/bin/python
# PYTHON3.6
# 
# Author: Kate Willett
# Created: 8 January 2016
# Last update: 11 April 2019
# Location: /data/local/hadkw/HADCRUH2/MARINE/EUSTACEMDS/EUSACE_SST_MAT/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Marine_Build/
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# This code takes works out nice time arrays for datasets
#
# make_days_since produces an array of integer day counts 
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# Python:
# import numpy as np
# import sys, os
# import scipy.stats
# import struct
# import os.path
# import datetime as dt
# from datetime import datetime
# import pdb # pdb.set_trace() or c
#
# -----------------------
# DATA
# -----------------------
# Feed the selected function start and end date
# make_days_since: start year, start month, end year, end month (integers), interval (day, month, year - string)
# This assumes 15th of month for 'month' and June 28th for 'year'
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# module load scitools/experimental-current
# python
#
# from GetNiceTimes import MakeDaysSince
# NiceTimes = GetNiceTimes.MakeDaysSince(1973,1,2017,12,'month') # use 'day','pentad', 'month','year'
# 
# -----------------------
# OUTPUT
# -----------------------
# a numpy array of times
#
# make_days_since returns integers
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
# 
# Version 2 11th Apr 2019
# ---------
#  
# Enhancements
# This can now work with pentads
#  
# Changes
#  
# Bug fixes
#
# Version 1 4th Feb 2019
# ---------
#  
# Enhancements
# This is now stand alone functions rather than within WriteNetCDF_CEDAESGF_JAN2016.py (/data/local/hadkw/HADCRUH2/UPDATE2017/PROGS/PYTHON/)
#  
# Changes
# Provide a time interval to specify the return values so that this can work with daily, monthly and annual data
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
import scipy.stats
import struct
import os.path
import datetime as dt
from datetime import datetime
import pdb # pdb.set_trace() or c

# Set up hardwired variables
MonthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
PentadDays = list(np.repeat(5,73))

#************************************************************************
# Subroutines
#************************************************************************
# MakeDaysSince
def MakeDaysSince(TheStYr,TheStMon,TheEdYr,TheEdMon,TheInterval,Return_Boundaries = False):
    ''' Take counts of months since TheStYr, TheStMon (assume 15th day of month or June 28th of year) '''
    ''' Incl leap days '''
    ''' Also work out time boundaries 1st and last day of month and return if Return_Boundaries = True'''
    ''' This can cope with incomplete years or individual months '''
    ''' INPUTS: '''
    ''' TheStYr = int start year '''
    ''' TheStMon = int start month from 1 to 12 or 73'''
    ''' TheEdYr = int end year '''
    ''' TheEdMon = int end month from 1 to 12 or 73'''
    ''' TheInterval = string of 'day', 'pentad', 'month' or 'year' to set time interval '''
    ''' ONLY SET UP FOR MONTHLY AT THE MOMENT '''
    ''' Return_Boundaries = boolean True to return a numpy array of time boundaries or False (default) to not '''
    ''' OUTPUTS: '''
    ''' TheTimes = an integer np array of days using the given interval '''
    ''' OPTIONALLY = an integer np array (ntims, 2) of start and end boundaries of time interval '''
    
    # set up arrays for month/pentad mid points and month bounds
    DaysArray = np.empty(((TheEdYr-TheStYr)+1)*((TheEdMon-TheStMon)+1))
    if Return_Boundaries:
        BoundsArray = np.empty((((TheEdYr-TheStYr)+1)*((TheEdMon-TheStMon)+1),2))
    
    # make a date object for each time point and subtract start date
    StartDate = datetime(TheStYr,TheStMon,1,0,0,0)	# 1st of month
    TheYear = TheStYr
    TheMonth = TheStMon
    
    if (TheInterval == 'month'):
        for mm in range(len(DaysArray)):
            if (TheMonth < 12):
                DaysArray[mm] = (datetime(TheYear,TheMonth+1,1,0,0,0) - datetime(TheYear,TheMonth,1,0,0,0)).days/2. + (datetime(TheYear,TheMonth,1,0,0,0) - StartDate).days
                if (Return_Boundaries):
                    BoundsArray[mm,0] = (datetime(TheYear,TheMonth,1,0,0,0) - StartDate).days+1
                    BoundsArray[mm,1] = (datetime(TheYear,TheMonth+1,1,0,0,0) - StartDate).days
            else:
                DaysArray[mm] = (datetime(TheYear+1,1,1,0,0,0) - datetime(TheYear,TheMonth,1,0,0,0)).days/2. + (datetime(TheYear,TheMonth,1,0,0,0) - StartDate).days	
                if (Return_Boundaries):
                    BoundsArray[mm,0] = (datetime(TheYear,TheMonth,1,0,0,0) - StartDate).days+1
                    BoundsArray[mm,1] = (datetime(TheYear+1,1,1,0,0,0) - StartDate).days
            TheMonth = TheMonth+1
            if (TheMonth == 13):
                TheMonth = 1
                TheYear = TheYear + 1

    if (TheInterval == 'pentad'):
        ThePT = 0
        TheMonth = 0
        DayMid = -2
        for pp in range(len(DaysArray)):
	    
	    # Have we just gone over a year boundary - in which case reset
            if (ThePT > 72):
                ThePT = 0
                TheMonth = 0
                DayMid = -2
                TheYear = TheYear + 1
	         	    
	    # get the pointers for days and months
            DayMid = DayMid + 5
            if (DayMid > MonthDays[TheMonth]):
                DayMid = DayMid - MonthDays[TheMonth]
                TheMonth = TheMonth + 1
		
            #print('Check pentad: ',pp, ThePT, TheMonth, DayMid, TheYear)
            
            DaysArray[pp] = (datetime(TheYear,TheMonth+1,DayMid,0,0,0) - StartDate).days + 0.5
            
            if (Return_Boundaries):
                BoundsArray[mm,0] = DaysArray[pp]-2.5
                BoundsArray[mm,1] = DaysArray[pp]+2.5

            ThePT = ThePT + 1
	    
    if Return_Boundaries:
        return DaysArray, BoundsArray
    else:
        return DaysArray	

##########################################################################################
