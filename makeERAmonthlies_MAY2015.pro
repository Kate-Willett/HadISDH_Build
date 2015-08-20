pro makeERAmonthlies_MAY2015

; Read in 6 hourly ERA files
; Convert to other variables
; Average to monthly
; Save

; USE calc_evap
; USE testleap

;************************************************
; File and vars set up
indir='/data/local/hadkw/HADCRUH2/UPDATE2014/OTHERDATA/'
outdir='/data/local/hadkw/HADCRUH2/UPDATE2014/OTHERDATA/'
infilT='ERAINTERIM_drybulbT_6hr_1by1_'
infilTd='ERAINTERIM_dewpointT_6hr_1by1_'
infilP='ERAINTERIM_sp_6hr_1by1_'
indecs=['1979010119881231','1989010119981231','1999010120081231','2009010120141231']

extra=0	; 1 means add the extra file
;infilEXTRA='ERAINTERIM_ALL_6hr_1by1_'
outfile='e2m_monthly_1by1_ERA-Interim_data_19792014.nc'
outfilTw='tw2m_monthly_1by1_ERA-Interim_data_19792014.nc'
outfilq='q2m_monthly_1by1_ERA-Interim_data_19792014.nc'
outfilRH='rh2m_monthly_1by1_ERA-Interim_data_19792014.nc'
outfilT='t2m_monthly_1by1_ERA-Interim_data_19792014.nc'
outfilTd='td2m_monthly_1by1_ERA-Interim_data_19792014.nc'
outfilDPD='dpd2m_monthly_1by1_ERA-Interim_data_19792014.nc'

mdi=-1e30

styr=1979	; 1979
edyr=2014	; 2013
nyrs=(edyr+1)-styr
nmons=nyrs*12
ndecs=4
int_mons=indgen(nmons)
nleaps=9	;1980,1984,1988,1992,1996,2000,2004,2008,2012
;ndays=LONG((nyrs*365)+nleaps)
;nhrs=LONG(ndays*4)	;51136

nlons=360
nlats=181

monthe=make_array(nlons,nlats,nmons,type=FLOAT,value=mdi)
monthTw=make_array(nlons,nlats,nmons,type=FLOAT,value=mdi)
monthq=make_array(nlons,nlats,nmons,type=FLOAT,value=mdi)
monthRH=make_array(nlons,nlats,nmons,type=FLOAT,value=mdi)
monthT=make_array(nlons,nlats,nmons,type=FLOAT,value=mdi)
monthTd=make_array(nlons,nlats,nmons,type=FLOAT,value=mdi)
monthDPD=make_array(nlons,nlats,nmons,type=FLOAT,value=mdi)

;************************************************
; Loop through each year, read in correct file
county=0	; counter through the years
FOR dd=0,ndecs-1 DO BEGIN
  sttim=0
  edtim=-1
  FOR yy=0,9 DO BEGIN
    
    ; get the correct pointers
    yrr=county+styr
    
    IF (yrr GT edyr) THEN break	; done all years!
    
    IF (testleap(yrr) EQ 0.0) THEN BEGIN
      sttim=edtim+1
      edtim=edtim+366*4
      mnarr=[31,29,31,30,31,30,31,31,30,31,30,31]
      hrarr=[124,116,124,120,124,120,124,124,120,124,120,124]
      pointarr=[124,240,364,484,608,728,852,976,1096,1220,1340,1464]
    ENDIF ELSE BEGIN
      sttim=edtim+1
      edtim=edtim+365*4
      mnarr=[31,28,31,30,31,30,31,31,30,31,30,31]
      hrarr=[124,112,124,120,124,120,124,124,120,124,120,124]
      pointarr=[124,236,360,480,604,724,848,972,1092,1216,1336,1460]
    ENDELSE
    
    print,yrr,sttim,edtim
    
    ; get the correct filename and read in the year
    inn=NCDF_OPEN(indir+infilT+indecs(dd)+'.nc')
    varid=NCDF_VARID(inn,'t2m')
    latid=NCDF_VARID(inn,'latitude')
    lonid=NCDF_VARID(inn,'longitude')
    NCDF_VARGET,inn,varid,tmp	;14612
    NCDF_VARGET,inn,latid,lats
    NCDF_VARGET,inn,lonid,lons
    NCDF_ATTGET,inn,varid,'scale_factor',scaleet
    NCDF_ATTGET,inn,varid,'add_offset',offseteet
    NCDF_CLOSE,inn
    t=(((tmp(*,*,sttim:edtim)*scaleet)+offseteet)-273.15)
    tmp=0
    print,'Read T'
