PRO plot_HadCRUH2STATIONuncertainty_FEB2013

styr=1973
edyr=2012
nyrs=(edyr+1)-styr
nmons=nyrs*12

chosendate=((1980-styr)*12)+5	; should be June 1980
;chosendate=((2000-styr)*12)+5	; should be June 2000
;chosendate=((2010-styr)*12)+5	; should be June 2000
;chosendate=((1980-styr)*12)+11	; should be Dec 1980
;chosendate=((2000-styr)*12)+11	; should be Dec 2000
;chosendate=((2010-styr)*12)+11	; should be Dec 2000

titlees=['Measurement Uncertainty June 1980','Climatology Uncertainty June 1980','Adjustment Uncertainty June 1980']
;titlees=['Measurement Uncertainty June 2000','Climatology Uncertainty June 2000','Adjustment Uncertainty June 2000']
;titlees=['Measurement Uncertainty June 2010','Climatology Uncertainty June 2010','Adjustment Uncertainty June 2010']
;titlees=['Measurement Uncertainty December 1980','Climatology Uncertainty December 1980','Adjustment Uncertainty December 1980']
;titlees=['Measurement Uncertainty December 2000','Climatology Uncertainty December 2000','Adjustment Uncertainty December 2000']
;titlees=['Measurement Uncertainty December 2010','Climatology Uncertainty December 2010','Adjustment Uncertainty December 2010']

filtab='Jun1980'
;filtab='Jun2000'
;filtab='Jun2010'
;filtab='Dec1980'
;filtab='Dec2000'
;filtab='Dec2010'

latlg=5.
lonlg=5.
stlt=-90+(latlg/2.)
stln=-180+(lonlg/2.)
nlats=180/latlg
nlons=360/lonlg
nbox=LONG(nlats*nlons)

lats=(findgen(nlats)*latlg)+stlt
lons=(findgen(nlons)*lonlg)+stln


indir='/data/local/hadkw/HADCRUH2/UPDATE2012/MONTHLIES/'
infile='HadISDH.landq.1.0.0.2012p.FLATgridPHA5by5'
outfil='/data/local/hadkw/HADCRUH2/UPDATE2012/IMAGES/HadISDHPHAFLAT_STATIONuncertainty_FEB2013_'+filtab+'.eps'

mdi=-1e+30

;--------------------------------------

filee=NCDF_OPEN(indir+infile+'.nc')
timvarid=NCDF_VARID(filee,'times')
longs_varid=NCDF_VARID(filee,'lon')
lats_varid=NCDF_VARID(filee,'lat')
qobid=NCDF_VARID(filee,'qhum_obserr') 	; may become uncertainty fields
qcmid=NCDF_VARID(filee,'qhum_climerr') 	; may become uncertainty fields
qajid=NCDF_VARID(filee,'qhum_adjerr') 	; may become uncertainty fields
NCDF_VARGET,filee,timvarid,times
NCDF_VARGET,filee,qobid,q_oberr
NCDF_VARGET,filee,qcmid,q_cmerr
NCDF_VARGET,filee,qajid,q_ajerr
NCDF_CLOSE,filee

timeunits='month'	
   
oberrfield=q_oberr(*,*,chosendate)
cmerrfield=q_cmerr(*,*,chosendate)
ajerrfield=q_ajerr(*,*,chosendate)
 
   


kcolsarrST=[100,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]	; 14 colours + black to ensure no botching
levsarrST=[-2e+30,0.0,0.01,0.02,0.03,0.04,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.8,10]

;kcolsarrT=[100,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]	; 14 colours + black to ensure no botching
;levsarrT=[-2e+30,0.000,0.005,0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,1.,10]

;kcolsarrT=[100,1,3,5,7,8,9,10,11,12,14,16,18]	; 14 colours + black to ensure no botching
;levsarrT=[-2e+30,0.000,0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.,10]

kcolsarrT=[100,1,4,7,9,11,13,15,18]	; 14 colours + black to ensure no botching
levsarrT=[-2e+30,0.000,0.01,0.1,0.3,0.5,0.7,1.,1.1,10]


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
;------------------------------------------------------------------------------------
xpos1=0.04
xpos2=0.86
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
boxfill,oberrfield,lons,lats,colors=kcolsarrT,levels=levsarrT	    ;,nofill_color=kcolsarrT(0)

     
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

MAKE_KEY,0.88,0.68,0.02,0.29,0.02,-0.007,/NORMAL,COLORS=colsarrT,labels=labsarrT,$
         charsize=1.1,charthick=4,bcolor=0,orientation=1
XYOUTS,0.97,0.82,'g/kg per decade',/normal,color=0,charsize=1.2,alignment=0.5,orientation=-90

!P.Position=[xpos1,ypos1(1),xpos2,ypos2(1)]
Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

XYOUTS,0.44,0.63,titlees(1),/NORMAL,alignment=0.5,charsize=1.2,color=0
XYOUTS,0.05,0.63,'b)',/NORMAL,alignment=0.5,charsize=1.2,color=0
  
!P.Position=[xpos1,ypos1(1),xpos2,ypos2(1)]
boxfill,cmerrfield,lons,lats,colors=kcolsarrT,levels=levsarrT	    ;,nofill_color=kcolsarrT(0)
     
; Overplot continents and islands again
!P.Position=[xpos1,ypos1(1),xpos2,ypos2(1)]
Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

PLOTS,[-179.9,0],[89.9,89.9],color=0
PLOTS,[0,179.9],[89.9,89.9],color=0
PLOTS,[-179.9,0],[-89.9,-89.9],color=0
PLOTS,[0,179.9],[-89.9,-89.9],color=0

MAKE_KEY,0.88,0.35,0.02,0.29,0.02,-0.007,/NORMAL,COLORS=colsarrT,labels=labsarrT,$
         charsize=1.1,charthick=4,bcolor=0,orientation=1
XYOUTS,0.97,0.49,'g/kg per decade',/normal,color=0,charsize=1.2,alignment=0.5,orientation=-90

;------------------------------------

!P.Position=[xpos1,ypos1(2),xpos2,ypos2(2)]
Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

XYOUTS,0.44,0.30,titlees(2),/NORMAL,alignment=0.5,charsize=1.2,color=0
XYOUTS,0.05,0.30,'c)',/NORMAL,alignment=0.5,charsize=1.2,color=0
  
!P.Position=[xpos1,ypos1(2),xpos2,ypos2(2)]
boxfill,ajerrfield,lons,lats,colors=kcolsarrT,levels=levsarrT	    ;,nofill_color=kcolsarrT(0)
     
; Overplot continents and islands again
!P.Position=[xpos1,ypos1(2),xpos2,ypos2(2)]
Map_set,/continents,color=0,/noborder,/noerase,/robinson,/grid, glinestyle=2

PLOTS,[-179.9,0],[89.9,89.9],color=0
PLOTS,[0,179.9],[89.9,89.9],color=0
PLOTS,[-179.9,0],[-89.9,-89.9],color=0
PLOTS,[0,179.9],[-89.9,-89.9],color=0

MAKE_KEY,0.88,0.02,0.02,0.29,0.02,-0.007,/NORMAL,COLORS=colsarrT,labels=labsarrT,$
         charsize=1.1,charthick=4,bcolor=0,orientation=1
XYOUTS,0.97,0.16,'g/kg per decade',/normal,color=0,charsize=1.2,alignment=0.5,orientation=-90




DEVICE,/close



return

END
