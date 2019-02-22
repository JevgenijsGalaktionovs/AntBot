#!/usr/bin/env python

import rospy
from   control_interface import AntBot
from   dynamixel_library import *
import time
from kinematics import *


def stand_up():

    # First Tripod
    #Leg 1
	Write1Pos(1,2048)
	Write1Pos(2,2448)
	Write1Pos(3,1024)

    #Leg 4
	Write1Pos(10,2048)
	Write1Pos(11,1648)
	Write1Pos(12,3072)

    #Leg 5
	Write1Pos(13,2048)
	Write1Pos(14,2448)
	Write1Pos(15,1024)


    # Second Tripod
    #Leg 2
	Write1Pos(4,2048)
	Write1Pos(5,1648)
	Write1Pos(6,3072)

    #Leg 3
	Write1Pos(7,2048)
	Write1Pos(8,2448)
	Write1Pos(9,1024)

    #Leg 6
	Write1Pos(16,2048)
	Write1Pos(17,1648)
	Write1Pos(18,3072)


if __name__=='__main__':
    try:
		EnableTorqueAllServos()
		stand_up()
		time.sleep(2)
		PrintForward()
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