;    stop
    
    inn=NCDF_OPEN(indir+infilTd+indecs(dd)+'.nc')
    varid=NCDF_VARID(inn,'d2m')
    latid=NCDF_VARID(inn,'latitude')
    lonid=NCDF_VARID(inn,'longitude')
    NCDF_VARGET,inn,varid,tmp	;14612
    NCDF_VARGET,inn,latid,lats
    NCDF_VARGET,inn,lonid,lons
    NCDF_ATTGET,inn,varid,'scale_factor',scaleed
    NCDF_ATTGET,inn,varid,'add_offset',offseteed
    NCDF_CLOSE,inn
    d=(((tmp(*,*,sttim:edtim)*scaleed)+offseteed)-273.15)
    tmp=0
    print,'Read Td'
    
    inn=NCDF_OPEN(indir+infilP+indecs(dd)+'.nc')
    varid=NCDF_VARID(inn,'sp')
    latid=NCDF_VARID(inn,'latitude')
    lonid=NCDF_VARID(inn,'longitude')
    NCDF_VARGET,inn,varid,tmp	;14612
    NCDF_VARGET,inn,latid,lats
    NCDF_VARGET,inn,lonid,lons
    NCDF_ATTGET,inn,varid,'scale_factor',scaleep
    NCDF_ATTGET,inn,varid,'add_offset',offseteep
    NCDF_CLOSE,inn
    p=(((tmp(*,*,sttim:edtim)*scaleep)+offseteep)/100.)
    tmp=0
    print,'Read P'
    
    FOR ltt=0,nlats-1 DO BEGIN
      FOR lnn=0,nlons-1 DO BEGIN
        df=d(lnn,ltt,*)
        tf=t(lnn,ltt,*)
        pf=p(lnn,ltt,*)
        e=calc_evap(df,pf)
        esat=calc_evap(tf,pf)
        tw=calc_wetbulb(e,pf,df,tf)
    ; NOW REDO FOR ICE BULBS - BIT OF ERROR AS Twet CALC FROM Ewater not Eice
        icicles=WHERE(tw LE 0.,count)
        IF (count GT 0) THEN BEGIN
          e(icicles)=calc_evap_ice(df(icicles),pf(icicles))
          esat(icicles)=calc_evap_ice(tf(icicles),pf(icicles))
          tw(icicles)=calc_wetbulb(e(icicles),pf(icicles),df(icicles),tf(icicles))
        ENDIF
        q=calc_qhum(e,pf)
        rh=(e/esat)*100.
        dpd=tf-df
	
        pointst=0
        pointed=-1
        FOR mm=0,11 DO BEGIN
	  mcount=((yrr-styr)*12)+mm
          pointst=pointed+1
          pointed=pointarr(mm)-1
          monthe(lnn,ltt,mcount)=mean(e(pointst:pointed))
          monthTw(lnn,ltt,mcount)=mean(tw(pointst:pointed))
          monthq(lnn,ltt,mcount)=mean(q(pointst:pointed))
          monthRH(lnn,ltt,mcount)=mean(rh(pointst:pointed))
          monthT(lnn,ltt,mcount)=mean(tf(pointst:pointed))
          monthTd(lnn,ltt,mcount)=mean(df(pointst:pointed))
          monthDPD(lnn,ltt,mcount)=mean(dpd(pointst:pointed))
;          print,mm,pointst,pointed
        ENDFOR
      ENDFOR
      print,ltt,lnn
    ENDFOR

    p=0 
    d=0
    t=0
    
    county=county+1
  ENDFOR
ENDFOR  

;************************************************
; Save as netCDF

; make times
moo=TIMEGEN(nmons+1,UNIT='Months',start=JULDAY(1,1,styr))
startee=JULDAY(1,1,styr)	; midday on 1st Jan 1979
noomoo=moo-startee
goomoo=(noomoo(0:nmons-1)-1)+(((noomoo(1:nmons)-1)-noomoo(0:nmons-1))/2.)

