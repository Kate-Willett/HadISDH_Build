; TIDL
; 
; Author: Kate Willett
; Created: 1 February 2013
; Last update: 15 January 2015
; Location: /data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/HADISDH_BUILD/	
; GitHub: https://github.com/Kate-Willett/HadISDH_Build					
; -----------------------
; CODE PURPOSE AND OUTPUT
; -----------------------
; <brief summary of code purpose and main outputs>
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
; <source data sets required for code; include data origin>
; 
; -----------------------
; HOW TO RUN THE CODE
; -----------------------
; <step by step guide to running the code>
; 
; -----------------------
; OUTPUT
; -----------------------
; <where this is written to and any other useful information about output>
; 
; -----------------------
; VERSION/RELEASE NOTES
; -----------------------
; 
; Version 2 (14 February 2018)
; ---------
;  
; Enhancements
; Now call param and homogtype from the command line
; Which variable?
; param      = 't'	;'dpd','td','t','tw','e','q','rh'
; Which homog type?
; homogtype  = 'ID'	;'PHA','ID','DPD', 'RAW'
;  
; Changes
;  
; Bug fixes
;  
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


pro plot_HadISDH_trendsscat_JAN2015,param,homogtype
;; Which variable?
;param      = 't'	;'dpd','td','t','tw','e','q','rh'
;; Which homog type?
;homogtype  = 'ID'	;'PHA','ID','DPD', 'RAW'



; add a comparison of regional time series and trends from the raw and homogenised data.



;-----------------------------------------------------
!Except=2

; EDITABLES

; Which start/end year?
styr = 1973
edyr = 2018
yearchoice = strcompress(styr,/remove_all)+strcompress(edyr,/remove_all)
OLDyearchoice = strcompress(styr,/remove_all)+strcompress(edyr-1,/remove_all)

; Which CLIMATOLOGY start/end year?
climst = 1981 	; 1976 or 1981
climed = 2010	; 2005 or 2010
CLMlab =     strmid(strcompress(climst,/remove_all),2,2)+strmid(strcompress(climed,/remove_all),2,2)
climchoice = 'anoms'+CLMlab ; 'anoms7605','anoms8110'
climchoiceOLD = 'anoms8110' ; Oh Dear - should compare with old anoms8110 but I haven't done it

; Which output date?
nowmon     = 'JAN'
nowyear    = '2019'

; Which input date?
thenmon     = 'JAN'
thenyear    = '2019'
OLDthenmon     = 'MAR'
OLDthenyear    = '2018'

; Which variable?
;param      = 't'	;'dpd','td','t','tw','e','q','rh';
;
;; Which homog type?
;homogtype  = 'ID'	;'PHA','ID','DPD', 'RAW'

; Which versions?
version    = '4.1.0.2018f'
OLDversion = '4.0.0.2017f'

; Which plot - compare old/new or raw/homog?
typee      = 'OLD' ;'RAW' for PHA vs RAW or 'OLD' for 2015 vs 2014

workingdir = '/data/local/hadkw/HADCRUH2/UPDATE20'+strmid(strcompress(edyr,/remove_all),2,2)
oldindir   = '/data/local/hadkw/HADCRUH2/UPDATE20'+strmid(strcompress(edyr-1,/remove_all),2,2)+'/STATISTICS/'
indir      = workingdir+'/STATISTICS/'
odir       = workingdir+'/IMAGES/BUILD/'

