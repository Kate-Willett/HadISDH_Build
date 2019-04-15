; NOW REDUNDANT BECAUSE WE HAVE make_area_avg_ts.py in PROGS/PYTHON

; TIDL
; 
; Author: Kate Willett
; Created: 1 February 2013
; Last update: 24 January 2019
; Location: /data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/HADISDH_BUILD/	
; GitHub: https://github.com/Kate-Willett/HadISDH_Build					
; -----------------------
; CODE PURPOSE AND OUTPUT
; -----------------------
; This code reads in monthly mean gridded (5by5) netCDF files and produces area average time series
; in netCDF and ASCII
; 
; <references to related published material, e.g. that describes data set>
; 
; -----------------------
; LIST OF MODULES
; -----------------------
; <List of program modules required to run the code, or link to compiler/batch file>
; 
; -----------------------
; DATA
; -----------------------
; HadISDH-land:
; /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/GRIDS/
; HadISDH.landq.3.0.0.2016p_FLATgridIDPHA5by5_anoms7605_JAN2017_cf.nc
; HadISDH-marine
; /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/GRIDS/
; HadISDH.marineq.1.0.0.2016p_OBSclim2BClocal_anoms8110_JAN2017_cf.nc
; HadISDH.marineq.1.0.0.2016p_OBSclim2BClocalship_anoms8110_JAN2017_cf.nc
; HadISDH-blend:
; /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/GRIDS/
; HadISDH.blendq.1.0.0.2016p_FULL_anoms8110_JAN2017_cf.nc
; HadISDH.blendq.1.0.0.2016p_FULLship_anoms8110_JAN2017_cf.nc
; Other:
; 
; -----------------------
; HOW TO RUN THE CODE
; -----------------------
; Make sure all of the EDITABLES are correct
; > tidl
; > .compile make_area_avg_ts
; > make_area_avg_ts,param,homogtype
; *** CHOOSE PARAMETER ***
;param =      'q'	;'dpd','td','t','tw','e','q','rh','w','evap'
; *** CHOOSE TYPE OF DATA ***
;homogtype =  'MARINEship'	;'PHA','ID','DPD', 'RAW', 'OTHER', 'BLEND','BLENDship','MARINE','MARINEship','ERA' 
;
; -----------------------
; OUTPUT
; -----------------------
; /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/TIMESERIES/
; HadISDH.landq.3.0.0.2016p_FLATgridIDPHA5by5_anoms7605_JAN2017_areaTS_19732016.nc
; HadISDH.blendq.1.0.0.2016p_FULL_anoms8110_JAN2017_areaTS_19732016.nc
; HadISDH.blendq.1.0.0.2016p_FULLship_anoms8110_JAN2017_areaTS_19732016.nc
; HadISDH.marineq.1.0.0.2016p_OBSclim2BClocal_anoms8110_JAN2017_areaTS_19732016.nc
; HadISDH.marineq.1.0.0.2016p_OBSclim2BClocalship_anoms8110_JAN2017_areaTS_19732016.nc
; 
; -----------------------
; VERSION/RELEASE NOTES
; -----------------------
; Version 3 (14 February 2018)
; ---------
;  
; Enhancements
; Automatically puts the styredyr string into the ERA filenames
;
; Changes
;  
; Bug fixes
;
;
; Version 3 (14 February 2018)
; ---------
;  
; Enhancements
; Now call variable and runtype from command line
; *** CHOOSE PARAMETER ***
;param =      'q'	;'dpd','td','t','tw','e','q','rh','w','evap'
; *** CHOOSE TYPE OF DATA ***
;homogtype =  'MARINEship'	;'PHA','ID','DPD', 'RAW', 'OTHER', 'BLEND','BLENDship','MARINE','MARINEship','ERA'
;
; Changes
;  
; Bug fixes
; 
; Version 2 (2 August 2016)
; ---------
;  
; Enhancements
; Can now work with updated marine and blended versions
;  
; Changes
;  
; Bug fixes
;
; Version 2 (2 August 2016)
; ---------
;  
; Enhancements
; Can now work with ERA data
; Can now work with actuals or anomalies
; Can mask with HadISDH land, HadISDH marine (when it exists, HadISDH blend
; (when it exists)
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


pro make_area_avg_ts,param,homogtype
;; *** CHOOSE PARAMETER ***
;param =      'q'	;'dpd','td','t','tw','e','q','rh','w','evap'
;
;; *** CHOOSE TYPE OF DATA ***
;homogtype =  'MARINEship'	;'PHA','ID','DPD', 'RAW', 'OTHER', 'BLEND','BLENDship','MARINE','MARINEship','ERA'

; to calculate area average - NO missing data tolerance - need a land/sea mask for that

;based on kate_timeseries.pro - WAVE for ICOADS

; written by Kate Willett
; last modified JUL 2012

;---------------------------------------------------
; EDITABLES set up directories and filenames
mdi =        -1e+30

; *** CHOOSE CANDIDATE set up values
styr =       1973	; 1850, 1973, 1950, 1880, 1979
edyr =       2018	; 
datestring = strcompress(styr,/remove_all)+strcompress(edyr,/remove_all)
climst =     1981	; 1976 or 1981
climed =     2010	; 2005 or 2010

; *** CHOOSE READ IN DATE ***
thenmon =     'FEB'
thenyear =    '2019'

; *** CHOOSE PRINT OUT DATE ***
nowmon =     'FEB'
nowyear =    '2019'

;; *** CHOOSE PARAMETER ***
;param =      'q'	;'dpd','td','t','tw','e','q','rh','w','evap';
;
;; *** CHOOSE TYPE OF DATA ***
;homogtype =  'MARINEship'	;'PHA','ID','DPD', 'RAW', 'OTHER', 'BLEND','BLENDship','MARINE','MARINEship','ERA'

; *** CHOOSE VERSION IF HadISDH ***
version =    '1.0.0.2018f' ; 4.1.0.2018f 1.0.0.2018f

; *** CHOOSE WORKING DIRECTORY ***
workingdir = 'UPDATE20'+strmid(strcompress(edyr,/remove_all),2,2)

; *** CHOOSE WHETHER TO MASK WITH HadISDH IF NOT HadISDH ***
mask =       'false'	; default = 'false', if 'true' then mask to HadISDH equivalent
; MASKFILE (HadISDH set up values)
mstyr =       1973	; 1850, 1973, 1950, 1880
medyr =       2016	; 2013, 2011
mclimst =     1981	; could be 1976 or 1981
mclimed =     2010	; could be 2005 or 2010

; *** CHOOSE WHETHER TO SUB-SELECT A DOMAIN IF NOT HADISDH ***
domain =     'marine'	; 'land','marine','blend'

; *** CHOOSE WHETHER TO WORK WITH ANOMALIES OR ACTUALS - COULD ADD RENORMALISATION IF DESIRED ***
isanom =     'true'	; 'false' for actual values, 'true' for anomalies

; *** Might add a renormalisation section later ***
; renorm = 'false'



CLMlab =     strmid(strcompress(climst,/remove_all),2,2)+strmid(strcompress(climed,/remove_all),2,2)
climchoice = 'anoms'+CLMlab ; 'anoms7605','anoms8110'

MCLMlab =     strmid(strcompress(mclimst,/remove_all),2,2)+strmid(strcompress(mclimed,/remove_all),2,2)
mclimchoice = 'anoms'+MCLMlab ; 'anoms7605','anoms8110'

print,' ARE YOU HAPPY WITH YOUR CHOICES OF YEARS?'
print,styr,edyr, climst, climed
stop

IF ((mask EQ 'true') AND (mclimchoice NE climchoice)) THEN BEGIN
  print,'Oy - your climatology periods are different between your candidate and mask!'
  print, 'Type .c for continue or fix it!'
  stop
ENDIF  

; Latitude and longitude gridbox width
latlg = 5.	;5., 4.
lonlg = 5. 	;5., 4.
  
IF (homogtype EQ 'OTHER') OR (homogtype EQ 'ERA') THEN $
  dir =   '/data/local/hadkw/HADCRUH2/'+workingdir+'/OTHERDATA/' ELSE $
  dir =   '/data/local/hadkw/HADCRUH2/'+workingdir+'/STATISTICS/'
    
maskdir = '/data/local/hadkw/HADCRUH2/'+workingdir+'/STATISTICS/GRIDS/'
odir =    '/data/local/hadkw/HADCRUH2/'+workingdir+'/STATISTICS/TIMESERIES/'

CASE param OF
  'evap': BEGIN
    param2 =    'evap'	
    infile =    'evap_monthly_5by5_ERA-Interim_data_19792015_anoms1981-2010'
    maskfileL = maskdir+'HadISDH.landq.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear
  END
  'dpd': BEGIN
    param2 = 'DPD'	
    IF (homogtype EQ 'PHA')    THEN infile = 'HadISDH.landDPD.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'RAW')    THEN infile = 'HadISDH.landDPD.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLEND')  THEN infile = 'HadISDH.blendDPD.'+version+'_FULL_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineDPD.'+version+'_BClocal5by5both_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLENDship')  THEN infile = 'HadISDH.blendDPD.'+version+'_FULLship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineDPD.'+version+'_BClocalSHIP5by5both_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'ERA') THEN BEGIN
      CASE isanom OF
	'true': BEGIN
	  IF (climchoice EQ 'anoms7605') OR (climchoice EQ 'anoms7905') THEN $
	    infile =  'dpd2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1979-2005' ELSE $
	    infile =  'dpd2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1981-2010'
	END
	'false': infile = 'dpd2m_monthly_5by5_ERA-Interim_data_'+datestring
      ENDCASE
    ENDIF
    maskfileL = maskdir+'HadISDH.landDPD.'+version+'_FLATgridPHA5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileM = maskdir+'HadISDH.marineDPD.'+version+'_BClocalSHIP5by5both_'+mclimchoice+'_'+thenmon+thenyear
    maskfileB = maskdir+'HadISDH.DPD.'+version+'_FLATgridPHABClocalSHIPboth5by5_'+mclimchoice+'_'+thenmon+thenyear
  END
  'td': BEGIN
   param2 = 'Td'	
    IF (homogtype EQ 'PHA')    THEN infile = 'HadISDH.landTd.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'DPD')    THEN infile = 'HadISDH.landTd.'+version+'_FLATgridPHADPD5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'RAW')    THEN infile = 'HadISDH.landTd.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLEND')  THEN infile = 'HadISDH.blendTd.'+version+'_FULL_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineTd.'+version+'_OBSclim2BClocal_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLENDship')  THEN infile = 'HadISDH.blendTd.'+version+'_FULLship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineTd.'+version+'_OBSclim2BClocalship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'ERA') THEN BEGIN
      CASE isanom OF
	'true': BEGIN
	  IF (climchoice EQ 'anoms7605') OR (climchoice EQ 'anoms7905') THEN $
	    infile = 'td2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1979-2005' ELSE $
	    infile = 'td2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1981-2010'
	END
	'false': infile = 'td2m_monthly_5by5_ERA-Interim_data_'+datestring
      ENDCASE
    ENDIF
    maskfileL = maskdir+'HadISDH.landTd.'+version+'_FLATgridPHADPD5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileM = maskdir+'HadISDH.marineTd.'+version+'_FLATgrid5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileB = maskdir+'GRIDS/HadISDH.Td.'+version+'_FLATgridPHA5by5_'+mclimchoice+'_'+thenmon+thenyear
  END
  't': BEGIN
   param2 = 'T'	
    IF (homogtype EQ 'ID')     THEN infile = 'HadISDH.landT.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'RAW')    THEN infile = 'HadISDH.landT.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear
