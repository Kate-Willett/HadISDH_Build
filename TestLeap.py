#!/usr/local/sci/bin/python
# PYTHON2.7

# import TestLeap
# TestVal = TestLeap.TestLeap(year)

import numpy as np

def TestLeap(year):

    '''function to test if a year is a leap year'''
    '''returns 0.0 if it is a leap year'''
    '''returns a non-zero number if it is not a leap year'''
    '''ONLY WORKS WITH SCALARS!!!'''

    # first test - is it divisible by 4?
    leapoo = (year/4.) - np.round(year/4.)	

    # second test - if it is divisible by 100. then is it also divisible by 400?
    if (((year/100.) - np.round(year/100.)) == 0.):
        leapoo = leapoo + ((year/400.) - np.round(year/400.))

    return leapoo