CASE param OF
  'dpd': BEGIN
    param2      = 'DPD'	;'DPD','Td','T','Tw','e','q','RH'
    unitees     = '!Eo!NC'
    inhomogmp   = indir+'TRENDS/HadISDH.landDPD.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
    inhomogts   = indir+'TIMESERIES/HadISDH.landDPD.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
    inrawmp     = indir+'TRENDS/HadISDH.landDPD.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
    inrawts     = indir+'TIMESERIES/HadISDH.landDPD.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
    inoldmp     = oldindir+'TRENDS/HadISDH.landDPD.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
    inoldts     = oldindir+'TIMESERIES/HadISDH.landDPD.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
    outfile     = odir+'HadISDH.landDPD.'+version+'_FLATgridPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    variname    = 'dew point depression'
  END
  'td': BEGIN
    param2      = 'Td'	;'DPD','Td','T','Tw','e','q','RH'
    unitees     = '!Eo!NC'
    IF (homogtype EQ 'PHA') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.landTd.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.landTd.'+version+'_FLATgridPHADPD5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.landTd.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.landTd.'+version+'_FLATgridPHADPD5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.landTd.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.landTd.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.landTd.'+version+'_FLATgridPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF ELSE IF (homogtype EQ 'DPD') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.landTd.'+version+'_FLATgridPHADPD5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.landTd.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.landTd.'+version+'_FLATgridPHADPD5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.landTd.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.landTd.'+OLDversion+'_FLATgridPHADPD5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.landTd.'+OLDversion+'_FLATgridPHADPD5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.landTd.'+version+'_FLATgridPHADPD5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF   
    variname='dew point temperature'
  END
  't': BEGIN
    param2      = 'T'	;'DPD','Td','T','Tw','e','q','RH'
    unitees     = '!Eo!NC'
    IF (homogtype EQ 'PHA') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.landT.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.landT.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.landT.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.landT.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.landT.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.landT.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.landT.'+version+'_FLATgridPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF ELSE IF (homogtype EQ 'ID') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.landT.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.landT.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.landT.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.landT.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.landT.'+OLDversion+'_FLATgridIDPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.landT.'+OLDversion+'_FLATgridIDPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.landT.'+version+'_FLATgridIDPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF   
    variname='temperature'
  END
  'tw': BEGIN
    param2      = 'Tw'	;'DPD','Td','T','Tw','e','q','RH'
    unitees     = '!Eo!NC'
    IF (homogtype EQ 'PHA') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.landTw.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.landTw.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.landTw.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.landTw.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.landTw.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.landTw.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.landTw.'+version+'_FLATgridPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF ELSE IF (homogtype EQ 'ID') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.landTw.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.landTw.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.landTw.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.landTw.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.landTw.'+OLDversion+'_FLATgridIDPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.landTw.'+OLDversion+'_FLATgridIDPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.landTw.'+version+'_FLATgridIDPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF   
    variname='wet bulb temperature'
  END
  'q': BEGIN
    param2      = 'q'	;'DPD','Td','T','Tw','e','q','RH'
    unitees     = 'g kg!E-1!N'
    IF (homogtype EQ 'PHA') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.landq.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.landq.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.landq.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.landq.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.landq.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.landq.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.landq.'+version+'_FLATgridPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF ELSE IF (homogtype EQ 'ID') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.landq.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.landq.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.landq.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.landq.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.landq.'+OLDversion+'_FLATgridIDPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.landq.'+OLDversion+'_FLATgridIDPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.landq.'+version+'_FLATgridIDPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF   
    variname='specific humidity'
 END
  'e': BEGIN
    param2      = 'e'	;'DPD','Td','T','Tw','e','q','RH'
    unitees     = 'hPa'
    IF (homogtype EQ 'PHA') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.lande.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.lande.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.lande.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.lande.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.lande.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.lande.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.lande.'+version+'_FLATgridPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF ELSE IF (homogtype EQ 'ID') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.lande.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.lande.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.lande.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.lande.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.lande.'+OLDversion+'_FLATgridIDPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.lande.'+OLDversion+'_FLATgridIDPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.lande.'+version+'_FLATgridIDPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF   
    variname='vapour pressure'
  END
  'rh': BEGIN
    param2      = 'RH'	;'DPD','Td','T','Tw','e','q','RH'
    unitees     = '%rh'
    IF (homogtype EQ 'PHA') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.landRH.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.landRH.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.landRH.'+version+'_FLATgridPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.landRH.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.landRH.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.landRH.'+OLDversion+'_FLATgridPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.landRH.'+version+'_FLATgridPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF ELSE IF (homogtype EQ 'ID') THEN BEGIN
      inhomogmp = indir+'TRENDS/HadISDH.landRH.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inrawmp   = indir+'TRENDS/HadISDH.landRH.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_cf_MPtrends_'+yearchoice+'.nc'
      inhomogts = indir+'TIMESERIES/HadISDH.landRH.'+version+'_FLATgridIDPHA5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inrawts   = indir+'TIMESERIES/HadISDH.landRH.'+version+'_FLATgridRAW5by5_'+climchoice+'_'+thenmon+thenyear+'_areaTS_'+yearchoice+'.nc'
      inoldmp   = oldindir+'TRENDS/HadISDH.landRH.'+OLDversion+'_FLATgridIDPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_cf_MPtrends_'+OLDyearchoice+'.nc'
      inoldts   = oldindir+'TIMESERIES/HadISDH.landRH.'+OLDversion+'_FLATgridIDPHA5by5_'+climchoiceOLD+'_'+OLDthenmon+OLDthenyear+'_areaTS_'+OLDyearchoice+'.nc'
      outfile   = odir+'HadISDH.landRH.'+version+'_FLATgridIDPHA5by5_'+nowmon+nowyear+'_MPtrendsscat'+typee+'_'+yearchoice+'.eps'
    ENDIF   
    variname='relative humidity'
  END
  
ENDCASE


;--------------------------------------------------------
; variables and arrays
mdi=-1e+30

latlg=5.
lonlg=5.
stlt=-90+(latlg/2.)
stln=-180+(lonlg/2.)
nlats=180/latlg
nlons=360/lonlg
nbox=LONG(nlats*nlons)

lats=(findgen(nlats)*latlg)+stlt
lons=(findgen(nlons)*lonlg)+stln

nyrs=(edyr+1)-styr
nmons=nyrs*12
int_mons=indgen(nmons)

adj_locs=make_array(nmons,/int,value=0)
adj_mags_accum=100. ;grow this array on the fly
adj_mags_act=100.

;----------------------------------------------------------
homogarr=make_array(4,nyrs,/float,value=mdi)
rawarr=make_array(4,nyrs,/float,value=mdi)
;---------------------------------------------------------
; open area ave TS files
inn=NCDF_OPEN(inhomogts)

