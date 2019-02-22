#!/usr/bin/env python

import rospy
import cProfile   # Used to measure execution time. Use: cProfile.run('your_function_name')
import time
import random
# from   control_interface import AntBot
from   dynamixel_library import *# from kinematics import *
from stupid_walk import *


if __name__=='__main__':
    try:
		EnableTorqueAllServos()
		stand_up()
		time.sleep(2)
		PrintForward()
		#WALK()

		Inverse_kinemat(0,80,0)
		Inverse_kinemat(0,-80,0)
		Inverse_kinemat(0,-80,0)
		Inverse_kinemat(0,80,0)
		Inverse_kinemat(0,80,0)
		Inverse_kinemat(0,-80,0)

		Inverse_kinemat(0,0,80)
		Inverse_kinemat(0,0,-80)
		Inverse_kinemat(0,0,-80)
		Inverse_kinemat(0,0,80)
		Inverse_kinemat(0,0,80)
		Inverse_kinemat(0,0,-80)

		Inverse_kinemat(30,0,0)
		Inverse_kinemat(-30,0,0)
		Inverse_kinemat(-30,0,0)
		Inverse_kinemat(30,0,0)
		Inverse_kinemat(30,0,0)
		Inverse_kinemat(-30,0,0)

    except rospy.ROSInterruptException :
        portHandler.closePort()
