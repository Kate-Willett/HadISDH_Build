# python 3
# 
# Author: Kate Willett
# Created: 18 January 2019
# Last update: 24 January 2019
# Location: /data/local/hadkw/HADCRUH2/MARINE/EUSTACEMDS/EUSTACE_SST_MAT/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Marine_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# This code creates the gridbox sampling uncertainty (1 sigma***) for each gridbox based on
# monthly mean variability, correlation and the number of stations/pseudostations
# 
# It can be used with land or marine HadISDH data
# 
# The sampling uncertainty follows the methodology applied for HadISDH-land which
# in turn follows Jones et al., 1999
#
# Willett, K. M., Williams Jr., C. N., Dunn, R. J. H., Thorne, P. W., Bell, 
# S., de Podesta, M., Jones, P. D., and Parker D. E., 2013: HadISDH: An 
# updated land surface specific humidity product for climate monitoring. 
# Climate of the Past, 9, 657-677, doi:10.5194/cp-9-657-2013. 
#
# Jones, P. D., Osborn, T. J., and Briffa, K. R.: Estimating sampling
# errors in large-scale temperature averages, J. Climate, 10, 2548–
# 2568, 1997.
#
# -----------------------
# LIST OF MODULES
# -----------------------
# import os
# import datetime as dt
# import numpy as np
# import sys
# import math
# from math import sin, cos, sqrt, atan2, radians
# import scipy.stats
# import matplotlib.pyplot as plt
# matplotlib.use('Agg') 
# import calendar
# import gc
# import netCDF4 as ncdf
# import copy
# import pdb
#
# Kate:
# from ReadNetCDF import GetGrid
# from ReadNetCDF import GetGrid4
#
# INTERNAL:
# 
# 
# -----------------------
# DATA
# -----------------------
# TheAnomsArr: times,lat,lon array of anomalies with TheMDI missing data
# TheLatsArr: nlats array of gridbox latitude centres from SOUTH to NORTH???
# TheLonsArr: nlons array of gridbox longitude centres from WEST to EAST???
# TheMeanNPoints: lat,lon array of npoints making up the gridbox average
# TheNPoints: times,lat,lon array of nstations or npoints making up the gridbox average
# TheMDI: scalar missing data ID
# IsMarine: boolean true for marine data and false for land data
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# >module load scitools/default-current
# >python 
# >import gridbox_sampling_uncertainty as gsu 
# > SESQArr, rbarArr, sbarSQArr = gsu.calc_sampling_unc(TheAnomsArr,TheLatsArr,TheLonsArr,TheMeanNPointsArr,TheNPointsArr,TheMDI,IsMarine)
#
# TheAnomsArr: times,lat,lon array of anomalies with TheMDI missing data
# TheLatsArr: nlats array of gridbox latitude centres from SOUTH to NORTH???
# TheLonsArr: nlons array of gridbox longitude centres from WEST to EAST???
# TheMeanNPoints: lat,lon array of npoints making up the gridbox average
# TheNPoints: times,lat,lon array of nstations or npoints making up the gridbox average
# TheMDI: scalar missing data ID
# IsMarine: boolean true for marine data and false for land data
#    
# This code hardwires:
# StYr = 1973 # Start year of dataset (assumes Jan to Dec complete for each year)
# ClimStart = 1981 # Start year of climatology
# ClimEnd = 2010 # End year of climatology
#    
# RETURNS:
# SESQArr: times, lat, lon array of 1 sigma sampling uncertainty with TheMDI missing data
# rbarArr: lat, lon array of average intersite correlation of gridbox with TheMDI missing data
# sbarSQArr: lat, lon array of mean station variance within gridbox with TheMDI missing data '''
#

# -----------------------
# OUTPUT
# -----------------------
#
# SESQArr: times, lat, lon array of 1 sigma sampling uncertainty with TheMDI missing data
# rbarArr: lat, lon array of average intersite correlation of gridbox with TheMDI missing data
# sbarSQArr: lat, lon array of mean station variance within gridbox with TheMDI missing data '''
#
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
# 
## Version 2 (18 January 2021)
# ---------
#  
# Enhancements
#  
# Changes
# Now has start and end year and start and end climatology year passed into it so nothing is hardcoded within
# Now uses HadCRUT.4.3.0.0.land_fraction.nc instead of new_coverpercent08.nc to provide land fraction (now 0-1, not 0-100)
# because this has far more detail of islands and inland waters and is used for the land data.
#  
# Bug fixes
# A check to make sure latitude order is same for data and land mask
# Added in case where >=120 months of data but no data for that particular point in time - was resulting in missing data when other missing data points were infilled.
# NOW NEED TO MASK TO ONLY PRESENT DATA I THINK WHEN USING. I WANT TO DO THIS FOR LAND SO WILL ADD TO f13_GriHadISDHFLAT.py IF I DECIDE TO DO THIS FOR MARINE TOO THEN BRING INTO THIS CODE
#

