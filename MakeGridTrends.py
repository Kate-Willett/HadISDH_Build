# PYTHON 3
# 
# Author: Kate Willett
# Created: 1 February 2013
# Last update: 15 January 2020
# Location: /data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/HADISDH_BUILD/	
# GitHub: https://github.com/Kate-Willett/HadISDH_Build					
# -----------------------
# CODE PURPOSE AND OUTPUT
# -----------------------
# Reads in a gridded dataset and outputs a decadal trend for each gridbox over the desired period.
# This can output with median pairwise or Ordinary least squares
# 
# <references to related published material, e.g. that describes data set>
# 
# -----------------------
# LIST OF MODULES
# -----------------------
# Inbuilt: (may not all be required actually)
# import numpy as np
# import matplotlib.pyplot as plt
# import sys, os, getopt
# import struct
# import pdb
# #import netCDF4 as nc4
# from netCDF4 import Dataset
#
# Kate's Functions - had to be copied into directory
# from LinearTrends import OLS_AR1Corr
# from LinearTrends import MedianPairwise
# from ReadNetCDF import GetGrid4
## 
# -----------------------
# DATA
# -----------------------
# Input gridded netCDF file of monthly mean values
# /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/HadISDH.land<Var>.'+version+'_FLATgrid<homogtype>PHA5by5_anoms7605_JAN2017
# 
# -----------------------
# HOW TO RUN THE CODE
# -----------------------
# Check you've got the desired year, clims, working files, variable, homogtype etc
# > module load scitools/default-current
# > python MakeGridTrends --var <var> --typee <type> --year1 <yyyy> --year2 <yyyy>
#
## Which variable?
# var = 'dpd'	#'dpd','td','t','tw','e','q','rh'
#
## Which homog type?
# typee = 'LAND', 'RAW','OTHER', 'BLEND', 'BLENDSHIP', 'MARINE','MARINESHIP', 'ERA5','EAR5MASK','ERA5LAND','ERA5MARINE','ERA5LANDMASK','ERA5MARINEMASK'
#
# year1 and year2 are start and end year of trends

# You can also run this from spice
# edit submit_spice_MakeGridTrend.bash as desired
# FIRST SET UP THE PYTHON ENVIRONMENT WHERE YOU ARE RUNNING FROM!!!
# module load scitools/default-current
# ./submit_spice_MakeGridTrend.bash
#
# See 'EDITABLES' for setting longer life things like version, dataset years etc.
# 
# -----------------------
# OUTPUT
# -----------------------
# Output netCDF file of gridbox decadal trends
# /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/HadISDH.land<Var>.'+version+'_FLATgrid<homogtype>PHA5by5_JAN2014_anoms7605_MPtrends_19732016.nc
# 
# -----------------------
# VERSION/RELEASE NOTES
# -----------------------
#
# Version 4 (5 November 2020)
# ---------
#  
# Enhancements
# Now works with ERA5 and maybe ERA-Interim
#
# Changes
# No longer has nowmon, thenmon, nowyear, thenyear in filename read ins so won't work on pre2020 HadISDH.
# 
# Bug fixes
#
# Version 3 (15 January 2020)
# ---------
#  
# Enhancements
# Can use OLS with AR(1) correction following Santer et al., 2008 as well as median pairwise
#
# Changes
# Now python 3 rather than IDL
#
# Version 3 (15 February 2018)
# ---------
#  
# Enhancements
# Now variable and homogtype are called from the command line - param, homogtype
# param = 'dpd'	#'dpd','td','t','tw','e','q','rh'
# homogtype = 'PHA'	#'PHA','IDPHA','PHADPD', 'RAW','OTHER', 'BLEND', 'BLENDSHIP','MARINE', 'MARINESHIP'
# 
# Version 2 (1 February 2017)
# ---------
#  
# Enhancements
# General tidy up of code and EDITABLES
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
# Python 3 version compared to IDL for median pairwise takes over an hour (much longer than IDL) but produces very similar results
# OLS is very fast to run but results in far fewer gridboxes than for median pairwise. This doesn't appear to be due to DoF being too low or AR(1) being negative
# Need to find out why by comparing at gridbox level.
#
#******************************************************
# Global variables and imports
# Inbuilt: (may not all be required actually)
import numpy as np
#import matplotlib.pyplot as plt
import sys, os, getopt
import struct
import pdb
#import netCDF4 as nc4
from netCDF4 import Dataset

