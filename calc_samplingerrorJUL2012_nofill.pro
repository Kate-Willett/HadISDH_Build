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
; Version 1 (7 September 2016)
; ---------
;  
; Enhancements
;  
; Changes
;  
; Bug fixes
; Changed cled to work with cllms(1)+1 rather than cllms(1) - to include the last 12 months of the final year.
; This was wrong previously - the sampling error (and gridbox variance) and hence total uncertainty is now slightly wider range for some
; e.g. q v2.1.0.2015p anoms7605 0.0440257-3.59143 compared to OLD 0.0442797-3.59118
; and similar but shifted for others
; e.g. RH v2.1.0.2015p anoms7605 0.322419029.0441 compared to OLD 0.323116-29.0480
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


function calc_samplingerrorJUL2012_nofill,datarr,latts,lonns,nstats,statcounts,mdi,cllms,samps_details


;q_samperr=calc_samplingerrorJUL2012(stat_anoms,lats,lons,nlats,nlons,GB_counts,mdi)
;datarr - 3 dimensional data array longs, lats, months - these are anomalies
;latts - 1 dimensional array containing latitudes
;lonns - 1 dimensional array containing longitudes
;nstats - 1 dimensional array of station counts, longs, lats, counts (0=total)
;statcounts=3 dimensaional array of actual statin counts
;mdi - missing data indicator
;cllms = clst - pointer for beginning of climatology period in years - needs changing to months
    	;cled - pointer for end of climatology period in years - needs changing to months
;samps_details = output for rbar and sbarSQ


; sampling error - after Jones et al. 1997

;Shat^2 = variance of gridbox(extended?) means over climatology period
;n = number of stations contributing to gridbox(extended?) over climatology period
;Xo = correlation decay distance (km) for that gridbox (where correlation = 1/e)
;Xdiag = diagonal from bottom left to top right of gridbox(extended?) (km) - use lats, longs and dist_calc
;rbar = (Xo/Xdiag)*(1-e(-Xdiag/Xo))
;sbar^2 = mean station variance within the gridbox
;sbar^2 = (Shat^2*n)/(1+((n-1)*rbar))
;INFILL empty gridboxes by interpolated Xo and then calculating rbar
;   Jones et al take 15 deg north and south, 25 deg east and west and average using a gaussian weighted filter
;   in 5 by 5 that gives 3 boxes north and south (6+1) and 5 boxes east and west (10+1) which gives
;   7*11 = 77 boxes
; I'll take nearest 77 boxes - if they have data then smooth over that - if they don't = say Xo=500km (CHECK)
; gaussian filtering - G(x,y)= (1/(2*pi*(stdev^2)))*EXP(-((x^2+y^2)/(2*stdev^2)))
; from http://homepages.inf.ed.ac.uk/rbf/HIPR2/gsmooth.htm
; WILL NEED LAND SEA MASK FOR THIS - OTHERDATA/new_coverpercentjul08.nc
; only infill for land only - but what about where % land <100%? - still has same error stats though?

;SE^2 = gridbox sampling error
;SE^2 = (sbar^2*rbar*(1-rbar))/(1+((n-1)*rbar))
;SE^2 (where n=0) = sbar^2*rbar (INFILL GB with Shat^2 - same technique as above)

;SEglob^2 = global average sampling error
;SEglob^2 = SEbar^2/Neff
;SEbar^2 = (SUM(SE^2*cos(lat)))/(SUM(cos(lat)))
;Neff = number of effectively independent points
;Neff = (2*R)/F
;R = radius of the earth (6371 km)
;F=(((e((-piR)/Xobar))/R)+(1/R))/((1/(Xobar^2))+(1/R^2))
;Xobar=(SUM(Xo*cos(lat)))/(SUM(cos(lat)))


; WHERE NO Xo or ShadSQarr: Gaussian weighted mean of surrounding GB within +/ 15lat and 25 lon, 
;   	    	    	    or the single value within that region 
;   	    	    	    or Xo=500 and ShatSQarr=10.

