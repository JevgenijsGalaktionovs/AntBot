#!/usr/bin/env python

import rospy
import time

from kinematics        import Kinematics
from dynamixel_library import *
from stupid_walk       import *

def gait_with_keypresses():

    stand_up()
    y = int(input("How much do you want to move forward in mm pr step? "))
    z=20#height
    x = int(input("How much do you want to move sideways in mm pr step? "))

    while(1):
        my_list = K.DoIKine(x/2,y/2,z)
        ae = [int(i) for i in my_list]
        WriteTripodGait(ae,1)
        time.sleep(0.3)
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        getch()
        my_list2 = K.DoIKine(x,y,-z)
        ae2 = [int(i) for i in my_list2]
        WriteTripodGait(ae2,1)
        time.sleep(0.3)
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        getch()
        my_list3 = K.DoIKine(x/2,y/2,z)
        ae3 = [int(i) for i in my_list3]
        WriteTripodGait(ae3,0)
        time.sleep(0.3)
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        getch()
        my_list4 = K.DoIKine(x,y,-z)
        ae4 = [int(i) for i in my_list4]
        WriteTripodGait(ae4,0)
        time.sleep(0.3)
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        getch()
        stand_up()
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        time.sleep(0.3)

if __name__=='__main__':
    try:
        CheckStatus()           # Checks if all 18 servos are connected
        WritePWMLimit([250]*18) # Modify PWM Limit (torque must be off)
        K = Kinematics()        # Creates Kinematics class object "K"
        EnableTorqueAllServos() # Enable Torque, duuh

        gait_with_keypresses()  # tripod gait that expects keyboard press between steps
    except rospy.ROSInterruptException :
        portHandler.closePort()
