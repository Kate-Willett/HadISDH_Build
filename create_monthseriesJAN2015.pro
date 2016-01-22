; TIDL
; 
; Author: Kate Willett
; Created: 1 February 2013
; Last update: 22 January 2016
; Location: /data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/HADISDH_BUILD/	
; GitHub: https://github.com/Kate-Willett/HadISDH_Build					
; -----------------------
; CODE PURPOSE AND OUTPUT
; -----------------------
; Reads in hourly HadISD data, converts to humidity variables, caluclates monthly means and monthly mean anomalies, saves to ascii and netCDF.
; Outputs to PHA folder: /data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/
; Outputs to /data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/NETCDF/
; Outputs to /data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/
;
; this program reads in every QC'd netcdf file and outputs a monthly mean anomaly, abs, clim and sd version
; this uses T, Tdew and SLP from the netCDF but also needs to know elevation in order to calculate SLP if necessary.
; this outputs T, Tdew, DPD, Twetbulb, vapour pressure, specific humidity and relative humidity using calc_evap.pro
; Also outputs SLP and windspeed
; May add heat indices in the future
;
; this also reads in source data and outputs a station history file
; /data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HISTORY/ of the format:
; /data/local/hadkw/HADCRUH2/PROGS/USHCN_v52d/src_codes/documentation/SHF_tob_inst.txt
; some amendments:
; SOURCE CODE 3=history created from raw data using: 
;	- change in station source (composited stations) 
; 	- change in ISD within file lat/lon (2012 onwards)
;	- change in observing frequency 
;	- change in observing times
;	- change in recording resolution (2012 onwards?)
; REMEMBER to convert lat/lon to degrees, minutes and seconds and elevation to feet (?)
;
; First, month hour averages are taken for each hour of the day - there must be at least 15 days present for each hour within the month
; Then the month average is made from the month hour averages. There must be at least 4 month hour averages with at least 1 in each tercile )) to 07,
; 08 to 15, 16 to 23
; There must also be at least one year in each decade of climatology 76-85, 86-95, 96-05
; There must be at least 15 years of T and Td (tests RH) within the 1976-2005 climatology period for each month present for the station to be kept
;
; <references to related published material, e.g. that describes data set>
; 
; -----------------------
; LIST OF MODULES
; -----------------------
; calc_evap.pro - written by kate Willett to calculate humidity variables
; make_months_oddtimesJAN2015.pro - written by Kate Willett to calculate monthly means - spitting out stations with too few obs.
; 
; -----------------------
; DATA
; -----------------------
; reads in netCDF hourly station data from HadISD /media/Kate1Ext3/HadISD.1.0.4.2015p/
; Old list of 6103 potential HadISD stations to include
; inlists='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/current_HadISD_stationinfo_AUG2011.txt'
; 20CR SLP data for making climatological SLP for humidity calculation
; inSLP='/data/local/hadkw/HADCRUH2/OTHERDATA/'	;CR20Jan7605MSLP_yycompos.151.170.240.10.37.8....nc
;
; -----------------------
; HOW TO RUN THE CODE
; -----------------------
; First make sure the source data are in the right place.
; Make sure this year's directories are set up: makeHadISDHdirectories.sh
; Make sure this year's PHA directories are set up: makePHAdirectories.sh
; Update this file to work with new version number and latest year of data and file structure
;
; > tidl
; > .compile make_months_oddtimesJAN2015.pro ; MUST BE FIRST!!!
; > .compile calc_evap.pro
; > .compile create_monthseriesJAN2015.pro
; create_monthseriesJAN2015.pro
; 
; if it fails and you need to re run
; > retall
; > close,/all
; .compile etc...
; -----------------------
; OUTPUT
; -----------------------
; ASCII monthly means and anomalies
; outdirASC='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/'
; GHCNM style ASCII monthly means for PHA
; outdirRAWq='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315q/monthly/raw/'
; outdirRAWe='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315e/monthly/raw/'
; outdirRAWt='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315t/monthly/raw/'
; outdirRAWdpd='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315dpd/monthly/raw/'
; outdirRAWtd='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315td/monthly/raw/'
; outdirRAWtw='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315tw/monthly/raw/'
; outdirRAWrh='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315rh/monthly/raw/'
; outdirRAWws='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315ws/monthly/raw/'
; outdirRAWslp='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315slp/monthly/raw/'
; outdirHIST='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HISTORY/'
; outdirNCF='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/NETCDF/'
; A list of stations that are not carried forward because they do not contain enough months of data
; ditchfile='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/tooshortforHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
; A list of stations that have enough months to be carried forward
; keepfile='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
; 
; -----------------------
; VERSION/RELEASE NOTES
; -----------------------
; 
; Version 2 (22 January 2016)
; ---------
;  
; Enhancements
; Updated to deal with 2016
; Added more detail to the header for code legacy
;  
; Changes
;  
; Bug fixes

;
; Version 1 (15 January 2015)
; ---------
;  
; Enhancements
;  
; Changes
;  
; Bug fixes
;  
; -----------------------
; OTHER INFORMATION
; -----------------------
;
;-------------------------------------------------------------------------
; JAN 2015
; updated to read in 2014
; now includes windpeed and sea level pressure
; moved 'BAD MONTHS' kick out to just below RH make_months and moved RH to be done first
; no point carrying on if there isn't enough humidity data - do not base on SLP which has lots of
; missing

; JAN 2014
; updated to read in 2013
; now creates hourly DPD and then monthly DPD AND monthly derived DPD (compare later)
; added a loop in make_months_oddtimesJAN2014.pro to remove all stations that have fewer 
; than 15 months for any one month within climatology period. This can occur in some cases 
; when the odd hour makes an hour_month clim possible but not a monthly..

; DEC 2013
; Adding dewpoint depression ready for 2013 update ***KATE STILL NEED TO DO THIS***
; Need to check that T-DPD = Td as it may not.
; Not entirely sure whether its best to calculate monthly T and Td and then create DPD
; Or whether its best to calculate monthly DPD directly from the hourly data
; For playing (to see whether there is more S-N ratio in DPD compared to Td) just use monthly conversions

; FEB 2013
; CHANGED station P calculation
; i) use actual station T to convert to monthly - test
; ii) make climatological monthly mean T values and use those to calc station P
; iii) read in CR20 monthly MSLP climatologies 1976-2005 and use these instead of 1013.25 - use climatological monthly mean T

;"Support for the Twentieth Century Reanalysis Project dataset is provided by the U.S. Department of Energy, 
; Office of Science Innovative and Novel Computational Impact on Theory and Experiment (DOE INCITE) program, 
; and Office of Biological and Environmental Research (BER), and by the National Oceanic and Atmospheric 
; Administration Climate Program Office."
;"20th Century Reanalysis V2 data provided by the NOAA/OAR/ESRL PSD, Boulder, Colorado, USA, from their Web site at 
; http://www.esrl.noaa.gov/psd/"
; We would also appreciate receiving a copy of the relevant publications. 

; both use Eq. from Smithsonian Tables p268

;-------------------------------------------------------------------------
pro create_monthseriesJAN2015

newstart=long(0)   	    ;long(0)	; use this to restart the program at a specified place 
nowmon='JAN'
nowyear='2016'
version='2.1.0.2015p'


indir='/media/Kate1Ext3/HadISD.1.0.4.2015p/'
inlists='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/current_HadISD_stationinfo_AUG2011.txt'
inSLP='/data/local/hadkw/HADCRUH2/OTHERDATA/'	;CR20Jan7605MSLP_yycompos.151.170.240.10.37.8....nc
outdirASC='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/ASCII/'
outdirRAWq='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315q/monthly/raw/'
outdirRAWe='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315e/monthly/raw/'
outdirRAWt='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315t/monthly/raw/'
outdirRAWdpd='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315dpd/monthly/raw/'
outdirRAWtd='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315td/monthly/raw/'
outdirRAWtw='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315tw/monthly/raw/'
outdirRAWrh='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315rh/monthly/raw/'
outdirRAWws='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315ws/monthly/raw/'
outdirRAWslp='/data/local/hadkw/HADCRUH2/UPDATE2015/PROGS/PHA_2015/PHA52j_full/pha_v52j/data/hadisdh/hadisdh7315slp/monthly/raw/'
outdirHIST='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/HISTORY/'
outdirNCF='/data/local/hadkw/HADCRUH2/UPDATE2015/MONTHLIES/NETCDF/'
ditchfile='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/tooshortforHadISDH.'+version+'_'+nowmon+nowyear+'.txt'
keepfile='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_'+nowmon+nowyear+'.txt'

; variables
mdi=-1e+30
stationid=''
stationelv=0.
;*** at some point add all the header info from the new HadISD files***

;times
monarr=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
styear=1973
stday=1
stmon=1
stjul=JULDAY(stmon,stday,styear,0)
edyear=2015 
edday=1
edmon=1
edjul=JULDAY(edmon,edday,edyear+1, 0)
edactjul=JULDAY(12,31,edyear,23)

ntims=LONG((edjul-stjul)*24.)
nmons=(edyear-styear+1)*12
nyrs=edyear-styear+1
actyears=indgen(nyrs)+styear
ndays=LONG(edjul-stjul)
full_times=(TIMEGEN(ntims,UNIT='Hours',START=stjul)-stjul) ; zero'd to jan 1st 1973, midnight?
int_times=lindgen(ntims)
times=TIMEGEN(nmons,UNIT='Months',START=stjul)
int_mons=indgen(nmons)
fulltemp_arr=make_array(ntims,/float,value=mdi)
fulldewp_arr=make_array(ntims,/float,value=mdi)
fullddep_arr=make_array(ntims,/float,value=mdi)
fulltwet_arr=make_array(ntims,/float,value=mdi)
fullevap_arr=make_array(ntims,/float,value=mdi)
fullesat_arr=make_array(ntims,/float,value=mdi)
fullqhum_arr=make_array(ntims,/float,value=mdi)
fullqsat_arr=make_array(ntims,/float,value=mdi)
fullrhum_arr=make_array(ntims,/float,value=mdi)
fullws_arr=make_array(ntims,/float,value=mdi)
fullslp_arr=make_array(ntims,/float,value=mdi)

; create array of half year counts taking into account leap years
; i.e., 1973 June 30th = 181st day Dec 31st = 365th day (184)
; i.e., 1974 June 30th = 181st day Dec 31st = 365th day (184)
; i.e., 1975 June 30th = 181st day Dec 31st = 365th day (184)
; i.e., 1976 June 30th = 182nt day Dec 31st = 366th day (184)
; leaps are 1976,1980,1984,1988,1992,1996,2000,2004,2008,2012
; leap if divisible by four by not 100, unless also divisible by 400 i.e. 1600, 2000

tots={structots,hd:[181,184]}
alltots=REPLICATE(tots,nyrs)
founds=WHERE(((actyears/4.)-FIX(actyears/4.) EQ 0.0) AND $
             (((actyears/100.)-FIX(actyears/100.) NE 0.0) OR $
	     ((actyears/400.)-FIX(actyears/400.) EQ 0.0)),count)
halfyrtots=REFORM(alltots.hd,2,nyrs)
halfyrtots(0,founds)=182
halfyrtots=REFORM(halfyrtots,nyrs*2)
leapsids=intarr(nyrs)
leapsids(founds)=1  ;1s identify leap years
JANpoint=indgen(744)
FEBpoint=indgen(696)+744
MARpoint=indgen(744)+1440
APRpoint=indgen(720)+2184
MAYpoint=indgen(744)+2904
JUNpoint=indgen(720)+3648
JULpoint=indgen(744)+4368
AUGpoint=indgen(744)+5112
SEPpoint=indgen(720)+5856
OCTpoint=indgen(744)+6576
NOVpoint=indgen(720)+7320
DECpoint=indgen(744)+8040

dates=[stjul,edactjul]
clims=[1976,2005]
;clpointies=indgen((clims(1)+1)-clims(0))+(clims(0)-styear)    ;an array from 3 to 32?
stclim=clims(0)-styear
edclim=clims(1)-styear
climsum=(edclim+1)-stclim
;stop,'check these clims'

