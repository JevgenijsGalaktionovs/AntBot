#!/usr/bin/env python2
from math import pi
import time
from service_router import *
from kinematics     import *
from locomotion     import *



riser = 170 #mm
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
time.sleep(5)
#a = K.doFkine(readPos())
#print(a)
half_step(0,35,20,0,0,0)
time.sleep(1)
parallelGait(0,0,0,0,0,20)
time.sleep(2)
tripodGait_stairs(20, True, False, False, 200, 160)
gama,beta = K.get_orientation()
time.sleep(1)
parallelGait(0,-beta,-gama,0,0,0)
time.sleep(1)
a = K.calc_translationStairs(riser)
print("a",a)
time.sleep(1)
parallelGait(0,0,0,0, a[1], a[0])
time.sleep(1)
checkContact()
continiousTripodTactile(0,30,20,2)
tripodGait_stairs(20, True, True, False, 200, 160)
time.sleep(2)
gama,beta = K.get_orientation()
time.sleep(1)
parallelGait(0,-beta,-gama,0,0,0)
time.sleep(1)
a = K.calc_translationStairs(riser)
print("a",a)
time.sleep(1)
parallelGait(0,0,0,0, a[1], a[0])
time.sleep(3)
tripodGait_stairs(20, False, False, False, 200, 160)
time.sleep(2)
tripodGait_stairs(20, True, True, False, 200, 160)
#time.sleep(2)
#checkContact()

##########################################################
#tripodGait_stairs(20, True, False, False, 180, 180)
#a = K.calc_translationStairs(riser)
#print("a",a)
#time.sleep(1)
#parallelGait(0,0,0,0, a[1], a[0])
#time.sleep(3)
#continiousTripodTactile(0,40,20,1)
#gama,beta = K.get_orientation()
#time.sleep(1)
#parallelGait(0,-beta,-gama,0,0,0)
#time.sleep(1)
#a = K.calc_translationStairs(riser)
#print("a",a)
#time.sleep(1)
#parallelGait(0,0,0,0, a[1], 30)
#time.sleep(3)
#parallelGait(0,0,0,0,30,0)
#time.sleep(3)
#continiousTripodTactile(0,40,20,1)
#tripodGait_stairs(20, True, False, False, 180, 100)
#time.sleep(1)
#tripodGait_stairs(20, False, True, False, 180, 100)

