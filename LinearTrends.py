#!/usr/local/sci/bin/python
# PYTHON3
# 
# Author: Kate Willett
# Created: 11 October 2012
# Last update: 3 May 2019
# Location: /data/local/hadkw/ISTI/PROGS/	
# GitHub: https://github.com/SurfaceTemp/ISTI_Clean_Worlds/
# Location: /data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/PYTHON/	
# GitHub: https://github.com/Kate-Willett/Climate_Explorer/tree/master/PYTHON/
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# All code in this file calculates linear trends with the exception of CI_tINV which works out confidence intervals
#
# MedianPairwise:
#     Median of Pairwise slopes estimation of a linear trend
#     95 percent confidence intervals based on weighted percentiles linked to degrees of freedom
#     Copes with missing data
#     After Sen, 1961
#     Based on IDL code - Mark McCarthy
# 
# Sen, P. K.: Estimates of the regression coef?cient based on Kendall?s tau, J. Am. Stat. Assoc., 63, 1379?1389, 1968.
# Helsel and Hirsch 1995, Statistical Methods in Water Resources, page 273 http://pubs.usgs.gov/twri/twri4a3/pdf/twri4a3-new.pdf
#
#
# OLS_AR1Corr
#	Ordinary Least Squares fit of a linear trends
# 	90 pct (2sigma) confidence intervals from Standard Error of the slope of the trend adjusted for AR(1) correlation
#	Following the method of Santer et al., 2008 and compared with Alexei Kaplan's IDL code ltr_olsdofrnan.pro. I have
#       followed the formula set out in Santer et al, 2008 and included the modifications of Kaplan: 
#         slope and intercept are computed using only the non-missing values via converting missing data to NaNs and 'drop'ping the NaNs in the OLS function
#         we compute the sample AR(1) correlation coefficient as in SAnter et al., 2008 - e(1:N-1) and e(2:N) rather than Kaplan's e(ind) and e(ind+1)
#         when the AR(1) correlation is negative it is reset to 0 - as in Kaplan
#         when the effective degrees of freedo falls below 3 then the code returns missing data for the trend and slopes, - as in Kaplan
#
#       The 1 sigma standard error is returned and the 90th percentile confidence intervals based on Alexei's tinv.pro
#
#
#       For this we use statsmodels and pandas
#
# Santer, B. D., P. W. Thorne,  L. Haimberger,  K. E. Taylor,  T. M. L. Wigley,
# J. R. Lanzante,  S. Solomon,  M. Free,  P. J. Gleckler,  P. D. Jones,  T. R. Karl,
# S. A. Klein,  C. Mears,  D. Nychka,  G. A. Schmidt,  S. C. Sherwood, and  F. J. Wentz, 2008:
# Consistency of modelled and observed temperature trends in the tropcial troposphere. 
# International Journal of Climatology, 28 (13), 1703-1722.
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# Inbuilt: (may not all be required actually)
# import numpy as np
# import sys, os
# from scipy.optimize import curve_fit,fsolve,leastsq
# from scipy import pi,sqrt,exp
# from scipy.special import erf
# import scipy.stats
# from scipy.special import betainc
# from math import sqrt,pi
# import struct
#
# import statsmodels.api as sm
# import statsmodels.formula as smf
# import pandas as pd
# 
# -----------------------
# DATA
# -----------------------
# MedianPairwise:
#    TheData - a numpy array of data which can contain missing data
#    TheMDI - the missing data indicator
#    TheSlope - a 3 element array or list to contain [trend per time unit, lower bound confidence range, upper bound confidence rnage]
# 
# OLS_AR1Corr
#    TheData - a numpy array of data which can contain missing data
#    TheMDI - the missing data indicator
#    TheConfRange: a number between 0 and 1 for the desired confidence interval e.g. 0.9 for 90th pct CI '''
#
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# MedianPairwise:
#     from LinearTrends import MedianPairwise
#     TheSlope=[0.,0.,0.]
#     TheSlope=MedianPairwise(TheData,TheMDI,TheSlope)
#
#
# OLS_AR1Corr:
#     from LinearTrends import OLS_AR1Corr
#     TheSlope=OLS_AR1Corr(TheData,TheMDI,ThePvalue)
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
# OLS_AR1Corr:
# 	Outputs a 7 element list containing: 
#		the trend per 1 time unit, 
#		the lower bound of 90th conf interval (5th percentile), (obtained using inverse students t CDF) 
#		the upper bouund of 90th conf interal 995th percentil) (as above)
#               the 1 sigma standard error
#               the +/- Confidence Interval for a given probability range (0 to 1)
#               the AR(1) correlation of regression residuals
#               the effective degrees of freedom
#               the p-value for the trend 
#
#
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
#
# Version 5 2nd Nov 2020
# ---------
#  
# Enhancements
# Now outputs the p-value for the OLS trend following Alexei Kaplan's IDL code
#  
# Changes
#  
# Bug fixes
#
# Version 4 6th Aug 2020
# ---------
#  
# Enhancements
#  
# Changes
#  
# Bug fixes
# I had misinterpretted case of AR(1) < 0
# In this case AR(1) should be set to 0 so it has no impact on deg of freedom - I had set it to trend = MDI
#
# Version 3 13th Jan 2020
# ---------
#  
# Enhancements
# NOw added OLS_AR1Corr which utilises statsmodels.formula and pandas
# This has been checked against Alexei Kaplan's IDL code and found to match to the first three decimal places at least.
#  
# Changes
# This now refuses to fit an OLS trend if > 50% of data are missing (it was 100% of data missing)
#  
# Bug fixes
#
# Version 2 3rd May 2019
# ---------
#  
# Enhancements
#  
# Changes
# Now python 3
#  
# Bug fixes
#
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
# The median pairwise code was originally coded in IDL by Mark McCarthy
# An IDL version exists called median_pairwise.pro
#
# Just playing with slopes
# moo = np.random.rand(100) # 100 random numbers between 0 and 1
# moo = np.sin(np.arange(100)) # 100 numbers between 0 and 1 with a sine curve
# moo = np.sin(np.random.normal(np.zeros(100))) # 100 normally distributed numbers with a mean of 0 and a sine curve
# moo = [(i*0.1)+ii for i,ii in enumerate(moo)] # adding a trend
#
# Testing IPCC Data - for IDL version see Desktop/IPCCAR6/ltr_OLSdofrNaN_code/
# Uncomment the print statements!!!
# > module load scitools/default_current - this loads Python 3.6.8
# > import numpy as np
# > from LinearTrends import OLS_AR1Corr
# > MyData = np.genfromtxt('TESTDATA/data4S2008comp.dat')
# > moo = np.array([i[1] for i in MyData]) - this is HadCRUT3v
# > Slopes = OLS_AR1Corr(moo,-1e30,0.9)
# Trend = 0.1188
# 1-sigS.E. = 0.1172
# Autocorrelation at lag 1 = 0.9342
# No of effective deg of freedom = 8.57
# 90th pct CI = 0.224 
# MATCH!
# > moo = np.array([i[2] for i in MyData]) - this is HadISST1
# > Slopes = OLS_AR1Corr(moo,-1e30,0.9)
# Trend = 0.1081
# 1-sigS.E. = 0.1331
# Autocorrelation at lag 1 = 0.9438
# No of effective deg of freedom = 7.29
# 90th pct CI = 0.265 
# MATCH!
# > moo = np.array([i[3] for i in MyData]) - this is ERSST-v2
# > Slopes = OLS_AR1Corr(moo,-1e30,0.9)
# Trend = 0.100
# 1-sigS.E. = 0.1308
# Autocorrelation at lag 1 = 0.9466
# No of effective deg of freedom = 6.918
# 90th pct CI = 0.265 
# MATCH!
# > moo = np.array([i[4] for i in MyData]) - this is ERSST-v3
# > Slopes = OLS_AR1Corr(moo,-1e30,0.9)
# Trend = 0.077
# 1-sigS.E. = 0.1207
# Autocorrelation at lag 1 = 0.9363
# No of effective deg of freedom = 8.2958
# 90th pct CI = 0.233 
# MATCH!

