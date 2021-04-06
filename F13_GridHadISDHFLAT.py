# PYTHON 3
# 
# Author: Kate Willett
# Created: 1 February 2013 IDL, Converted to Python 3 12th Jan 2021
# Last update: 12 January 2021
# Location: /home/h04/hadkw/HadISDH_Code/HADISDH_BUILD/		
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# For selected variable, grid the data and uncertainties, including the gridbox sampling uncertainty

# Read in list of goods
# - IF RAW: Read in raw netCDF of abs, anoms, clims.
# - IF PHA/IDPHA/PHADPD: Read in homogenised netCDF of abs, anoms, err, adjE, obsE, clmE, clims and climsds.

# move from gridbox to gridbox starting with -177.5W, 87.5S
# if there is a station then begin
# find all stations in GB - store lat, lon, elev
# calc gridbox mean (abs, anoms, clims), standard deviation (sds of abs), uncertainties (combined assuming no correlation and unique values) - already 2 sigma when read in!!!

# Call gridbox_sampling_uncertainty.py to compute gridbox sampling error due to missing data and incomplete spatial sampling.

# Write out to netCDF, ascii (abs, anoms, uncertainty) - all errors are 2 sigma errors!!!

# Write out gridding results min/max of each var

# 
# -----------------------
# LIST OF MODULES
# -----------------------
#import numpy as np # used
#import numpy.ma as npm # used
#from datetime import datetime # used
#import matplotlib.pyplot as plt
#import sys, os, getopt # used
#import struct
#import glob # used
#import pdb # used
#import netCDF4 as nc4
#
## Kate's Functions
#import CalcHums
#from RandomsRanges import LetterRange
#import gridbox_sampling_uncertainty as gsu
#
# -----------------------
# DATA
# -----------------------
# Input station list of 'good stations':
#  /scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/'
#    Posthomog<typee><var>_anoms'+CLMlab+'_<goods>HadISDH.'+versiondots+'.txt' 
# Input homogenised netCDF files of data with station uncertainties to grid - IDPHA version and PHADPD:
#  /scratch/hadkw/UPDATE<YYYY>/MONTHLIES/HOMOG/<typee>NETCDF/<VAR>DIR/' # this will then be PHANETCDF or IDPHANETCDF
#    <station>'_anoms<climLAB>_homog.nc'
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# > module load scitools/default-current
# > python F13_GridHadISDHFLAT --var <var> --typee <type>
#
## Which variable?
# var = 'dpd'	#'dpd','td','t','tw','e','q','rh'
#
## Which homog type?
# typee = 'PHA'	#'PHA' (for DPD only),'IDPHA' (for t, e, q, rh and tw),'PHADPD' (for Td) 
#
#
# Or ./F13_submit_spice.sh
# 
# 
# -----------------------
# OUTPUT
# -----------------------
# The gridded netCDF file:
#  /scratch/hadkw/UPDATE<YYYY>/STATISTICS/GRIDS/
#    HadISDH.land<var>.'+version+'_FLATgrid<homogtype>PHA5by5_anoms8110.nc 
# The summary min and max values for each variable within the netCDF file:
#  /scratch/hadkw/UPDATE<YYYY>/LISTS_DOCS/
#    GriddingResults_<versiondots>_anoms8110.txt	max/mins of all fields in nc file 
#
# THESE ARE OUTPUT AS 2 SIGMA ERRORS!!!
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
# 
# Version 6 (12 January 2021)
# ---------
#  
# Enhancements
# Double checked uncertainty calculations and they are quantitatively the same as for the marine code 
# but expressed differently so I have changed the code to match that for the marine.
#  
# Changes
# Now Python 3
# Using pythong gridbox_sampling_uncertainty.py rather than IDL code (as used for the marine data)
# gridbox_sampling_uncertainty.py uses HadCRUT.4.3.0.0.land_fraction.py to select land boxes
# gridbox_sampling_uncertainty.py sets rbar to 0.8 if there are missing values rather than the 0.1 previously which 
# was far too low. 0.8 is about mid-range for rbar
# Sampling uncertainty is very slightly different order 0.001 in a few places
# We now use the mean number of stations contributing to the gridbox rather than the maximum - this is smaller so 
# will result in slightly larger sampling uncertainty, especially in gridboxes with very few stations LARGER UNCERTAINTIES
# Combining uncertainty over gridbox now uses actual numer of stations for that month rather than total over time 
# period for that gridbox so new gridbox uncs are LARGER than IDL ones where there are fewer 
# stations contributing to the gridbox compared to the total. LARGER UNCERTAINTIES
#  
# Bug fixes
# In 2019 I reduced the combined uncertainties because I had thought that *2 made them 4 sigma. I hadn;t noticed the /2 in the equation. So, while the original
# equation of sqrt((staterr/2)^2 + (samperr/2)^2)*2 was pointless it was right and 2019 would have had combined uncertainty that was too small - now corrected!!!
# LARGER UNCERTAINTIES - BY *2
#
#
# Version 5 (29 March 2018)
# ---------
#  
# Enhancements
#  
# Changes
#  
# Bug fixes
# Wrong FILE_SEARCH string was finding multiple files and therefore sometimes reading in the wrong one (with sats/subzeros or duplicate!)
#
# Version 4 (13 February 2018)
# ---------
#  
# Enhancements
#Now has param and homogtype called at run time
## Which variable? T first, RH, DPD, q, e, td, tw
#param =      'tw'
## Which homog type?
#homogtype =  'ID'		#'ID','DPD' for Td, 'PHA' - req for DPD or PHA versions of all variables
#
# Now looks at Posthomog...lists to get station counts automatically rather than being hard coded
#  
# Changes
#  
# Bug fixes
# NetCDF err outputs had wrong long_names
#
# Version 3 (1 February 2017)
# ---------
#  
# Enhancements
# General tidy up and improved headers
#  
# Changes
#  
# Bug fixes
#
#
# Version 2 (7 September 2017)
# ---------
#  
# Enhancements
# General tidy up and reframe of tweakable variables to make the file/data batching easier for each variable/climatology choice etc.
# Can now work with different anomaly periods 7605 or 8110 which have to be created by create_homogNCDFall_stunc_JAN2015.pro
#  
# Changes
#  
# Bug fixes
# Fixed bug in sampling error which was only using first 29 years of the 30 year climatology period (missing +1)
# This fix is actually in the calc_samplingerrorJUL2012_nofill.pro.

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
# climerr is difference for some gridboxes - larger for new compared to old - when old is small new is large???
# sampling error needs to be saved only where there are data - not for all land.

