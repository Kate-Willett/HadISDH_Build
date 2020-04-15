; TIDL
; 
; Author: Kate Willett
; Created: 1 February 2013
; Last update: 14 February 2018
; Location: /data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/HADISDH_BUILD/	
; GitHub: https://github.com/Kate-Willett/HadISDH_Build					
; -----------------------
; CODE PURPOSE AND OUTPUT
; -----------------------
; Reads in a gridded dataset and outputs a decadal trend for each gridbox over the desired period.
; 
; <references to related published material, e.g. that describes data set>
; 
; -----------------------
; LIST OF MODULES
; -----------------------
; .compile median_pairwise.pro
; 
; -----------------------
; DATA
; -----------------------
; Input gridded netCDF file of monthly mean values
; /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/HadISDH.land<Var>.'+version+'_FLATgrid<homogtype>PHA5by5_anoms7605_JAN2017
; 
; -----------------------
; HOW TO RUN THE CODE
; -----------------------
; Check you've got the desired year, clims, working files, variable, homogtype etc
; >tidl
; >.compile median_pairwise
; >.compile make_MP_trends
; >make_MP_trends,param,homogtype
;; Which variable?
;param = 'dpd'	;'dpd','td','t','tw','e','q','rh'
;
;; Which homog type?
;homogtype = 'PHA'	;'PHA','ID','DPD', 'RAW','OTHER', 'BLEND', 'MARINE'
; 
; -----------------------
; OUTPUT
; -----------------------
; Output netCDF file of gridbox decadal trends
; /data/local/hadkw/HADCRUH2/UPDATE2016/STATISTICS/HadISDH.land<Var>.'+version+'_FLATgrid<homogtype>PHA5by5_JAN2014_anoms7605_MPtrends_19732016.nc
; 
; -----------------------
; VERSION/RELEASE NOTES
; -----------------------
;
; Version 3 (15 February 2018)
; ---------
;  
; Enhancements
; Now variable and homogtype are called from the command line - param, homogtype
; param = 'dpd'	;'dpd','td','t','tw','e','q','rh'
; homogtype = 'PHA'	;'PHA','ID','DPD', 'RAW','OTHER', 'BLEND', 'MARINE'
; 
; Version 2 (1 February 2017)
; ---------
;  
; Enhancements
; General tidy up of code and EDITABLES
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
pro make_MP_trends,param,homogtype
;; Which variable?
;param = 'dpd'	;'dpd','td','t','tw','e','q','rh'
;
;; Which homog type?
;homogtype = 'PHA'	;'PHA','ID','DPD', 'RAW','OTHER', 'BLEND', 'MARINE', 'MARINEship'

; to calculate trends - NO missing data tolerance - need a land/sea mask for that

;based on kate_timeseries.pro - WAVE for ICOADS

; written by Kate Willett
; last modified JUL 2012

; could use gridbox standard deviations or uncertainties
;   fit trend to val+unc and val-unc - look at differences
;   bootstrap 100+ timeseries randomly picking out values between val+/-unc, fit trends
;   ENSURE THERE IS A MAXMAX AND MINMIN timeseries?

;---------------------------------------------------
; EDITABLES
; set up directories and filenames

; Which start/end year?
styr = 1973	; 1973
edyr = 2018

; Which climatology period to work with?
climST = 1981 	;1976 or 1981
climED = 2010	;2005 or 2010
climBIT = 'anoms'+strmid(strcompress(climST,/remove_all),2,2)+strmid(strcompress(climED,/remove_all),2,2)

; Which TREND start/end year?
sttrd = 1973  	; years over which to calculate trends
edtrd = 2018  	;

; Which working file dates?
nowmon   = 'APR'
nowyear  = '2019'
thenmon  = 'FEB'
thenyear = '2019'

;; Which variable?
;param = 'dpd'	;'dpd','td','t','tw','e','q','rh';;
;
;; Which homog type?
;homogtype = 'MARINEship'	;'PHA','ID','DPD', 'RAW','OTHER', 'BLEND', 'MARINE'