# Version 1 (24 January 2018)
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
# This builds on original IDL code written for HadISDH-land by Kate Willett calp_samplingerrorJUL2012_nofill.pro
#
################################################################################################################
# IMPORTS:
import os
import datetime as dt
import numpy as np
import sys
import math
from math import sin, cos, sqrt, atan2, radians
import scipy.stats
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import calendar
import gc
import netCDF4 as ncdf
import copy
import pdb

# Kate:
from ReadNetCDF import GetGrid
from ReadNetCDF import GetGrid4

################################################################################################################
# SUBROUTINES #
################################################################################################################
# calc_sampling_unc #
##################################################
def calc_sampling_unc(TheAnomsArr,TheLatsArr,TheLonsArr,TheMeanNPointsArr,TheNPointsArr,TheMDI,IsMarine,StYr,EdYr,ClimStart,ClimEnd):
    '''Applies the Jones et al 1997 sampling uncertainty methodology for gridded data with n_stations info
    TheAnomsArr: times,lat,lon array of anomalies with TheMDI missing data
    TheLatsArr: nlats array of gridbox latitude centres from SOUTH to NORTH???
    TheLonsArr: nlons array of gridbox longitude centres from WEST to EAST???
    TheMeanNPointsArr: lat,lon array of npoints making up the gridbox average
    TheNPointsArr: times,lat,lon array of nstations or npoints making up the gridbox average
    TheMDI: scalar missing data ID
    IsMarine: boolean true for marine data and false for land data
    StYr: integer start year
    EdYr: integer end year
    ClimStart: integer start year of climatology
    ClimEnd: integer end year of climatology
    
    This code hardwires:
    StYr = 1973 # Start year of dataset (assumes Jan to Dec complete for each year)
    ClimStart = 1981 # Start year of climatology
    ClimEnd = 2010 # End year of climatology
    
    RETURNS:
    SESQArr: times, lat, lon array of 1 sigma sampling uncertainty with TheMDI missing data
    rbarArr: lat, lon array of average intersite correlation of gridbox with TheMDI missing data - forced to be 0.8 if cannot be evaluated (mid-range - was 0.1 but this gives tiny SE**2 values)
    sbarSQArr: lat, lon array of mean station variance within gridbox with TheMDI missing data  - forced to be 10 if cannot be evaluated (large)'''
      
# Open land sea mask and set up - reverse lats?
#    Filee = '/project/hadobs2/hadisdh/marine/otherdata/new_coverpercentjul08.nc'
    Filee = '/project/hadobs2/hadisdh/marine/otherdata/HadCRUT.4.3.0.0.land_fraction.nc'
#    ReadInfo = ['pct_land']
    ReadInfo = ['land_area_fraction']
#    LatInfo = ['latitudes']
#    LonInfo = ['longitudes']
    LatInfo = ['latitude']
    LonInfo = ['longitude']
    PctLandTmp = GetGrid(Filee,ReadInfo,LatInfo,LonInfo)
#    PctLand = PctLandTmp[0]
    PctLand = np.reshape(PctLandTmp[0],(len(TheLatsArr),len(TheLonsArr)))
    # OLD: This comes out as (lats{87.5N to 87.5S],lons[-177.5W to 177.5E]) and is 100&% over land
    # NEW: This comes out as (lats{-87.5S to 87.5N],lons[-177.5W to 177.5E]) and is 100&% over land
    # If lats for data are not S to N then need to flip
    if (TheLatsArr[0] > 0.): # then PctLand needs flipping
    
        PctLand = np.flip(PctLand,axis=0)
    
# Set up time infor
    Ntims = len(TheAnomsArr[:,0,0])
#    StYr = 1973
#    ClimStart = 1981
#    ClimEnd = 2010
#    EdYr = int(StYr + (Ntims / 12)) - 1
    ClimMonSt = (ClimStart - StYr) * 12 # start point of climatology in months
    ClimMonEd = ((ClimEnd + 1) - StYr) * 12 # end point of climatology in months