;    IF (homogtype EQ 'OTHER')  THEN infile = 'HadCRUT.4.3.0.0.median'
;    IF (homogtype EQ 'OTHER')  THEN infile = 'HadSST.3.1.1.0.median'
    IF (homogtype EQ 'OTHER')  THEN infile = 'CRUTEM.4.3.0.0.anomalies'
;    IF (homogtype EQ 'OTHER')  THEN infile = 'GHCNM_18802014'
    IF (homogtype EQ 'BLEND')  THEN infile = 'HadISDH.blendT.'+version+'_FULL_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineT.'+version+'_OBSclim2BClocal_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLENDship')  THEN infile = 'HadISDH.blendT.'+version+'_FULLship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineT.'+version+'_OBSclim2BClocalship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'ERA') THEN BEGIN
      CASE isanom OF
	'true': BEGIN
	  IF (climchoice EQ 'anoms7605') OR (climchoice EQ 'anoms7905') THEN $
	    infile = 't2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1979-2005' ELSE $
	    infile = 't2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1981-2010'
	END
	'false': infile = 't2m_monthly_5by5_ERA-Interim_data_'+datestring
      ENDCASE
    ENDIF
    maskfileL = maskdir+'HadISDH.landT.'+version+'_FLATgridIDPHA5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileM = maskdir+'HadISDH.marineT.'+version+'_FLATgrid5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileB = maskdir+'HadISDH.T.'+version+'_FLATgridPHA5by5_'+mclimchoice+'_'+thenmon+thenyear
  END
  'tw': BEGIN
   param2 = 'Tw'	
    IF (homogtype EQ 'ID')     THEN infile = 'HadISDH.landTw.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'RAW')    THEN infile = 'HadISDH.landTw.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLEND')  THEN infile = 'HadISDH.blendTw.'+version+'_FULL_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineTw.'+version+'_OBSclim2BClocal_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLENDship')  THEN infile = 'HadISDH.blendTw.'+version+'_FULLship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineTw.'+version+'_OBSclim2BClocalship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'ERA') THEN BEGIN
      CASE isanom OF
	'true': BEGIN 
	  IF (climchoice EQ 'anoms7605') OR (climchoice EQ 'anoms7905') THEN $
            infile = 'tw2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1979-2005'
	    infile = 'tw2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1981-2010'
	END
	'false': infile = 'tw2m_monthly_5by5_ERA-Interim_data_'+datestring
      ENDCASE
    ENDIF
    maskfileL = maskdir+'HadISDH.landTw.'+version+'_FLATgridIDPHA5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileM = maskdir+'HadISDH.marineTw.'+version+'_FLATgrid5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileB = maskdir+'HadISDH.Tw.'+version+'_FLATgridPHA5by5_'+mclimchoice+'_'+thenmon+thenyear
  END
  'q': BEGIN
   param2 = 'q'
    IF (homogtype EQ 'ID')     THEN infile = 'HadISDH.landq.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'PHA')    THEN infile = 'HadISDH.landq.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'RAW')    THEN infile = 'HadISDH.landq.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLEND')  THEN infile = 'HadISDH.blendq.'+version+'_FULL_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineq.'+version+'_BClocal5by5both_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLENDship')  THEN infile = 'HadISDH.blendq.'+version+'_FULLship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineq.'+version+'_BClocalSHIP5by5both_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'ERA') THEN BEGIN
      CASE isanom OF
	'true': BEGIN 
	  IF (climchoice EQ 'anoms7605') OR (climchoice EQ 'anoms7905') THEN $
            infile = 'q2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1979-2005' ELSE $
	    infile = 'q2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1981-2010'
	END
	'false': infile = 'q2m_monthly_5by5_ERA-Interim_data_'+datestring
      ENDCASE
    ENDIF
    maskfileL = maskdir+'HadISDH.landq.'+version+'_FLATgridIDPHA5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileM = maskdir+'HadISDH.marineq.'+version+'_BClocalSHIPboth5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileB = maskdir+'HadISDH.q.'+version+'_FLATgridIDPHABClocalSHIPboth5by5_'+mclimchoice+'_'+thenmon+thenyear
  END
  'e': BEGIN
   param2 = 'e'	
    IF (homogtype EQ 'ID')     THEN infile = 'HadISDH.lande.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'RAW')    THEN infile = 'HadISDH.lande.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLEND')  THEN infile = 'HadISDH.blende.'+version+'_FULL_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marinee.'+version+'_OBSclim2BClocal_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLENDship')  THEN infile = 'HadISDH.blende.'+version+'_FULLship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marinee.'+version+'_OBSclim2BClocalship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'ERA') THEN BEGIN
      CASE isanom OF
	'true': BEGIN 
	  IF (climchoice EQ 'anoms7605') OR (climchoice EQ 'anoms7905') THEN $
            infile = 'e2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1979-2005' ELSE $
	    infile = 'e2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1981-2010'
	END
	'false': infile = 'e2m_monthly_5by5_ERA-Interim_data_'+datestring
      ENDCASE
    ENDIF
    maskfileL = maskdir+'HadISDH.lande.'+version+'_FLATgridIDPHA5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileM = maskdir+'HadISDH.marinee.'+version+'_FLATgrid5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileB = maskdir+'HadISDH.e.'+version+'_FLATgridPHABClocalSHIPboth5by5_'+mclimchoice+'_'+thenmon+thenyear
  END
  'rh': BEGIN
   param2 = 'RH'	
    IF (homogtype EQ 'ID')     THEN infile = 'HadISDH.landRH.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'PHA')    THEN infile = 'HadISDH.landRH.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'RAW')    THEN infile = 'HadISDH.landRH.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLEND')  THEN infile = 'HadISDH.blendRH.'+version+'_FULL_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineRH.'+version+'_BClocal5by5both_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'BLENDship')  THEN infile = 'HadISDH.blendRH.'+version+'_FULLship_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineRH.'+version+'_BClocalSHIP5by5both_'+climchoice+'_'+thenmon+thenyear
    IF (homogtype EQ 'ERA') THEN BEGIN
      CASE isanom OF
	'true': BEGIN 
	  IF (climchoice EQ 'anoms7605') OR (climchoice EQ 'anoms7905') THEN $
            infile = 'rh2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1979-2005' ELSE $
	    infile = 'rh2m_monthly_5by5_ERA-Interim_data_'+datestring+'_anoms1981-2010'
	END
	'false': infile = 'rh2m_monthly_5by5_ERA-Interim_data_'+datestring
      ENDCASE
    ENDIF
    maskfileL = maskdir+'HadISDH.landRH.'+version+'_FLATgridIDPHA5by5_'+mclimchoice+'_'+thenmon+thenyear
    maskfileM = maskdir+'HadISDH.marineRH.'+version+'_BClocalSHIP5by5both_'+mclimchoice+'_'+thenmon+thenyear
    maskfileB = maskdir+'HadISDH.RH.'+version+'_FLATgridIDPHABClocalSHIPboth5by5_'+mclimchoice+'_'+thenmon+thenyear
  END
  'w': BEGIN
   param2 = 'w'	
    infile='waswind_v1_0_1.monthly'
    maskfileM = maskdir+'HadISDH.landw.'+version+'_FLATgridPHA5by5_'+mclimchoice+'_'+thenmon+thenyear
  END  