CASE param OF
  'dpd': BEGIN
    varg=NCDF_VARID(inn,'glob_DPD_anoms')
    varnh=NCDF_VARID(inn,'nhem_DPD_anoms')
    vart=NCDF_VARID(inn,'trop_DPD_anoms')
    varsh=NCDF_VARID(inn,'shem_DPD_anoms')
  END
  'td': BEGIN
    varg=NCDF_VARID(inn,'glob_Td_anoms')
    varnh=NCDF_VARID(inn,'nhem_Td_anoms')
    vart=NCDF_VARID(inn,'trop_Td_anoms')
    varsh=NCDF_VARID(inn,'shem_Td_anoms')
  END
  't': BEGIN
    varg=NCDF_VARID(inn,'glob_T_anoms')
    varnh=NCDF_VARID(inn,'nhem_T_anoms')
    vart=NCDF_VARID(inn,'trop_T_anoms')
    varsh=NCDF_VARID(inn,'shem_T_anoms')
  END
  'tw': BEGIN
    varg=NCDF_VARID(inn,'glob_Tw_anoms')
    varnh=NCDF_VARID(inn,'nhem_Tw_anoms')
    vart=NCDF_VARID(inn,'trop_Tw_anoms')
    varsh=NCDF_VARID(inn,'shem_Tw_anoms')
  END
  'q': BEGIN
    varg=NCDF_VARID(inn,'glob_q_anoms')
    varnh=NCDF_VARID(inn,'nhem_q_anoms')
    vart=NCDF_VARID(inn,'trop_q_anoms')
    varsh=NCDF_VARID(inn,'shem_q_anoms')
  END
  'e': BEGIN
    varg=NCDF_VARID(inn,'glob_e_anoms')
    varnh=NCDF_VARID(inn,'nhem_e_anoms')
    vart=NCDF_VARID(inn,'trop_e_anoms')
    varsh=NCDF_VARID(inn,'shem_e_anoms')
  END
  'rh': BEGIN
    varg=NCDF_VARID(inn,'glob_RH_anoms')
    varnh=NCDF_VARID(inn,'nhem_RH_anoms')
    vart=NCDF_VARID(inn,'trop_RH_anoms')
    varsh=NCDF_VARID(inn,'shem_RH_anoms')
  END
ENDCASE  

NCDF_VARGET,inn,varg,globval
NCDF_VARGET,inn,varnh,nhemval
NCDF_VARGET,inn,vart,tropval
NCDF_VARGET,inn,varsh,shemval
NCDF_CLOSE,inn

;make annual averages
globval=REFORM(globval,12,nyrs)
nhemval=REFORM(nhemval,12,nyrs)
tropval=REFORM(tropval,12,nyrs)
shemval=REFORM(shemval,12,nyrs)
FOR yy=0,nyrs-1 DO BEGIN
  subarr=globval(*,yy)
  gots=WHERE(subarr NE mdi,count)
  IF (count GT 8) THEN homogarr(0,yy)=MEAN(subarr(gots))	; at least 9 months present
  subarr=nhemval(*,yy)
  gots=WHERE(subarr NE mdi,count)
  IF (count GT 8) THEN homogarr(1,yy)=MEAN(subarr(gots))	; at least 9 months present
  subarr=tropval(*,yy)
  gots=WHERE(subarr NE mdi,count)
  IF (count GT 8) THEN homogarr(2,yy)=MEAN(subarr(gots))	; at least 9 months present
  subarr=shemval(*,yy)
  gots=WHERE(subarr NE mdi,count)
  IF (count GT 8) THEN homogarr(3,yy)=MEAN(subarr(gots))	; at least 9 months present  
ENDFOR

IF (typee EQ 'RAW') THEN inn=NCDF_OPEN(inrawts) ELSE inn=NCDF_OPEN(inoldts)

CASE param OF
  'dpd': BEGIN
    varg=NCDF_VARID(inn,'glob_DPD_anoms')
    varnh=NCDF_VARID(inn,'nhem_DPD_anoms')
    vart=NCDF_VARID(inn,'trop_DPD_anoms')
    varsh=NCDF_VARID(inn,'shem_DPD_anoms')
  END
  'td': BEGIN
    varg=NCDF_VARID(inn,'glob_Td_anoms')
    varnh=NCDF_VARID(inn,'nhem_Td_anoms')
    vart=NCDF_VARID(inn,'trop_Td_anoms')
    varsh=NCDF_VARID(inn,'shem_Td_anoms')
  END
  't': BEGIN
    varg=NCDF_VARID(inn,'glob_T_anoms')
    varnh=NCDF_VARID(inn,'nhem_T_anoms')
    vart=NCDF_VARID(inn,'trop_T_anoms')
    varsh=NCDF_VARID(inn,'shem_T_anoms')
  END
  'tw': BEGIN
    varg=NCDF_VARID(inn,'glob_Tw_anoms')
    varnh=NCDF_VARID(inn,'nhem_Tw_anoms')
    vart=NCDF_VARID(inn,'trop_Tw_anoms')
    varsh=NCDF_VARID(inn,'shem_Tw_anoms')
  END
  'q': BEGIN
    varg=NCDF_VARID(inn,'glob_q_anoms')
    varnh=NCDF_VARID(inn,'nhem_q_anoms')
    vart=NCDF_VARID(inn,'trop_q_anoms')
    varsh=NCDF_VARID(inn,'shem_q_anoms')
  END
  'e': BEGIN
    varg=NCDF_VARID(inn,'glob_e_anoms')
    varnh=NCDF_VARID(inn,'nhem_e_anoms')
    vart=NCDF_VARID(inn,'trop_e_anoms')
    varsh=NCDF_VARID(inn,'shem_e_anoms')
  END
  'rh': BEGIN
    varg=NCDF_VARID(inn,'glob_RH_anoms')
    varnh=NCDF_VARID(inn,'nhem_RH_anoms')
    vart=NCDF_VARID(inn,'trop_RH_anoms')
    varsh=NCDF_VARID(inn,'shem_RH_anoms')
  END
ENDCASE  

NCDF_VARGET,inn,varg,globval
NCDF_VARGET,inn,varnh,nhemval
NCDF_VARGET,inn,vart,tropval
NCDF_VARGET,inn,varsh,shemval
NCDF_CLOSE,inn

IF (typee EQ 'OLD') THEN BEGIN
  globval=[globval,replicate(mdi,12)]
  nhemval=[nhemval,replicate(mdi,12)]
  tropval=[tropval,replicate(mdi,12)]
  shemval=[shemval,replicate(mdi,12)]