# Set up lat and lon info
    Nlats = len(TheAnomsArr[0,:,0])
    Nlons = len(TheAnomsArr[0,0,:])
    LtHalf = abs(TheLatsArr[1] - TheLatsArr[0]) / 2.
    LtFull = abs(TheLatsArr[1] - TheLatsArr[0])
    LnHalf = abs(TheLonsArr[1] - TheLonsArr[0]) / 2.
    LnFull = abs(TheLonsArr[1] - TheLonsArr[0])
    NGaussLtBx = int((15.*2) / LtFull) # this will be 6 for 5by5 box - 3 boxes north and 3 boxes south then + candidate box
    NGaussLnBx = int((25.*2) / LnFull) # this will be 10 for 5by5 box - 5 boxes east and 5 boxes west then + candidate box
    #print("Lat/Lon info as expected? ",Nlats, Nlons, LtHalf, LtFull, LnHalf, LnFull, NGaussLtBx, NGaussLnBx)
    # yes
    
    EarthRadius = 6371 # Radius of the earth in km
    
# Set up empty arrays for key variables

    # Shat^2 variance of gridbox means over climatology period
    ShatSQArr = np.empty((Nlats,Nlons),dtype = float)
    ShatSQArr.fill(TheMDI)

    # Xo correlation decay distance (km) of gridbox (where correlation = 1/e)
    XoArr = np.empty((Nlats,Nlons),dtype = float)
    XoArr.fill(TheMDI)

    # Xdiag diagonal distance (km) from SW to NE of gridbox
    XdiagArr = np.empty((Nlats,Nlons),dtype = float)
    XdiagArr.fill(TheMDI)

    # rbar average intersite correlation of gridbox (estimated or forced to be 0.8)
    rbarArr = np.empty((Nlats,Nlons),dtype = float)
    rbarArr.fill(TheMDI)

    # Sbar^2 mean station variance within gridbox (estimated or forced to be 10)
    sbarSQArr = np.empty((Nlats,Nlons),dtype = float)
    sbarSQArr.fill(TheMDI)
    
    # SE^2 sampling error of gridbox
    SESQArr = np.empty((Ntims,Nlats,Nlons),dtype = float)
    SESQArr.fill(TheMDI)
        
# 1st Loop through each gridbox to calculate the variables where we have data
    # For each long and lat:
    for Nln,ln in enumerate(TheLonsArr):
        for Nlt,lt in enumerate(TheLatsArr):
	
            # Calc Xdiag diagonal distance from SW to NE of gridbox
	    # This is the Haversine method so assumes perfect sphere
	    # Should really use Vincenty method which uses eliptoidal model
	    # geopy.distance.distance would do this automatically but its not in scitools/experimental-current
	    # NOTE: This method DOES NOT WORK for nearly antipodial points (e.g. lat -2.5 to 2.5 and lon -107.5 72.5)
	    # These are generally very large distances with correlation most likely to be very low - dlon approaches pi
	    # Therefore where the longitude distance is greater than 3.1 I just skip!!!
	    # THIS ISN@T A PROBLEM HERE BECAUSE WE'RE ONLY COMPUTING DISTANCE ACROSS SINGLE GRIDBOX!!!
            lat1 = radians(lt - LtHalf)
            lon1 = radians(ln - LnHalf)
            lat2 = radians(lt + LtHalf)
            lon2 = radians(ln + LnHalf) 
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            XdiagArr[Nlt,Nln] = EarthRadius * c
            #print("Test distance calcs: ",lt,ln,XdiagArr[Nlt,Nln])
            #pdb.set_trace()
	
            # Only carry on if there are enough data over climatology period - 120+ months out of 360?
            subarrCAND = TheAnomsArr[ClimMonSt:ClimMonEd+1,Nlt,Nln]
            GoodPointsCAND = np.where(subarrCAND > TheMDI)[0]
            #print("Test counting of good points over clim: ",len(GoodPointsCAND))
            #pdb.set_trace()
            if (len(GoodPointsCAND) >= 120): 

