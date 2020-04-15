# PYTHON 3 code to run from CreateMonthSeriesfromHadISD.py 
# Not currently used!!!

# This used to be part of the IDL code to identify time periods of:
# 	- changes to reporting frequency (hourly, 3 hourly 6 hourly etc
# 	- changes to reporting resolution (0., 0.1, 0.5)
# 	- changes to source input station ID


def GetStationHistoryDetails(OUTFILE,full_times,obssource,stjul,edactjul,fulltemp_arr,fulldewp_arr,MDI):


#station hist arrays
tmp = np.repeat(' ',1000) 
tmpi = np.repeat(0,1000) 
histarr = {'source':tmp,                # 0 to 3
           'wmoid':tmp,	                # 999999
           'perst':tmp,              # yyyymmdd
           'pered':tmp,		# yyyymmdd
           'ltdeg':tmpi,		# -999
           'ltmin':tmpi,		# 99
           'ltsec':tmpi,		# 99
           'lndeg':tmpi,		# -999
           'lnmin':tmpi,		# 99
           'lnsec':tmpi,		# 99
           'chdist':tmp, 		# 999
           'chdisttp':tmp,		# MI ,YD , 
           'chdir':tmp,		#   N,
           'stelevft':tmp,		# 99999
           'itelevft':tmp,		# 9999 HM, TP
           'obtimsHUM':tmp,		# 06
           'obtimsTMP':tmp,		# HR this means all obs taken every 6 hours
           'itlist':tmp}		# 99999 99999 99999

    ntims = len(full_times)
TheStYr = dt.date.fromordinal(dates[0]).year
TheEdYr = dt.date.fromordinal(dates[1]).year

nyrs = (edyear + 1) - styear # time points in years
actyears = np.arange(styear, (edyear + 1)) # array of integer years

halfyrtots = np.repeat((181,184),nyrs) # an array of nyrs 181s followed by nyrs 184s
#tots = {structots,hd:[181,184]}
#alltots=REPLICATE(tots,nyrs)
# Identify the leap years
founds = np.where( ((actyears/4.) - np.floor(actyears/4.) == 0.0) & ( ((actyears/100.) - np.floor(actyears/100.) != 0.0) | ((actyears/400.) - np.floor(actyears/400.) == 0.0)))
# CHange those years to day count half years of 182
halfyrtots[founds] = 180
# Now reshape to get 181,184,181,184 etc,...
halfyrtots = np.reshape(np.transpose(np.reshape(halfyrtots,(2,nyrs))),len(halfyrtots))
#halfyrtots=REFORM(alltots.hd,2,nyrs)
#halfyrtots(0,founds)=182
#halfyrtots=REFORM(halfyrtots,nyrs*2)
leapsids = np.arange(0,nyrs)
leapsids[founds] = 1  #1s identify leap years
    
# Populate the inhomogeneity analysis historys arrays (frequency, resolution, input station source)
    
    obsfreq_tmp = np.repeat(0, ntims) 	# to look at reporting frequency
    obsfreq_hum = np.repeat(0, ntims) 
    obsres_tmp = np.repeat(MDI, ntims) 	# to look at recording resolution
    obsres_hum = np.repeat(MDI, ntims) 
  
    obsfreq_tmp[np.where(fulltemp_arr > MDI)] = 1 # only where actualy temperatures exist
    obsfreq_hum[np.where(fulldewp_arr > MDI)] = 1 # only where actualy dewpoint temperatures exist
    
    obsres_tmp[np.where(fulltemp_arr > MDI)] = abs(fulltemp_arr[np.where(fulltemp_arr > MDI)]) - np.floor(abs(fulltemp_arr[np.where(fulltemp_arr > MDI)])) 
    obsres_hum[np.where(fulldewp_arr > MDI)] = abs(fulldewp_arr[np.where(fulldewp_arr > MDI)]) - np.floor(abs(fulldewp_arr[np.where(fulldewp_arr > MDI)])) 

