#!/usr/bin/env python2
import time
from math            import pi, cos, sin, atan2, acos, sqrt, pow, radians
import numpy as np
#import numpy.matlib
#from service_router  import *
from kinematics      import Kinematics
from locomotion      import *
from math_calc		 import *


######
#a = 1
#rst_request(a)
#time.sleep(1)
K = Kinematics()
M = Math_Calc()

def get_orietation():
	#ee_xyz,servopos = np.array( K.doFkine(readPos()))
	standup_pos = [2048, 2218, 1024,   2048, 1878, 3048,
                   2048, 2218, 1024,   2048, 1878, 3048,
                   2048, 2218, 1024,   2048, 1878, 3048]
	ee_xyz,servopos =  K.doFkine(standup_pos)		   
	y_axis_unit = [0,1,0]
	p1 =  ee_xyz[0:3]
	p2 =  ee_xyz[3:6]
	p3 =  ee_xyz[6:9]
	p4 =  ee_xyz[9:12]
	print("p4",p4)
	p5 =  ee_xyz[12:15]
	print("p5",p5)
	p6 =  ee_xyz[15:18]
	length_p1 = M.length(p1)
	print(length_p1)
	p45 = M.subtract(p4,p5)
	print("p45",p45)
	p41 = M.subtract(p4,p1)
	print("p41",p41)
	p61 = M.subtract(p6,p1)
	length_p61 = M.length(p61)
	p52 = M.subtract(p5,p2)
	length_p52 = M.length(p52)
	p43 = M.subtract(p4,p3)
	length_p43 = M.length(p43)
	normz = np.cross(p45,p41)
	normz1 = M.crossProduct(p45,p41)
	print(normz)
	print(normz1)

	#normz_rounded = np.around(normz)
	##print(normz_rounded)
	#length_normz = sqrt(pow(normz[0],2)+pow(normz[1],2)+pow(normz[2],2))
	##unit_normz = np.around(pow(length_normz,-1)*normz)
	##print(unit_normz)
	#beta = atan2(normz[0],normz[2])*180/pi
	#gamma = -atan2(normz[1],normz[2])*180/pi
	##print(beta)
	##print(gamma)
	##angle_p61_p52 = acos(np.dot(p61,p52)/(length_p61*length_p52))*180/pi
	##angle_p52_p43 = acos(np.dot(p52,p43)/(length_p52*length_p43))*180/pi
	##angle_p1_yaxis = acos(np.dot(p1, y_axis_unit)/(length_p1)*180/pi
	#return gamma, beta
get_orietation()