#
#************************************************************************
# Set up python imports
import numpy as np
#import matplotlib.pyplot as plt
import sys, os
from scipy.optimize import curve_fit,fsolve,leastsq
from scipy import pi,sqrt,exp
from scipy.special import erf
import scipy.stats
from scipy.special import betainc # COMPARES VERY VERY CLOSELY WITH IDL IBETA()
from math import sqrt,pi
import struct
import pdb

import statsmodels.api as sm
import statsmodels.formula.api as smf
# >dir(smf) prints list of available models. Lower case ones accept formula 
# and df (for pandas data frame) arguments. Upper case take endog and exog design matrices. 
import pandas as pd

#************************************************************************
# Subroutines
#************************************************************************
# OLS_AR1Corr
def OLS_AR1Corr(TheData,TheMDI,TheConfRange): # ,Lowee=Lowee,Highee=Highee):
    ''' Calculates the linear trend using Ordinary Least Squares regression '''
    ''' Can cope with specified missing data indicator TheMDI '''
    ''' TheData: a numpy array of single time series data  - can have missing data = TheMDI'''
    ''' TheMDI: a number used to identify missing data (not NaN) '''
    ''' TheConfRange: a number between 0 and 1 for the desired confidence interval e.g. 0.9 for 90th pct CI '''
    ''' TheSlope[0]: Outputs the slope at a rate of unit per time step '''
    ''' TheSlope[1:3]: Outputs the 5th and 95th pctile standard error confidence intervals 
        (90pct confidence intervals) around the slope corrected for AR(1) correlation '''
    ''' TheSlope[3]: Outputs the 1 sigma standard error '''
    ''' TheSlope[4]: Outputs the +/- Confidence Interval for the given p-value '''
    ''' TheSlope[5]: Outputs the AR(1) correlation of regression residuals '''
    ''' TheSlope[6]: Outputs the effective degrees of freedom '''
    ''' TheSlope[7]: Outputs the p-value of the trend using two-sided students t test - can we reject H0 of no trend '''
    ''' Santer et al., 2008 - methodology '''
    ''' If Lowee and/or Highee are set they will come out as changed values '''
    ''' THis is intended to be identical to Alexey Kaplans IDL code which is almost identical to Samter et al '''
    ''' I have tested this with TESTDATA/data4S2008comp.dat and the IDL code and get identical values '''
    ''' The Kaplan code invokes a different method for missing data: '''
    '''      Data are compressed to only non-missing and then processed '''
    '''      I will test both running my method with missing data and compressing then running '''
    ''' The Kaplan method adds two caveats which I will add here: '''
    '''      If autocorrelation is -ve then set to 0 '''
    '''      If the effective Deg of Freedom < 3 then Inf or NaN are returned '''
    ''' Something else about the regression residuals using indices but I don't understand '''

    # Check the desired confidence range is between 0-1
    if ((TheConfRange < 0.) | (TheConfRange > 1.)):
        raise Exception("invalid confidnece range - should be between 0 and 1")    

    # Set up empty list for returning the output values
    #    - slope per unit time,
    #    - lower (10th pct) CI,
    #    - upper (90th pct) CI]
    #    - 1 sigma SE
    #    - The +/- confidence interval for the given p value
    #    - AR(1) correlation in the residuals
    #    - the effective degrees of freedom
    #    - the p-value for the trend
    TheSlope=np.array([0.,0.,0.,0.,0.,0.,0.,0.])		

    # Convert the data to a pandas dataframe?
    # First set any missing values to NaNs
    TheDataNANs = np.copy(TheData) # copying just to be safe
    gots = np.where(TheDataNANs == TheMDI)

    # ADD A CATCH FOR No. Data points < 3 as in KAPLAN (actually I'm setting it to 50% missing!!!
    if ((float(len(gots[0]))/float(len(TheData))) > 0.5):
        TheSlope[0:8] = TheMDI
        print('Fewer than 50% valid data points')