ENDCASE

inlandcover = '/data/local/hadkw/HADCRUH2/'+workingdir+'/OTHERDATA/HadCRUT.4.3.0.0.land_fraction.nc'

IF (homogtype EQ 'ERA') THEN BEGIN
  IF (mask EQ 'true') THEN BEGIN
    ofile=infile+'_areaTS_'+domain+'_MASK_'+strcompress(mstyr,/remove_all)+strcompress(medyr,/remove_all)
  ENDIF ELSE BEGIN
    IF (domain NE 'blend') THEN ofile=infile+'_areaTS_'+domain ELSE ofile=infile+'_areaTS'
  ENDELSE
ENDIF ELSE BEGIN
;  IF (isanom EQ 'true') THEN ofile=infile+'_'+climchoice+'_areaTS_'+strcompress(styr,/remove_all)+strcompress(edyr,/remove_all) $
  IF (isanom EQ 'true') THEN ofile=infile+'_areaTS_'+strcompress(styr,/remove_all)+strcompress(edyr,/remove_all) $
                        ELSE ofile=infile+'_absolutes_areaTS_'+strcompress(styr,/remove_all)+strcompress(edyr,/remove_all)	
ENDELSE

CASE param OF
  'rh': unitees =   '%rh'
  'e': unitees =    'hPa'
  'q': unitees =    'g/kg'
  'w': unitees =    'm/s'
  'evap': unitees = 'cm w.e.'
  ELSE: unitees =   'deg C'