#**** THIS IS WHERE TO ADD UNCERTAINTY ALA BROHAN et al. 2006
# Station error:
#   Tob - Tclim + errorCLIM + measurementerror + homogadj + adjuncertainty + reporting error
# Samping error:
# SE^2 = GBstdev*avg.intersite correlation*(1-avg.intersite corr)
#        --------------------------------------------------------
#          1 + ((num stations - 1) * avg.intersite correlation)
# Bias error:
# urbanisation? exposure change? irrigation?

# combine these by adding in quadrature.

# sampling error - after Jones et al. 1997

#Shat^2 = variance of gridbox(extended?) means over climatology period
#n = number of stations contributing to gridbox(extended?) over climatology period
#Xo = correlation decay distance (km) for that gridbox (where correlation = 1/e)
#X = diagonal from bottom left to top right of gridbox(extended?) (km) - use lats, longs and dist_calc
#rbar = (Xo/X)*(1-e(-X/Xo))
#sbar^2 = mean station variance within the gridbox
#sbar^2 = (Shat^2*n)/(1+((n-1)*rbar))
#INFILL empty gridboxes by interpolated Xo and then calculating rbar
#SE^2 = gridbox sampling error
#SE^2 = (sbar^2*rbar*(1-rbar))/(1+((n-1)*rbar))
#SE^2 (where n=0) = sbar^2*rbar (INFILL GB with Shat^2???)
#SEglob^2 = global average sampling error
#SEglob^2 = SEbar^2/Neff
#SEbar^2 = (SUM(SE^2*cos(lat)))/(SUM(cos(lat)))
#Neff = number of effectively independent points
#Neff = (2*R)/F
#R = radius of the earth (6371 km)
#F=(((e((-piR)/Xobar))/R)+(1/R))/((1/(Xobar^2))+(1/R^2))
#Xobar=(SUM(Xo*cos(lat)))/(SUM(cos(lat)))


#******************************************************
# Global variables and imports
# Inbuilt: (may not all be required actually)
import numpy as np # used
import numpy.ma as npm # used
from datetime import datetime # used
import matplotlib.pyplot as plt
import sys, os, getopt # used
import struct
import glob # used
import pdb # used
import netCDF4 as nc4
#from subprocess import call, check_output, run, PIPE # used

# Kate's Functions
import CalcHums
from RandomsRanges import LetterRange
import gridbox_sampling_uncertainty as gsu

# Start and end years if HardWire = 1
styear       = 1973
edyear       = 2019

# Which climatology?
MYclst = 1981	# 1976, 1981
MYcled = 2010	# 2005, 2010
CLMlab = str(MYclst)[2:4]+str(MYcled)[2:4]

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

# AttribDict held in memory to probide global attribute text later
#' Read in the attribute file to get all of the info
with open('F1_HadISDHBuildAttributes.txt') as f:
    
    AttribDict = dict(x.rstrip().split('=', 1) for x in f)

# NOT CODED THIS FUNCTIONALITY YET
## Are we working with homogenised actuals (True) or anomalies (False)?
#Actuals = True

# Set up directories locations
updateyy  = str(edyear)[2:4]
updateyyyy  = str(edyear)
workingdir  = '/scratch/hadkw/UPDATE'+updateyyyy
#workingdir  = '/data/users/hadkw/WORKING_HADISDH/UPDATE'+updateyyyy

# Set up filenames
INDIRLIST = workingdir+'/LISTS_DOCS/'
INDIRHOM = workingdir+'/MONTHLIES/HOMOG/' # this will then be PHAASCII or IDPHAASCII

#workingdir  = '/scratch/hadkw/UPDATE'+updateyyyy
OUTDIRLIST = workingdir+'/LISTS_DOCS/GriddingResults_'+versiondots+'_anoms'+CLMlab+'.txt'	
OUTDIRDAT = workingdir+'/STATISTICS/GRIDS/' 

# File for output stats but also for reading in missed adjustment uncertainties
OUTPUTLOG = workingdir+'/LISTS_DOCS/OutputLogFile'+versiondots+'.txt'

# Set up variables
MDI = -1e+30

LatBox = 5. # latitude gridbox size
LonBox = 5. # longitude gridbox size

# Dictionaries for param, units, homogdirprefix, STATION FILE PREFIX, standard name, long name, raw data suffix(only for test run)
ParamDict = dict([('q',['q','g/kg','IDPHA','Q','specific_humidity','monthly mean 2m specific humidity','qhum']),
	          ('rh',['RH','%rh','IDPHA','RH','relative_humidity','monthly mean 2m relative humidity','rhum']),
	          ('t',['T','deg C','IDPHA','T','drybulb_temperature','monthly mean 2m dry bulb temperature','temp']), # Note this needs to be changed to IDPHAMG later
	          ('td',['Td','deg C','IDPHA','TD','dewpoint_temperature','monthly mean 2m dew point temperature','dewp']),
	          ('tw',['Tw','deg C','IDPHA','TW','wetbulb_temperature','monthly mean 2m wetbulb temperature','twet']),
	          ('e',['e','hPa','IDPHA','E','vapour_pressure','monthly mean 2m vapour pressure','evap']),
	          ('dpd',['DPD','deg C','PHA','DPD','dewpoint depression','monthly mean 2m dew point depression','ddep'])])

# This is needed by WriteNetCDF and writing to ascii
MonthName = ['January   ',
             'February  ',
	     'March     ',
	     'April     ',
	     'May       ',
	     'June      ',
	     'July      ',
	     'August    ',
	     'September ',
	     'October   ',
	     'November  ',
	     'December  ']

