#!/usr/bin/env python2
from math import pi
import time
from service_router import *
from kinematics     import Kinematics
from locomotion     import *


riser = 100 #mm
depth = 254 #mm
for i in range(10):
    tripodGait(5, y, riser+3,1)
    time.sleep(0.1)
    gamma,beta = get_orietation()
    time.sleep(0.1)
    parallelGait(0, beta, gamma, 0, 0, 0)
    time.sleep(0.1)

