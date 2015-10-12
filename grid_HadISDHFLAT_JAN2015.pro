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



pro grid_HadISDHFLAT_JAN2015

; *** WILL NEED UPDATING WITH UNCERTAINTY ***

!EXCEPT=2
; this tells you where the underflow/overflow errors are

; program to make gridbox means using stations within the gridbox
; inside stations are weighted from 0.5 to 1
; no temporal smoothing
; standard deviations provided for each gridbox for each month from all contributing stations.
; IF only one station contributing - give arbitrary standard deviation of 100?

; cool surface plot:
; GBelvs(WHERE(GBelvs) EQ mdi)=0.
; cols=ROUND((GBelvs/MAX(GBelvs))*254
; device,decomposed=0
; restore_colors,'shortbow'
; surface,GBelvs,min_value=-100,shades=cols,/lego
; OR
; shade_surf,GBelvs,min_value=-100,shades=cols

;*********************************************
; NOTES OF UPDATES
; JAN 2015
; Added an output to ascii for the gridded anomalies, absolutes and combined
; uncertainty

; Made sure its CF1.0 compliant as for Convert_cfnc_AUG2014.py
; Global attributes
; Time as days since 1973-1-1 (not months)	
;*********************************************

;**** THIS IS WHERE TO ADD UNCERTAINTY ALA BROHAN et al. 2006
; Station error:
;   Tob - Tclim + errorCLIM + measurementerror + homogadj + adjuncertainty + reporting error
; Samping error:
; SE^2 = GBstdev*avg.intersite correlation*(1-avg.intersite corr)
;        --------------------------------------------------------
;          1 + ((num stations - 1) * avg.intersite correlation)
; Bias error:
; urbanisation? exposure change? irrigation?

; combine these by adding in quadrature.

; sampling error - after Jones et al. 1997

;Shat^2 = variance of gridbox(extended?) means over climatology period
;n = number of stations contributing to gridbox(extended?) over climatology period
;Xo = correlation decay distance (km) for that gridbox (where correlation = 1/e)
;X = diagonal from bottom left to top right of gridbox(extended?) (km) - use lats, longs and dist_calc
;rbar = (Xo/X)*(1-e(-X/Xo))
;sbar^2 = mean station variance within the gridbox
;sbar^2 = (Shat^2*n)/(1+((n-1)*rbar))
;INFILL empty gridboxes by interpolated Xo and then calculating rbar
;SE^2 = gridbox sampling error
;SE^2 = (sbar^2*rbar*(1-rbar))/(1+((n-1)*rbar))
;SE^2 (where n=0) = sbar^2*rbar (INFILL GB with Shat^2???)
;SEglob^2 = global average sampling error
;SEglob^2 = SEbar^2/Neff
;SEbar^2 = (SUM(SE^2*cos(lat)))/(SUM(cos(lat)))
;Neff = number of effectively independent points
;Neff = (2*R)/F
;R = radius of the earth (6371 km)
;F=(((e((-piR)/Xobar))/R)+(1/R))/((1/(Xobar^2))+(1/R^2))
;Xobar=(SUM(Xo*cos(lat)))/(SUM(cos(lat)))


; .compile calc_samplingerrorJUL2012_nofill

;-----------------------------------------------------
; editables
param='t'	;'dpd','td','t','tw','e','q','rh'
param2='T'	;'DPD','Td','T','Tw','e','q','RH'
nowmon='JAN'
nowyear='2015'
homogtype='RAW'	;'PHA','ID','DPD', 'RAW'
version='2.0.1.2014p'

;; files and directories
CASE param OF
  'dpd': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAdpd_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAdpd_satsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/PHANETCDF/DPDDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landDPD.'+version+'_FLATgridPHA'  
    ENDIF ELSE IF (homogtype EQ 'RAW') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAdpd_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAdpd_satsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/NETCDF/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landDPD.'+version+'_FLATgridRAW'  
    ENDIF
  END
  'td': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAtd_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAtd_satsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/PHANETCDF/TDDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landTd.'+version+'_FLATgridPHA'  
    ENDIF ELSE IF (homogtype EQ 'RAW') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHADPDtd_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHADPDtd_satsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/NETCDF/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landTd.'+version+'_FLATgridRAW'  
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHADPDtd_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHADPDtd_satsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHANETCDF/TDDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landTd.'+version+'_FLATgridPHADPD'  
    ENDELSE
  END
  'tw': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAtw_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAtw_satsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/PHANETCDF/TWDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landTw.'+version+'_FLATgridPHA'  
    ENDIF ELSE IF (homogtype EQ 'RAW') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAtw_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAtw_satsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/NETCDF/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landTw.'+version+'_FLATgridRAW'  
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAtw_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAtw_satsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHANETCDF/TWDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landTw.'+version+'_FLATgridIDPHA'      
    ENDELSE
  END
  't': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAt_goodsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/PHANETCDF/TDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landT.'+version+'_FLATgridPHA'  
    ENDIF ELSE IF (homogtype EQ 'RAW') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAt_goodsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/NETCDF/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landT.'+version+'_FLATgridRAW'  
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAt_goodsHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHANETCDF/TDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landT.'+version+'_FLATgridIDPHA'  
    ENDELSE
  END
  'rh': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHArh_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHArh_satsHadISDH.'+version+'_JAN2015.txt'
      inlistZ='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHArh_subzerosHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/PHANETCDF/RHDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landRH.'+version+'_FLATgridPHA'  
    ENDIF ELSE IF (homogtype EQ 'RAW') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHArh_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHArh_satsHadISDH.'+version+'_JAN2015.txt'
      inlistZ='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHArh_subzerosHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/NETCDF/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landRH.'+version+'_FLATgridRAW'  
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHArh_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHArh_satsHadISDH.'+version+'_JAN2015.txt'
      inlistZ='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHArh_subzerosHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHANETCDF/RHDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landRH.'+version+'_FLATgridIDPHA'  
    ENDELSE
  END
  'e': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAe_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAe_satsHadISDH.'+version+'_JAN2015.txt'
      inlistZ='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAe_subzerosHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/PHANETCDF/EDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.lande.'+version+'_FLATgridPHA'  
    ENDIF ELSE IF (homogtype EQ 'RAW') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAe_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAe_satsHadISDH.'+version+'_JAN2015.txt'
      inlistZ='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAe_subzerosHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/NETCDF/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.lande.'+version+'_FLATgridRAW'  
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAe_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAe_satsHadISDH.'+version+'_JAN2015.txt'
      inlistZ='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAe_subzerosHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHANETCDF/EDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.lande.'+version+'_FLATgridIDPHA'  
    ENDELSE
  END
  'q': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAq_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAq_satsHadISDH.'+version+'_JAN2015.txt'
      inlistZ='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogPHAq_subzerosHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/PHANETCDF/QDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landq.'+version+'_FLATgridPHA'  
    ENDIF ELSE IF (homogtype EQ 'RAW') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAq_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAq_satsHadISDH.'+version+'_JAN2015.txt'
      inlistZ='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAq_subzerosHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/NETCDF/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landq.'+version+'_FLATgridRAW'  
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAq_goodsHadISDH.'+version+'_JAN2015.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAq_satsHadISDH.'+version+'_JAN2015.txt'
      inlistZ='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/PosthomogIDPHAq_subzerosHadISDH.'+version+'_JAN2015.txt'
      indat='/data/local/hadkw/HADCRUH2/UPDATE2014/MONTHLIES/HOMOG/IDPHANETCDF/QDIR/'
      outdat='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/HadISDH.landq.'+version+'_FLATgridIDPHA'  
    ENDELSE
  END
ENDCASE

outresults='/data/local/hadkw/HADCRUH2/UPDATE2014/LISTS_DOCS/GriddingResults_'+version+'_'+nowmon+nowyear+'.txt'
;--------------------------------------------------------
; variables and arrays
mdi=-1e+30

;number of stations still having 15+ months after homog.
CASE param OF
  'dpd': nstations=3296	; 2015
  'td': IF (homogtype EQ 'PHA') THEN nstations=9999 ELSE nstations=3162	; 2015	
  't': nstations=3561 	; 2015
  'tw': nstations=2782		; 2015
  'e': nstations=3572		; 2015
  'q': IF (homogtype EQ 'PHA') THEN nstations=9999 ELSE nstations=3572	; 2015
  'rh': IF (homogtype EQ 'PHA') THEN nstations=9999 ELSE nstations=3611 ; 2015
ENDCASE

; subzeros
CASE param OF
  'dpd': nsubs=0	; 2015
  'td': nsubs=0		; 2015
  't': nsubs=0 		; 2015
  'tw': nsubs=0		; 2015		
  'e': nsubs=41		; 2015
  'q': IF (homogtype EQ 'PHA') THEN nsubs=99 ELSE nsubs=39	; 2015
  'rh': IF (homogtype EQ 'PHA') THEN nsubs=0 ELSE nsubs=0 	; 2015
ENDCASE

; supersats
CASE param OF
  'dpd': nsats=164 	; 2015
  'td': IF (homogtype EQ 'PHA') THEN nsats=999 ELSE nsats=160	; 2015	
  't': nsats=0 		; 2015
  'tw': nsats=860	; 2015		
  'e': nsats=29		; 2015
  'q': IF (homogtype EQ 'PHA') THEN nsats=99 ELSE nsats=29	; 2015
  'rh': IF (homogtype EQ 'PHA') THEN nsats=99 ELSE nsats=29 ; 2015
ENDCASE

;units
CASE param OF
  'q': unitees='g/kg'
  'rh': unitees='%rh'
  'e': unitees='hPa'
  ELSE: unitees='deg C'
ENDCASE

monarr=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
styr=1973
edyr=2014
nyrs=(edyr+1)-styr
clst=1976-styr
cled=2005-styr
nmons=nyrs*12
int_mons=indgen(nmons)
dayssince=findgen(nmons)
stpoint=JULDAY(1,1,1973)
; array of months in days since Jan 1st 1973 including Jan 2015 (nmons+1)
monthies=TIMEGEN(nmons+1,START=(stpoint),UNITS="Months")-stpoint ; an array of floats describing each month in days since Jan 1st 1973
monthies=ROUND(monthies*100.)/100.	; nicer numbers
; Now need to use the mid-point of each month.
FOR mm=0,nmons-1 DO BEGIN
  dayssince(mm)=monthies(mm)+(monthies(mm+1)-monthies(mm))/2.
ENDFOR
latlg=5.
lonlg=5.
stlt=-90+(latlg/2.)
stln=-180+(lonlg/2.)
nlats=180/latlg
nlons=360/lonlg
nbox=LONG(nlats*nlons)
inrad=(latlg/2.)*100	;250km for 5 by 5 gridbox
grid=strcompress(ROUND(latlg),/remove_all)+'by'+strcompress(ROUND(lonlg),/remove_all)

lats=(findgen(nlats)*latlg)+stlt
lons=(findgen(nlons)*lonlg)+stln

inGBstats={GBstats,wmo:strarr(100),lats:fltarr(100),lons:fltarr(100),elvs:fltarr(100),$
             dists:fltarr(100),weights:fltarr(100),nums:0}

; number of stations to ignore because they go below zero (q) or above 100 (RH)
IF (nsubs GT 0) THEN info_arrZ={infoz,statid:strarr(nsubs)}
; number of stations to ignore because they go below zero (q) or above 100 (RH)
IF (nsats GT 0) THEN info_arrT={infot,statid:strarr(nsats)}

GBelvs=make_array(nlons,nlats,/float,value=mdi)
stat_id={stationinfo,wmoids:strarr(nstations),lats:fltarr(nstations),lons:fltarr(nstations),elevs:fltarr(nstations)}
stat_abs=make_array(nstations,nmons,/float,value=mdi)
stat_anoms=make_array(nstations,nmons,/float,value=mdi)
stat_err=make_array(nstations,nmons,/float,value=mdi)
stat_adjE=make_array(nstations,nmons,/float,value=mdi)
stat_obsE=make_array(nstations,nmons,/float,value=mdi)
stat_clmE=make_array(nstations,nmons,/float,value=mdi)
stat_clims=make_array(nstations,12,/float,value=mdi)
stat_sds=make_array(nstations,12,/float,value=mdi)

q_anoms=make_array(nlons,nlats,nmons,/float,value=mdi)
q_abs=make_array(nlons,nlats,nmons,/float,value=mdi)
q_staterr=make_array(nlons,nlats,nmons,/float,value=mdi)
q_obserr=make_array(nlons,nlats,nmons,/float,value=mdi)
q_clmerr=make_array(nlons,nlats,nmons,/float,value=mdi)
q_adjerr=make_array(nlons,nlats,nmons,/float,value=mdi)
q_samperr=make_array(nlons,nlats,nmons,/float,value=mdi)
q_rbar=make_array(nlons,nlats,/float,value=mdi)
q_sbarSQ=make_array(nlons,nlats,/float,value=mdi)
q_comberr=make_array(nlons,nlats,nmons,/float,value=mdi)
q_stddevs=make_array(nlons,nlats,nmons,/float,value=mdi)
q_clims=make_array(nlons,nlats,12,/float,value=mdi)
GB_counts=make_array(nlons,nlats,/float,value=mdi)	;0=in GB only
station_counts=make_array(nlons,nlats,nmons,/integer,value=0) ; actual gridbox station counts over time
;---------------------------------------------------------
; open station file
; move from gridbox to gridbox starting with -177.5W, 87.5S
; if there is a station then begin
; find all stations in GB - store lat, lon, elev
; find all stations in surrrounding 8 GBs, store lat, lon, elev
; get in-GB distances from GB centre using elevation (calc GB mean elevation) - weight 0.5-1
; get out-GB distances from GB centre using elevation - weight 0.01-0.5
; calc GB mean and standard deviation for each month 

IF (nsubs GT 0) THEN BEGIN
  openr,42,inlistZ
  counter=0
  WHILE NOT EOF(42) DO BEGIN
    id=''
    mush=''
    readf,42,id,mush,format='(a11,a24)'
    info_arrZ.statid(counter)=id
    counter=counter+1
    print,counter
  ENDWHILE
  close,42
ENDIF
IF (nsats GT 0) THEN BEGIN
  openr,42,inlistT
  counter=0
  WHILE NOT EOF(42) DO BEGIN
    id=''
    mush=''
    readf,42,id,mush,format='(a11,a24)'
    info_arrT.statid(counter)=id
    counter=counter+1
    print,counter
  ENDWHILE
  close,42
ENDIF


; read in all station info
openr,5,inlist
counter=0
countbad=0
WHILE NOT EOF(5) DO BEGIN
  wmo=''
  lat=0.
  lon=0.
  elv=0.
  cid=''
  namoo=''
  readf,5,wmo,lat,lon,elv,cid,namoo,format='(a11,f9.4,f10.4,f7.1,x,a2,x,a29,x)'  
  print,counter,' ',wmo
; remove subzeros  and sats stations 
  IF (nsubs GT 0) THEN BEGIN
    findee=WHERE(info_arrZ.statid EQ wmo,count)
    IF (count GT 0) THEN BEGIN
;      stop,'GOT A SUBZERO'
      goto,endloop
    ENDIF
  ENDIF
  IF (nsats GT 0) THEN BEGIN
    findee=WHERE(info_arrT.statid EQ wmo,count)
    IF (count GT 0) THEN print,info_arrT.statid(findee(0))
    IF (count GT 0) THEN goto,endloop
  ENDIF  

  stat_id.wmoids(counter)=wmo 
  stat_id.lats(counter)=lat 
  stat_id.lons(counter)=lon 
  stat_id.elevs(counter)=elv 

 ; find file and read in to array 
  filee=FILE_SEARCH(indat+strmid(wmo,0,5)+'*',count=count)
  print,filee
  IF (count GT 0) THEN BEGIN
    inn=NCDF_OPEN(filee(0))
    IF (homogtype EQ'RAW') THEN BEGIN
      CASE param OF
        'dpd': BEGIN
          anmid=NCDF_VARID(inn,'ddep_anoms')	; not perfect as actually used de_ddep_abs but anoms not saved
          absid=NCDF_VARID(inn,'ddep_abs')
          clmid=NCDF_VARID(inn,'ddep_clims')
        END
        'td': BEGIN
          anmid=NCDF_VARID(inn,'dewp_anoms')
          absid=NCDF_VARID(inn,'dewp_abs')
          clmid=NCDF_VARID(inn,'dewp_clims')
        END
        't': BEGIN
          anmid=NCDF_VARID(inn,'temp_anoms')
          absid=NCDF_VARID(inn,'temp_abs')
          clmid=NCDF_VARID(inn,'temp_clims')
        END
        'tw': BEGIN
          anmid=NCDF_VARID(inn,'twet_anoms')
          absid=NCDF_VARID(inn,'twet_abs')
          clmid=NCDF_VARID(inn,'twet_clims')
         END
        'q': BEGIN
          anmid=NCDF_VARID(inn,'qhum_anoms')
          absid=NCDF_VARID(inn,'qhum_abs')
          clmid=NCDF_VARID(inn,'qhum_clims')
         END
        'e': BEGIN
          anmid=NCDF_VARID(inn,'evap_anoms')
          absid=NCDF_VARID(inn,'evap_abs')
          clmid=NCDF_VARID(inn,'evap_clims')
        END
        'rh': BEGIN
          anmid=NCDF_VARID(inn,'rhum_anoms')
          absid=NCDF_VARID(inn,'rhum_abs')
          clmid=NCDF_VARID(inn,'rhum_clims')
        END
      ENDCASE
    ENDIF ELSE BEGIN
      CASE param OF
        'dpd': BEGIN
          anmid=NCDF_VARID(inn,'dpd_anoms')
          absid=NCDF_VARID(inn,'dpd_abs')
          clmid=NCDF_VARID(inn,'dpd_clims')
          stdid=NCDF_VARID(inn,'dpd_stds')
          uncid=NCDF_VARID(inn,'dpd_uncertainty')
          obEid=NCDF_VARID(inn,'dpd_obserr')
          cmEid=NCDF_VARID(inn,'dpd_clmerr')
          ajEid=NCDF_VARID(inn,'dpd_adjerr')
        END
        'td': BEGIN
          anmid=NCDF_VARID(inn,'td_anoms')
          absid=NCDF_VARID(inn,'td_abs')
          clmid=NCDF_VARID(inn,'td_clims')
          stdid=NCDF_VARID(inn,'td_stds')
          uncid=NCDF_VARID(inn,'td_uncertainty')
          obEid=NCDF_VARID(inn,'td_obserr')
          cmEid=NCDF_VARID(inn,'td_clmerr')
          ajEid=NCDF_VARID(inn,'td_adjerr')
        END
        't': BEGIN
          anmid=NCDF_VARID(inn,'t_anoms')
          absid=NCDF_VARID(inn,'t_abs')
          clmid=NCDF_VARID(inn,'t_clims')
          stdid=NCDF_VARID(inn,'t_stds')
          uncid=NCDF_VARID(inn,'t_uncertainty')
          obEid=NCDF_VARID(inn,'t_obserr')
          cmEid=NCDF_VARID(inn,'t_clmerr')
          ajEid=NCDF_VARID(inn,'t_adjerr')
        END
        'tw': BEGIN
          anmid=NCDF_VARID(inn,'tw_anoms')
          absid=NCDF_VARID(inn,'tw_abs')
          clmid=NCDF_VARID(inn,'tw_clims')
          stdid=NCDF_VARID(inn,'tw_stds')
          uncid=NCDF_VARID(inn,'tw_uncertainty')
          obEid=NCDF_VARID(inn,'tw_obserr')
          cmEid=NCDF_VARID(inn,'tw_clmerr')
          ajEid=NCDF_VARID(inn,'tw_adjerr')
        END
        'q': BEGIN
          anmid=NCDF_VARID(inn,'q_anoms')
          absid=NCDF_VARID(inn,'q_abs')
          clmid=NCDF_VARID(inn,'q_clims')
          stdid=NCDF_VARID(inn,'q_stds')
          uncid=NCDF_VARID(inn,'q_uncertainty')
          obEid=NCDF_VARID(inn,'q_obserr')
          cmEid=NCDF_VARID(inn,'q_clmerr')
          ajEid=NCDF_VARID(inn,'q_adjerr')
        END
        'e': BEGIN
          anmid=NCDF_VARID(inn,'e_anoms')
          absid=NCDF_VARID(inn,'e_abs')
          clmid=NCDF_VARID(inn,'e_clims')
          stdid=NCDF_VARID(inn,'e_stds')
          uncid=NCDF_VARID(inn,'e_uncertainty')
          obEid=NCDF_VARID(inn,'e_obserr')
          cmEid=NCDF_VARID(inn,'e_clmerr')
          ajEid=NCDF_VARID(inn,'e_adjerr')
        END
        'rh': BEGIN
          anmid=NCDF_VARID(inn,'rh_anoms')
          absid=NCDF_VARID(inn,'rh_abs')
          clmid=NCDF_VARID(inn,'rh_clims')
          stdid=NCDF_VARID(inn,'rh_stds')
          uncid=NCDF_VARID(inn,'rh_uncertainty')
          obEid=NCDF_VARID(inn,'rh_obserr')
          cmEid=NCDF_VARID(inn,'rh_clmerr')
          ajEid=NCDF_VARID(inn,'rh_adjerr')
        END
      ENDCASE
    ENDELSE
    
    NCDF_VARGET,inn,anmid,anoms
    NCDF_VARGET,inn,absid,absols
    NCDF_VARGET,inn,clmid,clims
    IF (homogtype NE 'RAW') THEN BEGIN
      NCDF_VARGET,inn,stdid,stds
      NCDF_VARGET,inn,uncid,uncs
      NCDF_VARGET,inn,obEid,obsE
      NCDF_VARGET,inn,cmEid,clmE
      NCDF_VARGET,inn,ajEid,adjE
    ENDIF
    NCDF_CLOSE,inn
    
    stat_abs(counter,*)=absols
    stat_clims(counter,*)=clims
    stat_anoms(counter,*)=anoms
    IF (homogtype NE 'RAW') THEN BEGIN
      stat_sds(counter,*)=stds
      stat_err(counter,*)=uncs
      stat_adjE(counter,*)=adjE
      stat_clmE(counter,*)=clmE
      stat_obsE(counter,*)=obsE
    ENDIF
  ENDIF ELSE stop,'CANT FIND FILE'
  counter=counter+1
  
  IF (homogtype NE 'RAW') THEN BEGIN
    mahoos=WHERE(stat_obsE GT 1000,countM)
    IF (countM GT 0) THEN stop,'MAHOOSIVE OBS ERROR'
  ENDIF
  endloop:
ENDWHILE
close,5

; loop through gridboxes
counter=0L
actcount=0L
FOR ltt=0,nlats-1 DO BEGIN
  FOR lnn=0,nlons-1 DO BEGIN    
    inGBstats={GBstats,wmo:strarr(100),lats:fltarr(100),lons:fltarr(100),elvs:fltarr(100),$
             dists:fltarr(100),weights:fltarr(100),nums:0}

    gbpos=[lons(lnn)-(lonlg/2.),lats(ltt)-(latlg/2.),lons(lnn)+(lonlg/2.),lats(ltt)+(latlg/2.)]
    ; find inGB stations
    gots=WHERE(stat_id.lons GE gbpos(0) AND stat_id.lons LT gbpos(2) AND $
               stat_id.lats GE gbpos(1) AND stat_id.lats LT gbpos(3),count)
    inGBstats.nums=count
    IF (count GT 0) THEN BEGIN
      print,'GB: ',count,counter,actcount,gbpos
     ; IF THERE IS A STATION IN THE GRIDBOX THEN CARRY ON
      inGBstats.wmo(0:count-1)=REFORM(stat_id.wmoids(gots),count)
      inGBstats.lats(0:count-1)=REFORM(stat_id.lats(gots),count)
      inGBstats.lons(0:count-1)=REFORM(stat_id.lons(gots),count)
      inGBstats.elvs(0:count-1)=REFORM(stat_id.elevs(gots),count)
    ENDIF ELSE BEGIN
;      print,'NO STATIONS!'
      counter=counter+1
      continue
    ENDELSE
   ; create weighted gridbox average for means, anoms, clims and get stdev for each month (non-weighted)
    sterrsum=make_array(nmons,/float,value=0.)
    stcmEsum=make_array(nmons,/float,value=0.)
    stobEsum=make_array(nmons,/float,value=0.)
    stajEsum=make_array(nmons,/float,value=0.)
    abssum=make_array(nmons,/float,value=0.)
    absweight=make_array(nmons,/float,value=0.)
    anmsum=make_array(nmons,/float,value=0.)
    anmweight=make_array(nmons,/float,value=0.)
    clmsum=make_array(12,/float,value=0.)
    clmweight=make_array(12,/float,value=0.)
    stdvals=make_array(300,nmons,/float,value=mdi)
    stcount=0
    incount=0
    outcount=0
    FOR st=0,inGBstats.nums-1 DO BEGIN
      findit=WHERE(stat_id.wmoids EQ inGBstats.wmo(st),count)
      IF (count EQ 0) THEN stop,'CANNOT FIND STATION!'
      gots=WHERE(stat_abs(findit(0),*) NE mdi,count)
      IF (homogtype EQ 'RAW') THEN gotsANMS=WHERE(stat_anoms(findit(0),*) NE mdi,count)
      mons=WHERE(stat_clims(findit(0),*) NE mdi,count)
      IF (count GT 0) THEN BEGIN
; switch off if raw - here we're getting the Root mean square of the errors.
        sterrsum(gots)=sterrsum(gots)+(stat_err(findit(0),gots)^2)
        stcmEsum(gots)=stcmEsum(gots)+(stat_clmE(findit(0),gots)^2)
        stobEsum(gots)=stobEsum(gots)+(stat_obsE(findit(0),gots)^2)
        stajEsum(gots)=stajEsum(gots)+(stat_adjE(findit(0),gots)^2)
        abssum(gots)=abssum(gots)+stat_abs(findit(0),gots)
	absweight(gots)=absweight(gots)+1
        IF (homogtype NE 'RAW') THEN BEGIN
	  anmsum(gots)=anmsum(gots)+stat_anoms(findit(0),gots)
	  anmweight(gots)=anmweight(gots)+1
        ENDIF ELSE BEGIN
	  anmsum(gotsANMS)=anmsum(gotsANMS)+stat_anoms(findit(0),gotsANMS)
	  anmweight(gotsANMS)=anmweight(gotsANMS)+1	
	ENDELSE
	clmsum(mons)=clmsum(mons)+stat_clims(findit(0),mons)
	clmweight(mons)=clmweight(mons)+1
	stdvals(stcount,gots)=stat_abs(findit(0),gots)
	stcount=stcount+1
	incount=incount+1
	station_counts(lnn,ltt,gots)=station_counts(lnn,ltt,gots)+1 ;stations within GB only
      ENDIF      
    ENDFOR
    IF (homogtype NE 'RAW') THEN BEGIN
      mahoos=WHERE(stobEsum GT 1000,countM)
      IF (countM GT 0) THEN stop,'FOUND MAHOOSIVE OBS ERROR SUM'
    ENDIF
    vals=WHERE(absweight NE 0.,count)
    IF (count GT 0) THEN BEGIN
      GB_counts(lnn,ltt,0)=stcount
; switch off if raw - here we're getting the Root mean square of the errors.* 1/SQRT(nstations) after Brohan et al. 2006
      q_staterr(lnn,ltt,vals)=SQRT(sterrsum(vals)/stcount)*(1./SQRT(stcount))
      q_obserr(lnn,ltt,vals)=SQRT(stobEsum(vals)/stcount)*(1./SQRT(stcount))
      q_clmerr(lnn,ltt,vals)=SQRT(stcmEsum(vals)/stcount)*(1./SQRT(stcount))
      q_adjerr(lnn,ltt,vals)=SQRT(stajEsum(vals)/stcount)*(1./SQRT(stcount))
      q_abs(lnn,ltt,vals)=abssum(vals)/absweight(vals)
      IF (homogtype NE 'RAW') THEN BEGIN
        q_anoms(lnn,ltt,vals)=anmsum(vals)/anmweight(vals)
      ENDIF ELSE BEGIN
        valsANMS=WHERE(anmweight NE 0.,count)
        q_anoms(lnn,ltt,valsANMS)=anmsum(valsANMS)/anmweight(valsANMS)
      ENDELSE
      mons=WHERE(clmweight NE 0.,count)
      IF (count GT 0) THEN q_clims(lnn,ltt,mons)=clmsum(mons)/clmweight(mons)
      FOR mm=0,nmons-1 DO BEGIN
        gots=WHERE(stdvals(*,mm) NE mdi,count)
	IF (count GT 1) THEN q_stddevs(lnn,ltt,mm)=STDDEV(stdvals(gots,mm))
	IF (count EQ 1) THEN q_stddevs(lnn,ltt,mm)=100.
      ENDFOR
    ENDIF
    actcount=actcount+1
    counter=counter+1
  ENDFOR
ENDFOR

; now we have all the grids:
; GO AND GET SAMPLING ERROR - this is quite longwinded so doing it in a subprogram
; needs all gridded data, number of stations in each box
; use anomalies - better to correlate these than absolutes

clpoints=[clst,cled]
samps_details=make_array(nlons,nlats,2,/float,value=mdi)
q_samperr=calc_samplingerrorJUL2012_nofill(q_anoms,lats,lons,GB_counts,station_counts,mdi,clpoints,samps_details)

q_rbar(*,*)=REFORM(samps_details(*,*,0))
q_sbarSQ(*,*)=REFORM(samps_details(*,*,1))

;stop

; switch off if raw - here we're combining the sampling and station errors
FOR tt=0,nmons-1 DO BEGIN
  combarr=make_array(nlons,nlats,/float,value=mdi)
  subarr1=q_staterr(*,*,tt)
  subarr2=q_samperr(*,*,tt)
  gots=WHERE(subarr1 NE mdi AND subarr2 NE mdi,count)
  combarr(gots)=(SQRT(((subarr1(gots)/2.)^2)+((subarr2(gots)/2.)^2)))*2.
  q_comberr(*,*,tt)=combarr
ENDFOR
;stop

;write to netCDF file
openw,19,outresults,/append
printf,19,' '
printf,19,'PARAMETER ',param,' ', homogtype
wilma=NCDF_CREATE(outdat+grid+'_'+nowmon+nowyear+'_cf.nc',/clobber)
  
tid=NCDF_DIMDEF(wilma,'time',nmons)
clmid=NCDF_DIMDEF(wilma,'month',12)
charid=NCDF_DIMDEF(wilma, 'Character', 3)
latid=NCDF_DIMDEF(wilma,'latitude',nlats)
lonid=NCDF_DIMDEF(wilma,'longitude',nlons)
  
timesvar=NCDF_VARDEF(wilma,'time',[tid],/SHORT)
latsvar=NCDF_VARDEF(wilma,'latitude',[latid],/FLOAT)
lonsvar=NCDF_VARDEF(wilma,'longitude',[lonid],/FLOAT)
meanstvar=NCDF_VARDEF(wilma,'mean_n_stations',[lonid,latid],/FLOAT)
nstvar=NCDF_VARDEF(wilma,'actual_n_stations',[lonid,latid,tid],/FLOAT)
CASE param OF
  'dpd': BEGIN
    rhanomvar=NCDF_VARDEF(wilma,'dpd_anoms',[lonid,latid,tid],/FLOAT)
    rhabsvar=NCDF_VARDEF(wilma,'dpd_abs',[lonid,latid,tid],/FLOAT)
    rhsdvar=NCDF_VARDEF(wilma,'dpd_std',[lonid,latid,tid],/FLOAT)
    rhsterr=NCDF_VARDEF(wilma,'dpd_stationerr',[lonid,latid,tid],/FLOAT)
    rhajerr=NCDF_VARDEF(wilma,'dpd_adjerr',[lonid,latid,tid],/FLOAT)
    rhcmerr=NCDF_VARDEF(wilma,'dpd_climerr',[lonid,latid,tid],/FLOAT)
    rhoberr=NCDF_VARDEF(wilma,'dpd_obserr',[lonid,latid,tid],/FLOAT)
    rhsperr=NCDF_VARDEF(wilma,'dpd_samplingerr',[lonid,latid,tid],/FLOAT)
    rhrberr=NCDF_VARDEF(wilma,'dpd_rbar',[lonid,latid],/FLOAT)
    rhsberr=NCDF_VARDEF(wilma,'dpd_sbarSQ',[lonid,latid],/FLOAT)
    rhcberr=NCDF_VARDEF(wilma,'dpd_combinederr',[lonid,latid,tid],/FLOAT)
    rhclimvar=NCDF_VARDEF(wilma,'dpd_clims',[lonid,latid,clmid],/FLOAT)
  END
  'td': BEGIN
    rhanomvar=NCDF_VARDEF(wilma,'td_anoms',[lonid,latid,tid],/FLOAT)
    rhabsvar=NCDF_VARDEF(wilma,'td_abs',[lonid,latid,tid],/FLOAT)
    rhsdvar=NCDF_VARDEF(wilma,'td_std',[lonid,latid,tid],/FLOAT)
    rhsterr=NCDF_VARDEF(wilma,'td_stationerr',[lonid,latid,tid],/FLOAT)
    rhajerr=NCDF_VARDEF(wilma,'td_adjerr',[lonid,latid,tid],/FLOAT)
    rhcmerr=NCDF_VARDEF(wilma,'td_climerr',[lonid,latid,tid],/FLOAT)
    rhoberr=NCDF_VARDEF(wilma,'td_obserr',[lonid,latid,tid],/FLOAT)
    rhsperr=NCDF_VARDEF(wilma,'td_samplingerr',[lonid,latid,tid],/FLOAT)
    rhrberr=NCDF_VARDEF(wilma,'td_rbar',[lonid,latid],/FLOAT)
    rhsberr=NCDF_VARDEF(wilma,'td_sbarSQ',[lonid,latid],/FLOAT)
    rhcberr=NCDF_VARDEF(wilma,'td_combinederr',[lonid,latid,tid],/FLOAT)
    rhclimvar=NCDF_VARDEF(wilma,'td_clims',[lonid,latid,clmid],/FLOAT)
  END
  't': BEGIN
    rhanomvar=NCDF_VARDEF(wilma,'t_anoms',[lonid,latid,tid],/FLOAT)
    rhabsvar=NCDF_VARDEF(wilma,'t_abs',[lonid,latid,tid],/FLOAT)
    rhsdvar=NCDF_VARDEF(wilma,'t_std',[lonid,latid,tid],/FLOAT)
    rhsterr=NCDF_VARDEF(wilma,'t_stationerr',[lonid,latid,tid],/FLOAT)
    rhajerr=NCDF_VARDEF(wilma,'t_adjerr',[lonid,latid,tid],/FLOAT)
    rhcmerr=NCDF_VARDEF(wilma,'t_climerr',[lonid,latid,tid],/FLOAT)
    rhoberr=NCDF_VARDEF(wilma,'t_obserr',[lonid,latid,tid],/FLOAT)
    rhsperr=NCDF_VARDEF(wilma,'t_samplingerr',[lonid,latid,tid],/FLOAT)
    rhrberr=NCDF_VARDEF(wilma,'t_rbar',[lonid,latid],/FLOAT)
    rhsberr=NCDF_VARDEF(wilma,'t_sbarSQ',[lonid,latid],/FLOAT)
    rhcberr=NCDF_VARDEF(wilma,'t_combinederr',[lonid,latid,tid],/FLOAT)
    rhclimvar=NCDF_VARDEF(wilma,'t_clims',[lonid,latid,clmid],/FLOAT)
  END
  'tw': BEGIN
    rhanomvar=NCDF_VARDEF(wilma,'tw_anoms',[lonid,latid,tid],/FLOAT)
    rhabsvar=NCDF_VARDEF(wilma,'tw_abs',[lonid,latid,tid],/FLOAT)
    rhsdvar=NCDF_VARDEF(wilma,'tw_std',[lonid,latid,tid],/FLOAT)
    rhsterr=NCDF_VARDEF(wilma,'tw_stationerr',[lonid,latid,tid],/FLOAT)
    rhajerr=NCDF_VARDEF(wilma,'tw_adjerr',[lonid,latid,tid],/FLOAT)
    rhcmerr=NCDF_VARDEF(wilma,'tw_climerr',[lonid,latid,tid],/FLOAT)
    rhoberr=NCDF_VARDEF(wilma,'tw_obserr',[lonid,latid,tid],/FLOAT)
    rhsperr=NCDF_VARDEF(wilma,'tw_samplingerr',[lonid,latid,tid],/FLOAT)
    rhrberr=NCDF_VARDEF(wilma,'tw_rbar',[lonid,latid],/FLOAT)
    rhsberr=NCDF_VARDEF(wilma,'tw_sbarSQ',[lonid,latid],/FLOAT)
    rhcberr=NCDF_VARDEF(wilma,'tw_combinederr',[lonid,latid,tid],/FLOAT)
    rhclimvar=NCDF_VARDEF(wilma,'tw_clims',[lonid,latid,clmid],/FLOAT)
  END
  'e': BEGIN
    rhanomvar=NCDF_VARDEF(wilma,'e_anoms',[lonid,latid,tid],/FLOAT)
    rhabsvar=NCDF_VARDEF(wilma,'e_abs',[lonid,latid,tid],/FLOAT)
    rhsdvar=NCDF_VARDEF(wilma,'e_std',[lonid,latid,tid],/FLOAT)
    rhsterr=NCDF_VARDEF(wilma,'e_stationerr',[lonid,latid,tid],/FLOAT)
    rhajerr=NCDF_VARDEF(wilma,'e_adjerr',[lonid,latid,tid],/FLOAT)
    rhcmerr=NCDF_VARDEF(wilma,'e_climerr',[lonid,latid,tid],/FLOAT)
    rhoberr=NCDF_VARDEF(wilma,'e_obserr',[lonid,latid,tid],/FLOAT)
    rhsperr=NCDF_VARDEF(wilma,'e_samplingerr',[lonid,latid,tid],/FLOAT)
    rhrberr=NCDF_VARDEF(wilma,'e_rbar',[lonid,latid],/FLOAT)
    rhsberr=NCDF_VARDEF(wilma,'e_sbarSQ',[lonid,latid],/FLOAT)
    rhcberr=NCDF_VARDEF(wilma,'e_combinederr',[lonid,latid,tid],/FLOAT)
    rhclimvar=NCDF_VARDEF(wilma,'e_clims',[lonid,latid,clmid],/FLOAT)
  END
  'q': BEGIN
    rhanomvar=NCDF_VARDEF(wilma,'q_anoms',[lonid,latid,tid],/FLOAT)
    rhabsvar=NCDF_VARDEF(wilma,'q_abs',[lonid,latid,tid],/FLOAT)
    rhsdvar=NCDF_VARDEF(wilma,'q_std',[lonid,latid,tid],/FLOAT)
    rhsterr=NCDF_VARDEF(wilma,'q_stationerr',[lonid,latid,tid],/FLOAT)
    rhajerr=NCDF_VARDEF(wilma,'q_adjerr',[lonid,latid,tid],/FLOAT)
    rhcmerr=NCDF_VARDEF(wilma,'q_climerr',[lonid,latid,tid],/FLOAT)
    rhoberr=NCDF_VARDEF(wilma,'q_obserr',[lonid,latid,tid],/FLOAT)
    rhsperr=NCDF_VARDEF(wilma,'q_samplingerr',[lonid,latid,tid],/FLOAT)
    rhrberr=NCDF_VARDEF(wilma,'q_rbar',[lonid,latid],/FLOAT)
    rhsberr=NCDF_VARDEF(wilma,'q_sbarSQ',[lonid,latid],/FLOAT)
    rhcberr=NCDF_VARDEF(wilma,'q_combinederr',[lonid,latid,tid],/FLOAT)
    rhclimvar=NCDF_VARDEF(wilma,'q_clims',[lonid,latid,clmid],/FLOAT)
  END
  'rh': BEGIN
    rhanomvar=NCDF_VARDEF(wilma,'rh_anoms',[lonid,latid,tid],/FLOAT)
    rhabsvar=NCDF_VARDEF(wilma,'rh_abs',[lonid,latid,tid],/FLOAT)
    rhsdvar=NCDF_VARDEF(wilma,'rh_std',[lonid,latid,tid],/FLOAT)
    rhsterr=NCDF_VARDEF(wilma,'rh_stationerr',[lonid,latid,tid],/FLOAT)
    rhajerr=NCDF_VARDEF(wilma,'rh_adjerr',[lonid,latid,tid],/FLOAT)
    rhcmerr=NCDF_VARDEF(wilma,'rh_climerr',[lonid,latid,tid],/FLOAT)
    rhoberr=NCDF_VARDEF(wilma,'rh_obserr',[lonid,latid,tid],/FLOAT)
    rhsperr=NCDF_VARDEF(wilma,'rh_samplingerr',[lonid,latid,tid],/FLOAT)
    rhrberr=NCDF_VARDEF(wilma,'rh_rbar',[lonid,latid],/FLOAT)
    rhsberr=NCDF_VARDEF(wilma,'rh_sbarSQ',[lonid,latid],/FLOAT)
    rhcberr=NCDF_VARDEF(wilma,'rh_combinederr',[lonid,latid,tid],/FLOAT)
    rhclimvar=NCDF_VARDEF(wilma,'rh_clims',[lonid,latid,clmid],/FLOAT)
  END
ENDCASE
climsvar=NCDF_VARDEF(wilma,'month',[charid,clmid],/CHAR)

NCDF_ATTPUT,wilma,'time','standard_name','time'
NCDF_ATTPUT,wilma,'time','long_name','time'
NCDF_ATTPUT,wilma,'time','units','days since 1973-1-1 00:00:00'
NCDF_ATTPUT,wilma,'time','axis','T'
NCDF_ATTPUT,wilma,'time','calendar','gregorian'
NCDF_ATTPUT,wilma,'time','start_year',styr
NCDF_ATTPUT,wilma,'time','end_year',edyr
NCDF_ATTPUT,wilma,'time','start_month',1
NCDF_ATTPUT,wilma,'time','end_month',12

NCDF_ATTPUT,wilma,'month','standard_name','month'
NCDF_ATTPUT,wilma,'month','long_name','month'
NCDF_ATTPUT,wilma,'month','units','days since 1973-1-1 00:00:00'
NCDF_ATTPUT,wilma,'month','axis','T'
NCDF_ATTPUT,wilma,'month','calendar','gregorian'
NCDF_ATTPUT,wilma,'month','start_year',styr
NCDF_ATTPUT,wilma,'month','end_year',edyr
NCDF_ATTPUT,wilma,'month','start_month',1
NCDF_ATTPUT,wilma,'month','end_month',12

NCDF_ATTPUT,wilma,'latitude','standard_name','latitude'
NCDF_ATTPUT,wilma,'latitude','long_name','latitude'
NCDF_ATTPUT,wilma,'latitude','units','degrees_north'
NCDF_ATTPUT,wilma,'latitude','point_spacing','even'
NCDF_ATTPUT,wilma,'latitude','axis','X'

NCDF_ATTPUT,wilma,'longitude','standard_name','longitude'
NCDF_ATTPUT,wilma,'longitude','long_name','longitude'
NCDF_ATTPUT,wilma,'longitude','units','degrees_east'
NCDF_ATTPUT,wilma,'longitude','point_spacing','even'
NCDF_ATTPUT,wilma,'longitude','axis','X'


NCDF_ATTPUT,wilma,'mean_n_stations','long_name','Mean number of stations contributing to gridbox mean'
NCDF_ATTPUT,wilma,'mean_n_stations','units','standard'
min_t=0
max_t=MAX(GB_counts(*,*))
NCDF_ATTPUT,wilma,'mean_n_stations','valid_min',min_t(0)
NCDF_ATTPUT,wilma,'mean_n_stations','valid_max',max_t(0)
NCDF_ATTPUT,wilma,'mean_n_stations','missing_value',-1.e+30
NCDF_ATTPUT,wilma,'mean_n_stations','_FillValue',-1.e+30
NCDF_ATTPUT,wilma,'mean_n_stations','reference_period','1976 to 2005'

printf,19,'MEAN N STATIONS: ',min_t,max_t

NCDF_ATTPUT,wilma,'actual_n_stations','long_name','Actual number of stations within gridbox'
NCDF_ATTPUT,wilma,'actual_n_stations','units','standard'
min_t=0
max_t=MAX(station_counts(*,*,*))
NCDF_ATTPUT,wilma,'actual_n_stations','valid_min',min_t(0)
NCDF_ATTPUT,wilma,'actual_n_stations','valid_max',max_t(0)
NCDF_ATTPUT,wilma,'actual_n_stations','missing_value',-1.e+30
NCDF_ATTPUT,wilma,'actual_n_stations','_FillValue',-1.e+30
NCDF_ATTPUT,wilma,'actual_n_stations','reference_period','1976 to 2005'

printf,19,'ACTUAL N STATIONS: ',min_t,max_t

NCDF_ATTPUT,wilma,rhanomvar,'long_name','Monthly mean anomaly'
NCDF_ATTPUT,wilma,rhanomvar,'units',unitees
NCDF_ATTPUT,wilma,rhanomvar,'axis','T'
valid=WHERE(q_anoms NE -1.E+30, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_anoms(valid))
  max_t=MAX(q_anoms(valid))
  NCDF_ATTPUT,wilma,rhanomvar,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhanomvar,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhanomvar,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhanomvar,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhanomvar,'reference_period','1976 to 2005'

printf,19,'ANOMS: ',min_t,max_t

NCDF_ATTPUT,wilma,rhabsvar,'long_name','Monthly mean absolutes'
NCDF_ATTPUT,wilma,rhabsvar,'units',unitees
NCDF_ATTPUT,wilma,rhabsvar,'axis','T'
valid=WHERE(q_abs NE -1.E+30, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_abs(valid))
  max_t=MAX(q_abs(valid))
  NCDF_ATTPUT,wilma,rhabsvar,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhabsvar,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhabsvar,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhabsvar,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhabsvar,'reference_period','1976 to 2005'

printf,19,'ABS: ',min_t,max_t

NCDF_ATTPUT,wilma,rhsdvar,'long_name','Monthly mean st dev'
NCDF_ATTPUT,wilma,rhsdvar,'units',unitees
NCDF_ATTPUT,wilma,rhsdvar,'axis','T'
valid=WHERE(q_stddevs NE -1.E+30, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_stddevs(valid))
  max_t=MAX(q_stddevs(valid))
  NCDF_ATTPUT,wilma,rhsdvar,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhsdvar,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhsdvar,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhsdvar,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhsdvar,'reference_period','1976 to 2005'

printf,19,'ST DEV: ',min_t,max_t

NCDF_ATTPUT,wilma,rhclimvar,'long_name','Monthly climatology'
NCDF_ATTPUT,wilma,rhclimvar,'units',unitees
valid=WHERE(q_clims NE -1.E+30, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_clims(valid))
  max_t=MAX(q_clims(valid))
  NCDF_ATTPUT,wilma,rhclimvar,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhclimvar,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhclimvar,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhclimvar,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhclimvar,'reference_period','1976 to 2005'

printf,19,'CLIMS: ',min_t,max_t

NCDF_ATTPUT,wilma,rhsterr,'long_name','Station uncertainty over gridbox'
NCDF_ATTPUT,wilma,rhsterr,'units',unitees
valid=WHERE(q_staterr NE mdi, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_staterr(valid))
  max_t=MAX(q_staterr(valid))
  NCDF_ATTPUT,wilma,rhsterr,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhsterr,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhsterr,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhsterr,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhsterr,'reference_period','1976 to 2005'

printf,19,'STATION UNCERTAINTY: ',min_t,max_t

NCDF_ATTPUT,wilma,rhajerr,'long_name','Adjustment uncertainty over gridbox'
NCDF_ATTPUT,wilma,rhajerr,'units',unitees
valid=WHERE(q_adjerr NE mdi, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_adjerr(valid))
  max_t=MAX(q_adjerr(valid))
  NCDF_ATTPUT,wilma,rhajerr,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhajerr,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhajerr,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhajerr,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhajerr,'reference_period','1976 to 2005'

printf,19,'ADJUSTMENT UNCERTAINTY: ',min_t,max_t

NCDF_ATTPUT,wilma,rhoberr,'long_name','Station uncertainty over gridbox'
NCDF_ATTPUT,wilma,rhoberr,'units',unitees
valid=WHERE(q_obserr NE mdi, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_obserr(valid))
  max_t=MAX(q_obserr(valid))
  NCDF_ATTPUT,wilma,rhoberr,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhoberr,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhoberr,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhoberr,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhoberr,'reference_period','1976 to 2005'

printf,19,'MEASUREMENT UNCERTAINTY: ',min_t,max_t

NCDF_ATTPUT,wilma,rhcmerr,'long_name','Station uncertainty over gridbox'
NCDF_ATTPUT,wilma,rhcmerr,'units',unitees
valid=WHERE(q_clmerr NE mdi, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_clmerr(valid))
  max_t=MAX(q_clmerr(valid))
  NCDF_ATTPUT,wilma,rhcmerr,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhcmerr,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhcmerr,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhcmerr,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhcmerr,'reference_period','1976 to 2005'

printf,19,'CLIMATOLOGICAL UNCERTAINTY: ',min_t,max_t

NCDF_ATTPUT,wilma,rhsperr,'long_name','Sampling uncertainty over gridbox'
NCDF_ATTPUT,wilma,rhsperr,'units',unitees
valid=WHERE(q_samperr NE mdi, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_samperr(valid))
  max_t=MAX(q_samperr(valid))
  NCDF_ATTPUT,wilma,rhsperr,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhsperr,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhsperr,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhsperr,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhsperr,'reference_period','1976 to 2005'

printf,19,'SAMPLING UNCERTAINTY: ',min_t,max_t

NCDF_ATTPUT,wilma,rhrberr,'long_name','Intersite correlation (rbar - Jones et al 1997)'
NCDF_ATTPUT,wilma,rhrberr,'units','standard'
valid=WHERE(q_rbar NE mdi, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_rbar(valid))
  max_t=MAX(q_rbar(valid))
  NCDF_ATTPUT,wilma,rhrberr,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhrberr,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhrberr,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhrberr,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhrberr,'reference_period','1976 to 2005'

printf,19,'CROSS CORRELATION: ',min_t,max_t

NCDF_ATTPUT,wilma,rhsberr,'long_name','Mean variance over all stations in gridbox (sbarSQ - Jones et al 1997)'
NCDF_ATTPUT,wilma,rhsberr,'units',unitees
valid=WHERE(q_sbarSQ NE mdi, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_sbarSQ(valid))
  max_t=MAX(q_sbarSQ(valid))
  NCDF_ATTPUT,wilma,rhsberr,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhsberr,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhsberr,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhsberr,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhsberr,'reference_period','1976 to 2005'

printf,19,'GRIDBOX VARIANCE: ',min_t,max_t

NCDF_ATTPUT,wilma,rhcberr,'long_name','Combined uncertainty over gridbox'
NCDF_ATTPUT,wilma,rhcberr,'units',unitees
valid=WHERE(q_comberr NE mdi, tc)
IF tc GE 1 THEN BEGIN
  min_t=MIN(q_comberr(valid))
  max_t=MAX(q_comberr(valid))
  NCDF_ATTPUT,wilma,rhcberr,'valid_min',min_t(0)
  NCDF_ATTPUT,wilma,rhcberr,'valid_max',max_t(0)
ENDIF
NCDF_ATTPUT,wilma,rhcberr,'missing_value',-1.e+30
NCDF_ATTPUT,wilma,rhcberr,'_FillValue',-1.e+30
NCDF_ATTPUT,wilma,rhcberr,'reference_period','1976 to 2005'

printf,19,'TOTAL UNCERTAINTY: ',min_t,max_t

current_time=SYSTIME()

NCDF_ATTPUT,wilma,/GLOBAL,'file_created',STRING(current_time)
NCDF_ATTPUT,wilma,/GLOBAL,'description',"HadISDH monthly mean land surface "+param2+" climate monitoring product from 1973 onwards. "+$
                                         "Quality control, homogenisation, uncertainty estimation, averaging over gridboxes (no smoothing "+$
					 "or interpolation)."
NCDF_ATTPUT,wilma,/GLOBAL,'title',"HadISDH monthly mean land surface "+param2+" climate monitoring product from 1973 onwards."
NCDF_ATTPUT,wilma,/GLOBAL,'institution',"Met Office Hadley Centre (UK), National Climatic Data Centre (USA), Climatic Research Unit (UK), "+$
                                         "National Physical Laboratory (UK), Bjerknes Centre for Climate Research (Norway)"
NCDF_ATTPUT,wilma,/GLOBAL,'history',"Updated "+STRING(current_time)
NCDF_ATTPUT,wilma,/GLOBAL,'source',"HadISD.1.0.3.2014f (Dunn et al., 2012), www.metoffice.gov.uk/hadobs/hadisd/"
NCDF_ATTPUT,wilma,/GLOBAL,'comment'," "
NCDF_ATTPUT,wilma,/GLOBAL,'reference',"Willett, K. M., Dunn, R. J. H., Thorne, P. W., Bell, S., de Podesta, M., Parker, D. E., Jones, "+$
                                       "P. D., and Williams Jr., C. N.: HadISDH land surface multi-variable humidity and temperature "+$
				       "record for climate monitoring, Clim. Past, 10, 1983-2006, doi:10.5194/cp-10-1983-2014, 2014."
NCDF_ATTPUT,wilma,/GLOBAL,'version',"HadISDH.2.0.1.2014p"
NCDF_ATTPUT,wilma,/GLOBAL,'Conventions',"CF-1.0"

NCDF_CONTROL,wilma,/ENDEF

NCDF_VARPUT, wilma,timesvar, dayssince
NCDF_VARPUT, wilma,latsvar, lats
NCDF_VARPUT, wilma,lonsvar, lons
NCDF_VARPUT, wilma,meanstvar,GB_counts
NCDF_VARPUT, wilma,nstvar,station_counts
NCDF_VARPUT, wilma,rhanomvar,q_anoms
NCDF_VARPUT, wilma,rhabsvar,q_abs
NCDF_VARPUT, wilma,rhsdvar,q_stddevs
NCDF_VARPUT, wilma,rhsterr,q_staterr
NCDF_VARPUT, wilma,rhoberr,q_obserr
NCDF_VARPUT, wilma,rhcmerr,q_clmerr
NCDF_VARPUT, wilma,rhajerr,q_adjerr
NCDF_VARPUT, wilma,rhsperr,q_samperr
NCDF_VARPUT, wilma,rhrberr,q_rbar
NCDF_VARPUT, wilma,rhsberr,q_sbarSQ
NCDF_VARPUT, wilma,rhcberr,q_comberr

NCDF_VARPUT, wilma,climsvar,monarr
NCDF_VARPUT, wilma,rhclimvar,q_clims

NCDF_CLOSE,wilma
close,19

bads=where(q_abs EQ mdi,count)
IF (count GT 0) THEN q_abs(bads)=-9999.99
bads=where(q_anoms EQ mdi,count)
IF (count GT 0) THEN q_anoms(bads)=-9999.99
bads=where(q_comberr EQ mdi,count)
IF (count GT 0) THEN q_comberr(bads)=-9999.99

; Write out to ascii
openw,2,outdat+grid+'_actuals_'+nowmon+nowyear+'.dat'
openw,3,outdat+grid+'_anomalies19762005_'+nowmon+nowyear+'.dat'
openw,4,outdat+grid+'_uncertainty_'+nowmon+nowyear+'.dat'

; writes out 72 columns and 36 rows r1c1=-177.5W,87.5N to r36c72=177.5E,87.5S
year=styr
mcount=0
FOR mm=0,nmons-1 DO BEGIN
  printf,2,year,monarr(mcount),format='(i4,x,a3)'
  printf,3,year,monarr(mcount),format='(i4,x,a3)'
  printf,4,year,monarr(mcount),format='(i4,x,a3)'
  FOR ltt=0,35 DO BEGIN
    printf,2,q_abs(*,ltt,mm),format='(72f9.2)'
    printf,3,q_anoms(*,ltt,mm),format='(72f9.2)'
    printf,4,q_comberr(*,ltt,mm),format='(72f9.2)'
  ENDFOR
  mcount=mcount+1
  IF (mcount EQ 12) THEN BEGIN
    mcount=0
    year=year+1
  ENDIF
ENDFOR
printf,2,lons,format='(72f9.2)'
printf,2,lats,format='(36f9.2)'
printf,3,lons,format='(72f9.2)'
printf,3,lats,format='(36f9.2)'
printf,4,lons,format='(72f9.2)'
printf,4,lats,format='(36f9.2)'
close,2
close,3
close,4
stop
end
