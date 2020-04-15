# PYTHON 3
# 
# Author: Kate Willett
# Created: 4 March 2019
# Last update: 15 April 2019
# Location: /data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/PYTHON/	
# GitHub: https://github.com/Kate-Willett/PYTHON					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# This code reads in monthly mean gridded (5by5) netCDF files and produces area average time series
# in netCDF and ASCII
#
# Note that the mdi (-1e30) is different between IDL (float?) and Python (double?) and at the moment
# I have netCDF files created in both IDL and Python. So - first thing is to reset all missing values to
# the Python mdi used here.
# Actually now I make netCDF files with -999. as the missing data!
#
# This code was originally IDL written by Kate Willett make_area_avg_ts.pro and used
# globalmean.pro to do the area averaging which was written in IDL by Tim Osborn
# 
# <references to related published material, e.g. that describes data set>
# 
# -----------------------
# LIST OF MODULES
# -----------------------
## Modules
#from datetime import datetime
#import numpy as np
#from matplotlib.dates import date2num,num2date
#import sys, os
#from scipy.optimize import curve_fit,fsolve,leastsq
#from scipy import pi,sqrt,exp
#from scipy.special import erf
#import scipy.stats
#from math import sqrt,pi,radians,sin,cos,acos
#import struct
#from netCDF4 import Dataset
#from netCDF4 import stringtoarr # for putting strings in as netCDF variables
#import pdb
#
## Kates:
#import TestLeap 
#from ReadNetCDF import GetGrid4
#from ReadNetCDF import GetGrid4Slice
#from GetNiceTimes import MakeDaysSince
# 
# -----------------------
# DATA
# -----------------------
# HadISDH-land:
# /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/GRIDS/
# HadISDH.landq.3.0.0.2016p_FLATgridIDPHA5by5_anoms7605_JAN2017_cf.nc
# HadISDH-marine
# /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/GRIDS/
# HadISDH.marineq.1.0.0.2016p_OBSclim2BClocal_anoms8110_JAN2017_cf.nc
# HadISDH.marineq.1.0.0.2016p_OBSclim2BClocalship_anoms8110_JAN2017_cf.nc
# HadISDH-blend:
# /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/GRIDS/
# HadISDH.blendq.1.0.0.2016p_FULL_anoms8110_JAN2017_cf.nc
# HadISDH.blendq.1.0.0.2016p_FULLship_anoms8110_JAN2017_cf.nc
# Other:
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# Make sure all of the EDITABLES are correct
# module load scitools/experimental-current
# python MakeAreaAvgTS.py
#
# may later set up for command line choices: --var <var> --domain <domain>
# var can be q, RH, e, T, Td, Tw, DPD
# domain can be land, marine, marineship, blend, blendship, erainterim, era5
#
# if you want era5 data masked to HadISDH then set MaskIt = True internally
# if you want different years or regions then reset internally
#
# -----------------------
# OUTPUT
# -----------------------
# /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/TIMESERIES/
# HadISDH.landq.3.0.0.2016p_FLATgridIDPHA5by5_anoms7605_JAN2017_areaTS_19732016.nc
# HadISDH.blendq.1.0.0.2016p_FULL_anoms8110_JAN2017_areaTS_19732016.nc
# HadISDH.blendq.1.0.0.2016p_FULLship_anoms8110_JAN2017_areaTS_19732016.nc
# HadISDH.marineq.1.0.0.2016p_OBSclim2BClocal_anoms8110_JAN2017_areaTS_19732016.nc
# HadISDH.marineq.1.0.0.2016p_OBSclim2BClocalship_anoms8110_JAN2017_areaTS_19732016.nc
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
# 
# Version 1 (15 April 2019)
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
# Based on original IDL code by Kate Willett make_area_avg_ts.pro
############################################################################
# Modules
from datetime import datetime
import numpy as np
from matplotlib.dates import date2num,num2date
import sys, os
from scipy.optimize import curve_fit,fsolve,leastsq
from scipy import pi,sqrt,exp
from scipy.special import erf
import scipy.stats
from math import sqrt,pi,radians,sin,cos,acos
import struct
from netCDF4 import Dataset
from netCDF4 import stringtoarr # for putting strings in as netCDF variables
import pdb

# Kates:
import TestLeap 
from ReadNetCDF import GetGrid4
from ReadNetCDF import GetGrid4Slice
from GetNiceTimes import MakeDaysSince

# set up variables
# EDITABLES set up directories and filenames
mdi =        -1e+30