#                print("Location: ",ln,lt)	
#                print("Data presence: ",len(GoodPointsCAND))	
            
                # Calc Xo correlation decay distance - or set to 500 km (arbitrarily low number?)
	        
		# Set up empty arrays to fill
                GBcorrs = np.empty((Nlats,Nlons),dtype = float)
                GBcorrs.fill(TheMDI)
                GBdists = np.empty((Nlats,Nlons),dtype = float)
                GBdists.fill(TheMDI)
	        
		# Initialise candidate gridbox with correlation of 1 and distance of 0 with itself
                GBcorrs[Nlt,Nln] = 1.
                GBdists[Nlt,Nln] = 0.
        
	        # For each long and lat:
                for Nln_2,ln_2 in enumerate(TheLonsArr):
                    for Nlt_2,lt_2 in enumerate(TheLatsArr):
		
		        # continue only if we have NOT hit the CANDIDATE GRIDBOX
                        if (ln != ln_2) & (lt != lt_2):

                            # Only look at if there are enough MATCHING data over climatology period - 10+ months out of 360?
	                    # AND if the longitudinal distance (in radians) is less than (180 deg or pi in radians) (breaks haversine calculation and is generally massive)
                            subarrTMP = TheAnomsArr[ClimMonSt:ClimMonEd+1,Nlt_2,Nln_2]
                            GoodPointsTMP = np.where((subarrCAND > TheMDI) & (subarrTMP > TheMDI))[0]
                            #print("Test counting of MATCHING points over clim: ",lt, lt_2, ln, ln_2,len(GoodPointsTMP))
                            #pdb.set_trace()
                            if (len(GoodPointsTMP) >= 10):
			    
                                # Correlate where the data match			    			     
                                GBcorrs[Nlt_2,Nln_2] = np.corrcoef(subarrCAND[GoodPointsTMP],subarrTMP[GoodPointsTMP])[0,1]
                                #print("Test correlation: ",GBcorrs[Nlt_2,Nln_2])
                                #pdb.set_trace()
				
                                # Get the distance between the midpoint of the two gridboxes												
	                        # This is the Haversine method so assumes perfect sphere
	                        # Should really use Vincenty method which uses eliptoidal model
	                        # geopy.distance.distance would do this automatically but its not in scitools/experimental-current
				# NOTE: This method DOES NOT WORK for nearly antipodial points (e.g. lat -2.5 to 2.5 and lon -107.5 72.5)
				# These are generally very large distances with correlation most likely to be very low - dlon approaches pi
				# Therefore where the longitude distance is greater than 3.1 I just skip!!! This will leave the MDI
                                lat1 = radians(lt)
                                lon1 = radians(ln)
                                lat2 = radians(lt_2)
                                lon2 = radians(ln_2) 
                                dlon = lon2 - lon1
                                dlat = lat2 - lat1
                                #print(lt, lt_2, ln, ln_2)				
                                #print(lat1, lat2, lon1, lon2, dlat, dlon)
                                # test to check dlon is ok (less than pi) - else it just stays as MDI for GB and reset GBcorrs to MDI
                                if (abs(dlon) < 3.1):
                                    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                                    #print('a: ',a)
                                    c = 2 * atan2(sqrt(a), sqrt(1 - a))
                                    #print('c: ',c)
                                    GBdists[Nlt_2,Nln_2] = EarthRadius * c
                                    #print("Test GB distance calcs: ",lt_2,ln_2,GBdists[Nlt_2,Nln_2])
                                    #pdb.set_trace()
                                else:
                                    GBcorrs[Nlt_2,Nln_2] = TheMDI				
	
                # If there are at least 2 GBs where there is a correlation then Find the point aof corr <= 1/e 
		# and use that distance for Xo OR MAXIMUM distance in group 
                GotMatch = np.where(GBcorrs > TheMDI) # 2D array
                if (len(GotMatch[0]) > 2):
                    #print("Test Match and pointers for 2D GBcorrs: ", len(GotMatch[0]))
                    #pdb.set_trace()
		    
#                    # Sort corrs from high to low and dists from high to low corrs
                    #print(GBdists[GotMatch][0:10],GBcorrs[GotMatch][0:10])
                    SortedDists = np.flip(GBdists[GotMatch][np.argsort(GBcorrs[GotMatch])])
                    SortedCorrs = np.flip(np.sort(GBcorrs[GotMatch]))
                    #print('SortedDists: ',SortedDists[0:50],SortedDists[len(SortedDists)-50:len(SortedDists)])		    
                    #print('SortedCorrs: ',SortedCorrs[0:50],SortedCorrs[len(SortedDists)-50:len(SortedDists)])		    
                    #print("Test the sorting/flipping of corrs and dists")
                    #pdb.set_trace()##

#                    # I can do an exact method which will be affected by noise
## NOt doing this as its very flakey and susceptible to very high CCDs
#                    LowCorrs = np.where(SortedCorrs <= (1./np.exp(1)))[0]
#                    if (len(LowCorrs) > 0): 
#                        XoArr[Nlt,Nln] = SortedDists[LowCorrs[0]]
#                    else:
#                        XoArr[Nlt,Nln] = np.max(SortedDists) # IDL code line 231 set this to the last SOrtedDists element which may not have been the largest
#                    print("Exact Method CCD: ",len(LowCorrs), XoArr[Nlt,Nln])
		    
		    # OR
		    
		    # a smoothed/binned method which seems a little more sensible
		    # 5x5 gridboxes are at least 500km apart
                    xdist = (np.arange(30) + 1) * 500	# distances from 0 to 15000 km
                    ycorrs = np.empty(30,dtype = float)
                    ycorrs[0] = 1.# always 500 km  
                    for i in np.arange(1,29):
                        ins = np.where((SortedDists >= xdist[i-1]) & (SortedDists < xdist[i]))[0]
                        if (len(ins) > 0):
                            ycorrs[i] = np.mean(SortedCorrs[ins]) 
                        else:
                            ycorrs[i] = 0.4 # force to be bigger than 1/e just in case there is a gap
                    LowCorrs = np.where(ycorrs <= (1./np.exp(1)))[0]
                    if (len(LowCorrs) > 0):
                        XoArr[Nlt,Nln] = xdist[LowCorrs[0]] 
                    else:
                        XoArr[Nlt,Nln] = xdist[29]
                    #print('xdist: ',xdist)
                    #print('ycorrs: ',ycorrs)
