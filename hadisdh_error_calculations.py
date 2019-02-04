#!/usr/local/sci/bin/python
#*****************************
#
# Calculate the HadISDH (and other) error timeseries.
#
#
#************************************************************************
#                    SVN Info
#$Rev:: 72                                            $:  Revision of last commit
#$Author:: rdunn                                      $:  Author of last commit
#$Date:: 2015-05-20 15:21:59 +0100 (Wed, 20 May 2015) $:  Date of last commit
#************************************************************************

import numpy as np
import scipy as sp
import os
import sys
import datetime as dt
import iris
import iris.coord_categorisation
import copy

# RJHD routines
YEAREND = '2017'
DATALOCATION = "/data/local/hadkw/HADCRUH2/UPDATE"+YEAREND+"/STATISTICS/GRIDS/"
OUTDATALOCATION = "/data/local/hadkw/HADCRUH2/UPDATE"+YEAREND+"/STATISTICS/TIMESERIES/"
OTHERDATALOCATION = "/data/local/hadkw/HADCRUH2/UPDATE"+YEAREND+"/OTHERDATA/"
HADISDH_VER = "4.0.0.2017f"
HADISDH_DATE = "MAR2018"

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
    

    offset = np.zeros(len(observations.coord("time").points)/12)
    st_dev = np.zeros(len(observations.coord("time").points)/12)

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

    outfile = file(filename,'w')

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

    outfile = file(filename,'w')

    for d in range(len(ts)):

        outfile.write("".join(["{:10.5f} "*10,"\n"]).format(times[d], ts[d], ts[d]-sample[d], ts[d]+sample[d], ts[d]-coverage[d], ts[d]+coverage[d], ts[d]-station[d], ts[d]+station[d], ts[d]-combined[d], ts[d]+combined[d]))

    outfile.write("".join(["{:10s} "*10,"\n"]).format('#month','hadisdh','sample-','sample+','coverage-','coverage+','station-','station+','combined-','combined+'))
    outfile.write("# all 2-sigma errors\n")
    outfile.write("# 1981-2010 anomaly period")
    outfile.close()

    return # full_outfile_write


#*******************************
for variable in ["RH","Tw","e","T","Td","q","DPD"]:

    print variable

    era_file = "{}2m_monthly_5by5_ERA-Interim_data_1979{}_anoms1981-2010.nc".format(variable.lower(), YEAREND)

    if variable in ["RH","T","Tw","e","q"]:
        hadisdh_file = "HadISDH.land{}.{}_FLATgridIDPHA5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
    elif variable in ["DPD"]:
        hadisdh_file = "HadISDH.land{}.{}_FLATgridPHA5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)
    elif variable in ["Td"]:
        hadisdh_file = "HadISDH.land{}.{}_FLATgridPHADPD5by5_anoms8110_{}_cf.nc".format(variable, HADISDH_VER, HADISDH_DATE)

        
    # get hadisdh data and fix - this uses the long name!!!
    station_error_cube = iris.load(DATALOCATION + hadisdh_file, 'Station uncertainty over gridbox')[0]
    sampling_error_cube = iris.load(DATALOCATION + hadisdh_file, 'Sampling uncertainty over gridbox')[0]
    combined_error_cube = iris.load(DATALOCATION + hadisdh_file, 'Combined uncertainty over gridbox')[0]
    hadisdh_anoms_cube = iris.load(DATALOCATION + hadisdh_file, 'Monthly mean anomaly')[0]

    for cube in [station_error_cube, sampling_error_cube, combined_error_cube, hadisdh_anoms_cube]:
        cube.coord('latitude').guess_bounds()
        cube.coord('longitude').guess_bounds()
        cube.coord('time').guess_bounds()
        


    # get era data and fix
    era_cube = iris.load(OTHERDATALOCATION + era_file)[-1]
    
    # sort the coordinate system
    era_cube.coord('latitude').guess_bounds()
    era_cube.coord('longitude').guess_bounds()
    era_cube.coord('time').guess_bounds()

    # apply land-sea mask

    # lsm = iris.load(DATALOCATION + "new_coverpercentjul08.nc")[0]
    # lsm.data = np.flipud(lsm.data) # flip latitudes for new_coverpercentjul08.nc

    lsm = iris.load(OTHERDATALOCATION + "HadCRUT.4.3.0.0.land_fraction.nc")[1]
    masked_lsm = np.ma.masked_where(lsm.data == 0, lsm.data)
    
    era_cube.data = np.ma.array(era_cube.data, mask = np.array([masked_lsm.mask for i in range(era_cube.data.shape[0])]))

    for region in [global_region, nh_region, tropic_region, sh_region]:

        print region.name

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

        for year in range(annual_coverage_stdev.shape[0]):
            annual_times[year] = int(hadisdh_anoms.coord("time").units.name.split()[2][:4]) + year

            annual_ts[year] = np.mean(monthly_ts.data[year*12:(year*12)+12])

            # sampling error is treated as completely uncorrelated
            # hence error over year is just sqrt(sum of squared errors)/12
            #   Mean is Sum(X_i)/12, so error in Sum(X_i) is sqrt(sum(squares))
            #	  and /12 is just applied to data


            sampling_error = monthly_ts_sample[year*12:(year*12)+12] * monthly_ts_sample[year*12:(year*12)+12]  

            annual_ts_sample[year] = np.sqrt(np.sum(sampling_error)) / 12

            # station error is treated as completely correlated
            # hence error over year is just average of errors 

            annual_ts_station[year] = np.mean(monthly_ts_station[year*12:(year*12)+12] )

            annual_ts_all_combined[year] = np.sqrt(np.sum(annual_ts_coverage[year]**2 + annual_ts_station[year]**2 + annual_ts_sample[year]**2))

