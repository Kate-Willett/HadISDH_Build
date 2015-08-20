#!/usr/local/sci/bin/python

# ipython
# %pdb (the debugger)
# %run Convert_cfnc_AUG2014.py
# this should leave everything interactive

#***************************************
# 22 August 2014 KMW - v1
# Converts a netCDF file to a cf (pp) compliant netCDF
#
#************************************************************************
#                                 START
#************************************************************************
# USE python2.7
# python2.7 PlotTemporalCoverage_MAR2014.py
#
# REQUIRES
# 
#************************************************************************
# Set up python imports
import matplotlib.pyplot as plt
import numpy as np
import sys, os
import scipy.stats
import struct
import os.path
from mpl_toolkits.basemap import Basemap
import datetime as dt
from datetime import datetime
from matplotlib.dates import date2num,num2date
from netCDF4 import Dataset
from scipy.io import netcdf

# Set up directories and files

inmon='JAN'
inyear='2014'
outmon='NOV'
outyear='2014'

DATADIR='/data/local/hadkw/HADCRUH2/UPDATE2013/STATISTICS/'
#INFIL='HadISDH.landq.2.0.0.2013p_FLATgridIDPHA5by5_'
#INFIL='HadISDH.landRH.2.0.0.2013p_FLATgridIDPHA5by5_'
#INFIL='BLEND_NOCSv2.0_HadISDH.landq.2.0.0.2013p_abs_' # JUN!!!
#INFIL='HadISDH.landT.2.0.0.2013p_FLATgridIDPHA5by5_'
#INFIL='HadISDH.landTw.2.0.0.2013p_FLATgridIDPHA5by5_'
#INFIL='HadISDH.lande.2.0.0.2013p_FLATgridIDPHA5by5_'
#INFIL='HadISDH.landTd.2.0.0.2013p_FLATgridPHADPD5by5_'
INFIL='HadISDH.landDPD.2.0.0.2013p_FLATgridPHA5by5_'

INFILEE=INFIL+inmon+inyear

OUTFILEE=INFIL+outmon+outyear+'_cf'

#Typee='specific humidity'
#Typee='relative humidity'
#Typee='temperature'
#Typee='wet bulb temperature'
#Typee='vapour pressure'
#Typee='dew point temperature'
Typee='dew point depression'

# Set up variables

#************************************************************************
# Subroutines
#************************************************************************
# MakeDaysSince
def MakeDaysSince(TheStYr,TheStMon,TheEdYr,TheEdMon):
    ''' Take counts of months since styr, stmn (assume 15th day of month) '''
    ''' Work out counts of days since styr,stmn, January - incl leap days '''
    
    # set up array
    DaysArray=np.empty(((TheEdYr-TheStYr)+1)*12)
    
    # make a date object for each time point and subtract start date
    StartDate=datetime(TheStYr,TheStMon,1,0,0,0)	# January
    DaysArray[0]=(datetime(TheStYr,TheStMon+1,1,0,0,0)-StartDate).days/2.
    TheYear=TheStYr
    TheMonth=TheStMon+1
    for mm in range(1,len(DaysArray)):
        if (TheMonth < 12):
	    DaysArray[mm]=(datetime(TheYear,TheMonth+1,1,0,0,0)-datetime(TheYear,TheMonth,1,0,0,0)).days/2. + (datetime(TheYear,TheMonth,1,0,0,0)-StartDate).days
        else:
	    DaysArray[mm]=(datetime(TheYear+1,1,1,0,0,0)-datetime(TheYear,TheMonth,1,0,0,0)).days/2. + (datetime(TheYear,TheMonth,1,0,0,0)-StartDate).days	
	TheMonth=TheMonth+1
	if (TheMonth == 13):
	    TheMonth=1
	    TheYear=TheYear+1
	    
    return DaysArray

#************************************************************************
# ConvertNCCF
def ConvertNCCF(TheFileIn,TheFileOut,TheTimes,TheDaysArray,TheCLats,TheCLongs,TheClimPeriod,TheMissing,TheType):
    ''' Discover what is in the file '''
    ''' Open and read in all bits '''
    ''' Write out in cf compliant style '''

    ncf=Dataset(TheFileIn,'r')
    nc_dims = list(ncf.dimensions)	# list of dimensions [dim for dim in ncf.dimensions]
    nc_vars = list(ncf.variables)  # list of nc variables [var for var in ncf.variables]
    nc_attrs = ncf.ncattrs()		# list of global attributes

    ndims=len(nc_dims)
    nvars=len(nc_vars)
    ngatts=len(nc_attrs)

