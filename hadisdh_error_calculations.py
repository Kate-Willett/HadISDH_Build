#!/usr/local/sci/bin/python
#*****************************
#!/usr/local/sci/bin/python
# PYTHON3
# 
# Author: Kate Willett (was RObert Dunn)
# Created: 2 May 2019 (From RObert Dunn's code)
# Last update: 2 May 2019
# Location: /data/users/hadkw/WORKING_HADISDH/UPDATE201?/PROGS/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# Produces area average time series of each variable and uncertainty components for monthly and annual means and global, northern
# hemisphere, tropics and southern hemisphere land and marine time series.
#
# THis now also works on marine data. When combining obs uncertainties over the gridbox month we assume 100% correlation for 4 of the current components of station unc (or 5 of 6 when we include solar unc)
# 100% correlated are instrument adjustment uncertainty (SCN), height adjustment uncertainty (HGT) and climatology uncertainty (C). Uncorrelated are whole number (R) and measurement (M).
# When combining correlated uncertainties I use SQRT((U1 + U2 + U3 etc)**2) / SQRT(n_obs or n_grids). THis is different to here when combing annual station uncertainty which uses mean(U1, U2, U3 etc).
# My method results in larger uncertainties!!!
#
# When then combining uncertainties regionally over wider areas I currently do not assume any correlation. This is tricky. In truth there will be some degree of correlation but it is far from 100%, 
# espectially because we're combining the already combined station uncertainties some of which are correlated and some of which are not. Correlation reduces quickly over space for the same month 
# and over time for the same gridbox. However, there will be some correlation as ships move through gridboxes through time. We are already assuming worst case scenario when treating SCN, HGT and 
# C as 100% correlation so these are likely over estimates. I do not think it is necessary to then assume 100% correlation over space and time for regional averages. At present I am treating it as 
# completely uncorrelated which will be an underestimate. Until I can do a better job of working out the actual space time correlation of each ob/grid I cannot do better. So this is a first stab at 
# uncertainty quantification. It actually results in HUGE station uncertainty which I suspect/hope is an over estimate.
#
# All read in uncertainties are 2 sigma!!!
# The coverage uncertainty is *2 to make it 2 sigma too
#
# <references to related published material, e.g. that describes data set>
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# inbuilt:
# import datetime as dt
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.dates import date2num,num2date
# import sys, os
# from scipy.optimize import curve_fit,fsolve,leastsq
# from scipy import pi,sqrt,exp
# from scipy.special import erf
# import scipy.stats
# from math import sqrt,pi
# import struct
# import pdb
# 
# -----------------------
# DATA
# -----------------------
# reads in netCDF grids 
# '/data/users/hadkw/WORKING_HADISDH/UPDATE2018/STATISTICS/GRIDS/HadISDH.<domain><var>.<VER>_DOMAINBLURB_anoms181-2010_<thenmon
# inCIDs='/data/local/hadkw/HADCRUH2/UPDATE2017/LISTS_DOCS/isd-history_downloaded18JAN2018_1230.txt'
# 20CR SLP data for making climatological SLP for humidity calculation
# inSLP='/data/local/hadkw/HADCRUH2/UPDATE2017/OTHERDATA/'	#20CR*7605MSLP_yycompos.151.170.240.10.37.8.8.59.nc
#
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# 
# Makie sure you have selected the domain of interest (land or marine)
# Make sure the HADISDH_VER and HADISDH_DATE are correct
# module load scitools/default-current
# python hadisdh_error_calculations.py
#
# -----------------------
# OUTPUT
# -----------------------
# ASCII monthly and annual time series 
# /data/users/hadkw/WORKING_HADISDH/UPDATE2018/STATISTICS/TIMESERIES/HadISDH.<DOMAIN><var>.<VER>_region_annual_full_anoms8110_<mon><year>.dat'
# /data/users/hadkw/WORKING_HADISDH/UPDATE2018/STATISTICS/TIMESERIES/HadISDH.<DOMAIN><var>.<VER>_region_monthyl_full_anoms8110_<mon><year>.dat'
# /data/users/hadkw/WORKING_HADISDH/UPDATE2018/STATISTICS/TIMESERIES/HadISDH.<DOMAIN><var>.<VER>_region_ts_annual_anoms8110_<mon><year>.dat'
# /data/users/hadkw/WORKING_HADISDH/UPDATE2018/STATISTICS/TIMESERIES/HadISDH.<DOMAIN><var>.<VER>_region_ts_monthly_anoms8110_<mon><year>.dat'
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
#
# Version 3 (8th April 2020)
# ---------
#  
# Enhancements
# Updated to work with ERA5
#  
# Changes
# Now has a missing data threshold of 11 (so one missing month is ok for annual!!!) - for April 2015!
#  
# Bug fixes
#
# Version 2 (2nd May 2019)
# ---------
#  
# Enhancements
# Updated to deal with marine and new ERA files
#  
# Changes
# Now Python 3
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

