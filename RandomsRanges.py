#!/usr/local/sci/bin/python

#***************************************
# LetterRange: Range of characters
#
#
#
# 03 April 2014 KMW - v1
#************************************************************************
#                                 START
#************************************************************************
# USE python3
#************************************************************************
# Set up python imports
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from scipy.optimize import curve_fit,fsolve,leastsq
from scipy import pi,sqrt,exp
from scipy.special import erf
import scipy.stats
from math import sqrt,pi
import struct

#************************************************************************
# Subroutines
#************************************************************************
# LetterRange
def LetterRange(start,stop): 
    ''' provide either a start and end number corresponding to A-Z '''
    ''' or an 'a' to 'z' character '''
    ''' code returns an array of letters '''
    ''' a=97 so start+97 '''
    
    if isinstance(start,int):
        newstart=start+97
        newstop=stop+97
#	print('Integers: ',newstart,newstop)
    else:
        newstart=ord(start)
        newstop=ord(stop)
#	print('Characters: ',newstart,newstop)
       
    Alphabetti=[]
    
    for char in range(newstart,newstop):
#        print(chr(char))
        Alphabetti.append(chr(char))
        
    return  Alphabetti # LetterRange

#************************************************************************
