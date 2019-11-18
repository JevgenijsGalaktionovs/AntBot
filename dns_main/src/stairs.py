#!/usr/bin/env python2
from math import pi
import time
from service_router import *
from kinematics     import *
from locomotion     import *




riser = 170 #mm
depth = 264 #mm
#torque(0)
#pwm_list = [800]*18
#pwmAll(pwm_list)
#scaler_acc = [50] * 18
#scaler_vel = [20] * 18
#velocityAll(scaler_vel)
#accelerationAll(scaler_acc)
#time.sleep(0.1)
#torque(1)
#standUp()
#time.sleep(5)
parallelGait(0,0,-5,0,0,0)
a = K.step_to_rad(readPos())
print(a) 



#singleLeg_walk(50,0,0,0,0,0,6)
#time.sleep(2)
#checkContact()
#checkContact()
#a = K.doFkine(readPos())
#print ()
#K.printForward(readPos())
#singleLeg_walk(0,0,100,0,0,0,6)
#time.sleep(2)
#singleLeg_walk(0,0,-145,0,0,0,6)
#time.sleep(2)
#a = K.doFkine(readPos())
#K.printForward(readPos())
#singleLeg_walk(50,0,0,0,0,0,6)
#time.sleep(1)
##################333#checkContact()
###################tripodGait_stairs(True, 80 , depth, riser)
#time.sleep(1)
#checkContact()
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
#gama,beta = K.get_orientation([1,5,6])
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
# #tripodGait_stairs(20, False, True, False, 180, 100)


#######################################################
#parallelGait(0,0,-10,0,0,0) #distance is 115 mm
#a = K.calc_translationStairs(riser)
#print("a",a)
##parallelGait(0,0,0,0, 0, a[0])##190
#a = K.calc_translationStairs(riser)
#print("a",a)