#                    print("Smoothed Method CCD: ",len(LowCorrs),XoArr[Nlt,Nln])
                    #pdb.set_trace()
		    		
		# There aren't enough matches so set XoArr[Nlt,Nln] to 500 km - artbitrarily low?
                else:		    
        
                    XoArr[Nlt,Nln] = 500 # I think that this is actually quite high - but its' one gridbox!!!	                    		    		    		                       		    		

                # Calc ShatSQArr (Shat^2) - variances of all gridbox month means over climatology period for this long and lat
                
                ShatSQArr[Nlt,Nln] = np.std(subarrCAND[GoodPointsCAND])**2

                # Calc rbarArr (Xo/Xdiag)*(1-e(-Xdiag/Xo)) - average intersite correlation of gridbox (estimated) for this long and lat

                rbarArr[Nlt,Nln] = (XoArr[Nlt,Nln] / XdiagArr[Nlt,Nln]) * (1. - np.exp(-XdiagArr[Nlt,Nln] / XoArr[Nlt,Nln]))

                # Calc sbarSQArr (ShatSQ*n)/(1+((n-1)*rbar)) - mean station variance for this long and lat

                sbarSQArr[Nlt,Nln] = (ShatSQArr[Nlt,Nln] * TheMeanNPointsArr[Nlt,Nln]) / (1.+((TheMeanNPointsArr[Nlt,Nln] - 1) * rbarArr[Nlt,Nln]))
                
		# Calc SESQArr (sbarSQ*rbar*(1-rbar))/(1+((n-1)*rbar))) - sampling error for this long and lat and all times where there are data
                GotCounts = np.where(TheNPointsArr[:,Nlt,Nln] > 0)[0]
                if (len(GotCounts) > 0): 
#                    print('GotCounts: ',TheNPointsArr[GotCounts[0:5],Nlt,Nln])
                    SESQArr[GotCounts,Nlt,Nln] = ((sbarSQArr[Nlt,Nln] * rbarArr[Nlt,Nln] * (1. - rbarArr[Nlt,Nln])) / (1. + ((TheNPointsArr[GotCounts,Nlt,Nln] - 1.) * rbarArr[Nlt,Nln]))) #for IDL and HadISDH-land this was *2 for 2sigma

# ADDED CATCH FOR WHERE THERE ARE NO DATA POINTS AT THAT POINT BUT ENOUGH TO CALCULATE CLIMATOLOGY AT OTHERS. THIS WAS AN ERROR I THINK - CREATING MISSING GRIDBOXES
                # Where we do not have data default to sbarSQ * rbar (SHOULD BE LARGER!)
                GotZeros = np.where(TheNPointsArr[:,Nlt,Nln] == 0)[0]
                if (len(GotZeros) > 0): 
                
                    SESQArr[GotZeros,Nlt,Nln] = (sbarSQArr[Nlt,Nln] * rbarArr[Nlt,Nln]) 
                
# 
#
#                print("Sampling Unc results where there are data: ")
#                print("ShatSQ (climatological variance of gridbox) = ",ShatSQArr[Nlt,Nln])
#                print("rbar (average intersite correlation of gridbox) = ",rbarArr[Nlt,Nln])
#                print("sbarSQ (mean station variance within gridbox) = ",sbarSQArr[Nlt,Nln])
#                print("SESQ (sampling uncertainty) = ",SESQArr[GotCounts[0:5],Nlt,Nln])
                #pdb.set_trace()
		# DO NOT *2 BECAUSE WE WANT 1SIGMA ERRORS