ENDIF

;make annual averages
globval=REFORM(globval,12,nyrs)
nhemval=REFORM(nhemval,12,nyrs)
tropval=REFORM(tropval,12,nyrs)
shemval=REFORM(shemval,12,nyrs)
FOR yy=0,nyrs-1 DO BEGIN
  subarr=globval(*,yy)
  gots=WHERE(subarr NE mdi,count)
  IF (count GT 8) THEN rawarr(0,yy)=MEAN(subarr(gots))	; at least 9 months present
  subarr=nhemval(*,yy)
  gots=WHERE(subarr NE mdi,count)
  IF (count GT 8) THEN rawarr(1,yy)=MEAN(subarr(gots))	; at least 9 months present
  subarr=tropval(*,yy)
  gots=WHERE(subarr NE mdi,count)
  IF (count GT 8) THEN rawarr(2,yy)=MEAN(subarr(gots))	; at least 9 months present
  subarr=shemval(*,yy)
  gots=WHERE(subarr NE mdi,count)
  IF (count GT 8) THEN rawarr(3,yy)=MEAN(subarr(gots))	; at least 9 months present  
ENDFOR


;---------------------------------------------------------
; open gridbox trend files file

filee=NCDF_OPEN(inhomogmp)
longs_varid=NCDF_VARID(filee,'longitude')
lats_varid=NCDF_VARID(filee,'latitude')

CASE param OF
  'dpd': qid=NCDF_VARID(filee,'DPD_MPtrend') 	; may become uncertainty fields
  'td': qid=NCDF_VARID(filee,'Td_MPtrend') 	; may become uncertainty fields
  't': qid=NCDF_VARID(filee,'T_MPtrend') 	; may become uncertainty fields
  'tw': qid=NCDF_VARID(filee,'Tw_MPtrend') 	; may become uncertainty fields
  'q': qid=NCDF_VARID(filee,'q_MPtrend') 	; may become uncertainty fields
  'rh': qid=NCDF_VARID(filee,'RH_MPtrend') 	; may become uncertainty fields
  'e': qid=NCDF_VARID(filee,'e_MPtrend') 	; may become uncertainty fields
ENDCASE

NCDF_VARGET,filee,qid,q1_trend
NCDF_CLOSE,filee

;print,inoldmp

IF (typee EQ 'RAW') THEN BEGIN 
  filee=NCDF_OPEN(inrawmp) 
ENDIF ELSE BEGIN
  filee=NCDF_OPEN(inoldmp)
ENDELSE
longs_varid=NCDF_VARID(filee,'longitude')
lats_varid=NCDF_VARID(filee,'latitude')
;longs_varid=NCDF_VARID(filee,'lon')
;lats_varid=NCDF_VARID(filee,'lat')

CASE param OF
  'dpd': qid=NCDF_VARID(filee,'DPD_MPtrend') 	; may become uncertainty fields
  'td': qid=NCDF_VARID(filee,'Td_MPtrend') 	; may become uncertainty fields
  't': qid=NCDF_VARID(filee,'T_MPtrend') 	; may become uncertainty fields
  'tw': qid=NCDF_VARID(filee,'Tw_MPtrend') 	; may become uncertainty fields
  'q': qid=NCDF_VARID(filee,'q_MPtrend') 	; may become uncertainty fields
  'rh': qid=NCDF_VARID(filee,'RH_MPtrend') 	; may become uncertainty fields
  'e': qid=NCDF_VARID(filee,'e_MPtrend') 	; may become uncertainty fields
ENDCASE
NCDF_VARGET,filee,qid,q2_trend
NCDF_CLOSE,filee

diffs=make_array(nlons,nlats,/float,value=mdi)
gots=WHERE(q1_trend NE mdi AND q2_trend NE mdi,countgots)
diffs(gots)=q1_trend(gots)-q2_trend(gots)
ratios=make_array(nlons,nlats,/float,value=mdi)	
;raw/homog 
;1+ = raw greater than homog and same sign
;0to1 = raw closer to zero than homog and same sign
;-1to0 = raw closer to zero than homog and opposite sign
;-1+ = raw greater than homog and opposite sign

ratios(gots)=q2_trend(gots)/q1_trend(gots)

  set_plot,'PS'
  
  device,filename=outfile,/color,/ENCAPSUL,xsize=26,ysize=20,/landscape,/helvetica,/bold
  !P.Font=0
  !P.Thick=4
  plotsym,0,0.55,/fill


;; *** WATERMARK
;tvlct,230,230,230,100
;XYOUTS,0.5,0.5,'DRAFT',/normal,color=100,charsize=16,alignment=0.5,orientation=30

