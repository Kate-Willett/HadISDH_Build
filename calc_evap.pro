; WHATS IN HERE?
; function calc_evap,t,P: VAPOUR PRESSURE WITH RESPECT TO WATER (IF dewpoint T is used) hPa, SATURATION VAPOUR PRESSURE WITH RESPECT TO WATER (IF T is used)
; function calc_evap_ice,t,P: VAPOUR PRESSURE WITH RESPECT TO ICE (IF dewpoint T is used) hPa, SATURATION VAPOUR PRESSURE WITH RESPECT TO ICE (IF T is used)
; function calc_dewp,e,P: DEWPOINT TEMPERATURE WITH RESPECT TO WATER (deg C)
; function calc_dewp_ice,e,P: DEWPOINT TEMPERATURE WITH RESPECT TO ICE (deg C)
; function calc_wetbulb, e,P,Td,T: WETBULB TEMPERATURE in deg C
; function calc_qhum,e,P: SPECIFIC HUMIDITY (g/kg)
; function calc_ehum,q,P: VAPOUR PRESSURE FROM SPECIFIC HUMIDITY (hPa)
; function calc_rh,e,es: RELATIVE HUMIDITY %rh 
; function calc_erh,es,rh: VAPOUR PRESSURE (hPa) from relative humidity and saturated vapour pressure
; function calc_esrh,e,rh: SATURATED VAPOUR PRESSURE (hPa) from relative humidity and vapour pressure
; function calc_thi,t,rh: THI (TEMPERATURE HUMIDITY INDEX) for cows 0-100.
; function calc_wbgt,e,t: PSEUDO WET BULB GLOBE TEMPERATURE deg C
; function calc_ewbgt,w,t: VAPOUR PRESSURE FROM PSEUDO-WET BULB GLOBE TEMPERATURE in hPa
; function calc_humidex, e,t: HUMIDEX in deg C?
; function calc_appt, e,t,u: APPARENT TEMPERATURE (in the shade) in deg C
; function calc_hi, rh,t: HEAT INDEX in deg C

;**************************************************************
function calc_evap,t,P
; VAPOUR PRESSURE WITH RESPECT TO WATER (IF dewpoint T is used) hPa
; SATURATION VAPOUR PRESSURE WITH RESPECT TO WATER (IF T is used)
; temperature (or dewpoint temperature) in deg C 
; station level pressure in hPa
; Buck 1981
; Buck, A. L.: New equations for computing vapor pressure and en-
; hancement factor, J. Appl. Meteorol., 20, 1527?1532, 1981.

f=1+(7.*10.^(-4.))+((3.46*10.^(-6.))*P)

e=6.1121*f*EXP(((18.729-(t/227.3))*t)/(257.87+t))

return,e

end

;---------
function calc_evap_ice,t,P
; VAPOUR PRESSURE WITH RESPECT TO ICE (IF dewpoint T is used) hPa
; SATURATION VAPOUR PRESSURE WITH RESPECT TO ICE (IF T is used)
; I USE THIS WHEN WETBULB TEMPERATURE IS LESS THAN OR EQUAL TO 0 DEG C
; temperature (or dewpoint temperature) in deg C 
; station level pressure in hPa
; Buck 1981
; Buck, A. L.: New equations for computing vapor pressure and en-
; hancement factor, J. Appl. Meteorol., 20, 1527?1532, 1981.

f=1+(3.*10.^(-4.))+((4.18*10.^(-6.))*P)

e=6.1115*f*EXP(((23.036-(t/333.7))*t)/(279.82+t))

return,e

end

;--------

function calc_dewp,e,P
; DEWPOINT TEMPERATURE WITH RESPECT TO WATER (deg C)
; reverse Eq. for evap to get dewpoint
; temperature (or dewpoint temperature) in deg C 
; station level pressure in hPa
; Buck 1981
; Buck, A. L.: New equations for computing vapor pressure and en-
; hancement factor, J. Appl. Meteorol., 20, 1527?1532, 1981.

f=1+(7.*10.^(-4.))+((3.46*10.^(-6.))*P)

a=1
b=(227.3*alog(e/(6.1121*f)))-(18.729*227.3)
c=(257.87*227.3*alog(e/(6.1121*f)))

d=(-b-SQRT(b^2-(4*a*c)))/(2*a)

return,d

end