# Kate's Functions
from LinearTrends import OLS_AR1Corr
from LinearTrends import MedianPairwise
from ReadNetCDF import GetGrid4

#*******************************************************
# SUBROUTINES
#*********************************************************
# GetTrends
def GetTrends(TheOrigData,TheStyr,TheEdyr,TheSttrd,TheEdtrd,TheTrendType,TheConfIntP,TheMDI,TheMissingDataThresh):
    ''' Code to open and read netCDF file of data, compute decadal trends for each gridbox and then save as a 2D netCDF '''
    ''' Confidence intervals around the trend are also computed and saved '''

    # Set up MDI filled arrays for output
    TheTrendGrids = np.empty_like(TheOrigData[0,:,:])
    TheTrendGrids.fill(TheMDI)

    TheLowBoundGrids = np.empty_like(TheOrigData[0,:,:])
    TheLowBoundGrids.fill(TheMDI)

    TheUpperBoundGrids = np.empty_like(TheOrigData[0,:,:])
    TheUpperBoundGrids.fill(TheMDI)

    TheSE1sigGrids = np.empty_like(TheOrigData[0,:,:])
    TheSE1sigGrids.fill(TheMDI)
    
    # Check to see whether we need to shorten the timeseres
    # We're only working in complete years here
    st = 0
    ed = len(TheOrigData[:,0,0])
    
    # If one is different then we need to reset teh data pointers
    if (TheStyr != TheSttrd):
    
        st = (TheSttrd - TheStyr) * 12 # should be 0 if they are the same, 12 if one year different 24 if 2 etc	    

    # If one is different then we need to reset teh data pointers
    if (TheEdyr != TheEdtrd):
    
        ed = 12 + ((TheEdtrd - TheStyr) * 12) # should be 120 if they are 10 years apart (1973 to 1982)	 
	# Ensures +1 on the pointer for array slicing   

    # Loop through each gridbox
    for lt in range(len(TheOrigData[0,:,0])):
    
        for ln in range(len(TheOrigData[0,0,:])):
	
	    # Only carrying on if there is some data - equal or more than the missing datat thresshold
            gots = np.where(TheOrigData[st:ed,lt,ln] > TheMDI)
            if (np.float(len(gots[0])) / len(TheOrigData[st:ed,lt,ln]) >= TheMissingDataThresh):
	    
                
                # Calculate trend adn confidence intervals
		# Which trend tupe?
                if (TheTrendType == 'OLS'):
                
                    Slopes = OLS_AR1Corr(TheOrigData[st:ed,lt,ln],TheMDI,TheConfIntP)
# Code for testing where OLS and MP give different answers
#                    Slopes2 = [0,0,0]
#                    Slopes2 = MedianPairwise(TheOrigData[st:ed,lt,ln],TheMDI,Slopes2)
#		    
#                    if ((Slopes1[0] == TheMDI) & (Slopes2[0] > TheMDI)):
#		    
#                        print('Found a mismatch!')
#                        pdb.set_trace()
			
                else:
		    
                    Slopes = [0,0,0]
                    Slopes = MedianPairwise(TheOrigData[st:ed,lt,ln],TheMDI,Slopes)
	    
	        # Now check for irregularity - is there a non-MDI trend value, sig value and conf int values?
	        # If there is something wrong then the trend isn't computed: 
	        # OLS error if < 3 datapoints, effective DoF < 3, AR < 0
                if (Slopes[0] > TheMDI):
	    
                    TheTrendGrids[lt,ln] = Slopes[0]*120	    
                    TheLowBoundGrids[lt,ln] = Slopes[1]*120	    
                    TheUpperBoundGrids[lt,ln] = Slopes[2]*120	    

                    if (TheTrendType == 'OLS'):
                        
                        TheSE1sigGrids[lt,ln] = Slopes[3]*120	 
			
                    else:   

                        TheSE1sigGrids[lt,ln] = ((Slopes[2]*120) - (Slopes[1]*120)) / 2.	 
    
                print(TheTrendType,' slope: ',TheTrendGrids[lt,ln],' for Lt, Ln ',lt,ln)            


    return TheTrendGrids, TheLowBoundGrids, TheUpperBoundGrids, TheSE1sigGrids
    
