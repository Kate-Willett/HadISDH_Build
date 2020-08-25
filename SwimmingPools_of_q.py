#python

# Calculate the amount of water in terms of olympic swimming pools (50x25x2) 
# that has gone into the atmosphere at the surface since 1973

EarthArea = 510100000000000 # earth area in m2 thanks to google
AirDensity = 1.225 # at sea level and 15 degrees kg/m3
Deltaq = 0.08 # HadISDH.blend.1.0.0.2019f g/kg/10yr
Decades = 4.7 # as of 2019 so 1973 to 2019 is 47 years
SwimmingPool = 2500000 # kg 50x25x5m pool contains about 2500000 litres and 1 litre ~ 1kg

# How much water vapour has been added per kg over time (in kg)
TotalDeltaqKG = Deltaq*Decades/1000.

# What is the mass of the bottom 1m of the atmosphere (in kg)
#Mass1m = 1/AirDensity
Mass1m = AirDensity
Surface1mMass = Mass1m * EarthArea

# For each kg there has been an increase of TotalDeltaqKG so calculate the total increase over the bottom 1m of the surface
Surface1mDeltaq = Surface1mMass * TotalDeltaqKG

# How many swimming pools is this?
NoPools = Surface1mDeltaq / SwimmingPool

print('Since 1973 approximately ',NoPools,' Olympic (50x25x2m) swimming pools worth of water more is now being held in the atmosphere as a gas')

# 62627.79 so ~63000!!!



# John's Code
import numpy as np

q_trend = 0.08 #g/kg/10yr
air_density = 1.225 #kg/m3
water_density = 997. #kg/m3
radius_of_earth = 6371. #km
one_swimming_pool = 50. * 25. * 2.#m3

area_earth_in_m2 = 4 * np.pi * (radius_of_earth * 1000.)**2
mass = area_earth_in_m2 * air_density #m3 * kg/m3
water_in_g = mass * q_trend * (2019-1973+1)/10. 
water_in_kg = water_in_g/1000.
water_in_m3 = water_in_kg / water_density
swimming_pools = water_in_m3 / one_swimming_pool
print('John Ks: ',swimming_pools)
