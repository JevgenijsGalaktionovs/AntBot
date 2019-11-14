#!/usr/bin/env python2
import rospy
from service_router import *
from locomotion import *

if __name__ == '__main__':
    try:
        torque(1)
        standUp()
    except rospy.ROSInterruptException:
        SystemExit