; if there are insufficient data points OR Xo could not be calculated then interpolate (carry on)
; also - only go there if the land-sea mask says LAND (gt 0%) - and/or if Xo already set to 500.
; should be values within +/3-5 boxes for all land points except Antarctic?
; if I really can't fill then it will be 500
; CHECK WHETHER 500 thing is sensible
; get Xo for all other gridboxes with data and their distances
;INFILL empty gridboxes by interpolated Xo and then calculating rbar
;   Jones et al take 15 deg north and south, 25 deg east and west and average using a gaussian weighted filter
;   in 5 by 5 that gives 3 boxes north and south (6+1) and 5 boxes east and west (10+1) which gives
;   7*11 = 77 boxes
; I'll take nearest 77 boxes - if they have data then smooth over that - if they don't = say Xo=500km (CHECK)
; gaussian filtering - G(x,y)= (1/(2*pi*(stdev^2)))*EXP(-((x^2+y^2)/(2*stdev^2)))
; from http://homepages.inf.ed.ac.uk/rbf/HIPR2/gsmooth.htm

; PROBLEM - not getting true standard deviation if there are missing gridboxes!!!
	; get gaussian weighting for each gridbox and apply to Xo value in readiness to calculate a weighted mean

;----------------------------------------------------------------------
ntims=n_elements(datarr(0,0,*))
nlts=n_elements(datarr(0,*,0))
nlns=n_elements(datarr(*,0,0))

lthf=ABS(latts(1)-latts(0))/2.
lnhf=ABS(lonns(1)-lonns(0))/2.
ltfl=ABS(latts(1)-latts(0))
lnfl=ABS(lonns(1)-lonns(0))

ngaussltbx=(15.*2)/ltfl ; if ltfl is 5 then this should be 3 	
ngausslnbx=(25.*2)/lnfl ; if lnfl is 5 then this should be 5
;print,ngaussltbx,ngausslnbx

radearth=6371.	; earth's radius in km

ShatSQarr=make_array(nlns,nlts,/float,value=mdi)
Xo=make_array(nlns,nlts,/float,value=mdi)
Xdiag=make_array(nlns,nlts,/float,value=mdi)
rbar=make_array(nlns,nlts,/float,value=mdi)
sbarSQ=make_array(nlns,nlts,/float,value=mdi)
SESQ=make_array(nlns,nlts,ntims,/float,value=mdi)

;renew each loop
GBcorrs=make_array(nlns,nlts,/float,value=mdi)
GBdists=make_array(nlns,nlts,/float,value=mdi)

;convert clim pointers to months not years
clst=cllms(0)*12
cled=(cllms(1)+1)*12 ; +1 to capture all 12 months of last year BUG FIX SEPTEMBER 2016

inLSmask='/data/users/hadkw/WORKING_HADISDH/UPDATE2018/OTHERDATA/new_coverpercentjul08.nc'
; lat goes from 87.5 to -87.5 so flip array to match input data
inLS=NCDF_OPEN(inLSmask)
LSid=NCDF_VARID(inLS,'pct_land')
NCDF_VARGET,inLS,LSid,landpct
NCDF_CLOSE,inLS
landpct=REVERSE(landpct,2)



; once through for actuals
FOR lnn=0,nlns-1 DO BEGIN
  FOR ltt=0,nlts-1 DO BEGIN
; calc the diagonal distance of the gridbox at this lat and lon - it will differ
    radlat2=DOUBLE(EOS_EH_CONVANG(latts(ltt)-lthf,1))	; code 1 = degrees to radians
    radlon2=DOUBLE(EOS_EH_CONVANG(lonns(lnn)-lnhf,1))	; code 1 = degrees to radians
    radlat1=EOS_EH_CONVANG(latts(ltt)+lthf,1)	    	; code 1 = degrees to radians
    radlon1=EOS_EH_CONVANG(lonns(lnn)+lnhf,1)	    	; code 1 = degrees to radians
    deltalat = radlat2-radlat1
    deltalon = radlon2-radlon1
    aaa=DOUBLE(((SIN(deltalat/2.))^2)+((COS(radlat1))*(COS(radlat2))*((SIN(deltalon/2.))^2)))
    ccc=DOUBLE(2.*(ATAN(SQRT(aaa), SQRT(1.-aaa))))
    Xdiag(lnn,ltt)=DOUBLE(radearth*ccc)
