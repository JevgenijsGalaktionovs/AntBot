#!/usr/bin/env python2
from math import pi, cos, sin, atan2, acos, sqrt, pow, radians
from kinematics import *

class Math_Calc(object):
    def dotProduct(self,a,b):
        c = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
        return c
    def abs_dotProduct(self,c):
        if c < 0:
            return -c
        else:
            return c
    def crossProduct(self,a,b):
        cross = [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]
        return cross

    def length(self,c):
        abs = sqrt(pow(c[0],2) + pow(c[1],2) + pow(c[2],2))
        return abs

    def subtract(self,a,b):
        sub = [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
        return sub

    def add(self,a,b):
        sum = [a[0] + b[0], a[1] + b1[1], a[2] + b[2]]
        return sum

    def unit(self,c):
        length_c = self.length(c)
        unit_c = [c[0]/length_c, c[1]/length_c, c[2]/length_c]
        return unit_c

    def make_polygan(self,ee_xyz)
        for i in range(len(ee_xyz/3)):
            