# Get all global attributes
    TheGAtts=np.empty(ngatts,dtype=object)	# an empty array with the right number of string elements
    for (noo,att) in enumerate(nc_attrs):	# enumerate and use elements of the list
        TheGAtts[noo]=ncf.getncattr(att)	# get each global attribute and populate array

# Get all dimensions
    TheDims=np.empty(ndims)	# an empty array with the right number of string elements
    for (noo,dim) in enumerate(nc_dims):	# enumerate and use elements of the list
        TheDims[noo]=len(ncf.dimensions[dim])	# get length of each dimension
# NO DIMENSION ATTRIBUTES - 
#    TheDimAttrNames=[[] for i in xrange(ndims)]		# create list of lists - one for the attribute names of each dimension
#    TheDimAttrs=[[] for i in xrange(ndims)]		# create list of lists - one for the attributes of each dimension
#    for (noo,dim) in enumerate(nc_dims):	# enumerate and use elements of the list
#        TheDimAttrNames[noo]=ncf.dimensions[dim].ncattrs()	# fill names
#        for (nee,nats) in enumerate(TheDimAttrNames[noo]):      # loop through each name and get the attribute   
#            TheDimAttrs[noo][nee]=f.dimensions[dim].getncattr(nats)	

# Get all variables, and their attributes
    TheVarAttrNames=[[] for i in xrange(nvars)]		# create list of lists - one for the attribute names of each dimension
    TheVarAttrs=[[] for i in xrange(nvars)]		# create list of lists - one for the attributes of each dimension
    TheVars=[[] for i in xrange(nvars)]		# create list of lists - one for the attributes of each dimension
    for (noo,var) in enumerate(nc_vars):	# enumerate and use elements of the list
        TheVarAttrNames[noo]=ncf.variables[var].ncattrs()	# fill names
        for (nee,nats) in enumerate(TheVarAttrNames[noo]):      # loop through each name and get the attribute   
            TheVarAttrs[noo].append(ncf.variables[var].getncattr(nats))	
        TheVars[noo]=ncf.variables[nc_vars[noo]][:]


# Now write out, checking if the standard stuff is not there, and if not, then add in
    ncfw=Dataset(TheFileOut,'w',format='NETCDF3_CLASSIC')
    
# Set up the global attributes
# Is there a description?
    moo=np.where(np.array(nc_attrs) == 'description')
    if (moo[0] >= 0):
        ncfw.description=TheGAtts[moo[0]]
    else:
        ncfw.description="HadISDH monthly mean land surface "+TheType+" climate monitoring product from 1973 onwards. Quality control, homogenisation, uncertainty estimation, averaging over gridboxes (no smoothing or interpolation)."
# Is there a title?
    moo=np.where(np.array(nc_attrs) == 'title')
    if (moo[0] >= 0):
        ncfw.title=TheGAtts[moo[0]]
    else:
        ncfw.title="HadISDH monthly mean land surface "+TheType+" climate monitoring product from 1973 onwards."
# Is there an institution?
    moo=np.where(np.array(nc_attrs) == 'institution')
    if (moo[0] >= 0):
        ncfw.institution=TheGAtts[moo[0]]
    else:
        ncfw.institution="Met Office Hadley Centre (UK), National Climatic Data Centre (USA), Climatic Research Unit (UK), National Physical Laboratory (UK), Bjerknes Centre for Climate Research (Norway)"
# Is there a history?
    moo=np.where(np.array(nc_attrs) == 'history')
    if (moo[0] >= 0):
        ncfw.history=TheGAtts[moo[0]]
    else:
        ncfw.history="Updated 4 February 2014"
# Is there a source?
    moo=np.where(np.array(nc_attrs) == 'source')
    if (moo[0] >= 0):
        ncfw.source=TheGAtts[moo[0]]
    else:
        ncfw.source="HadISD.1.0.2.2013f (Dunn et al., 2012)"
# Is there a comment?
    moo=np.where(np.array(nc_attrs) == 'comment')
    if (moo[0] >= 0):
        ncfw.comment=TheGAtts[moo[0]]
    else:
        ncfw.comment=""
# Is there a reference?
    moo=np.where(np.array(nc_attrs) == 'reference')
    if (moo[0] >= 0):
        ncfw.reference=TheGAtts[moo[0]]
    else:
        ncfw.reference="Willett, K. M., Dunn, R. J. H., Thorne, P. W., Bell, S., de Podesta, M., Parker, D. E., Jones, P. D., and Williams Jr., C. N.: HadISDH land surface multi-variable humidity and temperature record for climate monitoring, Clim. Past, 10, 1983-2006, doi:10.5194/cp-10-1983-2014, 2014."
# Is there a version?
    moo=np.where(np.array(nc_attrs) == 'version')
    if (moo[0] >= 0):
        ncfw.version=TheGAtts[moo[0]]
    else:
        ncfw.version="HadISDH.2.0.0.2013p"