# 2nd LOOP THROUGH AGAIN TO INFILL MISSING GRIDBOXES BY INTERPOLATION WHERE POSSIBLE
    # For each long and lat:
    for Nln,ln in enumerate(TheLonsArr):
        for Nlt,lt in enumerate(TheLatsArr):
	
	    ## switch this off for testing
            #continue
	
            # Only carry on if there are NOT enough data over climatology period - 120+ months out of 360? AND this is a LAND (IsMarine = False) or MARINE (IsLand = True) GRIDBOX!!!
            subarrCAND = TheAnomsArr[ClimMonSt:ClimMonEd+1,Nlt,Nln]
            GoodPointsCAND = np.where(subarrCAND > TheMDI)[0]
            if (len(GoodPointsCAND) < 120): 

                # Only work on either Marine (IsMarine = True) or Land (IsLand = True)
		# Therefore, if there are NO datapoints we need to check if this is a land (>0) or marine (<100) gridbox 
		# Arguably - do we need sampling uncertainty if there are no datapoints?
		# if we're working with marine but its 100% land then ignore gridbox
                #print(len(GoodPointsCAND))		
                #print(IsMarine)		
                #print(PctLand[Nlt,Nln])		
#                if (len(GoodPointsCAND) == 0) & (IsMarine) & (PctLand[Nlt,Nln] >= 99.9): # just being cautious about funny floating point things
#                    continue
#		# if we're working with land but its 100% marine then ignore gridbox
#                if (len(GoodPointsCAND) == 0) & (not IsMarine) & (PctLand[Nlt,Nln] < 0.0001): # just being cautious about funny floating point things
#                    continue
                if (len(GoodPointsCAND) == 0) & (IsMarine) & (PctLand[Nlt,Nln] > 0.99999): # just being cautious about funny floating point things
                    continue
		# if we're working with land but its 100% marine then ignore gridbox
                if (len(GoodPointsCAND) == 0) & (not IsMarine) & (PctLand[Nlt,Nln] < 0.00001): # just being cautious about funny floating point things
                    continue
		
                print("Location: ",ln,lt)	
                print("Data presence: ",len(GoodPointsCAND), "IsMarine = ",IsMarine)	
            
                # Calc Xo correlation decay distance by gaussian filtering over nearest gridboxes 3 N, 3 S, 6 E and 6 W - or set to 500 km (arbitrarily low number?)
                # gaussian filtering - G(x,y)= (1/(2*pi*(stdev^2)))*EXP(-((x^2+y^2)/(2*stdev^2)))
                # from http://homepages.inf.ed.ac.uk/rbf/HIPR2/gsmooth.htm
                # PROBLEM - not getting true standard deviation if there are missing gridboxes!!!
	        
		# Set up empty scalars and arrays to fill
                Weighty = 0.
                TotWeights = 0.
                TotsbarSQ = 0.
                Totrbar = 0.

                GBrbarArr = np.empty((NGaussLtBx+1,NGaussLnBx+1),dtype = float)
                GBrbarArr.fill(TheMDI)
                GBsbarSQArr = np.empty((NGaussLtBx+1,NGaussLnBx+1),dtype = float)
                GBsbarSQArr.fill(TheMDI)
                GBdists = np.empty((3,NGaussLtBx+1,NGaussLnBx+1),dtype = float) # 0=actual distance, 1=distance E-W(x), 2=distance S-N(y)
                GBdists.fill(TheMDI)
		
	        # For each long and lat:
                for Nln_2 in range(NGaussLnBx+1): # This needs to include the candidate box
		    
		    # get a pointer for the gridbox longitude
                    LnPt = int((Nln - (NGaussLnBx / 2.)) + Nln_2)
		    # Longs can wrap around so no problem with boundaries here
                    if (LnPt < 0):
                        LnPt = Nlons + LnPt - 1
                    if (LnPt >= Nlons):
                        LnPt = LnPt - Nlons
		
                    for Nlt_2 in range(NGaussLtBx+1): # This needs to include the candidate box
                       
                        # get a pointer for the gridbox latitude  		       
                        LtPt = int((Nlt - (NGaussLtBx / 2.)) + Nlt_2)
                        # lats cannot wrap around - just use the boxes there are in that hemisphere
                        if (LtPt < 0):
                            continue
                        if (LtPt >= Nlats):
                            continue
                        
                        #print("LONS: ",Nln_2,LnPt," LATS: ",Nlt_2,LtPt,rbarArr[LtPt,LnPt],sbarSQArr[LtPt,LnPt])

                        # Now fill with rbar and SbarSQ IF they are sensible / not guessed values (filled with 0.8 and 10 respectively below)
			# The CANDIDATE gridbox should be TheMDI because it won't have been set above