CASE param OF
  'dpd': BEGIN
    kcolsarrST=[255,2,5,7,9,10,12,14,17]	; 14 colours + black to ensure no botching
    levsarrST=[-2e+30,-500.,-2.,-1.0,-0.5,0.0,0.5,1.0,2.0,100]
  END
  'td': BEGIN
    kcolsarrST=[255,2,5,7,9,10,12,14,17]	; 14 colours + black to ensure no botching
    levsarrST=[-2e+30,-500.,-2.,-1.0,-0.5,0.0,0.5,1.0,2.0,100]
  END
  't': BEGIN
    kcolsarrST=[255,2,5,7,9,10,12,14,17]	; 14 colours + black to ensure no botching
    levsarrST=[-2e+30,-500.,-2.,-1.0,-0.5,0.0,0.5,1.0,2.0,100]
  END
  'tw': BEGIN
    kcolsarrST=[255,2,5,7,9,10,12,14,17]	; 14 colours + black to ensure no botching
    levsarrST=[-2e+30,-500.,-2.,-1.0,-0.5,0.0,0.5,1.0,2.0,100]
  END
  'q': BEGIN
    kcolsarrST=[255,2,5,7,9,10,12,14,17]	; 14 colours + black to ensure no botching
    levsarrST=[-2e+30,-500.,-2.,-1.0,-0.5,0.0,0.5,1.0,2.0,100]
  END
  'rh': BEGIN
    kcolsarrST=[255,2,5,7,9,10,12,14,17]	; 14 colours + black to ensure no botching
    levsarrST=[-2e+30,-500.,-2.,-1.0,-0.5,0.0,0.5,1.0,2.0,100]
  END
  'e': BEGIN
    kcolsarrST=[255,2,5,7,9,10,12,14,17]	; 14 colours + black to ensure no botching
    levsarrST=[-2e+30,-500.,-2.,-1.0,-0.5,0.0,0.5,1.0,2.0,100]
  END

ENDCASE

;kcolsarrST=[100,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]	; 14 colours + black to ensure no botching
;kcolsarrST=[255,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]	; 14 colours + black to ensure no botching
;DIFFS
;levsarrST=[-2e+30,-0.4,-0.35,-0.3,-0.25,-0.2,-0.15,-0.1,-0.05,-0.01,  0.0  ,0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,10]
;RATIONS
;levsarrST=[-2e+30,-500.,-10.,-5.0,-2.,-1.5,-1.0,-0.75,-0.5,-0.25,0.0,0.25,0.5,0.75,1.0,1.5,2.0,5.0,10.,100]




; colour settings - Uni ORegon blue to red
tvlct,0,0,0,0
tvlct,240,240,240,100
tvlct,200,200,200,120

ncols=n_elements(kcolsarrST)
colsarrST=kcolsarrST(1:ncols-1)
nlevs=n_elements(levsarrST)-1
labsarrST=strarr(nlevs)
labsarrST(0)=''
labsarrST((nlevs-1))=''
labsarrST(1:nlevs-2)=string(levsarrST(2:nlevs-1),format='(f5.2)')
;------------------------------------------------------------------------------------

;  tvlct,10,0,0,1
;  tvlct,20,1,0,2
;  tvlct,30,5,0,3
;  tvlct,51,25,0,4
;  tvlct,102,47,0,5
;  tvlct,153,96,53,6
;  tvlct,204,155,122,7
;  tvlct,216,175,151,8
;  tvlct,242,218,205,9
;  tvlct,204,253,255,10
;  tvlct,153,248,255,11
;  tvlct,101,239,255,12
;  tvlct,50,227,255,13
;  tvlct,0,169,204,14
;  tvlct,0,122,153,15
;  tvlct,0,75,100,16
;  tvlct,0,40,80,17
;  tvlct,0,10,40,18

tvlct,153,15,15,2
tvlct,178,44,44,5
tvlct,229,126,126,7
tvlct,255,178,178,9

tvlct,191,178,255,10
tvlct,143,126,229,12
tvlct,66,44,178,14
tvlct,38,15,153,17


!P.Position=[0.04,0.52,0.44,0.93]

;!P.Position=[0.03,0.06,0.25,0.46]
;!P.Position=[0.28,0.06,0.50,0.46]

;!P.Position=[0.55,0.735,0.97,0.96]
;!P.Position=[0.55,0.51,0.97,0.735]
;!P.Position=[0.55,0.285,0.97,0.51]
;!P.Position=[0.55,0.06,0.97,0.285]

Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2


;boxfill,diffs,lons,lats,colors=kcolsarrST,levels=levsarrST	    ;,nofill_color=kcolsarrT(0)
boxfill,ratios,lons,lats,colors=kcolsarrST,levels=levsarrST	    ;,nofill_color=kcolsarrT(0)
     
; Overplot continents and islands again
Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

IF (typee EQ 'RAW') THEN BEGIN
  ;XYOUTS,0.24,0.95,'Homogenised-Raw',/normal,alignment=0.5,charsize=1.2
  XYOUTS,0.24,0.94,'Ratio of Raw to Homogenised',/normal,alignment=0.5,charsize=1.2
ENDIF ELSE BEGIN
  XYOUTS,0.24,0.94,'Ratio of '+oldversion+' to '+version,/normal,alignment=0.5,charsize=1.2
ENDELSE

PLOTS,[-179.9,0],[89.9,89.9],color=0
PLOTS,[0,179.9],[89.9,89.9],color=0
PLOTS,[-179.9,0],[-89.9,-89.9],color=0
PLOTS,[0,179.9],[-89.9,-89.9],color=0

MAKE_KEY,0.45,0.54,0.015,0.37,0.02,-0.007,/NORMAL,COLORS=colsarrST,labels=labsarrST,$
         charsize=1.,charthick=4,bcolor=0,orientation=1
;XYOUTS,0.475,0.97,'g/kg/decade',/normal,color=0,charsize=1.1,alignment=0.5
XYOUTS,0.475,0.92,'ratio',/normal,color=0,charsize=1.1,alignment=0.5

XYOUTS,0.5,0.97,variname,/normal,color=0,charsize=1.5,alignment=0.5

XYOUTS,0.01,0.93,'a)',/normal,color=0,charsize=1.2

