#!/usr/bin/env python2
import time
from math            import pi, cos, sin, atan2, acos, sqrt, pow, radians
#import numpy as np
#import numpy.matlib
#from service_router  import *
from kinematics      import Kinematics
from math_calc         import *
######
#a = 1
#rst_request(a)
#time.sleep(1)
K = Kinematics()
M = Math_Calc()
def get_orietation():
    ee_xyz,servopos = K.doFkine(readPos())
    #standup_pos = [2048, 2218, 1024,   2048, 1878, 3048,
   #               2048, 2218, 1024,   2048, 1878, 3048,
   #               2048, 2218, 1024,   2048, 1878, 3048]          
    y_axis_unit = [0,1,0]
    p1 =  ee_xyz[0:3]
    p2 =  ee_xyz[3:6]
    p3 =  ee_xyz[6:9]
    p4 =  ee_xyz[9:12]
    p5 =  ee_xyz[12:15]
    p6 =  ee_xyz[15:18]
    length_p1 = M.length(p1)
    p51 = M.subtract(p5,p1)
    p56 = M.subtract(p5,p6)
    p61 = M.subtract(p6,p1)
    length_p51 = M.length(p51)
    p52 = M.subtract(p5,p2)
    length_p56 = M.length(p56)
    p43 = M.subtract(p4,p3)
    length_p43 = M.length(p43)
    normz = M.crossProduct(p51,p56)
    unitz = M.unit(normz)
    print(normz)
    print(unitz)
    beta = atan2(normz[0],normz[2])*180/pi
    gamma = -atan2(normz[1],normz[2])*180/pi
    print("beta is this number",beta)
    print(gamma)
    return gamma, beta