filename=outdir+outfile
file_out=NCDF_CREATE(filename,/clobber)
time_id=NCDF_DIMDEF(file_out,'time',nmons)
timvarid=NCDF_VARDEF(file_out,'time',[time_id],/DOUBLE)
lat_id=NCDF_DIMDEF(file_out,'latitude',nlats)
latvarid=NCDF_VARDEF(file_out,'latitude',[lat_id],/DOUBLE)
lon_id=NCDF_DIMDEF(file_out,'longitude',nlons)
lonvarid=NCDF_VARDEF(file_out,'longitude',[lon_id],/DOUBLE)

varid=NCDF_VARDEF(file_out,'e2m',[lon_id,lat_id,time_id],/FLOAT)

NCDF_ATTPUT,file_out,timvarid,'units','days since 1979-1-1 00:00:00'
NCDF_ATTPUT,file_out,timvarid,'long_name','Time'
NCDF_ATTPUT,file_out,varid,'units','hPa'
NCDF_ATTPUT,file_out,varid,'long_name','2 metre vapour pressure from 6hrly T and Td'
NCDF_ATTPUT,file_out,varid,'missing_value',-1e30
NCDF_ATTPUT,file_out,latvarid,'units','degrees_north'
NCDF_ATTPUT,file_out,latvarid,'long_name','latitude'
NCDF_ATTPUT,file_out,lonvarid,'units','degrees_east'
NCDF_ATTPUT,file_out,lonvarid,'long_name','longitude'

NCDF_CONTROL,file_out,/ENDEF

NCDF_VARPUT,file_out,varid,monthe
NCDF_VARPUT,file_out,latvarid,lats
NCDF_VARPUT,file_out,lonvarid,lons
NCDF_VARPUT,file_out,time_id,goomoo
NCDF_CLOSE,file_out;

filename=outdir+outfilTw
file_out=NCDF_CREATE(filename,/clobber)
time_id=NCDF_DIMDEF(file_out,'time',nmons)
timvarid=NCDF_VARDEF(file_out,'time',[time_id],/DOUBLE)
lat_id=NCDF_DIMDEF(file_out,'latitude',nlats)
latvarid=NCDF_VARDEF(file_out,'latitude',[lat_id],/DOUBLE)
lon_id=NCDF_DIMDEF(file_out,'longitude',nlons)
lonvarid=NCDF_VARDEF(file_out,'longitude',[lon_id],/DOUBLE)

varid=NCDF_VARDEF(file_out,'tw2m',[lon_id,lat_id,time_id],/FLOAT)

NCDF_ATTPUT,file_out,timvarid,'units','days since 1979-1-1 00:00:00'
NCDF_ATTPUT,file_out,timvarid,'long_name','Time'
NCDF_ATTPUT,file_out,varid,'units','degrees C'
NCDF_ATTPUT,file_out,varid,'long_name','2 metre wet bulb temperature from 6hrly T and Td'
NCDF_ATTPUT,file_out,varid,'missing_value',-1e30
NCDF_ATTPUT,file_out,latvarid,'units','degrees_north'
NCDF_ATTPUT,file_out,latvarid,'long_name','latitude'
NCDF_ATTPUT,file_out,lonvarid,'units','degrees_east'
NCDF_ATTPUT,file_out,lonvarid,'long_name','longitude'

NCDF_CONTROL,file_out,/ENDEF

NCDF_VARPUT,file_out,varid,monthTw
NCDF_VARPUT,file_out,latvarid,lats
NCDF_VARPUT,file_out,lonvarid,lons
NCDF_VARPUT,file_out,time_id,goomoo
NCDF_CLOSE,file_out;

filename=outdir+outfilq
file_out=NCDF_CREATE(filename,/clobber)
time_id=NCDF_DIMDEF(file_out,'time',nmons)
timvarid=NCDF_VARDEF(file_out,'time',[time_id],/DOUBLE)
lat_id=NCDF_DIMDEF(file_out,'latitude',nlats)
latvarid=NCDF_VARDEF(file_out,'latitude',[lat_id],/DOUBLE)
lon_id=NCDF_DIMDEF(file_out,'longitude',nlons)
lonvarid=NCDF_VARDEF(file_out,'longitude',[lon_id],/DOUBLE)

