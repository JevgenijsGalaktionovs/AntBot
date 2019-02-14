#!/usr/bin/env python

import rospy
from   sensor_msgs.msg   import Joy
from   dynamixel_library import *

PS3_BUTTON_SELECT           =  0
PS3_BUTTON_STICK_LEFT       =  1
PS3_BUTTON_STICK_RIGHT      =  2
PS3_BUTTON_START            =  3
PS3_BUTTON_CROSS_UP         =  4
PS3_BUTTON_CROSS_RIGHT      =  5
PS3_BUTTON_CROSS_DOWN       =  6
PS3_BUTTON_CROSS_LEFT       =  7
PS3_BUTTON_REAR_LEFT_2      =  8
PS3_BUTTON_REAR_RIGHT_2     =  9
PS3_BUTTON_REAR_LEFT_1      =  10
PS3_BUTTON_REAR_RIGHT_1     =  11
PS3_BUTTON_ACTION_TRIANGLE  =  12
PS3_BUTTON_ACTION_CIRCLE    =  13
PS3_BUTTON_ACTION_CROSS     =  14
PS3_BUTTON_ACTION_SQUARE    =  15
PS3_BUTTON_PAIRING          =  16

class AntBot:

    button_inputs =  17*[0] # Button presses
    toggle_torque = False

    def __init__(self):
        self.ControllerNode()
    def callback(self,msg):
        self.button_inputs = msg.buttons
    def CreateEmptyMsgJoy(self):
        msg = Joy()
        msg.axes = [0.0]*20
        msg.buttons = [0.0]*17
        return msg

    def ButtonMapping(self):
        b = self.button_inputs

######################################
#######    General control     #######
######################################
        if b[PS3_BUTTON_SELECT]:
            if self.toggle_torque == False:
                EnableTorqueAllServos()
                self.toggle_torque = not self.toggle_torque
                rospy.sleep(0.3)
            else:
                DisableTorqueAllServos()
                self.toggle_torque = not self.toggle_torque
                rospy.sleep(0.3)
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_START]:
            RebootAllServos()
            self.toggle_torque = False
            self.pub.publish(self.CreateEmptyMsgJoy())
            rospy.sleep(0.5)
        elif b[PS3_BUTTON_PAIRING]:
            quit()

######################################
#######     Motion control     #######
######################################
        elif b[PS3_BUTTON_ACTION_SQUARE]:
            if self.toggle_torque == True:
                self.pub.publish(self.CreateEmptyMsgJoy())
                rospy.sleep(0.2)
            else:
                print "Torque is not turned on! Cannot set PWM."
                print "Press any button to turn torque on!"
                getch()
                EnableTorqueAllServos()
                self.toggle_torque = not self.toggle_torque
                rospy.sleep(0.2)
        elif b[PS3_BUTTON_ACTION_CROSS]:
            if self.toggle_torque == True:
                self.pub.publish(self.CreateEmptyMsgJoy())
                rospy.sleep(0.2)
            else:
                print "Torque is not turned on! Cannot set PWM."
                print "Press any button to turn torque on!"
                getch()
                EnableTorqueAllServos()
                self.toggle_torque = not self.toggle_torque
                rospy.sleep(0.2)
        elif b[PS3_BUTTON_ACTION_CIRCLE]:
            if self.toggle_torque == True:
                self.pub.publish(self.CreateEmptyMsgJoy())
                rospy.sleep(0.2)
            else:
                print "Torque is not turned on! Cannot set PWM."
                print "Press any button to turn torque on!"
                getch()
                EnableTorqueAllServos()
                self.toggle_torque = not self.toggle_torque
                rospy.sleep(0.2)

        rospy.sleep(0.01)

    def ControllerNode(self):
	rospy.init_node('Controller')
        while not rospy.is_shutdown():
            rospy.Subscriber('joy', Joy, self.callback, queue_size=3)
            self.pub = rospy.Publisher('joy', Joy,queue_size=1)
            self.ButtonMapping()