# go through hours and look for changes in input stations, reporting frequency and recording resolution
# time consuming - could use some UNIQUE command?

  changehis=stjul
  changetyp=0	       #0=none,1=input,2=freq,3=res
  changeinput=strmid(obssource(0),0,6) #starting source station
  obsfreqT='00'
  obsfreqH='00'
  obsresT='BLANK'
  obsresH='BLANK '
  countch=0
  lasttime=0.  #1973,Jan 1st zerod
  histarr={histee,source:tmp,$         # 0 to 3
		wmoid:tmp,$	       # 999999
	       perst:tmp,$	       # yyyymmdd
	       pered:tmp,$	       # yyyymmdd
	       ltdeg:tmpi,$	       # -999
	       ltmin:tmpi,$	       # 99
	       ltsec:tmpi,$	       # 99
	       lndeg:tmpi,$	       # -999
	       lnmin:tmpi,$	       # 99
	       lnsec:tmpi,$	       # 99
		chdist:tmp,$	       # 999
	       chdisttp:tmp,$	       # MI ,YD , 
	       chdir:tmp,$	       #   N,
	       stelevft:tmp,$	       # 99999
	       itelevft:tmp,$	       # 9999 HM, TP
	       obtimsHUM:tmp,$         # 06
	       obtimsTMP:tmp,$         # HR this means all obs taken every 6 hours
	       itlist:tmp}	       # 99999 99999 99999

# find changes in source data by year
# bundle up into seasons (well 182 day periods) - may still be too sensitive
  uniqinputs=UNIQ(obssource(WHERE(obssource NE '999999')))     # finds ENDS of sustained periods
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
    counthfyrs=0    #counter to loop through halfyrtots
    FOR dd=0,ndays-1 DO BEGIN
      gots=WHERE(obssource(*,dd) NE '999999',count)
      IF (count GT 0) THEN totsource=[totsource,strmid(obssource(gots,dd),0,6)]
      yrcount=yrcount+1
      IF (yrcount EQ halfyrtots(counthfyrs)) THEN BEGIN
	IF (n_elements(totsource) GT 400) THEN BEGIN   # most days present (4 hours times 180 days = 720 obs)
	  totsource=totsource(1:n_elements(totsource)-1)
	  monhist=HISTOGRAM(FIX(totsource,type=3),binsize=1,min=MIN(FIX(totsource,type=3)))
	  binsies=lindgen(n_elements(monhist))+MIN(FIX(totsource,type=3))
	  mainsource=binsies(WHERE(monhist EQ MAX(monhist)))
	  sourcepct=MAX(monhist)/TOTAL(monhist)
	  IF (beginit EQ 0) THEN BEGIN
	    beginit=1  # 0 implies not enough data.
	   oldsource=mainsource
	   oldpct=sourcepct
	   yrcount=0
	   counthfyrs=counthfyrs+1
	    totsource='999999'
	    datestamp=full_times(0,dd+1)+stjul #date from beginning of year
	    continue
	  ENDIF ELSE IF (mainsource NE oldsource) OR ((sourcepct NE oldpct) AND ((sourcepct EQ 1.0) OR (oldpct EQ 1.0))) THEN BEGIN
	   print,'FOUND SOURCE CHANGE'
	    changehis=[changehis,datestamp]
	    changetyp=[changetyp,1]
	    changeinput=[changeinput,string(mainsource,format='(i06)')]        # the new ID after change
	    obsfreqT=[obsfreqT,'00']	       # new frequency after change
	    obsfreqH=[obsfreqH,'00']
	    obsresT=[obsresT,'BLANK']
	    obsresH=[obsresH,'BLANK ']
	    countch=countch+1
	    oldsource=mainsource
	   oldpct=sourcepct
	  ENDIF 
	ENDIF 
	IF (dd LT ndays-1) THEN datestamp=full_times(0,dd+1)+stjul     #date from beginning of year
	yrcount=0
       counthfyrs=counthfyrs+1
	totsource='999999'	
      ENDIF
    ENDFOR
ENDIF  
  
# find changes in reporting frequencies 
# bundle up into months (well 182 day periods) - may still be too sensitive
# IF LESS THAN 4 obs per day (4 hourly) then this month wouldn't make it so ignore.  
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
  counthfyrs=0    #counter to loop through halfyrtots
  FOR dd=0,ndays-1 DO BEGIN
    totfreqT(yrcount)=TOTAL(obsfreq_tmp(*,dd))
    totfreqH(yrcount)=TOTAL(obsfreq_hum(*,dd))
    yrcount=yrcount+1
