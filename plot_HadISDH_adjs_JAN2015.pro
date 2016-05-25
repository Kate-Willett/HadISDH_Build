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


pro plot_HadISDH_adjs_JAN2015

; RESULTS 2016
; q - ID 
; 3.99 changepoints per station
; ABS mean=0.26, st dev=0.30
; Mean = -0.01, st dev=0.40
; mean of diffs=-0.01, stdev=0.16

; RH - ID 
; 3.99 changepoints per station
; ABS mean=2.88, st dev=2.19
; Mean = 0.01, st dev=3.62
; mean of diffs=0.03, stdev=1.01

; e - ID
; 3.99 changepoints per station
; ABS mean=0.41, st dev=0.46
; Mean = -0.01, st dev=0.62
; mean of diffs=0.00, stdev=0.20

; Tw - ID 
; 3.99 changepoints per station
; ABS mean=0.31, st dev=0.37
; Mean = -0.01, st dev=0.48
; mean of diffs=0.00, stdev=0.18

; T - PHA+ID 
; 3.81 changepoints per station
; ABS mean=0.39, st dev=0.49
; Mean = -0.02, st dev=0.62
; mean of diffs=0.00, stdev=0.26

; T - PHA 
; 1.43 changepoints per station
; ABS mean=0.75, st dev=0.63
; Mean = -0.09, st dev=0.98
; mean of diffs=0.00, stdev=0.19

; DPD - PHA
; 2.68 changepoints per station
; ABS mean=0.99, st dev=0.70
; Mean = -0.00, st dev=1.21
; mean of diffs=-0.01, stdev=0.26

; Td - PHADPD
; 3.88 changepoints per station
; ABS mean=0.78, st dev=0.69
; Mean = -0.01, st dev=1.04
; mean of diffs=-0.01, stdev=0.31

;*****************************
; RESULTS 2015

; DPD - PHA
; 2.57 changepoints per station
; ABS mean=0.75, st dev=0.63
; Mean = -0.00, st dev=1.22
; mean of diffs=-0.00, stdev=0.28

; T - PHA 
; 1.36 changepoints per station
; ABS mean=0.75, st dev=0.57
; Mean = -0.10, st dev=0.94
; mean of diffs=0.00, stdev=0.18

; T - PHA+ID 
; 3.62 changepoints per station
; ABS mean=0.38, st dev=0.46
; Mean = -0.02, st dev=0.60
; mean of diffs=0.01, stdev=0.25

; q - ID 
; 3.84 changepoints per station
; ABS mean=0.26, st dev=0.29
; Mean = -0.01, st dev=0.40
; mean of diffs=0.00, stdev=0.14

; e - ID
; 3.84 changepoints per station
; ABS mean=0.41, st dev=0.46
; Mean = -0.01, st dev=0.61
; mean of diffs=-0.01, stdev=0.19

; RH - ID 
; 3.84 changepoints per station
; ABS mean=2.88, st dev=2.20
; Mean = 0.01, st dev=3.63
; mean of diffs=-0.08, stdev=0.99

; Td - PHADPD
; 3.70 changepoints per station
; ABS mean=0.78, st dev=0.68
; Mean = -0.02, st dev=1.04
; mean of diffs=0.00, stdev=0.26

; Tw - ID 
; 3.83 changepoints per station
; ABS mean=0.31, st dev=0.33
; Mean = -0.01, st dev=0.45
; mean of diffs=0.00, stdev=0.17

;**************
; RESULTS 2014
; DPD - PHA
; 2.52 changepoints per station
; ABS mean=0.98, st dev=0.69
; Mean = -0.01, st dev=1.21
; mean of diffs=0.00, stdev=0.26

; q - ID 
; 3.76 changepoints per station
; ABS mean=0.26, st dev=0.29
; Mean = -0.01, st dev=0.39
; mean of diffs=0.00, stdev=0.14

; RH - ID 
; 3.75 changepoints per station
; ABS mean=2.88, st dev=2.19
; Mean = 0.01, st dev=3.62
; mean of diffs=0.00, stdev=1.00

; e - ID
; 3.76 changepoints per station
; ABS mean=0.41, st dev=0.46
; Mean = -0.01, st dev=0.61
; mean of diffs=-0.00, stdev=0.19

; Tw - ID 
; 3.75 changepoints per station
; ABS mean=0.31, st dev=0.32
; Mean = -0.01, st dev=0.45
; mean of diffs=0.01, stdev=0.17

; T - PHA 
; 1.34 changepoints per station
; ABS mean=0.75, st dev=0.57
; Mean = -0.10, st dev=0.94
; mean of diffs=0.00, stdev=0.18