#*******************************************************
# WriteNetCDF
def WriteNetCDF(Filename,TheTrendGrids,TheLowBoundGrids,TheUpperBoundGrids,TheSE1SigGrids,TheMDI,TheComment,
		TheVar,TheVarBig,TheStandardName,TheLongName,TheUnit,TheLats,TheLons):
    '''
    This function writes out a NetCDF 4 file
    
    INPUTS:
    Filename - string file name
    TheTrendGrids[:,:] - 2D array of decadal average trends
    TheLowBoundGrids[:,:] - 2D array of decadal average trends
    TheUpperBoundGrids[:,:] - 2D array of decadal average trends
    TheSE1SigGrids[:,:] - 2D array of decadal average trends
    TheMDI - the missind data value
    TheComment - text describing the trend method
    TheVar - string short name of var q
    TheVarBig - string short name of var in capitals RH
    TheStandardName - string standard name of variable
    TheLongName - strong long name of variable
    TheUnit - string unit of variable
    TheLats[:] - vector of latitudes from -90 to 90
    TheLons[:] - vector of longitudes from -180 to 180
    OUTPUTS:
    None
    
    '''
    
    # No need to convert float data using given scale_factor and add_offset to integers - done within writing program (packV = (V-offset)/scale
    # Not sure what this does to float precision though...

    # Create a new netCDF file - have tried zlib=True,least_significant_digit=3 (and 1) - no difference
    ncfw = Dataset(Filename,'w',format='NETCDF4_CLASSIC') # need to try NETCDF4 and also play with compression but test this first

    # Set up the dimension names and quantities
    ncfw.createDimension('latitude',len(TheLats))
    ncfw.createDimension('longitude',len(TheLons))
    
    # Go through each dimension and set up the variable and attributes for that dimension if needed
    MyVarLt = ncfw.createVariable('latitude','f4',('latitude',))
    MyVarLt.standard_name = 'latitude'
    MyVarLt.long_name = 'latitude'
    MyVarLt.units = 'degrees_north'
    MyVarLt.valid_min = np.min(TheLats)
    MyVarLt.valid_max = np.max(TheLats)
    MyVarLt.point_spacing = 'even'
    MyVarLt.axis = 'X'
    MyVarLt[:] = TheLats

    MyVarLn = ncfw.createVariable('longitude','f4',('longitude',))
    MyVarLn.standard_name = 'longitude'
    MyVarLn.long_name = 'longitude'
    MyVarLn.units = 'degrees east'
    MyVarLn.valid_min = np.min(TheLons)
    MyVarLn.valid_max = np.max(TheLons)
    MyVarLn.point_spacing = 'even'
    MyVarLn.axis = 'X'
    MyVarLn[:] = TheLons

    # Go through each variable and set up the variable attributes
    # I've added zlib=True so that the file is in compressed form
    # I've added least_significant_digit=4 because we do not need to store information beyone 4 significant figures.
    MyVar = ncfw.createVariable(TheVarBig+'_trend','f4',('latitude','longitude',),fill_value = TheMDI,zlib=True,least_significant_digit=4)
    MyVar.standard_name = TheStandardName
    MyVar.long_name = TheLongName
    MyVar.units = TheUnit
    MyVar.comment = TheComment
    MyVar.valid_min = np.min(TheTrendGrids)
    MyVar.valid_max = np.max(TheTrendGrids)