!P.Position=[0.06,0.1,0.25,0.46]

  tvlct,0,122,153,15

  minx=FLOOR(MIN(q1_trend(WHERE(q1_trend NE mdi))))
  maxx=CEIL(MAX(q1_trend))
  miny=(FLOOR(MIN(q2_trend(WHERE(q2_trend NE mdi)))*10.))/10.
  maxy=(CEIL(MAX(q2_trend)*10.))/10.

  IF (typee EQ 'RAW') THEN BEGIN
    ytitlee='Raw trends ('+unitees+' decade!E-1!N)'
    xtitlee='Homogenised trends ('+unitees+' decade!E-1!N)'
  ENDIF ELSE BEGIN
    ytitlee=oldversion+' trends ('+unitees+' decade!E-1!N)'
    xtitlee=version+' trends ('+unitees+' decade!E-1!N)'
  ENDELSE
  plot,q1_trend(gots),q2_trend(gots),min_value=-100,psym=8,symsize=0.8,yrange=[miny,maxy],xrange=[miny,maxy],ystyle=1,xstyle=1,$
       ytitle=ytitlee,xtitle=xtitlee,charsize=1,/noerase
  
  PLOTS,[0,0],[miny,maxy],color=15,thick=4
  PLOTS,[miny,maxy],[0,0],color=15,thick=4
  PLOTS,[miny,maxy],[miny,maxy],color=120,linestyle=2,thick=4

  comps=WHERE(q1_trend(gots) GE 0. AND q2_trend(gots) GE 0.,counthappywet)
  comps=WHERE(q1_trend(gots) LT 0. AND q2_trend(gots) LT 0.,counthappydry)
  comps=WHERE(q1_trend(gots) LT 0. AND q2_trend(gots) GE 0.,countsaddry)
  comps=WHERE(q1_trend(gots) GE 0. AND q2_trend(gots) LT 0.,countsadwet)
  
  print,countgots
  print,'WET WET: ',counthappywet,(FLOAT(counthappywet)/countgots)*100.
  print,'DRY DRY: ',counthappydry,(FLOAT(counthappydry)/countgots)*100.
  print,'DRY WET: ',countsaddry,(FLOAT(countsaddry)/countgots)*100.
  print,'WET DRY: ',countsadwet,(FLOAT(countsadwet)/countgots)*100.
  
  
  XYOUTS,0.23,0.43,string(((FLOAT(counthappywet)/countgots)*100.),format='(f4.1)')+'%',/normal,color=0,charsize=1.1,alignment=1
  XYOUTS,0.23,0.11,string(((FLOAT(countsadwet)/countgots)*100.),format='(f4.1)')+'%',/normal,color=0,charsize=1.1,alignment=1
  XYOUTS,0.07,0.11,string(((FLOAT(counthappydry)/countgots)*100.),format='(f4.1)')+'%',/normal,color=0,charsize=1.1,alignment=0
  XYOUTS,0.07,0.43,string(((FLOAT(countsaddry)/countgots)*100.),format='(f4.1)')+'%',/normal,color=0,charsize=1.1,alignment=0

XYOUTS,0.01,0.47,'b)',/normal,color=0,charsize=1.2

; overplotted histograms of trends

!P.Position=[0.31,0.1,0.50,0.46]

  minx=(FLOOR((MIN([MIN(q1_trend(gots)),MIN(q2_trend(gots))])*10.))/10.)-0.1
  maxx=(CEIL((MAX([MAX(q1_trend(gots)),MAX(q2_trend(gots))])*10.))/10.)+0.1
  numbins=(maxx-minx)/0.1
  hist1=HISTOGRAM(q1_trend(gots),min=minx,binsize=0.1,nbins=numbins)
  hist2=HISTOGRAM(q2_trend(gots),min=minx,binsize=0.1,nbins=numbins)
  xarr=(dindgen(numbins)*0.1)+minx
  
  ymax=MAX([hist1,hist2])+10
  
  plot,xarr,hist1,psym=-5,symsize=0.5,min_value=0.01,yrange=[-10,ymax],ystyle=1,xstyle=1,$
       ytitle='No. gridboxes',$
       xtitle='Trend ('+unitees+' decade!E-1!N)',charsize=1,thick=4,/noerase
  oplot,xarr,hist2,symsize=0.5,psym=-5,min_value=0.01,color=15,thick=4
  
  PLOTS,[0,0],[-10,ymax],color=0,thick=4
  IF (typee EQ 'RAW') THEN BEGIN
    XYOUTS,0.32,0.44,'Homogenised',/normal,color=0,charsize=1.
    XYOUTS,0.32,0.42,'Raw',/normal,color=15,charsize=1.
  ENDIF ELSE BEGIN
    XYOUTS,0.32,0.44,version,/normal,color=0,charsize=1.
    XYOUTS,0.32,0.42,oldversion,/normal,color=15,charsize=1.
  ENDELSE
  XYOUTS,0.26,0.47,'c)',/normal,color=0,charsize=1.2


;-------------------------------------
;the time series plots
tvlct,0,0,0,0		;black			; HadCRUH2
tvlct,0,122,153,15	;blue (same as hist plot)

; YEAR***
fulltims=indgen(nyrs+1)
zeros=intarr(nyrs+1)

CASE param OF
  'dpd': BEGIN
    ymax=1			;YEAR***
    ymin=-1 		;YEAR***
  END
  'td': BEGIN
    ymax=1			;YEAR***
    ymin=-1 		;YEAR***
  END
  't': BEGIN
    ymax=1.2			;YEAR***
    ymin=-1 		;YEAR***
  END
  'tw': BEGIN
    ymax=1			;YEAR***
    ymin=-1 		;YEAR***
  END
  'q': BEGIN
    ymax=1			;YEAR***
    ymin=-1 		;YEAR***
  END
  'rh': BEGIN
    ymax=2.5			;YEAR***
    ymin=-2.5 		;YEAR***
  END
  'e': BEGIN
    ymax=1			;YEAR***
    ymin=-1 		;YEAR***
  END