; T - PHA+ID 
; 3.58 changepoints per station
; ABS mean=0.38, st dev=0.46
; Mean = -0.02, st dev=0.60
; mean of diffs=0.01, stdev=0.25

; Td - PHADPD
; 3.62 changepoints per station
; ABS mean=0.77, st dev=0.65
; Mean = -0.01, st dev=1.01
; mean of diffs=0.00, stdev=0.26

; Td - PHA
; 2.16 changepoints per station
; ABS mean=1.00, st dev=0.72
; Mean = -0.06, st dev=1.23
; mean of diffs=-0.01, stdev=0.24

; q - PHA
; 2.16 changepoints per station
; ABS mean=0.46, st dev=0.38
; Mean = -0.02, st dev=0.59
; mean of diffs=-0.00, stdev=0.12

; RH - PHA
; 2.7 changepoints per station
; ABS mean=4.00, st dev=2.44
; Mean = 0.09, st dev=4.68
; mean of diffs=0.01, stdev=1.02


;-----------------------------------------------------
!Except=2

startee=' ' 	; fix as a station to restart
homogtype='DPD'	;'PHA' or 'ID' or 'DPD'
param='td'	;'dpd','rh','td','t','tw','e','q'
param2='Td'	;'DPD','RH','Td','T','Tw','e','q
nowmon='JAN'
nowyear='2016'
version='2.1.0.2015p'
plotonly='FALSE'	; TRUE or FALSE

CASE param OF

  'dpd': BEGIN
    inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAdpd_JAN2016.txt'
    inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landDPD.'+version+'_PHA_JAN2016.log' 
    outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.landDPD.'+version+'_adjspread_PHA_'+nowmon+nowyear+'.eps'
    outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_landDPD.'+version+'_PHA_'+nowmon+nowyear+'.txt'  
  END
  'rh': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHArh_JAN2016.txt'
      inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landRH.'+version+'_PHA_JAN2016.log' 
      outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.landRH.'+version+'_adjspread_PHA_'+nowmon+nowyear+'.eps'
      outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_landRH.'+version+'_PHA_'+nowmon+nowyear+'.txt'
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHArh_JAN2016.txt'
      inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landRH.'+version+'_IDPHA_JAN2016.log' 
      outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.landRH.'+version+'_adjspread_IDPHA_'+nowmon+nowyear+'.eps'
      outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_landRH.'+version+'_IDPHA_'+nowmon+nowyear+'.txt'
    ENDELSE
  END
  'td': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAtd_JAN2016.txt'
      inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landTd.'+version+'_PHA_JAN2016.log' 
      outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.landTd.'+version+'_adjspread_PHA_'+nowmon+nowyear+'.eps'
      outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_landTd.'+version+'_PHA_'+nowmon+nowyear+'.txt'
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHADPDtd_JAN2016.txt'
      inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landTd.'+version+'_PHADPD_JAN2016.log' 
      outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.landTd.'+version+'_adjspread_PHADPD_'+nowmon+nowyear+'.eps'
      outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_landTd.'+version+'_PHADPD_'+nowmon+nowyear+'.txt'
    ENDELSE
  END
  't': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAt_JAN2016.txt'
      inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landT.'+version+'_PHA_JAN2016.log' 
      outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.landT.'+version+'_adjspread_PHA_'+nowmon+nowyear+'.eps'
      outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_landT.'+version+'_PHA_'+nowmon+nowyear+'.txt'
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAt_JAN2016.txt'
      inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landT.'+version+'_IDPHAMG_JAN2016.log' 
      outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.landT.'+version+'_adjspread_IDPHAMG_'+nowmon+nowyear+'.eps'
      outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_landT.'+version+'_IDPHAMG_'+nowmon+nowyear+'.txt'
    ENDELSE
  END
  'tw': BEGIN
    inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAtw_JAN2016.txt'
    inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landTw.'+version+'_IDPHA_JAN2016.log' 
    outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.landTw.'+version+'_adjspread_IDPHA_'+nowmon+nowyear+'.eps'
    outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_landTw.'+version+'_IDPHA_'+nowmon+nowyear+'.txt'
  END
  'e': BEGIN
    inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAe_JAN2016.txt'
    inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.lande.'+version+'_IDPHA_JAN2016.log' 
    outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.lande.'+version+'_adjspread_IDPHA_'+nowmon+nowyear+'.eps'
    outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_lande.'+version+'_IDPHA_'+nowmon+nowyear+'.txt'
  END
  'q': BEGIN
    IF (homogtype EQ 'PHA') THEN BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_PHAq_JAN2016.txt'
      inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landq.'+version+'_PHA_JAN2016.log' 
      outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.landq.'+version+'_adjspread_PHA_'+nowmon+nowyear+'.eps'
      outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_landq.'+version+'_PHA_'+nowmon+nowyear+'.txt'
    ENDIF ELSE BEGIN
      inlist='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/goodforHadISDH.'+version+'_IDPHAq_JAN2016.txt'
      inlog='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/HadISDH.landq.'+version+'_IDPHA_JAN2016.log' 
      outplots='/data/local/hadkw/HADCRUH2/UPDATE2015/IMAGES/BUILD/HadISDH.landq.'+version+'_adjspread_IDPHA_'+nowmon+nowyear+'.eps'
      outadjs='/data/local/hadkw/HADCRUH2/UPDATE2015/LISTS_DOCS/Largest_Adjs_landq.'+version+'_IDPHA_'+nowmon+nowyear+'.txt'
    ENDELSE
  END