#    MyVar.missing_value = mdi
    # Provide the data to the variable - depending on howmany dimensions there are
    MyVar[:] = TheTrendGrids[:,:]  	

    MyVarL = ncfw.createVariable(TheVarBig+'_lowCI','f4',('latitude','longitude',),fill_value = TheMDI,zlib=True,least_significant_digit=4)
    MyVarL.standard_name = TheStandardName
    MyVarL.long_name = 'Lower Confidence Interval '+TheLongName
    MyVarL.units = TheUnit
    MyVarL.comment = TheComment
    MyVarL.valid_min = np.min(TheLowBoundGrids)
    MyVarL.valid_max = np.max(TheLowBoundGrids)
#    MyVarL.missing_value = mdi
    # Provide the data to the variable - depending on howmany dimensions there are
    MyVarL[:] = TheLowBoundGrids[:,:]  	

    MyVarU = ncfw.createVariable(TheVarBig+'_upperCI','f4',('latitude','longitude',),fill_value = TheMDI,zlib=True,least_significant_digit=4)
    MyVarU.standard_name = TheStandardName
    MyVarU.long_name = 'Upper Confidence Interval '+TheLongName
    MyVarU.units = TheUnit
    MyVarU.comment = TheComment
    MyVarU.valid_min = np.min(TheUpperBoundGrids)
    MyVarU.valid_max = np.max(TheUpperBoundGrids)
#    MyVarU.missing_value = mdi
    # Provide the data to the variable - depending on howmany dimensions there are
    MyVarU[:] = TheUpperBoundGrids[:,:]  	

    MyVarSE = ncfw.createVariable(TheVarBig+'_1sigSE','f4',('latitude','longitude',),fill_value = TheMDI,zlib=True,least_significant_digit=4)
    MyVarSE.standard_name = TheStandardName
    MyVarSE.long_name = '1 sigma standard error '+TheLongName
    MyVarSE.units = TheUnit
    MyVarSE.comment = TheComment
    MyVarSE.valid_min = np.min(TheSE1SigGrids)
    MyVarSE.valid_max = np.max(TheSE1SigGrids)
#    MyVarSE.missing_value = mdi
    # Provide the data to the variable - depending on howmany dimensions there are
    MyVarSE[:] = TheSE1SigGrids[:,:]  	

    ncfw.close()

    return
    
#*******************************************************
# MAIN
#********************************************************
def main(argv):
    # INPUT PARAMETERS AS STRINGS!!!!
    var = 'q'	    # 'q','rh','e','td','tw','t','dpd'
    typee = 'LAND' # 'LAND','RAW','OTHER', 'BLEND', 'BLENDSHIP', 'MARINE', 'MARINESHIP' # domain does not need to be set correctly!!!
    # can also be 'ERA5' 'ERA5LAND','ERA5MARINE' 'ERA5MARINEMASK' ERA5LANDMASK'
    year1 = '1973' # Start year of trend
    year2 = '2018' # End year of trend
    
    try:
        opts, args = getopt.getopt(argv, "hi:",
	                           ["var=","typee=","year1=","year2="])
    except getopt.GetoptError:
        print('Usage (as strings) MakeGridTrends.py --var <q> --typee <IDPHA> --year1 <1973> --year2 <2018>')
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
        elif opt == "--year1":
            try:
                year1 = arg
            except:
                sys.exit("Failed: year1 not an integer")
        elif opt == "--year2":
            try:
                year2 = arg
            except:
                sys.exit("Failed: year2 not an integer")

    assert year1 != -999 and year2 != -999, "Year not specified."

    print(var,typee,year1, year2)