ENDCASE

; Time and dimension variables
nyrs =     (edyr+1)-styr
nmons =    nyrs*12
int_mons = indgen(nmons)
stlt =     -90+(latlg/2.)
stln =     -180+(lonlg/2.)
nlats =    180/latlg
nlons =    360/lonlg
nbox =     LONG(nlats*nlons)

mnyrs =     (medyr+1)-mstyr
mnmons =    mnyrs*12
mint_mons = indgen(mnmons)

lats = (findgen(nlats)*latlg)+stlt
lons = (findgen(nlons)*lonlg)+stln

;----------------------------------------------------
; read in files
IF (homogtype EQ 'OTHER') OR (homogtype EQ 'ERA') THEN BEGIN
  filee = NCDF_OPEN('/data/local/hadkw/HADCRUH2/'+workingdir+'/OTHERDATA/'+infile+'.nc')
ENDIF ELSE BEGIN
  filee = NCDF_OPEN(dir+'GRIDS/'+infile+'_cf.nc')
ENDELSE
longs_varid = NCDF_VARID(filee,'longitude')
lats_varid =  NCDF_VARID(filee,'latitude')
;IF (homogtype EQ 'BLEND') THEN tims_varid = NCDF_VARID(filee,'times') ELSE  tims_varid=NCDF_VARID(filee,'time')
tims_varid=NCDF_VARID(filee,'time')

