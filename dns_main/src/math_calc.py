#!/usr/bin/env python2
from math import sqrt, pow

def scale_vec(a,b):
    scale_vec = [a[0]/length_b, a[1]/length_b, a[2]/length_b]   
    length_b = vector_length(b)
    return scale_vec
def scale_scale(a,t):

    scale_scale = [a[0]*t,a[1]*t,a[2]*t]
    return scale_scale