#******************************************************
# SUBROUTINES #
#******************************************************
# READDATA
def ReadData(FileName,typee,delimee):
    ''' Use numpy genfromtxt reading to read in all rows from a complex array '''
    ''' Need to specify format as it is complex '''
    ''' outputs an array of tuples that in turn need to be subscripted by their names defaults f0...f8 '''
    return np.genfromtxt(FileName, dtype=typee, delimiter=delimee, encoding='latin-1') # ReadData
#    return np.genfromtxt(FileName, dtype=typee, delimiter=delimee) # ReadData

#****************************************************
# MakeDaysSince
def MakeDaysSince(TheStYr,TheStMon,TheEdYr,TheEdMon):
    ''' Take counts of months since styr, stmn (assume 15th day of month) '''
    ''' Work out counts of days since styr,stmn, January - incl leap days '''
    ''' Also work out time boundaries 1st and last day of month '''
    ''' This can cope with incomplete years or individual months '''
    
    # set up arrays for month month bounds
    BoundsArray = np.empty((((TheEdYr-TheStYr)+1)*((TheEdMon-TheStMon)+1),2))
    
    # make a date object for each time point and subtract start date
    StartDate = datetime(TheStYr,TheStMon,1,0,0,0)	# January
    
    DaysArray = list(np.array([[(datetime(j,i,1,0,0,0)-StartDate).days + 15 for i in np.arange(1,13)] for j in np.arange(TheStYr,TheEdYr+1)]).flat)
    BoundsArray[:,0] = list(np.array([[(datetime(j,i,1,0,0,0)-StartDate).days for i in np.arange(1,13)] for j in np.arange(TheStYr,TheEdYr+1)]).flat)
    BoundsArray[:,1] = np.append(BoundsArray[1:,0]-1,(datetime(TheEdYr,TheEdMon,31,23,59,59)-StartDate).days)
            
    return DaysArray,BoundsArray

#**************************************************************************************
# WriteNetCDF
def WriteNetCDF(FileName,TheStYr,TheEdYr,TheClims,TheLats, TheLons, TheLatBounds, TheLonBounds, DataObject,DimObject,AttrObject,GlobAttrObject,TheMDI):
    ''' WRites NetCDF4 '''
    ''' Sort out the date/times to write out and time bounds '''
    ''' Convert variables using the obtained scale_factor and add_offset: stored_var=int((var-offset)/scale) '''
    ''' Write to file, set up given dimensions, looping through all potential variables and their attributes, and then the provided dictionary of global attributes '''

#    # Attributes and things common to all vars
#    add_offset = -100.0 # storedval=int((var-offset)/scale)
#    scale_factor = 0.01
    
    # Sort out date/times to write out
    TimPoints,TimBounds = MakeDaysSince(int(TheStYr),1,int(TheEdYr),12)
    nTims = len(TimPoints)

    # Create a new netCDF file - have tried zlib=True,least_significant_digit=3 (and 1) - no difference
    ncfw = nc4.Dataset(FileName,'w',format='NETCDF4_CLASSIC') # need to try NETCDF4 and also play with compression but test this first
    
    # Write out the global attributes
    if ('description' in GlobAttrObject):
        ncfw.description = GlobAttrObject['description']
	#print(GlobAttrObject['description'])
	
    if ('File_created' in GlobAttrObject):
        ncfw.File_created = GlobAttrObject['File_created']

    if ('Title' in GlobAttrObject):
        ncfw.Title = GlobAttrObject['Title']

    if ('Institution' in GlobAttrObject):
        ncfw.Institution = GlobAttrObject['Institution']

    if ('History' in GlobAttrObject):
        ncfw.History = GlobAttrObject['History']

    if ('Licence' in GlobAttrObject):
        ncfw.Licence = GlobAttrObject['Licence']

    if ('Project' in GlobAttrObject):
        ncfw.Project = GlobAttrObject['Project']

    if ('Processing_level' in GlobAttrObject):
        ncfw.Processing_level = GlobAttrObject['Processing_level']

    if ('Acknowledgement' in GlobAttrObject):
        ncfw.Acknowledgement = GlobAttrObject['Acknowledgement']

    if ('Source' in GlobAttrObject):
        ncfw.Source = GlobAttrObject['Source']

    if ('Comment' in GlobAttrObject):
        ncfw.Comment = GlobAttrObject['Comment']

    if ('References' in GlobAttrObject):
        ncfw.References = GlobAttrObject['References']

    if ('Creator_name' in GlobAttrObject):
        ncfw.Creator_name = GlobAttrObject['Creator_name']

    if ('Creator_email' in GlobAttrObject):
        ncfw.Creator_email = GlobAttrObject['Creator_email']

    if ('Version' in GlobAttrObject):
        ncfw.Version = GlobAttrObject['Version']

    if ('doi' in GlobAttrObject):
        ncfw.doi = GlobAttrObject['doi']

    if ('Conventions' in GlobAttrObject):
        ncfw.Conventions = GlobAttrObject['Conventions']

    if ('netcdf_type' in GlobAttrObject):
        ncfw.netcdf_type = GlobAttrObject['netcdf_type']
	
    # Loop through and set up the dimension names and quantities
    for vv in range(len(DimObject[0])):
        ncfw.createDimension(DimObject[0][vv],DimObject[1][vv])
	
    # Go through each dimension and set up the variable and attributes for that dimension if needed
    for vv in range(len(DimObject)-2): # ignore first two elements of the list but count all other dictionaries