IF (homogtype EQ 'ERA') THEN BEGIN
  IF (isanom EQ 'true') THEN qvarid = NCDF_VARID(filee,'anomalies') ELSE qvarid=NCDF_VARID(filee,'actuals')
ENDIF ELSE BEGIN

  CASE param OF
    'evap': BEGIN
      qvarid = NCDF_VARID(filee,'anomalies_land')
  ;    qvarid = NCDF_VARID(filee,'anomalies_sea')
    END 
    'dpd': BEGIN
      IF (isanom EQ 'true') THEN qvarid = NCDF_VARID(filee,'dpd_anoms') ELSE qvarid=NCDF_VARID(filee,'dpd_abs')
    END
    'td': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'td_anoms') ELSE qvarid=NCDF_VARID(filee,'td_abs')
    END
    't': BEGIN
      IF (homogtype EQ 'OTHER') THEN BEGIN
        qvarid=NCDF_VARID(filee,'temperature_anomaly')
;       qvarid=NCDF_VARID(filee,'sst')      
      ENDIF ELSE BEGIN
        IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'t_anoms') ELSE qvarid=NCDF_VARID(filee,'t_abs')
      ENDELSE
    END
    'tw': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'tw_anoms') ELSE qvarid=NCDF_VARID(filee,'tw_abs')
    END
    'q': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'q_anoms') ELSE qvarid=NCDF_VARID(filee,'q_abs')
    END
    'rh': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'rh_anoms') ELSE qvarid=NCDF_VARID(filee,'rh_abs')
    END
    'e': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'e_anoms') ELSE qvarid=NCDF_VARID(filee,'e_abs')
    END
    'w': BEGIN
      qabsid=NCDF_VARID(filee,'sp')
    END
  ENDCASE
ENDELSE

;qstdid=NCDF_VARID(filee,'td_combinederr') 	; may become uncertainty fields
;if (homogtype NE 'OTHER') AND (param NE 'w') AND (homogtype NE 'BLEND') AND (homogtype NE 'MARINE') THEN NCDF_VARGET,filee,qabsid,q_abs
IF (param NE 'w') THEN BEGIN
  NCDF_VARGET,filee,qvarid,q_values
ENDIF ELSE BEGIN ; only in the case of wind 1981-2010 clim!!!
  bads=WHERE(q_abs LT -999,count)
  IF (count GT 0) THEN q_abs(bads)=mdi
  ; make anomalies from the monthlies
  q_values=make_array(nlons,nlats,nmons,/float,value=mdi)
  FOR ltt=0,nlats-1 DO BEGIN
    FOR lnn=0,nlons-1 DO BEGIN
      subarr=REFORM(q_abs(lnn,ltt,*),12,nyrs)
      FOR mm=0,11 DO BEGIN
        gots=WHERE(subarr(mm,*) NE mdi,count)
	climsub=subarr(mm,1981-styr:2010-styr)
	gotsC=WHERE(climsub NE mdi,countC)
	IF (countC GE 15) AND (count GE 40) THEN subarr(mm,gots)=subarr(mm,gots)-MEAN(climsub(gotsC)) ELSE subarr(mm,*)=mdi
      ENDFOR
      q_values(lnn,ltt,*)=REFORM(subarr,nmons)
    ENDFOR
  ENDFOR
  
ENDELSE
;NCDF_VARGET,filee,qstdid,q_err
NCDF_VARGET,filee,lats_varid,lats
NCDF_VARGET,filee,longs_varid,longs
NCDF_VARGET,filee,tims_varid,dayssince
NCDF_CLOSE,filee

; If we're working with blended or marine then this has been written in python and mdi is higher than IDL -1e30
; so need to reset to IDL mdi
IF (homogtype EQ 'MARINE') OR (homogtype EQ 'MARINEship') THEN BEGIN
  ;mdi = min(q_values)
  stop
  gots = where(q_values LT -10000,count)
  q_values(gots) = mdi
END

;If (homogtype EQ 'MARINE') THEN BEGIN
;  q_values = reverse(q_values,2)
;  bads = where(q_values LT -100,count)
;  if (count GT 0) THEN q_values(bads) = mdi
;ENDIF
If ((homogtype EQ 'ERA') OR (homogtype EQ 'OTHER')) AND (mask EQ 'true') THEN BEGIN
  CASE domain OF
    'land': filee=NCDF_OPEN(maskfileL+'_cf.nc')
    'marine': filee=NCDF_OPEN(maskfileM+'_cf.nc')
    'blend': filee=NCDF_OPEN(maskfileB+'_cf.nc')
  ENDCASE
  tims_varid=NCDF_VARID(filee,'time')
  
  CASE param OF
    'dpd': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'dpd_anoms') ELSE qvarid=NCDF_VARID(filee,'dpd_abs')
    END
    'td': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'td_anoms') ELSE qvarid=NCDF_VARID(filee,'td_abs')
    END
    't': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'t_anoms') ELSE qvarid=NCDF_VARID(filee,'t_abs')
    END
    'tw': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'tw_anoms') ELSE qvarid=NCDF_VARID(filee,'tw_abs')
    END
    'q': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'q_anoms') ELSE qvarid=NCDF_VARID(filee,'q_abs')
    END
    'rh': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'rh_anoms') ELSE qvarid=NCDF_VARID(filee,'rh_abs')
    END
    'e': BEGIN
      IF (isanom EQ 'true') THEN qvarid=NCDF_VARID(filee,'e_anoms') ELSE qvarid=NCDF_VARID(filee,'e_abs')
    END
    'w': BEGIN
      qabsid=NCDF_VARID(filee,'sp')
    END
  ENDCASE
  NCDF_VARGET,filee,qvarid,mask_values
  NCDF_VARGET,filee,tims_varid,dayssince
  NCDF_CLOSE,filee
  
