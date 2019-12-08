#!/usr/bin/env python2
from math import pi
import time
from service_router import *
from kinematics     import *
from locomotion     import *



riser = 164 #mm
depth = 344.746#mm
torque(0)
pwm_list = [885]*18
pwmAll(pwm_list)
scaler_acc = [50] * 18
scaler_vel = [20] * 18
velocityAll(scaler_vel)
accelerationAll(scaler_acc)
time.sleep(0.05)
torque(1)

standup_pos = [ 2048, 2048, 1296, 2048, 2048, 1296,
                2048, 2048, 1296, 2048,  2048, 1296,
                2048, 2048, 1296, 2048, 2048, 1296]
print(standup_pos)
front_standup = list_combine(leg[1] + leg[2], standup_pos)
rear_standup = list_combine(leg[5] + leg[6], standup_pos)
middle_standup = list_combine(leg[3] + leg[4], standup_pos)
positionN(front_standup)
time.sleep(1)
positionN(rear_standup)
time.sleep(1)
positionN(middle_standup)
time.sleep(3)
# parallelGait(0,0,23,0,0,0)




# half_step(0,60,20,0,0,0)
K = Kinematics()
# init_pos = [1,2048,2,2048,3,1024,4,2048,5,2048,6,1024,7,2048,8,2048,9,1024,10,2048,11,2048,12,1024,13,2048,14,2048,15,1024,16,2048,17,2048,18,1024]
# positionN(init_pos)#1144


# half_step(0,80,0,0,0,0)
# time.sleep(5)
# print("pos",readPos())
ee_xyz, servopos = K.doFkine(readPos())
print("fkine",ee_xyz)
# print("servo pos", servopos)
# K.printKinematics(readPos(),0,0,0)
# print("pos",readPos())



#parallelGait(0,0,27,0,0,0)
#a = K.step_to_rad(readPos())
#print(a) 
#tripodGait_stairs(True, 60, depth , riser)

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
##################tripodGait_stairs(True, 80 , depth, riser)
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
# parallelGait(0,0,0,100,100,0) #distance is 115 mm
# time.sleep(2)
# #a = K.calc_translationStairs(riser)
# #print("a",a)
# ##parallelGait(0,0,0,0, 0, a[0])##190
# #a = K.calc_translationStairs(riser)
# #print("a",a)

# #################testpolygon
# #checkContact()
#K.check_stabilty()
####################test adjustment
#K.calc_translationStairs(riser,1,0)
# gamma,beta = K.get_orientation([1,5,6])
# print(gamma,beta)