ENDCASE

;--------------------------------------------------------
; variables and arrays

mdi=-1e+30

CASE param OF 
  'dpd': nstations=3671							
  'rh': IF (homogtype EQ 'PHA') THEN nstations=3670 ELSE nstations=3657	
  'td': IF (homogtype EQ 'PHA') THEN nstations=3674 ELSE nstations=3666	
  't': IF (homogtype EQ 'PHA') THEN nstations=3675 ELSE nstations=3666	
  'tw': IF (homogtype EQ 'PHA') THEN nstations=3674 ELSE nstations=3663	
  'e': IF (homogtype EQ 'PHA') THEN nstations=3673 ELSE nstations=3663	
  'q': IF (homogtype EQ 'PHA') THEN nstations=3673 ELSE nstations=3663	
ENDCASE

styr=1973
edyr=2015
nyrs=(edyr+1)-styr
nmons=nyrs*12
int_mons=indgen(nmons)

stat_adjs=make_array(nmons,nstations,/float,value=mdi)
adj_locs=make_array(nmons,/int,value=0)
adj_mags_accum=100. ;grow this array on the fly
adj_mags_act=100.
adj_lats=999.
adj_wmos='999999'

;---------------------------------------------------------
; open station file

; read in and loop through all station info
openr,5,inlist
counter=0
WHILE NOT EOF(5) DO BEGIN
  wmo=''
  lat=0.
  lon=0.
  elv=0.
  cid=''
  namoo=''
  readf,5,wmo,lat,lon,elv,cid,namoo,format='(a11,f8.4,f10.4,f7.1,x,a2,x,a29,x)' 
  IF (startee NE ' ') AND (startee NE wmo) THEN continue    ;restart code 

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
    ENDWHILE
    close,4
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
;    stop,'Check all the adj values'
  endloop:
ENDWHILE
close,5

; plot histogram of actual adjustments
; plot histogram of accumulated adjustments
; plot timeseries of locations hits
  set_plot,'PS'
  device,filename=outplots,/color,/ENCAPSUL,xsize=20,ysize=26,/portrait,/helvetica,/bold
  !P.Font=0
  !P.Thick=4
  
  tvlct,200,0,0,1
  tvlct,150,150,150,2
  tvlct,000,0,200,3
