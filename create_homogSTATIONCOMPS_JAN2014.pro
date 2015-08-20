pro create_homogSTATIONCOMPS_JAN2014

; program to read through PHA log and pull out neighbour networks for each station
; plot raw station with neighbours from network and then homogenised station
; fit trend to station anomalies and save to file for later comparison with other homogenisation

; median_pairwise.pro

;------------------------------------------------------------------------
;inputs and outputs

param='q'	;'t','td','dpd','e','q','rh',tw'
param2='q'	;'T','Td','DPD','e','q','RH','Tw'
nowmon='DEC'
nowyear='2013'

CASE param OF
  'dpd': BEGIN
    inlist='/data/local/hadkw/HADCRUH2/UPDATE2013/LISTS_DOCS/PosthomogPHAdpd_goodsHadISDH_DEC2013.txt'
    inraw='/data/local/hadkw/HADCRUH2/PROGS/PHA_2013/pha_v52i/data/hadisdh/hadisdh7312dpd/monthly/raw/'	;'99999999999.raw.tavg'
    inhomog='/data/local/hadkw/HADCRUH2/DPDPLAY/MONTHLIES/HOMOG/NEWADJASCII/'					;999999_CWadj.txt'
    inlog='/data/local/hadkw/HADCRUH2/PROGS/PHA_2013/pha_v52i/data/hadisdh/hadisdh7312dpd/output/PHAv52i.FAST.MLY.TEST.1312051205.tavg.hadisdh7312dpd.r00.out'
    outtrends='/data/local/hadkw/HADCRUH2/UPDATE2013/LISTS_DOCS/HadISDH.landDPD.quicklook_7312trends_'+nowmon+nowyear+'.txt'
    outplots='/data/local/hadkw/HADCRUH2/DPDPLAY/MONTHLIES/HOMOG/STAT_PLOTS/ADJCOMPS/'	;'99999999999_MOHCtrendcomp_7311Feb2013.eps'
  END
  'q': BEGIN
    inlist='/data/local/hadkw/HADCRUH2/UPDATE2012/LISTS_DOCS/PosthomogPHA_goodsHadISDH_FEB2013.txt'
    inraw='/data/local/hadkw/HADCRUH2/PROGS/PHA_2013/pha_v52i/data/hadisdh/hadisdh7312/monthly/raw/'	;'99999999999.raw.tavg'
    inhomog='/data/local/hadkw/HADCRUH2/UPDATE2012/MONTHLIES/HOMOG/NEWADJASCII/'					;999999_CWadj.txt'
    inlog='/data/local/hadkw/HADCRUH2/PROGS/PHA_2013/pha_v52i/data/hadisdh/hadisdh7312/output/PHAv52i.FAST.MLY.TEST.1302251617.tavg.hadisdh7312.r00.out'
    outtrends='/data/local/hadkw/HADCRUH2/UPDATE2012/LISTS_DOCS/HadISDH.1.0.0.2012p_7312trends_FEB2013.txt'
    outplots='/data/local/hadkw/HADCRUH2/UPDATE2012/MONTHLIES/HOMOG/STAT_PLOTS/ADJCOMPS/'	;'99999999999_MOHCtrendcomp_7311Feb2013.eps'
  END
ENDCASE

;-------------------------------------------------------------------------
; variables and arrays
mdi=-99.99
styr=1973
edyr=2012
nyrs=(edyr-styr)+1
nmons=((edyr+1)-styr)*12

CASE param OF
  'q': unitees='g/kg'
  'e': unitees='hPa'
  'rh': unitees='%rh'
  ELSE: unitees='deg C'
ENDCASE

rawarr=make_array(nmons,/float,value=mdi)
homogarr=make_array(nmons,/float,value=mdi)
networkarr=make_array(nmons,200,/float,value=mdi)

rawtrend=0.
rawuc=0.
rawlc=0.
homogtrend=0.
homoguc=0.
homoglc=0.

;------------------------------------------------------------------------
; read in station list and loop through

starter='999999'	; Default=999999

openr,7,inlist
openw,9,outtrends
WHILE NOT EOF(7) DO BEGIN
  rawarr=make_array(nmons,/float,value=mdi)
  homogarr=make_array(nmons,/float,value=mdi)
  rawYRarr=make_array(nmons,/float,value=mdi)
  homogYRarr=make_array(nmons,/float,value=mdi)
  rawANMarr=make_array(nmons,/float,value=mdi)
  homogANMarr=make_array(nmons,/float,value=mdi)
  networkarr=make_array(nyrs,200,/float,value=mdi)

  rawtrend=0.
  rawuc=0.
  rawlc=0.
  homogtrend=0.
  homoguc=0.
  homoglc=0.
  neighwmo='00000000000'

  wmo=''
  wban=''
  readf,7,wmo,wban,format='(a6,a5,x)'
  
  IF (starter NE '999999') AND (wmo NE starter) THEN continue
  