#        simple_outfile_write(DATALOCATION + '{}_{}_ts_monthly.dat'.format(variable,region.name), monthly_times, monthly_ts.data, monthly_ts_sample, monthly_ts_coverage, monthly_ts_station, monthly_ts_all_combined)
#        full_outfile_write(DATALOCATION + '{}_{}_monthly_full.dat'.format(variable,region.name), monthly_times, monthly_ts.data, monthly_ts_sample, monthly_ts_coverage, monthly_ts_station, monthly_ts_all_combined)
##
#
#        simple_outfile_write(DATALOCATION + '{}_{}_ts_annual.dat'.format(variable,region.name), annual_times, annual_ts, annual_ts_sample, annual_ts_coverage, annual_ts_station, annual_ts_all_combined)
#        full_outfile_write(DATALOCATION + '{}_{}_annual_full.dat'.format(variable,region.name), annual_times, annual_ts, annual_ts_sample, annual_ts_coverage, annual_ts_station, annual_ts_all_combined)

        simple_outfile_write(OUTDATALOCATION + 'HadISDH.land{}.{}_{}_ts_monthly_anoms8110_{}.dat'.format(variable,HADISDH_VER,region.name,HADISDH_DATE), monthly_times, monthly_ts.data, monthly_ts_sample, monthly_ts_coverage, monthly_ts_station, monthly_ts_all_combined)
        full_outfile_write(OUTDATALOCATION + 'HadISDH.land{}.{}_{}_monthly_full_anoms8110_{}.dat'.format(variable,HADISDH_VER,region.name,HADISDH_DATE), monthly_times, monthly_ts.data, monthly_ts_sample, monthly_ts_coverage, monthly_ts_station, monthly_ts_all_combined)


        simple_outfile_write(OUTDATALOCATION + 'HadISDH.land{}.{}_{}_ts_annual_anoms8110_{}.dat'.format(variable,HADISDH_VER,region.name,HADISDH_DATE), annual_times, annual_ts, annual_ts_sample, annual_ts_coverage, annual_ts_station, annual_ts_all_combined)
        full_outfile_write(OUTDATALOCATION + 'HadISDH.land{}.{}_{}_annual_full_anoms8110_{}.dat'.format(variable,HADISDH_VER,region.name,HADISDH_DATE), annual_times, annual_ts, annual_ts_sample, annual_ts_coverage, annual_ts_station, annual_ts_all_combined)