# *** CHOOSE CANDIDATE set up values
styr =       1973	# 1850, 1973, 1950, 1880, 1979
edyr =       2019	# 
climst =     1981	# 1976 or 1981
climed =     2010	# 2005 or 2010

# *** CHOOSE READ IN DATE ***
thenmon =     'JAN'
thenyear =    '2020'

# *** CHOOSE PRINT OUT DATE ***
nowmon =     'JAN'
nowyear =    '2020'

# *** CHOOSE PARAMETER ***
param =      'e'	#'dpd','td','t','tw','e','q','rh','w','evap'

# *** CHOOSE TYPE OF DATA ***
homogtype =  'MARINEship'	#'PHA','ID','DPD', 'RAW', 'OTHER', 'BLEND','BLENDship','MARINE','MARINEship','ERA-Interim', 'ERA5'

# *** CHOOSE VERSION IF HadISDH ***
version =    '1.0.0.2019f' # 3.0.0.3016p 1.0.0.2016p
#version =    '4.2.0.2019f' # 3.0.0.3016p 1.0.0.2016p

# *** CHOOSE WORKING DIRECTORY ***
workingdir = 'UPDATE'+str(edyr)

# *** CHOOSE WHETHER TO MASK WITH HadISDH IF NOT HadISDH ***
# IF mask=True then you will need version, thenmon, thenyear to be correct
mask = False     	# default = 'False', if 'True' then mask to HadISDH equivalent
# MASKFILE (HadISDH set up values)
mstyr =       1973	# 1850, 1973, 1950, 1880
medyr =       2019	# 2013, 2011
mclimst =     1981	# could be 1976 or 1981
mclimed =     2010	# could be 2005 or 2010

# *** CHOOSE WHETHER TO SUB-SELECT A DOMAIN IF NOT HADISDH ***
domain =     'marine'	# 'land','marine','blend'

# *** CHOOSE WHETHER TO WORK WITH ANOMALIES OR ACTUALS - COULD ADD RENORMALISATION IF DESIRED ***
isanom =     True	# 'false' for actual values, 'true' for anomalies

# *** Might add a renormalisation section later ***
# renorm = 'false'

# SEt up area average masks
MaskDict = dict([('G',[-70.,70.]),
                 ('NH',[20.,70.]),
		 ('T',[-20.,20.]),
		 ('SH',[-70.,-20.])])

#*******************************************************
CLMlab =     str(climst)[2:4]+str(climed)[2:4]
climchoice = 'anoms'+CLMlab # 'anoms8110'

MCLMlab =     str(mclimst)[2:4]+str(mclimed)[2:4]
mclimchoice = 'anoms'+MCLMlab # 'anoms8110'

print('Year choice: ',styr,edyr, climst, climed)

if ((mask == True) & (mclimchoice != climchoice)):
    print('Oy - your climatology periods are different between your candidate and mask!')
    print( 'Type c for continue or fix it!')
    pdb.set_trace()

# Latitude and longitude gridbox width
latlg = 5.	#5., 4.
lonlg = 5. 	#5., 4.
  
indir =   '/data/users/hadkw/WORKING_HADISDH/'+workingdir
    
ParamDict = dict([('q',['q','q2m','g/kg']),
                  ('rh',['RH','rh2m','%rh']),
		  ('t',['T','t2m','deg C']),
		  ('td',['Td','td2m','deg C']),
		  ('tw',['Tw','tw2m','deg C']),
		  ('e',['e','e2m','hPa']),
		  ('dpd',['DPD','dpd2m','deg C']),
		  ('evap',['q','evap','cm w.e.'])])

# Dictionary for looking up variable standard (not actually always standard!!!) names for netCDF output of variables
StandardNameDict = dict([('q','specific_humidity'),
             ('rh','relative_humidity'),
	     ('e','vapour_pressure'),
	     ('tw','wetbulb_temperature'),
	     ('t','drybulb_temperature'),
	     ('td','dewpoint_temperature'),
	     ('dpd','dewpoint depression'),
	     ('evap','evaporation')])

# Dictionary for looking up variable long names for netCDF output of variables
LongNameDict = dict([('q','specific_humidity'),
             ('rh','2m relative humidity '),
	     ('e','2m vapour_pressure '),
	     ('tw','2m wetbulb_temperature '),
	     ('t','2m drybulb_temperature '),
	     ('td','2m dewpoint_temperature '),
	     ('dpd','2m dewpoint depression '),
	     ('evap','evaporation from 1by1 ')])

unitees = ParamDict[param][2]
varname = param