;station hist arrays
tmp=make_array(1000,/string,value=' ')
tmpi=make_array(1000,/int,value=0)
histarr={histee,source:tmp,$		; 0 to 3
                wmoid:tmp,$		; 999999
		perst:tmp,$		; yyyymmdd
		pered:tmp,$		; yyyymmdd
		ltdeg:tmpi,$		; -999
		ltmin:tmpi,$		; 99
		ltsec:tmpi,$		; 99
		lndeg:tmpi,$		; -999
		lnmin:tmpi,$		; 99
		lnsec:tmpi,$		; 99
                chdist:tmp,$ 		; 999
		chdisttp:tmp,$		; MI ,YD , 
		chdir:tmp,$		;   N,
		stelevft:tmp,$		; 99999
		itelevft:tmp,$		; 9999 HM, TP
		obtimsHUM:tmp,$		; 06
		obtimsTMP:tmp,$		; HR this means all obs taken every 6 hours
		itlist:tmp}		; 99999 99999 99999

;-----------------------------------------------------------------------------
; IF SLP conversion method 3 then read in CR20 data
CR20arr=make_array(180,91,12,/float,value=mdi)
inn=NCDF_OPEN(inSLP+'20CRJan7605MSLP_yycompos.151.170.240.10.37.8.8.59.nc')
lonid=NCDF_VARID(inn,'lon') 	;centre points of 2deg boxes from 0 to 358.
latid=NCDF_VARID(inn,'lat') 	;centre points of 2deg boxes from 90 to -90
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,lonid,CR20lons
NCDF_VARGET,inn,latid,CR20lats
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,0)=CR20vals/100.
;make lats the northern most boundary
CR20lats=CR20lats+1.
;make lons the western most boundary starting from -180
CR20lons=CR20lons-1
CR20lons(WHERE(CR20lons GE 180))=-(360.-CR20lons(WHERE(CR20lons GE 180)))
CR20lons=SHIFT(CR20lons,89) ; they now go from -179 to 179
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179