import numpy as np
import scipy as sp
import os
import sys
import datetime as dt
import iris
import iris.coord_categorisation
import copy
import pdb

# RJHD routines
YEAREND = '2019'
DATALOCATION = "/data/users/hadkw/WORKING_HADISDH/UPDATE"+YEAREND+"/STATISTICS/GRIDS/"
OUTDATALOCATION = "/data/users/hadkw/WORKING_HADISDH/UPDATE"+YEAREND+"/STATISTICS/TIMESERIES/"
OTHERDATALOCATION = "/data/users/hadkw/WORKING_HADISDH/UPDATE"+YEAREND+"/OTHERDATA/"
DOMAIN = 'blend'
#DOMAIN = 'land'
#DOMAIN = 'marine'

if (DOMAIN == 'land'):

    HADISDH_VER = "4.2.0.2019f"
    HADISDH_DATE = "JAN2020"
    Ship = False # needs to be set or code will fail

elif (DOMAIN == 'marine'):

    HADISDH_VER = "1.0.0.2019f"
    HADISDH_DATE = "JAN2020"
#    Ship = False # plot ship only data or False plot the ship and buoy
    Ship = True # plot ship only data or False plot the ship and buoy

elif (DOMAIN == 'blend'):

    HADISDH_VER = "1.0.0.2019f"
    HADISDH_DATE = "JAN2020"
#    Ship = False # plot ship only data or False plot the ship and buoy
    Ship = True # plot ship only data or False plot the ship and buoy

class Region(object):

    def __init__(self, name, coords):

        self.name = name
        self.coords = coords

    def __str__(self):
        return "{} {}".format(self.name, self.coords)

    __repr__ = __str__



# regions
global_region=Region("global", [-180.,-70.,180.,70.])
nh_region=Region("northern_hemisphere",[-180.,20.,180.,70.])
tropic_region=Region("tropics",[-180.,-20.,180.,20.])
sh_region=Region("southern_hemisphere",[-180.,-70.,180.,-20.])

#*******************************
def latConstraint(lats):
    ''' Constrain cube latitudes '''
    import iris
    # the "+1" and "-1" result in bounds being used for the test as well as the box centers
    return iris.Constraint(latitude = lambda lat: lats[0]+1 <= lat <= lats[1]-1) # latConstraint


#*******************************
def compute_coverage_error_monthly(observations, reanalysis):
    '''
    Calculate the coverage error on a monthly basis

    Takes each month in observations, find all the corresponding calendar months in reanalysis
    (i.e. for Jan 1973, finds all Jans in ERA).  Then mask by data coverage, and get
    range of residuals in global average.  Use these residuals to estimate error

    '''
    

    offset = np.zeros(len(observations.coord("time").points))
    st_dev = np.zeros(len(observations.coord("time").points))

    # add month names into data
    iris.coord_categorisation.add_month(reanalysis, 'time', name = 'month')
    iris.coord_categorisation.add_month(observations, 'time', name = 'month')

    for m, month  in enumerate(observations.coord("time").points):

        # get weightings for cubes
        grid_areas = iris.analysis.cartography.cosine_latitude_weights(observations[m]) 
        area_average = observations[m].collapsed(['longitude', 'latitude'], iris.analysis.MEAN, weights=grid_areas)

        if area_average == observations.data.fill_value:
            # no data for this month
            offset[m] = observations.data.fill_value
            st_dev[m] = observations.data.fill_value
            
        else:
            # extract cube using month name
            this_month_name = observations.coord('month').points[m]
            selected_months = reanalysis.extract(iris.Constraint(month = lambda cell: cell == this_month_name))
            
            # get a clean-mean
            grid_areas = iris.analysis.cartography.cosine_latitude_weights(selected_months)              

            total_mean = selected_months.collapsed(['longitude', 'latitude'], iris.analysis.MEAN, weights=grid_areas)

            # apply the observation coverage mask to all months
            # combine the lsm with the data mask
            combined_mask = np.ma.mask_or(np.array([observations[m].data.mask for i in range(selected_months.data.shape[0])]), selected_months.data.mask)

            selected_months.data.mask = combined_mask

            # get a masked mean
            grid_areas = iris.analysis.cartography.cosine_latitude_weights(selected_months)              
            masked_mean = selected_months.collapsed(['longitude', 'latitude'], iris.analysis.MEAN, weights=grid_areas)
            
            # calculate residuals and find mean and st_dev
            residuals = masked_mean.data - total_mean.data

            offset[m] = np.mean(residuals)
            st_dev[m] = np.std(residuals, ddof = 1) # to match IDL

    return offset, st_dev # compute_coverage_error_monthly