; Which version (if not marine or OTHER???)
;version = '4.1.0.2018f'
version = '1.0.0.2018f'

workingdir = '/data/users/hadkw/WORKING_HADISDH/UPDATE20'+strmid(strcompress(edyr,/remove_all),2,2)

indir  = workingdir+'/STATISTICS/'
outdir = workingdir+'/STATISTICS/'
IF (homogtype EQ 'OTHER') THEN BEGIN
    indir  = workingdir+'/OTHERDATA/'
    outdir = workingdir+'/OTHERDATA/'
ENDIF ;ELSE IF (homogtype EQ 'MARINE') THEN BEGIN
;    indir  = workingdir+'/OTHERDATA/'
;;    indir = '/project/hadobs2/hadisdh/marine/ICOADS.2.5.1/GRIDS3/'
;    outdir = '/data/users/hadkw/WORKING_HADISDH/MARINE/DATA/'
;ENDIF

CASE param OF
  'dpd': BEGIN
    param2 = 'DPD'	;'DPD','Td','T','Tw','e','q','RH'
    unitees = 'deg C'
    IF (homogtype EQ 'PHA') THEN infile    = 'HadISDH.landDPD.'+version+'_FLATgridPHA5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'RAW') THEN infile    = 'HadISDH.landDPD.'+version+'_FLATgridRAW5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineDPD.'+version+'_BClocal5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineDPD.'+version+'_BClocalSHIP5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
  END
  'td': BEGIN
    param2 = 'Td'	;'DPD','Td','T','Tw','e','q','RH'
    unitees = 'deg C'
    IF (homogtype EQ 'PHA') THEN infile    = 'HadISDH.landTd.'+version+'_FLATgridPHA5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'DPD') THEN infile    = 'HadISDH.landTd.'+version+'_FLATgridPHADPD5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'RAW') THEN infile    = 'HadISDH.landTd.'+version+'_FLATgridRAW5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineTd.'+version+'_BClocal5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineTd.'+version+'_BClocalSHIP5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
  END
  't': BEGIN
    param2 = 'T'	;'DPD','Td','T','Tw','e','q','RH'
    unitees = 'deg C'
    IF (homogtype EQ 'ID') THEN infile     = 'HadISDH.landT.'+version+'_FLATgridIDPHA5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'RAW') THEN infile    = 'HadISDH.landT.'+version+'_FLATgridRAW5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineT.'+version+'_BClocal5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineT.'+version+'_BClocalSHIP5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'BLEND') THEN infile  = 'BLEND_HadISDH.landT.2.1.0.2015p.marineT.QC0.0.0_OCT2016'
    IF (homogtype EQ 'OTHER') THEN infile  = 'GISS_T_5by519762005clim_anoms_19732014'
