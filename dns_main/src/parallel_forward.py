#!/usr/bin/env python2
import time
from math import pi, cos, sin, atan2, acos, sqrt, pow, radians
import numpy as np

from service_router import *
from kinematics     import Kinematics
from locomotion     import *
from service_router import *


######
#a = 1
#rst_request(a)
#time.sleep(1)
K = Kinematics()
toggle_torque = True
torque(toggle_torque)
standUp()
time.sleep(1)
parallelGait(0, pi, -pi, 0, 0, 0)
time.sleep(2)
ee_xyz,servopos = np.array( K.doFkine(readPos()))
p1 =  ee_xyz[0:3]
p4 = ee_xyz[9:12]#np.around( ee_xyz[9:12])
p5 = ee_xyz[12:15]#np.around( ee_xyz[12:15])
p45 = p4-p5#np.around(p4-p5, decimals = 2)
p41 = p4-p1#np.around(p4-p1, decimals = 2)
normz = np.cross(p45,p41)
normz_rounded = np.around(normz)
print(normz_rounded)
length_normz = sqrt(pow(normz[0],2)+pow(normz[1],2)+pow(normz[2],2))
#unit_normz = np.around(pow(length_normz,-1)*normz)
#print(unit_normz)
beta = atan2(normz[0],normz[2])*180/pi
gamma = -atan2(normz[1],normz[2])*180/pi
print(beta)
print(gamma)
