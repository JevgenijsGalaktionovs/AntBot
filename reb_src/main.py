import rospy
import time

from kinematics        import Kinematics
from dynamixel_library import *
from stupid_walk       import *
from walking_gaits     import *
from math              import pi,cos,sin,atan2,acos,sqrt,pow


def gait_with_keypresses():


    stand_up()
    time.sleep(2)
    rotationz(-30)
    #getch()
    # y = int(input("How much do you want to move forward in mm pr step? "))
    # z = int(input("How much do you want to lift up the legs? "))
    # x = int(input("How much do you want to move sideways in mm pr step? "))
    # gama = int(input("How much do you want to rotate around x axis? "))
    # gama_rad = gama*pi/180
    # alpha = int(input("How much do you want to rotate around z axis? "))
    # alpha_rad = alpha*pi/180
    # beta = int(input("How much do you want to rotate around y axis? "))
    # beta_rad = beta*pi/180
    # dist_x = int(input("How much do you want to translate along x axis? "))
    # dist_y = int(input("How much do you want to translate along y axis? "))
    # dist_z = int(input("How much do you want to translate along z axis? "))

    #TripodGait(x,y,z)
    # parallelGait(alpha_rad,beta_rad,gama_rad, dist_x, dist_y, dist_z)
    #rippleStairs(x,y,z,1)
    #rippleStairs(0,0,-z,1)
    # rippleMirror(0,0,z,1)
    # time.sleep(1)
    # rippleMirror(x,y,0,1)
    # time.sleep(1)
    # rippleMirror(0,0,-z,2)
    # while(1):
    #     TripodGait(x,y,z)

if __name__=='__main__':
    try:
        CheckStatus()
        pwm_list =[250]*18        # Checks if all 18 servos are connected
        WritePWMLimit(pwm_list) # Modify PWM Limit (torque must be off)
        K = Kinematics()        # Creates Kinematics class object "K"
        EnableTorqueAllServos() # Enable Torque, duuh
        #W = WalkingGaits()

        gait_with_keypresses()  # tripod gait that expects keyboard press between steps
    except rospy.ROSInterruptException :
        portHandler.closePort()
