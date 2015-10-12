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


pro boxfill,data,lon,lat,colors=colors,levels=levels,nofill_color=nofill_color

; give gridbox centres

if not keyword_set(nofill_color) then nofill_color=255
;print,nofill_color
;*mdi=-1.e+30
lond=(lon(1)-lon(0))/2.
latd=abs(lat(1)-lat(0))/2.
for i=0,n_elements(lon)-1 do begin  ;changed from -2 
  for j=0,n_elements(lat)-1 do begin
; j was j=1,n_elements but this looked a bit odd - 0 seems to work better - last loop covers j=0 but with half boxes
; perhaps this is to cope with global data

	s=min(where(levels gt data(i,j)))-1
print,s,data(i,j)
;*	if (data(i,j) NE mdi) THEN BEGIN
	  if colors(s(0)) ne nofill_color then $
	  polyfill,[lon(i)-lond,lon(i)-lond,lon(i)+lond,lon(i)+lond,lon(i)-lond],$
		[lat(j)-latd,lat(j)+latd,lat(j)+latd,lat(j)-latd,lat(j)-latd],$
		color=colors(s)
;	print,lon(i)-lond,lon(i)-lond,lon(i)+lond,lon(i)+lond,lon(i)-lond,$
;		lat(j)-latd,lat(j)+latd,lat(j)+latd,lat(j)-latd,lat(j)-latd
;*	endif
  endfor
  j=0
  s=min(where(levels gt data(i,j)))-1
;*  if(data(i,j) NE mdi) THEN BEGIN
    if colors(s(0)) ne nofill_color then $
    polyfill,[lon(i)-lond,lon(i)-lond,lon(i)+lond,lon(i)+lond,lon(i)-lond],$
    [lat(j)-latd,lat(j),lat(j),lat(j)-latd,lat(j)-latd],$
    color=colors(s)
;*  endif
endfor
end