ENDCASE
yyrange=ymax-ymin

allnames=['1975','1980','1985','1990','1995','2000','2005','2010','2015']

!P.Position=[0.57,0.735,0.99,0.96]
plot,fulltims,zeros,min_value=-100,ystyle=1,xstyle=5,yrange=[ymin,ymax],ythick=4,charsize=0.9,$
     ytitle='anomalies ('+unitees+')',charthick=1,color=0,/noerase,thick=4,/nodata	
oplot,fulltims(0:nyrs),zeros,min_value=-100,color=0,thick=1
oplot,fulltims(0:nyrs-1),homogarr(0,*),min_value=-100,color=0,thick=4
oplot,fulltims(0:nyrs-1),rawarr(0,*),min_value=-100,color=15,linestyle=1,thick=6		; YEAR***	HadISDH
PLOTS,[0,nyrs],[ymax,ymax],color=0	; YEAR***
PLOTS,[0,nyrs],[ymin,ymin],color=0	; YEAR***
FOR tt=1,nyrs-1 DO BEGIN
  IF (((tt+3.)/5.)-FLOOR(((tt+3.)/5.)) GT 0.) THEN BEGIN
    PLOTS,[tt,tt],[ymin,ymin*0.97],color=0,thick=4 
    PLOTS,[tt,tt],[ymax,ymax*0.97],color=0,thick=4 
  ENDIF ELSE BEGIN
    PLOTS,[tt,tt],[ymin,ymin*0.94],color=0,thick=4
    PLOTS,[tt,tt],[ymax,ymax*0.94],color=0,thick=4
  ENDELSE
ENDFOR

XYOUTS,0.78,0.93,'GLOBE (70S-70N)',/normal,alignment=0.5,color=0,charsize=1.
XYOUTS,0.52,0.94,'d)',/normal,color=0,charsize=1.2
IF (typee EQ 'RAW') THEN BEGIN
  XYOUTS,0.58,0.935,'Homogenised',/normal,color=0,charsize=1.
  XYOUTS,0.58,0.915,'Raw (dotted)',/normal,color=15,charsize=1.
ENDIF ELSE BEGIN
  XYOUTS,0.58,0.935,version,/normal,color=0,charsize=1.
  XYOUTS,0.58,0.915,oldversion+' (dotted)',/normal,color=15,charsize=1.
ENDELSE
trend=median_pairwise(homogarr(0,*),mdi,se,lc,uc)
XYOUTS,0.58,0.765,string(trend*10.,format='(f5.2)')+' '+unitees+' decade!E-1!N ('+string(lc*10.,format='(f5.2)')+$
                 ' to '+string(uc*10.,format='(f5.2)')+')',/normal,color=0,charsize=1,alignment=0
trend=median_pairwise(rawarr(0,*),mdi,se,lc,uc)
XYOUTS,0.58,0.745,string(trend*10.,format='(f5.2)')+' '+unitees+' decade!E-1!N ('+string(lc*10.,format='(f5.2)')+$
                 ' to '+string(uc*10.,format='(f5.2)')+')',/normal,color=15,charsize=1,alignment=0

!P.Position=[0.57,0.51,0.99,0.735]
plot,fulltims,zeros,min_value=-100,ystyle=1,xstyle=5,yrange=[ymin,ymax],ythick=4,charsize=0.9,$
     ytitle='anomalies ('+unitees+')',charthick=1,color=0,/noerase,thick=4,/nodata	
oplot,fulltims(0:nyrs),zeros,min_value=-100,color=0,thick=1
oplot,fulltims(0:nyrs-1),homogarr(1,*),min_value=-100,color=0,thick=4
oplot,fulltims(0:nyrs-1),rawarr(1,*),min_value=-100,color=15,linestyle=1,thick=6		; YEAR***	HadISDH
PLOTS,[0,nyrs],[ymax,ymax],color=0	; YEAR***
PLOTS,[0,nyrs],[ymin,ymin],color=0	; YEAR***
FOR tt=1,nyrs-1 DO BEGIN
  IF (((tt+3.)/5.)-FLOOR(((tt+3.)/5.)) GT 0.) THEN BEGIN
    PLOTS,[tt,tt],[ymin,ymin*0.97],color=0,thick=4 
    PLOTS,[tt,tt],[ymax,ymax*0.97],color=0,thick=4 
  ENDIF ELSE BEGIN
    PLOTS,[tt,tt],[ymin,ymin*0.94],color=0,thick=4
    PLOTS,[tt,tt],[ymax,ymax*0.94],color=0,thick=4
  ENDELSE
ENDFOR

XYOUTS,0.78,0.705,'N. HEMISPHERE (20N-70N)',/normal,alignment=0.5,color=0,charsize=1.
XYOUTS,0.52,0.715,'e)',/normal,color=0,charsize=1.2
trend=median_pairwise(homogarr(1,*),mdi,se,lc,uc)
XYOUTS,0.58,0.54,string(trend*10.,format='(f5.2)')+' '+unitees+' decade!E-1!N ('+string(lc*10.,format='(f5.2)')+$
                 ' to '+string(uc*10.,format='(f5.2)')+')',/normal,color=0,charsize=1,alignment=0