if (homogtype == 'ERA-Interim') | (homogtype == 'ERA5'):
    infile = indir+'/OTHERDATA/'+ParamDict[param][1]+'_5by5_monthly_anoms1981-2010_'+homogtype+'_data_1979'+str(edyr)+'.nc'
    outfile = indir+'/STATISTICS/TIMESERIES/'+ParamDict[param][1]+'_5by5_monthly_anoms1981-2010_'+homogtype+'_areaTS_1979'+str(edyr)
    # reset varname for ERA
    varname = ParamDict[param][1]
elif (homogtype == 'MARINE'):
    infile = indir+'/STATISTICS/GRIDS/HadISDH.marine'+ParamDict[param][0]+'.'+version+'_BClocal5by5both_anoms8110_'+thenmon+thenyear+'_cf.nc'
    outfile = indir+'/STATISTICS/TIMESERIES/HadISDH.marine'+ParamDict[param][0]+'.'+version+'_BClocal5by5both_anoms8110_'+nowmon+nowyear+'_areaTS_'+str(styr)+str(edyr)
elif (homogtype == 'MARINEship'):
    infile = indir+'/STATISTICS/GRIDS/HadISDH.marine'+ParamDict[param][0]+'.'+version+'_BClocalSHIP5by5both_anoms8110_'+thenmon+thenyear+'_cf.nc'
    outfile = indir+'/STATISTICS/TIMESERIES/HadISDH.marine'+ParamDict[param][0]+'.'+version+'_BClocalSHIP5by5both_anoms8110_'+nowmon+nowyear+'_areaTS_'+str(styr)+str(edyr)
elif (homogtype == 'ID'):
    infile = indir+'/STATISTICS/GRIDS/HadISDH.land'+ParamDict[param][0]+'.'+version+'_FLATgridIDPHA5by5_anoms8110_'+thenmon+thenyear+'_cf.nc'
    outfile = indir+'/STATISTICS/TIMESERIES/HadISDH.land'+ParamDict[param][0]+'.'+version+'_FLATgridIDPHA5by5_anoms8110_'+nowmon+nowyear+'_areaTS_'+str(styr)+str(edyr)
elif (homogtype == 'PHA'):
    infile = indir+'/STATISTICS/GRIDS/HadISDH.land'+ParamDict[param][0]+'.'+version+'_FLATgridPHA5by5_anoms8110_'+thenmon+thenyear+'_cf.nc'
    outfile = indir+'/STATISTICS/TIMESERIES/HadISDH.land'+ParamDict[param][0]+'.'+version+'_FLATgridPHA5by5_anoms8110_'+nowmon+nowyear+'_areaTS_'+str(styr)+str(edyr)
elif (homogtype == 'DPD'):
    infile = indir+'/STATISTICS/GRIDS/HadISDH.land'+ParamDict[param][0]+'.'+version+'_FLATgridPHADPD5by5_anoms8110_'+thenmon+thenyear+'_cf.nc'
    outfile = indir+'/STATISTICS/TIMESERIES/HadISDH.land'+ParamDict[param][0]+'.'+version+'_FLATgridPHADPD5by5_anoms8110_'+nowmon+nowyear+'_areaTS_'+str(styr)+str(edyr)
elif (homogtype == 'RAW'):
    infile = indir+'/STATISTICS/GRIDS/HadISDH.land'+ParamDict[param][0]+'.'+version+'_FLATgridRAW5by5_anoms8110_'+thenmon+thenyear+'_cf.nc'
    outfile = indir+'/STATISTICS/TIMESERIES/HadISDH.land'+ParamDict[param][0]+'.'+version+'_FLATgridRAW5by5_anoms8110_'+nowmon+nowyear+'_areaTS_'+str(styr)+str(edyr)
elif (homogtype == 'BLEND'):
    infile = indir+'/STATISTICS/GRIDS/HadISDH.blend'+ParamDict[param][0]+'.'+version+'_BClocal5by5both_anoms8110_'+thenmon+thenyear+'_cf.nc'
    outfile = indir+'/STATISTICS/TIMESERIES/HadISDH.blend'+ParamDict[param][0]+'.'+version+'_BClocal5by5both_anoms8110_'+nowmon+nowyear+'_areaTS_'+str(styr)+str(edyr)
elif (homogtype == 'BLENDship'):
    infile = indir+'/STATISTICS/GRIDS/HadISDH.blend'+ParamDict[param][0]+'.'+version+'_BClocalSHIP5by5both_anoms8110_'+thenmon+thenyear+'_cf.nc'
    outfile = indir+'/STATISTICS/TIMESERIES/HadISDH.blend'+ParamDict[param][0]+'.'+version+'_BClocalSHIP5by5both_anoms8110_'+nowmon+nowyear+'_areaTS_'+str(styr)+str(edyr)

