#!/usr/bin/env python2
from math import pi
import time
from service_router import *
from kinematics     import Kinematics
from locomotion     import *
from parallel_forward import *


riser = 100 #mm
depth = 254 #mm
#torque(0)
#a = K.step_to_rad(readPos())
#print(a)
time.sleep(0.1)
torque(1)
standUp()
time.sleep(2)
parallelGait(0, 10, -10, 0, 0, 0)
time.sleep(2)
#singleLeg(0, 50, 120, 0, 0, 0, 1)
get_orietation()