inn=NCDF_OPEN(inSLP+'20CRFeb7605MSLP_yycompos.151.170.240.10.37.8.12.55.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,1)=CR20vals/100.

inn=NCDF_OPEN(inSLP+'20CRMar7605MSLP_yycompos.151.170.240.10.37.8.13.49.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,2)=CR20vals/100.

inn=NCDF_OPEN(inSLP+'20CRApr7605MSLP_yycompos.151.170.240.10.37.8.14.40.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,3)=CR20vals/100.

inn=NCDF_OPEN(inSLP+'20CRMay7605MSLP_yycompos.151.170.240.10.37.8.15.32.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,4)=CR20vals/100.

inn=NCDF_OPEN(inSLP+'20CRJun7605MSLP_yycompos.151.170.240.10.37.8.16.16.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,5)=CR20vals/100.

inn=NCDF_OPEN(inSLP+'20CRJul7605MSLP_yycompos.151.170.240.10.37.8.17.0.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,6)=CR20vals/100.

inn=NCDF_OPEN(inSLP+'20CRAug7605MSLP_yycompos.151.170.240.10.37.8.17.54.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,7)=CR20vals/100.

inn=NCDF_OPEN(inSLP+'20CRSep7605MSLP_yycompos.151.170.240.10.37.8.18.36.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,8)=CR20vals/100.

inn=NCDF_OPEN(inSLP+'20CROct7605MSLP_yycompos.151.170.240.10.37.8.19.23.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,9)=CR20vals/100.

inn=NCDF_OPEN(inSLP+'20CRNov7605MSLP_yycompos.151.170.240.10.37.8.20.1.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,10)=CR20vals/100.

inn=NCDF_OPEN(inSLP+'20CRDec7605MSLP_yycompos.151.170.240.10.37.8.20.54.nc')
varid=NCDF_VARID(inn,'prmsl')
NCDF_VARGET,inn,varid,CR20vals
NCDF_CLOSE,inn
CR20vals=SHIFT(CR20vals,89) ; lons now go gtom -179 to 179
CR20arr(*,*,11)=CR20vals/100.


;--------------------------------------------------------------------------------
; open station list and begin to loop through
openr,5,inlists
WHILE NOT EOF(5) DO BEGIN
  wmoid=''
  wbanid=''
  namoo=''
  cid=''
  lat=0.
  lon=0.
  stationelv=0.
  readf,5,wmoid,wbanid,namoo,cid,lat,lon,stationelv,format='(a6,x,a5,2x,a29,x,a2,x,f7.3,x,f8.3,x,f6.1)'
  IF (LONG(wmoid) LT LONG(newstart)) THEN continue
  stationid=wmoid+'-'+wbanid	; New ISD will have different filenames
  outstationid=wmoid+wbanid	; New ISD will have different filenames
  
;  IF (wmoid NE 722486) THEN continue
  
; open the file----------------------------------------------------------
  print,'Working on ',stationid

  filee=indir+stationid+'_mask2.nc.gz'
  spawn,'gunzip -c '+filee+' > homogfile.nc'
  inn=NCDF_OPEN('homogfile.nc')
  timid=NCDF_VARID(inn,'time')
  tmpid=NCDF_VARID(inn,'temperatures')
  dpid=NCDF_VARID(inn,'dewpoints')
  slpid=NCDF_VARID(inn,'slp')
  wsid=NCDF_VARID(inn,'windspeeds')
  inputid=NCDF_VARID(inn,'input_station_id')
  ; USING CONSTANT PRESSURE CALCULATED FROM ELEVATION BECAUSE SLP MAY NOT BE GOOD QUALITY 
  ; ANY CHANGES IN HUMIDITY ARE NOT DUE TO CHANGES IN PRESSURE THEN.
  NCDF_VARGET,inn,timid,tims
  NCDF_VARGET,inn,tmpid,temps
  NCDF_VARGET,inn,dpid,dewps
  NCDF_VARGET,inn,slpid,slps
  NCDF_VARGET,inn,wsid,ws
  NCDF_VARGET,inn,inputid,inputs
  NCDF_CLOSE,inn
  spawn,'rm homogfile.nc'

  
; make all mdis the same
  bads=WHERE(temps LE mdi,count)
  IF (count GT 0) THEN temps(bads)=mdi
  bads=WHERE(dewps LE mdi,count)
  IF (count GT 0) THEN dewps(bads)=mdi
  bads=WHERE(slps LE mdi,count)
  IF (count GT 0) THEN slps(bads)=mdi
  bads=WHERE(ws LE mdi,count)
  IF (count GT 0) THEN ws(bads)=mdi

;  MATCH,tims,full_times,suba,subb
  MATCH,tims,int_times,suba,subb    
  print,n_elements(suba),n_elements(subb)
;stop
  
  fulltemp_arr=make_array(ntims,/float,value=mdi)
  fulldewp_arr=make_array(ntims,/float,value=mdi)
  fullddep_arr=make_array(ntims,/float,value=mdi)
  fulltwet_arr=make_array(ntims,/float,value=mdi)
  fullevap_arr=make_array(ntims,/float,value=mdi)
  fullqhum_arr=make_array(ntims,/float,value=mdi)
  fullqsat_arr=make_array(ntims,/float,value=mdi)
  fullesat_arr=make_array(ntims,/float,value=mdi)
  fullrhum_arr=make_array(ntims,/float,value=mdi)
  fullws_arr=make_array(ntims,/float,value=mdi)
  fullslp_arr=make_array(ntims,/float,value=mdi)
  statP_arr=make_array(ntims,/float,value=mdi)	; ***FEB2013
  obsfreq_tmp=make_array(ntims,/int,value=0)	; to look at reporting frequency
  obsfreq_hum=make_array(ntims,/int,value=0)
  obsres_tmp=make_array(ntims,/float,value=mdi)	; to look at recording resolution
  obsres_hum=make_array(ntims,/float,value=mdi)
  obssource=make_array(ntims,/string,value='999999')
  
  
  fulltemp_arr(subb)=temps(suba)
  fulldewp_arr(subb)=dewps(suba)
  fullws_arr(subb)=ws(suba)
  fullslp_arr(subb)=slps(suba)
  obsfreq_tmp(subb(WHERE(temps(suba) NE mdi)))=1	; only where actualy temperatures exist
  obsfreq_hum(subb(WHERE(dewps(suba) NE mdi)))=1	; only where actualy dewpoint temperatures exist
  boo=where(obsfreq_tmp EQ 1,countt)
  boo=where(obsfreq_hum EQ 1,counth)
  print,countt,' ',counth
;stop  
  gotTs=WHERE(temps NE mdi)
  gotHs=WHERE(dewps NE mdi)
  restemps=temps
  restemps(gotTs)=ABS(temps(gotTs))-(FLOOR(ABS(temps(gotTs))))
  resdewps=dewps
  resdewps(gotHs)=ABS(dewps(gotHs))-(FLOOR(ABS(dewps(gotHs))))
  obsres_tmp(subb)=restemps(suba)		; only where actualy temperatures exist
  obsres_hum(subb)=resdewps(suba)		; only where actualy dewpoint temperatures exist

  obssource(subb)=FIX(inputs(*,suba),TYPE=7)
  
;  stop,'CHECK THESE FREQ, RES and INPUT are working'

; convert to other variables---------------------------------------------
  gots=WHERE(fulltemp_arr NE mdi AND fulldewp_arr NE mdi,count)
  IF (count GT 24000) THEN BEGIN	; 300 days for 20 years with 4 obs per day.

;  FEB2013 IF iii) then use CR20 MSLP
    tempyearsarr=make_array(8784,climsum,/float,value=mdi)        ; array with all hours including leaps present for each year
    tempclimsarr=make_array(8784,nyrs,/float,value=mdi)        ; array with all hours including leaps present for each year
    slpclimsarr=make_array(8784,nyrs,/float,value=mdi) ; array with all hours including leaps present for each year
    temppointer=0L
    FOR yrfill=0,nyrs-1 DO BEGIN
      IF (leapsids(yrfill) NE 1) THEN BEGIN   ; not a leap year so fill to Feb 28th and from Mar 1st
	IF (yrfill GE stclim) AND (yrfill LE edclim) THEN BEGIN
	  tempyearsarr(0:1415,yrfill-stclim)=fulltemp_arr(temppointer:temppointer+1415)
	  tempyearsarr(1440:8783,yrfill-stclim)=fulltemp_arr(temppointer+1416:temppointer+8759)
	ENDIF
	temppointer=temppointer+8760	
      ENDIF ELSE BEGIN
	IF (yrfill GE stclim) AND (yrfill LE edclim) THEN tempyearsarr(*,yrfill-stclim)=fulltemp_arr(temppointer:temppointer+8783)
        temppointer=temppointer+8784	    
      ENDELSE
;    print,temppointer,actyears(yrfill)
    ENDFOR
  ; now subset to get clims for each month, fill tempclimsarr with those clims, slpclimsarr with CR20 MSLP for closestgridbox
    matchlats=WHERE(CR20lats LT lat)
    thelat=matchlats(0)-1 
    matchlons=WHERE(CR20lons GT lon)
    IF (lon GT -179) THEN thelon=matchlons(0)-1 ELSE thelon=179 ; the last of 180 gridboxes covering 179 to -179
;    stop, 'check CR lats and lons'
    lotsofhours=tempyearsarr(JANpoint,*)   ; calculate T clims over clim period 1976-2005
    tempclimsarr(JANpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(JANpoint,*)=CR20arr(thelon,thelat,0)
    lotsofhours=tempyearsarr(FEBpoint,*)
    tempclimsarr(FEBpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(FEBpoint,*)=CR20arr(thelon,thelat,1)
    lotsofhours=tempyearsarr(MARpoint,*)
    tempclimsarr(MARpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(MARpoint,*)=CR20arr(thelon,thelat,2)
    lotsofhours=tempyearsarr(APRpoint,*)
    tempclimsarr(APRpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(APRpoint,*)=CR20arr(thelon,thelat,3)
    lotsofhours=tempyearsarr(MAYpoint,*)
    tempclimsarr(MAYpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(MAYpoint,*)=CR20arr(thelon,thelat,4)
    lotsofhours=tempyearsarr(JUNpoint,*)
    tempclimsarr(JUNpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(JUNpoint,*)=CR20arr(thelon,thelat,5)
    lotsofhours=tempyearsarr(JULpoint,*)
    tempclimsarr(JULpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(JULpoint,*)=CR20arr(thelon,thelat,6)
    lotsofhours=tempyearsarr(AUGpoint,*)
    tempclimsarr(AUGpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(AUGpoint,*)=CR20arr(thelon,thelat,7)
    lotsofhours=tempyearsarr(SEPpoint,*)
    tempclimsarr(SEPpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(SEPpoint,*)=CR20arr(thelon,thelat,8)
    lotsofhours=tempyearsarr(OCTpoint,*)
    tempclimsarr(OCTpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(OCTpoint,*)=CR20arr(thelon,thelat,9)
    lotsofhours=tempyearsarr(NOVpoint,*)
    tempclimsarr(NOVpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(NOVpoint,*)=CR20arr(thelon,thelat,10)
    lotsofhours=tempyearsarr(DECpoint,*)
    tempclimsarr(DECpoint,*)=MEDIAN(lotsofhours(WHERE(lotsofhours NE mdi)))
    slpclimsarr(DECpoint,*)=CR20arr(thelon,thelat,11)
  ;now convert back to fulltemp_arr space without fake leap years - converting standard P too
    temppointer=0L
    FOR yrfill=0,nyrs-1 DO BEGIN
      IF (leapsids(yrfill) NE 1) THEN BEGIN   ; not a leap year so fill to Feb 28th and from Mar 1st
;	statP_arr(temppointer:temppointer+1415)=slpclimsarr(0:1415,yrfill)*((((273.15+tempclimsarr(0:1415,yrfill))-(0.0065*stationelv))/(273.15+tempclimsarr(0:1415,yrfill)))^5.256)   
;	statP_arr(temppointer+1416:temppointer+8759)=slpclimsarr(1440:8783,yrfill)*((((273.15+tempclimsarr(1440:8783,yrfill))-(0.0065*stationelv))/(273.15+tempclimsarr(1440:8783,yrfill)))^5.256)   
; AS WE'RE USING STATION T NOT SEA LEVEL T, TO GET RATIO OF SEA LEVEL T TO STATION T NEEDS A REARRANGMENT OF THE (slT-HeightConv)/slT to stT/(stT+HeighConv)
	statP_arr(temppointer:temppointer+1415)=slpclimsarr(0:1415,yrfill)*(((273.15+tempclimsarr(0:1415,yrfill))/((273.15+tempclimsarr(0:1415,yrfill))+(0.0065*stationelv)))^5.256)   
	statP_arr(temppointer+1416:temppointer+8759)=slpclimsarr(1440:8783,yrfill)*(((273.15+tempclimsarr(1440:8783,yrfill))/((273.15+tempclimsarr(1440:8783,yrfill))+(0.0065*stationelv)))^5.256)   
	temppointer=temppointer+8760	
      ENDIF ELSE BEGIN
;	statP_arr(temppointer:temppointer+8783)=slpclimsarr(*,yrfill)*((((273.15+tempclimsarr(*,yrfill))-(0.0065*stationelv))/(273.15+tempclimsarr(*,yrfill)))^5.256)	
	statP_arr(temppointer:temppointer+8783)=slpclimsarr(*,yrfill)*(((273.15+tempclimsarr(*,yrfill))/((273.15+tempclimsarr(*,yrfill))+(0.0065*stationelv)))^5.256)	
	temppointer=temppointer+8784	    
      ENDELSE
    ENDFOR
;  stop,'check out station Ps'
    
    fullddep_arr(gots)=fulltemp_arr(gots)-fulldewp_arr(gots)
; Check DPD for subzeros - there really shouldn't be any as QC should have picked this up
    subszeros=WHERE(fullddep_arr(gots) LT 0.,countss)
    IF (countss GT 0) THEN stop,'SUB ZEROS FOUND'
    
    fullevap_arr(gots)=calc_evap(fulldewp_arr(gots),statP_arr(gots))	    ;station_P
    fullesat_arr(gots)=calc_evap(fulltemp_arr(gots),statP_arr(gots))	    ;station_P
    fullrhum_arr(gots)=(fullevap_arr(gots)/calc_evap(fulltemp_arr(gots),statP_arr(gots)))*100.    ;station_P
    fulltwet_arr(gots)=calc_wetbulb(fullevap_arr(gots),statP_arr(gots),fulldewp_arr(gots),fulltemp_arr(gots)) ;station_P
    ice=WHERE(fulltwet_arr(gots) LE 0,icount)
    IF (icount GT 0) THEN BEGIN
      fullevap_arr(gots(ice))=calc_evap_ice(fulldewp_arr(gots(ice)),statP_arr(gots))	;station_P
      fullesat_arr(gots(ice))=calc_evap_ice(fulltemp_arr(gots(ice)),statP_arr(gots))	;station_P
      fullrhum_arr(gots(ice))=(fullevap_arr(gots(ice))/calc_evap(fulltemp_arr(gots(ice)),statP_arr(gots)))*100.   ;station_P
    ENDIF  
; recalc wets with correct (?) evaps - NOT 100% this is correct but errors are smallish
    fulltwet_arr(gots)=calc_wetbulb(fullevap_arr(gots),statP_arr(gots),fulldewp_arr(gots),fulltemp_arr(gots)) ;station_P
    fullqhum_arr(gots)=calc_qhum(fullevap_arr(gots),statP_arr(gots))	;station_P
    fullqsat_arr(gots)=calc_qhum(fullesat_arr(gots),statP_arr(gots))	;station_P
  ENDIF ELSE BEGIN
    openw,99,ditchfile,/append
    printf,99,stationid,'HOURS: ',count,format='(a12,x,a7,i6)'
    close,99
    print,'Too few hours, moving on...'
    continue
  ENDELSE

;create monthly means/anoms/clims/sds------------------------------------

  RHabs_mm=make_array(nmons,/float,value=mdi)
  RHanoms_mm=make_array(nmons,/float,value=mdi)
  RHsd_mm=make_array(nmons,/float,value=mdi)
  RHclims_mm=make_array(12,/float,value=mdi)
  RHanoms_mm=make_months_oddtimesJAN2015(fullrhum_arr,dates,clims,mdi,type=type,stdev_mm=RHsd_mm,abs_mm=RHabs_mm,clims_mm=RHclims_mm)

  ; deliberately only after RH which requires T and Td to be present
  ; if insufficient data here then ditch station
  ; do not need to process ALL others
  IF (type EQ 'BAD') THEN BEGIN
    openw,99,ditchfile,/append
    printf,99,stationid,'BAD CLIMS',format='(a12,x,a9)'
    close,99
    print,'Cannot calculate climatology, moving on...'
    continue
  ENDIF

  Pabs_mm=make_array(nmons,/float,value=mdi)
  Panoms_mm=make_array(nmons,/float,value=mdi)
  Psd_mm=make_array(nmons,/float,value=mdi)
  Pclims_mm=make_array(12,/float,value=mdi)
  Panoms_mm=make_months_oddtimesJAN2015(statP_arr,dates,clims,mdi,type=type,stdev_mm=Psd_mm,abs_mm=Pabs_mm,clims_mm=Pclims_mm)

  Tabs_mm=make_array(nmons,/float,value=mdi)
  Tanoms_mm=make_array(nmons,/float,value=mdi)
  Tsd_mm=make_array(nmons,/float,value=mdi)
  Tclims_mm=make_array(12,/float,value=mdi)
  Tanoms_mm=make_months_oddtimesJAN2015(fulltemp_arr,dates,clims,mdi,type=type,stdev_mm=Tsd_mm,abs_mm=Tabs_mm,clims_mm=Tclims_mm)

  Tdabs_mm=make_array(nmons,/float,value=mdi)
  Tdanoms_mm=make_array(nmons,/float,value=mdi)
  Tdsd_mm=make_array(nmons,/float,value=mdi)
  Tdclims_mm=make_array(12,/float,value=mdi)
  Tdanoms_mm=make_months_oddtimesJAN2015(fulldewp_arr,dates,clims,mdi,type=type,stdev_mm=Tdsd_mm,abs_mm=Tdabs_mm,clims_mm=Tdclims_mm)

  DPDabs_mm=make_array(nmons,/float,value=mdi)
  DPDanoms_mm=make_array(nmons,/float,value=mdi)
  DPDsd_mm=make_array(nmons,/float,value=mdi)
  DPDclims_mm=make_array(12,/float,value=mdi)
  DPDanoms_mm=make_months_oddtimesJAN2015(fullddep_arr,dates,clims,mdi,type=type,stdev_mm=DPDsd_mm,abs_mm=DPDabs_mm,clims_mm=DPDclims_mm)

; Derive Td and DPD at the monthly resolution for comparison
  derivedDPDabs_mm=make_array(nmons,/float,value=mdi)
  derivedTdabs_mm=make_array(nmons,/float,value=mdi)
  gots=WHERE(DPDabs_mm NE mdi,countgots)
  IF (countgots GT 0) THEN BEGIN
    derivedDPDabs_mm(gots)=Tabs_mm(gots)-Tdabs_mm(gots)
    derivedTdabs_mm(gots)=Tabs_mm(gots)-DPDabs_mm(gots)
  ENDIF
;  stop,'Compare Td and DPD derived and calculated directly'

  Twabs_mm=make_array(nmons,/float,value=mdi)
  Twanoms_mm=make_array(nmons,/float,value=mdi)
  Twsd_mm=make_array(nmons,/float,value=mdi)
  Twclims_mm=make_array(12,/float,value=mdi)
  Twanoms_mm=make_months_oddtimesJAN2015(fulltwet_arr,dates,clims,mdi,type=type,stdev_mm=Twsd_mm,abs_mm=Twabs_mm,clims_mm=Twclims_mm)

  eabs_mm=make_array(nmons,/float,value=mdi)
  eanoms_mm=make_array(nmons,/float,value=mdi)
  esd_mm=make_array(nmons,/float,value=mdi)
  eclims_mm=make_array(12,/float,value=mdi)
  eanoms_mm=make_months_oddtimesJAN2015(fullevap_arr,dates,clims,mdi,type=type,stdev_mm=esd_mm,abs_mm=eabs_mm,clims_mm=eclims_mm)

  qabs_mm=make_array(nmons,/float,value=mdi)
  qanoms_mm=make_array(nmons,/float,value=mdi)
  qsd_mm=make_array(nmons,/float,value=mdi)
  qclims_mm=make_array(12,/float,value=mdi)
  qanoms_mm=make_months_oddtimesJAN2015(fullqhum_arr,dates,clims,mdi,type=type,stdev_mm=qsd_mm,abs_mm=qabs_mm,clims_mm=qclims_mm)

  qsatabs_mm=make_array(nmons,/float,value=mdi)
  qsatanoms_mm=make_array(nmons,/float,value=mdi)
  qsatsd_mm=make_array(nmons,/float,value=mdi)
  qsatclims_mm=make_array(12,/float,value=mdi)
  qsatanoms_mm=make_months_oddtimesJAN2015(fullqsat_arr,dates,clims,mdi,type=type,stdev_mm=qsatsd_mm,abs_mm=qsatabs_mm,clims_mm=qsatclims_mm)

  WSabs_mm=make_array(nmons,/float,value=mdi)
  WSanoms_mm=make_array(nmons,/float,value=mdi)
  WSsd_mm=make_array(nmons,/float,value=mdi)
  WSclims_mm=make_array(12,/float,value=mdi)
  WSanoms_mm=make_months_oddtimesJAN2015(fullws_arr,dates,clims,mdi,type=type,stdev_mm=WSsd_mm,abs_mm=WSabs_mm,clims_mm=WSclims_mm)

  SLPabs_mm=make_array(nmons,/float,value=mdi)
  SLPanoms_mm=make_array(nmons,/float,value=mdi)
  SLPsd_mm=make_array(nmons,/float,value=mdi)
  SLPclims_mm=make_array(12,/float,value=mdi)
  SLPanoms_mm=make_months_oddtimesJAN2015(fullslp_arr,dates,clims,mdi,type=type,stdev_mm=SLPsd_mm,abs_mm=SLPabs_mm,clims_mm=SLPclims_mm)
   
; go through hours and look for changes in input stations, reporting frequency and recording resolution
; time consuming - could use some UNIQUE command?

  changehis=stjul
  changetyp=0	       ;0=none,1=input,2=freq,3=res
  changeinput=strmid(obssource(0),0,6) ;starting source station
  obsfreqT='00'
  obsfreqH='00'
  obsresT='BLANK'
  obsresH='BLANK '
  countch=0
  lasttime=0.  ;1973,Jan 1st zerod
  histarr={histee,source:tmp,$         ; 0 to 3
		wmoid:tmp,$	       ; 999999
	       perst:tmp,$	       ; yyyymmdd
	       pered:tmp,$	       ; yyyymmdd
	       ltdeg:tmpi,$	       ; -999
	       ltmin:tmpi,$	       ; 99
	       ltsec:tmpi,$	       ; 99
	       lndeg:tmpi,$	       ; -999
	       lnmin:tmpi,$	       ; 99
	       lnsec:tmpi,$	       ; 99
		chdist:tmp,$	       ; 999
	       chdisttp:tmp,$	       ; MI ,YD , 
	       chdir:tmp,$	       ;   N,
	       stelevft:tmp,$	       ; 99999
	       itelevft:tmp,$	       ; 9999 HM, TP
	       obtimsHUM:tmp,$         ; 06
	       obtimsTMP:tmp,$         ; HR this means all obs taken every 6 hours
	       itlist:tmp}	       ; 99999 99999 99999

; find changes in source data by year
; bundle up into seasons (well 182 day periods) - may still be too sensitive
  uniqinputs=UNIQ(obssource(WHERE(obssource NE '999999')))     ; finds ENDS of sustained periods
  IF (n_elements(uniqinputs) GT 1) THEN BEGIN
    PRINT,'A COMPOSITE!'
    obssource=REFORM(obssource,24,ndays)  
    full_times=REFORM(full_times,24,ndays)
    totsource='999999'
    yrcount=0
    oldsource='999999'
    oldpct=0.
    beginit=0
    datestamp=stjul
    counthfyrs=0    ;counter to loop through halfyrtots
    FOR dd=0,ndays-1 DO BEGIN
      gots=WHERE(obssource(*,dd) NE '999999',count)
      IF (count GT 0) THEN totsource=[totsource,strmid(obssource(gots,dd),0,6)]
      yrcount=yrcount+1
      IF (yrcount EQ halfyrtots(counthfyrs)) THEN BEGIN
	IF (n_elements(totsource) GT 400) THEN BEGIN   ; most days present (4 hours times 180 days = 720 obs)
	  totsource=totsource(1:n_elements(totsource)-1)
	  monhist=HISTOGRAM(FIX(totsource,type=3),binsize=1,min=MIN(FIX(totsource,type=3)))
	  binsies=lindgen(n_elements(monhist))+MIN(FIX(totsource,type=3))
	  mainsource=binsies(WHERE(monhist EQ MAX(monhist)))
	  sourcepct=MAX(monhist)/TOTAL(monhist)
	  IF (beginit EQ 0) THEN BEGIN
	    beginit=1  ; 0 implies not enough data.
	   oldsource=mainsource
	   oldpct=sourcepct
	   yrcount=0
	   counthfyrs=counthfyrs+1
	    totsource='999999'
	    datestamp=full_times(0,dd+1)+stjul ;date from beginning of year
	    continue
	  ENDIF ELSE IF (mainsource NE oldsource) OR ((sourcepct NE oldpct) AND ((sourcepct EQ 1.0) OR (oldpct EQ 1.0))) THEN BEGIN
	   print,'FOUND SOURCE CHANGE'
	    changehis=[changehis,datestamp]
	    changetyp=[changetyp,1]
	    changeinput=[changeinput,string(mainsource,format='(i06)')]        ; the new ID after change
	    obsfreqT=[obsfreqT,'00']	       ; new frequency after change
	    obsfreqH=[obsfreqH,'00']
	    obsresT=[obsresT,'BLANK']
	    obsresH=[obsresH,'BLANK ']
	    countch=countch+1
	    oldsource=mainsource
	   oldpct=sourcepct
	  ENDIF 
	ENDIF 
	IF (dd LT ndays-1) THEN datestamp=full_times(0,dd+1)+stjul     ;date from beginning of year
	yrcount=0
       counthfyrs=counthfyrs+1
	totsource='999999'	
      ENDIF
    ENDFOR
ENDIF  
  
; find changes in reporting frequencies 
; bundle up into months (well 182 day periods) - may still be too sensitive
; IF LESS THAN 4 obs per day (4 hourly) then this month wouldn't make it so ignore.  
  obsfreq_tmp=REFORM(obsfreq_tmp,24,ndays)  
  obsfreq_hum=REFORM(obsfreq_hum,24,ndays)  
  full_times=REFORM(full_times,24,ndays)
  totfreqT=intarr(halfyrtots(0))
  totfreqH=intarr(halfyrtots(0))
  binsies=indgen(25)
  yrcount=0
  oldfreqT='00'
  oldfreqH='00'
  beginit=0
  datestamp=stjul
  counthfyrs=0    ;counter to loop through halfyrtots
  FOR dd=0,ndays-1 DO BEGIN
    totfreqT(yrcount)=TOTAL(obsfreq_tmp(*,dd))
    totfreqH(yrcount)=TOTAL(obsfreq_hum(*,dd))
    yrcount=yrcount+1
;    print,yrcount,halfyrtots(counthfyrs),counthfyrs
    IF (yrcount EQ halfyrtots(counthfyrs)) THEN BEGIN
      IF (TOTAL(totfreqT) GT 0) AND (TOTAL(totfreqH) GT 0) THEN BEGIN
	monhist=HISTOGRAM(totfreqT(WHERE(totfreqT NE 0)),binsize=1,nbins=25,min=0)
	freqT=binsies(WHERE(monhist EQ MAX(monhist)))
	monhist=HISTOGRAM(totfreqH(WHERE(totfreqH NE 0)),binsize=1,nbins=25,min=0)
	freqH=binsies(WHERE(monhist EQ MAX(monhist)))
;	 print,freqH,freqT
	CASE 1 OF
	 freqT(0) GT 8: freqT='24'
	 freqT(0) GT 4 AND freqT(0) LT 9: freqT='08'
	 freqT(0) EQ 4: freqT='04'
	 freqT(0) LT 4: freqT=oldfreqT
	ENDCASE
	CASE 1 OF
	 freqH(0) GT 8: freqH='24'
	 freqH(0) GT 4 AND freqH(0) LT 9: freqH='08'
	 freqH(0) EQ 4: freqH='04'     
	 freqH(0) LT 4: freqH=oldfreqH
	ENDCASE
;	 print,counthfyrs,' ',freqH,oldfreqH, freqT,oldfreqT
	IF (beginit EQ 0) THEN BEGIN
	  beginit=1    ; 0 implies not enough data.
	 oldfreqT=freqT
	 oldfreqH=freqH
	 yrcount=0
	 counthfyrs=counthfyrs+1
	  totfreqT=intarr(halfyrtots(counthfyrs))
	  totfreqH=intarr(halfyrtots(counthfyrs))
	  datestamp=full_times(0,dd+1)+stjul   ;date from beginning of year
	 continue
	ENDIF ELSE IF (TOTAL(totfreqH) GT 400) AND ((freqT NE oldfreqT) OR (freqH NE oldfreqH)) THEN BEGIN ; enough data
	 print,'FOUND FREQ CHANGE'
;	 stop
	  changehis=[changehis,datestamp]
	  changetyp=[changetyp,2]
	  changeinput=[changeinput,'999999']   ; the new ID after change
	  obsfreqT=[obsfreqT,freqT]	       ; new frequency after change
	  obsfreqH=[obsfreqH,freqH]
	  obsresT=[obsresT,'BLANK']
	  obsresH=[obsresH,'BLANK ']
	  countch=countch+1
	  oldfreqT=freqT
	 oldfreqH=freqH
	ENDIF 
      ENDIF
      IF (dd LT ndays-1) THEN BEGIN
	datestamp=full_times(0,dd+1)+stjul     ;date from beginning of year
	yrcount=0
	counthfyrs=counthfyrs+1
	totfreqT=intarr(halfyrtots(counthfyrs))
	totfreqH=intarr(halfyrtots(counthfyrs))
      ENDIF
    ENDIF
  ENDFOR

; find changes in reporting resolutions WHOLE, WH&DM, HALF, DECIM
; bundle up into months (well 182 day periods) - may still be too sensitive
; IF LESS THAN 4 obs per day (4 hourly) then this month wouldn't make it so ignore.  
  obsres_tmp=REFORM(obsres_tmp,24,ndays)  
  obsres_hum=REFORM(obsres_hum,24,ndays)  
  totresT=0.
  totresH=0.
  binsies=findgen(10)*0.1
  yrcount=0
  oldresT=0
  oldresH=0
  beginit=0
  datestamp=stjul
  counthfyrs=0    ;counter to loop through halfyrtots
  FOR dd=0,ndays-1 DO BEGIN
    gots=WHERE(obsres_tmp(*,dd) NE mdi,count)
    IF (count GT 0) THEN totresT=[totresT,obsres_tmp(gots,dd)]
    gots=WHERE(obsres_hum(*,dd) NE mdi,count)
    IF (count GT 0) THEN totresH=[totresH,obsres_hum(gots,dd)]
    yrcount=yrcount+1
    IF (yrcount EQ halfyrtots(counthfyrs)) THEN BEGIN
      IF (n_elements(totresH) GT 400) AND (n_elements(totresT) GT 400) THEN BEGIN      ; check there are some data
       monhistT=HISTOGRAM(totresT,binsize=0.1,nbins=10,min=0.)
	findresT=binsies(REVERSE(SORT(monhistT)))
       monhistT=monhistT(REVERSE(SORT(monhistT)))
	monhistH=HISTOGRAM(totresH,binsize=0.1,nbins=10,min=0.)
	findresH=binsies(REVERSE(SORT(monhistH)))
       monhistH=monhistH(REVERSE(SORT(monhistH)))
	resT='BLANK'
       resH='BLANK '
       CASE 1 OF
	 findresT(0) EQ 0.0 AND (monhistT(0)/TOTAL(monhistT) GE 0.99): resT='WHOLE'    ; 90% of obs
	 findresT(0) EQ 0.0 AND (monhistT(0)/TOTAL(monhistT) GE 0.6): resT='WH&DM'     ; 60% of obs
	 TOTAL(findresT(0:1)) EQ 0.5 AND (TOTAL(monhistT(0:1)) GT TOTAL(monhistT(2:9))): resT=' HALF'
	 ELSE: resT='DECIM'
       ENDCASE
       CASE 1 OF
	 findresH(0) EQ 0.0 AND (monhistH(0)/TOTAL(monhistH) GE 0.99): resH='WHOLE '
	 findresH(0) EQ 0.0 AND (monhistH(0)/TOTAL(monhistH) GE 0.6): resH='WH&DM '    ; 60% of obs
	 TOTAL(findresH(0:1)) EQ 0.5 AND (TOTAL(monhistH(0:1)) GT TOTAL(monhistH(2:9))): resH=' HALF '         
	 ELSE: resH='DECIM '
       ENDCASE
;      print,resT,findresT(0),findresT(1),monhistT(0),monhistT(1),TOTAL(monhistT)
;      print,resH,findresH(0),findresH(1),monhistT(0),monhistH(1),TOTAL(monhistH)
	IF (beginit EQ 0) THEN BEGIN
	  beginit=1    ; 0 implies not enough data.
	 oldresT=resT  ; should be WHOLE, DECIM or HALF
	 oldresH=resH
	 yrcount=0
	 counthfyrs=counthfyrs+1
	  totresT=0.
	  totresH=0.
	  datestamp=full_times(0,dd+1)+stjul   ;date from beginning of year
	  continue
	ENDIF ELSE IF (resT NE oldresT) OR (resH NE oldresH) THEN BEGIN
	 print,'FOUND RES CHANGE'
	  changehis=[changehis,datestamp]
	  changetyp=[changetyp,3]
	  changeinput=[changeinput,'999999']   ; the new ID after change
	  obsfreqT=[obsfreqT,'00']
	  obsfreqH=[obsfreqH,'00']
	  obsresT=[obsresT,resT]	       ; new resolution after change
	  obsresH=[obsresH,resH]
	  countch=countch+1
	  oldresT=resT
	 oldresH=resH
	ENDIF 
      ENDIF
      IF (dd LT ndays-1) THEN datestamp=full_times(0,dd+1)+stjul
      yrcount=0
      counthfyrs=counthfyrs+1
      totresT=0.
      totresH=0.
    ENDIF
  ENDFOR

; compile and sort changes feeding though all info   
; WILL ONLY PRINT FROM histarr(1) onwards
  histarr.source=make_array(1000,/string,value='3')

  hissort=SORT(changehis)
  changehis=changehis(hissort) ;need to be converted to year, month, day
  CALDAT,changehis(0),mm,dd,yy
  histarr.perst(0)=string(yy,format='(i4)')+string(mm,format='(i02)')+string(dd,format='(i02)')  
  histarr.pered(0)=histarr.perst(0)
  IF (lat GE 0.0) THEN BEGIN
    histarr.ltdeg(*)=FLOOR(lat) 
    histarr.ltmin(*)=FLOOR((lat-(FLOOR(lat)))*60.) 
    histarr.ltsec(*)=ROUND((((lat-(FLOOR(lat)))*60.)-FLOOR((lat-(FLOOR(lat)))*60.))*60.)     
  ENDIF ELSE BEGIN
    histarr.ltdeg(*)=CEIL(lat)
    histarr.ltmin(*)=ABS(CEIL((lat-(CEIL(lat)))*60.)) 
    histarr.ltsec(*)=ABS(ROUND((((lat-(CEIL(lat)))*60.)-CEIL((lat-(CEIL(lat)))*60.))*60.))	 
  ENDELSE
  IF (lon GE 0.0) THEN BEGIN
    histarr.lndeg(*)=FLOOR(lon)
    histarr.lnmin(*)=FLOOR((lon-(FLOOR(lon)))*60.) 
    histarr.lnsec(*)=ROUND((((lon-(FLOOR(lon)))*60.)-FLOOR((lon-(FLOOR(lon)))*60.))*60.)     
  ENDIF ELSE BEGIN
    histarr.lndeg(*)=CEIL(lon)
    histarr.lnmin(*)=ABS(CEIL((lon-(CEIL(lon)))*60.)) 
    histarr.lnsec(*)=ABS(ROUND((((lon-(CEIL(lon)))*60.)-CEIL((lon-(CEIL(lon)))*60.))*60.))	   
  ENDELSE
  
;  changetyp=changetyp(hissort) ; info not yet incorporated
  histarr.wmoid(0:countch)=changeinput(hissort)        
  histarr.obtimsTMP(0:countch)=obsfreqT(hissort)
  histarr.obtimsHUM(0:countch)=obsfreqH(hissort)
  histarr.itlist(0:countch)=obsresH(hissort)+obsresT(hissort)  ; put in itlist for now

  IF (countch GT 0) THEN BEGIN
    FOR cc=1,countch DO BEGIN
      IF (histarr.wmoid(cc) EQ '999999') THEN histarr.wmoid(cc)=histarr.wmoid(cc-1)
      IF (histarr.obtimsTMP(cc) EQ '00') THEN histarr.obtimsTMP(cc)=histarr.obtimsTMP(cc-1)
      IF (histarr.obtimsHUM(cc) EQ '00') THEN histarr.obtimsHUM(cc)=histarr.obtimsHUM(cc-1)
      IF (histarr.itlist(cc) EQ 'BLANK BLANK') THEN histarr.itlist(cc)=histarr.itlist(cc-1)
      CALDAT,changehis(cc),mm,dd,yy
      histarr.pered(cc)=string(yy,format='(i4)')+string(mm,format='(i02)')+string(dd,format='(i02)')  
      histarr.perst(cc)=histarr.pered(cc-1)
      IF (histarr.pered(cc) EQ histarr.pered(cc-1)) THEN BEGIN
	print,'DOUBLE!!!',histarr.pered(cc)
	; this is the same time as the one before, and could be the same as the one before that actually
	IF (histarr.wmoid(cc-1) NE histarr.wmoid(cc)) THEN histarr.wmoid(cc-1)=histarr.wmoid(cc)
	IF (histarr.obtimsTMP(cc-1) NE histarr.obtimsTMP(cc)) THEN histarr.obtimsTMP(cc-1)=histarr.obtimsTMP(cc)
	IF (histarr.obtimsHUM(cc-1) NE histarr.obtimsHUM(cc)) THEN histarr.obtimsHUM(cc-1)=histarr.obtimsHUM(cc)
	IF (histarr.itlist(cc-1) NE histarr.itlist(cc) ) THEN histarr.itlist(cc-1)=histarr.itlist(cc)
	histarr.perst(cc)=histarr.perst(cc-1)
       
       histarr.source(cc)='X'  ;stops line being printed
	IF (cc GE 2) THEN BEGIN
	 IF (histarr.pered(cc) EQ histarr.pered(cc-2)) THEN BEGIN
	    print,'TRIPLE!!!',histarr.pered(cc)
	; this is the same time as the one before, and the same as the one before that actually
	    IF (histarr.wmoid(cc-2) NE histarr.wmoid(cc)) THEN histarr.wmoid(cc-2)=histarr.wmoid(cc)
	    IF (histarr.obtimsTMP(cc-2) NE histarr.obtimsTMP(cc)) THEN histarr.obtimsTMP(cc-2)=histarr.obtimsTMP(cc)
	    IF (histarr.obtimsHUM(cc-2) NE histarr.obtimsHUM(cc)) THEN histarr.obtimsHUM(cc-2)=histarr.obtimsHUM(cc)
	    IF (histarr.itlist(cc-2) NE histarr.itlist(cc)) THEN histarr.itlist(cc-2)=histarr.itlist(cc)
	    histarr.perst(cc)=histarr.perst(cc-2)
       
	   histarr.source(cc)='X'      ;stops line being printed
	  ENDIF
       ENDIF
      ENDIF
    ENDFOR
  ENDIF
   
;save to files----------------------------------------------------------- 
  openw,99,outdirHIST+stationid+'.his'
  IF (countch GT 0) THEN BEGIN
    FOR cc=1,countch DO BEGIN
      IF (histarr.source(cc) NE 'X') THEN $ 
      printf,99,histarr.source(cc),histarr.wmoid(cc),histarr.perst(cc),histarr.pered(cc),$
	      histarr.ltdeg(cc),histarr.ltmin(cc),histarr.ltsec(cc),$
	      histarr.lndeg(cc),histarr.lnmin(cc),histarr.lnsec(cc),$
	     histarr.chdist(cc),histarr.chdisttp(cc),histarr.chdir(cc),$
	     histarr.stelevft(cc),histarr.itelevft(cc),$
	     histarr.obtimsHUM(cc),histarr.obtimsTMP(cc),histarr.itlist(cc),$
	     format='(a0,x,a6,x,2(a8,x),2(i4,x,i2,x,i2,x),a3,x,a3,x,a3,x,a5,x,a4,x,a2,a2,x,a11)'
    ENDFOR
  ENDIF
  close,99

  full_times=REFORM(full_times,ntims)

  netcdf_outfile=outdirNCF+stationid+'_hummonthQC.nc'
  
  wilma=NCDF_CREATE(netcdf_outfile,/clobber)
  
  tid=NCDF_DIMDEF(wilma,'time',nmons)
  clmid=NCDF_DIMDEF(wilma,'month',12)
  charid=NCDF_DIMDEF(wilma, 'Character', 3)
  
  timesvar=NCDF_VARDEF(wilma,'times',[tid],/SHORT)
  tempanomvar=NCDF_VARDEF(wilma,'temp_anoms',[tid],/FLOAT)
  tempabsvar=NCDF_VARDEF(wilma,'temp_abs',[tid],/FLOAT)
  tempsdvar=NCDF_VARDEF(wilma,'temp_std',[tid],/FLOAT)
  dewpanomvar=NCDF_VARDEF(wilma,'dewp_anoms',[tid],/FLOAT)
  dewpabsvar=NCDF_VARDEF(wilma,'dewp_abs',[tid],/FLOAT)
  dewpsdvar=NCDF_VARDEF(wilma,'dewp_std',[tid],/FLOAT)
  ddepanomvar=NCDF_VARDEF(wilma,'ddep_anoms',[tid],/FLOAT)
  ddepabsvar=NCDF_VARDEF(wilma,'ddep_abs',[tid],/FLOAT)
  ddepsdvar=NCDF_VARDEF(wilma,'ddep_std',[tid],/FLOAT)
  twetanomvar=NCDF_VARDEF(wilma,'twet_anoms',[tid],/FLOAT)
  twetabsvar=NCDF_VARDEF(wilma,'twet_abs',[tid],/FLOAT)
  twetsdvar=NCDF_VARDEF(wilma,'twet_std',[tid],/FLOAT)
  evapanomvar=NCDF_VARDEF(wilma,'evap_anoms',[tid],/FLOAT)
  evapabsvar=NCDF_VARDEF(wilma,'evap_abs',[tid],/FLOAT)
  evapsdvar=NCDF_VARDEF(wilma,'evap_std',[tid],/FLOAT)
  qhumanomvar=NCDF_VARDEF(wilma,'qhum_anoms',[tid],/FLOAT)
  qhumabsvar=NCDF_VARDEF(wilma,'qhum_abs',[tid],/FLOAT)
  qhumsdvar=NCDF_VARDEF(wilma,'qhum_std',[tid],/FLOAT)
  rhumanomvar=NCDF_VARDEF(wilma,'rhum_anoms',[tid],/FLOAT)
  rhumabsvar=NCDF_VARDEF(wilma,'rhum_abs',[tid],/FLOAT)
  rhumsdvar=NCDF_VARDEF(wilma,'rhum_std',[tid],/FLOAT)
  wsanomvar=NCDF_VARDEF(wilma,'ws_anoms',[tid],/FLOAT)
  wsabsvar=NCDF_VARDEF(wilma,'ws_abs',[tid],/FLOAT)
  wssdvar=NCDF_VARDEF(wilma,'ws_std',[tid],/FLOAT)
  slpanomvar=NCDF_VARDEF(wilma,'slp_anoms',[tid],/FLOAT)
  slpabsvar=NCDF_VARDEF(wilma,'slp_abs',[tid],/FLOAT)
  slpsdvar=NCDF_VARDEF(wilma,'slp_std',[tid],/FLOAT)

  dedewpabsvar=NCDF_VARDEF(wilma,'de_dewp_abs',[tid],/FLOAT)
  deddepabsvar=NCDF_VARDEF(wilma,'de_ddep_abs',[tid],/FLOAT)
  
  statPabsvar=NCDF_VARDEF(wilma,'20CRstation_Pclim',[tid],/FLOAT)

  climsvar=NCDF_VARDEF(wilma,'months',[charid,clmid],/CHAR)
  tempclimvar=NCDF_VARDEF(wilma,'temp_clims',[clmid],/FLOAT)
  dewpclimvar=NCDF_VARDEF(wilma,'dewp_clims',[clmid],/FLOAT)
  ddepclimvar=NCDF_VARDEF(wilma,'ddep_clims',[clmid],/FLOAT)
  twetclimvar=NCDF_VARDEF(wilma,'twet_clims',[clmid],/FLOAT)
  evapclimvar=NCDF_VARDEF(wilma,'evap_clims',[clmid],/FLOAT)
  qhumclimvar=NCDF_VARDEF(wilma,'qhum_clims',[clmid],/FLOAT)
  rhumclimvar=NCDF_VARDEF(wilma,'rhum_clims',[clmid],/FLOAT)
  wsclimvar=NCDF_VARDEF(wilma,'ws_clims',[clmid],/FLOAT)
  slpclimvar=NCDF_VARDEF(wilma,'slp_clims',[clmid],/FLOAT)

  NCDF_ATTPUT,wilma,'times','long_name','time'
  NCDF_ATTPUT,wilma,'times','units','months beginning Jan 1973'
  NCDF_ATTPUT,wilma,'times','axis','T'
  NCDF_ATTPUT,wilma,'times','calendar','gregorian'
  NCDF_ATTPUT,wilma,'times','valid_min',0.
  NCDF_ATTPUT,wilma,'months','long_name','month'
  NCDF_ATTPUT,wilma,'months','units','months of the year'

  NCDF_ATTPUT,wilma,'temp_anoms','long_name','Dry bulb temperature monthly mean anomaly'
  NCDF_ATTPUT,wilma,'temp_anoms','units','Degrees C'
  NCDF_ATTPUT,wilma,'temp_anoms','axis','T'
  valid=WHERE(Tanoms_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Tanoms_mm(valid))
    max_t=MAX(Tanoms_mm(valid))
    NCDF_ATTPUT,wilma,'temp_anoms','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'temp_anoms','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'temp_anoms','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'temp_abs','long_name','Dry bulb temperature monthly mean absolutes'
  NCDF_ATTPUT,wilma,'temp_abs','units','Degrees C'
  NCDF_ATTPUT,wilma,'temp_abs','axis','T'
  valid=WHERE(Tabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Tabs_mm(valid))
    max_t=MAX(Tabs_mm(valid))
    NCDF_ATTPUT,wilma,'temp_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'temp_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'temp_abs','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'temp_std','long_name','Dry bulb temperature monthly mean st dev'
  NCDF_ATTPUT,wilma,'temp_std','units','Degrees C'
  NCDF_ATTPUT,wilma,'temp_std','axis','T'
  valid=WHERE(Tsd_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Tsd_mm(valid))
    max_t=MAX(Tsd_mm(valid))
    NCDF_ATTPUT,wilma,'temp_std','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'temp_std','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'temp_std','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'temp_clims','long_name','Dry bulb temperature monthly climatology'
  NCDF_ATTPUT,wilma,'temp_clims','units','Degrees C'
  valid=WHERE(Tclims_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Tclims_mm(valid))
    max_t=MAX(Tclims_mm(valid))
    NCDF_ATTPUT,wilma,'temp_clims','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'temp_clims','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'temp_clims','missing_value',-1.e+30

  NCDF_ATTPUT,wilma,'dewp_anoms','long_name','Dewpoint Temperature monthly mean anomaly'
  NCDF_ATTPUT,wilma,'dewp_anoms','units','Degrees C'
  NCDF_ATTPUT,wilma,'dewp_anoms','axis','T'
  valid=WHERE(Tdanoms_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Tdanoms_mm(valid))
    max_t=MAX(Tdanoms_mm(valid))
    NCDF_ATTPUT,wilma,'dewp_anoms','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'dewp_anoms','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'dewp_anoms','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'dewp_abs','long_name','Dewpoint Temperature monthly mean absolutes'
  NCDF_ATTPUT,wilma,'dewp_abs','units','Degrees C'
  NCDF_ATTPUT,wilma,'dewp_abs','axis','T'
  valid=WHERE(Tdabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Tdabs_mm(valid))
    max_t=MAX(Tdabs_mm(valid))
    NCDF_ATTPUT,wilma,'dewp_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'dewp_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'dewp_abs','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'dewp_std','long_name','Dewpoint Temperature monthly mean st dev'
  NCDF_ATTPUT,wilma,'dewp_std','units','Degrees C'
  NCDF_ATTPUT,wilma,'dewp_std','axis','T'
  valid=WHERE(Tdsd_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Tdsd_mm(valid))
    max_t=MAX(Tdsd_mm(valid))
    NCDF_ATTPUT,wilma,'dewp_std','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'dewp_std','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'dewp_std','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'dewp_clims','long_name','Dewpoint Temperature monthly climatology'
  NCDF_ATTPUT,wilma,'dewp_clims','units','Degrees C'
  valid=WHERE(Tdclims_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Tdclims_mm(valid))
    max_t=MAX(Tdclims_mm(valid))
    NCDF_ATTPUT,wilma,'dewp_clims','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'dewp_clims','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'dewp_clims','missing_value',-1.e+30

  NCDF_ATTPUT,wilma,'ddep_anoms','long_name','Dewpoint Depression monthly mean anomaly'
  NCDF_ATTPUT,wilma,'ddep_anoms','units','Degrees C'
  NCDF_ATTPUT,wilma,'ddep_anoms','axis','T'
  valid=WHERE(DPDanoms_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(DPDanoms_mm(valid))
    max_t=MAX(DPDanoms_mm(valid))
    NCDF_ATTPUT,wilma,'ddep_anoms','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'ddep_anoms','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'ddep_anoms','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'ddep_abs','long_name','Dewpoint Depression monthly mean absolutes'
  NCDF_ATTPUT,wilma,'ddep_abs','units','Degrees C'
  NCDF_ATTPUT,wilma,'ddep_abs','axis','T'
  valid=WHERE(DPDabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(DPDabs_mm(valid))
    max_t=MAX(DPDabs_mm(valid))
    NCDF_ATTPUT,wilma,'ddep_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'ddep_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'ddep_abs','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'ddep_std','long_name','Dewpoint Depression monthly mean st dev'
  NCDF_ATTPUT,wilma,'ddep_std','units','Degrees C'
  NCDF_ATTPUT,wilma,'ddep_std','axis','T'
  valid=WHERE(DPDsd_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(DPDsd_mm(valid))
    max_t=MAX(DPDsd_mm(valid))
    NCDF_ATTPUT,wilma,'ddep_std','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'ddep_std','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'ddep_std','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'ddep_clims','long_name','Dewpoint Depression monthly climatology'
  NCDF_ATTPUT,wilma,'ddep_clims','units','Degrees C'
  valid=WHERE(DPDclims_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(DPDclims_mm(valid))
    max_t=MAX(DPDclims_mm(valid))
    NCDF_ATTPUT,wilma,'ddep_clims','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'ddep_clims','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'ddep_clims','missing_value',-1.e+30

  NCDF_ATTPUT,wilma,'twet_anoms','long_name','Wet-bulb Temperature monthly mean anomaly'
  NCDF_ATTPUT,wilma,'twet_anoms','units','Degrees C'
  NCDF_ATTPUT,wilma,'twet_anoms','axis','T'
  valid=WHERE(Twanoms_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Twanoms_mm(valid))
    max_t=MAX(Twanoms_mm(valid))
    NCDF_ATTPUT,wilma,'twet_anoms','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'twet_anoms','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'twet_anoms','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'twet_abs','long_name','Wet-bulb Temperature monthly mean absolutes'
  NCDF_ATTPUT,wilma,'twet_abs','units','Degrees C'
  NCDF_ATTPUT,wilma,'twet_abs','axis','T'
  valid=WHERE(Twabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Twabs_mm(valid))
    max_t=MAX(Twabs_mm(valid))
    NCDF_ATTPUT,wilma,'twet_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'twet_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'twet_abs','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'twet_std','long_name','Wet-bulb Temperature monthly mean st dev'
  NCDF_ATTPUT,wilma,'twet_std','units','Degrees C'
  NCDF_ATTPUT,wilma,'twet_std','axis','T'
  valid=WHERE(Twsd_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Twsd_mm(valid))
    max_t=MAX(Twsd_mm(valid))
    NCDF_ATTPUT,wilma,'twet_std','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'twet_std','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'twet_std','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'twet_clims','long_name','Wet-bulb Temperature monthly climatology'
  NCDF_ATTPUT,wilma,'twet_clims','units','Degrees C'
  valid=WHERE(Twclims_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Twclims_mm(valid))
    max_t=MAX(Twclims_mm(valid))
    NCDF_ATTPUT,wilma,'twet_clims','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'twet_clims','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'twet_clims','missing_value',-1.e+30

  NCDF_ATTPUT,wilma,'evap_anoms','long_name','Vapour Pressure monthly mean anomaly'
  NCDF_ATTPUT,wilma,'evap_anoms','units','hPa'
  NCDF_ATTPUT,wilma,'evap_anoms','axis','T'
  valid=WHERE(eanoms_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(eanoms_mm(valid))
    max_t=MAX(eanoms_mm(valid))
    NCDF_ATTPUT,wilma,'evap_anoms','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'evap_anoms','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'evap_anoms','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'evap_abs','long_name','Vapour Pressure monthly mean absolutes'
  NCDF_ATTPUT,wilma,'evap_abs','units','hPa'
  NCDF_ATTPUT,wilma,'evap_abs','axis','T'
  valid=WHERE(eabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(eabs_mm(valid))
    max_t=MAX(eabs_mm(valid))
    NCDF_ATTPUT,wilma,'evap_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'evap_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'evap_abs','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'evap_std','long_name','Vapour Pressure monthly mean st dev'
  NCDF_ATTPUT,wilma,'evap_std','units','hPa'
  NCDF_ATTPUT,wilma,'evap_std','axis','T'
  valid=WHERE(esd_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(esd_mm(valid))
    max_t=MAX(esd_mm(valid))
    NCDF_ATTPUT,wilma,'evap_std','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'evap_std','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'evap_std','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'evap_clims','long_name','Vapour Pressure monthly climatology'
  NCDF_ATTPUT,wilma,'evap_clims','units','hPa'
  valid=WHERE(eclims_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(eclims_mm(valid))
    max_t=MAX(eclims_mm(valid))
    NCDF_ATTPUT,wilma,'evap_clims','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'evap_clims','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'evap_clims','missing_value',-1.e+30

  NCDF_ATTPUT,wilma,'qhum_anoms','long_name','Specific Humidity monthly mean anomaly'
  NCDF_ATTPUT,wilma,'qhum_anoms','units','g/kg'
  NCDF_ATTPUT,wilma,'qhum_anoms','axis','T'
  valid=WHERE(qanoms_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(qanoms_mm(valid))
    max_t=MAX(qanoms_mm(valid))
    NCDF_ATTPUT,wilma,'qhum_anoms','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'qhum_anoms','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'qhum_anoms','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'qhum_abs','long_name','Specific Humidity monthly mean absolutes'
  NCDF_ATTPUT,wilma,'qhum_abs','units','g/kg'
  NCDF_ATTPUT,wilma,'qhum_abs','axis','T'
  valid=WHERE(qabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(qabs_mm(valid))
    max_t=MAX(qabs_mm(valid))
    NCDF_ATTPUT,wilma,'qhum_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'qhum_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'qhum_abs','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'qhum_std','long_name','Specific Humidity monthly mean st dev'
  NCDF_ATTPUT,wilma,'qhum_std','units','g/kg'
  NCDF_ATTPUT,wilma,'qhum_std','axis','T'
  valid=WHERE(qsd_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(qsd_mm(valid))
    max_t=MAX(qsd_mm(valid))
    NCDF_ATTPUT,wilma,'qhum_std','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'qhum_std','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'qhum_std','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'qhum_clims','long_name','Specific Humidity monthly climatology'
  NCDF_ATTPUT,wilma,'qhum_clims','units','g/kg'
  valid=WHERE(qclims_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(qclims_mm(valid))
    max_t=MAX(qclims_mm(valid))
    NCDF_ATTPUT,wilma,'qhum_clims','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'qhum_clims','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'qhum_clims','missing_value',-1.e+30

  NCDF_ATTPUT,wilma,'rhum_anoms','long_name','Relative Humidity monthly mean anomaly'
  NCDF_ATTPUT,wilma,'rhum_anoms','units','%'
  NCDF_ATTPUT,wilma,'rhum_anoms','axis','T'
  valid=WHERE(RHanoms_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(RHanoms_mm(valid))
    max_t=MAX(RHanoms_mm(valid))
    NCDF_ATTPUT,wilma,'rhum_anoms','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'rhum_anoms','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'rhum_anoms','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'rhum_abs','long_name','Relative Humidity monthly mean absolutes'
  NCDF_ATTPUT,wilma,'rhum_abs','units','%'
  NCDF_ATTPUT,wilma,'rhum_abs','axis','T'
  valid=WHERE(RHabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(RHabs_mm(valid))
    max_t=MAX(RHabs_mm(valid))
    NCDF_ATTPUT,wilma,'rhum_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'rhum_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'rhum_abs','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'rhum_std','long_name','Relative Humidity monthly mean st dev'
  NCDF_ATTPUT,wilma,'rhum_std','units','%'
  NCDF_ATTPUT,wilma,'rhum_std','axis','T'
  valid=WHERE(RHsd_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(RHsd_mm(valid))
    max_t=MAX(RHsd_mm(valid))
    NCDF_ATTPUT,wilma,'rhum_std','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'rhum_std','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'rhum_std','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'rhum_clims','long_name','Relative Humidity monthly climatology'
  NCDF_ATTPUT,wilma,'rhum_clims','units','%'
  valid=WHERE(RHclims_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(RHclims_mm(valid))
    max_t=MAX(RHclims_mm(valid))
    NCDF_ATTPUT,wilma,'rhum_clims','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'rhum_clims','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'rhum_clims','missing_value',-1.e+30

  NCDF_ATTPUT,wilma,'ws_anoms','long_name','Wind speed monthly mean anomaly'
  NCDF_ATTPUT,wilma,'ws_anoms','units','m s-1'
  NCDF_ATTPUT,wilma,'ws_anoms','axis','T'
  valid=WHERE(WSanoms_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(WSanoms_mm(valid))
    max_t=MAX(WSanoms_mm(valid))
    NCDF_ATTPUT,wilma,'ws_anoms','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'ws_anoms','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'ws_anoms','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'ws_abs','long_name','Wind speed monthly mean absolutes'
  NCDF_ATTPUT,wilma,'ws_abs','units','m s-1'
  NCDF_ATTPUT,wilma,'ws_abs','axis','T'
  valid=WHERE(WSabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(WSabs_mm(valid))
    max_t=MAX(WSabs_mm(valid))
    NCDF_ATTPUT,wilma,'ws_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'ws_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'ws_abs','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'ws_std','long_name','Wind speed monthly mean st dev'
  NCDF_ATTPUT,wilma,'ws_std','units','m s-1'
  NCDF_ATTPUT,wilma,'ws_std','axis','T'
  valid=WHERE(WSsd_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(WSsd_mm(valid))
    max_t=MAX(WSsd_mm(valid))
    NCDF_ATTPUT,wilma,'ws_std','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'ws_std','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'ws_std','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'ws_clims','long_name','Wind speed monthly climatology'
  NCDF_ATTPUT,wilma,'ws_clims','units','m s-1'
  valid=WHERE(WSclims_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(WSclims_mm(valid))
    max_t=MAX(WSclims_mm(valid))
    NCDF_ATTPUT,wilma,'ws_clims','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'ws_clims','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'ws_clims','missing_value',-1.e+30

  NCDF_ATTPUT,wilma,'slp_anoms','long_name','Station level pressure monthly mean anomaly'
  NCDF_ATTPUT,wilma,'slp_anoms','units','hPa'
  NCDF_ATTPUT,wilma,'slp_anoms','axis','T'
  valid=WHERE(SLPanoms_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(SLPanoms_mm(valid))
    max_t=MAX(SLPanoms_mm(valid))
    NCDF_ATTPUT,wilma,'slp_anoms','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'slp_anoms','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'slp_anoms','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'slp_abs','long_name','Station level pressure monthly mean absolutes'
  NCDF_ATTPUT,wilma,'slp_abs','units','hPa'
  NCDF_ATTPUT,wilma,'slp_abs','axis','T'
  valid=WHERE(SLPabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(SLPabs_mm(valid))
    max_t=MAX(SLPabs_mm(valid))
    NCDF_ATTPUT,wilma,'slp_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'slp_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'slp_abs','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'slp_std','long_name','Station level pressure monthly mean st dev'
  NCDF_ATTPUT,wilma,'slp_std','units','hPa'
  NCDF_ATTPUT,wilma,'slp_std','axis','T'
  valid=WHERE(SLPsd_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(SLPsd_mm(valid))
    max_t=MAX(SLPsd_mm(valid))
    NCDF_ATTPUT,wilma,'slp_std','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'slp_std','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'slp_std','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'slp_clims','long_name','Station level pressure monthly climatology'
  NCDF_ATTPUT,wilma,'slp_clims','units','hPa'
  valid=WHERE(SLPclims_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(SLPclims_mm(valid))
    max_t=MAX(SLPclims_mm(valid))
    NCDF_ATTPUT,wilma,'slp_clims','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'slp_clims','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'slp_clims','missing_value',-1.e+30

  NCDF_ATTPUT,wilma,'20CRstation_Pclim','long_name','Monthly Climatological (76-05) station pressure'
  NCDF_ATTPUT,wilma,'20CRstation_Pclim','units','hPa'
  NCDF_ATTPUT,wilma,'20CRstation_Pclim','axis','T'
  valid=WHERE(Pabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(Pabs_mm(valid))
    max_t=MAX(Pabs_mm(valid))
    NCDF_ATTPUT,wilma,'20CRstation_Pclim','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'20CRstation_Pclim','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'20CRstation_Pclim','missing_value',-1.e+30

  NCDF_ATTPUT,wilma,'de_dewp_abs','long_name','Derived Dewpoint Temperature monthly mean absolutes'
  NCDF_ATTPUT,wilma,'de_dewp_abs','units','Degrees C'
  NCDF_ATTPUT,wilma,'de_dewp_abs','axis','T'
  valid=WHERE(derivedTdabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(derivedTdabs_mm(valid))
    max_t=MAX(derivedTdabs_mm(valid))
    NCDF_ATTPUT,wilma,'de_dewp_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'de_dewp_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'de_dewp_abs','missing_value',-1.e+30
  NCDF_ATTPUT,wilma,'de_ddep_abs','long_name','Derived Dewpoint Depression monthly mean absolutes'
  NCDF_ATTPUT,wilma,'de_ddep_abs','units','Degrees C'
  NCDF_ATTPUT,wilma,'de_ddep_abs','axis','T'
  valid=WHERE(derivedDPDabs_mm NE -1.E+30, tc)
  IF tc GE 1 THEN BEGIN
    min_t=MIN(derivedDPDabs_mm(valid))
    max_t=MAX(derivedDPDabs_mm(valid))
    NCDF_ATTPUT,wilma,'de_ddep_abs','valid_min',min_t(0)
    NCDF_ATTPUT,wilma,'de_ddep_abs','valid_max',max_t(0)
  ENDIF
  NCDF_ATTPUT,wilma,'ddep_abs','missing_value',-1.e+30

 NCDF_ATTPUT,wilma,/GLOBAL,'station_information','Where station is a composite the station id refers to the primary source used in the timestep and may not apply to all elements'
  current_time=SYSTIME()
  ;PRINT,current_time
  NCDF_ATTPUT,wilma,/GLOBAL,'file_created',STRING(current_time)
  NCDF_CONTROL,wilma,/ENDEF
  
  NCDF_VARPUT, wilma,timesvar, int_mons
  NCDF_VARPUT, wilma,tempanomvar,Tanoms_mm
  NCDF_VARPUT, wilma,tempabsvar,Tabs_mm
  NCDF_VARPUT, wilma,tempsdvar,Tsd_mm
  NCDF_VARPUT, wilma,dewpanomvar,Tdanoms_mm
  NCDF_VARPUT, wilma,dewpabsvar,Tdabs_mm
  NCDF_VARPUT, wilma,dewpsdvar,Tdsd_mm
  NCDF_VARPUT, wilma,ddepanomvar,DPDanoms_mm
  NCDF_VARPUT, wilma,ddepabsvar,DPDabs_mm
  NCDF_VARPUT, wilma,ddepsdvar,DPDsd_mm
  NCDF_VARPUT, wilma,twetanomvar,Twanoms_mm
  NCDF_VARPUT, wilma,twetabsvar,Twabs_mm
  NCDF_VARPUT, wilma,twetsdvar,Twsd_mm
  NCDF_VARPUT, wilma,evapanomvar,eanoms_mm
  NCDF_VARPUT, wilma,evapabsvar,eabs_mm
  NCDF_VARPUT, wilma,evapsdvar,esd_mm
  NCDF_VARPUT, wilma,qhumanomvar,qanoms_mm
  NCDF_VARPUT, wilma,qhumabsvar,qabs_mm
  NCDF_VARPUT, wilma,qhumsdvar,qsd_mm
  NCDF_VARPUT, wilma,rhumanomvar,RHanoms_mm
  NCDF_VARPUT, wilma,rhumabsvar,RHabs_mm
  NCDF_VARPUT, wilma,rhumsdvar,RHsd_mm
  NCDF_VARPUT, wilma,wsanomvar,WSanoms_mm
  NCDF_VARPUT, wilma,wsabsvar,WSabs_mm
  NCDF_VARPUT, wilma,wssdvar,WSsd_mm
  NCDF_VARPUT, wilma,slpanomvar,SLPanoms_mm
  NCDF_VARPUT, wilma,slpabsvar,SLPabs_mm
  NCDF_VARPUT, wilma,slpsdvar,SLPsd_mm
  NCDF_VARPUT, wilma,statPabsvar,Pabs_mm

  NCDF_VARPUT, wilma,climsvar,monarr
  NCDF_VARPUT, wilma,tempclimvar,Tclims_mm
  NCDF_VARPUT, wilma,dewpclimvar,Tdclims_mm
  NCDF_VARPUT, wilma,ddepclimvar,DPDclims_mm
  NCDF_VARPUT, wilma,twetclimvar,Twclims_mm
  NCDF_VARPUT, wilma,evapclimvar,eclims_mm
  NCDF_VARPUT, wilma,qhumclimvar,qclims_mm
  NCDF_VARPUT, wilma,rhumclimvar,RHclims_mm
  NCDF_VARPUT, wilma,wsclimvar,WSclims_mm
  NCDF_VARPUT, wilma,slpclimvar,SLPclims_mm

  NCDF_VARPUT, wilma,dedewpabsvar,derivedTdabs_mm
  NCDF_VARPUT, wilma,deddepabsvar,derivedDPDabs_mm
  
  NCDF_CLOSE,wilma

  asciiRAW_outfileq=outdirRAWq+strmid(stationid,0,6)+strmid(stationid,7,5)+'.raw.tavg'
  asciiRAW_outfilee=outdirRAWe+strmid(stationid,0,6)+strmid(stationid,7,5)+'.raw.tavg'
  asciiRAW_outfileRH=outdirRAWRH+strmid(stationid,0,6)+strmid(stationid,7,5)+'.raw.tavg'
  asciiRAW_outfileT=outdirRAWT+strmid(stationid,0,6)+strmid(stationid,7,5)+'.raw.tavg'
  asciiRAW_outfileTw=outdirRAWTw+strmid(stationid,0,6)+strmid(stationid,7,5)+'.raw.tavg'
  asciiRAW_outfileDPD=outdirRAWDPD+strmid(stationid,0,6)+strmid(stationid,7,5)+'.raw.tavg'
  asciiRAW_outfileTd=outdirRAWTd+strmid(stationid,0,6)+strmid(stationid,7,5)+'.raw.tavg'
  asciiRAW_outfileSLP=outdirRAWslp+strmid(stationid,0,6)+strmid(stationid,7,5)+'.raw.tavg'
  asciiRAW_outfileWS=outdirRAWws+strmid(stationid,0,6)+strmid(stationid,7,5)+'.raw.tavg'

  asciiANOM_outfileT=outdirASC+'TANOMS/'+stationid+'_TmonthQCanoms.raw'
  asciiANOM_outfileTd=outdirASC+'TDANOMS/'+stationid+'_TdmonthQCanoms.raw'
  asciiANOM_outfileDPD=outdirASC+'DPDANOMS/'+stationid+'_DPDmonthQCanoms.raw'
  asciiANOM_outfileTw=outdirASC+'TWANOMS/'+stationid+'_TwmonthQCanoms.raw'
  asciiANOM_outfilee=outdirASC+'EANOMS/'+stationid+'_emonthQCanoms.raw'
  asciiANOM_outfileq=outdirASC+'QANOMS/'+stationid+'_qmonthQCanoms.raw'
  asciiANOM_outfileRH=outdirASC+'RHANOMS/'+stationid+'_RHmonthQCanoms.raw'
  asciiANOM_outfileWS=outdirASC+'WSANOMS/'+stationid+'_WSmonthQCanoms.raw'
  asciiANOM_outfileSLP=outdirASC+'SLPANOMS/'+stationid+'_SLPmonthQCanoms.raw'

  asciiABS_outfileT=outdirASC+'TABS/'+stationid+'_TmonthQCabs.raw'
  asciiABS_outfileTd=outdirASC+'TDABS/'+stationid+'_TdmonthQCabs.raw'
  asciiABS_outfileDPD=outdirASC+'DPDABS/'+stationid+'_DPDmonthQCabs.raw'
  asciiABS_outfiledeTd=outdirASC+'derivedTDABS/'+stationid+'_deTdmonthQCabs.raw'
  asciiABS_outfiledeDPD=outdirASC+'derivedDPDABS/'+stationid+'_deDPDmonthQCabs.raw'
  asciiABS_outfileTw=outdirASC+'TWABS/'+stationid+'_TwmonthQCabs.raw'
  asciiABS_outfilee=outdirASC+'EABS/'+stationid+'_emonthQCabs.raw'
  asciiABS_outfileq=outdirASC+'QABS/'+stationid+'_qmonthQCabs.raw'
  asciiABS_outfileRH=outdirASC+'RHABS/'+stationid+'_RHmonthQCabs.raw'
  asciiABS_outfileWS=outdirASC+'WSABS/'+stationid+'_WSmonthQCabs.raw'
  asciiABS_outfileSLP=outdirASC+'SLPABS/'+stationid+'_SLPmonthQCabs.raw'
  
  Tanoms_mm=REFORM(Tanoms_mm,12,nyrs)
  Tdanoms_mm=REFORM(Tdanoms_mm,12,nyrs)
  DPDanoms_mm=REFORM(DPDanoms_mm,12,nyrs)
  Twanoms_mm=REFORM(Twanoms_mm,12,nyrs)
  eanoms_mm=REFORM(eanoms_mm,12,nyrs)
  qanoms_mm=REFORM(qanoms_mm,12,nyrs)
  RHanoms_mm=REFORM(RHanoms_mm,12,nyrs)
  WSanoms_mm=REFORM(WSanoms_mm,12,nyrs)
  SLPanoms_mm=REFORM(SLPanoms_mm,12,nyrs)
  
  Tabs_mm=REFORM(Tabs_mm,12,nyrs)
  Tdabs_mm=REFORM(Tdabs_mm,12,nyrs)
  DPDabs_mm=REFORM(DPDabs_mm,12,nyrs)
  derivedTdabs_mm=REFORM(derivedTdabs_mm,12,nyrs)
  derivedDPDabs_mm=REFORM(derivedDPDabs_mm,12,nyrs)
  Twabs_mm=REFORM(Twabs_mm,12,nyrs)
  eabs_mm=REFORM(eabs_mm,12,nyrs)
  qabs_mm=REFORM(qabs_mm,12,nyrs)
  qsatabs_mm=REFORM(qsatabs_mm,12,nyrs)
  RHabs_mm=REFORM(RHabs_mm,12,nyrs)
  WSabs_mm=REFORM(WSabs_mm,12,nyrs)
  SLPabs_mm=REFORM(SLPabs_mm,12,nyrs)
  
  ;change mdi to -9999 and multiply values by 10 - round whole number
  gots=WHERE(qanoms_mm NE mdi,cgots)
  miss=WHERE(qanoms_mm EQ mdi,cmiss)	; these should map to all other variables
  ; *** POSSIBLE THE qanom mapping is different from qabs and RHabs etc - so <15 months may have been passed by abs but failed by anoms
  ; good to mask out where bad for anoms but then this will fail later
  IF (cmiss GT 0) THEN BEGIN
    Tanoms_mm(miss)=-9999
    Tdanoms_mm(miss)=-9999
    DPDanoms_mm(miss)=-9999
    Twanoms_mm(miss)=-9999
    eanoms_mm(miss)=-9999
    qanoms_mm(miss)=-9999
    RHanoms_mm(miss)=-9999
    WSanoms_mm(miss)=-9999
    SLPanoms_mm(miss)=-9999
    Tabs_mm(miss)=-9999
    Tdabs_mm(miss)=-9999
    DPDabs_mm(miss)=-9999
    derivedTdabs_mm(miss)=-9999
    derivedDPDabs_mm(miss)=-9999
    Twabs_mm(miss)=-9999
    eabs_mm(miss)=-9999
    qabs_mm(miss)=-9999
    qsatabs_mm(miss)=-9999
    RHabs_mm(miss)=-9999
    WSabs_mm(miss)=-9999
    SLPabs_mm(miss)=-9999
  ENDIF
  IF (cgots GT 200) THEN BEGIN	; if there aren't at least 200 months then ditch the station - save to ditchfile
    Tanoms_mm(gots)=ROUND(Tanoms_mm(gots)*100.)
    Tdanoms_mm(gots)=ROUND(Tdanoms_mm(gots)*100.)
    DPDanoms_mm(gots)=ROUND(DPDanoms_mm(gots)*100.)
    Twanoms_mm(gots)=ROUND(Twanoms_mm(gots)*100.)
    eanoms_mm(gots)=ROUND(eanoms_mm(gots)*100.)
    qanoms_mm(gots)=ROUND(qanoms_mm(gots)*100.)
    RHanoms_mm(gots)=ROUND(RHanoms_mm(gots)*100.)
    WSanoms_mm(gots)=ROUND(WSanoms_mm(gots)*100.)
    SLPanoms_mm(gots)=ROUND(SLPanoms_mm(gots)*100.)

    Tabs_mm(gots)=ROUND(Tabs_mm(gots)*100.)
    Tdabs_mm(gots)=ROUND(Tdabs_mm(gots)*100.)
    DPDabs_mm(gots)=ROUND(DPDabs_mm(gots)*100.)
    derivedTdabs_mm(gots)=ROUND(derivedTdabs_mm(gots)*100.)
    derivedDPDabs_mm(gots)=ROUND(derivedDPDabs_mm(gots)*100.)
    Twabs_mm(gots)=ROUND(Twabs_mm(gots)*100.)
    eabs_mm(gots)=ROUND(eabs_mm(gots)*100.)
    qabs_mm(gots)=ROUND(qabs_mm(gots)*100.)
    qsatabs_mm(gots)=ROUND(qsatabs_mm(gots)*100.)
    RHabs_mm(gots)=ROUND(RHabs_mm(gots)*100.)
    WSabs_mm(gots)=ROUND(WSabs_mm(gots)*100.)
    SLPabs_mm(gots)=ROUND(SLPabs_mm(gots)*100.)
  ENDIF ELSE BEGIN
    openw,99,ditchfile,/append
    printf,99,stationid,'MONTHS: ',cgots,format='(a12,x,a8,i4)'
    close,99
    print,'Too small, moving on...'
    continue
  ENDELSE

  openw,6,asciiANOM_outfileT
  openw,7,asciiANOM_outfileTd
  openw,8,asciiANOM_outfileTw
  openw,9,asciiANOM_outfilee
  openw,10,asciiANOM_outfileq
  openw,11,asciiANOM_outfileRH
  openw,12,asciiANOM_outfileDPD
  openw,13,asciiANOM_outfileWS
  openw,14,asciiANOM_outfileSLP

  openw,26,asciiABS_outfileT
  openw,27,asciiABS_outfileTd
  openw,28,asciiABS_outfileTw
  openw,29,asciiABS_outfilee
  openw,30,asciiABS_outfileq
  openw,31,asciiABS_outfileRH
  openw,32,asciiABS_outfileDPD
  openw,33,asciiABS_outfiledeTd
  openw,34,asciiABS_outfiledeDPD
  openw,35,asciiABS_outfileWS
  openw,36,asciiABS_outfileSLP

  openw,76,asciiRAW_outfileT
  openw,77,asciiRAW_outfileDPD
  openw,78,asciiRAW_outfileTw
  openw,79,asciiRAW_outfilee
  openw,80,asciiRAW_outfileq
  openw,81,asciiRAW_outfileRH
  openw,82,asciiRAW_outfileTd
  openw,83,asciiRAW_outfileWS
  openw,84,asciiRAW_outfileSLP
  
  FOR yy=styear,edyear DO BEGIN
    printf,76,wmoid,wbanid,strcompress(yy,/remove_all),Tabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,77,wmoid,wbanid,strcompress(yy,/remove_all),derivedDPDabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,78,wmoid,wbanid,strcompress(yy,/remove_all),Twabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,79,wmoid,wbanid,strcompress(yy,/remove_all),eabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,80,wmoid,wbanid,strcompress(yy,/remove_all),qabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,81,wmoid,wbanid,strcompress(yy,/remove_all),RHabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,82,wmoid,wbanid,strcompress(yy,/remove_all),Tdabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,83,wmoid,wbanid,strcompress(yy,/remove_all),WSabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,84,wmoid,wbanid,strcompress(yy,/remove_all),SLPabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    
    printf,6,wmoid,wbanid,strcompress(yy,/remove_all),Tanoms_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,7,wmoid,wbanid,strcompress(yy,/remove_all),Tdanoms_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,8,wmoid,wbanid,strcompress(yy,/remove_all),Twanoms_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,9,wmoid,wbanid,strcompress(yy,/remove_all),eanoms_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,10,wmoid,wbanid,strcompress(yy,/remove_all),qanoms_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,11,wmoid,wbanid,strcompress(yy,/remove_all),RHanoms_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,12,wmoid,wbanid,strcompress(yy,/remove_all),DPDanoms_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,13,wmoid,wbanid,strcompress(yy,/remove_all),WSanoms_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,14,wmoid,wbanid,strcompress(yy,/remove_all),SLPanoms_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'

    printf,26,wmoid,wbanid,strcompress(yy,/remove_all),Tabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,27,wmoid,wbanid,strcompress(yy,/remove_all),Tdabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,28,wmoid,wbanid,strcompress(yy,/remove_all),Twabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,29,wmoid,wbanid,strcompress(yy,/remove_all),eabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,30,wmoid,wbanid,strcompress(yy,/remove_all),qabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,31,wmoid,wbanid,strcompress(yy,/remove_all),RHabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,32,wmoid,wbanid,strcompress(yy,/remove_all),DPDabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,33,wmoid,wbanid,strcompress(yy,/remove_all),derivedTdabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,34,wmoid,wbanid,strcompress(yy,/remove_all),derivedDPDabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,35,wmoid,wbanid,strcompress(yy,/remove_all),WSabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
    printf,36,wmoid,wbanid,strcompress(yy,/remove_all),SLPabs_mm(*,yy-styear),format='(a6,a5,x,a4,12(i6,3x))'
  ENDFOR
  
  close,6
  close,7
  close,8
  close,9
  close,10
  close,11
  close,12
  close,13
  close,14

  close,26
  close,27
  close,28
  close,29
  close,30
  close,31
  close,32
  close,33
  close,34
  close,35
  close,36
  
  close,76
  close,77
  close,78
  close,79
  close,80
  close,81
  close,82
  close,83
  close,84
  
  openw,99,keepfile,/append
    printf,99,wmoid,wbanid,lat,lon,stationelv,cid,namoo,'MONTHS: ',cgots,format='(a6,a5,f8.4,x,f9.4,x,f6.1,x,a2,x,a29,x,a8,i4)'
  close,99

ENDWHILE
close,5
END