;  ; set up the output file name now that were working with masks 
;  ofile=infile+'_areaTSMSK'+strmid(strcompress(mclimst,/remove_all),2,2)+strmid(strcompress(mclimed,/remove_all),2,2)+'_'+strcompress(mstyr,/remove_all)+strcompress(medyr,/remove_all)
  
  ; make time element as long as the mask which is HadISDH
  oldq_values=q_values
  ; mask to HadISDH over the joint period of record  
  q_values=make_array(nlons,nlats,mnmons,/float,value=mdi)
  ; sort out which one starts/ends before the other to get time matches
  stdiff=(styr-mstyr)*12 ; candidate - mask
  IF (stdiff GT 0) THEN mpointerst=stdiff ELSE mpointerst=0
  IF (stdiff LT 0) THEN cpointerst=(-(stdiff)) ELSE cpointerst=0
  eddiff=(edyr-medyr)*12 ; candidate - mask
  IF (eddiff GE 0) THEN mpointered=mnmons-1 ELSE mpointered=-(eddiff)
  IF (eddiff LE 0) THEN cpointered=nmons-1 ELSE cpointered=eddiff
  print,mpointerst,mpointered,cpointerst,cpointered
  stop
  q_values(*,*,mpointerst:mpointered)=oldq_values(*,*,cpointerst:cpointered)	;shorten to same time period as HadISDH
  ; mask out and points that do not have data in the mask
  bads=WHERE(mask_values LT -999,count)
  IF (count GT 0) THEN q_values(bads)=mdi
  
; Change nmons (candidate number of months) to mnmons (masked number of months)  
  nmons=mnmons
; Change int_mons (index of candidate number of months) to mint_mons (index of masked number of months)  
  int_mons=mint_mons
; Change styr (start year of candidate number of months) to mstyr (start year of masked number of months)  
  styr=mstyr
; Change edyr (end year of candidate number of months) to medyr (end year of masked number of months)  
  edyr=medyr
; Change nyrs (nyrs of candidate number of months) to myrs (nyrs of masked number of months)  
  nyrs=mnyrs
  
;  ; make anomalies from the monthlies if you want to be precise about anomalising with same coverage as HadISDH
;  newq_values=make_array(nlons,nlats,nmons,/float,value=mdi)
;  FOR ltt=0,nlats-1 DO BEGIN
;    FOR lnn=0,nlons-1 DO BEGIN
;      subarr=REFORM(q_values(lnn,ltt,*),12,nyrs)
;      FOR mm=0,11 DO BEGIN
;        gots=WHERE(subarr(mm,*) NE mdi,count)
;	 climsub=subarr(mm,mclimst-styr:mclimst-styr)
;	 gotsC=WHERE(climsub NE mdi,countC)
;	 IF (countC GE 15) THEN subarr(mm,gots)=subarr(mm,gots)-MEAN(climsub(gotsC)) ELSE subarr(mm,*)=mdi
;      ENDFOR
;      newq_values(lnn,ltt,*)=REFORM(subarr,nmons)
;    ENDFOR
;  ENDFOR
;  ;stop
;  q_values=newq_values
ENDIF ELSE IF (mask EQ 'false') AND (homogtype EQ 'ERA') AND (domain NE 'all') THEN BEGIN
  ; read in the land cover
  inn = NCDF_OPEN(inlandcover)
  varid = NCDF_VARID(inn, 'land_area_fraction')
  NCDF_VARGET, inn, varid, pctland
  NCDF_CLOSE, inn
  
  ; mask to desired domain
  FOR mm=0,nmons-1 DO BEGIN
    IF (domain EQ 'land') THEN chucks = where(pctland EQ 0.,count) ELSE chucks = where(pctland EQ 1.,count)
    subarr = q_values(*,*,mm)
    subarr(chucks) = mdi
    q_values(*,*,mm) = subarr
  ENDFOR  
ENDIF
;---------------------------------------------------------------

;stop

;make mask - set anything greater than 70 deg lat to mdi

global_mask = q_values(*,*,0)
global_mask(*,*) = 1
nhem_mask=global_mask
shem_mask=global_mask
trop_mask=global_mask

for deg=0,nlats-1 DO BEGIN
  if (lats(deg) LT -70.) OR (lats(deg) GT 70.) THEN BEGIN
    global_mask(*,deg) = mdi
  endif
  if (lats(deg) LT 20.) OR (lats(deg) GT 70.) THEN BEGIN
    nhem_mask(*,deg) = mdi
  endif
  if (lats(deg) LT -70.) OR (lats(deg) GT -20.) THEN BEGIN
    shem_mask(*,deg) = mdi
  endif
  if (lats(deg) LT -20.) OR (lats(deg) GT 20.) THEN BEGIN
    trop_mask(*,deg) = mdi
  endif  
