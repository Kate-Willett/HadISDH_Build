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


function make_months_oddtimesJAN2015,hour_tmp,dates,clims,mdi,type=type,stdev_mm=stdev_mm,abs_mm=abs_mm,clims_mm=clims_mm

; NOTE APR 2014: fewer anoms than abs - so won't fail on abs but when later masked to anoms it does fail.

; a function to take hourly data and convert it to monthly mean abs, clims, stdevs and anomalies

; THIS PROGRAM CAN COPE WITH SMALL CHANGES IN STANDARD REPORTING HOURS
; e.g. Melbourne has daylight saving but records at the same local time throughout so reported hours in 
; GMT are different in summer and winter

; BE AWARE THAT WHEN ISD WAS READ IN (PETER THORNE) THE NEAREST OB TO THE HOUR WAS TAKEN AS THE OB FOR THAT HOUR
; THEREFORE THERE MAY BE SOME ODD HOURS REPORTED WHEN OBSERVERS GOT IN >30 MINUTES LATE OR SLIGHT INHOMOGENEITIES
; THESE SHOULD BE SMALL

; have some switches for sophisticated things 
; INPUTS:
; hour_tmp 	= this should be a one dimensional array containing complete years of hourly data (
; 	     	from midnight, Jan 1st to 11pm Dec 31st (missing data indicator provided)
; dates		= 2 element double array containing julian date for midnight Jan 1st of starting year
; 		  and julian date for 11pm Dec 31st of ending year
; clims		= 2 element integer array containing year to begin climatological reference period
;		  and year to end climatological reference period (inclusive so until Dec 31st of that year)
; mdi 		= this is the missing data indicator
; stdev_mm 	= a storage array for the pentad stdevs
; abs_mm 	= a storage array for the pentad absolutes
; clims_mm 	= a storage array for the pentad clims

; OUTPUTS:
; type		= 'bad' if a complete climatology cannot be calculated or 'good'
; anoms_mm 	- switch for simple/complex RETURNED
; stdev_mm 	- switch for simple/complex
; abs_mm 	- switch for simple/complex
; clims_mm 	- switch for simple/complex

; SIMPLE - this is a simple average of all hours within each pentad
; COMPLEX - this is where pentad hour clims are calculated and subtracted from each hour
;	  - pentad hour anoms are then averaged to give pentad mean anoms
; 	  - pentad hour clims are then averaged to give pentad clims
;	  - the absolute value (pentad clim + pentad anom) may not be the same as the simple absolute pentad

;--------------------------------------------------------
; KATE HAD MADE A DECISION - 9/8/11
; use COMPLEX
; this does differ very slightly to simple because it removes the diurnal cycle before averaging.
; this has a larger effect on a pentad when there are missing data
; this is because by not fully sampling the diurnal cycle there are biases towards the data that are present
; therefore I think it is better to remove to mean diurnal cycle from each hour first 
; there is still a diurnal cycle in the variance which is very clear in the data
; I DO NOT THINK THIS SHOULD BE REMOVED - IT IS AN IMPORTANT PART OF NATURAL VARIABILITY - AND PREVENTS GETTING BACK TO TRUE ABS

; JAN 2014 BUGFIX:
; make_months_oddtimesJAN2014.pro needs to be adapted so that stations only pass
; through if there are enough resulting months to create a climatology for each
; month. Currently some stations pass through because hours here and there enable
; an hour_month_clim to be calculated and thus a month_clim. Month_anoms or
; month_abs may not be able to be created for some years though when there are
; insufficient hour_month_anoms available.

; JAN 2015
; added windspeed and slp - no changes to this code made though


;--------------------------------------------------------

; OTHER PARAMETERS
; lleaps 	= this is an integer array of all the zeroed times for the leap days from start_date to end_date
; nyyrs 	= integer for number of years - calc from start_date and end_date
; nmms		= integer for number of months - calc from start_date and end_date
; nppts 	= integer for number of pentads - calc from start_date and end_date
; nddys 	= integer for number of days - calc from start_date and end_date
; nhhrs	= integer for number of hours - n_elements(hour_tmp)
; clim_points		= 2 element array containing the count for start year of clim and end year of clim in years
;	PRINT OUT A CHECK TO MAKE SURE THESE ARE CORRECT

; make hour month anomalies and average to give month anomalies - save the month climatologies to add back
; times going from 0.0 to 12782.958
; leap years are 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004
; these are JUL days: 2442837.5,2444298.5,2445759.5,2447220.5,2448681.5,2450142.5,2451603.5,2453064.5 
; these are zeroed JUl days: 1154.0, 2615.0, 4076.0, 5537.0, 6998.0, 8459.0, 9920.0, 11381.0 
; make hour month means - could average over all data in simple way BUT if there is data missing then month
;  will be skewed towards part of diurnal cycle that is present - using anomalies is a safer method
; make month hour clims
; subtract month hour clims
; average month hour anoms

;-------------------------------------------------
; CALCULATE NECESSARY PARAMETERS FROM INFO GIVEN
nhhrs=n_elements(hour_tmp)
nddys=CEIL(dates(1)-dates(0))
IF (nddys NE nhhrs/24) THEN stop,'DAYS DONT MATCH - LINE ',nddys,nhhrs/24.
CALDAT,dates(0),sm,sd,sy,sh
CALDAT,dates(1),em,ed,ey,eh
nyyrs=(ey+1)-sy
nmms=nyyrs*12
clim_points=[clims(0)-sy,clims(1)-sy]
climlength=(clims(1)-clims(0))+1
nddecs=3	; assumes we're always using a 30 year climatology
dec1=clim_points(0)+9
dec2=clim_points(0)+19

;print,'CHECK TIME STATS: ',nyyrs,nmms,nddys,nhhrs,sm,sd,sy,sh,em,ed,ey,eh

leapcount=0
FOR yloo=0,nyyrs-1 DO BEGIN
  yy=sy+yloo
  daydiff=CEIL(JULDAY(3,1,yy,0)-JULDAY(2,1,yy,0))
  IF (daydiff EQ 29) THEN BEGIN
    IF (leapcount EQ 0) THEN lleaps=JULDAY(2,29,yy,0)-dates(0) ELSE $
       			     lleaps=[lleaps,JULDAY(2,29,yy,0)-dates(0)]	; day count where 0 is start_date day
    leapcount=leapcount+1
  ENDIF
ENDFOR

;print,'CHECK NUMBER OF LEAPS: ',leapcount,lleaps

mondays=[31,28,31,30,31,30,31,31,30,31,30,31]

;-------------------------------------------------
; set up container arrays
 mm_hr_abs=make_array(24,nmms,/float,value=mdi)
 mm_hr_anoms=make_array(24,nmms,/float,value=mdi)
 mm_hr_clims=make_array(24,12,/float,value=mdi)
IF (keyword_set(abs_mm) EQ 0) THEN abs_mm=make_array(nmms,/float,value=mdi)
IF (keyword_set(anoms_mm) EQ 0) THEN anoms_mm=make_array(nmms,/float,value=mdi)
IF (keyword_set(clims_mm) EQ 0) THEN clims_mm=make_array(12,/float,value=mdi)
IF (keyword_set(stdev_mm) EQ 0) THEN stdev_mm=make_array(nmms,/float,value=mdi)

check_hours=indgen(24)

;-------------------------------------------------

; this bit makes month hour means for each year
; should take into account the 6 day pentad in leap years
hour_tmp=REFORM(hour_tmp,24,nddys)	; check this fills logically - IT DOES
;stop
day_count=0	; this counts all days
mm_count=0	; this loops months 0-11
FOR mm=0,nmms-1 DO BEGIN
  allvalsbin=0.
  mm_tots=fltarr(24)
  mm_divs=intarr(24)
  FOR dys=0,mondays(mm_count)-1 DO BEGIN
    start_leap1:
    gots=WHERE(hour_tmp(*,day_count) NE mdi,count)
    IF (count GT 0) THEN BEGIN
      mm_tots(gots)=mm_tots(gots)+hour_tmp(gots,day_count)
      mm_divs(gots)=mm_divs(gots)+1
      allvalsbin=[allvalsbin,REFORM(hour_tmp(gots,day_count),count)]	; place for storing all hourly values
    ENDIF
    day_count=day_count+1
;    print,day_count
    found_leap=WHERE(lleaps EQ day_count,countleap)
    IF (countleap EQ 1) THEN BEGIN
;      print,'LEAP!!!',day_count,lleaps
      goto,start_leap1
    ENDIF			     
  ENDFOR
  mm_count=mm_count+1
  IF (mm_count EQ 12) THEN mm_count=0
; CHECK THAT AT LEAST 15 DAYS PRESENT TO CALCULATE A MONTH HOUR
; THIS COULD HAVE BEEN 20 BUT THEN STATIONS WITH CHANGES TO GMT REPORTING WITHIN A MONTH i.e. Australia MAY 
; HAVE EVERY e.g. MARCH and SEPTEMBER REMOVED.
  bigs=WHERE(mm_divs GE 15,countdivs)	
  IF (countdivs GT 0) THEN BEGIN
    mm_hr_abs(bigs,mm)=mm_tots(bigs)/mm_divs(bigs)
;    stop,'CHECK YOUR PTS HERE!'
    gots=WHERE(mm_hr_abs(*,mm) NE mdi,count)
    hourgots1=WHERE(gots LE 7,count1)				; CHECK 4 HOURS PRESENT WITH ONE IN EACH THIRD OF DAY
    hourgots2=WHERE(gots GE 8 AND gots LE 15,count2)
    hourgots3=WHERE(gots GE 16 AND gots LE 23,count3)
    IF (count GE 4) AND ((count1 GT 0) AND (count2 GT 0) AND(count3 GT 0)) THEN BEGIN
      abs_mm(mm)=MEAN(mm_hr_abs(gots,mm)) 
      stdev_mm(mm)=STDDEV(allvalsbin(1:n_elements(allvalsbin)-2))	
;      print,'GOT MONTH',mm
    ENDIF

  ENDIF
ENDFOR

; this bit gets the month hour climatologies across the climatological period given
; it also averages these to create month climatologies
mm_hr_abs=REFORM(mm_hr_abs,24,12,nyyrs)
;???? FOR HOMOG SHOULD I calc clim over all years so as not to bias any timeseries with large missing chunks relative to other series
;KW 18/1/12 - well we did optimise station coverage by choosing 1976 -2005 so stick to that. Using complete series will also create
;biases for stations with skewed temporal data coverage 
FOR mm=0,11 DO BEGIN
  FOR hh=0,23 DO BEGIN
    submm=mm_hr_abs(hh,mm,clim_points(0):clim_points(1))	; EXTRACT FOR CLIMATOLOGY PERIOD
    gots=WHERE(submm NE mdi,count)
    dec_count=0
    decgots1=WHERE(gots LE dec1,countdec1)
    decgots2=WHERE(gots GT dec1 AND gots LE dec2,countdec2)
    decgots3=WHERE(gots GT dec2 ,countdec3)
; DO YOU WANT ONLY LIVE STATIONS OR IS THERE SOME USE FOR SHORT ONES?
; FOR CLIMATE TRENDS WE NEED LONG ONES
    IF (countdec1 GT 0) THEN dec_count=dec_count+1 
    IF (countdec2 GT 0) THEN dec_count=dec_count+1
    IF (countdec3 GT 0) THEN dec_count=dec_count+1	; ARE THERE AT LEAST 1 YEAR IN EACH DECADE AND 50% of YEARS IN CLIM PERIOD?
    IF (countdec1+countdec2+countdec3 GT FLOOR(climlength*0.5)) AND (dec_count GE nddecs) THEN mm_hr_clims(hh,mm)=MEAN(submm(gots))	; more than 15 years present
;    stop,'CHECK YOUR DECADE COUNTS HERE!'
  ENDFOR			
  gots=WHERE(mm_hr_clims(*,mm) NE mdi,count)
  hourgots1=WHERE(gots LE 7,count1)				; CHECK 4 HOURS PRESENT WITH ONE IN EACH THIRD OF DAY
  hourgots2=WHERE(gots GE 8 AND gots LE 15,count2)
  hourgots3=WHERE(gots GE 16 AND gots LE 23,count3)
  IF (count GE 4) AND ((count1 GT 0) AND (count2 GT 0) AND(count3 GT 0)) THEN clims_mm(mm)=MEAN(mm_hr_clims(gots,mm)) 	
ENDFOR
;stop,'CHECK CLIM HERE!'	

;stop
type='BAD'
gotclims=WHERE(clims_mm NE mdi,count)	; need to have majority of climatology 
IF (count EQ 12) THEN BEGIN
  type='GOOD'
  ; this bit creates month hour anomalies for all then averages these to create month mean anomalies
  day_count=0
  mm_count=0
  FOR mm=0,nmms-1 DO BEGIN
    mm_tots=fltarr(24)
    mm_divs=intarr(24)
    FOR dys=0,mondays(mm_count)-1 DO BEGIN
      start_leap2:
      gots=WHERE((hour_tmp(*,day_count) NE mdi) AND (mm_hr_clims(*,mm_count) NE mdi),count)
      IF (count GT 0) THEN BEGIN
        mm_tots(gots)=mm_tots(gots)+(hour_tmp(gots,day_count)-mm_hr_clims(gots,mm_count))
        mm_divs(gots)=mm_divs(gots)+1
      ENDIF
      day_count=day_count+1
;      print,day_count
      found_leap=WHERE(lleaps EQ day_count,countleap)
      IF (countleap EQ 1) THEN BEGIN
;        print,'LEAP!!!',day_count,lleaps
        goto,start_leap2
      ENDIF			     
    ENDFOR
    mm_count=mm_count+1
    IF (mm_count EQ 12) THEN mm_count=0
    bigs=WHERE(mm_divs GE 15,countdivs)	
; CHECK THAT AT LEAST 15 DAYS PRESENT TO CALCULATE A MONTH HOUR
; THIS COULD HAVE BEEN 20 BUT THEN STATIONS WITH CHANGES TO GMT REPORTING WITHIN A MONTH i.e. Australia MAY 
; HAVE EVERY e.g. MARCH and SEPTEMBER REMOVED.
    IF (countdivs GT 0) THEN BEGIN
      mm_hr_anoms(bigs,mm)=mm_tots(bigs)/mm_divs(bigs)
;      stop,'CHECK YOUR MMS HERE!'
      gots=WHERE(mm_hr_anoms(*,mm) NE mdi,count)
      hourgots1=WHERE(gots LE 7,count1)				; CHECK 4 HOURS PRESENT WITH ONE IN EACH THIRD OF DAY
      hourgots2=WHERE(gots GE 8 AND gots LE 15,count2)
      hourgots3=WHERE(gots GE 16 AND gots LE 23,count3)
      IF (count GE 4) AND ((count1 GT 0) AND (count2 GT 0) AND(count3 GT 0)) THEN anoms_mm(mm)=MEAN(mm_hr_anoms(gots,mm)) 
    ENDIF
  ENDFOR
;  stop,'CHECK MM ANOM COMPLEX HERE!'	;,plot,hour_tmp(*,day_count-5:day_count)	

 
mm_hr_abs=REFORM(mm_hr_abs,24,12*nyyrs)
mm_hr_abs=REFORM(mm_hr_abs,24,12*nyyrs)

anoms_mm=REFORM(anoms_mm,nmms)

ENDIF ;ELSE type='BAD' 

; Final check after all this that there are enough ABSOLUTE MONTHS TO CREATE A CLIMATOLOGY
IF (type NE 'BAD') THEN BEGIN
  abs_mm=REFORM(abs_mm,12,nyyrs)
  checkclims=intarr(12)
  FOR mm=0,11 DO BEGIN
    gots=WHERE(abs_mm(mm,clim_points(0):clim_points(1)) NE mdi,count)
    IF (count LT 15) THEN BEGIN
      type='BAD'
;      stop,'Found a dodgy month in make_months'
      break
    ENDIF
  ENDFOR
  abs_mm=REFORM(abs_mm,nmms)
ENDIF
RETURN, anoms_mm
end