;---------
function calc_dewp_ice,e,P
; DEWPOINT TEMPERATURE WITH RESPECT TO ICE (deg C)
; I USE THIS WHEN WETBULB TEMPERATURE IS LESS THAN OR EQUAL TO 0 DEG C
; reverse Eq. for evap to get dewpoint
; temperature (or dewpoint temperature) in deg C 
; station level pressure in hPa
; = saturation vapour pressure or vapour pressure in hPa
; Buck 1981
; Buck, A. L.: New equations for computing vapor pressure and en-
; hancement factor, J. Appl. Meteorol., 20, 1527?1532, 1981.

f=1+(3.*10.^(-4.))+((4.18*10.^(-6.))*P)

a=1
b=(333.7*alog(e/(6.1115*f)))-(23.036*333.7)
c=(279.82*333.7*alog(e/(6.1115*f)))

d=(-b-SQRT(b^2-(4*a*c)))/(2*a)

return,d

end

;---------
function calc_wetbulb, e,P,Td,T
; WETBULB TEMPERATURE in deg C
; e = vapour pressure in hPa
; P = pressure in hPa
; dewpoint temperature in deg C
; temperature in deg C
; Jenson et al 1990
; Jensen, M. E., Burman, R. D., and Allen, R. G. (Eds.): Evapotran-
; spiration and Irrigation Water Requirements: ASCE Manuals and
; Reports on Engineering Practices No. 70, American Society of
; Civil Engineers, New York, 360 pp., 1990.

a=0.000066*P
b=((409.8*e)/((Td+237.3)^2))

w=(((a*T)+(b*Td))/(a+b))

return,w

end

;----------

function calc_qhum,e,P
; SPECIFIC HUMIDITY (g/kg)
; vapour pressure in hPa
; station pressure in hPa
; = specific humidity in g/kg
; Peixoto & Oort, 1996, Ross & Elliott, 1996
; Peixoto, J. P. and Oort, A. H.: The climatology of relative humidity
; in the atmosphere, J. Climate, 9, 3443?3463, 1996.


q=1000.*((0.622*e)/(P-((1-0.622)*e)))

return,q

end

;----------

function calc_ehum,q,P	; calc e from q
; VAPOUR PRESSURE FROM SPECIFIC HUMIDITY (hPa)
; station pressure in hPa

e=((q/1000.)*P)/(0.622+(0.388*(q/1000.)))

return,e

end

;------------
function calc_rh,e,es
; RELATIVE HUMIDITY %rh 
; vapour pressure in hPa
; saturated vapour pressure in hPa

rh=(e/es)*100.

return,rh

end

;------------
function calc_erh,es,rh
; VAPOUR PRESSURE (hPa) from relative humidity and saturated vapour pressure
; relative humdity in %rh
; saturated vapour pressure in hPa

erh=(rh*es)/100.

return,erh

end

;------------
function calc_esrh,e,rh
; SATURATED VAPOUR PRESSURE (hPa) from relative humidity and vapour pressure
; relative humdity in %rh
; vapour pressure in hPa 

esrh=(e/rh)*100.

return,esrh

end
;---------

function calc_thi,t,rh
; THI (TEMPERATURE HUMIDITY INDEX) for cows 0-100.
; drybulb temperature in deg C
; relative humidity in %rh
; Davis?

thi=((1.8*t)+32.)-((0.55-(0.0055*rh))*((1.8*t)-26.))

return,thi

end

;-------------

function calc_wbgt,e,t
; PSEUDO WET BULB GLOBE TEMPERATURE deg C
; vapour pressure in hPa
; drybulb temperature in deg C
; ACSM, 1984
; ACSM. 1984. Prevention of thermal injuries during distance running.
; American College of Sports Medicine. Medical Journal of Australia
; 141: 876?879.

wbgt=(0.567*t) + (0.393*e) + 3.94

return,wbgt

end

;----------

function calc_ewbgt,w,t
; VAPOUR PRESSURE FROM PSEUDO-WET BULB GLOBE TEMPERATURE in hPa
; wetbulb globe temperature in deg C
; drybulb temperature in deg C
; ACSM, 1984
; ACSM. 1984. Prevention of thermal injuries during distance running.
; American College of Sports Medicine. Medical Journal of Australia
; 141: 876?879.

e=(w - 3.94 - (0.567*t)) / 0.393	

return,e

end