#        print(DimObject[vv+2]['var_name'])
	
	# NOt 100% sure this works in a loop with overwriting
	# initiate variable with name, type and dimensions
        MyVar = ncfw.createVariable(DimObject[vv+2]['var_name'],DimObject[vv+2]['var_type'],DimObject[vv+2]['var_dims'])
        
	# Apply any other attributes
        if ('standard_name' in DimObject[vv+2]):
            MyVar.standard_name = DimObject[vv+2]['standard_name']
	    
        if ('long_name' in DimObject[vv+2]):
            MyVar.long_name = DimObject[vv+2]['long_name']
	    
        if ('units' in DimObject[vv+2]):
            MyVar.units = DimObject[vv+2]['units']
		   	 
        if ('axis' in DimObject[vv+2]):
            MyVar.axis = DimObject[vv+2]['axis']

        if ('calendar' in DimObject[vv+2]):
            MyVar.calendar = DimObject[vv+2]['calendar']

        if ('start_year' in DimObject[vv+2]):
            MyVar.start_year = DimObject[vv+2]['start_year']

        if ('end_year' in DimObject[vv+2]):
            MyVar.end_year = DimObject[vv+2]['end_year']

        if ('start_month' in DimObject[vv+2]):
            MyVar.start_month = DimObject[vv+2]['start_month']

        if ('end_month' in DimObject[vv+2]):
            MyVar.end_month = DimObject[vv+2]['end_month']

        if ('bounds' in DimObject[vv+2]):
            MyVar.bounds = DimObject[vv+2]['bounds']
	
	# Provide the data to the variable
        if (DimObject[vv+2]['var_name'] == 'time'):
            MyVar[:] = TimPoints

        if (DimObject[vv+2]['var_name'] == 'bounds_time'):
            MyVar[:,:] = TimBounds

        if (DimObject[vv+2]['var_name'] == 'month'):
#            pdb.set_trace()
#            MyVar[mm,:] = [nc4.stringtochar(np.array(MonthName[mm],dtype='S10')) for mm in np.arange(1,13)] 
            MyVar[:,:] = [[MonthName[mm][cc] for cc in range(10)] for mm in range(12)] 

        if (DimObject[vv+2]['var_name'] == 'latitude'):
            MyVar[:] = TheLats

        if (DimObject[vv+2]['var_name'] == 'bounds_lat'):
            MyVar[:,:] = TheLatBounds

        if (DimObject[vv+2]['var_name'] == 'longitude'):
            MyVar[:] = TheLons

        if (DimObject[vv+2]['var_name'] == 'bounds_lon'):
            MyVar[:,:] = TheLonBounds

    # Go through each variable and set up the variable attributes
    for vv in range(len(AttrObject)): # ignore first two elements of the list but count all other dictionaries

        print(AttrObject[vv]['var_name'])

        # initiate variable with name, type and dimensions
        if (AttrObject[vv]['var_type'] == 'f4'):
        
            MyVar = ncfw.createVariable(AttrObject[vv]['var_name'],AttrObject[vv]['var_type'],AttrObject[vv]['var_dims'],fill_value = TheMDI)
        
        elif (AttrObject[vv]['var_type'] == 'i4'):	

            MyVar = ncfw.createVariable(AttrObject[vv]['var_name'],AttrObject[vv]['var_type'],AttrObject[vv]['var_dims'],fill_value = 0)
	
	# Apply any other attributes
        if ('long_name' in AttrObject[vv]):
            MyVar.long_name = AttrObject[vv]['long_name']
	    
        if ('units' in AttrObject[vv]):
            MyVar.units = AttrObject[vv]['units']

#        MyVar.add_offset = add_offset
#        MyVar.scale_factor = scale_factor

        MyVar.reference_period = str(TheClims[0])+', '+str(TheClims[1])

	# Provide the data to the variable - depending on howmany dimensions there are
	## First change masked array to normal array filled with MDI
        if (len(AttrObject[vv]['var_dims']) == 1):
            MyVar[:] = DataObject[vv].filled()
	    
        if (len(AttrObject[vv]['var_dims']) == 2):
            MyVar[:,:] = DataObject[vv].filled()
	    
        if (len(AttrObject[vv]['var_dims']) == 3):
            MyVar[:,:,:] = DataObject[vv].filled()
	    	    
    ncfw.close()
   
    return # WriteNCCF