#        pdb.set_trace()
        return TheSlope
    # Tested
    
    if (len(gots[0]) > 0):
        TheDataNANs[np.where(TheDataNANs == TheMDI)] = float('NaN')
    DataDF = pd.DataFrame(TheDataNANs, index=np.arange(len(TheDataNANs)),columns=['variable'],dtype=float,copy=True)
    # This needs to be a copy otherwise changes to TheData lead to changes to DataDF.variable[]
    
    # As we are using formula= then we don't need to specify a column of 1s and an intercept is calculated
    olsmod = smf.ols(formula='variable ~ np.arange(len(TheDataNANs))',data=DataDF,missing='drop') # drop the NaNs
    olsres = olsmod.fit()
    # olsmod.summary() prints all
    # olsmod.params prints the slopes for each item 0 = intercept, 1 = variable
    # olsmod.predict() prints the predicted values using the model fit, including intercept
    # olsmod.bse prints the standard errors (1 sigma using n-2 degrees of freedom) 0 = intercept, 1 = variable
    TheSlope[0] = olsres.params[1]
#    print('Decadal Trend: ',np.round(TheSlope[0]*120,4))
    #pdb.set_trace()
    
    # Now get the original 1 sigma standard error which uses n-2 degrees of freedom and then calculate the corrected one
    # First we need to use masked arrays to make sure we account for missing data
    TheDataMSK = np.ma.masked_equal(TheData,TheMDI) # better hope that this captures them all and nothing silly with floats
    
    # Now get the time series of regression residuals for each data point
    # First create a masked array of missing data
    TheResids = np.ma.masked_equal(np.repeat(TheMDI,len(TheDataMSK)),TheMDI)
    # Get a pointer array to the non-missing data but need to test if there are any missing first
    if (np.ma.count(TheDataMSK) == len(TheData)):
        print('no missing')
        # then we do not need to faff with the missing data
        # Subtract the predicted values for each time point from the actual values
        TheResids = TheDataMSK - olsres.predict() # if there are missing values then these won't be predicted so we need to fill back in
        MaskofPoints = np.arange(len(TheData))
    
    else:
        # we do need to faff with the missing data
        print('got a missing')
        MaskofPoints = np.where(np.ma.getmask(TheDataMSK) == False)
        # Subtract the predicted values for each time point from the actual values
        TheResids[MaskofPoints] = TheDataMSK[MaskofPoints] - olsres.predict() # if there are missing values then these won't be predicted so we need to fill back in

    # We need the AR(1) values of the regression residuals and shoudl probably test to make sure the data are autocorrelated
    # Using the np.ma.corrcoef works even if all data are present
    # This ignores missing data points so isn't ideal - better to take the longest continuous period of data?
    Lag1AR = np.ma.corrcoef(TheResids[0:-1],TheResids[1:])[0][1]
    TheSlope[5] = Lag1AR