# Is there a Conventions?
    moo=np.where(np.array(nc_attrs) == 'Conventions')
    if (moo[0] >= 0):
        ncfw.Conventions=TheGAtts[moo[0]]
    else:
        ncfw.Conventions="CF-1.0"

# Now set up the dimensions (time, latitude, longitude, optional-month)
    data={}	# Not really sure what this is about

    moo=np.where(np.array(nc_dims) == 'time')
    goo=np.where(np.array(nc_vars) == 'time')
    if not(goo[0] >= 0): goo=np.where(np.array(nc_vars) == 'times')	# Look for mistakes in HadISDH
    if (moo[0] >= 0) & (goo[0] >= 0):
        ncfw.createDimension(nc_dims[moo[0]],ncf.variables[nc_vars[goo[0]]].size)        
    else:
        ncfw.createDimension('time',TheTimes)        
    
    data['time']=ncfw.createVariable('time','f8',('time',))    

    data['time'].setncattr('standard_name',u'time')
    data['time'].setncattr('long_name',u'time')
    data['time'].setncattr('units',u'days since 1973-1-1 00:00:00')
    data['time'].setncattr('calendar',u'gregorian')
    data['time'].setncattr('start_year',u'1973s')
    data['time'].setncattr('end_year',u'2013s')
    data['time'].setncattr('start_month',u'1s')
    data['time'].setncattr('end_month',u'12s')
    data['time'].setncattr('axis',u'T')

    moo=np.where(np.array(nc_dims) == 'latitude')
    goo=np.where(np.array(nc_vars) == 'latitude')
    if not(goo[0] >= 0): goo=np.where(np.array(nc_vars) == 'lat')	# Look for mistakes in HadISDH
    if (moo[0] >= 0) & (goo[0] >= 0):
        ncfw.createDimension(nc_dims[moo[0]],ncf.variables[nc_vars[goo[0]]].size)        
    else:
        ncfw.createDimension('latitude',TheCLats)        

    data['latitude']=ncfw.createVariable('latitude','f8',('latitude',))     
   
    data['latitude'].setncattr('standard_name',u'latitude')
    data['latitude'].setncattr('long_name',u'latitude')
    data['latitude'].setncattr('units',u'degrees_north')
    data['latitude'].setncattr('point_spacing',u'even')
    data['latitude'].setncattr('axis',u'Y')

    moo=np.where(np.array(nc_dims) == 'longitude')
    goo=np.where(np.array(nc_vars) == 'longitude')
    if not(goo[0] >= 0): goo=np.where(np.array(nc_vars) == 'lon')	# Look for mistakes in HadISDH
    if (moo[0] >= 0) & (goo[0] >= 0):
        ncfw.createDimension(nc_dims[moo[0]],ncf.variables[nc_vars[goo[0]]].size)        
    else:
        ncfw.createDimension('longitude',TheCLongs)        

    data['longitude']=ncfw.createVariable('longitude','f8',('longitude',))     
    
    data['longitude'].setncattr('standard_name',u'longitude')
    data['longitude'].setncattr('long_name',u'longitude')
    data['longitude'].setncattr('units',u'degrees_east')
    data['longitude'].setncattr('point_spacing',u'even')
    data['longitude'].setncattr('axis',u'X')

    makemonth=0    
    moo=np.where(np.array(nc_dims) == 'month')
    goo=np.where(np.array(nc_vars) == 'month')
    if not(goo[0] >= 0): goo=np.where(np.array(nc_vars) == 'months')	# Look for mistakes in HadISDH
    if (moo[0] >= 0) & (goo[0] >= 0):
        makemonth=1
        ncfw.createDimension('month',12)        
    
        data['month']=ncfw.createVariable('month','i',('month',))    

        data['month'].setncattr('standard_name',u'month')
        data['month'].setncattr('long_name',u'month')
        data['month'].setncattr('units',u'days since 1973-1-1 00:00:00')
        data['month'].setncattr('calendar',u'gregorian')
        data['month'].setncattr('start_year',u'1973s')
        data['month'].setncattr('end_year',u'1973s')
        data['month'].setncattr('start_month',u'1s')
        data['month'].setncattr('end_month',u'12s')
        data['month'].setncattr('axis',u'T')
    