varid=NCDF_VARDEF(file_out,'q2m',[lon_id,lat_id,time_id],/FLOAT)

NCDF_ATTPUT,file_out,timvarid,'units','days since 1979-1-1 00:00:00'
NCDF_ATTPUT,file_out,timvarid,'long_name','Time'
NCDF_ATTPUT,file_out,varid,'units','g/kg'
NCDF_ATTPUT,file_out,varid,'long_name','2 metre specific humidity from 6hrly T and Td'
NCDF_ATTPUT,file_out,varid,'missing_value',-1e30
NCDF_ATTPUT,file_out,latvarid,'units','degrees_north'
NCDF_ATTPUT,file_out,latvarid,'long_name','latitude'
NCDF_ATTPUT,file_out,lonvarid,'units','degrees_east'
NCDF_ATTPUT,file_out,lonvarid,'long_name','longitude'

NCDF_CONTROL,file_out,/ENDEF

NCDF_VARPUT,file_out,varid,monthq
NCDF_VARPUT,file_out,latvarid,lats
NCDF_VARPUT,file_out,lonvarid,lons
NCDF_VARPUT,file_out,time_id,goomoo
NCDF_CLOSE,file_out;

filename=outdir+outfilRH
file_out=NCDF_CREATE(filename,/clobber)
time_id=NCDF_DIMDEF(file_out,'time',nmons)
timvarid=NCDF_VARDEF(file_out,'time',[time_id],/DOUBLE)
lat_id=NCDF_DIMDEF(file_out,'latitude',nlats)
latvarid=NCDF_VARDEF(file_out,'latitude',[lat_id],/DOUBLE)
lon_id=NCDF_DIMDEF(file_out,'longitude',nlons)
lonvarid=NCDF_VARDEF(file_out,'longitude',[lon_id],/DOUBLE)

varid=NCDF_VARDEF(file_out,'rh2m',[lon_id,lat_id,time_id],/FLOAT)

NCDF_ATTPUT,file_out,timvarid,'units','days since 1979-1-1 00:00:00'
NCDF_ATTPUT,file_out,timvarid,'long_name','Time'
NCDF_ATTPUT,file_out,varid,'units','%rh'
NCDF_ATTPUT,file_out,varid,'long_name','2 metre relative humidity from 6hrly T and Td'
NCDF_ATTPUT,file_out,varid,'missing_value',-1e30
NCDF_ATTPUT,file_out,latvarid,'units','degrees_north'
NCDF_ATTPUT,file_out,latvarid,'long_name','latitude'
NCDF_ATTPUT,file_out,lonvarid,'units','degrees_east'
NCDF_ATTPUT,file_out,lonvarid,'long_name','longitude'

NCDF_CONTROL,file_out,/ENDEF

NCDF_VARPUT,file_out,varid,monthRH
NCDF_VARPUT,file_out,latvarid,lats
NCDF_VARPUT,file_out,lonvarid,lons
NCDF_VARPUT,file_out,time_id,goomoo
NCDF_CLOSE,file_out;

filename=outdir+outfilT
file_out=NCDF_CREATE(filename,/clobber)
time_id=NCDF_DIMDEF(file_out,'time',nmons)
timvarid=NCDF_VARDEF(file_out,'time',[time_id],/DOUBLE)
lat_id=NCDF_DIMDEF(file_out,'latitude',nlats)
latvarid=NCDF_VARDEF(file_out,'latitude',[lat_id],/DOUBLE)
lon_id=NCDF_DIMDEF(file_out,'longitude',nlons)
lonvarid=NCDF_VARDEF(file_out,'longitude',[lon_id],/DOUBLE)

varid=NCDF_VARDEF(file_out,'t2m',[lon_id,lat_id,time_id],/FLOAT)

NCDF_ATTPUT,file_out,timvarid,'units','days since 1979-1-1 00:00:00'
NCDF_ATTPUT,file_out,timvarid,'long_name','Time'
NCDF_ATTPUT,file_out,varid,'units','degrees C'
NCDF_ATTPUT,file_out,varid,'long_name','2 metre dry bulb temperature from 6hrly T and Td'
NCDF_ATTPUT,file_out,varid,'missing_value',-1e30
NCDF_ATTPUT,file_out,latvarid,'units','degrees_north'
NCDF_ATTPUT,file_out,latvarid,'long_name','latitude'
NCDF_ATTPUT,file_out,lonvarid,'units','degrees_east'
NCDF_ATTPUT,file_out,lonvarid,'long_name','longitude'

