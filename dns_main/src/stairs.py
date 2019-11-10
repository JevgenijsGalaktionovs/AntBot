#!/usr/bin/env python2
from math import pi
import time
from service_router import *
from kinematics     import *
from locomotion     import *



riser = 100 #mm
depth = 254 #mm
torque(0)
pwm_list = [800]*18
pwmAll(pwm_list)
scaler_acc = [50] * 18
scaler_vel = [20] * 18
velocityAll(scaler_vel)
accelerationAll(scaler_acc)
#time.sleep(0.1)
torque(1)
standUp()
#a = K.step_to_rad(readPos())
#print(a)
time.sleep(2)
#parallelGait(0, 10, -10, 0, 0, 0)
#time.sleep(2)
#singleLeg(0, 50, 50, 0, 0, 0, 4)
#auto_calcTrajectory(0,0,150,1)
#singleLeg_stairs(0, 0, 120, 0, 0, 0, 1)
#get_orietation()
tripodGait_stairsFirst(20, 0, 0, 0, 180, 100)

#tripodGait(0,25,20,2)
#time.sleep(2)
#checkContact()
a = K.calc_translationStairs(riser)
print("a",a)
time.sleep(1)
parallelGait(0,0,0,0, a[1], -a[0])
time.sleep(3)
continiousTripodTactile(0,40,20,1)
gama,beta = K.get_orientation()
time.sleep(1)
parallelGait(0,0,0,0, a[1], -a[0])
time.sleep(3)
time.sleep(0.1)
parallelGait(0,-beta,-gama,0,0,0)
time.sleep(1)
a = K.calc_translationStairs(riser)
print("a",a)
time.sleep(1)
parallelGait(0,0,0,0, a[1], -a[0])
time.sleep(3)
parallelGait(0,0,0,0,20,0)
time.sleep(3)
tripodGait_stairsSecond(20, 0, 0, 0, 180, 100)