;  !P.Position=[0.1,0.71,0.95,0.96]
  !P.Position=[0.15,0.58,0.95,0.94]

  CASE param OF
    'rh': binsize=0.5
    'e': binsize=0.05
    'q': binsize=0.05
    'tw': binsize=0.05
    ELSE: binsize=0.1
  ENDCASE
  
  minx=FLOOR(MIN(adj_mags_act))-binsize/2.
  maxx=CEIL(MAX(adj_mags_act))+binsize/2.
  IF (ABS(minx) GT maxx) THEN maxx=ABS(minx) ELSE minx=-(maxx)
  ;stop
  numbins=(maxx-minx)/binsize
  histacts=HISTOGRAM(adj_mags_act,min=minx,binsize=binsize,LOCATION=loc,nbins=numbins)
  xarr=(dindgen(numbins)*binsize)+minx
  
  keep_adj_vals=adj_mags_act
  adj_mags_act=adj_mags_act(SORT(adj_mags_act))
  nadjs=n_elements(adj_mags_act)
  
  abs_adj_mags_act=ABS(adj_mags_act)
  abs_adj_mags_act=abs_adj_mags_act(SORT(abs_adj_mags_act))
  print,'ABSOLUTE MEAN: ',MEAN(abs_adj_mags_act),' ABSOLUTE MEDIAN: ',abs_adj_mags_act(ROUND(nadjs/2))
  print,'ABSOLUTE ST DEV',STDDEV(abs_adj_mags_act)
  print,'ABSOLUTE 2SIGMA, 5th, 95th',STDDEV(abs_adj_mags_act)*2,abs_adj_mags_act(ROUND(nadjs*0.05)),abs_adj_mags_act(ROUND(nadjs*0.95))
  print,' '
  print,'MEAN: ',MEAN(adj_mags_act),' MEDIAN: ',adj_mags_act(ROUND(nadjs/2))
  print,'ST DEV',STDDEV(adj_mags_act)
  print,'2SIGMA, 5th, 95th',STDDEV(adj_mags_act)*2,adj_mags_act(ROUND(nadjs*0.05)),adj_mags_act(ROUND(nadjs*0.95))

  CASE param OF
    'rh': letters=['g)','h)']	
    'e': letters=['a)','b)']
    'q': letters=['a)','b)']
    't': IF (homogtype EQ 'PHA') THEN letters=['a)','b)'] ELSE letters=['c)','d)']
    'tw': letters=['a)','b)']
    'td': letters=['a)','b)']	
    'dpd': letters=['e)','f)']	
  ENDCASE

  CASE param OF
    'rh': IF (homogtype EQ 'PHA') THEN ymax=1000 ELSE ymax=1500	
    'e': ymax=1000
    'q': ymax=1500
    't': IF (homogtype EQ 'PHA') THEN ymax=600 ELSE ymax=1800
    'tw': ymax=1500
    'td': ymax=1000	
    'dpd': ymax=1000	
  ENDCASE
  
  CASE param OF
    'rh': unitees='%rh'
    'e': unitees='hPa'
    'q': unitees='g kg!E-1!N'
    ELSE: unitees='!Eo!NC'
  ENDCASE
  
  plot,xarr+(binsize/2.),histacts,min_value=-100,psym=10,yrange=[0,ymax],ystyle=1,xstyle=1,$
       title='actual adjustments',ytitle='frequency',xtitle='adjustment magnitude ('+unitees+')',charsize=1.5,/noerase
  XYOUTS,0.02,0.96,letters(0),/normal,color=0,charsize=1.8

; now do a gaussfit using only the tails to get actual gaussian, get the difference of the two
; 1 sigma uncertainty is 1st dev of the difference hist
  ;binsize=1.0	; 0.1 from earlier
;  hist = HISTOGRAM(monthly_values, BINSIZE=binsize,LOCATION=loc, MAX=max_val, MIN=min_val) 
;  hist=[0,0,0,histacts,0,0,0] 
    
;******************************************
; adjust for padding in histogram
;******************************************
  min_bin=MIN(loc)
  max_bin=MAX(loc)
  binns=loc
  ;[min_bin-(3.*binsize),min_bin-(2.*binsize),min_bin-binsize,loc,max_bin+binsize,max_bin+(2.*binsize),max_bin+(3.*binsize)]+(binsize/2.)

;******************************************
; fit gaussian to histogram
;******************************************
  newhist=histacts
;  newhist=intarr(n_elements(hist))
;  newhist(0:30)=hist(0:30)
;  newhist(n_elements(hist)-31:n_elements(hist)-1)=hist(n_elements(hist)-31:n_elements(hist)-1)
;  newhist=[hist(0:30),hist(n_elements(hist)-31:n_elements(hist)-1)]
;  binns=[binns(0:30),binns(n_elements(hist)-31:n_elements(hist)-1)]

; estimated a max value for the middle of the gaussian - this is optimised by trial and error
; to provide a reasonable fit
; It needs to be higher for direct PHA where the middle is completely missing - completely unrepresented
; It can be lower for IDPHA where there middle is somewhat represented
  CASE param OF
    'rh': IF (homogtype EQ 'PHA') THEN pseudomax=4000 ELSE pseudomax=3000	;good
    'e': pseudomax=2000
    'q': pseudomax=2000
    't': pseudomax=2000
    'tw': pseudomax=2000
    'td': pseudomax=3000	;good - 2000 or 3000 makes no difference
    'dpd': pseudomax=3000	
  ENDCASE
  
  newhist(ROUND(n_elements(histacts)/2))=pseudomax		;4000
