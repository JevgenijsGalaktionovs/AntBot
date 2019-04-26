#!/usr/bin/env python

import rospy
from   sensor_msgs.msg   import Joy
from   dynamixel_library import *
from   kinematics        import *
from   stupid_walk       import *


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
    axes_inputs = 20*[0]
    toggle_torque = False
    a = []
    b = []
    old_pitch = 0
    old_roll = 0
    converted_pitch = 0
    converted_roll = 0
    new_newpitch = 0
    new_roll = 0
    my_list = []
    toggle = False
    toggle_roll = 0
    toggle_pitch = 0
    carry_pitch = 0
    carry_roll = 0

    CheckStatus()           # Checks if all 18 servos are connected
    WritePWMLimit([250]*18) # Modify PWM Limit (torque must be off)
    K = Kinematics()        # Creates Kinematics class object "K"
    EnableTorqueAllServos()
    stand_up()
    def __init__(self):
        self.ControllerNode()
    def callback(self,msg):
        self.button_inputs = msg.buttons
        self.axes_inputs = msg.axes
    def CreateEmptyMsgJoy(self):
        msg = Joy()
        msg.axes = [0.0]*20
        msg.buttons = [0.0]*17
        return msg

    def ButtonMapping(self):
        b = self.button_inputs
        a = self.axes_inputs

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

        elif b[8] :
            print("a is here")
            # if a[18] :
            #
            #         stand_up()
            #         self.old_pitch = 0
            #         self.pld_roll = 0
            # elif a[17] or a[16] :
            #         print("old pitch: ", self.old_pitch)
            #         print("old roll: ", self.old_roll)
            #         self.converted_pitch = a[17]
            #         self.converted_roll = a[16]
            #         #self.converted_pitch = self.converted_pitch*pi/180
            #         self.new_pitch = self.converted_pitch-self.old_pitch
            #         self.new_roll = self.converted_roll-self.old_roll
            #         if self.new_pitch > 0.03 or self.new_roll>0.01 :
            #             print("new pitch: ", self.new_pitch)
            #             print("new roll: ", self.new_roll)
            #             self.my_list = self.K.DoIKineRotationEuler(0, self.new_roll, self.new_pitch)
            #             ae = [int(i) for i in self.my_list]
            #             velocity_list = calc_Velocity(ae)
            #             WriteProfVel(velocity_list)
            #             WriteProfAcc(velocity_list)
            #             WriteAllPositions(ae)
            #             self.old_pitch = self.converted_pitch
            #             self.old_roll = self.converted_roll
            #         elif self.new_pitch < -0.03 or self.new_roll>-0.01 :
            #             print("new pitch: ", self.new_pitch)
            #             print("new roll: ", self.new_roll)
            #             self.my_list = self.K.DoIKineRotationEuler(0, self.new_roll, self.new_pitch)
            #             ae = [int(i) for i in self.my_list]
            #             velocity_list = calc_Velocity(ae)
            #             WriteProfVel(velocity_list)
            #             WriteProfAcc(velocity_list)
            #             WriteAllPositions(ae)
            #             self.old_pitch = self.converted_pitch
            #             self.old_roll = self.converted_roll
                    #print("servo angles: ", self.my_list)


#####increments###############################################


            if a[17]:
                self.new_pitch = a[17]
                pitch = self.new_pitch - self.old_pitch
                self.old_pitch = self.new_pitch
                if pitch > 0.03 :
                    self.toggle = True
                    self.toggle_pitch = 0.017*3
                    print("b+ is here")
                elif pitch < -0.03 :
                    self.toggle = True
                    self.toggle_pitch = -0.017*3
                    print("b- is here")
            elif a[16]:
                #print("c is here")
                self.new_roll = a[16]
                roll = self.new_roll - self.old_roll
                self.old_roll = self.new_roll
                if roll > 0.1 :
                    self.toggle = True
                    self.toggle_roll = 0.017*3
                elif roll < -0.1 :
                    self.toggle = True
                    self.toggle_roll = -0.017*3

        if self.toggle == True :
            print("d is here")
            self.carry_roll = self.carry_roll + self.toggle_roll
            self.carry_pitch = self.carry_pitch + self.toggle_pitch
            if self.carry_roll < 0 :
                self.carry_roll = self.carry_roll*-1
                #print("carry_roll: ", self.carry_roll)

            elif self.carry_pitch < 0 :
                self.carry_pitch = self.carry_pitch*-1
                #print("carry_pitch: ", self.carry_roll)
            elif self.carry_roll < 0.35 and self.carry_pitch < 0.35:
                self.my_list = self.K.DoIKineRotationEuler(0, self.toggle_roll, self.toggle_pitch)
                ae = [int(i) for i in self.my_list]
                WriteAllPositions(ae)
                print("cary roll",self.carry_roll)
                print("carry pitch",self.carry_pitch)
        if b[9]:
            stand_up()


                    # elif a[16] and a[17] :
                    #     self.new_pitch = a[17]
                    #     self.new_roll = a[16]
                    #     pitch = self.new_pitch - self.old_pitch
                    #     self.old_pitch = self.new_pitch
                    #     if pitch > 0.1 :
                    #         toggle_pitch_up = True
                    #     elif pitch < -0.1 :
                    #         self.toggle_pitch_down = True
                    #     roll = self.new_roll - self.old_roll
                    #     self.old_roll = self.new_roll
                    #     if roll > 0.1 :
                    #         self.toggle_roll_up = True
                    #     elif roll < -0.1 :
                    #         toggle_roll_down = True







        rospy.sleep(1)
        #rospy.sleep(0.01)

    def ControllerNode(self):
	rospy.init_node('Controller')
        while not rospy.is_shutdown():
            rospy.Subscriber('joy', Joy, self.callback, queue_size=3)
            self.pub = rospy.Publisher('joy', Joy,queue_size=1)
            self.ButtonMapping()

AntBot()