;----------------------
function calc_humidex, e,t
; HUMIDEX in deg C?
; vapoure pressure in hPa
; drybulb temperature in deg C
; Masterson and Richardson, 1979
; Masterson J, Richardson FA. 1979. Humidex, A method of Quantifying
; Human Discomfort Due to Excessive Heat and Humidity.
; Environment Canada: Downsview, Ontario, pp 45.

h= t + (0.5555*(e-10.))

return,h

end
;-----------------------------
function calc_appt, e,t,u
; APPARENT TEMPERATURE (in the shade) in deg C
; vapoure pressure in hPa
; drybulb temperature in deg C
; wind speed in m s-1
; Steadman 1994
; Steadman N. 1994. Norms of apparent temperature in Australia.
; Australian Meteorology Magazine 43: 1?16.


at = t + (0.33*e) - (0.7*u) - 4.

return,at

end
;-----------------------------
function calc_hi, rh,t
; HEAT INDEX in deg C
; NOTE - MEANINGLESS/SCREWY RESULTS WHEN t<26.6 and RH < 40%
; relative humidity in %rh
; drybulb temperature in deg C (added in conversion to/from fahrenheit here
; Rothfusz, 1990
; Rothfusz LP. 1990. The Heat Index Equation, SR Technical Attachment,
; 94-19, pp 6.

; http://www.hpc.ncep.noaa.gov/html/heatindex_equation.shtml

tf = t * (9./5.) + 32

hif = -42.379 + (2.04901523*tf) + (10.14333127*rh) + $
      (-0.22475541*tf*rh) + (-0.006837837*tf*tf) + $
      (-0.05481717*rh*rh) + (0.001228747*tf*tf*rh) + $
      (0.00085282*tf*rh*rh) + (-0.00000199*tf*tf*rh*rh)

; apply adjustment factors
; IF (rh LT 13) AND ((tf GT 80) AND (tf LT 112)) 
gots=WHERE((rh LT 13) AND ((tf GT 80) AND (tf LT 112)),count)
IF (gots GT 0) THEN hic(gots)=hic(gots) - ((13.- (rh(gots)))/4.)*SQRT((17.-ABS(tf(gots)-95.))/17.) 
; IF (rh GT 85) AND ((tf GT 80) AND (tf LT 87)) 
gots=WHERE((rh GT 85) AND ((tf GT 80) AND (tf LT 87)),count)
IF (gots GT 0) THEN hic(gots)=hic(gots) - ((rh(gots)-85)/10.)*((87.-tf(gots))/5.)
; IF (hif LT 80) 
gots=WHERE(hif LT 80,count)
IF (gots GT 0) THEN hic(gots)= 0.5 * (tf(gots) + 61. + ((tf(gots)-68.)*1.2) + (rh(gots)*0.094))
 
hic = (hif - 32) / (9./5.)

return,hic


;The computation of the heat index is a refinement of a result obtained by multiple regression analysis carried out by Lans P. Rothfusz and described in a 1990 National Weather Service (NWS) Technical Attachment (SR 90-23).  The regression equation of Rothfusz is

;    HI = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH 

;where T is temperature in degrees F and RH is relative humidity in percent.  HI is the heat index expressed as an apparent temperature in degrees F.  If the RH is less than 13% and the temperature is between 80 and 112 degrees F, then the following adjustment is subtracted from HI:

;    ADJUSTMENT = [(13-RH)/4]*SQRT{[17-ABS(T-95.)]/17} 

;where ABS and SQRT are the absolute value and square root functions, respectively.  On the other hand, if the RH is greater than 85% and the temperature is between 80 and 87 degrees F, then the following adjustment is added to HI:

;    ADJUSTMENT = [(RH-85)/10] * [(87-T)/5] 

;The Rothfusz regression is not appropriate when conditions of temperature and humidity warrant a heat index value below about 80 degrees F. In those cases, a simpler formula is applied to calculate values consistent with Steadman's results:

;    HI = 0.5 * {T + 61.0 + [(T-68.0)*1.2] + (RH*0.094)} 

;In practice, the simple formula is computed first and the result averaged with the temperature. If this heat index value is 80 degrees F or higher, the full regression equation along with any adjustment as described above is applied.

;The Rothfusz regression is not valid for extreme temperature and relative humidity conditions beyond the range of data considered by Steadman. 
end
;-----------------------------