;    print,Xdiag(lnn,ltt),lonns(lnn),latts(ltt)
;    stop, 'Check dist calcs'
    subarr=datarr(lnn,ltt,clst:cled) ;this should be 30*12 so 360 months lets say there must be 1/3 so 120 months
    gooddats=WHERE(subarr NE mdi,count)
; if there are enough data points then carry on
    IF (count GE 120) THEN BEGIN
      print,Xdiag(lnn,ltt),lonns(lnn),latts(ltt)
    
; calc the correlation decay distance for this gridbox - I think this will differ gridbox to gridbox
; this is involved and will take a while.
    ;renew each loop
      GBcorrs=make_array(nlns,nlts,/float,value=mdi)
      GBdists=make_array(nlns,nlts,/float,value=mdi)
      GBcorrs(lnn,ltt)=1.
      GBdists(lnn,ltt)=0.
      FOR lnn2=0,nlns-1 DO BEGIN
        FOR ltt2=0,nlts-1 DO BEGIN
	  subarr2=datarr(lnn2,ltt2,clst:cled)
          gots=WHERE(subarr NE mdi AND subarr2 NE mdi,count)
   	  IF (count GE 10) THEN BEGIN
	    GBcorrs(lnn2,ltt2)=CORRELATE(subarr(gots),subarr2(gots))
            radlat2=DOUBLE(EOS_EH_CONVANG(latts(ltt),1))	; code 1 = degrees to radians
            radlon2=DOUBLE(EOS_EH_CONVANG(lonns(lnn),1))	; code 1 = degrees to radians
            radlat1=EOS_EH_CONVANG(latts(ltt2),1)	    	; code 1 = degrees to radians
            radlon1=EOS_EH_CONVANG(lonns(lnn2),1)	    	; code 1 = degrees to radians
            deltalat = radlat2-radlat1
            deltalon = radlon2-radlon1
            aaa=DOUBLE(((SIN(deltalat/2.))^2)+((COS(radlat1))*(COS(radlat2))*((SIN(deltalon/2.))^2)))
            ccc=DOUBLE(2.*(ATAN(SQRT(aaa), SQRT(1.-aaa))))
            GBdists(lnn2,ltt2)=DOUBLE(radearth*ccc)
	  ENDIF
        ENDFOR
      ENDFOR
      gots=WHERE(GBcorrs NE mdi,count)
      IF (count GT 0) THEN BEGIN    
        GBcorrs=REFORM(GBcorrs(gots),count)
        GBdists=REFORM(GBdists(gots),count)
        sortcorrs=GBcorrs(REVERSE(SORT(GBcorrs)))
        sortdists=GBdists(REVERSE(SORT(GBcorrs)))
        ;lows=WHERE(sortcorrs LE (1./EXP(1)),countlows)
        ;IF (countlows GT 0) THEN Xo(lnn,ltt)=sortdists(lows(0)) ELSE Xo(lnn,ltt)=max(sortdists)
        ;plot,sortdists,sortcorrs,psym=5,symsize=0.6
        ;print,countlows,Xo(lnn,ltt)
	xdist=indgen(30)*500	; distances from 0 to 15000km
	ycorrs=fltarr(30)
	ycorrs(0)=1.	;always 500km
	FOR i=1,29 DO BEGIN
	  ins=WHERE(sortdists GE xdist(i-1) AND sortdists LT xdist(i),countins)
	  IF (countins GT 0) THEN ycorrs(i)=MEAN(sortcorrs(ins)) ELSE ycorrs(i)=0.4 ; force to be bigger than 1/e just in case there is a gap
	ENDFOR
	lows=WHERE(ycorrs LE (1./EXP(1)),countlows)
        IF (countlows GT 0) THEN Xo(lnn,ltt)=xdist(lows(0)) ELSE Xo(lnn,ltt)=xdist(29)
        oplot,xdist,ycorrs,color=200
        print,countlows,Xo(lnn,ltt)