if (domain == 'land'):
    maskfile = indir+'/STATISTICS/GRIDS/HadISDH.land'+ParamDict[param][0]+'.'+version+'_FLATgridIDPHA5by5_'+mclimchoice+'_'+thenmon+thenyear+'_cf.nc'
if (domain == 'marine'):
    maskfile = indir+'/STATISTICS/GRIDS/HadISDH.marine'+ParamDict[param][0]+'.'+version+'_BClocalSHIP5by5both_'+mclimchoice+'_'+thenmon+thenyear+'_cf.nc'
if (domain == 'blend'):
    maskfile = indir+'/STATISTICS/GRIDS/HadISDH.blend'+ParamDict[param][0]+'.'+version+'_FLATgridIDPHA5by5_'+mclimchoice+'_'+thenmon+thenyear+'_cf.nc'

inlandcover = '/data/users/hadkw/WORKING_HADISDH/'+workingdir+'/OTHERDATA/HadCRUT.4.3.0.0.land_fraction.nc'

if (mask == True):
    outfile = outfile+'_MASK'

if (isanom == False):
    outfile = outfile+'_ABS'


# Time and dimension variables
nyrs =     (edyr+1)-styr
nmons =    nyrs*12
stlt =     -90+(latlg/2.)
stln =     -180+(lonlg/2.)
nlats =    int(180/latlg)
nlons =    int(360/lonlg)

mnyrs =     (medyr+1)-mstyr
mnmons =    mnyrs*12

# Get pointers for pulling out the matching time slice of masked data
mskstpt = (styr - mstyr) * 12
mskedpt = mnmons

lats = (np.arange(nlats)*latlg) + stlt
lons = (np.arange(nlons)*lonlg) + stln

############################################################################
# SUBROUTINES #
############################################################################
# AreaMean
def AreaMean(DataField,TheLats,MaskField=None,Cover=None):
    '''
    This function computes the spatial area average using cosine weighting of the latitudes
    Its based on original IDL code by Tim Osborn globalmean.pro
    Computes a global mean from a field (or set of fields if fd is 3D),
    accounting for missing data.  
    A separate mask (of same dimension) can (has to be at the moment) be supplied if required.  
    Single hemisphere means can also be returned (not at the moment)
    The number of boxes with data is returned in cover (not at the moment)
    
    mdi is passed from above
    
    DOES NOT ASSUME MASK IS IDENTICAL FOR EACH TIME STEP!!!
    
    INPUTS:
    DataField[:,:,:] - time, lat, lon np.array of data - can cope with missing data (mdi)
    TheLats[:] - np.array of latitudes
    Optional:
    MaskField[:,:,:] - if not supplied then average computed over entire DataField
    Cover[:] - if supplied then the number of boxes non-missing is returned per time step 
    OUTPUTS:
    DataTS[:] - np.array time series of area averages
        
    '''
    # Find dimensions
    fullsize = np.shape(DataField)

    if (len(fullsize) < 2) | (len(fullsize) > 3): 
        print('DataField must be 2D or 3D')
        pdb.set_trace()
	
    # Set up dimensions depending on whether its 2D or 3D
    if (len(fullsize) == 3):
        Ntims = fullsize[0]
        Nlons = fullsize[2] #nx = fullsize(1)
        Nlats = fullsize[1] #ny = fullsize(2)

    else:
        Ntims = 1
        Nlons = fullsize[1] #nx = fullsize(1)
        Nlats = fullsize[0] #ny = fullsize(2)

    # if a mask is supplied then use to remove points from fd
    masksize = np.shape(MaskField)
    if (len(masksize) > 0):
  
        if (len(masksize) != len(fullsize)) & (len(masksize) != 2):
            print('Mask is wrong size')
            pdb.set_trace()

        # Set up dimensions depending on whether its 2D or 3D
        if (len(masksize) == 3):
            if (masksize[0] != Ntims):
                print('Mask is wrong size')
                pdb.set_trace()
            if (masksize[2] != Nlons) | (masksize[1] != Nlats):
                print('Mask is wrong size')
                pdb.set_trace()
            Ntimsmask = masksize[0]
        else: 
            if (masksize[1] != Nlons) | (masksize[0] != Nlats):
                print('Mask is wrong size')
                pdb.set_trace()
            Ntimsmask = 1
	
    # In the case of no mask then compute over all boxes
    else:
        Ntimsmask = 1
        MaskField = np.empty((Nlats,Nlons),dtype = float) # IDL was lons,lats

    # Now make arrays
    # IDL code below but it seems redundant to me because data was already lon, lat, time in IDL
    # In python its time, lat, lon!!!
    #fd = reform(fd,nx,ny,nz)
    #mask=reform(mask,nx,ny,nzmask)
    sumval = np.zeros(Ntims,dtype = float) 
    sumarea = np.zeros(Ntims,dtype = float) 