#                        if (rbarArr[LtPt,LnPt] > TheMDI) & (rbarArr[LtPt,LnPt] != 0.1): 
# THIS WAS WRONG AS WE'RE NOW SETTING rbar to 0.8 SO OK TO USE - OTHERWISE WE MIGHT REMOVE VALID 0.8 values....
                        if (rbarArr[LtPt,LnPt] > TheMDI) :
                            GBrbarArr[Nlt_2,Nln_2] = rbarArr[LtPt,LnPt]
                        if (sbarSQArr[LtPt,LnPt] > TheMDI) & (sbarSQArr[LtPt,LnPt] != 10):
                            GBsbarSQArr[Nlt_2,Nln_2] = sbarSQArr[LtPt,LnPt]
				
                        # Get the distance between the midpoints of the CANDIDATE and all surrounding gridboxes	
			# This will obvs be 0 km for the CANDIDATE box with itself											
	                # This is the Haversine method so assumes perfect sphere
	                # Should really use Vincenty method which uses eliptoidal model
	                # geopy.distance.distance would do this automatically but its not in scitools/experimental-current
                        # These boxes are close to each other so shouldn't cause a problem with points on opposite sides of the globe and equator
                        lat1 = radians(lt)
                        lon1 = radians(ln)
                        lat2 = radians(TheLatsArr[LtPt])
                        lon2 = radians(TheLonsArr[LnPt]) 
                        dlon = lon2 - lon1
                        dlat = lat2 - lat1
                        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                        c = 2 * atan2(sqrt(a), sqrt(1 - a))
                        GBdists[0,Nlt_2,Nln_2] = EarthRadius * c

                        # Get distance E to W
                        dlonEW = dlon
                        dlatEW = 0
                        a = sin(dlatEW / 2)**2 + cos(lat1) * cos(lat2) * sin(dlonEW / 2)**2
                        c = 2 * atan2(sqrt(a), sqrt(1 - a))
                        GBdists[1,Nlt_2,Nln_2] = EarthRadius * c

                        # Get distance S to N
                        dlonSN = 0
                        dlatSN = dlat
                        a = sin(dlatSN / 2)**2 + cos(lat1) * cos(lat2) * sin(dlonSN / 2)**2
                        c = 2 * atan2(sqrt(a), sqrt(1 - a))
                        GBdists[2,Nlt_2,Nln_2] = EarthRadius * c
                        #print("Test GB distance calcs: ",TheLatsArr[LtPt],TheLonsArr[LnPt],GBdists[:,Nlt_2,Nln_2])
                        #pdb.set_trace()

                        # Make the distances -ve for west or south of the CANDIDATE gridbox
                        if (Nln_2 < (NGaussLnBx / 2.)):
                            GBdists[2,Nlt_2,Nln_2] = -(GBdists[2,Nlt_2,Nln_2])
                        if (Nlt_2 < (NGaussLtBx / 2.)):
                            GBdists[1,Nlt_2,Nln_2] = -(GBdists[1,Nlt_2,Nln_2])

                # Is there at least two sensible values of sbarSQ in the surrounding gridboxes
                GotsbarSQ = np.where(GBsbarSQArr > TheMDI)
                if (len(GotsbarSQ[0]) > 1):
		
                    SDdist = np.std(GBdists[0,:,:]) # standard deviation of distances from centre gridbox

                    # get gaussian weighting for each gridbox and apply to Xo value in readiness to calculate a weighted mean
                    # first need to normalise to give stdev of ~1 and mean of ~0
                    GBdists[1,:,:] = (GBdists[1,:,:] - np.mean(GBdists[1,:,:])) / SDdist
                    GBdists[2,:,:] = (GBdists[2,:,:] - np.mean(GBdists[2,:,:])) / SDdist
		    
                    for Nln_2 in range(NGaussLnBx+1): # +1 because this must include boxes either side AND candidate box

#		        # get a pointer for the gridbox longitude
#                        LnPt = int((Nln - (NGaussLnbBx / 2.)) + Nln_2)
#		        # Longs can wrap around so no problem with boundaries here
#                        if (LnPt < 0):
#                            LnPt = Nlons + LnPt - 1
#                        if (LnPt >= Nlons):
#                            LnPt = LnPt - Nlons
#		
                        for Nlt_2 in range(NGaussLtBx+1): # This needs to include the candidate box