;    IF (homogtype EQ 'OTHER') THEN infile  = 'BERKELEY_T_5by519762005clim_anoms_19732014'
;    IF (homogtype EQ 'OTHER') THEN infile  = 'CRUTEM.4.3.0.0.anomalies'
;    IF (homogtype EQ 'OTHER') THEN infile  = 'HadCRUT.4.3.0.0.median'
;    IF (homogtype EQ 'OTHER') THEN infile  = 'GHCNM_18802014'
  END
  'tw': BEGIN
    param2 = 'Tw'	;'DPD','Td','T','Tw','e','q','RH'
    unitees = 'deg C'
    IF (homogtype EQ 'ID') THEN infile     = 'HadISDH.landTw.'+version+'_FLATgridIDPHA5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'RAW') THEN infile    = 'HadISDH.landTw.'+version+'_FLATgridRAW5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineTw.'+version+'_BClocal5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineTw.'+version+'_BClocalSHIP5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
  END
  'q': BEGIN
    param2 = 'q'	;'DPD','Td','T','Tw','e','q','RH'
    unitees = 'g/kg'
    IF (homogtype EQ 'ID') THEN infile     = 'HadISDH.landq.'+version+'_FLATgridIDPHA5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'PHA') THEN infile    = 'HadISDH.landq.'+version+'_FLATgridPHA5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'RAW') THEN infile    = 'HadISDH.landq.'+version+'_FLATgridRAW5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineq.'+version+'_BClocal5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineq.'+version+'_BClocalSHIP5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'BLEND') THEN infile  = 'BLEND_HadISDH.landq.2.1.0.2015p.marineq.QC0.0.0_OCT2016'
  END
  'e': BEGIN
    param2 = 'e'	;'DPD','Td','T','Tw','e','q','RH'
    unitees = 'hPa'
    IF (homogtype EQ 'ID') THEN infile     = 'HadISDH.lande.'+version+'_FLATgridIDPHA5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'RAW') THEN infile    = 'HadISDH.lande.'+version+'_FLATgridRAW5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marinee.'+version+'_BClocal5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marinee.'+version+'_BClocalSHIP5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
  END
  'rh': BEGIN
    param2 = 'RH'	;'DPD','Td','T','Tw','e','q','RH'
    unitees = '%rh'
    IF (homogtype EQ 'ID') THEN infile     = 'HadISDH.landRH.'+version+'_FLATgridIDPHA5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'PHA') THEN infile    = 'HadISDH.landRH.'+version+'_FLATgridPHA5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'RAW') THEN infile    = 'HadISDH.landRH.'+version+'_FLATgridRAW5by5_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINE') THEN infile = 'HadISDH.marineRH.'+version+'_BClocal5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'MARINEship') THEN infile = 'HadISDH.marineRH.'+version+'_BClocalSHIP5by5both_'+climBIT+'_'+thenmon+thenyear+'_cf'
    IF (homogtype EQ 'BLEND') THEN infile  = 'BLEND_HadISDH.landRH.2.1.0.2015p.marineRH.QC0.0.0_OCT2016'
  END
  
ENDCASE
ofile=infile+'_MPtrends_'+strcompress(sttrd,/remove_all)+strcompress(edtrd,/remove_all)	;70S-70N

;--------------------------------------------------
; variables and arrays
mdi = -1e+30

latlg = 5.
lonlg = 5.
stlt  = -90+(latlg/2.)
stln  = -180+(lonlg/2.)
nlats = 180/latlg
nlons = 360/lonlg
nbox  = LONG(nlats*nlons)

trdst = (sttrd-styr)*12	; zero if 1973
trded = (((edtrd+1)-styr)*12)-1	; zero if 1973
;setting trend years and mons which will replace actual
nyrs = (edtrd+1)-sttrd
nmons = nyrs*12

;nyrs     = (edyr+1)-styr
;nmons    = nyrs*12
;int_mons = indgen(nmons)

print,trdst,trded,nyrs,nmons

nboots = 100
int_boots = indgen(nboots)

lats = (findgen(nlats)*latlg)+stlt
lons = (findgen(nlons)*lonlg)+stln

trendvals      = make_array(nlons,nlats,/float,value=mdi)	;trend
trendvalsU     = make_array(nlons,nlats,/float,value=mdi)	;95th pct
trendvalsL     = make_array(nlons,nlats,/float,value=mdi)	;5th pct
boottrendvals  = make_array(nlons,nlats,nboots,/float,value=mdi)
boottrendvalsU = make_array(nlons,nlats,nboots,/float,value=mdi)
boottrendvalsL = make_array(nlons,nlats,nboots,/float,value=mdi)

;----------------------------------------------------
; read in files

IF (homogtype EQ 'OTHER') THEn BEGIN ;OR (homogtype EQ 'MARINE') THEN BEGIN ;
  filee = NCDF_OPEN(indir+infile+'.nc')
ENDIF ELSE BEGIN 
  filee = NCDF_OPEN(indir+'GRIDS/'+infile+'.nc')
ENDELSE

IF (homogtype EQ 'BLEND') THEN timvarid = NCDF_VARID(filee,'times') ELSE timvarid = NCDF_VARID(filee,'time')

