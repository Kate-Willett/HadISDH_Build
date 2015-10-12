PRO plot_HadCRUH2uncertainty_FEB2013

styr=1973
edyr=2014
nyrs=(edyr+1)-styr
nmons=nyrs*12

chosendate=((1995-styr)*12)+5	; should be June 1980
chosenclim=5	; JUNE

titleyear='1995'
titlemonth='July'

latlg=5.
lonlg=5.
stlt=-90+(latlg/2.)
stln=-180+(lonlg/2.)
nlats=180/latlg
nlons=360/lonlg
nbox=LONG(nlats*nlons)

lats=(findgen(nlats)*latlg)+stlt
lons=(findgen(nlons)*lonlg)+stln


indir='/data/local/hadkw/HADCRUH2/UPDATE2014/STATISTICS/GRIDS/'
;infile='HadISDH.landT.2.0.1.2014p_FLATgridIDPHA5by5_JAN2015_cf'
infile='HadISDH.landq.2.0.1.2014p_FLATgridIDPHA5by5_JAN2015_cf'
;outfil='/data/local/hadkw/HADCRUH2/UPDATE2014/IMAGES/OTHER/HadISDH.landT.2.0.1.2014p_uncertainty'+titlemonth+titleyear+'_MAY2015.eps'
outfil='/data/local/hadkw/HADCRUH2/UPDATE2014/IMAGES/OTHER/HadISDH.landq.2.0.1.2014p_uncertainty'+titlemonth+titleyear+'_MAY2015.eps'


mdi=-1e+30

;--------------------------------------

filee=NCDF_OPEN(indir+infile+'.nc')
timvarid=NCDF_VARID(filee,'time')
longs_varid=NCDF_VARID(filee,'longitude')
lats_varid=NCDF_VARID(filee,'latitude')
;qstid=NCDF_VARID(filee,'t_stationerr') 	; may become uncertainty fields
;qspid=NCDF_VARID(filee,'t_samplingerr') 	; may become uncertainty fields
;qcbid=NCDF_VARID(filee,'t_combinederr') 	; may become uncertainty fields
;qclim=NCDF_VARID(filee,'t_clims') 	; may become uncertainty fields
qstid=NCDF_VARID(filee,'q_stationerr') 	; may become uncertainty fields
qspid=NCDF_VARID(filee,'q_samplingerr') 	; may become uncertainty fields
qcbid=NCDF_VARID(filee,'q_combinederr') 	; may become uncertainty fields
qclim=NCDF_VARID(filee,'q_clims') 	; may become uncertainty fields
NCDF_VARGET,filee,timvarid,times
NCDF_VARGET,filee,qstid,q_sterr
NCDF_VARGET,filee,qspid,q_sperr
NCDF_VARGET,filee,qcbid,q_cberr
NCDF_VARGET,filee,qclim,q_clim
NCDF_CLOSE,filee

timeunits='month'	
 
sterrfield=q_sterr(*,*,chosendate)
sperrfield=q_sperr(*,*,chosendate)
combfield=q_cberr(*,*,chosendate)

combpct=make_array(nlons,nlats,/float,value=mdi)
clims=REFORM(q_clim(*,*,chosenclim),nlons,nlats)
gots=WHERE(combfield NE mdi AND clims NE mdi,count)
combpct(gots)=(combfield(gots)/abs(clims(gots)))*100.
 
 
titlees=['Station Uncertainty '+titlemonth+' '+titleyear,'Sampling Uncertainty '+titlemonth+' '+titleyear,'Combined Uncertainty '+titlemonth+' '+titleyear]
   


kcolsarrST=[255,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]	; 14 colours + black to ensure no botching
levsarrST=[-2e+30,0.0,0.01,0.02,0.03,0.04,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.8,10]

;kcolsarrT=[255,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]	; 14 colours + black to ensure no botching
;levsarrT=[-2e+30,0.000,0.005,0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,1.,10]

;kcolsarrPCT=[255,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]	; 14 colours + black to ensure no botching
;levsarrPCT=[-2e+30,0.0,0.1,0.2,0.4,0.6,0.8,1.0,1.5,2.0,3.0,4.0,5.0,7.5,10.0,12.5,15.0,17.5,20.,200]