#    print,yrcount,halfyrtots(counthfyrs),counthfyrs
    IF (yrcount EQ halfyrtots(counthfyrs)) THEN BEGIN
      IF (TOTAL(totfreqT) GT 0) AND (TOTAL(totfreqH) GT 0) THEN BEGIN
	monhist=HISTOGRAM(totfreqT(WHERE(totfreqT NE 0)),binsize=1,nbins=25,min=0)
	freqT=binsies(WHERE(monhist EQ MAX(monhist)))
	monhist=HISTOGRAM(totfreqH(WHERE(totfreqH NE 0)),binsize=1,nbins=25,min=0)
	freqH=binsies(WHERE(monhist EQ MAX(monhist)))
#	 print,freqH,freqT
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
#	 print,counthfyrs,' ',freqH,oldfreqH, freqT,oldfreqT
	IF (beginit EQ 0) THEN BEGIN
	  beginit=1    # 0 implies not enough data.
	 oldfreqT=freqT
	 oldfreqH=freqH
	 yrcount=0
	 counthfyrs=counthfyrs+1
	  totfreqT=intarr(halfyrtots(counthfyrs))
	  totfreqH=intarr(halfyrtots(counthfyrs))
	  datestamp=full_times(0,dd+1)+stjul   #date from beginning of year
	 continue
	ENDIF ELSE IF (TOTAL(totfreqH) GT 400) AND ((freqT NE oldfreqT) OR (freqH NE oldfreqH)) THEN BEGIN # enough data
	 print,'FOUND FREQ CHANGE'
#	 stop
	  changehis=[changehis,datestamp]
	  changetyp=[changetyp,2]
	  changeinput=[changeinput,'999999']   # the new ID after change
	  obsfreqT=[obsfreqT,freqT]	       # new frequency after change
	  obsfreqH=[obsfreqH,freqH]
	  obsresT=[obsresT,'BLANK']
	  obsresH=[obsresH,'BLANK ']
	  countch=countch+1
	  oldfreqT=freqT
	 oldfreqH=freqH
	ENDIF 
      ENDIF
      IF (dd LT ndays-1) THEN BEGIN
	datestamp=full_times(0,dd+1)+stjul     #date from beginning of year
	yrcount=0
	counthfyrs=counthfyrs+1
	totfreqT=intarr(halfyrtots(counthfyrs))
	totfreqH=intarr(halfyrtots(counthfyrs))
      ENDIF
    ENDIF
  ENDFOR

# find changes in reporting resolutions WHOLE, WH&DM, HALF, DECIM
# bundle up into months (well 182 day periods) - may still be too sensitive
# IF LESS THAN 4 obs per day (4 hourly) then this month wouldn't make it so ignore.  
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
  counthfyrs=0    #counter to loop through halfyrtots
  FOR dd=0,ndays-1 DO BEGIN
    gots=WHERE(obsres_tmp(*,dd) NE MDI,count)
    IF (count GT 0) THEN totresT=[totresT,obsres_tmp(gots,dd)]
    gots=WHERE(obsres_hum(*,dd) NE MDI,count)
    IF (count GT 0) THEN totresH=[totresH,obsres_hum(gots,dd)]
    yrcount=yrcount+1
    IF (yrcount EQ halfyrtots(counthfyrs)) THEN BEGIN
      IF (n_elements(totresH) GT 400) AND (n_elements(totresT) GT 400) THEN BEGIN      # check there are some data
       monhistT=HISTOGRAM(totresT,binsize=0.1,nbins=10,min=0.)
	findresT=binsies(REVERSE(SORT(monhistT)))
       monhistT=monhistT(REVERSE(SORT(monhistT)))
	monhistH=HISTOGRAM(totresH,binsize=0.1,nbins=10,min=0.)
	findresH=binsies(REVERSE(SORT(monhistH)))
       monhistH=monhistH(REVERSE(SORT(monhistH)))
	resT='BLANK'
       resH='BLANK '
       CASE 1 OF
	 findresT(0) EQ 0.0 AND (monhistT(0)/TOTAL(monhistT) GE 0.99): resT='WHOLE'    # 90% of obs
	 findresT(0) EQ 0.0 AND (monhistT(0)/TOTAL(monhistT) GE 0.6): resT='WH&DM'     # 60% of obs
	 TOTAL(findresT(0:1)) EQ 0.5 AND (TOTAL(monhistT(0:1)) GT TOTAL(monhistT(2:9))): resT=' HALF'
	 ELSE: resT='DECIM'
       ENDCASE
       CASE 1 OF
	 findresH(0) EQ 0.0 AND (monhistH(0)/TOTAL(monhistH) GE 0.99): resH='WHOLE '
	 findresH(0) EQ 0.0 AND (monhistH(0)/TOTAL(monhistH) GE 0.6): resH='WH&DM '    # 60% of obs
	 TOTAL(findresH(0:1)) EQ 0.5 AND (TOTAL(monhistH(0:1)) GT TOTAL(monhistH(2:9))): resH=' HALF '         
	 ELSE: resH='DECIM '
       ENDCASE