IF (homogtype EQ 'OTHER') THEN BEGIN
  longs_varid = NCDF_VARID(filee,'lon')
  lats_varid  = NCDF_VARID(filee,'lat')
ENDIF ELSE BEGIN
  longs_varid = NCDF_VARID(filee,'longitude')
  lats_varid  = NCDF_VARID(filee,'latitude')
ENDELSE

IF (homogtype EQ 'OTHER') THEN BEGIN
  qvarid = NCDF_VARID(filee,'temperature_anomaly')
  ;qvarid = NCDF_VARID(filee,'anomalies')
ENDIF ;ELSE IF (homogtype EQ 'MARINE') THEN BEGIN
;  CASE param OF
;    'dpd': qvarid = NCDF_VARID(filee,'dew_point_depression_anomalies')
;    'td':  qvarid = NCDF_VARID(filee,'dew_point_temperature_anomalies')
;    't':   qvarid = NCDF_VARID(filee,'marine_air_temperature_anomalies')
;    'tw':  qvarid = NCDF_VARID(filee,'wet_bulb_temperature_anomalies')
;    'q':   qvarid = NCDF_VARID(filee,'specific_humidity_anomalies')
;    'rh':  qvarid = NCDF_VARID(filee,'relative_humidity_anomalies')
;    'e':   qvarid = NCDF_VARID(filee,'vapor_pressure_anomalies')
;  ENDCASE
;ENDIF ELSE IF (homogtype EQ 'BLEND') THEN BEGIN
;  CASE param OF
;    'dpd': qvarid = NCDF_VARID(filee,'blend_dpd_anoms')
;    'td':  qvarid = NCDF_VARID(filee,'blend_td_anoms')
;    't':   qvarid = NCDF_VARID(filee,'blend_t_anoms')
;    'tw':  qvarid = NCDF_VARID(filee,'blend_tw_anoms')
;    'q':   qvarid = NCDF_VARID(filee,'blend_q_anoms')
;    'rh':  qvarid = NCDF_VARID(filee,'blend_rh_anoms')
;    'e':   qvarid = NCDF_VARID(filee,'blend_e_anoms')
;  ENDCASE
;ENDIF ELSE BEGIN
  CASE param OF
    'dpd': qvarid = NCDF_VARID(filee,'dpd_anoms')
    'td':  qvarid = NCDF_VARID(filee,'td_anoms')
    't':   qvarid = NCDF_VARID(filee,'t_anoms')
    'tw':  qvarid = NCDF_VARID(filee,'tw_anoms')
    'q':   qvarid = NCDF_VARID(filee,'q_anoms')
    'rh':  qvarid = NCDF_VARID(filee,'rh_anoms')
    'e':   qvarid = NCDF_VARID(filee,'e_anoms')
  ENDCASE
;ENDELSE

NCDF_VARGET,filee,timvarid,times
NCDF_VARGET,filee,qvarid,q_values
NCDF_VARGET,filee,lats_varid,lats
NCDF_VARGET,filee,longs_varid,longs
NCDF_CLOSE,filee

q_values = q_values(*,*,trdst:trded)

;; If its marine data then we need to flip lats
;IF (homogtype EQ 'MARINE') THEN q_values = reverse(q_values,2)

;; If marine then the mdi seems to not work so double check
;IF (homogtype EQ 'MARINE') THEN BEGIN
  bads = where(q_values LT -100,count)
  if (count GT 0) THEN q_values(bads) = mdi
;ENDIF

;filee=NCDF_OPEN(dir+infile100+'.nc')
;timvarid=NCDF_VARID(filee,'times')
;longs_varid=NCDF_VARID(filee,'lon')
;lats_varid=NCDF_VARID(filee,'lat')
;qvarid=NCDF_VARID(filee,'qhum_anoms')
;NCDF_VARGET,filee,timvarid,times
;NCDF_VARGET,filee,qvarid,q_boots
;NCDF_CLOSE,filee