kcolsarrT=[255,1,4,7,9,11,13,15,18]	; 14 colours + black to ensure no botching
;levsarrT=[-2e+30,0.000,0.01,0.1,0.3,0.5,0.7,1.,1.1,10]
levsarrT=[-2e+30,0.000,0.1,0.25,0.5,0.75,1.,1.25,1.5,10]

kcolsarrPCT=[255,1,4,7,9,11,13,15,18]	; 14 colours + black to ensure no botching
levsarrPCT=[-2e+30,0.0,0.05,1.0,2.5,5.0,10.0,15.0,20.,200]


; colour settings - Uni ORegon blue to red
tvlct,0,0,0,0
tvlct,200,200,200,100

ncols=n_elements(kcolsarrST)
colsarrST=kcolsarrST(1:ncols-1)
nlevs=n_elements(levsarrST)-1
labsarrST=strarr(nlevs)
labsarrST(0)=''
labsarrST((nlevs-1))=''
labsarrST(1:nlevs-2)=string(levsarrST(2:nlevs-1),format='(f5.2)')

ncols=n_elements(kcolsarrT)
colsarrT=kcolsarrT(1:ncols-1)
nlevs=n_elements(levsarrT)-1
labsarrT=strarr(nlevs)
labsarrT(0)=''
labsarrT((nlevs-1))=''
labsarrT(1:nlevs-2)=string(levsarrT(2:nlevs-1),format='(f5.2)')

ncols=n_elements(kcolsarrPCT)
colsarrPCT=kcolsarrPCT(1:ncols-1)
nlevs=n_elements(levsarrPCT)-1
labsarrPCT=strarr(nlevs)
labsarrPCT(0)=''
labsarrPCT((nlevs-1))=''
labsarrPCT(1:nlevs-2)=string(levsarrPCT(2:nlevs-1),format='(f5.1)')
;------------------------------------------------------------------------------------
xpos1=0.04
xpos2=0.84
ypos1=[0.68,0.35,0.02]
ypos2=[0.95,0.62,0.29]
;------------------------------------------------------------------------------------
;make the plot
set_plot,'PS'
device,filename=outfil,/ENCAPSUL,$
       xsize=20,ysize=26,/portrait,/color,/helvetica,/bold


!P.Font=0
!P.Thick=4

  tvlct,14,50,239,1
  tvlct,28,80,225,2
  tvlct,41,80,214,3
  tvlct,55,80,199,4
  tvlct,68,80,185,5
  tvlct,83,80,172,6
  tvlct,96,80,158,7
  tvlct,111,80,143,8
  tvlct,123,80,132,9
  tvlct,138,80,115,10
  tvlct,152,80,102,11
  tvlct,167,80,87,12
  tvlct,181,80,74,13
  tvlct,194,80,59,14
  tvlct,208,80,45,15
  tvlct,223,80,31,16
  tvlct,237,80,17,17
  tvlct,250,50,3,18

!P.Position=[xpos1,ypos1(0),xpos2,ypos2(0)]
;MAP_SET, 0, 180, /ISOTROPIC, $  
;   /HORIZON,/CONTINENTS, /GRID, $  
;  /NOBORDER,/ROBINSON,mlinethick=4,/noerase

Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

XYOUTS,0.44,0.96,titlees(0),/NORMAL,alignment=0.5,charsize=1.2,color=0
XYOUTS,0.05,0.96,'a)',/NORMAL,alignment=0.5,charsize=1.2,color=0

!P.Position=[xpos1,ypos1(0),xpos2,ypos2(0)]
boxfill,sterrfield,lons,lats,colors=kcolsarrT,levels=levsarrT	    ;,nofill_color=kcolsarrT(0)

     
; Overplot continents and islands again
!P.Position=[xpos1,ypos1(0),xpos2,ypos2(0)]
;MAP_SET, 0, 180, /ISOTROPIC, $  
;   /HORIZON,/CONTINENTS, /GRID, $  
;  /NOBORDER,/ROBINSON,mlinethick=4,/noerase
Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

PLOTS,[-179.9,0],[89.9,89.9],color=0
PLOTS,[0,179.9],[89.9,89.9],color=0
PLOTS,[-179.9,0],[-89.9,-89.9],color=0
PLOTS,[0,179.9],[-89.9,-89.9],color=0

