#!/usr/bin/env python

import rospy
import os
from   sensor_msgs.msg   import Joy
from   dynamixel_library import *
#from   camera_neck       import CameraNeck
from   dynamics		     import *


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
PS3_BUTTON_REAR_LEFT_1      = 10
PS3_BUTTON_REAR_RIGHT_1     = 11
PS3_BUTTON_ACTION_TRIANGLE  = 12
PS3_BUTTON_ACTION_CIRCLE    = 13
PS3_BUTTON_ACTION_CROSS     = 14
PS3_BUTTON_ACTION_SQUARE    = 15
PS3_BUTTON_PAIRING          = 16

STEP_INCREMENT_MAX_LIMIT    = 5


if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class JoystickPS3:

    button_inputs =  17*[0] # Button presses
    toggle_condition = False
    step_increment = 1 #Debuggin feature
    #camera = CameraNeck()

    def __init__(self):
        self.listener()

    def callback(self,msg):
        self.button_inputs = msg.buttons

    def empty_msg_Joy(self):
        msg = Joy()
        msg.axes = [0.0]*20
        msg.buttons = [0.0]*17
        return msg

    def key_mapping(self):
        b = self.button_inputs

        if b[PS3_BUTTON_SELECT] == 1:
            if self.toggle_condition == False:
                EnableTorqueAllServos()
                self.toggle_condition = not self.toggle_condition
                rospy.sleep(0.3)
            else:
                DisableTorqueAllServos()
                self.toggle_condition = not self.toggle_condition
                rospy.sleep(0.3)
            self.pub.publish(self.empty_msg_Joy())

        elif b[PS3_BUTTON_START] == 1:
            RebootAllServos()
            self.toggle_condition = False
            self.pub.publish(self.empty_msg_Joy())
            rospy.sleep(0.5)

        elif b[PS3_BUTTON_ACTION_CROSS] == 1:
            if self.toggle_condition == True:
		#Place for WALK_FORWRD function
                self.pub.publish(self.empty_msg_Joy())
                rospy.sleep(0.2)
            else:
                print "Torque is not turned on! Cannot set PWM."
                print "See some magic,SMASH THE KEYBOARD!"
                getch()
                EnableTorqueAllServos()
                self.toggle_condition = not self.toggle_condition
                rospy.sleep(0.2)
        elif b[PS3_BUTTON_ACTION_CIRCLE] == 1:
            if self.toggle_condition == True:
                Standing()
                self.pub.publish(self.empty_msg_Joy())
                rospy.sleep(0.2)
            else:
                print "Torque is not turned on! Cannot set PWM."
                print "See some magic,SMASH THE KEYBOARD!"
                getch()
                EnableTorqueAllServos()
                self.toggle_condition = not self.toggle_condition
                rospy.sleep(0.2)

        elif b[PS3_BUTTON_REAR_RIGHT_2] == 1:
            self.step_increment += 1
	    #Open place
            print "Testing lag %d" % self.step_increment
            self.pub.publish(self.empty_msg_Joy())
            rospy.sleep(0.3)
        elif b[PS3_BUTTON_REAR_RIGHT_1] == 1:
	    #Open place
            self.step_increment -= 1
            print "Testing lag %d" % self.step_increment
            self.pub.publish(self.empty_msg_Joy())
            rospy.sleep(0.3)

        elif b[PS3_BUTTON_REAR_LEFT_2]:
            #Open place
            self.pub.publish(self.empty_msg_Joy())
            rospy.sleep(0.3)
        elif b[PS3_BUTTON_REAR_LEFT_1]:
	    self.camera.NeckStartPos()
            self.pub.publish(self.empty_msg_Joy())
            rospy.sleep(0.3)
	elif b[PS3_BUTTON_CROSS_RIGHT]:
	    self.camera.PanRight(1)
            self.pub.publish(self.empty_msg_Joy())
            rospy.sleep(0.3)
	elif b[PS3_BUTTON_CROSS_LEFT]:
	    self.camera.PanLeft(1)
            self.pub.publish(self.empty_msg_Joy())
            rospy.sleep(0.3)
	elif b[PS3_BUTTON_CROSS_UP]:
	    self.camera.TiltUp(1)
            self.pub.publish(self.empty_msg_Joy())
            rospy.sleep(0.3)
	elif b[PS3_BUTTON_CROSS_DOWN]:
	    self.camera.TiltDown(1)
            self.pub.publish(self.empty_msg_Joy())
            rospy.sleep(0.3)



        rospy.sleep(0.01)


    def listener(self):
	rospy.init_node('Controller')
        while not rospy.is_shutdown():
            rospy.Subscriber('joy', Joy, self.callback, queue_size=3)
            self.pub = rospy.Publisher('joy', Joy,queue_size=1)
            self.key_mapping()
