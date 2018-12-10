#!/usr/bin/env python

import rospy
# import math
# from   kinematics        import *
#
# from   timeit            import default_timer as timer
# from   joystick_map_node import *
#from   camera_neck 	     import CameraNeck
from dynamixel_library import *

if __name__=='__main__': # equivalent to "int main" in c++
    try:
        RebootAllServos()
        DisableTorqueAllServos()
	 # JoystickPS3()

    except rospy.ROSInterruptException :
        DisableTorqueAllServos()
