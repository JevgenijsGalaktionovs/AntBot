#!/usr/bin/env python2
from math import pi
import time
from service_router import *
from kinematics     import Kinematics
from locomotion     import *
from parallel_forward import *


riser = 100 #mm
depth = 254 #mm
torque(0)
time.sleep(0.1)
torque(1)
standUp()
time.sleep(1)

rippleMirror(0, 25, 103, 0, 0, 0, 1)
time.sleep(1)
rippleMirror(0, 25, -3, 0, 0, 0, 1)
time.sleep(1)
gamma,beta = get_orietation()
time.sleep(1)
print(gamma,beta)
parallelGait(0, beta, gamma, 0, 0, 0)
time.sleep(1)