;        stop,'Check methods for getting correlation decay distance
      ENDIF ELSE Xo(lnn,ltt)=500.     ; arbitrarily low number - CHECK THIS IS REASONABLE
; now get Shat^2 - 
      ShatSQarr(lnn,ltt)=STDDEV(subarr(gooddats))^2
; now get rbar = (Xo/Xdiag)*(1-e(-Xdiag/Xo))
      rbar(lnn,ltt)=(Xo(lnn,ltt)/Xdiag(lnn,ltt))*(1.-EXP(-Xdiag(lnn,ltt)/Xo(lnn,ltt)))
; now get sbar^2 = (Shat^2*n)/(1+((n-1)*rbar))
      sbarSQ(lnn,ltt)=(ShatSQarr(lnn,ltt)*nstats(lnn,ltt))/(1.+((nstats(lnn,ltt)-1)*rbar(lnn,ltt)))
;now get SE^2 = (sbar^2*rbar*(1-rbar))/(1+((n-1)*rbar))
      gotcounts=WHERE(statcounts(lnn,ltt,*) GT 0,countcounts)
      IF (countcounts GT 0) THEN SESQ(lnn,ltt,gotcounts)=((sbarSQ(lnn,ltt)*rbar(lnn,ltt)*(1.-rbar(lnn,ltt)))/$
         (1.+((statcounts(lnn,ltt,gotcounts)-1.)*rbar(lnn,ltt))))*2
	 ; 2 sigma errors!!!!
      print,ShatSQarr(lnn,ltt),rbar(lnn,ltt),sbarSQ(lnn,ltt),SESQ(lnn,ltt)
;      stop,'Check sampling errors for data gridboxes'
    ENDIF
  ENDFOR
ENDFOR

;**** LEAVING THIS FOR NOW - MAY NEED GCMs TO INFILL OVER ANTARCTIC

;twice through for interpolation over missing gridboxes
FOR lnn=0,nlns-1 DO BEGIN
  FOR ltt=0,nlts-1 DO BEGIN
    subarr=datarr(lnn,ltt,clst:cled)	;this should be 30*12 so 360 months lets say there must be 1/3 so 120 months
    gooddats=WHERE(subarr NE mdi,count)
; if there are insufficient data points OR Xo could not be calculated then interpolate (carry on)
; also - only go there if the land-sea mask says LAND (gt 0%) - and/or if Xo already set to 500.
; should be values within +/3-5 boxes for all land points except Antarctic?
; if I really can't fill then it will be 500
; CHECK WHETHER 500 thing is sensible
    IF ((count LT 120) AND (landpct(lnn,ltt) GT 0)) THEN BEGIN
      weighty=0.
      totweights=0.
      totsbarSQ=0.
      totrbar=0.
; get Xo for all other gridboxes with data and their distances
;INFILL empty gridboxes by interpolated Xo and then calculating rbar
;   Jones et al take 15 deg north and south, 25 deg east and west and average using a gaussian weighted filter
;   in 5 by 5 that gives 3 boxes north and south (6+1) and 5 boxes east and west (10+1) which gives
;   7*11 = 77 boxes
; I'll take nearest 77 boxes - if they have data then smooth over that - if they don't = say Xo=500km (CHECK)
; gaussian filtering - G(x,y)= (1/(2*pi*(stdev^2)))*EXP(-((x^2+y^2)/(2*stdev^2)))
; from http://homepages.inf.ed.ac.uk/rbf/HIPR2/gsmooth.htm

; PROBLEM - not getting true standard deviation if there are missing gridboxes!!!
    ;renew each loop
      GBrbar=make_array(ngausslnbx+1,ngaussltbx+1,/float,value=mdi)
      GBSbarSQ=make_array(ngausslnbx+1,ngaussltbx+1,/float,value=mdi)
      GBdists=make_array(ngausslnbx+1,ngaussltbx+1,3,/float,value=0.)	;0=actual distance, 1=distance E-W(x), 2=distance S-N(y)
      FOR lnn2=0,ngausslnbx DO BEGIN	    ;not -1 because this must include boxes either side AND candidate box
        ; longs can wrap around therefore no problem
	lnpt=(lnn-(ngausslnbx/2.))+lnn2
	IF (lnpt LT 0) THEN lnpt=nlns+lnpt
	IF (lnpt GE nlns) THEN lnpt=lnpt-nlns
