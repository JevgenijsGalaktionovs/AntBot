#!/usr/bin/env python

import rospy
from   control_interface import AntBot
from   dynamixel_library import *
import time
from kinematics import *


 	


if __name__=='__main__':
    try:
		DisableTorqueAllServos()
		time.sleep(3)
		EnableTorqueAllServos()
		alternative_stand_up()
		time.sleep(2)
		# PrintForward()
		#WALK()
		y = int(input("How much do you want to move forward in mm pr step? "))
		z=50#hight
		x = int(input("How much do you want to move sideways in mm pr step? "))
		while(1):
			Inverse_kinemat_gait1(x/2,y/2,z)
			Inverse_kinemat_gait1(x,y,-z)
			Inverse_kinemat_gait2(x/2,y/2,z)
			Inverse_kinemat_gait2(x,y,-z)
			stand_up()
    except rospy.ROSInterruptException :
        portHandler.closePort()
