#!/usr/bin/env python

import rospy
from   dynamixel_library import *

toggle = 0

while 1:
    if toggle == 0:
        getch()
        EnableTorqueAllServos()
        toggle = 1
    else:
        getch()
        DisableTorqueAllServos()
        toggle = 0
