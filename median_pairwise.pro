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


;#==============================================================================
;# RCS Header:
;#   File         [$Source: /home/hc0100/hadobs/Sondes.projects/automatic.arch/analysis_tools/median_pairwise.pro,v $]
;#   Revision     [$Revision: 1.8 $]     Named [$Name: head#main $]
;#   Last checkin [$Date: 2006/04/03 10:03:40 $]
;#   Author       [$Author: hadmc $]
;#==============================================================================

FUNCTION median_pairwise, y, mdi, se, lc, uc  

;
; NAME: median_pairwise
;
; CODE DESCRIPTION: PV-Wave
;
; TYPE: 
;
; PURPOSE:
;    To calculate the median of pairwise slopes of a series, accounting for 
;    missing data as well as the standard error of the fit.
;    Returns mdi if less than 3 pairs of non-missing points in the series. 
;   
; INTERFACES:
;
;    Arguments (required):
;
;       y - an array containing the time series.
;
;       mdi - missing data indicator
;
;    Outputs:
;
;    	bb - the median of pairwise slopes
;
;    	se - the standard error of the slope
;
;    Keywords (optional): none
;
;    Input files: none
;
;    Output files: none
;
; FUNCTIONAL DESCRIPTION:
;
;    The function calculates the diagnostics as follows:
;
;    1.  Calculate the median of pairwise slopes.
;
;    2.  Calculate the intercept of the slope.
;
;    3.  Calculate the standard error.
;
; CALLS:
; 
;
; CALLED BY:
;   
;
; EXCEPTION HANDLING:
;
;
; RESTRICTIONS:
;
;
; CURRENT CODE OWNER: Mark McCarthy 
;
; HISTORY:
;
;   Version         Date       Comment
;   -------         ----         -------
;   0.0             04/08/05  First version
;   0.1     	    11/08/05  Calculation of standard error added.
;   0.2             09/11/05  NINT changed to LONG at lines 109/10 (Holly)

;-----------------------------------------------

;WAVE: ON_ERROR, 1   ; Ensures that we return to the high level code on encountering a MESSAGE statement.

;Calculate the pairwise slopes
i=n_elements(y)
x=indgen(i)  
b=fltarr((LONG(i)*(LONG(i)-1))/2)
c=-1
c = long(c) 
FOR j=i-1,0,-1 DO BEGIN    
  FOR k=j-1,0,-1 DO BEGIN    
    IF y(j) NE mdi AND y(k) NE mdi THEN BEGIN
      c=c+1      
      b(c)=(y(j)-y(k))/(x(j)-x(k))    
    ENDIF
  ENDFOR 
ENDFOR  

IF c GE 3 THEN BEGIN

  b=b(0:c)
  
  ; Calculate the median of the pairwise slopes
  bb=MEDIAN(b)
  
  ; Calculate the 95% confidence range.
  s = SORT(b)
  b = b(s)
  i = WHERE(y NE mdi,n)
  dof = LONG((LONG(n)*(LONG(n)-1))/2.)
  w = LONG(SQRT(LONG(n)*(LONG(n)-1)*((2*LONG(n))+5)/18.))
;  stop
  rank_uc = ((dof+1.96*w)/2.)+1
;  stop
  rank_lc = ((dof-1.96*w)/2.)-1
  IF LONG(rank_uc) GE N_ELEMENTS(b) THEN rank_uc=N_ELEMENTS(b)-1
  IF LONG(rank_uc) LT 0 THEN rank_uc=0
  IF LONG(rank_lc) LT 0 THEN rank_lc=0
  uc = b(LONG(rank_uc))
  lc = b(LONG(rank_lc))  
  
  vals = where(y ne mdi, nvals)
  res = fltarr(nvals)
  
  ; Calculate the residuals 
  for i = 0, nvals-1 do begin
    res(i) = y(vals(i)) - (bb*vals(i))
  endfor
  
  ; Calculate the intercept from the average of the residuals
  intercept = MEAN(res)
;  print,intercept
  
;  sqr = fltarr(i)
  sqr = fltarr(nvals)	; Kate May 2011
  
  for i = 0, nvals-1 do begin
    
    ; Calculate the expected value from the slope and the intercept    
    predicted_y = intercept + (bb*vals(i))
    
    ; Calculate the squares of the residual errors
    sqr(i) = (predicted_y - y(vals(i)))^2
  
  endfor
;  stop
  ; Calculate the standard error from the sum of the squares.
  se = ((TOTAL(sqr))/(FLOAT(nvals-2)))^0.5
;  print,se
; THIS GIVES A HUGE ERROR - NEED SOMETHING THAT TAKES INTO ACCOUNT AUTOCORRELATION
  
ENDIF ELSE BEGIN
  
  bb=mdi
  se=mdi

ENDELSE

RETURN,bb

END