#*******************************
def compute_coverage_error_annual(observations, reanalysis):
    '''
    Calculate the coverage error on a monthly basis

    Takes each month in observations, find all the corresponding calendar months in reanalysis
    (i.e. for Jan 1973, finds all Jans in ERA).  Then mask by data coverage, and get
    range of residuals in global average.  Use these residuals to estimate error

    Combines months and uncertainties (checking for correlations) into annual series
    '''
    

    offset = np.zeros(np.int(len(observations.coord("time").points)/12))
    st_dev = np.zeros(np.int(len(observations.coord("time").points)/12))

    # add year into data
    iris.coord_categorisation.add_year(reanalysis, 'time', name = 'year')
    iris.coord_categorisation.add_year(observations, 'time', name = 'year')

    for y, year  in enumerate(np.unique(observations.coord("year").points)):

        this_year_data = observations.extract(iris.Constraint(year = lambda cell: cell == year))

        # get weightings for cubes
        grid_areas = iris.analysis.cartography.cosine_latitude_weights(this_year_data) 
        area_average = this_year_data.collapsed(['longitude', 'latitude'], iris.analysis.MEAN, weights=grid_areas)

        if observations.data.fill_value in area_average.data: # this is now an array of 12 monthly values
            # no data for this month
            offset[y] = observations.data.fill_value
            st_dev[y] = observations.data.fill_value
            
        else:
            masked_annual = np.zeros(len(np.unique(reanalysis.coord("year").points)))
            total_annual = np.zeros(len(np.unique(reanalysis.coord("year").points)))
            
            
            for ry, ryear  in enumerate(np.unique(reanalysis.coord("year").points)):

                this_year_reanalysis = reanalysis.extract(iris.Constraint(year = lambda cell: cell == ryear))
           
                # get a clean-mean
                grid_areas = iris.analysis.cartography.cosine_latitude_weights(this_year_reanalysis) 
                total_mean = this_year_reanalysis.collapsed(['longitude', 'latitude'], iris.analysis.MEAN, weights=grid_areas)

                # apply the observation coverage mask to all months
                # combine the lsm with the data mask
                combined_mask = np.ma.mask_or(this_year_data.data.mask, this_year_reanalysis.data.mask)

                # apply the observation coverage mask to all months
                this_year_reanalysis.data = np.ma.array(this_year_reanalysis.data, mask = combined_mask)

                # get a masked mean
                grid_areas = iris.analysis.cartography.cosine_latitude_weights(this_year_reanalysis) 
                masked_mean = this_year_reanalysis.collapsed(['longitude', 'latitude'], iris.analysis.MEAN, weights=grid_areas)
            
                # average up the twelve months
                masked_annual[ry] = masked_mean.collapsed(['time'], iris.analysis.MEAN).data
                total_annual[ry] = total_mean.collapsed(['time'], iris.analysis.MEAN).data

            # calculate residuals and find mean and st_dev
            residuals = masked_annual - total_annual

            offset[y] = np.mean(residuals)
            st_dev[y] = np.std(residuals, ddof = 1) # to match IDL
           
    return offset, st_dev # compute_coverage_error_annual

