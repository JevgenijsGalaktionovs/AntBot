#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

from sherlock_ants.msg import Dynamixel_array
from dynamixel_library import *


rospy.init_node('Servo_Information')

Servo1  = rospy.Publisher('Servo1', Dynamixel_array, queue_size=2)
Servo2  = rospy.Publisher('Servo2', Dynamixel_array, queue_size=2)
Servo3  = rospy.Publisher('Servo3', Dynamixel_array, queue_size=2)
Servo4  = rospy.Publisher('Servo4', Dynamixel_array, queue_size=2)
Servo5  = rospy.Publisher('Servo5', Dynamixel_array, queue_size=2)
Servo6  = rospy.Publisher('Servo6', Dynamixel_array, queue_size=2)
Servo7  = rospy.Publisher('Servo7', Dynamixel_array, queue_size=2)
Servo8  = rospy.Publisher('Servo8', Dynamixel_array, queue_size=2)
Servo9  = rospy.Publisher('Servo9', Dynamixel_array, queue_size=2)
Servo10 = rospy.Publisher('Servo10', Dynamixel_array, queue_size=2)
Servo11 = rospy.Publisher('Servo11', Dynamixel_array, queue_size=2)
Servo12 = rospy.Publisher('Servo12', Dynamixel_array, queue_size=2)
Servo13 = rospy.Publisher('Servo13', Dynamixel_array, queue_size=2)
Servo14 = rospy.Publisher('Servo14', Dynamixel_array, queue_size=2)
Servo15 = rospy.Publisher('Servo15', Dynamixel_array, queue_size=2)
Servo16 = rospy.Publisher('Servo16', Dynamixel_array, queue_size=2)
Servo17 = rospy.Publisher('Servo17', Dynamixel_array, queue_size=2)
Servo18 = rospy.Publisher('Servo18', Dynamixel_array, queue_size=2)

rate = rospy.Rate(3) # HZ

def BuildServoMessage(servo_id):
    msg = Dynamixel_array()
    msg.Servo_ID         = 0 #ReadID(servo_id)
    msg.Present_Position = ReadPosition(servo_id)
    msg.Present_Velocity = 0 #ReadVelocity(servo_id)
    msg.Present_PWM      = 0 #ReadPWM(servo_id)
    msg.Present_Load     = 0 #ReadLoad(servo_id)
    return msg

while not rospy.is_shutdown():

    Servo1.publish(BuildServoMessage(1))
    Servo2.publish(BuildServoMessage(2))
    Servo3.publish(BuildServoMessage(3))
    Servo4.publish(BuildServoMessage(4))
    Servo5.publish(BuildServoMessage(5))
    Servo6.publish(BuildServoMessage(6))
    Servo7.publish(BuildServoMessage(7))
    Servo8.publish(BuildServoMessage(8))
    Servo9.publish(BuildServoMessage(9))
    Servo10.publish(BuildServoMessage(10))
    Servo11.publish(BuildServoMessage(11))
    Servo12.publish(BuildServoMessage(12))
    Servo13.publish(BuildServoMessage(13))
    Servo14.publish(BuildServoMessage(14))
    Servo15.publish(BuildServoMessage(15))
    Servo16.publish(BuildServoMessage(16))
    Servo17.publish(BuildServoMessage(17))
    Servo18.publish(BuildServoMessage(18))
    rate.sleep()
