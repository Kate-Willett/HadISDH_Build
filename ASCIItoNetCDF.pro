pro ASCIItoNetCDF

indir='/data/local/hadkw/HADCRUH2/UPDATE2014/OTHERDATA/grid-mntp-1880-current-v3.2.2.dat'
outdir='/data/local/hadkw/HADCRUH2/UPDATE2014/OTHERDATA/GHCNM_18802014.nc'

mdiin=-9999
mdiout=-1e30

styr=1880
edyr=2014
nyrs=(edyr-styr)+1
nmons=nyrs*12

nlats=36
nlons=72
lats=87.5-(indgen(nlats)*5.)
lons=-177.5+(indgen(nlons)*5.)

valarr=make_array(nlons,nlats,nmons,/float,value=mdiout)

; read in the data
dummy=''
openr,3,indir
FOR mm=0,nmons-1 DO BEGIN
  FOR llt=nlats,0,-1 DO BEGIN ;extra row for month,year
    print, llt
    IF (llt EQ nlats) THEN BEGIN
      readf,3,dummy,format='(a)' 
    ENDIF ELSE BEGIN
      tmps=intarr(72)
      readf,3,tmps,format='(72i6)'
      valarr(*,llt,mm)=tmps/100.
    ENDELSE
  ENDFOR
ENDFOR
close,3
bads=WHERE(valarr EQ mdiin/100.,count)
IF (count GT 0) THEN valarr(bads)=mdiout

; output the data
lats=REVERSE(lats)

inn=NCDF_CREATE(outdir,/clobber)

time_id=NCDF_DIMDEF(inn,'time',nmons)
timvarid=NCDF_VARDEF(inn,'time',[time_id],/DOUBLE)
lat_id=NCDF_DIMDEF(inn,'latitude',nlats)
lon_id=NCDF_DIMDEF(inn,'longitude',nlons)
latvarid=NCDF_VARDEF(inn,'latitude',[lat_id],/DOUBLE)
lonvarid=NCDF_VARDEF(inn,'longitude',[lon_id],/DOUBLE)

t_varid=NCDF_VARDEF(inn,'temperature_anomaly',[lon_id,lat_id,time_id],/FLOAT)

NCDF_ATTPUT,inn,timvarid,'units','months since 1880'
NCDF_ATTPUT,inn,timvarid,'long_name','Time'

NCDF_ATTPUT,inn,latvarid,'units','Degrees North'
NCDF_ATTPUT,inn,latvarid,'long_name','Latitude'

NCDF_ATTPUT,inn,timvarid,'units','Degrees East'
NCDF_ATTPUT,inn,timvarid,'long_name','Time'

NCDF_ATTPUT,inn,t_varid,'units','deg C'
NCDF_ATTPUT,inn,t_varid,'long_name','GHCNM Land Surface Temperature Anomalies'
NCDF_ATTPUT,inn,t_varid,'missing_value',mdiout
NCDF_CONTROL,inn,/ENDEF

NCDF_VARPUT,inn,t_varid,valarr
NCDF_VARPUT,inn,timvarid,indgen(nmons)
NCDF_VARPUT,inn,latvarid,lats
NCDF_VARPUT,inn,lonvarid,lons

NCDF_CLOSE,inn



end