trend=median_pairwise(rawarr(1,*),mdi,se,lc,uc)
XYOUTS,0.58,0.52,string(trend*10.,format='(f5.2)')+' '+unitees+' decade!E-1!N ('+string(lc*10.,format='(f5.2)')+$
                 ' to '+string(uc*10.,format='(f5.2)')+')',/normal,color=15,charsize=1,alignment=0

!P.Position=[0.57,0.285,0.99,0.51]
plot,fulltims,zeros,min_value=-100,ystyle=1,xstyle=5,yrange=[ymin,ymax],ythick=4,charsize=0.9,$
     ytitle='anomalies ('+unitees+')',charthick=1,color=0,/noerase,thick=4,/nodata	
oplot,fulltims(0:nyrs),zeros,min_value=-100,color=0,thick=1
oplot,fulltims(0:nyrs-1),homogarr(2,*),min_value=-100,color=0,thick=4
oplot,fulltims(0:nyrs-1),rawarr(2,*),min_value=-100,color=15,linestyle=1,thick=6		; YEAR***	HadISDH
PLOTS,[0,nyrs],[ymax,ymax],color=0	; YEAR***
PLOTS,[0,nyrs],[ymin,ymin],color=0	; YEAR***
FOR tt=1,nyrs-1 DO BEGIN
  IF (((tt+3.)/5.)-FLOOR(((tt+3.)/5.)) GT 0.) THEN BEGIN
    PLOTS,[tt,tt],[ymin,ymin*0.97],color=0,thick=4 
    PLOTS,[tt,tt],[ymax,ymax*0.97],color=0,thick=4 
  ENDIF ELSE BEGIN
    PLOTS,[tt,tt],[ymin,ymin*0.94],color=0,thick=4
    PLOTS,[tt,tt],[ymax,ymax*0.94],color=0,thick=4
  ENDELSE
ENDFOR

XYOUTS,0.78,0.48,'TROPICS (20S-20N)',/normal,alignment=0.5,color=0,charsize=1.
XYOUTS,0.52,0.49,'f)',/normal,color=0,charsize=1.2
trend=median_pairwise(homogarr(2,*),mdi,se,lc,uc)
XYOUTS,0.58,0.315,string(trend*10.,format='(f5.2)')+' '+unitees+' decade!E-1!N ('+string(lc*10.,format='(f5.2)')+$
                 ' to '+string(uc*10.,format='(f5.2)')+')',/normal,color=0,charsize=1,alignment=0
trend=median_pairwise(rawarr(2,*),mdi,se,lc,uc)
XYOUTS,0.58,0.295,string(trend*10.,format='(f5.2)')+' '+unitees+' decade!E-1!N ('+string(lc*10.,format='(f5.2)')+$
                 ' to '+string(uc*10.,format='(f5.2)')+')',/normal,color=15,charsize=1,alignment=0

!P.Position=[0.57,0.06,0.99,0.285]
plot,fulltims,zeros,min_value=-100,ystyle=1,xstyle=5,yrange=[ymin,ymax],ythick=4,charsize=0.9,$
     ytitle='anomalies ('+unitees+')',charthick=1,color=0,/noerase,thick=4,/nodata	
oplot,fulltims(0:nyrs),zeros,min_value=-100,color=0,thick=1
oplot,fulltims(0:nyrs-1),homogarr(3,*),min_value=-100,color=0,thick=4
oplot,fulltims(0:nyrs-1),rawarr(3,*),min_value=-100,color=15,linestyle=1,thick=6		; YEAR***	HadISDH
PLOTS,[0,nyrs],[ymax,ymax],color=0	; YEAR***
PLOTS,[0,nyrs],[ymin,ymin],color=0	; YEAR***
yrcount=0
FOR tt=1,nyrs-1 DO BEGIN
  IF (((tt+3.)/5.)-FLOOR(((tt+3.)/5.)) GT 0.) THEN BEGIN
    PLOTS,[tt,tt],[ymin,ymin*0.97],color=0,thick=4 
    PLOTS,[tt,tt],[ymax,ymax*0.97],color=0,thick=4 
  ENDIF ELSE BEGIN
    PLOTS,[tt,tt],[ymin,ymin*0.94],color=0,thick=4
    PLOTS,[tt,tt],[ymax,ymax*0.94],color=0,thick=4
    XYOUTS,tt,ymin*1.2,allnames(yrcount),alignment=0.5,color=0,charsize=1.
    yrcount=yrcount+1
  ENDELSE
ENDFOR
XYOUTS,0.78,0.01,'YEAR',/normal,alignment=0.5,charsize=1.1,color=0

XYOUTS,0.78,0.255,'S. HEMISPHERE (70S-20S)',/normal,alignment=0.5,color=0,charsize=1.
XYOUTS,0.52,0.265,'g)',/normal,color=0,charsize=1.2
trend=median_pairwise(homogarr(3,*),mdi,se,lc,uc)
XYOUTS,0.58,0.09,string(trend*10.,format='(f5.2)')+' '+unitees+' decade!E-1!N ('+string(lc*10.,format='(f5.2)')+$
                 ' to '+string(uc*10.,format='(f5.2)')+')',/normal,color=0,charsize=1,alignment=0
trend=median_pairwise(rawarr(3,*),mdi,se,lc,uc)
XYOUTS,0.58,0.07,string(trend*10.,format='(f5.2)')+' '+unitees+' decade!E-1!N ('+string(lc*10.,format='(f5.2)')+$
                 ' to '+string(uc*10.,format='(f5.2)')+')',/normal,color=15,charsize=1,alignment=0


device,/close

end