; search through PHA log to find candidate station neighbours
  findline='^Dstep Dtrend:'+strcompress(wmo,/remove_all)+strcompress(wban,/remove_all)
;  findline='^Dstep Dtrend:KSH00'+strcompress(wmo,/remove_all)
  spawn,'grep -c "'+findline+'" '+inlog,countDD		;count only
  gotadj=0
  IF (countDD GT 0) THEN BEGIN
    gotadj=1
    spawn,'grep "'+findline+'" '+inlog+' > DDpha.arr'
    openr,99,'DDpha.arr'
    WHILE NOT EOF(99) DO BEGIN
      nwmo=''
      nwban=''
      readf,99,nwmo,nwban,format='(25x,a6,a5,141x)'
;      readf,99,nwmo,format='(30x,a6,141x)'
      neighwmo=[neighwmo,nwmo+nwban]    
;      neighwmo=[neighwmo,nwmo]    
    ENDWHILE
    close,99
    spawn,'rm DDpha.arr'
    neighwmo=neighwmo(SORT(neighwmo))
    neighwmo=neighwmo(1:(n_elements(neighwmo)-1))
    neighwmo=neighwmo(UNIQ(neighwmo))
    countN=n_elements(neighwmo)
; read in raw neighbours
    FOR nn=0,countN-1 DO BEGIN 
      openr,55,inraw+neighwmo(nn)+'*.raw.tavg'
      WHILE NOT EOF(55) DO BEGIN
        yr=0
        tmp=intarr(12)
        readf,55,yr,tmp,format='(12x,i4,12(i6,3x))'
        IF (yr GE styr) AND (yr LE edyr) THEN BEGIN
	  gots=WHERE(tmp/100. NE mdi,count)
	  IF (count GT 8) THEN networkarr(yr-styr,nn)=MEAN(tmp(gots)/100.)
	ENDIF
      ENDWHILE
      close,55
    ENDFOR
  ENDIF
  
; read in candidate raw and candidate homogenised
    rawarr=REFORM(rawarr,12,nyrs)
    openr,55,inraw+wmo+'*.raw.tavg'
    WHILE NOT EOF(55) DO BEGIN
      yr=0
      tmp=intarr(12)
      readf,55,yr,tmp,format='(12x,i4,12(i6,3x))'
      IF (yr GE styr) AND (yr LE edyr) THEN BEGIN
        rawarr(*,yr-styr)=tmp/100.    
        gots=WHERE(tmp/100. NE mdi,count)
	IF (count GT 8) THEN rawYRarr(yr-styr)=MEAN(tmp(gots)/100.)
      ENDIF
    ENDWHILE
    close,55
    rawarr=REFORM(rawarr,nmons)
    
    homogarr=REFORM(homogarr,12,nyrs)
;    openr,55,inhomog+wmo+wban+'.WMs.r00.tavg'
    openr,55,inhomog+wmo+wban+'_PHAadj.txt'
    WHILE NOT EOF(55) DO BEGIN
      yr=0
      tmp=intarr(12)
;      readf,55,yr,tmp,format='(12x,i4,12(i6,3x))'
      readf,55,yr,tmp,format='(12x,i4,12(i6,x))'
;      readf,55,yr,tmp,format='(7x,i4,12(i6,x))'
      IF (yr GE styr) AND (yr LE edyr) THEN BEGIN
        homogarr(*,yr-styr)=tmp/100.    
        gots=WHERE(tmp/100. NE mdi,count)
	IF (count GT 8) THEN homogYRarr(yr-styr)=MEAN(tmp(gots)/100.)
      ENDIF    
    ENDWHILE
    close,55
    homogarr=REFORM(homogarr,nmons)

    ; get anomalies for rawarr and homogarr
    homogANMarr=REFORM(homogarr,12,nyrs)
    rawANMarr=REFORM(rawarr,12,nyrs)
    FOR mm=0,11 DO BEGIN
      gots=WHERE(homogANMarr(mm,*) NE mdi,count)
      IF (count GT 15) THEN homogANMarr(mm,gots)=homogANMarr(mm,gots)-MEAN(homogANMarr(mm,gots)) ELSE homogANMarr(mm,*)=mdi
      gots=WHERE(rawANMarr(mm,*) NE mdi,count)
      IF (count GT 15) THEN rawANMarr(mm,gots)=rawANMarr(mm,gots)-MEAN(rawANMarr(mm,gots)) ELSE rawANMarr(mm,*)=mdi
    ENDFOR
    homogANMarr=REFORM(homogANMarr,nmons)
    rawANMarr=REFORM(rawANMarr,nmons)
    

    rawtrend=median_pairwise(rawANMarr,mdi,se,lc,uc)
    rawtrend=rawtrend*120.
    rawuc=uc*120.
    rawlc=lc*120.
    homogtrend=median_pairwise(homogANMarr,mdi,se,lc,uc)
    homogtrend=homogtrend*120.
    homoguc=uc*120.
    homoglc=lc*120.
    gotsR=WHERE(rawANMarr NE mdi,countR)
    IF (countR EQ 0) THEN BEGIN
      rawtrend=mdi
      rawuc=mdi
      rawlc=mdi
    ENDIF
    gotsH=WHERE(homogANMarr NE mdi,countH) 
    IF (countH EQ 0) THEN BEGIN
      homogtrend=mdi
      homoguc=mdi
      homoglc=mdi 
    ENDIF
 