#*******************************
def simple_outfile_write(filename, times, ts, sample, coverage, station, combined):
    '''
    Write outfile of uncertainties
    '''

#    outfile = file(filename,'w')
    outfile = open(filename,'w')

    for d in range(len(ts)):

        outfile.write("".join(["{:10.5f} "*6,"\n"]).format(times[d], ts[d], sample[d], coverage[d], station[d], combined[d]))
 
    outfile.write("".join(["{:10s} "*6,"\n"]).format('#month','hadisdh','sample','coverage','station','combined'))
    outfile.write("# all 2-sigma errors\n")
    outfile.write("# 1981-2010 anomaly period")
    outfile.close()

    return # simple_outfile_write

#*******************************
def full_outfile_write(filename, times, ts, sample, coverage, station, combined):
    '''
    Write outfile with full range of uncertainties for ease of plotting
    '''

#    outfile = file(filename,'w')
    outfile = open(filename,'w')

    for d in range(len(ts)):

        outfile.write("".join(["{:10.5f} "*10,"\n"]).format(times[d], ts[d], ts[d]-sample[d], ts[d]+sample[d], ts[d]-coverage[d], ts[d]+coverage[d], ts[d]-station[d], ts[d]+station[d], ts[d]-combined[d], ts[d]+combined[d]))

    outfile.write("".join(["{:10s} "*10,"\n"]).format('#month','hadisdh','sample-','sample+','coverage-','coverage+','station-','station+','combined-','combined+'))
    outfile.write("# all 2-sigma errors\n")
    outfile.write("# 1981-2010 anomaly period")
    outfile.close()

    return # full_outfile_write