NCDF_CONTROL,file_out,/ENDEF

NCDF_VARPUT,file_out,varid,monthT
NCDF_VARPUT,file_out,latvarid,lats
NCDF_VARPUT,file_out,lonvarid,lons
NCDF_VARPUT,file_out,time_id,goomoo
NCDF_CLOSE,file_out;

filename=outdir+outfilTd
file_out=NCDF_CREATE(filename,/clobber)
time_id=NCDF_DIMDEF(file_out,'time',nmons)
timvarid=NCDF_VARDEF(file_out,'time',[time_id],/DOUBLE)
lat_id=NCDF_DIMDEF(file_out,'latitude',nlats)
latvarid=NCDF_VARDEF(file_out,'latitude',[lat_id],/DOUBLE)
lon_id=NCDF_DIMDEF(file_out,'longitude',nlons)
lonvarid=NCDF_VARDEF(file_out,'longitude',[lon_id],/DOUBLE)

varid=NCDF_VARDEF(file_out,'td2m',[lon_id,lat_id,time_id],/FLOAT)

NCDF_ATTPUT,file_out,timvarid,'units','days since 1979-1-1 00:00:00'
NCDF_ATTPUT,file_out,timvarid,'long_name','Time'
NCDF_ATTPUT,file_out,varid,'units','degrees C'
NCDF_ATTPUT,file_out,varid,'long_name','2 metre dew point temperature from 6hrly T and Td'
NCDF_ATTPUT,file_out,varid,'missing_value',-1e30
NCDF_ATTPUT,file_out,latvarid,'units','degrees_north'
NCDF_ATTPUT,file_out,latvarid,'long_name','latitude'
NCDF_ATTPUT,file_out,lonvarid,'units','degrees_east'
NCDF_ATTPUT,file_out,lonvarid,'long_name','longitude'

NCDF_CONTROL,file_out,/ENDEF

NCDF_VARPUT,file_out,varid,monthTd
NCDF_VARPUT,file_out,latvarid,lats
NCDF_VARPUT,file_out,lonvarid,lons
NCDF_VARPUT,file_out,time_id,goomoo
NCDF_CLOSE,file_out;

filename=outdir+outfilDPD
file_out=NCDF_CREATE(filename,/clobber)
time_id=NCDF_DIMDEF(file_out,'time',nmons)
timvarid=NCDF_VARDEF(file_out,'time',[time_id],/DOUBLE)
lat_id=NCDF_DIMDEF(file_out,'latitude',nlats)
latvarid=NCDF_VARDEF(file_out,'latitude',[lat_id],/DOUBLE)
lon_id=NCDF_DIMDEF(file_out,'longitude',nlons)
lonvarid=NCDF_VARDEF(file_out,'longitude',[lon_id],/DOUBLE)

varid=NCDF_VARDEF(file_out,'dpd2m',[lon_id,lat_id,time_id],/FLOAT)

NCDF_ATTPUT,file_out,timvarid,'units','days since 1979-1-1 00:00:00'
NCDF_ATTPUT,file_out,timvarid,'long_name','Time'
NCDF_ATTPUT,file_out,varid,'units','degrees C'
NCDF_ATTPUT,file_out,varid,'long_name','2 metre dew point depression from 6hrly T and Td'
NCDF_ATTPUT,file_out,varid,'missing_value',-1e30
NCDF_ATTPUT,file_out,latvarid,'units','degrees_north'
NCDF_ATTPUT,file_out,latvarid,'long_name','latitude'
NCDF_ATTPUT,file_out,lonvarid,'units','degrees_east'
NCDF_ATTPUT,file_out,lonvarid,'long_name','longitude'

NCDF_CONTROL,file_out,/ENDEF

NCDF_VARPUT,file_out,varid,monthDPD
NCDF_VARPUT,file_out,latvarid,lats
NCDF_VARPUT,file_out,lonvarid,lons
NCDF_VARPUT,file_out,time_id,goomoo
NCDF_CLOSE,file_out;

;************************************************

stop
end
