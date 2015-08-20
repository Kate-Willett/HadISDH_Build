pro plot_HadISDH_adjsmaps_DEC2013


;-----------------------------------------------------
!Except=2

startee=' ' 	; fix as a station to restart
homogtype='DPD'	;'PHA' or 'ID' or 'DPD'
param='td'	;'dpd','rh','td','t','tw','e','q'
param2='Td'	;'DPD','RH','Td','T','Tw','e','q

CASE param OF

  'dpd': BEGIN
  END
  'td': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2013/LISTS_DOCS/PosthomogPHAtd_goodsHadISDH_DEC2013.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2013/LISTS_DOCS/PosthomogPHAtd_satsHadISDH_DEC2013.txt'
      inlog='/data/local/hadkw/HADCRUH2/UPDATE2013/LISTS_DOCS/HadISDH.landTd.quicklook_JUN2013.log' 
      outplots='/data/local/hadkw/HADCRUH2/UPDATE2013/IMAGES/HadISDHTd_adjspreadmaps_DEC2013.eps'
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2013/LISTS_DOCS/PosthomogDPDPHAtd_goodsHadISDH_DEC2013.txt'
      inlistT='/data/local/hadkw/HADCRUH2/UPDATE2013/LISTS_DOCS/PosthomogDPDPHAtd_satsHadISDH_DEC2013.txt'
      inlog='/data/local/hadkw/HADCRUH2/UPDATE2013/LISTS_DOCS/HadISDH.landTd.quicklookDPD_DEC2013.log' 
      outplots='/data/local/hadkw/HADCRUH2/UPDATE2013/IMAGES/HadISDHTd_DPDPHA_adjspreadmaps_DEC2013.eps'
    ENDELSE   
  END
  't': BEGIN
  END
  'tw': BEGIN
  END
  'q': BEGIN
  END
  'e': BEGIN
  END
  'RH': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/RHPLAY/LISTS_DOCS/PosthomogPHArh_goodsHadISDH_OCT2013.txt'
      inlistT='/data/local/hadkw/HADCRUH2/RHPLAY/LISTS_DOCS/PosthomogPHArh_satsHadISDH_OCT2013.txt'
      inlog='/data/local/hadkw/HADCRUH2/RHPLAY/LISTS_DOCS/HadISDH.landRH.quicklook_JUN2013.log' 
      outplots='/data/local/hadkw/HADCRUH2/RHPLAY/IMAGES/HadISDHrh_adjspreadmaps_OCT2013.eps'
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/RHPLAY/LISTS_DOCS/PosthomogIDPHArh_goodsHadISDH_NOV2013.txt'
      inlistT='/data/local/hadkw/HADCRUH2/RHPLAY/LISTS_DOCS/PosthomogIDPHArh_satsHadISDH_NOV2013.txt'
      inlog='/data/local/hadkw/HADCRUH2/RHPLAY/LISTS_DOCS/HadISDH.landRH.indirect_OCT2013.log' 
      outplots='/data/local/hadkw/HADCRUH2/RHPLAY/IMAGES/HadISDHrh_IDPHA_adjspreadmaps_NOV2013.eps'
    ENDELSE   
  END
  
ENDCASE


;--------------------------------------------------------
; variables and arrays
mdi=-1e+30
CASE param OF 
  'dpd': nstations=3359
  'rh': IF (homogtype EQ 'PHA') THEN nstations=3410 ELSE nstations=3619
  'td': IF (homogtype EQ 'PHA') THEN nstations=3316 ELSE nstations=3231
  't': nstations=4000
  'tw': nstations=4000
  'e': nstations=4000
  'q': nstations=4000
ENDCASE

CASE param OF 
  'dpd': nsats=100
  'rh': IF (homogtype EQ 'PHA') THEN nsats=26 ELSE nsats=26
  'td': IF (homogtype EQ 'PHA') THEN nsats=174 ELSE nsats=0	; 100 for DPD but already removed
  't': nsats=4000
  'tw': nsats=4000
  'e': nsats=4000
  'q': nsats=4000
ENDCASE

CASE param OF 
  'dpd': nsubs=0
  'rh': IF (homogtype EQ 'PHA') THEN nsubs=0 ELSE nsubs=0
  'td': nsubs=0
  't': nsubs=4000
  'tw': nsubs=4000
  'e': nsubs=4000
  'q': nsubs=4000
ENDCASE

CASE param OF
  'rh': unitees='% rh'
  'e': unitees='hPa'
  'q': unitees='g/kg'
  ELSE: unitees='deg C'
ENDCASE

