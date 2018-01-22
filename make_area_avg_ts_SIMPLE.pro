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


pro make_area_avg_ts

; to calculate area average - NO missing data tolerance - need a land/sea mask for that

;based on kate_timeseries.pro - WAVE for ICOADS

; written by Kate Willett
; last modified JUL 2012

;---------------------------------------------------
; set up directories and filenames
mdi=-1e+30

param='dpd'	;'dpd','td','t','tw','e','q','rh','w'
param2='DPD'	;'DPD','Td','T','Tw','e','q','RH','w'
nowmon='JAN'
nowyear='2016'
homogtype='PHA'	;'PHA','ID','DPD', 'RAW', 'OTHER'
version='2.1.0.2015p'

mask='false'	; If true then mask to HadISDH equivalent

styr=1973	; 1850, 1973, 1950, 1880
edyr=2015	; 2013, 2011
nyrs=(edyr+1)-styr
nmons=nyrs*12
int_mons=indgen(nmons)
latlg=5.	;5., 4.
lonlg=5. 	;5., 4.
stlt=-90+(latlg/2.)
stln=-180+(lonlg/2.)
nlats=180/latlg
nlons=360/lonlg
nbox=LONG(nlats*nlons)

lats=(findgen(nlats)*latlg)+stlt
lons=(findgen(nlons)*lonlg)+stln

IF (homogtype EQ 'OTHER') THEN dir='/data/local/hadkw/HADCRUH2/UPDATE2015/OTHERDATA/' $ 
    ELSE dir='/data/local/hadkw/HADCRUH2/UPDATE2015/STATISTICS/'
    
odir='/data/local/hadkw/HADCRUH2/UPDATE2015/STATISTICS/TIMESERIES/'

CASE param OF
  'dpd': BEGIN
    IF (homogtype EQ 'PHA') THEN infile='HadISDH.landDPD.'+version+'_FLATgridPHA5by5_JAN2016'
    IF (homogtype EQ 'RAW') THEN infile='HadISDH.landDPD.'+version+'_FLATgridRAW5by5_JAN2016'
    maskfile='/data/local/hadkw/HADCRUH2/UPDATE2015/STATISTICS/GRIDS/HadISDH.landDPD.'+version+'_FLATgridPHA5by5_JAN2016'
  END
  'td': BEGIN
    IF (homogtype EQ 'PHA') THEN infile='HadISDH.landTd.'+version+'_FLATgridPHA5by5_MAY2014'
    IF (homogtype EQ 'DPD') THEN infile='HadISDH.landTd.'+version+'_FLATgridPHADPD5by5_JAN2016'
    IF (homogtype EQ 'RAW') THEN infile='HadISDH.landTd.'+version+'_FLATgridRAW5by5_JAN2016'
    maskfile='/data/local/hadkw/HADCRUH2/UPDATE2015/STATISTICS/GRIDS/HadISDH.landTd.'+version+'_FLATgridPHADPD5by5_JAN2016'
  END
  't': BEGIN
    IF (homogtype EQ 'ID') THEN infile='HadISDH.landT.'+version+'_FLATgridIDPHA5by5_JAN2016'
    IF (homogtype EQ 'RAW') THEN infile='HadISDH.landT.'+version+'_FLATgridRAW5by5_JAN2016'
;    IF (homogtype EQ 'OTHER') THEN infile='HadCRUT.4.3.0.0.median'
;    IF (homogtype EQ 'OTHER') THEN infile='HadSST.3.1.1.0.median'
    IF (homogtype EQ 'OTHER') THEN infile='CRUTEM.4.3.0.0.anomalies'