#    # For southern hemisphere component
#    sval = np.zeros(Ntims,dtype = float) 
#    sarea = np.zeros(Ntims,dtype = float) 
#    # For northern hemisphere component
#    nval = np.zeros(Ntims,dtype = float) 
#    narea = np.zeros(Ntims,dtype = float)

    # If Cover exists then set up for filling it
    CoverTest = np.shape(Cover)
    if (len(CoverTest) > 0):
        # For number of non-mdi boxes contributing 
        Cover = np.zeros(Ntims,dtype = float) 

#    print('Test AreaMean set up so far')
#    pdb.set_trace()

    # If the MaskField has been supplied then it should have the same dimensions as DataField
    # DOes not assume that mask is identical for each time step
    for ln in range(Nlons): #i
        for lt in range(Nlats): #j
	
#            print(ln,lt)
	 
	    # Is this lat/lon a 1 or an mdi in the mask - 1 = compute!
            temp_data = np.copy(DataField[:,lt,ln])				
            CarryOn = 0
            if (Ntims == Ntimsmask): 
                temp_mask = np.copy(MaskField[:,lt,ln])			
                mask_cover = np.where(temp_mask == mdi)
                if (len(mask_cover[0]) > 0): 
                    temp_data[mask_cover] = mdi	# 
                kl = np.where(temp_data != mdi)
                CarryOn = 1	  
            else:
                if (MaskField[lt,ln] != mdi):
                    kl = np.where(temp_data != mdi)
                    CarryOn = 1	  
            if (CarryOn == 1) & (len(kl) > 0):
#                print('Test kl values and how this bit works')	
#                pdb.set_trace()			
                sumval[kl] = sumval[kl] + temp_data[kl]*cos(radians(TheLats[lt]))
                sumarea[kl] = sumarea[kl] + cos(radians(TheLats[lt]))
                if (len(CoverTest) > 0):
                    Cover[kl] = Cover[kl] + 1.
#                if (TheLats[lt] < 0.):
#                    sval[kl] = sval[kl] + DataField[kl,lt,ln]*cos(radians(TheLats[lt]))
#                    sarea[kl] = sarea[kl] + cos(radians(TheLats[lt]))
#                else:
#                    nval[kl] = nval[kl] + DataField[kl,lt,ln]*cos(radians(TheLats[lt]))
#                    narea[kl] = narea[kl] + cos(radians(TheLats[lt]))

    gots = np.where(sumarea > 0)
    if (len(gots[0]) > 0): 
        sumval[gots] = sumval[gots] / sumarea[gots]
    
    misses = np.where(sumarea == 0)
    if (len(misses[0]) > 0): 
        sumval[misses] = mdi
    
    if (Ntims == 1): # convert to scalars
        sumval = sumval[0]
  
    if (len(CoverTest) > 0):
        return sumval, Cover 
    else:	
        return sumval

############################################################################
# WriteNetCDF
def WriteNetCDF(Filename,TheGArray,TheNHArray,TheTArray,TheSHArray,TheTimes,TheStYr, TheEdYr, TheClimStart, TheClimEnd, TheName, TheStandardName, TheLongName, TheUnit, TheRegions):
    '''
    This function writes out a NetCDF 4 file
    
    INPUTS:
    Filename - string file name
    TheGArray[:] - time array of global average values
    TheNHArray[:] - time array of nhem average values
    TheTArray[:] - time array of tropical average values
    TheSHArray[:] - time array of shem average values
    TheTimes[:] - times in days since TheStYr, Jan 1st    
    TheStYr - integer start year assumes Jan start 
    TheEdYr - integer end year assumes Dec start 
    TheClimStart - integer start of clim Jan start 
    TheClimEnd - integer end of clim Dec start
    TheName - string short name of var q2m
    TheStandardName - string standard name of variable
    TheUnit - string unit of variable
    TheRegions - dictionary with G, NH, T and SH [lower lat, upper lat] boundaries
    OUTPUTS:
    None
    
    '''
    
    # No need to convert float data using given scale_factor and add_offset to integers - done within writing program (packV = (V-offset)/scale
    # Not sure what this does to float precision though...

    # Create a new netCDF file - have tried zlib=True,least_significant_digit=3 (and 1) - no difference
    ncfw = Dataset(Filename+'.nc','w',format='NETCDF4_CLASSIC') # need to try NETCDF4 and also play with compression but test this first

    # Set up the dimension names and quantities
    ncfw.createDimension('time',len(TheTimes))
    
    # Go through each dimension and set up the variable and attributes for that dimension if needed
    MyVarT = ncfw.createVariable('time','f4',('time',))
    MyVarT.standard_name = 'time'
    MyVarT.long_name = 'time'
    MyVarT.units = 'days since '+str(TheStYr)+'-1-1 00:00:00'
    MyVarT.start_year = str(TheStYr)
    MyVarT.end_year = str(TheEdYr)
    MyVarT[:] = TheTimes

    # Go through each variable and set up the variable attributes
    # I've added zlib=True so that the file is in compressed form
    # I've added least_significant_digit=4 because we do not need to store information beyone 4 significant figures.
    MyVarG = ncfw.createVariable('glob_'+TheName+'_anoms','f4',('time',),fill_value = mdi,zlib=True,least_significant_digit=4)
    #MyVarG.standard_name = TheStandardName
    MyVarG.long_name = TheLongName+' global average anomalies '+'%5.1f' % (TheRegions['G'][0])+' to '+'%5.1f' % (TheRegions['G'][1])
    MyVarG.units = TheUnit
    MyVarG.valid_min = np.min(TheGArray)
    MyVarG.valid_max = np.max(TheGArray)