#
#*******************************************************
# MAIN
#******************************************************
def main(argv):

    # INPUT PARAMETERS AS STRINGS!!!!
    var = 'q'	    # 'q','rh','e','td','tw','t','dpd'
    typee = 'IDPHA' # 'PHA','IDPHA','PHADPD'

    try:
        opts, args = getopt.getopt(argv, "hi:",
	                           ["var=","typee="])
    except getopt.GetoptError:
        print('Usage (as strings) F13_GridHadISDHFLAT.py --var <q> --typee <IDPHA>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--var":
            try:
                var = arg
            except:
                sys.exit("Failed: var not a string")
        elif opt == "--typee":
            try:
                typee = arg
            except:
                sys.exit("Failed: typee not a string")
 
#    assert var != '' and typee != '', "Input values not specified."

    print(var,typee)
    
#*******************************************************
    # variable specific filepaths and directories
    # homogenised data file suffix
    DatSuffix = '_anoms'+CLMlab+'_homog.nc'
#    DatSuffix = '_anoms'+CLMlab+'_homogJAN2020.nc'

    # Set up files for read in and write out    
#    InList = INDIRLIST+'Posthomog'+typee+var+'_anoms'+CLMlab+'_goodsHadISDH.'+versiondots+'_JAN2020.txt'
    InList = INDIRLIST+'Posthomog'+typee+var+'_anoms'+CLMlab+'_goodsHadISDH.'+versiondots+'.txt'
    
    InHom = INDIRHOM+ParamDict[var][2]+'NETCDF/'+ParamDict[var][3]+'DIR/'	    #***
    
    OutFile = OUTDIRDAT+'HadISDH.land'+ParamDict[var][0]+'.'+versiondots+'_FLATgridHOM5by5_anoms'+CLMlab # will be .nc and .dat
 
    # Time related variables and arrays 
    clst =     MYclst - int(styear)
    cled =     MYcled - int(styear)
    nyrs =     (int(edyear) + 1) - int(styear)
    nmons =    nyrs * 12
    # Save netCDF file as days since 01-01-1973 DD-MM-YYYY

    # Space related variables and arrays
    StLat = -90. + (LatBox / 2.)
    StLon = -180. + (LonBox / 2.)
    nlats = int(180 / LatBox)
    nlons = int(360 / LonBox)
    nbox = nlats * nlons
    Lats = StLat + (np.arange(nlats) * 5.) # -90 to 90
    Lons = StLon + (np.arange(nlons) * 5.) # -180 to 80
    # Sort out LatBounds and LonBounds
    LatBounds = np.transpose(np.tile(Lats-(LatBox/2.),(2,1)))
    LatBounds[:,1] = LatBounds[:,1] + LatBox
    LonBounds = np.transpose(np.tile(Lons-(LonBox/2.),(2,1)))
    LonBounds[:,1] = LonBounds[:,1] + LonBox
    #print('Check Lat and Lon Bounds')
    #pdb.set_trace()

    # Masked Arrays for grids
    GBanoms = npm.masked_equal(np.tile(MDI,(nmons,nlats,nlons)),MDI)   # Anomalies NOT lons,lats,time as in IDL
    GBabs = npm.copy(GBanoms)                                          # Actuals   
    GBstaterr = npm.copy(GBanoms)                                      # Station Uncertainty   
    GBobserr = npm.copy(GBanoms)                                       # Measurement Uncertainty     
    GBclmerr = npm.copy(GBanoms)                                       # Climatology Uncertainty     
    GBadjerr = npm.copy(GBanoms)                                       # Adjustment Uncertainty     
    GBsamperr = npm.copy(GBanoms)                                      # Sampling Uncertainty     
    GBrbar = npm.masked_equal(np.tile(MDI,(nlats,nlons)),MDI)          # intersite correlation within gridbox
    GBsbarSQ = npm.copy(GBrbar)                                        # mean station variance within gridbox
    GBcomberr = npm.copy(GBanoms)                                      # Total Uncertainty
    GBstddevs = npm.copy(GBanoms)                                      # Standard Deviation of Montyhly Mean Anomalies contributing to Gridbox mean
    GBclims = npm.masked_equal(np.tile(MDI,(12,nlats,nlons)),MDI)      # Monthly mean climatology
    GBclimstds = npm.copy(GBclims)                                     # Monthly mean standard deviation of station climatologies within gridbox
    GBcounts = npm.masked_equal(np.tile(0,(nlats,nlons)),0)	       # GB average count - so could be a float but CEIL to nearest integer?
    GBstation_counts = npm.masked_equal(np.tile(0,(nmons,nlats,nlons)),0) # actual gridbox station counts over time

#*****************************************************************************************    
# Read in station list
#*****************************************************************************************

    # Open and read in station list 
    MyTypes         = ("|U11","float","float","float","|U1","|U2","|U1","|U29")
    MyDelimiters    = [11,9,10,7,1,2,1,29]
    RawData         = ReadData(InList,MyTypes,MyDelimiters)
    StationListID  = np.array(RawData['f0'])
    StationListLat  = np.array(RawData['f1'])
    StationListLon  = np.array(RawData['f2'])
    StationListElev = np.array(RawData['f3'])
    StationListCID  = np.array(RawData['f5'])
    StationListName = np.array(RawData['f7'])
    nstations       = len(StationListID)
   
#*******************************************************************************************
# Loop through each gridbox to create gridbox averages - find stations >= Southern and WEstern boundaries and < northern and eastern boundaries
#******************************************************************************************
# There are no stations at 90.0 North!!!
# Note that the RAW data may have a different pattern of abs and anoms 
# This is because RAW anoms are calculated from hourly clim anoms whereas HOM anoms are calculated from abs-clim
# I would like to homogenise the anomalies so that I can bring in this more robust way of calculating the anomalies and then abs = clim+anoms
    for lt, Lat in enumerate(Lats):

        LatLow = LatBounds[lt,0] # Gridbox Southern most point
        LatHigh = LatBounds[lt,1] # Gribbox Northern most point
	
        for ln, Lon in enumerate(Lons):

            LonLow = LonBounds[ln,0] # Gridbox Western most point
            LonHigh = LonBounds[ln,1] # Gribbox Eastern most point
            
	    # Locate all stations within this gridbox
            LocateStations = np.where((StationListLat >= LatLow) & (StationListLat < LatHigh) & (StationListLon >= LonLow) & (StationListLon < LonHigh))

            # Read in any stations within this gridbox
            if (len(LocateStations[0]) > 0):

                #print('Check station search works')
                #pdb.set_trace()	# NOT CONVINCED THIS IS WORKING
	    
                for s,ss in enumerate(LocateStations[0]):
		
                    # read in a masked array of the monthly station data
                    ncf = nc4.Dataset(InHom+StationListID[ss]+DatSuffix,'r')

                    # For the first station in the gridbox initialise arrays
                    if (s == 0): 

                        TMPanoms = npm.reshape(ncf.variables[var+'_anoms'][:],(1,nmons)) 
                        TMPabs = npm.reshape(ncf.variables[var+'_abs'][:],(1,nmons)) 
                        TMPstaterr = npm.reshape(ncf.variables[var+'_uncertainty'][:],(1,nmons))
                        TMPobserr = npm.reshape(ncf.variables[var+'_obserr'][:],(1,nmons))
                        TMPclmerr = npm.reshape(ncf.variables[var+'_climerr'][:],(1,nmons))
                        TMPadjerr = npm.reshape(ncf.variables[var+'_adjerr'][:],(1,nmons))
                        TMPclims = npm.reshape(ncf.variables[var+'_clims'][:],(1,12))

                    # For station 2+ append
                    else:

                        TMPanoms = npm.append(TMPanoms,npm.reshape(ncf.variables[var+'_anoms'][:],(1,nmons)),axis=0) 
                        TMPabs = npm.append(TMPabs,npm.reshape(ncf.variables[var+'_abs'][:],(1,nmons)),axis=0) 
                        TMPstaterr = npm.append(TMPstaterr,npm.reshape(ncf.variables[var+'_uncertainty'][:],(1,nmons)),axis=0) 
                        TMPobserr = npm.append(TMPobserr,npm.reshape(ncf.variables[var+'_obserr'][:],(1,nmons)),axis=0) 
                        TMPclmerr = npm.append(TMPclmerr,npm.reshape(ncf.variables[var+'_climerr'][:],(1,nmons)),axis=0) 
                        TMPadjerr = npm.append(TMPadjerr,npm.reshape(ncf.variables[var+'_adjerr'][:],(1,nmons)),axis=0) 
                        TMPclims = npm.append(TMPclims,npm.reshape(ncf.variables[var+'_clims'][:],(1,12)),axis=0) 
		    
                    ncf.close()
                
                #print('Check that appending of arrays has worked')
                #pdb.set_trace()  

                # Calculate means for the gridbox
                GBanoms[:,lt,ln] = npm.mean(TMPanoms,axis=0)		
                GBabs[:,lt,ln] = npm.mean(TMPabs,axis=0)
                GBclims[:,lt,ln] = npm.mean(TMPclims,axis=0)
                
		# Combine uncertainties assuming no correlation and that they are not identical
                # IDL version was this: q_staterr(lnn,ltt,vals) = SQRT(sterrsum(vals)/stcount)*(1./SQRT(stcount))
		# where - sterrsum(vals) was the sum of vals^2
		# This turns out to be the same as: npm.sqrt(npm.sum(npm.power(TMPstaterr,2.),axis=0)) / npm.count(TMPanoms,axis=0)
		# which follows: marine methods, John K's error_derivation.pdf which is his derivation based on: https://en.wikipedia.org/wiki/Propagation_of_uncertainty
		# SQRT(sum(vals^2)) / N
		# THis is sort of annoying as I was hoping to reduce the uncertainties but great because I didn't mess up in the first place.
		# These are masked arrays so this should work with missing data - all uncertainties are given actual missing data mask too
		# NOTE THAT THIS DIFFERS FROM IDL BECAUSE THE ERROR WAS DIMINISHED BY DIVIDING BY TOTAL NUMBER OF STATIONS OVER PERIOD 
		# RATHER THAN ACTUAL NUMBER OF STATIONS FOR THAT MONTH - SO NEW UNCS WILL BE LARGER WHHERE THERE ARE FEWER STATIONS.
                GBstaterr[:,lt,ln] = npm.sqrt(npm.sum(npm.power(TMPstaterr,2.),axis=0)) / npm.count(TMPanoms,axis=0)
                GBobserr[:,lt,ln] = npm.sqrt(npm.sum(npm.power(TMPobserr,2.),axis=0)) / npm.count(TMPobserr,axis=0)
                GBclmerr[:,lt,ln] = npm.sqrt(npm.sum(npm.power(TMPclmerr,2.),axis=0)) / npm.count(TMPclmerr,axis=0)
                GBadjerr[:,lt,ln] = npm.sqrt(npm.sum(npm.power(TMPadjerr,2.),axis=0)) / npm.count(TMPadjerr,axis=0)
                
		# Calculate the standard deviation of station anoms and clims contributing to the gridbox mean
                GBstddevs[:,lt,ln] = npm.std(TMPanoms,axis=0)
                GBclimstds[:,lt,ln] = npm.std(TMPclims,axis=0)
		# Add a check on GBclimstds where there is only one station in the gridbox because the standard deviation will be 0. - set it to 100.
                GBstddevs[np.where(GBstddevs[:,lt,ln] == 0.0),lt,ln] = 100.
                GBclimstds[np.where(GBclimstds[:,lt,ln] == 0.0),lt,ln] = 100.
		
		# Get station counts average and actual (INTEGER)
                GBstation_counts[:,lt,ln] = npm.count(TMPanoms,axis=0)	
		# Forcing this to be a ceiling-ed integer as a mean will likely leave a float.
                GBcounts[lt,ln] = npm.ceil(npm.mean(GBstation_counts[:,lt,ln]))
  
                #print(len(LocateStations[0]),Lat, Lon,'Check mean/std/quad/count/100. of arrays has worked') # They have - for 1, multiple, masked and all present
                #pdb.set_trace()  

#***********************************************************************************
# Calculate the sampling uncertainty for the gridboxes
#************************************************************************************
    # This code isn't set up with masked arrays because the marine data doesn't use masked arrays yet...so need to convert to normal with MDI then convert back
    # When I tidy up marine code I will set up with masked arrays!!!
    IsMarine = False
    GBsamperr, GBrbar, GBsbarSQ = gsu.calc_sampling_unc(npm.filled(GBanoms,MDI), Lats, Lons, npm.filled(GBcounts,0), npm.filled(GBstation_counts,0), MDI, IsMarine, int(styear), int(edyear), MYclst, MYcled)

    # The output array should be normal so I need to convert to masked    
    GBsamperr = npm.masked_equal(GBsamperr,MDI)  
    GBrbar = npm.masked_equal(GBrbar,MDI)         
    GBsbarSQ = npm.masked_equal(GBsbarSQ,MDI)   
    
    # Multiply the uncertainty by 2 to get 2 sigma
    GBsamperr = GBsamperr * 2.       # masked array so will ignore MDI                         

    #print('Check the sampling uncertainty and array masking') # looks identical to old version to me.
    #pdb.set_trace()

#************************************************************************************
# Calculate full gridbox uncertainty
#*************************************************************************************
    GBcomberr = npm.sqrt(npm.power(GBsamperr,2.) + npm.power(GBstaterr,2.))
    # Note that there was an error here in 2019 where I had stupidly /2. but then removed the *2 so combined uncertainties were too small.

# What about where we've given random large values???
#*************************************************************************************    
# Write out to netCDF
#***********************************************************************************
    # NOTE THAT ITS JUST ONE VARIABLE!!!
    # List data together to pass to NetCDF writer
    DataList = [GBanoms, GBabs, GBstddevs, GBclims, GBclimstds, GBadjerr, GBclmerr, GBobserr, GBstaterr, GBsamperr, GBrbar, GBsbarSQ, GBcomberr, GBcounts, GBstation_counts]

    # List all of the dimensions
    DimList = [['time','month','characters','latitude','longitude','bound_pairs'],
	           [nmons,12,10,36,72,2],
    	           dict([('var_type','f4'),
    		         ('var_name','time'),
    		         ('var_dims',('time',)),
    		         ('standard_name','time'),
    		         ('long_name','time'),
    		         ('units','days since 1973-1-1 00:00:00'),
    		         ('axis','T'),
    		         ('calendar','gregorian'),
    		         ('start_year',int(styear)),
    		         ('end_year',int(edyear)),
    		         ('start_month',1),
    		         ('end_month',12),
    		         ('bounds','bounds_time')]),
    	           dict([('var_type','i4'),
    		         ('var_name','bounds_time'),
    		         ('var_dims',('time','bound_pairs',)), 
    		         ('standard_name','time'),
    		         ('long_name','time period boundaries')]),
    	           dict([('var_type','S1'),
    		         ('var_name','month'),
    		         ('var_dims',('month','characters',)), 
    		         ('long_name','month of year')]),
                   dict([('var_type','f4'),
    		         ('var_name','latitude'),
    		         ('var_dims',('latitude',)), 
    		         ('standard_name','latitude'),
    		         ('long_name','gridbox centre latitude'),
    		         ('units','degrees_north'),
    		         ('axis','Y'),
    		         ('point_spacing','even'),
    		         ('bounds','bounds_lat')]),
    	           dict([('var_type','f4'),
    		         ('var_name','bounds_lat'),
    		         ('var_dims',('latitude','bound_pairs',)), 
    		         ('standard_name','latitude'),
    		         ('long_name','latitude gridbox boundaries')]),
    	           dict([('var_type','f4'),
    		         ('var_name','longitude'),
    		         ('var_dims',('longitude',)), 
    		         ('standard_name','longitude'),
    		         ('long_name','gridbox centre longitude'),
    		         ('units','degrees_east'),
    		         ('axis','X'),
    		         ('point_spacing','even'),
    		         ('bounds','bounds_lon')]),
    	           dict([('var_type','f4'),
    		         ('var_name','bounds_lon'),
    		         ('var_dims',('longitude','bound_pairs',)), 
    		         ('standard_name','longitude'),
    		         ('long_name','longitude gridbox boundaries')])]

    # Attribute list for variables
    AttrList = [dict([('var_type','f4'),
	                  ('var_name',var+'_anoms'),
		          ('var_dims',('time','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' anomaly'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_abs'),
		          ('var_dims',('time','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_std'),
		          ('var_dims',('time','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' standard deviation of station monthly mean anomalies'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_clims'),
		          ('var_dims',('month','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' climatology '+str(MYclst)+'-'+str(MYcled)),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_clim_std'),
		          ('var_dims',('month','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' climatological standard deviation '+str(MYclst)+'-'+str(MYcled)),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_adjerr'),
		          ('var_dims',('time','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' adjustment uncertainty estimate including missed adjustment (2sigma)'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_climerr'),
		          ('var_dims',('time','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' climatology uncertainty estimate (2sigma)'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_obserr'),
		          ('var_dims',('time','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' measurement uncertainty estimate (2sigma)'),
	                  ('units',ParamDict[var][1])]),
                    dict([('var_type','f4'),
	                  ('var_name',var+'_stationerr'),
		          ('var_dims',('time','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' combined station uncertainty estimate (2sigma)'),
	                  ('units',ParamDict[var][1])]),
	            dict([('var_type','f4'),
	                  ('var_name',var+'_samplingerr'),
		          ('var_dims',('time','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' gridbox sampling uncertainty estimate (2sigma)'),
	                  ('units',ParamDict[var][1])]),
	            dict([('var_type','f4'),
	                  ('var_name',var+'_rbar'),
		          ('var_dims',('latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' gridbox intersite correlation estimate following Jones et al 1997 (rbar)'),
	                  ('units','1')]),
		    dict([('var_type','f4'),
	                  ('var_name',var+'_sbarSQ'),
		          ('var_dims',('latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+'mean variance over all observations in gridbox following Jones et al 1997 (sbar2)'),
	                  ('units',ParamDict[var][1])]),
		    dict([('var_type','f4'),
	                  ('var_name',var+'_combinederr'),
		          ('var_dims',('time','latitude','longitude',)), 
	                  ('long_name',ParamDict[var][5]+' combined gridbox uncertainty estimate (2sigma)'),
	                  ('units',ParamDict[var][1])]),
		    dict([('var_type','i4'),
	                  ('var_name','mean_n_stations'),
		          ('var_dims',('latitude','longitude',)), 
	                  ('long_name','Monthly mean number of stations within gridbox averaged over full period'),
	                  ('units','1')]),
		    dict([('var_type','i4'),
	                  ('var_name','actual_n_stations'),
		          ('var_dims',('time','latitude','longitude',)), 
	                  ('long_name','Actual number of stations within gridbox month'),
	                  ('units','1')])]  

    # Global attribute list
    GlobAttrObjectList = dict([['File_created',datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')], # Is there a call for time stamping?
			       ['Description','HadISDH monthly mean land surface homogenised data'],
			       ['Title','HadISDH monthly mean land surface climate monitoring product'], 
			       ['Institution', AttribDict['Institution']],
			       ['History', AttribDict['History']], 
			       ['Licence', AttribDict['OGLicence']],
			       ['Project', AttribDict['Project']],
			       ['Processing_level', AttribDict['Processing_level']],
			       ['Acknowledgement', AttribDict['Acknowledgement']],
			       ['Source', 'HadISD '+hadisdversiondots+' '+AttribDict['Source']],
			       ['Comment',''],
			       ['References', AttribDict['References']],
			       ['Creator_name', AttribDict['Creator_name']],
			       ['Creator_email', AttribDict['Creator_email']],
			       ['Version', versiondots],
			       ['doi',''], # This needs to be filled in
			       ['Conventions', AttribDict['Conventions']],
			       ['netCDF_type', AttribDict['netCDF_type']]]) 

    # Write out monthly data to netCDF
    WriteNetCDF(OutFile+'.nc',styear,edyear,[MYclst,MYcled],Lats, Lons, LatBounds, LonBounds, DataList,DimList,AttrList,GlobAttrObjectList,MDI)
    #print('WRITEN TO NCDF: Check that this hasnt left the masked arrays filled with MDIs')
    #pdb.set_trace()

#**************************************************************************
# Write out to ASCII
#**************************************************************************
    # First write out stats to OUTPUTLOG
    filee = open(OUTPUTLOG,'a+')

    filee.write('%s%s%s%s%i\n' % (var, '_', typee, '_MEAN_N_STATIONS_MIN=', np.min(GBcounts)))
    filee.write('%s%s%s%s%i\n' % (var, '_', typee, '_MEAN_N_STATIONS_MAX=', np.max(GBcounts)))

    filee.write('%s%s%s%s%i\n' % (var, '_', typee, '_ACTUAL_N_STATIONS_MIN=', np.min(GBstation_counts)))
    filee.write('%s%s%s%s%i\n' % (var, '_', typee, '_ACTUAL_N_STATIONS_MAX=', np.max(GBstation_counts)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_ANOMS_MIN=', np.min(GBanoms)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_ANOMS_MAX=', np.max(GBanoms)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_ACTUALS_MIN=', np.min(GBabs)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_ACTUALS_MAX=', np.max(GBabs)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_STDEVS_MIN=', np.min(GBstddevs)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_STDEVS_MAX=', np.max(GBstddevs[np.where(GBstddevs < 100.)])))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_CLIMS_MIN=', np.min(GBclims)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_CLIMS_MAX=', np.max(GBclims)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_CLIMSTD_MIN=', np.min(GBclimstds)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_CLIMSTD_MAX=', np.max(GBclimstds[np.where(GBclimstds < 100.)])))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_STATION_UNCERTAINTY=', np.min(GBstaterr)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_STATION_UNCERTAINTY=', np.max(GBstaterr)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_ADJUSTMENT_UNCERTAINTY=', np.min(GBadjerr)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_ADJUSTMENT_UNCERTAINTY=', np.max(GBadjerr)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_CLIMATOLOGY_UNCERTAINTY=', np.min(GBclmerr)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_CLIMATOLOGY_UNCERTAINTY=', np.max(GBclmerr)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_MEASUREMENT_UNCERTAINTY=', np.min(GBobserr)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_MEASUREMENT_UNCERTAINTY=', np.max(GBobserr)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_SAMPLING_UNCERTAINTY=', np.min(GBsamperr)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_SAMPLING_UNCERTAINTY=', np.max(GBsamperr)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_CROSS_CORRELATION=', np.min(GBrbar)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_CROSS_CORRELATION=', np.max(GBrbar)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_GRIDBOX_VARIANCE=', np.min(GBsbarSQ)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_GRIDBOX_VARIANCE=', np.max(GBsbarSQ)))

    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_TOTAL_UNCERTAINTY=', np.min(GBcomberr)))
    filee.write('%s%s%s%s%f\n' % (var, '_', typee, '_TOTAL_UNCERTAINTY=', np.max(GBcomberr)))

    filee.close()
 
# Now write out the ascii anoms, actuals and combined uncertainties    
    GBanoms = GBanoms.filled(-9999.99)
    GBabs = GBabs.filled(-9999.99)
    GBcomberr = GBcomberr.filled(-9999.99)

    fileeAN = open(OutFile+'_anomalies.dat','a+') # might need to be 'ab'
    fileeAB = open(OutFile+'_actuals.dat','a+')
    fileeUN = open(OutFile+'_2sig_uncertainty.dat','a+')
 
    year = int(styear)
    MCount = 0
    for mm in range(nmons):
   
        # Write the YYYY Month header for each month
        fileeAN.write('%i %s\n' % (year, MonthName[MCount]))
        fileeAB.write('%i %s\n' % (year, MonthName[MCount]))
        fileeUN.write('%i %s\n' % (year, MonthName[MCount]))

        # Loop through all lats North to South (arrays currently listed south to north!!!) and print all lons -180 to 180
        for ll in range(nlats):
       
            np.savetxt(fileeAN, np.reshape(np.round(GBanoms[mm,ll,:],2),(1,72)), fmt='% 9.2f', delimiter='') # may need newline='\n' 
            np.savetxt(fileeAB, np.reshape(np.round(GBabs[mm,ll,:],2),(1,72)), fmt='% 9.2f', delimiter='') # may need newline='\n' 
            np.savetxt(fileeUN, np.reshape(np.round(GBcomberr[mm,ll,:],2),(1,72)), fmt='% 9.2f', delimiter='') # may need newline='\n' 
 
        #Increment month count and test for year increment
        MCount += 1     
        if (MCount == 12):
       
            MCount = 0
            year += 1

    np.savetxt(fileeAN, np.reshape(np.round(Lats,3),(1,36)), fmt='% 9.2f', delimiter='') # may need newline='\n' 
    np.savetxt(fileeAB, np.reshape(np.round(Lats,3),(1,36)), fmt='% 9.2f', delimiter='') # may need newline='\n' 
    np.savetxt(fileeUN, np.reshape(np.round(Lats,3),(1,36)), fmt='% 9.2f', delimiter='') # may need newline='\n' 

    np.savetxt(fileeAN, np.reshape(np.round(Lons,3),(1,72)), fmt='% 9.2f', delimiter='') # may need newline='\n' 
    np.savetxt(fileeAB, np.reshape(np.round(Lons,3),(1,72)), fmt='% 9.2f', delimiter='') # may need newline='\n' 
    np.savetxt(fileeUN, np.reshape(np.round(Lons,3),(1,72)), fmt='% 9.2f', delimiter='') # may need newline='\n' 
          
    fileeAN.close() 
    fileeAB.close() 
    fileeUN.close() 
 

    print('And we are done!')
    
if __name__ == '__main__':
    
    main(sys.argv[1:])
