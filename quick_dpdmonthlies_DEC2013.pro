pro quick_dpdmonthlies_DEC2013

; Program to create monthly mean DPD by subtracting Td from T at monthly resolution
; Ideally DPD would be created directly from hourly values using:
;	create_monthseriesDEC2013.pro
; But for initial playing/testing just use quick calculation
; THIS RESULTS IN 391 MONTHS WHERE DPD is < 0
; THESE MONTHS ARE CONVERTED TO MDIs HERE
; I THINK THIS MAY HAPPEN WHEN T AND TD HOURS A NOT ALWAYS SIMULTANEOUS
; SUCH THAT A MONTHLY MEAN OF T MAY NOT INCLUDE IDENTICAL HOURS TO MONTHLY
; MEAN TD
; THIS SUPPORTS DPD BUILD FROM HOURLY DIRECT IN FUTURE

; input from /data/local/hadkw/HADCRUH2/UPDATE2012/MONTHLIES/ASCII/TABS and TDABS
; output to /data/local/hadkw/HADCRUH2/UPDATE2012/MONTHLIES/ASCII/DPDABS

;--------------------------------------------------------------
; files and directories
inlist='/data/local/hadkw/HADCRUH2/UPDATE2012/LISTS_DOCS/current_HadISD_stationinfo_AUG2011.txt'
indatadirT='/data/local/hadkw/HADCRUH2/UPDATE2012/MONTHLIES/ASCII/TABS/'
indatadirTd='/data/local/hadkw/HADCRUH2/UPDATE2012/MONTHLIES/ASCII/TDABS/'
outdatadir='/data/local/hadkw/HADCRUH2/UPDATE2012/MONTHLIES/ASCII/DPDABS/'
infilT='_TmonthQCabs.raw'
infilTd='_TdmonthQCabs.raw'
outfil='_DPDmonthQCabs.raw'

;--------------------------------------------------------------
; variables
mdi=-99.99

styr=1973
edyr=2012
nyrs=(edyr-styr)+1
nmons=nyrs*12

stationid=''
;--------------------------------------------------------------
; Main program

; open station list and begin to loop through

countboo=0
openr,5,inlist
WHILE NOT EOF(5) DO BEGIN
  wmoid=''
  wbanid=''
  namoo=''
  cid=''
  lat=0.
  lon=0.
  stationelv=0.
  readf,5,wmoid,wbanid,namoo,cid,lat,lon,stationelv,format='(a6,x,a5,2x,a29,x,a2,x,f7.3,x,f8.3,x,f6.1)'
  stationid=wmoid+'-'+wbanid	; New ISD will have different filenames
  infilid=wmoid+wbanid

; search for T and Td files
  filee1=FILE_SEARCH(indatadirT+stationid+infilT,count=count1)
  filee2=FILE_SEARCH(indatadirTd+stationid+infilTd,count=count2)
  If (count1 GT 0) AND (count2 GT 0) THEN BEGIN

; read in T and Td for that station
    Ttmparr=fltarr(12,nyrs)
    openr,7,filee1(0)
    lincount=0
    WHILE NOT EOF(7) DO BEGIN
      mush=' '
      tmp=intarr(12)
      readf,7,mush,tmp,format='(a16,12(i6,3x))'
      Ttmparr(*,lincount)=FLOAT(tmp(0:11)/100.)
      lincount=lincount+1
    ENDWHILE
    close,7

    Tdtmparr=fltarr(12,nyrs)
    openr,7,filee2(0)
    lincount=0
    WHILE NOT EOF(7) DO BEGIN
      mush=' '
      tmp=intarr(12)
      readf,7,mush,tmp,format='(a16,12(i6,3x))'
      Tdtmparr(*,lincount)=FLOAT(tmp(0:11)/100.)
      lincount=lincount+1
    ENDWHILE
    close,7

; subtract Td from T where both are present
    dpdarr=make_array(nmons,/float,value=mdi)
    Ttmparr=REFORM(Ttmparr,nmons)
    Tdtmparr=REFORM(Tdtmparr,nmons)
    For m=0,nmons-1 DO BEGIN
      IF (Ttmparr(m) GT mdi) AND (Tdtmparr(m) GT mdi) THEN BEGIN
        dpdarr(m)=Ttmparr(m)-Tdtmparr(m)
        IF (dpdarr(m) LT 0) THEN BEGIN
          print,stationid,' ',dpdarr(m),' BOO!'
	  countboo=countboo+1
          dpdarr(m)=mdi
        ENDIF
      ENDIF
    ENDFOR
    
; output to DPD file
    dpdarr=REFORM(ROUND(dpdarr*100.),12,nyrs)
    openw,7,outdatadir+stationid+outfil
    yr=styr
    FOR yy=0,nyrs-1 DO BEGIN
      printf,7,infilid,yr,dpdarr(*,yy),format='(a11,x,i4,12(i6,3x))'
      yr=yr+1
    ENDFOR
    close,7

  ENDIF ;ELSE print,stationid
  
ENDWHILE
close,5

print,countboo

end
