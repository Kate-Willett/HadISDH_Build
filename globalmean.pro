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

function globalmean,fd,ylat,mdi,mask=mask,nhemi=nhemi,shemi=shemi,cover=cover
;
; Computes a global mean from a field (or set of fields if fd is 3D),
; accounting for missing data.  A separate mask (of same dimension) can
; be supplied if required.  Single hemisphere means can also be returned.
; The number of boxes with data is returned in cover.
;
; Find dimensions
;
if keyword_set(mdi) then begin
  mdi=mdi
endif else message,'no mdi given'


fullsize=size(fd)
if (fullsize(0) lt 2) or (fullsize(0) gt 3) then $
  message,'fullfd must be 2D or 3D'
nx = fullsize(1)
ny = fullsize(2)
nz = 1
if fullsize(0) eq 3 then nz = fullsize(3)
;
; Use optional mask to remove points from fd
;
if keyword_set(mask) then begin
  masksize=size(mask)
  if (masksize(0) ne fullsize(0)) and (masksize(0) ne 2) then $
    message,'Mask is wrong size'
  if (masksize(1) ne nx) or (masksize(2) ne ny) then $
    message,'Mask is wrong size'
  if masksize(0) eq 2 then begin
    nzmask=1
  endif else begin
    if masksize(3) ne nz then message,'Mask is wrong size'
    nzmask=nz
  endelse
endif else begin
  nzmask=1
  mask=fltarr(nx,ny)
endelse
;
; Now make arrays
;
fd=reform(fd,nx,ny,nz)
mask=reform(mask,nx,ny,nzmask)
sumval=fltarr(nz)
sumarea=fltarr(nz)
sval=fltarr(nz)
sarea=fltarr(nz)
nval=fltarr(nz)
narea=fltarr(nz)
cover=fltarr(nz)
;
;-------------------------------------------
if nz eq nzmask then begin
for i = 0 , nx-1 do begin
  for j = 0 , ny-1 do begin
    temp_data=fd(i,j,*)				;NEW
    temp_mask=mask(i,j,*)			;NEW
    mask_cover=where(temp_mask EQ mdi,maskcount)	;NEW
    if (maskcount GT 0) THEN temp_data(mask_cover) = mdi	;NEW
    kl=where(temp_data NE mdi,nkeep)	;NEW    
;     kl=where(finite(fd(i,j,*)*mask(i,j,*)),nkeep)	;OLD
    if nkeep gt 0 then begin				
      sumval(kl) = sumval(kl) + fd(i,j,kl)*cos(ylat(j)*!dtor)
      sumarea(kl) = sumarea(kl) + cos(ylat(j)*!dtor)
      cover(kl) = cover(kl) + 1.
      if ylat(j) lt 0. then begin
        sval(kl) = sval(kl) + fd(i,j,kl)*cos(ylat(j)*!dtor)
        sarea(kl) = sarea(kl) + cos(ylat(j)*!dtor)
      endif else begin
        nval(kl) = nval(kl) + fd(i,j,kl)*cos(ylat(j)*!dtor)
        narea(kl) = narea(kl) + cos(ylat(j)*!dtor)
      endelse
;     endif	;OLD
    endif  	;NEW
  endfor
endfor
;-------------------------------------------
endif else begin
for i = 0 , nx-1 do begin
  for j = 0 , ny-1 do begin
;  if finite(mask(i,j,0)) then begin	;OLD
;   kl=where(finite(fd(i,j,*)),nkeep)	;OLD
    temp_data=fd(i,j,*)				;NEW
   if (mask(i,j,0) NE mdi) THEN BEGIN	;NEW
    kl=where(temp_data NE mdi,nkeep)
    if nkeep gt 0 then begin		
      sumval(kl) = sumval(kl) + fd(i,j,kl)*cos(ylat(j)*!dtor)
      sumarea(kl) = sumarea(kl) + cos(ylat(j)*!dtor)
      cover(kl) = cover(kl) + 1.
      if ylat(j) lt 0. then begin
        sval(kl) = sval(kl) + fd(i,j,kl)*cos(ylat(j)*!dtor)
        sarea(kl) = sarea(kl) + cos(ylat(j)*!dtor)
      endif else begin
        nval(kl) = nval(kl) + fd(i,j,kl)*cos(ylat(j)*!dtor)
        narea(kl) = narea(kl) + cos(ylat(j)*!dtor)
      endelse
    endif
   endif
  endfor
endfor
;-------------------------------------------
endelse
;
poot=size(sumval)
;print,poot(0)
if (poot(0) EQ 1) THEN BEGIN
  gots=WHERE(sumarea NE 0.0,count)
  if (count GT 0) THEN sumval(gots)=sumval(gots)/sumarea(gots)
  misses=WHERE(sumarea EQ 0.0,count)
  IF (count GT 0) THEN sumval(misses)=mdi
  if (count EQ n_elements(sumarea)) THEN sumval=-1e+30
;  if (sumval(0) NE 0) THEN sumval=sumval/sumarea
;  if (sumval(0) EQ 0) THEN sumval=-1e+30
endif else sumval=sumval/sumarea
;shemi=sval/sarea
;nhemi=nval/narea
if nz eq 1 then begin     ; convert to scalars
  sumval=sumval(0)
;  shemi=shemi(0)
;  nhemi=nhemi(0)
  fd=reform(fd)
  mask=reform(mask)
endif
return,sumval
;
end