;	print,'LONGS: ',lnn2,lnpt
        FOR ltt2=0,ngaussltbx DO BEGIN
	  ; lats cannot wrap around - if get to > ABS(77.5) then just use the boxes there are in that hemisphere
          ltpt=(ltt-(ngaussltbx/2.))+ltt2
	  IF (ltpt LT 0) THEN continue
	  IF (ltpt GE nlts) THEN continue
;	  print,'LATS: ',ltt2,ltpt,rbar(lnpt,ltpt),sbarSQ(lnpt,ltpt)
          IF (rbar(lnpt,ltpt) NE mdi) AND (rbar(lnpt,ltpt) NE 0.1) THEN GBrbar(lnn2,ltt2)=rbar(lnpt,ltpt) 
	  ; don't infill with the ARBITRARILY POOR values in case there are real values in there 
          IF (sbarSQ(lnpt,ltpt) NE mdi) AND (sbarSQ(lnpt,ltpt) NE 10) THEN GBSbarSQ(lnn2,ltt2)=sbarSQ(lnpt,ltpt)
	  radlat2=DOUBLE(EOS_EH_CONVANG(latts(ltt),1))	; code 1 = degrees to radians
          radlon2=DOUBLE(EOS_EH_CONVANG(lonns(lnn),1))	; code 1 = degrees to radians
          radlat1=EOS_EH_CONVANG(latts(ltpt),1)	    	; code 1 = degrees to radians
          radlon1=EOS_EH_CONVANG(lonns(lnpt),1)	    	; code 1 = degrees to radians
          deltalat = radlat2-radlat1
          deltalon = radlon2-radlon1
          deltaUPlat=deltalat
          deltaUPlon=0.
          deltaACSlat=0.
          deltaACSlon=deltalon 
	  aaa=DOUBLE(((SIN(deltalat/2.))^2)+((COS(radlat1))*(COS(radlat2))*((SIN(deltalon/2.))^2)))
          ccc=DOUBLE(2.*(ATAN(SQRT(aaa), SQRT(1.-aaa))))
          GBdists(lnn2,ltt2,0)=DOUBLE(radearth*ccc)
	  aaa=DOUBLE(((SIN(deltaACSlat/2.))^2)+((COS(0.))*(COS(radlat2))*((SIN(deltaACSlon/2.))^2)))
          ccc=DOUBLE(2.*(ATAN(SQRT(aaa), SQRT(1.-aaa))))
          GBdists(lnn2,ltt2,1)=DOUBLE(radearth*ccc)
	  aaa=DOUBLE(((SIN(deltaUPlat/2.))^2)+((COS(radlat1))*(COS(radlat2))*((SIN(deltaUPlon/2.))^2)))
          ccc=DOUBLE(2.*(ATAN(SQRT(aaa), SQRT(1.-aaa))))
          GBdists(lnn2,ltt2,2)=DOUBLE(radearth*ccc)
	  IF (lnn2 LT ngausslnbx/2.) THEN GBdists(lnn2,ltt2,2)=-(GBdists(lnn2,ltt2,2))
	  IF (ltt2 LT ngaussltbx/2.) THEN GBdists(lnn2,ltt2,1)=-(GBdists(lnn2,ltt2,1))
;	  print,'X and Y dists: ',GBdists(lnn2,ltt2,0),GBdists(lnn2,ltt2,1),GBdists(lnn2,ltt2,2)
        ENDFOR
      ENDFOR