endfor

field_values=make_array(nlons,nlats,nmons,/float)	;all values or a subsection
num_val=n_elements(field_values(0,0,*))

global_mask_3d=fltarr(nlons,nlats,num_val)
nhem_mask_3d=fltarr(nlons,nlats,num_val)
shem_mask_3d=fltarr(nlons,nlats,num_val)
trop_mask_3d=fltarr(nlons,nlats,num_val)

for add=0,num_val-1 do begin
  global_mask_3d(*,*,add) = global_mask(*,*)
  nhem_mask_3d(*,*,add)=nhem_mask(*,*)
  shem_mask_3d(*,*,add)=shem_mask(*,*)
  trop_mask_3d(*,*,add)=trop_mask(*,*)
endfor

field_values(*,*,*)=q_values(*,*,0:nmons-1)
print,n_elements(field_values(0,0,*))
num_val=n_elements(field_values(0,0,*))
glob_avg_ts=fltarr(num_val)
glob_avg_ts=globalmean(field_values,lats,mdi,mask=global_mask_3d)

print,n_elements(glob_avg_ts)
print,max(glob_avg_ts)
print,min(glob_avg_ts)
print,glob_avg_ts(0:10)

nhem_avg_ts=fltarr(num_val)
nhem_avg_ts=globalmean(field_values,lats,mdi,mask=nhem_mask_3d)

print,n_elements(nhem_avg_ts)
print,max(nhem_avg_ts)
print,min(nhem_avg_ts)
print,nhem_avg_ts(0:10)

shem_avg_ts=fltarr(num_val)
shem_avg_ts=globalmean(field_values,lats,mdi,mask=shem_mask_3d)

print,n_elements(shem_avg_ts)
print,max(shem_avg_ts)
print,min(shem_avg_ts)
print,shem_avg_ts(0:10)

trop_avg_ts=fltarr(num_val)
trop_avg_ts=globalmean(field_values,lats,mdi,mask=trop_mask_3d)

print,n_elements(trop_avg_ts)
print,max(trop_avg_ts)
print,min(trop_avg_ts)
print,trop_avg_ts(0:10)
  
;save to file;
;
filename=odir+ofile+'.nc'
file_out=NCDF_CREATE(filename,/clobber)
time_id=NCDF_DIMDEF(file_out,'time',nmons)
timvarid=NCDF_VARDEF(file_out,'time',[time_id],/DOUBLE)

CASE param OF
  'evap': BEGIN
    glob_varid=NCDF_VARDEF(file_out,'glob_evap_anoms',[time_id],/FLOAT)
    trop_varid=NCDF_VARDEF(file_out,'trop_evap_anoms',[time_id],/FLOAT)
    nhem_varid=NCDF_VARDEF(file_out,'nhem_evap_anoms',[time_id],/FLOAT)
    shem_varid=NCDF_VARDEF(file_out,'shem_evap_anoms',[time_id],/FLOAT)
  END
  'dpd': BEGIN
    glob_varid=NCDF_VARDEF(file_out,'glob_DPD_anoms',[time_id],/FLOAT)
    trop_varid=NCDF_VARDEF(file_out,'trop_DPD_anoms',[time_id],/FLOAT)
    nhem_varid=NCDF_VARDEF(file_out,'nhem_DPD_anoms',[time_id],/FLOAT)
    shem_varid=NCDF_VARDEF(file_out,'shem_DPD_anoms',[time_id],/FLOAT)
  END
  'td': BEGIN
    glob_varid=NCDF_VARDEF(file_out,'glob_Td_anoms',[time_id],/FLOAT)
    trop_varid=NCDF_VARDEF(file_out,'trop_Td_anoms',[time_id],/FLOAT)
    nhem_varid=NCDF_VARDEF(file_out,'nhem_Td_anoms',[time_id],/FLOAT)
    shem_varid=NCDF_VARDEF(file_out,'shem_Td_anoms',[time_id],/FLOAT)
  END
  't': BEGIN
    glob_varid=NCDF_VARDEF(file_out,'glob_T_anoms',[time_id],/FLOAT)
    trop_varid=NCDF_VARDEF(file_out,'trop_T_anoms',[time_id],/FLOAT)
    nhem_varid=NCDF_VARDEF(file_out,'nhem_T_anoms',[time_id],/FLOAT)
    shem_varid=NCDF_VARDEF(file_out,'shem_T_anoms',[time_id],/FLOAT)
  END
  'tw': BEGIN
    glob_varid=NCDF_VARDEF(file_out,'glob_Tw_anoms',[time_id],/FLOAT)
    trop_varid=NCDF_VARDEF(file_out,'trop_Tw_anoms',[time_id],/FLOAT)
    nhem_varid=NCDF_VARDEF(file_out,'nhem_Tw_anoms',[time_id],/FLOAT)
    shem_varid=NCDF_VARDEF(file_out,'shem_Tw_anoms',[time_id],/FLOAT)
  END
  'q': BEGIN
    glob_varid=NCDF_VARDEF(file_out,'glob_q_anoms',[time_id],/FLOAT)
    trop_varid=NCDF_VARDEF(file_out,'trop_q_anoms',[time_id],/FLOAT)
    nhem_varid=NCDF_VARDEF(file_out,'nhem_q_anoms',[time_id],/FLOAT)
    shem_varid=NCDF_VARDEF(file_out,'shem_q_anoms',[time_id],/FLOAT)
  END
  'rh': BEGIN
    glob_varid=NCDF_VARDEF(file_out,'glob_RH_anoms',[time_id],/FLOAT)
    trop_varid=NCDF_VARDEF(file_out,'trop_RH_anoms',[time_id],/FLOAT)
    nhem_varid=NCDF_VARDEF(file_out,'nhem_RH_anoms',[time_id],/FLOAT)
    shem_varid=NCDF_VARDEF(file_out,'shem_RH_anoms',[time_id],/FLOAT)
  END
  'e': BEGIN
    glob_varid=NCDF_VARDEF(file_out,'glob_e_anoms',[time_id],/FLOAT)
    trop_varid=NCDF_VARDEF(file_out,'trop_e_anoms',[time_id],/FLOAT)
    nhem_varid=NCDF_VARDEF(file_out,'nhem_e_anoms',[time_id],/FLOAT)
    shem_varid=NCDF_VARDEF(file_out,'shem_e_anoms',[time_id],/FLOAT)
  END
  'w': BEGIN
    glob_varid=NCDF_VARDEF(file_out,'glob_w_anoms',[time_id],/FLOAT)
    trop_varid=NCDF_VARDEF(file_out,'trop_w_anoms',[time_id],/FLOAT)
    nhem_varid=NCDF_VARDEF(file_out,'nhem_w_anoms',[time_id],/FLOAT)
    shem_varid=NCDF_VARDEF(file_out,'shem_w_anoms',[time_id],/FLOAT)
  END  