# Now set up the variables
#    stop()
    for loo in range(nvars):	# miss out time, lat and lon - and month at the end
        print(loo)
	if (nc_vars[loo] != 'time') & (nc_vars[loo] != 'latitude') & (nc_vars[loo] != 'longitude') & (nc_vars[loo] != 'month') & \
	   (nc_vars[loo] != 'times') & (nc_vars[loo] != 'latitudes') & (nc_vars[loo] != 'longitudes') & (nc_vars[loo] != 'months') & \
	   (nc_vars[loo] != 'lat') & (nc_vars[loo] != 'lon'): 
	   
	    print(nc_vars[loo])

	    ncfw_var=ncfw.createVariable(nc_vars[loo],ncf.variables[nc_vars[loo]].dtype,ncf.variables[nc_vars[loo]].dimensions)

            if (any(np.where(np.array(ncf.variables[nc_vars[loo]].ncattrs()) == '_FillValue'))):
	        ncfw_var.setncattr('_FillValue',ncf.variables[nc_vars[loo]].getncattr('_FillValue')) 
            elif (any(np.where(np.array(ncf.variables[nc_vars[loo]].ncattrs()) == 'missing_value'))):
	        ncfw_var.setncattr('_FillValue',ncf.variables[nc_vars[loo]].getncattr('missing_value')) 
	    else:    
		ncfw_var.setncattr('_FillValue',TheMissing) 

            if (any(np.where(np.array(ncf.variables[nc_vars[loo]].ncattrs()) == 'missing_value'))):
	        ncfw_var.setncattr('missing_value',ncf.variables[nc_vars[loo]].getncattr('missing_value')) 
            elif (any(np.where(np.array(ncf.variables[nc_vars[loo]].ncattrs()) == '_FillValue'))):
	        ncfw_var.setncattr('missing_value',ncf.variables[nc_vars[loo]].getncattr('_FillValue')) 
	    else:    
		ncfw_var.setncattr('missing_value',TheMissing) 

            if (any(np.where(np.array(ncf.variables[nc_vars[loo]].ncattrs()) == 'valid_min'))):
	        ncfw_var.setncattr('valid_min',ncf.variables[nc_vars[loo]].getncattr('valid_min')) 
	    else:    
		ncfw_var.setncattr('valid_min',min(ncf.variables[nc_vars[0]][np.where(ncf.variables[nc_vars[0]][:] != TheMissing)])) 

            if (any(np.where(np.array(ncf.variables[nc_vars[loo]].ncattrs()) == 'valid_max'))):
	        ncfw_var.setncattr('valid_max',ncf.variables[nc_vars[loo]].getncattr('valid_max')) 
	    else:    
		ncfw_var.setncattr('valid_max',max(ncf.variables[nc_vars[0]][np.where(ncf.variables[nc_vars[0]][:] != TheMissing)])) 

            if (any(np.where(np.array(ncf.variables[nc_vars[loo]].ncattrs()) == 'reference_period'))):
	        ncfw_var.setncattr('reference_period',ncf.variables[nc_vars[loo]].getncattr('reference_period')) 
	    else:    
		ncfw_var.setncattr('reference_period',ClimPeriod) 
	        
	    ncfw_var.setncatts({'long_name':ncf.variables[nc_vars[loo]].getncattr('long_name'),
                            'units':ncf.variables[nc_vars[loo]].getncattr('units')})
# Now fill the variables
    ncfw.variables['time'][:]=TheDaysArray
    ncfw.variables['latitude'][:]=ncf.variables[nc_vars[1]][:]
    ncfw.variables['longitude'][:]=ncf.variables[nc_vars[2]][:]
    if (makemonth == 1): 
        ncfw.variables['month'][:]=TheDaysArray[0:12]

    for loo in range((nvars)):	# miss out time, lat and lon
        print(loo)
	if (nc_vars[loo] != 'time') & (nc_vars[loo] != 'latitude') & (nc_vars[loo] != 'longitude') & (nc_vars[loo] != 'month') & \
	   (nc_vars[loo] != 'times') & (nc_vars[loo] != 'latitudes') & (nc_vars[loo] != 'longitudes') & (nc_vars[loo] != 'months') & \
	   (nc_vars[loo] != 'lat') & (nc_vars[loo] != 'lon'): 
	   
	    print(nc_vars[loo])
            ncfw.variables[nc_vars[loo]][:]=ncf.variables[nc_vars[loo]][:]
   
    
    ncfw.close()
   
    return # ConvertNCCF

    
#************************************************************************
# MAIN PROGRAM
#************************************************************************
# run
ntims=492
nlats=36
nlongs=72
ClimPeriod=u'1976 to 2005'
MDI=-1e30
StYr=1973
StMon=1
EdYr=2013
EdMon=12
DaysArray=MakeDaysSince(StYr,StMon,EdYr,EdMon)
ConvertNCCF(DATADIR+INFILEE+'.nc', DATADIR+OUTFILEE+'.nc',ntims,DaysArray,nlats,nlongs,ClimPeriod,MDI,Typee)
		
#    stop()

print("And, we are done!")