;  stop
  yfit = GAUSSFIT(binns, newhist, coeff, NTERMS=3, ESTIMATES=[800,0.,5.],chisq=chi_sq)     ;max(hist)
  oplot,xarr+(binsize/2),yfit,color=2
  
  mergefit=histacts
  mergefit(WHERE(yfit GT histacts AND histacts NE 0))=yfit(WHERE(yfit GT histacts AND histacts NE 0))
  diffs=mergefit-histacts
  oplot,xarr+(binsize/2),mergefit,color=1,linestyle=2
  oplot,xarr+(binsize/2),diffs,color=3,linestyle=1

; get values again
  gots=WHERE(diffs NE 0,count)
  FOR i=0,count-1 DO BEGIN
    IF (i EQ 0) THEN BEGIN
      diffarr=fltarr(diffs(gots(i)))
      diffarr(*)=binns(gots(i))+(binsize/2.)
    ENDIF ELSE BEGIN
      garr=fltarr(diffs(gots(i)))
      garr(*)=binns(gots(i))+(binsize/2.)
      diffarr=[diffarr,garr]
    ENDELSE
  ENDFOR
  print,'MEAN OF GAUSS DIFFS',MEAN(diffarr)
  print,'ST DEV OF GAUSS DIFFS',STDDEV(diffarr)

  XYOUTS,1.,ymax*0.9,'MEAN: '+string(MEAN(diffarr),format='(f6.3)')+' '+unitees,/data,color=0,charsize=1.5
  XYOUTS,1.,ymax*0.8,'ST DEV: '+string(STDDEV(diffarr),format='(f6.3)')+' '+unitees,/data,color=0,charsize=1.5

;  !P.Position=[0.1,0.38,0.95,0.63]
;
;  minx=FLOOR(MIN(adj_mags_accum))
;  maxx=CEIL(MAX(adj_mags_accum))
;  numbins=(maxx-minx)/0.1
;  histaccum=HISTOGRAM(adj_mags_accum,min=minx,binsize=0.1,nbins=numbins)
;  xarr=(dindgen(numbins)*0.1)+minx
;  
;  plot,xarr,histaccum,min_value=-100,yrange=[0,1000],ystyle=1,xstyle=1,$
;       title='Accumulated Adjustments',ytitle='Frequency',xtitle='adjustment magnitude (%)',charsize=1,/noerase
  
;  !P.Position=[0.1,0.05,0.95,0.30]
  !P.Position=[0.15,0.08,0.95,0.44]

  
  xarr=indgen(nmons)
  ymax=MAX(adj_locs)+1
  ymin=0
  yrange=ymax-ymin
  
  plot,xarr,adj_locs,min_value=-100,yrange=[ymin,ymax],ystyle=1,xstyle=5,psym=-5,symsize=0.3,$
       title='changepoint dates',ytitle='frequency',charsize=1.5,/noerase
  PLOTS,[xarr(0),xarr(nmons-1)],[ymin,ymin],color=0
  PLOTS,[xarr(0),xarr(nmons-1)],[ymax,ymax],color=0
  FOR yy=1,nyrs-1 DO BEGIN
    mm=yy*12
    IF ((((yy+styr)/5.)-FIX((yy+styr)/5.)) GT 0.) THEN BEGIN
      PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.03*yrange)],color=0
      PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.03*yrange)],color=0
    ENDIF ELSE BEGIN
      PLOTS,[xarr(mm),xarr(mm)],[ymin,ymin+(0.05*yrange)],color=0
      PLOTS,[xarr(mm),xarr(mm)],[ymax,ymax-(0.05*yrange)],color=0    
      XYOUTS,xarr(mm),ymin-(0.08*yrange),strcompress(string(yy+styr),/remove_all),alignment=0.5,color=0,charsize=1.5
    ENDELSE
  ENDFOR
  XYOUTS,0.55,0.03,'years',/normal,color=0,alignment=0.5,charsize=1.5

  XYOUTS,0.02,0.46,letters(1),/normal,color=0,charsize=1.8

device,/close

orderadj=REVERSE(SORT(ABS(keep_adj_vals)))
print,keep_adj_vals(orderadj(0:99))
print,adj_wmos(orderadj(0:99))

print, 'AVERAGE No. ADJ PER ALL STATIONS: ',n_elements(keep_adj_vals)/float(nstations)

IF (plotonly EQ 'FALSE') THEN BEGIN
  openw,9,outadjs
  FOR loo=0,n_elements(keep_adj_vals)-1 DO BEGIN
    printf,9,adj_wmos(orderadj(loo)),keep_adj_vals(orderadj(loo)),format='(a11,x,f6.2)'
  ENDFOR
  close,9
ENDIF

print," PUT THIS VALUE IN CREATE_HOMOGNCDFALL_STUNC...",STDDEV(diffarr)
stop
end