;    IF (homogtype EQ 'OTHER') THEN infile='GHCNM_18802014'
    maskfile='/data/local/hadkw/HADCRUH2/UPDATE2015/STATISTICS/GRIDS/HadISDH.landT.'+version+'_FLATgridIDPHA5by5_JAN2016'
  END
  'tw': BEGIN
    IF (homogtype EQ 'ID') THEN infile='HadISDH.landTw.'+version+'_FLATgridIDPHA5by5_JAN2016'
    IF (homogtype EQ 'RAW') THEN infile='HadISDH.landTw.'+version+'_FLATgridRAW5by5_JAN2016'
    maskfile='/data/local/hadkw/HADCRUH2/UPDATE2015/STATISTICS/GRIDS/HadISDH.landTw.'+version+'_FLATgridIDPHA5by5_JAN2016'
  END
  'q': BEGIN
    IF (homogtype EQ 'ID') THEN infile='HadISDH.landq.'+version+'_FLATgridIDPHA5by5_JAN2016'
    IF (homogtype EQ 'PHA') THEN infile='HadISDH.landq.'+version+'_FLATgridPHA5by5_MAY2014'
    IF (homogtype EQ 'RAW') THEN infile='HadISDH.landq.'+version+'_FLATgridRAW5by5_JAN2016'
    maskfile='/data/local/hadkw/HADCRUH2/UPDATE2015/STATISTICS/GRIDS/HadISDH.landq.'+version+'_FLATgridIDPHA5by5_JAN2016'
  END
  'e': BEGIN
    IF (homogtype EQ 'ID') THEN infile='HadISDH.lande.'+version+'_FLATgridIDPHA5by5_JAN2016'
    IF (homogtype EQ 'RAW') THEN infile='HadISDH.lande.'+version+'_FLATgridRAW5by5_JAN2016'
    maskfile='/data/local/hadkw/HADCRUH2/UPDATE2015/STATISTICS/GRIDS/HadISDH.lande.'+version+'_FLATgridIDPHA5by5_JAN2016'
  END
  'rh': BEGIN
    IF (homogtype EQ 'ID') THEN infile='HadISDH.landRH.'+version+'_FLATgridIDPHA5by5_JAN2016'
    IF (homogtype EQ 'PHA') THEN infile='HadISDH.landRH.'+version+'_FLATgridPHA5by5_MAY2014'
    IF (homogtype EQ 'RAW') THEN infile='HadISDH.landRH.'+version+'_FLATgridRAW5by5_JAN2016'
    maskfile='/data/local/hadkw/HADCRUH2/UPDATE2015/STATISTICS/GRIDS/HadISDH.landRH.'+version+'_FLATgridIDPHA5by5_JAN2016'
  END
  'w': BEGIN
    infile='waswind_v1_0_1.monthly'
    maskfile='/data/local/hadkw/HADCRUH2/UPDATE2015/STATISTICS/GRIDS/HadISDH.landw.'+version+'_FLATgridPHA5by5_JAN2016'
  END
  
ENDCASE

ofile=infile+'_areaTS_'+strcompress(styr,/remove_all)+strcompress(edyr,/remove_all)	

CASE param OF
  'rh': unitees='% rh'
  'e': unitees='hPa'
  'q': unitees='g/kg'
  'w':unitees='m/s'
  ELSE: unitees='deg C'
ENDCASE

;----------------------------------------------------
; read in files
IF (homogtype NE 'OTHER') THEN filee=NCDF_OPEN(dir+'GRIDS/'+infile+'_cf.nc') $
    ELSE filee=NCDF_OPEN('/data/local/hadkw/HADCRUH2/UPDATE2015/OTHERDATA/'+infile+'.nc')
longs_varid=NCDF_VARID(filee,'longitude')
lats_varid=NCDF_VARID(filee,'latitude')
tims_varid=NCDF_VARID(filee,'time')

CASE param OF
  'dpd': BEGIN
    qabsid=NCDF_VARID(filee,'dpd_abs')
    qvarid=NCDF_VARID(filee,'dpd_anoms')
  END
  'td': BEGIN
    qabsid=NCDF_VARID(filee,'td_abs')
    qvarid=NCDF_VARID(filee,'td_anoms')
  END
  't': BEGIN
    IF (homogtype EQ 'OTHER') THEN BEGIN
      qvarid=NCDF_VARID(filee,'temperature_anomaly')
;      qvarid=NCDF_VARID(filee,'sst')      
    ENDIF ELSE BEGIN
      qabsid=NCDF_VARID(filee,'t_abs')
      qvarid=NCDF_VARID(filee,'t_anoms')
    ENDELSE
  END
  'tw': BEGIN
    qabsid=NCDF_VARID(filee,'tw_abs')
    qvarid=NCDF_VARID(filee,'tw_anoms')
  END
  'q': BEGIN
    qabsid=NCDF_VARID(filee,'q_abs')
    qvarid=NCDF_VARID(filee,'q_anoms')
  END
  'rh': BEGIN
    qabsid=NCDF_VARID(filee,'rh_abs')
    qvarid=NCDF_VARID(filee,'rh_anoms')
  END
  'e': BEGIN
    qabsid=NCDF_VARID(filee,'e_abs')
    qvarid=NCDF_VARID(filee,'e_anoms')
  END
  'w': BEGIN
    qabsid=NCDF_VARID(filee,'sp')
  END