#*******************************
for variable in ["q","RH","T","Td","Tw","e","DPD"]:
#for variable in ["RH","T","Td","Tw","e","DPD"]:
#for variable in ["q"]:

    print(variable)

    era_file = "{}2m_monthly_5by5_ERA5_1979{}.nc".format(variable.lower(), YEAREND)

    # Dictionary for looking up variable long names for netCDF output of variables
    LongNameDict = dict([('q','2m specific humidity from 1by1 hrly T, Td and p ERA5'),
             ('RH','2m relative humidity from 1by1 hrly T, Td and p ERA5'),
	     ('e','2m vapour pressure from 1by1 hrly T, Td and p ERA5'),
	     ('Tw','2m wetbulb temperature from 1by1 hrly T, Td and p ERA5'),
	     ('T','2m drybulb temperature from 1by1 hrly T ERA5'),
	     ('Td','2m dewpoint temperature from 1by1 hrly Td ERA5'),
	     ('DPD','2m dewpoint depression from 1by1 hrly T, Td and p ERA5'),
	     ('SLP','2m mean_sea level pressure from 1by1 hrly msl ERA5'),
	     ('P','2m surface pressure from 1by1 hrly sp ERA5'), # does this matter that its p not sp
	     ('UV',['10 metre U wind component from 1by1 hrly ERA5','10 metre V wind component from 1by1 6hrlyERA5']), # this one might not work
	     ('WS','10 metre windspeed from 1by1 hrlyERA5'),
	     ('SST','sea surface temperature from 1by1 hrlyERA5')])

    if (DOMAIN == 'land'):

        if variable in ["RH","T","Tw","e","q"]:
            hadisdh_file = "HadISDH.land{}.{}_FLATgridIDPHA5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
        elif variable in ["DPD"]:
            hadisdh_file = "HadISDH.land{}.{}_FLATgridPHA5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
        elif variable in ["Td"]:
            hadisdh_file = "HadISDH.land{}.{}_FLATgridPHADPD5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
        
        # get hadisdh data and fix - this uses the long name!!!
        station_error_cube = iris.load(DATALOCATION + hadisdh_file, 'Station uncertainty over gridbox (2 sigma)')[0]
        sampling_error_cube = iris.load(DATALOCATION + hadisdh_file, 'Sampling uncertainty over gridbox (2 sigma)')[0]
        combined_error_cube = iris.load(DATALOCATION + hadisdh_file, 'Combined uncertainty over gridbox (2 sigma)')[0]
        hadisdh_anoms_cube = iris.load(DATALOCATION + hadisdh_file, 'Monthly mean anomaly')[0]

    elif (DOMAIN == 'marine'):

        if (Ship):
            hadisdh_file = "HadISDH.marine{}.{}_BClocalSHIP5by5both_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
        else:
            hadisdh_file = "HadISDH.marine{}.{}_BClocal5by5both_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
	
        VarDict = {'q':'Specific Humidity',
	           'RH':'Relative Humidity',
		   'Tw':'Wet Bulb Temperature',
		   'e':'Vapor Pressure',
		   'T':'Marine Air Temperature',
		   'Td':'Dew Point Temperature',
		   'DPD':'Dew Point Pepression'} # THIS NEEDS CORRECTING IN THE FILES!
        
        # get hadisdh data and fix - this uses the long name!!!
        station_error_cube = iris.load(DATALOCATION + hadisdh_file, 'Monthly Mean '+VarDict[variable]+' Anomalies total observation uncertainty (2 sigma)')[0]
        sampling_error_cube = iris.load(DATALOCATION + hadisdh_file, 'Monthly Mean '+VarDict[variable]+' Anomalies gridbox sampling uncertainty (2 sigma)')[0]
        combined_error_cube = iris.load(DATALOCATION + hadisdh_file, 'Monthly Mean '+VarDict[variable]+' Anomalies full gridbox uncertainty (2 sigma)')[0]
        hadisdh_anoms_cube = iris.load(DATALOCATION + hadisdh_file, 'Monthly Mean '+VarDict[variable]+' Anomalies')[0]

    elif (DOMAIN == 'blend'):

        if (Ship):
            if variable in ["RH","T","Tw","e","q"]:
                hadisdh_file = "HadISDH.blend{}.{}_FLATgridIDPHABClocalSHIPboth5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
            elif variable in ["DPD"]:
                hadisdh_file = "HadISDH.blend{}.{}_FLATgridPHABClocalSHIPboth5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
            elif variable in ["Td"]:
                hadisdh_file = "HadISDH.blend{}.{}_FLATgridPHADPDBClocalSHIPboth5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
        else:
            if variable in ["RH","T","Tw","e","q"]:
                hadisdh_file = "HadISDH.blend{}.{}_FLATgridIDPHABClocalboth5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
            elif variable in ["DPD"]:
                hadisdh_file = "HadISDH.blend{}.{}_FLATgridPHABClocalboth5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
            elif variable in ["Td"]:
                hadisdh_file = "HadISDH.blend{}.{}_FLATgridPHADPDBClocalboth5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
	
        VarDict = {'q':'Specific Humidity',
	           'RH':'Relative Humidity',
		   'Tw':'Wet Bulb Temperature',
		   'e':'Vapor Pressure',
		   'T':'Air Temperature',
		   'Td':'Dew Point Temperature',
		   'DPD':'Dew Point Pepression'} # THIS NEEDS CORRECTING IN THE FILES!

        
        # get hadisdh data and fix - this uses the long name!!!
        station_error_cube = iris.load(DATALOCATION + hadisdh_file, VarDict[variable]+' monthly mean anomaly observation uncertainty (2 sigma)')[0]
        sampling_error_cube = iris.load(DATALOCATION + hadisdh_file, VarDict[variable]+' monthly mean anomaly sampling uncertainty')[0]
        combined_error_cube = iris.load(DATALOCATION + hadisdh_file, VarDict[variable]+' monthly mean anomaly full uncertainty')[0]
        hadisdh_anoms_cube = iris.load(DATALOCATION + hadisdh_file, VarDict[variable]+' monthly mean anomalies')[0]



    for cube in [station_error_cube, sampling_error_cube, combined_error_cube, hadisdh_anoms_cube]:
        cube.coord('latitude').guess_bounds()
        cube.coord('longitude').guess_bounds()
        cube.coord('time').guess_bounds()
        


    # get era data and fix
    # Silly Iris doesn't distinguiss by var_name if the units isn't something it likes - %rh not ok apparently! so we need to guess which field is the complete coverage anomalies, read in and double check