#                       
#                            # get a pointer for the gridbox latitude  		       
#                            LtPt = int((Nlt - (NGaussLtBx / 2.)) + Nlt_2)
#                            # lats cannot wrap around - just use the boxes there are in that hemisphere
#                            if (LtPt < 0):
#                                continue
#                            if (LtPt >= Nlats):
#                                continue
#                            #### IDL CODE HAS WRAP AROUND LATS WHICH DOESN@T SEEM RIGHT ###
#                            # IF (ltpt LT 0) THEN ltpt=nlts+ltpt
#                            # IF (ltpt GE nlts) THEN ltpt=ltpt-nlts
#                        
#			    print("LONS: ",Nln_2,LnPt," LATS: ",Nlt_2,LtPt,rbarArr[LtPt,LnPt],sbarSQArr[LtPt,LnPt])
            
                            # If we have put in a value for this then use it, and get a weight for it - will ignore candidate which should be TheMDI
                            if (GBsbarSQArr[Nlt_2,Nln_2] > TheMDI):
                                nsd = 1 	# 1 standard dev
                                Weighty = (1. / ((2 * np.pi * (nsd **2)))) * np.exp(-(((GBdists[1,Nlt_2,Nln_2]**2) + (GBdists[2,Nlt_2,Nln_2]**2)) / (2 * (nsd**2))))
                                #print('WEIGHTING HERE: ',Weighty)
                                TotWeights = TotWeights + Weighty
                                TotsbarSQ = TotsbarSQ + (GBsbarSQArr[Nlt_2,Nln_2] * Weighty)
                                Totrbar = Totrbar + (GBrbarArr[Nlt_2,Nln_2] * Weighty)
               
                # Now depending what we have to work with INFILL sbarSQ and rbar
		# THIS DIFFERS FROM IDL / LAND BECAUSE THE TotWeights > 0 IF LOOP WAS WITHIN THE ABOVE IF LOOP - THIS SHOULDN'T MAKE A DIFFERENCE BECAUSE IF THERE ARE 2 OR MORE GotsbarSQ THERE SHOULD BE WEIGHTS
		# BUT ITS TIDIER THIS WAY
		
		# Where there are some weights - there should be
                if (TotWeights > 0.):
                    sbarSQArr[Nlt,Nln] = TotsbarSQ / TotWeights    
                    rbarArr[Nlt,Nln] = Totrbar / TotWeights
                # Where there are no weights but there is 1 sensible sbarSQ value within the surrounding 3S-N and 6W-E gridboxes then use that one value
                elif (len(GotsbarSQ[0]) == 1):
                    sbarSQArr[Nlt,Nln] = GBsbarSQArr[GotsbarSQ[0][0],GotsbarSQ[1][0]]  
                    rbarArr[Nlt,Nln] = GBrbarArr[GotsbarSQ[0][0],GotsbarSQ[1][0]]  
                # Where there is nothing fill with arbitrary poor values
                else: 
                    sbarSQArr[Nlt,Nln] = 10.  
                    rbarArr[Nlt,Nln] = 0.8 # This was 0.1 but this gives very low SESQ values and 0.8 is mid-range  
 
                # Now get SE^2 = (sbar^2*rbar)	WHEN n>0 and when n=0
		# It seems strange that SESQ is larger when intersite correlation (rbar) is higher - I would have thoought the opposite.
		# So for gridboxes where we do not know rbar - is the worst case scenario a highly correlating gridbox? - THIS NEEDS A REVISIT
                # Where we have data (but less than 120 months) then use that information
                GotCounts = np.where(TheNPointsArr[:,Nlt,Nln] > 0)[0]
                if (len(GotCounts) > 0): 
                
                    SESQArr[GotCounts,Nlt,Nln] = ((sbarSQArr[Nlt,Nln] * rbarArr[Nlt,Nln] * (1. - rbarArr[Nlt,Nln])) / (1. + ((TheNPointsArr[GotCounts,Nlt,Nln] - 1.) * rbarArr[Nlt,Nln]))) # for IDL and HadISDH-land this was *2 for 2sigma

                # Where we do not have data default to sbarSQ * rbar (SHOULD BE LARGER!)
                GotZeros = np.where(TheNPointsArr[:,Nlt,Nln] == 0)[0]
                if (len(GotZeros) > 0): 
                
                    SESQArr[GotZeros,Nlt,Nln] = (sbarSQArr[Nlt,Nln] * rbarArr[Nlt,Nln]) # for IDL and HadISDH-land this was *2 for 2sigma
                
#                print("Sampling Unc results where there are data: ")
#                print("ShatSQ (climatological variance of gridbox) = ",ShatSQArr[Nlt,Nln])
                print("rbar (average intersite correlation of gridbox) = ",rbarArr[Nlt,Nln])
                print("SbarSQ (mean station variance within gridbox) = ",sbarSQArr[Nlt,Nln])
                print("SESQ (sampling uncertainty) = ",SESQArr[0:5,Nlt,Nln])
                #pdb.set_trace()
		# DO NOT *2 BECAUSE WE WANT 1SIGMA ERRORS

# ADDED IN MASKING OF SAMPLING ERROR TO ACTUAL DATA POINTS

    SESQArr[np.where(TheAnomsArr == TheMDI)] = TheMDI

    return SESQArr,rbarArr,sbarSQArr 