FOR lnn=0,nlons-1 DO BEGIN
  FOR ltt=0,nlats-1 DO BEGIN
    print,lnn,ltt
    gots = WHERE(q_values(lnn,ltt,*) NE mdi,countq)
    IF (countq GT nmons*0.7) THEN BEGIN
      trendvals(lnn,ltt)  = (median_pairwise(q_values(lnn,ltt,*),mdi,se,lc,uc))*120.	;decadal
      trendvalsU(lnn,ltt) = uc*120.
      trendvalsL(lnn,ltt) = lc*120.
;      FOR i=0,nboots-1 DO BEGIN
;;        print,i
;        boottrendvals(lnn,ltt,i)  = (median_pairwise(q_boots(lnn,ltt,*,i),mdi,se,lc,uc))*120.
;        boottrendvalsU(lnn,ltt,i) = (uc)*120.
;        boottrendvalsL(lnn,ltt,i) = (lc)*120.
;      ENDFOR    
    ENDIF
  ENDFOR
ENDFOR
  
;save to file;
;
IF (homogtype EQ 'OTHER') THEN filename = outdir+ofile+'.nc' $ ;OR (homogtype EQ 'MARINE') THEN filename = outdir+ofile+'.nc' $
    ELSE filename = outdir+'TRENDS/'+ofile+'.nc'
file_out = NCDF_CREATE(filename,/clobber)
;bootid = NCDF_DIMDEF(file_out,'bootstrap',nboots)
latid    = NCDF_DIMDEF(file_out,'latitude',nlats)
lonid    = NCDF_DIMDEF(file_out,'longitude',nlons)
  
latsvar  = NCDF_VARDEF(file_out,'latitude',[latid],/FLOAT)
lonsvar  = NCDF_VARDEF(file_out,'longitude',[lonid],/FLOAT)
;bootsvar = NCDF_VARDEF(file_out,'boots',[bootid],/SHORT)

CASE param OF
  'dpd': BEGIN
    qvar  = NCDF_VARDEF(file_out,'DPD_MPtrend',[lonid,latid],/FLOAT)
    qvarU = NCDF_VARDEF(file_out,'DPD_MP95th',[lonid,latid],/FLOAT)
    qvarL = NCDF_VARDEF(file_out,'DPD_MP5th',[lonid,latid],/FLOAT)
  END
  'td': BEGIN
    qvar  = NCDF_VARDEF(file_out,'Td_MPtrend',[lonid,latid],/FLOAT)
    qvarU = NCDF_VARDEF(file_out,'Td_MP95th',[lonid,latid],/FLOAT)
    qvarL = NCDF_VARDEF(file_out,'Td_MP5th',[lonid,latid],/FLOAT)
  END
  't': BEGIN
    qvar  = NCDF_VARDEF(file_out,'T_MPtrend',[lonid,latid],/FLOAT)
    qvarU = NCDF_VARDEF(file_out,'T_MP95th',[lonid,latid],/FLOAT)
    qvarL = NCDF_VARDEF(file_out,'T_MP5th',[lonid,latid],/FLOAT)
  END
  'tw': BEGIN
    qvar  = NCDF_VARDEF(file_out,'Tw_MPtrend',[lonid,latid],/FLOAT)
    qvarU = NCDF_VARDEF(file_out,'Tw_MP95th',[lonid,latid],/FLOAT)
    qvarL = NCDF_VARDEF(file_out,'Tw_MP5th',[lonid,latid],/FLOAT)  
  END
  'q': BEGIN
    qvar  = NCDF_VARDEF(file_out,'q_MPtrend',[lonid,latid],/FLOAT)
    qvarU = NCDF_VARDEF(file_out,'q_MP95th',[lonid,latid],/FLOAT)
    qvarL = NCDF_VARDEF(file_out,'q_MP5th',[lonid,latid],/FLOAT)  
  END
  'rh': BEGIN
    qvar  = NCDF_VARDEF(file_out,'RH_MPtrend',[lonid,latid],/FLOAT)
    qvarU = NCDF_VARDEF(file_out,'RH_MP95th',[lonid,latid],/FLOAT)
    qvarL = NCDF_VARDEF(file_out,'RH_MP5th',[lonid,latid],/FLOAT)  
  END
  'e': BEGIN
    qvar  = NCDF_VARDEF(file_out,'e_MPtrend',[lonid,latid],/FLOAT)
    qvarU = NCDF_VARDEF(file_out,'e_MP95th',[lonid,latid],/FLOAT)
    qvarL = NCDF_VARDEF(file_out,'e_MP5th',[lonid,latid],/FLOAT)  
  END