#    era_cube = iris.load(OTHERDATALOCATION + era_file)[-1]
#    era_cube = iris.load(OTHERDATALOCATION + era_file)[3]
#    tmp_era_cube = iris.load(OTHERDATALOCATION + era_file)
    
    if (DOMAIN == 'land'):
        
        era_cube = iris.load(OTHERDATALOCATION + era_file, LongNameDict[variable]+' land anomalies from 1981-2010')[0]    

    elif (DOMAIN == 'marine'):    

        era_cube = iris.load(OTHERDATALOCATION + era_file, LongNameDict[variable]+' ocean anomalies from 1981-2010')[0]    

    elif (DOMAIN == 'blend'):    

        era_cube = iris.load(OTHERDATALOCATION + era_file, LongNameDict[variable]+' anomalies from 1981-2010')[0]    
    
    mdi = -1e+30

#    Cube_Counts = [len(np.where(tmp_era_cube[i].data > mdi)[0]) for i in np.arange(len(tmp_era_cube))]
#    GetCube = np.where(Cube_Counts == np.max(Cube_Counts))[0]
##    pdb.set_trace()
#    era_cube = tmp_era_cube[GetCube[0]] # hope that this is anoms not actuals but check for that later
#    tmp_era_cube=[]
#
#    # Now check that there are 72 values present at the north and south pole to see if this is the complete field
#    if (len(np.where(era_cube.data[0,0,:] > mdi)[0]) == 0):
#        print('Wrong ERA field - no data at South Pole')
#        pdb.set_trace()
#
#    if (len(np.where(era_cube.data[0,35,:] > mdi)[0]) == 0):
#        print('Wrong ERA field - no data at North Pole')
#        pdb.set_trace()
#
#    # Now check that there are values below zero to see if this is the anomaly field
#    if (np.min(era_cube.data) > 0.):
#        print('Doesnt look like ERA-Interim anomalies')
#        pdb.set_trace()	
#	#
##pp    # Noe check that there are more than 12 time elements to make sure its not clim or stdev
#    if (len(era_cube.data[:,0,0]) < 24):
#        print('Looks like climatology or stdev field')
#        pdb.set_trace()	
#                                                  
#    #OK = carry on!
#    
    #pdb.set_trace()                                           
    
    # sort the coordinate system
    era_cube.coord('latitude').guess_bounds()
    era_cube.coord('longitude').guess_bounds()
    era_cube.coord('time').guess_bounds()

#    # NOW JUST READ IN ERA5 land or ocean masked data
#    # apply land-sea mask
######
#    # lsm = iris.load(DATALOCATION + "new_coverpercentjul08.nc")[0]
#    # lsm.data = np.flipud(lsm.data) # flip latitudes for new_coverpercentjul08.nc
#
#    lsm = iris.load(OTHERDATALOCATION + "HadCRUT.4.3.0.0.land_fraction.nc")[1]
#    
#    if (DOMAIN == 'land'):
#    
#        masked_lsm = np.ma.masked_where(lsm.data == 0, lsm.data)
#    
#    elif (DOMAIN == 'marine'):#
#
#        masked_lsm = np.ma.masked_where(lsm.data == 1, lsm.data)
#    
#    
#    era_cube.data = np.ma.array(era_cube.data, mask = np.array([masked_lsm.mask for i in range(era_cube.data.shape[0])]))#

