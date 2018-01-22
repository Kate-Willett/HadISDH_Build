#!/usr/local/sci/bin/python
# PYTHON2.7
# 
# Author: Kate Willett
# Created: 11 October 2012
# Last update: 8 October 2015
# Location: /data/local/hadkw/ISTI/PROGS/	
# GitHub: https://github.com/SurfaceTemp/ISTI_Clean_Worlds/
# Location: /data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/PYTHON/	
# GitHub: https://github.com/Kate-Willett/Climate_Explorer/tree/master/PYTHON/
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# All code in this file calculates linear trends
#
# MedianPairwise:
#     Median of Pairwise slopes estimation of a linear trend
#     95 percent confidence intervals based on weighted percentiles linked to degrees of freedom
#     Copes with missing data
#     After Sen, 1961
#     Based on IDL code - Mark McCarthy
#
# 
# Sen, P. K.: Estimates of the regression coef?cient based on Kendall?s tau, J. Am. Stat. Assoc., 63, 1379?1389, 1968.
# Helsel and Hirsch 1995, Statistical Methods in Water Resources, page 273 http://pubs.usgs.gov/twri/twri4a3/pdf/twri4a3-new.pdf
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# Inbuilt: (may not all be required actually)
# import numpy as np
# import matplotlib.pyplot as plt
# import sys, os
# from scipy.optimize import curve_fit,fsolve,leastsq
# from scipy import pi,sqrt,exp
# from scipy.special import erf
# import scipy.stats
# from math import sqrt,pi
# import struct
# 
# -----------------------
# DATA
# -----------------------
# MedianPairwise:
#    TheData - a numpy array of data which can contain missing data
#    TheMDI - the missing data indicator
#    TheSlope - a 3 element array or list to contain [trend per time unit, lower bound confidence range, upper bound confidence rnage]
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# MedianPairwise:
#     from LinearTrends import MedianPairwise
#     TheSlope=[0.,0.,0.]
#     TheSlope=MedianPairwise(TheData,TheMDI,TheSlope)
#
# -----------------------
# OUTPUT
# -----------------------
# MedianPairwise:
# 	Outputs a 3 element list containing: 
#		the trend per 1 time unit, 
#		the lower bound of 95th conf, 
#		the upper bouund of 95th conf
#
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
# 
# Version 1 (8th October 2015)
# ---------
#  
# Enhancements
# Added catch and change to make sure ranks don't go below zero or exceed N
#  
# Changes
#  
# Bug fixes
# No -1 for rankL needed
#  
# -----------------------
# OTHER INFORMATION
# -----------------------
# This code was originally coded in IDL by Mark McCarthy
# An IDL version exists called median_pairwise.pro
#
#************************************************************************
# Set up python imports
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from scipy.optimize import curve_fit,fsolve,leastsq
from scipy import pi,sqrt,exp
from scipy.special import erf
import scipy.stats
from math import sqrt,pi
import struct

#************************************************************************
# Subroutines
#************************************************************************
# MedianPairwise
def MedianPairwise(TheData,TheMDI,TheSlope): # ,Lowee=Lowee,Highee=Highee):
    ''' Calculates slope from every point to every other point '''
    ''' Outputs the median of those slopes at a rate of unit per time step '''
    ''' Optionally outputs the 5th and 95th percentiles of those slopes as uncertainty ranges '''
    ''' If Lowee and/or Highee are set they will come out as changed values '''
    TheSlope=[0.,0.,0.]		# median, 5th adn 95th percentile rate of change per time step
    PairwiseSlopes=[]
    for i,ii in enumerate(TheData):
#        print i,ii
        if ii > TheMDI:
	    for r in range(len(TheData)-1,i,-1):
	        if TheData[r] > TheMDI:
		    PairwiseSlopes=np.append(PairwiseSlopes,((TheData[r]-ii)/(r-i)))
#		    print i,r,ii,TheData[r],(TheData[r]-ii)/(r-i)
    
#    print(len(PairwiseSlopes))
#    print "%5.2f"*len(PairwiseSlopes) % tuple(PairwiseSlopes)
    if len(PairwiseSlopes) > 10:	# check there are sufficient data
	TheSlope[0]=np.median(PairwiseSlopes)
        nData=len(list(TheData[np.where(TheData > TheMDI)]))
        DegofFree=(nData * (nData-1))/2.
	weight=np.sqrt(nData * (nData-1) * ((2*nData)+5) / 18.)
#	print "No. PW, No. Data Present, Deg Free ",len(PairwiseSlopes),nData, DegofFree
#	print "WEIGHT ", weight
        rankL=int(((DegofFree-1.96*weight)/2.))
        rankU=int(((DegofFree+1.96*weight)/2.)+1)

# Checks to make sure the ranks are actually sensible
        if (rankU >= len(PairwiseSlopes)):
	    rankU=len(PairwiseSlopes)-1
        if (rankU < 0):
	    rankU=0
        if (rankL < 0):
	    rankL=0

#	print "RANKS ",rankL,rankU
	PairwiseSlopes.sort()
	TheSlope[1]=PairwiseSlopes[rankL]
	TheSlope[2]=PairwiseSlopes[rankU]

         	
#        print(TheSlope)
#        num_bins = 50
#        # the histogram of the data
#        n, bins, patches = plt.hist(PairwiseSlopes, num_bins, normed=1, facecolor='green', alpha=0.5)
#        plt.show()
    
    ''' At present I think the 5th and 95th are too sensitive to variability '''
    ''' This is a quicklook Kate version of the code and needs to be statistically verified '''
    return  TheSlope # ReadData

#************************************************************************