ENDCASE

NCDF_ATTPUT,file_out,timvarid,'units','days since 1973-1-1 00:00:00'
NCDF_ATTPUT,file_out,timvarid,'long_name','time'
NCDF_ATTPUT,file_out,timvarid,'calendar','gregorian'
NCDF_ATTPUT,file_out,glob_varid,'units',unitees
NCDF_ATTPUT,file_out,glob_varid,'long_name','Globally Averaged Anomalies 70S-70N'
NCDF_ATTPUT,file_out,glob_varid,'missing_value',mdi

NCDF_ATTPUT,file_out,trop_varid,'units',unitees
NCDF_ATTPUT,file_out,trop_varid,'long_name','Tropics Averaged Anomalies 20S-20N'
NCDF_ATTPUT,file_out,trop_varid,'missing_value',mdi

NCDF_ATTPUT,file_out,nhem_varid,'units',unitees
NCDF_ATTPUT,file_out,nhem_varid,'long_name','Northern Hemisphere Averaged Anomalies 20N-70N'
NCDF_ATTPUT,file_out,nhem_varid,'missing_value',mdi

NCDF_ATTPUT,file_out,shem_varid,'units',unitees
NCDF_ATTPUT,file_out,shem_varid,'long_name','Southern Hemisphere Averaged Anomalies 70S-20S'
NCDF_ATTPUT,file_out,shem_varid,'missing_value',mdi
NCDF_CONTROL,file_out,/ENDEF

NCDF_VARPUT,file_out,glob_varid,glob_avg_ts
NCDF_VARPUT,file_out,trop_varid,trop_avg_ts
NCDF_VARPUT,file_out,nhem_varid,nhem_avg_ts
NCDF_VARPUT,file_out,shem_varid,shem_avg_ts
NCDF_VARPUT,file_out,time_id,dayssince
NCDF_CLOSE,file_out;

; Output to ascii too
IF (homogtype NE 'OTHER') AND (homogtype NE 'ERA') THEN openw,2,dir+'TIMESERIES/'+ofile+'_monthly.dat' $
    ELSE openw,2,odir+ofile+'_monthly.dat'
printf,2,'DATE','GLOBAL','N_HEMI','TROPICS','S_HEMI',format='(a6,4a8)'
year=styr
mpoint=0
monarr=['01','02','03','04','05','06','07','08','09','10','11','12']
FOR mm=0,nmons-1 DO BEGIN
 
printf,2,year,monarr(mpoint),glob_avg_ts(mm),nhem_avg_ts(mm),trop_avg_ts(mm),shem_avg_ts(mm),format='(i4,a2,x,4(f7.2,x))'
  mpoint=mpoint+1
  IF (mpoint EQ 12) THEN BEGIN
    mpoint=0
    year=year+1
  ENDIF
ENDFOR
close,2

IF (homogtype NE 'OTHER') AND (homogtype NE 'ERA') THEN openw,2,dir+'TIMESERIES/'+ofile+'_annual.dat' $
    ELSE openw,2,odir+ofile+'_annual.dat'
printf,2,'DATE','GLOBAL','N_HEMI','TROPICS','S_HEMI',format='(a4,4a8)'
year=styr
mpoint=0
glob_avg_ts=REFORM(glob_avg_ts,12,nyrs)
nhem_avg_ts=REFORM(nhem_avg_ts,12,nyrs)
trop_avg_ts=REFORM(trop_avg_ts,12,nyrs)
shem_avg_ts=REFORM(shem_avg_ts,12,nyrs)
FOR yy=0,nyrs-1 DO BEGIN
  printf,2,year,mean(glob_avg_ts(*,yy)),mean(nhem_avg_ts(*,yy)),mean(trop_avg_ts(*,yy)),mean(shem_avg_ts(*,yy)),format='(i4,x,4(f7.2,x))'
  year=year+1
ENDFOR
close,2
return

end