ENDCASE

;qbootsvar  = NCDF_VARDEF(file_out,'rh_MPboottrend',[lonid,latid,bootid],/FLOAT)
;qbootsvarU = NCDF_VARDEF(file_out,'rh_MPboot95th',[lonid,latid,bootid],/FLOAT)
;qbootsvarL = NCDF_VARDEF(file_out,'rh_MPboot5th',[lonid,latid,bootid],/FLOAT)

;NCDF_ATTPUT,file_out,bootsvar,'long_name','Bootstrap Member'
;NCDF_ATTPUT,file_out,bootsvar,'units','1 to 100'
NCDF_ATTPUT,file_out,latsvar,'long_name','Latitude'
NCDF_ATTPUT,file_out,latsvar,'units','Degrees'
NCDF_ATTPUT,file_out,latsvar,'valid_min',-90.
NCDF_ATTPUT,file_out,latsvar,'valid_max',90.
NCDF_ATTPUT,file_out,lonsvar,'long_name','Longitude'
NCDF_ATTPUT,file_out,lonsvar,'units','Degrees'
NCDF_ATTPUT,file_out,lonsvar,'valid_min',-180.
NCDF_ATTPUT,file_out,lonsvar,'valid_max',180.

NCDF_ATTPUT,file_out,qvar,'units',unitees
NCDF_ATTPUT,file_out,qvar,'long_name','Decadal MP trends'
NCDF_ATTPUT,file_out,qvar,'missing_value',mdi

NCDF_ATTPUT,file_out,qvarU,'units',unitees
NCDF_ATTPUT,file_out,qvarU,'long_name','Decadal MP 95th pct trends'
NCDF_ATTPUT,file_out,qvarU,'missing_value',mdi

NCDF_ATTPUT,file_out,qvarL,'units',unitees
NCDF_ATTPUT,file_out,qvarL,'long_name','Decadal MP 5th pct trends'
NCDF_ATTPUT,file_out,qvarL,'missing_value',mdi

;NCDF_ATTPUT,file_out,qbootsvar,'units',unitees
;NCDF_ATTPUT,file_out,qbootsvar,'long_name','Bootstrap Decadal MP trends'
;NCDF_ATTPUT,file_out,qbootsvar,'missing_value',mdi
;
;NCDF_ATTPUT,file_out,qbootsvarU,'units',unitees
;NCDF_ATTPUT,file_out,qbootsvarU,'long_name','Bootstrap Decadal MP 95th pct trends'
;NCDF_ATTPUT,file_out,qbootsvarU,'missing_value',mdi
;
;NCDF_ATTPUT,file_out,qbootsvarL,'units',unitees
;NCDF_ATTPUT,file_out,qbootsvarL,'long_name','Bootstrap Decadal MP 5th pct trends'
;NCDF_ATTPUT,file_out,qbootsvarL,'missing_value',mdi

NCDF_CONTROL,file_out,/ENDEF
NCDF_VARPUT,file_out,qvar,trendvals
NCDF_VARPUT,file_out,qvarU,trendvalsU
NCDF_VARPUT,file_out,qvarL,trendvalsL
;NCDF_VARPUT,file_out,qbootsvar,boottrendvals
;NCDF_VARPUT,file_out,qbootsvarU,boottrendvalsU
;NCDF_VARPUT,file_out,qbootsvarL,boottrendvalsL
;NCDF_VARPUT,file_out,bootsvar,int_boots
NCDF_CLOSE,file_out

return

end