styr=1973
edyr=2012
nyrs=(edyr+1)-styr
nmons=nyrs*12
int_mons=indgen(nmons)

If (nsats GT 0) THEN info_arrT={infoz,statid:strarr(nsats)}
If (nsubs GT 0) THEN info_arrZ={infoz,statid:strarr(nsubs)}

stat_adjs=make_array(nmons,nstations,/float,value=mdi)
adj_locs=make_array(nmons,/int,value=0)
adj_mags_accum=100. ;grow this array on the fly
adj_mags_act=100.
adj_lats=999.
adj_wmos='999999'

;---------------------------------------------------------
; open station file

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

;---------------------------------------------------------------------------
; plot lats vs adj on top left
; plot map of max adj. on top right
; plot area average time series on bottom

set_plot,'PS'
device,filename=outplots,/color,/ENCAPSUL,xsize=26,ysize=16,/landscape,/helvetica,/bold
!P.Font=0
!P.Thick=4

tvlct,200,0,0,1
tvlct,150,150,150,2
tvlct,000,0,200,3
!P.Position=[0.33,0.08,0.91,0.92]
XYOUTS,0.33,0.92,'b)',/normal,charsize=1.2

Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2
plotsym,0,0.55,/fill

PLOTS,[-179.9,0],[89.9,89.9],color=0
PLOTS,[0,179.9],[89.9,89.9],color=0
PLOTS,[-179.9,0],[-89.9,-89.9],color=0
PLOTS,[0,179.9],[-89.9,-89.9],color=0


;kcolsarrST=[100,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]	; 14 colours + black to ensure no botching
;levsarrST=[-2e+30,-4.0,-2.0,-1.5,-1.0,-0.75,-0.5,-0.25,-0.1,-0.05,  0.0  ,0.05,0.1,0.25,0.5,0.75,1.0,1.5,2.0,10]
kcolsarrST=[100,1,4,5,6,7,8,9,10,11,13,14,15,16,18]	; 14 colours + black to ensure no botching
levsarrST=[-2e+30,-40.0,-12.0,-8.0,-4.0,-2.0,-1.0,-0.5,  0.0  ,0.5,1.,2.0,4.0,8.0,12.0,40]
; colour settings - Uni ORegon brown to blue
tvlct,0,0,0,0
tvlct,240,240,240,100

  tvlct,10,0,0,1
  tvlct,20,1,0,2
  tvlct,30,5,0,3
  tvlct,51,25,0,4
  tvlct,102,47,0,5
  tvlct,153,96,53,6
  tvlct,204,155,122,7
  tvlct,216,175,151,8
  tvlct,242,218,205,9
  tvlct,204,253,255,10
  tvlct,153,248,255,11
  tvlct,101,239,255,12
  tvlct,50,227,255,13
  tvlct,0,169,204,14
  tvlct,0,122,153,15
  tvlct,0,75,100,16
  tvlct,0,40,80,17
  tvlct,0,10,40,18

ncols=n_elements(kcolsarrST)
colsarrST=kcolsarrST(1:ncols-1)
nlevs=n_elements(levsarrST)-1
labsarrST=strarr(nlevs)
labsarrST(0)=''
labsarrST((nlevs-1))=''
labsarrST(1:nlevs-2)=string(levsarrST(2:nlevs-1),format='(f5.2)')

MAKE_KEY,0.92,0.08,0.02,0.84,0.03,-0.01,/NORMAL,COLORS=colsarrST,labels=labsarrST,$
         charsize=1.1,charthick=4,bcolor=0,orientation=1
XYOUTS,0.93,0.935,unitees,/normal,color=0,charsize=1.2,alignment=0.5



; read in and loop through all station info
openr,5,inlist
counter=0
WHILE NOT EOF(5) DO BEGIN
  stadj=-999.
  stmon=0
  edmon=0
  ibreak=0
  cbreak=0
  adj=0.
  eadj=0.
  wmo=''
  lat=0.
  lon=0.
  elv=0.
  cid=''
  namoo=''
  mush=''
  readf,5,wmo,lat,lon,elv,cid,namoo,format='(a11,f9.4,f10.4,f7.1,x,a2,x,a29,x)'  
  IF (startee NE ' ') AND (startee NE wmo) THEN continue    ;restart code 

; remove subzeros or supersats stations 
  IF (nsubs GT 0) THEN BEGIN 
    findee=WHERE(info_arrZ.statid EQ wmo,count)
    IF (count GT 0) THEN goto,endloop
  ENDIF
  IF (nsats GT 0) THEN BEGIN 
    findee=WHERE(info_arrT.statid EQ wmo,count)
    IF (count GT 0) THEN goto,endloop
  ENDIF

 ; find homog file and read in to array 
