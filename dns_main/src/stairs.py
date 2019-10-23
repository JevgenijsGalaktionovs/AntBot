#!/usr/bin/env python2
from math import pi
import time
from service_router import *
from kinematics     import Kinematics
from locomotion     import *


riser = 100 #mm
depth = 254 #mm
tripodGait(5, y, riser+3, 10)
gamma,beta = get_orietation()
parallelGait()

