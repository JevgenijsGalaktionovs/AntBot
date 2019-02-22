#!/usr/bin/env python

import rospy
import cProfile   # Used to measure execution time. Use: cProfile.run('your_function_name')
import time
import random
# from   control_interface import AntBot
from   dynamixel_library import *# from kinematics import *
from stupid_walk import *





def imitatingKinematics():
	srv_pos = [0]*3
	for x in range(0,3):
		srv_pos[x] = random.randint(0,4096)
	return srv_pos

if __name__=='__main__':
    try:
		# while(1):
		# 	DisableTorqueAllServos()
		# 	time.sleep(2)
			# for x in range (1,19):
			# 	Write1VelocitLimit(x,200)
			# ReadAllVelocitylimits()
			#
			# for x in range (1,19):
			# 	# WritePWMLimit(x,885)
			# 	write4byte(x,108,32767)
			# 	write4byte(x,112,200)
			cProfile.run('ReadAllVelocitylimits()')

			# EnableTorqueAllServos()
			# alternative_stand_up()
			# time.sleep(3)
    except rospy.ROSInterruptException :
        portHandler.closePort()