#    MyVarG.missing_value = mdi
    # Provide the data to the variable - depending on howmany dimensions there are
    MyVarG[:] = TheGArray[:]  	

    MyVarN = ncfw.createVariable('nhem_'+TheName+'_anoms','f4',('time',),fill_value = mdi,zlib=True,least_significant_digit=4)
    #MyVarN.standard_name = TheStandardName
    MyVarN.long_name = TheLongName+' northern hemisphere average anomalies '+'%5.1f' % (TheRegions['NH'][0])+' to '+'%5.1f' % (TheRegions['NH'][1])
    MyVarN.units = TheUnit
    MyVarN.valid_min = np.min(TheNHArray)
    MyVarN.valid_max = np.max(TheNHArray)
#    MyVarN.missing_value = mdi
    # Provide the data to the variable - depending on howmany dimensions there are
    MyVarN[:] = TheNHArray[:]  	

    MyVarT = ncfw.createVariable('trop_'+TheName+'_anoms','f4',('time',),fill_value = mdi,zlib=True,least_significant_digit=4)
    #MyVarT.standard_name = TheStandardName
    MyVarT.long_name = TheLongName+' tropical average anomalies '+'%5.1f' % (TheRegions['T'][0])+' to '+'%5.1f' % (TheRegions['T'][1])
    MyVarT.units = TheUnit
    MyVarT.valid_min = np.min(TheTArray)
    MyVarT.valid_max = np.max(TheTArray)
#    MyVarT.missing_value = mdi
    # Provide the data to the variable - depending on howmany dimensions there are
    MyVarT[:] = TheTArray[:]  	

    MyVarS = ncfw.createVariable('shem_'+TheName+'_anoms','f4',('time',),fill_value = mdi,zlib=True,least_significant_digit=4)
    #MyVarS.standard_name = TheStandardName
    MyVarS.long_name = TheLongName+' southern hemisphere average anomalies '+'%5.1f' % (TheRegions['SH'][0])+' to '+'%5.1f' % (TheRegions['SH'][1])
    MyVarS.units = TheUnit
    MyVarS.valid_min = np.min(TheSHArray)
    MyVarS.valid_max = np.max(TheSHArray)
#    MyVarS.missing_value = mdi
    # Provide the data to the variable - depending on howmany dimensions there are
    MyVarS[:] = TheSHArray[:]  	

    ncfw.close()

    return

############################################################################
# WriteText
def WriteText(Filename,TheGArray,TheNHArray,TheTArray,TheSHArray,TheTimes,TheStYr,TheEdYr):
    '''
    This function writes out two files with year or yearmonth and then Global, N Hemi, Tropics and S Hemi time series
    There has to be at least 11 months of the year present to calculate an annual value
    '''
    # Minimum missing data threshold
    MinThresh = 11
    
    # Open the file for annual and monthly
    ann = open(Filename+'_annual.dat', "a")
    mon = open(Filename+'_monthly.dat', "a")

    # Write the file header
    ann.write("DATE  GLOBAL  N_HEMI TROPICS  S_HEMI\n")
    mon.write("  DATE  GLOBAL  N_HEMI TROPICS  S_HEMI\n")

    # Loop through each year and month and write out
    yy = 0
    mm = 0
    for tt in range(len(TheTimes)):
        
	# Write monthlies to file
        m = '%02i' % (mm+1)