#      print,resT,findresT(0),findresT(1),monhistT(0),monhistT(1),TOTAL(monhistT)
#      print,resH,findresH(0),findresH(1),monhistT(0),monhistH(1),TOTAL(monhistH)
	IF (beginit EQ 0) THEN BEGIN
	  beginit=1    # 0 implies not enough data.
	 oldresT=resT  # should be WHOLE, DECIM or HALF
	 oldresH=resH
	 yrcount=0
	 counthfyrs=counthfyrs+1
	  totresT=0.
	  totresH=0.
	  datestamp=full_times(0,dd+1)+stjul   #date from beginning of year
	  continue
	ENDIF ELSE IF (resT NE oldresT) OR (resH NE oldresH) THEN BEGIN
	 print,'FOUND RES CHANGE'
	  changehis=[changehis,datestamp]
	  changetyp=[changetyp,3]
	  changeinput=[changeinput,'999999']   # the new ID after change
	  obsfreqT=[obsfreqT,'00']
	  obsfreqH=[obsfreqH,'00']
	  obsresT=[obsresT,resT]	       # new resolution after change
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

# compile and sort changes feeding though all info   
# WILL ONLY PRINT FROM histarr(1) onwards
  histarr.source=make_array(1000,/string,value='3')

  hissort=SORT(changehis)
  changehis=changehis(hissort) #need to be converted to year, month, day
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
  
#  changetyp=changetyp(hissort) # info not yet incorporated
  histarr.wmoid(0:countch)=changeinput(hissort)        
  histarr.obtimsTMP(0:countch)=obsfreqT(hissort)
  histarr.obtimsHUM(0:countch)=obsfreqH(hissort)
  histarr.itlist(0:countch)=obsresH(hissort)+obsresT(hissort)  # put in itlist for now

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
	# this is the same time as the one before, and could be the same as the one before that actually
	IF (histarr.wmoid(cc-1) NE histarr.wmoid(cc)) THEN histarr.wmoid(cc-1)=histarr.wmoid(cc)
	IF (histarr.obtimsTMP(cc-1) NE histarr.obtimsTMP(cc)) THEN histarr.obtimsTMP(cc-1)=histarr.obtimsTMP(cc)
	IF (histarr.obtimsHUM(cc-1) NE histarr.obtimsHUM(cc)) THEN histarr.obtimsHUM(cc-1)=histarr.obtimsHUM(cc)
	IF (histarr.itlist(cc-1) NE histarr.itlist(cc) ) THEN histarr.itlist(cc-1)=histarr.itlist(cc)
	histarr.perst(cc)=histarr.perst(cc-1)
       
       histarr.source(cc)='X'  #stops line being printed
	IF (cc GE 2) THEN BEGIN
	 IF (histarr.pered(cc) EQ histarr.pered(cc-2)) THEN BEGIN
	    print,'TRIPLE!!!',histarr.pered(cc)
	# this is the same time as the one before, and the same as the one before that actually
	    IF (histarr.wmoid(cc-2) NE histarr.wmoid(cc)) THEN histarr.wmoid(cc-2)=histarr.wmoid(cc)
	    IF (histarr.obtimsTMP(cc-2) NE histarr.obtimsTMP(cc)) THEN histarr.obtimsTMP(cc-2)=histarr.obtimsTMP(cc)
	    IF (histarr.obtimsHUM(cc-2) NE histarr.obtimsHUM(cc)) THEN histarr.obtimsHUM(cc-2)=histarr.obtimsHUM(cc)
	    IF (histarr.itlist(cc-2) NE histarr.itlist(cc)) THEN histarr.itlist(cc-2)=histarr.itlist(cc)
	    histarr.perst(cc)=histarr.perst(cc-2)
       
	   histarr.source(cc)='X'      #stops line being printed
	  ENDIF
       ENDIF
      ENDIF
    ENDFOR
  ENDIF
   
#save to files----------------------------------------------------------- 
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





    return
