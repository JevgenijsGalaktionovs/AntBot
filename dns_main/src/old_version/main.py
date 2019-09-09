import rospy
import time

from kinematics        import Kinematics
from dynamixel_library import *
from stupid_walk       import *
from walking_gaits     import *
from math              import pi,cos,sin,atan2,acos,sqrt,pow


def gait_with_keypresses():

    alpha = 0
    beta = 0
    gama = 0
    t=0
    initial_pos = [2048,2218,1024,
				   2048,1878,3048,
				   2048,2218,1024,
				   2048,1878,3048,
				   2048,2218,1024,
				   2048,1878,3048]
    velocity_list = [500, 500, 500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    acc_list =[500,500,500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    WriteRippleVel(velocity_list,1)
    WriteRippleAcc(acc_list,1)
    Write1Pos(1,2048)
    Write1Pos(2,2218)
    Write1Pos(3,1024)
    time.sleep(5)
    singleLeg(0,100,200,0,0,0,1)
    t1 = time.time()
    print(t-t1)
    for i in range(0,150):
        t2 = time.time()
        t = t2-t1
        K.PrintForward(t)
    time.sleep(2)
    # singleLeg(0,50,-50,0,0,0,1)
    # for i in range(0,100):
    #     K.PrintForward()

    # parallelGait(0,0,-10,0,0,0)
    # time.sleep(1)
    # gama = -10
    # ae = K.DoIKine(0,0,0,alpha,beta,gama,0)



if __name__=='__main__':
    try:
        CheckStatus()
        pwm_list =[500]*18        # Checks if all 18 servos are connected
        WritePWMLimit(pwm_list) # Modify PWM Limit (torque must be off)
        K = Kinematics()        # Creates Kinematics class object "K"
        EnableTorqueAllServos() # Enable Torque, duuh
        #W = WalkingGaits()

        gait_with_keypresses()  # tripod gait that expects keyboard press between steps
    except rospy.ROSInterruptException :
        portHandler.closePort()