#    pdb.set_trace()

    #****************** LONGER LIFE EDITABLES****************
    # TWEAK ME!!!!
    # Which trend type and confidence interval?
    TrendType = 'OLS' # this is in fact with AR(1) correction as in Santer et al., 2008
    #TrendType = 'MP'  # this is median pairwise as in Sen 1968

    ConfIntP = 0.9 # confidence interval p value	
    MissingDataThresh = 0.7 # Proportion of data values that must be present across the trend period

    # Which start/end year of the complete dataset?
    styr = 1973 # 1973
    edyr = 2019

    # Which climatology period to work with?
    climST = str(1981)	    #1976 or 1981
    climED = str(2010)	    #2005 or 2010
    climBIT = 'anoms'+climST[2:4]+climED[2:4]

    # Which working file dates?
    nowmon   = 'JAN'
    nowyear  = '2020'
    thenmon  = 'JAN'
    thenyear = '2020'

    # What domain?
    if (typee == 'MARINE') | (typee == 'MARINESHIP') | (typee == 'ERA5MARINE') | (typee == 'ERA5MARINEMASK'):
        domain = 'marine'
        version = '1.0.0.2019f'
    elif (typee == 'BLEND') | (typee == 'BLENDSHIP') | (typee == 'ERA5') | (typee == 'ERA5MASK'):
        domain = 'blend'
        version = '1.0.0.2019f'
    else:
        domain = 'land'
        version = '4.2.0.2019f'

    # Latitude and Longitude gridbox width and variable names
    latlg = 5.
    lonlg = 5.
    #latlg = 1.
    #lonlg = 1.
    LatInfo = ['latitude'] 
    LonInfo = ['longitude'] 

    # Time and dimension variables
    nyrs =     (edyr+1)-styr
    nmons =    nyrs*12
    stlt =     -90+(latlg/2.)
    stln =     -180+(lonlg/2.)
    nlats =    int(180/latlg)
    nlons =    int(360/lonlg)

    lats = (np.arange(nlats)*latlg) + stlt
    lons = (np.arange(nlons)*lonlg) + stln

    MDI = -1e30 # missing data indicator

    WORKINGDIR = '/data/users/hadkw/WORKING_HADISDH/UPDATE20'+str(edyr)[2:4]

    INDIR  = WORKINGDIR+'/STATISTICS/GRIDS/'
    OUTDIR = WORKINGDIR+'/STATISTICS/TRENDS/'
    
    # If we're working with ERA5 then set INDIR to OTHERDATA
    if (typee.find('ERA5') >= 0):

        INDIR  = WORKINGDIR+'/OTHERDATA/'
        INDIRH  = WORKINGDIR+'/STATISTICS/GRIDS/'

    # END OF EDITABLES**********************************************************

    # Dictionaries for filename and other things
    ParamDict = dict([('q',['q','q2m','g/kg']),
	      ('rh',['RH','rh2m','%rh']),
	      ('t',['T','t2m','deg C']),
	      ('td',['Td','td2m','deg C']),
	      ('tw',['Tw','tw2m','deg C']),
	      ('e',['e','e2m','hPa']),
	      ('dpd',['DPD','dpd2m','deg C']),
	      ('evap',['q','evap','cm w.e.'])])

    # Dictionary for looking up variable standard (not actually always standard!!!) names for netCDF output of variables
    NameDict = dict([('q',['specific_humidity',' decadal trend in specific humidity anomaly ('+climST+' to '+climED+' base period)']),
	 ('rh',['relative_humidity',' decadal trend in relative humidity anomaly ('+climST+' to '+climED+' base period)']),
	 ('e',['vapour_pressure',' decadal trend in vapour pressure anomaly ('+climST+' to '+climED+' base period)']),
	 ('tw',['wetbulb_temperature',' decadal trend in wetbulb temperature anomaly ('+climST+' to '+climED+' base period)']),
	 ('t',['drybulb_temperature',' decadal trend in dry bulb temperature anomaly ('+climST+' to '+climED+' base period)']),
	 ('td',['dewpoint_temperature',' decadal trend in dew point temperature anomaly ('+climST+' to '+climED+' base period)']),
	 ('dpd',['dewpoint depression',' decadal trend in dew point depression anomaly ('+climST+' to '+climED+' base period)']),
	 ('evap',['evaporation',' decadal trend in evaporation anomaly ('+climST+' to '+climED+' base period)'])])

    ## Dictionary for looking up variable long names for netCDF output of variables
    #LongNameDict = dict([('q','specific_humidity'),