#        pdb.set_trace()
        mon.write('{:4d}{:2s}  {:6.2f}  {:6.2f}  {:6.2f}  {:6.2f}\n'.format(yy+TheStYr,m,TheGArray[tt],TheNHArray[tt],TheTArray[tt],TheSHArray[tt]))
        mm = mm+1
	
        if (mm == 12):
            # Get annual mean value and write to file
            TmpArr = TheGArray[tt-11:tt+1]
            gots = np.where(TmpArr > mdi)
            if (len(gots[0]) >= MinThresh):
                TheGVal = np.mean(TmpArr[gots])
            else:
                TheGVal = mdi    		

            TmpArr = TheNHArray[tt-11:tt+1]
            gots = np.where(TmpArr > mdi)
            if (len(gots[0]) >= MinThresh):
                TheNHVal = np.mean(TmpArr[gots])
            else:
                TheNHVal = mdi    		

            TmpArr = TheTArray[tt-11:tt+1]
            gots = np.where(TmpArr > mdi)
            if (len(gots[0]) >= MinThresh):
                TheTVal = np.mean(TmpArr[gots])
            else:
                TheTVal = mdi    		

            TmpArr = TheSHArray[tt-11:tt+1]
            gots = np.where(TmpArr > mdi)
            if (len(gots[0]) >= MinThresh):
                TheSHVal = np.mean(TmpArr[gots])
            else:
                TheSHVal = mdi    		

            ann.write('{:4d}  {:6.2f}  {:6.2f}  {:6.2f}  {:6.2f}\n'.format(yy+TheStYr,TheGVal, TheNHVal, TheTVal, TheSHVal))
            yy = yy+1
            mm = 0

    # CLose the files
    ann.close()
    mon.close()
    
    return
    
############################################################################
# MAIN #
############################################################################
# read in files
LatInfo = ['latitude'] 
LonInfo = ['longitude'] 

if (isanom == True):
    if (homogtype == 'ERA-Interim') | (homogtype == 'ERA5'):
        if (domain == 'land'):
            ReadInfo = [varname+'_anoms_land','time']
            outfile = outfile+'_land'
        if (domain == 'marine'):
            ReadInfo = [varname+'_anoms_ocean','time']
            outfile = outfile+'_marine'
    else:
        ReadInfo = [varname+'_anoms','time']
else:
    if (homogtype == 'ERA-Interim') | (homogtype == 'ERA5'): 
        if (domain == 'land'):
            ReadInfo = [varname+'_land','time']
            outfile = outfile+'_land'
        if (domain == 'marine'):
            ReadInfo = [varname+'_ocean','time']
            outfile = outfile+'_land'
    else:
        ReadInfo = [varname+'_abs','time']

print('Reading in the data for :',homogtype)
TmpVals,Latitudes,Longitudes = GetGrid4(infile,ReadInfo,LatInfo,LonInfo)

# Seperate out data and times
TheData = TmpVals[0]
Times = TmpVals[1]
TmpVals = []

# Check the mdis = IDL output netCDF differs from Python output
bads = np.where(TheData < -10000)
if (len(bads[0]) > 0):
    TheData[bads] = mdi

# Now if we're masking then read in the mask for the time slice of ERA-Interim
if (mask == True): 

    SliceInfo = dict([('TimeSlice',[mskstpt,mskedpt]),
           		 ('LatSlice',[0,nlats]),
           		 ('LonSlice',[0,nlons])]) 
	
    if (isanom == True):
        ReadInfo = [param+'_anoms']
    else:
        ReadInfo = [param+'_abs']

    print('Reading in the mask data for :',homogtype)
    TmpVals,Latitudes,Longitudes = GetGrid4Slice(maskfile,ReadInfo,SliceInfo,LatInfo,LonInfo)

    # Seperate out data and times
    MSKTheData = TmpVals
#    MSKTimes = TmpVals[1]
    TmpVals = []
  
    # Check the mdis = IDL output netCDF differs from Python output
    bads = np.where(MSKTheData < -10000)
    if (len(bads[0]) > 0):
        MSKTheData[bads] = mdi
  
    # mask out points in candidate that do not have data in the mask
    bads = np.where(MSKTheData <= mdi)
#    pdb.set_trace()
    if (len(bads[0]) > 0):
        TheData[bads] = mdi
    