MAKE_KEY,0.87,0.68,0.02,0.29,0.03,-0.007,/NORMAL,COLORS=colsarrT,labels=labsarrT,$
         charsize=1.1,charthick=4,bcolor=0,orientation=1
;XYOUTS,0.97,0.82,'!Eo!N C',/normal,color=0,charsize=1.2,alignment=0.5,orientation=-90
XYOUTS,0.97,0.82,'g kg!E-1!N',/normal,color=0,charsize=1.2,alignment=0.5,orientation=-90

!P.Position=[xpos1,ypos1(1),xpos2,ypos2(1)]
Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

XYOUTS,0.44,0.63,titlees(1),/NORMAL,alignment=0.5,charsize=1.2,color=0
XYOUTS,0.05,0.63,'b)',/NORMAL,alignment=0.5,charsize=1.2,color=0
  
!P.Position=[xpos1,ypos1(1),xpos2,ypos2(1)]
boxfill,sperrfield,lons,lats,colors=kcolsarrT,levels=levsarrT	    ;,nofill_color=kcolsarrT(0)
     
; Overplot continents and islands again
!P.Position=[xpos1,ypos1(1),xpos2,ypos2(1)]
Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

PLOTS,[-179.9,0],[89.9,89.9],color=0
PLOTS,[0,179.9],[89.9,89.9],color=0
PLOTS,[-179.9,0],[-89.9,-89.9],color=0
PLOTS,[0,179.9],[-89.9,-89.9],color=0

MAKE_KEY,0.87,0.35,0.02,0.29,0.03,-0.007,/NORMAL,COLORS=colsarrT,labels=labsarrT,$
         charsize=1.1,charthick=4,bcolor=0,orientation=1
;XYOUTS,0.97,0.49,'!Eo!N C',/normal,color=0,charsize=1.2,alignment=0.5,orientation=-90
XYOUTS,0.97,0.49,'g kg!E-1!N',/normal,color=0,charsize=1.2,alignment=0.5,orientation=-90

;------------------------------------

!P.Position=[xpos1,ypos1(2),xpos2,ypos2(2)]
Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

XYOUTS,0.44,0.30,titlees(2),/NORMAL,alignment=0.5,charsize=1.2,color=0
XYOUTS,0.05,0.30,'c)',/NORMAL,alignment=0.5,charsize=1.2,color=0
  
!P.Position=[xpos1,ypos1(2),xpos2,ypos2(2)]
;boxfill,combfield,lons,lats,colors=kcolsarrST,levels=levsarrST	    ;,nofill_color=kcolsarrT(0)
boxfill,combpct,lons,lats,colors=kcolsarrPCT,levels=levsarrPCT	    ;,nofill_color=kcolsarrT(0)
     
; Overplot continents and islands again
!P.Position=[xpos1,ypos1(2),xpos2,ypos2(2)]
Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

PLOTS,[-179.9,0],[89.9,89.9],color=0
PLOTS,[0,179.9],[89.9,89.9],color=0
PLOTS,[-179.9,0],[-89.9,-89.9],color=0
PLOTS,[0,179.9],[-89.9,-89.9],color=0

;MAKE_KEY,0.87,0.02,0.02,0.29,0.03,-0.007,/NORMAL,COLORS=colsarrST,labels=labsarrST,$
;         charsize=1.1,charthick=4,bcolor=0,orientation=1
;XYOUTS,0.97,0.16,'g/kg',/normal,color=0,charsize=1.2,alignment=0.5,orientation=-90
MAKE_KEY,0.87,0.02,0.02,0.29,0.03,-0.007,/NORMAL,COLORS=colsarrPCT,labels=labsarrPCT,$
         charsize=1.1,charthick=4,bcolor=0,orientation=1
XYOUTS,0.97,0.16,'% of '+titlemonth+' climatology',/normal,color=0,charsize=1.2,alignment=0.5,orientation=-90




DEVICE,/close
gots=WHERE(combpct GT 0.,countall)
smalls=WHERE(combpct GT 0. AND combpct LT 5.,count)
print,'LESS THAN 5%: ',count,(count/FLOAT(countall))*100
bigss=WHERE(combpct GT 0. AND combpct GT 10.,count)
print,'GREATER THAN 10%: ',count,(count/FLOAT(countall))*100

stop

return

END