#	 ('rh','2m relative humidity '),
#	('e','2m vapour_pressure '),
#	 ('tw','2m wetbulb_temperature '),
#	 ('t','2m drybulb_temperature '),
#	 ('td','2m dewpoint_temperature '),
#	 ('dpd','2m dewpoint depression '),
#	 ('evap','evaporation from 1by1 ')])

    # Set up the trend years
    sttrd = int(year1)
    edtrd = int(year2)

    if domain == 'land':
        DatTyp = 'IDPHA'
        if (var == 'dpd'):
            DatTyp = 'PHA'
        if (var == 'td'):
            DatTyp = 'PHADPD'
        fileblurb = 'FLATgrid'+DatTyp+'5by5'
    elif domain == 'marine':
        if (typee == 'MARINE'):
            fileblurb = 'BClocal5by5both'
        elif (typee == 'MARINESHIP') | (typee == 'ERA5MARINEMASK') | (typee == 'ERA5MARINE'):
            fileblurb = 'BClocalSHIP5by5both'
    elif domain == 'blend':
        DatTyp = 'IDPHA'
        if (var == 'dpd'):
            DatTyp = 'PHA'
        if (var == 'td'):
            DatTyp = 'PHADPD'

        if (typee == 'BLEND'):
            fileblurb = 'FLATgrid'+DatTyp+'BClocalboth5by5'
        elif (typee == 'BLENDSHIP') | (typee == 'ERA5MASK') | (typee == 'ERA5'):
            fileblurb = 'FLATgrid'+DatTyp+'BClocalSHIPboth5by5'

#    if (typee == 'OTHER'):
#        INDIR  = WORKINGDIR+'/OTHERDATA/'
#        OUTDIR  = WORKINGDIR+'/OTHERDATA/'
#    elif (typee == 'MARINE'):
#        INDIR  = '/project/hadobs2/hadisdh/marine/ICOADS.3.0.0/'
#        OUTDIR = '/data/users/hadkw/WORKING_HADISDH/MARINE/DATA/'

#    INFILE = 'HadISDH.'+domain+ParamDict[var][0]+'.'+version+'_'+fileblurb+'_'+climBIT+'_cf'
    INFILE = 'HadISDH.'+domain+ParamDict[var][0]+'.'+version+'_'+fileblurb+'_'+climBIT+'_'+thenmon+thenyear+'_cf'
    OUTFILE = 'HadISDH.'+domain+ParamDict[var][0]+'.'+version+'_'+fileblurb+'_'+climBIT+'_'+TrendType+'trends_'+str(sttrd)+str(edtrd)	#70S-70N

    if (typee.find('ERA5') >= 0):

        INFILE = var+'2m_monthly_5by5_ERA5_1979'+str(edyr)
        OUTFILE = var+'2m_monthly_5by5_ERA5_'+climBIT+'_'+TrendType+'trends_'+str(sttrd)+str(edtrd)	#70S-70N

#        INFILEH = 'HadISDH.'+domain+ParamDict[var][0]+'.'+version+'_'+fileblurb+'_'+climBIT+'_cf'
        INFILEH = 'HadISDH.'+domain+ParamDict[var][0]+'.'+version+'_'+fileblurb+'_'+climBIT+'_'+thenmon+thenyear+'_cf'
        OUTFILEH = 'HadISDH.'+domain+ParamDict[var][0]+'.'+version+'_'+fileblurb+'_'+climBIT+'_'+TrendType+'trends_'+str(sttrd)+str(edtrd)	#70S-70N
