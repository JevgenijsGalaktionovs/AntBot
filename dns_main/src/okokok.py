#!/usr/bin/env python2
import time
from math import radians
from service_router import *
from locomotion     import *
from math import asin, pi, atan2
from testing import *
#, positionN, \
#    velocityAll, accelerationAll, positionAll, readFSR
from kinematics import Kinematics

from math_calc import vector_length
K=Kinematics()


torque(0)
pwm_list = [800]*18
pwmAll(pwm_list)
scaler_acc = [20] * 18
scaler_vel = [20] * 18
velocityAll(scaler_vel)
accelerationAll(scaler_acc)
torque(1)
standUpForStairs()
time.sleep(1)
threshold = 50
stepSize = 50
riser = 140
thread = 340

def correct_me(z):
    print("please kill me")
    Up          =   [0, 0,  z]
    LiftUp      =   calc_motion(Up)
    pos = list()
    pos.extend(LiftUp[12:18])
    pos.extend(LiftUp[18:24])
    positionN(pos)
    leg_case = [3,4]
    check_position_error_legs(80, 20, pos, leg_case)
    ServoCentering=[7,2048,10,2048]
    positionN(ServoCentering)
    time.sleep(1)

correct_me(40)