; read in log and find adjustment uncertainties - apply
    IF (homogtype EQ 'PHA') THEN findline='^Adj write:'+strcompress(wmo,/remove_all) $
                            ELSE findline='^'+strcompress(wmo,/remove_all)
    spawn,'grep "'+findline+'" '+inlog+' > tmp.arr'
    openr,4,'tmp.arr'
    adjvals=100.
    countadj=0
    dummy='a'
    readf,4,dummy,format='(a)'	; ignore first line - no adj in recent period
    WHILE NOT EOF(4) DO BEGIN
      stadj=-999.
      stmon=0
      edmon=0
      ibreak=0
      cbreak=0
      adj=0.
      eadj=0.
      IF (homogtype EQ 'PHA') THEN readf,4,stmon,edmon,ibreak,cbreak,adj,eadj,format='(32x,i4,16x,i4,12x,i1,4x,i1,2(x,f6.2),x)' $
                              ELSE readf,4,stmon,edmon,adj,eadj,format='(14x,i4,i4,14x,2(f7.2))'
;      print,stmon,edmon,ibreak,cbreak,adj,eadj
      stat_adjs(stmon-1:edmon-1,counter)=-(adj) ; these go from 1+, not 0+, first in loop is most recent period - no adjustment here
      loc=edmon-1
;      IF (edmon-1 EQ int_mons(nmons-1)) THEN continue ;loops past most recent period where adj=0.
      adj_locs(loc)=adj_locs(loc)+1 
      ; CHECK - IS THIS A 5th-95th or 25th-75th? Is it one sided or a range?
      countadj=countadj+1
      IF (adj_mags_accum(0) EQ 100.) THEN adj_mags_accum=-(adj) ELSE adj_mags_accum=[adj_mags_accum,-(adj)]
      IF (adjvals(0) EQ 100.) THEN adjvals=-(adj) ELSE adjvals=[adjvals,-(adj)]
      IF (adj_lats(0) EQ 999.) THEN adj_lats=lat ELSE adj_lats=[adj_lats,lat]
      IF (adj_wmos(0) EQ '999999') THEN adj_wmos=wmo ELSE adj_wmos=[adj_wmos,wmo]
      IF (stadj EQ -999.) THEN stadj=-(adj) ELSE stadj=[stadj,-(adj)]
       
    ENDWHILE
    close,4
     ; find largest adjustment and plot for that station
      pinpoint=WHERE(ABS(stadj) EQ MAX(ABS(stadj)))
      pincol=WHERE(levsarrST GT stadj(pinpoint(0)))
      coll=kcolsarrST(pincol(0)-1)
      print,lat,lon,stadj(pinpoint(0)),coll
      IF (coll NE 100) THEN PLOTS,lon,lat,psym=8,color=coll,symsize=0.8 


    spawn,'rm tmp.arr'
    ; now get actual adjustments from adjvals
    FOR ca=0,countadj-1 DO BEGIN
      IF (ca EQ 0) THEN BEGIN
        IF (adj_mags_act(0) EQ 100.) THEN adj_mags_act=adjvals(ca) ELSE adj_mags_act=[adj_mags_act,adjvals(ca)]
      ENDIF ELSE BEGIN
        deltaadj=adjvals(ca)-adjvals(ca-1)
        adj_mags_act=[adj_mags_act,deltaadj]
      ENDELSE
    ENDFOR  
  endloop:
ENDWHILE
close,5
;    PLOT SCATTER OF ADJS vs LATS
 !P.Font=0
 !P.Thick=4
 !X.thick=4
 !Y.thick=4

 !P.Position=[0.07,0.08,0.31,0.92]
  XYOUTS,0.01,0.92,'a)',/normal,color=0,charsize=1.2
  ymin=FLOOR(MIN(adj_mags_act))
  ymax=CEIL(MAX(adj_mags_act))
  print,ymin,ymax
  plot,adj_mags_act,adj_lats,min_value=-100,xrange=[ymin,ymax],yrange=[-90,90],ystyle=1,xstyle=1,psym=8,symsize=0.4,$
       xtitle='Adjustment '+unitees,ytitle='Latitude',charsize=1,xminor=2,/noerase

  PLOTS,[0,0],[-90,90],/data,color=0,thick=1
print,'Average number of stations: ',n_elements(adj_mags_act)/FLOAT(nstations)
print,'Average Adjustment size: ',mean(adj_mags_act)	; relative to next most recent homogeneous sub period
print,'1 Standard Deviation of Adjustment size: ',stddev(adj_mags_act)

 
device,/close


stop
end
