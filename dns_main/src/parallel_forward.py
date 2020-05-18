#!/usr/bin/env python2
import time
from math            import pi, cos, sin, atan2, acos, sqrt, pow, radians
import numpy as np
import numpy.matlib
from service_router  import *
from kinematics      import Kinematics
from locomotion      import *
from service_router  import *


######
#a = 1
#rst_request(a)
#time.sleep(1)
K = Kinematics()
toggle_torque = True
torque(toggle_torque)
standUp()
time.sleep(1)
parallelGait(0, 0, 0, 0, 0, 50)
time.sleep(1)
ee_xyz,servopos = np.array( K.doFkine(readPos()))
y_axis_unit = np.array([0,1,0])
p1 =  ee_xyz[0:3]
p2 =  ee_xyz[3:6]
p3 =  ee_xyz[6:9]
p4 =  ee_xyz[9:12]#np.around( ee_xyz[9:12])
p5 =  ee_xyz[12:15]#np.around( ee_xyz[12:15])
p6 =  ee_xyz[15:18]
length_p1 =  sqrt(pow(p1[0],2)+pow(p1[1],2)+pow(p1[2],2))

p45 = p4-p5#np.around(p4-p5, decimals = 2)
p41 = p4-p1#np.around(p4-p1, decimals = 2)

p61 = p6-p1
length_p61 = sqrt(pow(p61[0],2)+pow(p61[1],2)+pow(p61[2],2))
p52 = p5-p2
length_p52 = sqrt(pow(p52[0],2)+pow(p52[1],2)+pow(p52[2],2))
p43 = p4-p3
length_p43 = sqrt(pow(p43[0],2)+pow(p43[1],2)+pow(p43[2],2))
normz = np.cross(p45,p41)
normz_rounded = np.around(normz)
#print(normz_rounded)
length_normz = sqrt(pow(normz[0],2)+pow(normz[1],2)+pow(normz[2],2))
#unit_normz = np.around(pow(length_normz,-1)*normz)
#print(unit_normz)
beta = atan2(normz[0],normz[2])*180/pi
gamma = -atan2(normz[1],normz[2])*180/pi
angle_p61_p52 = acos(np.dot(p61,p52)/(length_p61*length_p52))*180/pi
angle_p52_p43 = acos(np.dot(p52,p43)/(length_p52*length_p43))*180/pi
angle_p61_yaxis = -150 + acos(np.dot(y_axis_unit,p61)/(length_p61))*180/pi
#print(angle_p61_p52)
print(angle_p61_yaxis)
print(beta)
print(gamma)