#    for region in [sh_region]:#
    for region in [global_region, nh_region, tropic_region, sh_region]:#

        print(region.name)

        hadisdh_anoms = hadisdh_anoms_cube.extract(latConstraint([region.coords[x] for x in (1,3)]))
        station_error = station_error_cube.extract(latConstraint([region.coords[x] for x in (1,3)]))
        sample_error = sampling_error_cube.extract(latConstraint([region.coords[x] for x in (1,3)]))
        combined_error = combined_error_cube.extract(latConstraint([region.coords[x] for x in (1,3)]))
 
        era = era_cube.extract(latConstraint([region.coords[x] for x in (1,3)]))


        monthly_coverage_offset, monthly_coverage_stdev = compute_coverage_error_monthly(hadisdh_anoms, era)
        
        annual_coverage_offset, annual_coverage_stdev = compute_coverage_error_annual(hadisdh_anoms, era)

        annual_coverage_stdev *= 2
        monthly_coverage_stdev *= 2


        # weights for the region
        weights = iris.analysis.cartography.cosine_latitude_weights(hadisdh_anoms) 
        
        monthly_ts = hadisdh_anoms.collapsed(['longitude', 'latitude'], iris.analysis.MEAN, weights=weights)
        #pdb.set_trace()
        monthly_ts_coverage = monthly_coverage_stdev

        # and the rest is long hand
        monthly_ts_sample = np.zeros(monthly_ts.data.shape)
        monthly_ts_station = np.zeros(monthly_ts.data.shape)
        monthly_ts_combined = np.zeros(monthly_ts.data.shape)
        monthly_ts_all_combined = np.zeros(monthly_ts.data.shape)
        monthly_times = np.zeros(monthly_ts.data.shape)

        for m, month in enumerate(hadisdh_anoms.coord("time").points):
            
            monthly_times[m] = int(hadisdh_anoms.coord("time").units.name.split()[2][:4]) + m/12.

            sample_error_month = sample_error.data[m,:,:]
            station_error_month = station_error.data[m,:,:]
            combined_error_month = combined_error.data[m,:,:]

            good = np.where(hadisdh_anoms.data[m].mask == False)

            monthly_ts_sample[m] = np.sqrt(np.sum(weights[m]**2 * sample_error_month**2) / (np.sum(weights[m][good])**2))
            monthly_ts_station[m] = np.sqrt(np.sum(weights[m]**2 * station_error_month**2) / (np.sum(weights[m][good])**2))
            monthly_ts_combined[m] = np.sqrt(np.sum(weights[m]**2 * combined_error_month**2) / (np.sum(weights[m][good])**2))

            monthly_ts_all_combined[m] = np.sqrt(np.sum(monthly_ts_coverage[m]**2 + monthly_ts_station[m]**2 + monthly_ts_sample[m]**2))

        # and for years
        annual_ts = np.zeros(annual_coverage_stdev.shape)
        annual_ts_sample = np.zeros(annual_coverage_stdev.shape)
        annual_ts_station = np.zeros(annual_coverage_stdev.shape)
        annual_ts_all_combined = np.zeros(annual_coverage_stdev.shape)
        annual_times = np.zeros(annual_coverage_stdev.shape)

        annual_ts_coverage = annual_coverage_stdev

        # Add a fix in the case that one month is missin (e.g. April 2015!!!)
	# At this statg
        for year in range(annual_coverage_stdev.shape[0]):
            annual_times[year] = int(hadisdh_anoms.coord("time").units.name.split()[2][:4]) + year

            #annual_ts[year] = np.mean(monthly_ts.data[year*12:(year*12)+12])
            this_year_data = monthly_ts.data[year*12:(year*12)+12]
            this_year_sample = monthly_ts_sample[year*12:(year*12)+12]
            this_year_station = monthly_ts_station[year*12:(year*12)+12]
            if (len(np.where(this_year_data)[0]) >= 11):
                annual_ts[year] = np.mean(this_year_data[np.where(this_year_data)[0]])
                sampling_error = this_year_sample[np.where(this_year_data)[0]] * this_year_sample[np.where(this_year_data)[0]]  
                annual_ts_sample[year] = np.sqrt(np.sum(sampling_error)) / len(np.where(this_year_data)[0])
                annual_ts_station[year] = np.mean(this_year_station[np.where(this_year_data)[0]])
                annual_ts_all_combined[year] = np.sqrt(np.sum(annual_ts_coverage[year]**2 + annual_ts_station[year]**2 + annual_ts_sample[year]**2))
            else:
                annual_ts[year] = mdi
                annual_ts_sample[year] = 0.
                annual_ts_station[year] = 0.
                annual_ts_all_combined[year] = 0.
	    
            # sampling error is treated as completely uncorrelated
            # hence error over year is just sqrt(sum of squared errors)/12
            #   Mean is Sum(X_i)/12, so error in Sum(X_i) is sqrt(sum(squares))
            #	  and /12 is just applied to data


            #sampling_error = monthly_ts_sample[year*12:(year*12)+12] * monthly_ts_sample[year*12:(year*12)+12]  
            #annual_ts_sample[year] = np.sqrt(np.sum(sampling_error)) / 12

            # station error is treated as completely correlated
            # hence error over year is just average of errors 

            #annual_ts_station[year] = np.mean(monthly_ts_station[year*12:(year*12)+12] )

            #annual_ts_all_combined[year] = np.sqrt(np.sum(annual_ts_coverage[year]**2 + annual_ts_station[year]**2 + annual_ts_sample[year]**2))