# Removed the nowmonnowyear thenmonthenyear bits
#        INFILE = 'HadISDH.'+domain+ParamDict[var][0]+'.'+version+'_'+fileblurb+'_'+climBIT+'_'+thenmon+thenyear+'_cf'
#        OUTFILE = 'HadISDH.'+domain+ParamDict[var][0]+'.'+version+'_'+fileblurb+'_'+climBIT+'_'+nowmon+nowyear+'_'+TrendType+'trends_'+str(sttrd)+str(edtrd)	#70S-70N

    # Get Data
    if (typee.find('ERA') >= 0):
        styrh = np.copy(styr)
        styr = 1979
	
        if (domain == 'land'):
            ReadInfo = [var+'2m_anoms_land','time']
            OUTFILE = OUTFILE+'_land'
        if (domain == 'marine'):
            ReadInfo = [var+'2m_anoms_ocean','time']
            OUTFILE = OUTFILE+'_marine'
        if (domain == 'blend'):
            ReadInfo = [var+'2m_anoms','time']

        ReadInfoH = [var+'_anoms','time']
   
    else:
        ReadInfo = [var+'_anoms','time']

    print('Reading in the data for :',var,typee)
    TmpVals,Latitudes,Longitudes = GetGrid4(INDIR+INFILE+'.nc',ReadInfo,LatInfo,LonInfo)
    # Check that data have been read in
    #pdb.set_trace()
    
    # Seperate out data and times
    TheData = TmpVals[0]
    Times = TmpVals[1]
    TmpVals = []

    # Check the mdis = IDL output netCDF differs from Python output
    bads = np.where(TheData < -10000)
    if (len(bads[0]) > 0):
        TheData[bads] = MDI

    # If we're masking ERA then read in HadISDH
    if (typee.find('MASK') >= 0):
    
        print('Masking ERA5')
        OUTFILE = OUTFILE+'_mask'
        TmpValsH,LatitudesH,LongitudesH = GetGrid4(INDIRH+INFILEH+'.nc',ReadInfoH,LatInfo,LonInfo)

        # Seperate out data and times
        TheDataH = TmpValsH[0]
        TimesH = TmpValsH[1]
        TmpValsH = []

        # Check the mdis = IDL output netCDF differs from Python output
        bads = np.where(TheDataH < -10000)
        if (len(bads[0]) > 0):
            TheDataH[bads] = MDI
	    
	# Make HadISDH start in the same years
        TheDataH = TheDataH[(styr-styrh)*12:((edyr-styrh) + 1)*12,:,:]
	    
	# Now mask the ERA data with HadISDH missing data
        TheData[np.where(TheDataH == MDI)] = MDI

    # Calculate trends
    TrendGrids,LowBoundGrids,UpperBoundGrids,SE1sigGrids = GetTrends(TheData,styr,edyr,sttrd,edtrd,TrendType,ConfIntP,MDI,MissingDataThresh)
    
    
    # Write out files
    if (TrendType == 'OLS'):
    
        CommentText = TrendType+' decadal trend with p='+str(ConfIntP)+' confidence intervals [AR(1) correction following Santer et al., 2008] using a missing data threshold >= '+str(MissingDataThresh) 

    else:

        CommentText = TrendType+' decadal trend with p='+str(ConfIntP)+' confidence intervals following Sen 1968 using a missing data threshold >= '+str(MissingDataThresh)
    
    WriteNetCDF(OUTDIR+OUTFILE+'.nc',TrendGrids,LowBoundGrids,UpperBoundGrids,SE1sigGrids,MDI,CommentText,var,ParamDict[var][0],NameDict[var][0],str(sttrd)+' to '+str(edtrd)+NameDict[var][1],ParamDict[var][2],lats,lons)

    print("And were done")

if __name__ == '__main__':
    
    main(sys.argv[1:])

#************************************************************************
