#!/usr/bin/env python2
from math import pi
import time
#from service_router import *
from kinematics     import Kinematics
from locomotion     import *
from parallel_forward import *


riser = 100 #mm
depth = 254 #mm
torque(0)
pwm_list = [800]*18
pwmAll(pwm_list)
scaler_acc = [50] * 18
scaler_vel = [20] * 18
velocityAll(scaler_vel)
accelerationAll(scaler_acc)
time.sleep(0.1)
torque(1)
standUp()
#a = K.step_to_rad(readPos())
#print(a)
time.sleep(2)
#parallelGait(0, 10, -10, 0, 0, 0)
#time.sleep(2)
#singleLeg(0, 50, 50, 0, 0, 0, 4)
#auto_calcTrajectory(0,0,150,1)
#singleLeg_stairs(0, 0, 120, 0, 0, 0, 2)
#get_orietation()
#tripodGait_stairs(20, 0, 0, 0, 180, 100)
continiousTripodTactile(0,40,40,3)
#tripodGait(0,25,20,2)
#time.sleep(2)
#checkContact()