#        simple_outfile_write(DATALOCATION + '{}_{}_ts_monthly.dat'.format(variable,region.name), monthly_times, monthly_ts.data, monthly_ts_sample, monthly_ts_coverage, monthly_ts_station, monthly_ts_all_combined)
#        full_outfile_write(DATALOCATION + '{}_{}_monthly_full.dat'.format(variable,region.name), monthly_times, monthly_ts.data, monthly_ts_sample, monthly_ts_coverage, monthly_ts_station, monthly_ts_all_combined)
##
#
#        simple_outfile_write(DATALOCATION + '{}_{}_ts_annual.dat'.format(variable,region.name), annual_times, annual_ts, annual_ts_sample, annual_ts_coverage, annual_ts_station, annual_ts_all_combined)
#        full_outfile_write(DATALOCATION + '{}_{}_annual_full.dat'.format(variable,region.name), annual_times, annual_ts, annual_ts_sample, annual_ts_coverage, annual_ts_station, annual_ts_all_combined)

#        if (DOMAIN == 'marine') & (Ship):
        if (Ship):

            simple_outfile_write(OUTDATALOCATION + 'HadISDH.{}{}.{}{}_{}_ts_monthly_anoms8110_{}.dat'.format(DOMAIN,variable,HADISDH_VER,'SHIP',region.name,HADISDH_DATE), monthly_times, monthly_ts.data, monthly_ts_sample, monthly_ts_coverage, monthly_ts_station, monthly_ts_all_combined)
            full_outfile_write(OUTDATALOCATION + 'HadISDH.{}{}.{}{}_{}_monthly_full_anoms8110_{}.dat'.format(DOMAIN,variable,HADISDH_VER,'SHIP',region.name,HADISDH_DATE), monthly_times, monthly_ts.data, monthly_ts_sample, monthly_ts_coverage, monthly_ts_station, monthly_ts_all_combined)

            simple_outfile_write(OUTDATALOCATION + 'HadISDH.{}{}.{}{}_{}_ts_annual_anoms8110_{}.dat'.format(DOMAIN,variable,HADISDH_VER,'SHIP',region.name,HADISDH_DATE), annual_times, annual_ts, annual_ts_sample, annual_ts_coverage, annual_ts_station, annual_ts_all_combined)
            full_outfile_write(OUTDATALOCATION + 'HadISDH.{}{}.{}{}_{}_annual_full_anoms8110_{}.dat'.format(DOMAIN,variable,HADISDH_VER,'SHIP',region.name,HADISDH_DATE), annual_times, annual_ts, annual_ts_sample, annual_ts_coverage, annual_ts_station, annual_ts_all_combined)

        else:

            simple_outfile_write(OUTDATALOCATION + 'HadISDH.{}{}.{}_{}_ts_monthly_anoms8110_{}.dat'.format(DOMAIN,variable,HADISDH_VER,region.name,HADISDH_DATE), monthly_times, monthly_ts.data, monthly_ts_sample, monthly_ts_coverage, monthly_ts_station, monthly_ts_all_combined)
            full_outfile_write(OUTDATALOCATION + 'HadISDH.{}{}.{}_{}_monthly_full_anoms8110_{}.dat'.format(DOMAIN,variable,HADISDH_VER,region.name,HADISDH_DATE), monthly_times, monthly_ts.data, monthly_ts_sample, monthly_ts_coverage, monthly_ts_station, monthly_ts_all_combined)

            simple_outfile_write(OUTDATALOCATION + 'HadISDH.{}{}.{}_{}_ts_annual_anoms8110_{}.dat'.format(DOMAIN,variable,HADISDH_VER,region.name,HADISDH_DATE), annual_times, annual_ts, annual_ts_sample, annual_ts_coverage, annual_ts_station, annual_ts_all_combined)
            full_outfile_write(OUTDATALOCATION + 'HadISDH.{}{}.{}_{}_annual_full_anoms8110_{}.dat'.format(DOMAIN,variable,HADISDH_VER,region.name,HADISDH_DATE), annual_times, annual_ts, annual_ts_sample, annual_ts_coverage, annual_ts_station, annual_ts_all_combined)