#    print('Autocorrelation at lag 1: ',np.round(Lag1AR,4)) 
    #pdb.set_trace()

    # ADD A CATCH FOR NEGATIVE AR(1) - as in Kaplan
    # ERROR - If AR(1) is negative then it should be given a value of 0 so it has no effect on reducing deg of freedom
    # previously I had set the trends to MDI - IDIOT!!!
    if (Lag1AR < 0.):
        Lag1AR = 0.
	#TheSlope[0:5] = TheMDI
        #TheSlope[6] = TheMDI
#        print('Negative AR(1)')
        #return TheSlope
    # Tested
    
    # This is the original number of samples of time NOT INCLUDING MISSING DATA POINTS
    nORIG = np.ma.count(TheDataMSK) # number of data points
    
    # Now get the effective number of samples dependent on the degree of autocorrelation at lag 1
    nEFF = nORIG * ((1 - Lag1AR) / (1 + Lag1AR))
    TheSlope[6] = nEFF
#    print('Original no. time points: ',nORIG)
#    print('Effective no. time points: ',np.round(nEFF,4))
    #pdb.set_trace()

    # ADD A CATCH FOR nEFF < 3 as in KAPLAN
    if (nEFF < 3):
        TheSlope[1:6] = TheMDI
        TheSlope[7] = TheMDI
#        print('Fewer than 3 effective degrees of freedom: ',nEFF)
        return TheSlope
    # Tested
    
    # Now get the variance of the regression residuals s_e^2
    s_eSQ = (1 / (nEFF - 2)) * np.ma.sum(TheResids**2)
    # and just for comparison get it for the original number of samples
    s_eSQORIG = (1 / (nORIG - 2)) * np.ma.sum(TheResids**2)

#    print('Decade Original variance of regression residuals: ',np.round(s_eSQORIG*120,4))
#    print('Decade Effective variance of regression residuals: ',np.round(s_eSQ*120,4))
    #pdb.set_trace()
    
    # Now calculate the 1 sigma standard error
    s_1sig = (s_eSQ / np.sum((MaskofPoints - np.mean(MaskofPoints))**2))**0.5
    # and just for comparison get it for the original number of samples
    s_1sigORIG = (s_eSQORIG / np.sum((MaskofPoints - np.mean(MaskofPoints))**2))**0.5
    TheSlope[3] = s_1sig

#    print('Decade Original 1 sigma standard error: ',np.round(s_1sigORIG*120,4))
#    print('Decade Effective 1 sigma standard error: ',np.round(s_1sig*120,4))
    #pdb.set_trace()

#   Now calculate the p-value to test whether the H0 (no trend) is rejected (if p-value < 0.05)
    t_students_2tail = TheSlope[0] / s_1sig
    integration_lev = (nEFF - 2.0) / ((nEFF - 2.0) + t_students_2tail**2.)
    TheSlope[7] = betainc((nEFF - 2.0)/2., 0.5, integration_lev)