; plot cand raw, cand raw neighbours and cand homog
    set_plot,'PS'
;    device,filename=outplots+wmo+wban+'_MOHCtrendcomp_7311Feb2013.eps',/color,/ENCAPSUL,xsize=26,ysize=20,/landscape,/helvetica,/bold
    device,filename=outplots+wmo+wban+'_trendcomp_7312Feb2013.eps',/color,/ENCAPSUL,xsize=26,ysize=20,/landscape,/helvetica,/bold
;    device,filename=outplots+wmo+wban+'_trendcomp_'+nowmon+nowyear+'.eps',/color,/ENCAPSUL,xsize=26,ysize=20,/landscape,/helvetica,/bold

    !P.Font=0
    !P.Thick=4
    !X.thick=4
    !Y.thick=4

    !P.Position=[0.08,0.07,0.92,0.92] 
    allnames=['1975','1980','1985','1990','1995','2000','2005','2010']
    tvlct,40,87,255,24 ;blue
    tvlct,216,21,47,25 ;red
 
   
    ymin=FLOOR(MIN(networkarr(WHERE(networkarr NE mdi))))-1.
    ymax=CEIL(MAX(networkarr(WHERE(networkarr NE mdi))))+2.
    yrange=ymax-ymin
    zeros=fltarr(nyrs+1)
    plot,indgen(nyrs+1),zeros,min_value=-100,ystyle=1,xstyle=5,yrange=[ymin,ymax],ythick=4,charsize=1.5,$
      ytitle=unitees,color=0,/noerase,thick=4
    IF (gotadj EQ 1) THEN BEGIN
      FOR nn=0,countN-1 DO BEGIN
        oplot,indgen(nyrs),networkarr(*,nn),min_value=-50,color=0,thick=1
      ENDFOR
    ENDIF
    oplot,indgen(nyrs),rawYRarr,min_value=-50,color=25,thick=8
    oplot,indgen(nyrs),homogYRarr,min_value=-50,color=24,thick=8
    
    PLOTS,[0,nyrs],[ymax,ymax],color=0 ; YEAR***
    PLOTS,[0,nyrs],[ymin,ymin],color=0 ; YEAR***
    

    XYOUTS,3.5,ymax-(yrange*0.08),'RAW: '+string(rawtrend,format='(f6.2)')+' ('+string(rawlc,format='(f6.2)')+' to '+string(rawuc,format='(f6.2)')+')',color=25,charsize=1.5,charthick=2
    XYOUTS,3.5,ymax-(yrange*0.16),'HOMOG: '+string(homogtrend,format='(f6.2)')+' ('+string(homoglc,format='(f6.2)')+' to '+string(homoguc,format='(f6.2)')+')',color=24,charsize=1.5,charthick=2

    yrcount=0
    FOR tt=1,nyrs-1 DO BEGIN
      IF (((tt+3.)/5.)-FLOOR(((tt+3.)/5.)) GT 0.) THEN BEGIN
	PLOTS,[tt,tt],[ymin,ymin+(yrange*0.03)],color=0,thick=4 
	PLOTS,[tt,tt],[ymax,ymax-(yrange*0.03)],color=0,thick=4 
      ENDIF ELSE BEGIN
	PLOTS,[tt,tt],[ymin,ymin+(yrange*0.06)],color=0,thick=4
	PLOTS,[tt,tt],[ymax,ymax-(yrange*0.06)],color=0,thick=4
	XYOUTS,tt,ymin-(yrange*0.03),allnames(yrcount),alignment=0.5,color=0,charsize=1.5,charthick=2
	yrcount=yrcount+1
      ENDELSE
    ENDFOR
    XYOUTS,0.5,0.01,'YEAR',/normal,alignment=0.5,charsize=1.5,charthick=2,color=0

    device,/close


; fit trend to cand raw and cand homog and save to file
    IF ((rawtrend GT 0.) AND (homogtrend LT 0.)) OR ((rawtrend LT 0.) AND (homogtrend GT 0.)) THEN note='DIFF' ELSE note='SAME'
    IF (gotadj EQ 0) THEN note2='NOHO' ELSE note2='HOMO'; no adjustments applied
    printf,9,wmo,wban,'RAW: ',rawtrend,rawlc,rawuc,'HOMOG: ',homogtrend,homoglc,homoguc,note,note2,$
	     format='(a6,a5,x,a5,3(f6.2,x),a7,3(f6.2,x),x,a4,x,a4)'
   

ENDWHILE

close,7
close,9

stop
end
