#!/usr/bin/env python

import rospy
import time

from kinematics        import *
from dynamixel_library import *
from stupid_walk       import *


def Gait1(my_list):
    Write1Pos(1,my_list[0])
    Write1Pos(2,my_list[1])
    Write1Pos(3,my_list[2])
    Write1Pos(10,my_list[9])
    Write1Pos(11,my_list[10])
    Write1Pos(12,my_list[11])
    Write1Pos(13,my_list[12])
    Write1Pos(14,my_list[13])
    Write1Pos(15,my_list[14])

def Gait2(my_list):
    Write1Pos(4,my_list[3])
    Write1Pos(5,my_list[4])
    Write1Pos(6,my_list[5])
    Write1Pos(7,my_list[6])
    Write1Pos(8,my_list[7])
    Write1Pos(9,my_list[8])
    Write1Pos(16,my_list[15])
    Write1Pos(17,my_list[16])
    Write1Pos(18,my_list[17])


if __name__=='__main__':
    try:
        DisableTorqueAllServos()
        time.sleep(3)
        EnableTorqueAllServos()
        stand_up()
        time.sleep(2)
		# PrintForward()
		#WALK()
        y = int(input("How much do you want to move forward in mm pr step? "))
        z=50#height
        x = int(input("How much do you want to move sideways in mm pr step? "))
        while(1):

            my_list = Inverse_kinematics(x/2,y/2,z)
            ae = [int(x) for x in my_list]
            Gait1(ae)
            my_list = Inverse_kinematics(x,y,-z)
            ae = [int(x) for x in my_list]
            Gait1(ae)

            my_list = Inverse_kinematics(x/2,y/2,z)
            ae = [int(x) for x in my_list]
            Gait2(ae)
            my_list = Inverse_kinematics(x,y,-z)
            ae = [int(x) for x in my_list]
            Gait2(ae)
            stand_up()
    except rospy.ROSInterruptException :
        portHandler.closePort()