;      stop,'CHECK GBdists X and Y dists'
      gots=WHERE(GBSbarSQ NE mdi,count)
      IF (count GT 1) THEN BEGIN
	SDdist=STDDEV(REFORM(GBdists(*,*,0),n_elements(GBdists(*,*,0))))  	; standard deviation of distances from centre gridbox
	; get gaussian weighting for each gridbox and apply to Xo value in readiness to calculate a weighted mean
	; first need to normalise to give stdev of ~1 and mean of ~0
	GBdists(*,*,1)=(GBdists(*,*,1)-MEAN(GBdists(*,*,1)))/SDdist
	GBdists(*,*,2)=(GBdists(*,*,2)-MEAN(GBdists(*,*,2)))/SDdist
        FOR lnn2=0,ngausslnbx DO BEGIN	    ;not -1 because this must include boxes either side AND candidate box
          lnpt=(lnn-(ngausslnbx/2.))+lnn2
	  IF (lnpt LT 0) THEN lnpt=nlns+lnpt
	  IF (lnpt GE nlns) THEN lnpt=lnpt-nlns
          FOR ltt2=0,ngaussltbx DO BEGIN
            ltpt=(ltt-(ngaussltbx/2.))+ltt2
	    IF (ltpt LT 0) THEN ltpt=nlts+ltpt
	    IF (ltpt GE nlts) THEN ltpt=ltpt-nlts
            IF (GBSbarSQ(lnn2,ltt2) NE mdi) THEN BEGIN
	      nsd=1 	; 1 standard dev
	      weighty=(1./((2*!pi*(nsd^2))))*EXP(-(((GBdists(lnn2,ltt2,1)^2)+(GBdists(lnn2,ltt2,2)^2))/(2*(nsd^2))))
;              print,'WEIGHTING HERE: ',weighty
	      totweights=totweights+weighty
              totsbarSQ=totsbarSQ+(GBSbarSQ(lnn2,ltt2)*weighty)
	      totrbar=totrbar+(GBrbar(lnn2,ltt2)*weighty)
	    ENDIF
          ENDFOR
        ENDFOR
	IF (totweights GT 0.) THEN BEGIN
	  sbarSQ(lnn,ltt)=totsbarSQ/totweights    
	  rbar(lnn,ltt)=totrbar/totweights
	ENDIF
;	stop,'CHECK OUT GBSbarSQ and GBrbar and totals'
      ENDIF ELSE IF (count EQ 1) THEN BEGIN
	sbarSQ(lnn,ltt)=GBSbarSQ(gots(0))  
	rbar(lnn,ltt)=GBrbar(gots(0))
      ENDIF ELSE BEGIN	    	; FILL WITH ARBITRARY POOR VALUES
	sbarSQ(lnn,ltt)=10.    
	rbar(lnn,ltt)=0.8 ; This was 0.1 but this gives a small SE      
      ENDELSE
;now get SE^2 = (sbar^2*rbar)	WHEN n=0
      gotcounts=WHERE(statcounts(lnn,ltt,*) GT 0,countcounts)
      IF (countcounts GT 0) THEN SESQ(lnn,ltt,gotcounts)=((sbarSQ(lnn,ltt)*rbar(lnn,ltt)*(1.-rbar(lnn,ltt)))/$
         (1.+((statcounts(lnn,ltt,gotcounts)-1.)*rbar(lnn,ltt))))*2
	 ; 2 sigma errors!!!!
;      nocounts=WHERE(statcounts(lnn,ltt,*) EQ 0,countcounts)
;      IF (countcounts GT 0) THEN SESQ(lnn,ltt,nocounts)=(sbarSQ(lnn,ltt)*rbar(lnn,ltt))*2

	 ; 2 sigma errors!!!!
       print,rbar(lnn,ltt),sbarSQ(lnn,ltt),SESQ(lnn,ltt)
;      stop,'Check filled sampling errors for data gridboxes'
    ENDIF
  ENDFOR
ENDFOR

;stop,'Check Xo variability - is 500 a reasonable arbitrary number?'

returnarr=fltarr(nlns,nlts,ntims)	; 0 is SEsq, 1 is rbar (intersite correlation), 2 is sbarSQ (mean variance of all stations in gridbox) - save to netCDF)
returnarr(*,*,*)=SESQ(*,*,*)
samps_details(*,*,0)=rbar(*,*)
samps_details(*,*,1)=sbarSQ(*,*)

return,returnarr

end