ENDCASE

;qstdid=NCDF_VARID(filee,'td_combinederr') 	; may become uncertainty fields
if (homogtype NE 'OTHER') AND (param NE 'w') THEN NCDF_VARGET,filee,qabsid,q_abs
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

If (mask EQ 'true') THEN BEGIN ; generally only in case of ERA-Interim so then need to anomalise to correct period
  filee=NCDF_OPEN(maskfile+'_cf.nc')

  CASE param OF
    'dpd': BEGIN
      qabsid=NCDF_VARID(filee,'dpd_abs')
      qvarid=NCDF_VARID(filee,'dpd_anoms')
    END
    'td': BEGIN
      qabsid=NCDF_VARID(filee,'td_abs')
      qvarid=NCDF_VARID(filee,'td_anoms')
    END
    't': BEGIN
      qabsid=NCDF_VARID(filee,'t_abs')
      qvarid=NCDF_VARID(filee,'t_anoms')
    END
    'tw': BEGIN
      qabsid=NCDF_VARID(filee,'tw_abs')
      qvarid=NCDF_VARID(filee,'tw_anoms')
    END
    'q': BEGIN
      qabsid=NCDF_VARID(filee,'q_abs')
      qvarid=NCDF_VARID(filee,'q_anoms')
    END
    'rh': BEGIN
      qabsid=NCDF_VARID(filee,'rh_abs')
      qvarid=NCDF_VARID(filee,'rh_anoms')
    END
    'e': BEGIN
      qabsid=NCDF_VARID(filee,'e_abs')
      qvarid=NCDF_VARID(filee,'e_anoms')
    END
    'w': BEGIN
      qabsid=NCDF_VARID(filee,'sp')
    END
  ENDCASE
  NCDF_VARGET,filee,qvarid,mask_values
  NCDF_CLOSE,filee
  
  ; mask to HadISDH over the joint period of record
  ostyr=styr
  oedyr=edyr
  onyrs=nyrs
  onmons=nmons
  oint_mons=int_mons
  styr=1973	; 1850, 1973, 1950, 1880
  edyr=2014	; 2013, 2011
  nyrs=(edyr+1)-styr
  nmons=nyrs*12
  int_mons=indgen(nmons)
  
  ofile=infile+'_areaTSMSK7605_'+strcompress(styr,/remove_all)+strcompress(edyr,/remove_all)
  
  stfrm=(styr-ostyr)*12
  oldq_values=q_values
  q_values=q_values(*,*,stfrm:onmons-1)	;shorten to same time period as HadISDH
  bads=WHERE(mask_values LT -999,count)
  IF (count GT 0) THEN q_values(bads)=mdi

  ; make anomalies from the monthlies
  newq_values=make_array(nlons,nlats,nmons,/float,value=mdi)
  FOR ltt=0,nlats-1 DO BEGIN
    FOR lnn=0,nlons-1 DO BEGIN
      subarr=REFORM(q_values(lnn,ltt,*),12,nyrs)
      FOR mm=0,11 DO BEGIN
        gots=WHERE(subarr(mm,*) NE mdi,count)
;	climsub=subarr(mm,1981-styr:2010-styr)
	climsub=subarr(mm,1976-styr:2005-styr)
	gotsC=WHERE(climsub NE mdi,countC)
	IF (countC GE 15) THEN subarr(mm,gots)=subarr(mm,gots)-MEAN(climsub(gotsC)) ELSE subarr(mm,*)=mdi
      ENDFOR
      newq_values(lnn,ltt,*)=REFORM(subarr,nmons)
    ENDFOR
  ENDFOR
  ;stop
  q_values=newq_values
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
IF (homogtype NE 'OTHER') THEN openw,2,dir+'TIMESERIES/'+ofile+'_monthly.dat' $
    ELSE openw,2,dir+ofile+'_monthly.dat'
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

IF (homogtype NE 'OTHER') THEN openw,2,dir+'TIMESERIES/'+ofile+'_annual.dat' $
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