#  # make anomalies from the monthlies if you want to be precise about anomalising with same coverage as HadISDH
#  newq_values=make_array(nlons,nlats,nmons,/float,value=mdi)
#  FOR ltt=0,nlats-1 DO BEGIN
#    FOR lnn=0,nlons-1 DO BEGIN
#      subarr=REFORM(q_values(lnn,ltt,*),12,nyrs)
#      FOR mm=0,11 DO BEGIN
#        gots=WHERE(subarr(mm,*) NE mdi,count)
#	 climsub=subarr(mm,mclimst-styr:mclimst-styr)
#	 gotsC=WHERE(climsub NE mdi,countC)
#	 IF (countC GE 15) THEN subarr(mm,gots)=subarr(mm,gots)-MEAN(climsub(gotsC)) ELSE subarr(mm,*)=mdi
#      ENDFOR
#      newq_values(lnn,ltt,*)=REFORM(subarr,nmons)
#    ENDFOR
#  ENDFOR
#  #stop
#  q_values=newq_values

# make spatial area masks - set anything greater than 70 deg lat to mdi

global_mask = np.zeros((nlats,nlons),dtype = float)
global_mask.fill(1)
nhem_mask = np.copy(global_mask)
shem_mask = np.copy(global_mask)
trop_mask = np.copy(global_mask)

for deg in range(nlats):
    if (lats[deg] < MaskDict['G'][0]) | (lats[deg] > MaskDict['G'][1]):
        global_mask[deg,:] = mdi
    if (lats[deg] < MaskDict['NH'][0]) | (lats[deg] > MaskDict['NH'][1]):
        nhem_mask[deg,:] = mdi
    if (lats[deg] < MaskDict['T'][0]) | (lats[deg] > MaskDict['T'][1]):
        trop_mask[deg,:] = mdi
    if (lats[deg] < MaskDict['SH'][0]) | (lats[deg] > MaskDict['SH'][1]):
        shem_mask[deg,:] = mdi

global_mask_3d = np.repeat(global_mask[np.newaxis,:,:],nmons, axis = 0)
nhem_mask_3d = np.repeat(nhem_mask[np.newaxis,:,:],nmons, axis = 0)
shem_mask_3d = np.repeat(shem_mask[np.newaxis,:,:],nmons, axis = 0)
trop_mask_3d = np.repeat(trop_mask[np.newaxis,:,:],nmons, axis = 0)

#CoverTS = np.empty(nmons,dtype = float)
#CoverTS.fill(mdi)
#glob_avg_ts,CoverTS = AreaMean(TheData,lats,global_mask_3d,CoverTS)
glob_avg_ts = AreaMean(TheData,lats,global_mask_3d)
print(len(glob_avg_ts),np.max(glob_avg_ts),np.min(glob_avg_ts))
#pdb.set_trace()

nhem_avg_ts = AreaMean(TheData,lats,nhem_mask_3d)
print(len(nhem_avg_ts),np.max(nhem_avg_ts),np.min(nhem_avg_ts))

trop_avg_ts = AreaMean(TheData,lats,trop_mask_3d)
print(len(trop_avg_ts),np.max(trop_avg_ts),np.min(trop_avg_ts))

shem_avg_ts = AreaMean(TheData,lats,shem_mask_3d)
print(len(shem_avg_ts),np.max(shem_avg_ts),np.min(shem_avg_ts))
  
# save to file as netCDF and .dat

WriteNetCDF(outfile,glob_avg_ts,nhem_avg_ts,trop_avg_ts,shem_avg_ts,Times,styr, edyr, climst, climed, ParamDict[param][0], StandardNameDict[param], LongNameDict[param], unitees, MaskDict)
WriteText(outfile,glob_avg_ts,nhem_avg_ts,trop_avg_ts,shem_avg_ts,Times,styr, edyr)

# Note if any of the series have missing data because at these large scales they should not
if (len(np.where(glob_avg_ts <= mdi)[0]) > 0):
    
    print('Missing months for Global average: ',len(np.where(glob_avg_ts <= mdi)[0]))
    pdb.set_trace()

if (len(np.where(nhem_avg_ts <= mdi)[0]) > 0):
    
    print('Missing months for NHemi average: ',len(np.where(nhem_avg_ts <= mdi)[0]))
    pdb.set_trace()

if (len(np.where(trop_avg_ts <= mdi)[0]) > 0):
    
    print('Missing months for Tropics average: ',len(np.where(trop_avg_ts <= mdi)[0]))
    pdb.set_trace()

if (len(np.where(shem_avg_ts <= mdi)[0]) > 0):
    
    print('Missing months for Shemi average: ',len(np.where(shem_avg_ts <= mdi)[0]))
    pdb.set_trace()

print('And we are done!')