#    pdb.set_trace()
    
    # Now find the 90th percentile confidence intervals by integrating the area under the assumed curve
    # and populate TheSlope array with the lower and upper bound 
    # I INCORRECTLY assumed that this is slope - 2*s_1sig and slope + 2*s_1sig - this would actually be 95pct confidence intervals approximately
    # This uses the inverse of students t CDF (quantile function) using the bisection method of the incomplete beta function (scipy.special.betainc)
    # When later the slope may be multiplied to get decadal trend the standard errors should be multiplied likewise
    ConfInt = CI_tINV(s_1sig, TheConfRange, nEFF)
    TheSlope[4] = ConfInt
#    print('Confidence interval for the p-value ', ThePvalue,' :',np.round(ConfInt*120,4))
    TheSlope[1] = TheSlope[0] - ConfInt
    TheSlope[2] = TheSlope[0] + ConfInt

#    print('Decade AR(1) corrected 90th pct standard error confidence intervals: ',np.round(TheSlope[1]*120,4),np.round(TheSlope[2]*120,4))
    #pdb.set_trace()
    
    return  TheSlope # ReadData

#***********************************************************************
# CI_tINV
def CI_tINV(sig1SE,plev,DoF):
    ''' Calculates the +/- confidence interval of a given p-value (e.g. 90th pct 0.9 or 95th pct 0.95)
        around the estimated value (e.g., mean or linear trend '''
    ''' e.g., p = 0.9 therefore we expect 90% of the likely values of the linear trend to lie within this bound
        or that there is a 90% chance that these bounds incorporate the true linear trend value '''
    ''' 1 in ten of times we estimate this the trend might be outside of these bounds '''
    ''' This uses the same method as A. Kaplan: '''
    ''' The inverse student's t CDF (quantile function) is used with the bisection method (incomplete beta function)
         to estimate the area under the curve '''
    ''' sig1SE = 1 sigma standard error '''
    ''' plev = 0.9 or 0.95 or 0.99 - a desired probability level of which we want to bound the estimated trend to capture the 
        true trend - this becomes 0.5*pval/2.0 '''
    ''' DoF = degrees of freedom (NOTE when used with AR(1) correction this should be the effective deg of freedom) - this becomes DoF - 2 '''
    
    # Set up working values
    Working_plev = 0.5 + plev / 2.0
    Reduced_DoF = DoF - 2
    
    # Halve Degrees of Freedom
    HalfReduced_DoF = Reduced_DoF / 2.
    
    # Set the maximum number of iterations
    Maxit = 30
    
    # Set up the bounds for integration?
    x1 = 0.
    x2 = 1.0
    
    fv = 2.0 * (1.0 - Working_plev)
    
    # Compute the incomplete beta integral of the HalfReduced_DoF and 0.5 between 0 and x1 (0) 
    f1 = betainc(HalfReduced_DoF, 0.5, x1) - fv

    # Compute the incomplete beta integral of the HalfReduced_DoF and 0.5 between 0 and x2 (1)
    f2 = betainc(HalfReduced_DoF, 0.5, x2) - fv
    
    # Now iterate to work out the area under the curve
    for i in range(Maxit):
        
        xm = (x1 + x2) / 2.0 # this sets the integration level for each step
        fm = betainc(HalfReduced_DoF, 0.5, xm) - fv
	
        if ((f1*fm) < 0.0):
            x2 = xm
            f2 = fm
	    
        else:
            x1 = xm
            f1 = fm	
	
    tinv2 = (1.0 / xm - 1.0) * Reduced_DoF
    tinv = np.sqrt(tinv2)
	   
    ConfInt = sig1SE * tinv
    
    #pdb.set_trace()

    return ConfInt

#*******************************************************************************
# MedianPairwise
def MedianPairwise(TheData,TheMDI,TheSlope): # ,Lowee=Lowee,Highee=Highee):
    ''' Calculates slope from every point to every other point '''
    ''' Outputs the median of those slopes at a rate of unit per time step '''
    ''' Optionally outputs the 2.5th and 97.5th percentiles (95% confidence) of those slopes as uncertainty ranges '''
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
        #pdb.set_trace()
        rankL=int(((DegofFree-1.96*weight)/2.)) # NO -1 because int() floors the data rather than rounding
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
