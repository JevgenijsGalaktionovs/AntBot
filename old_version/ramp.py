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
    stand_up()
    time.sleep(3)
    parallelGait(0,0,0,0,50,0)
    time.sleep(2)
    parallelGait(0,0,0,0,15,0)
    time.sleep(5)
    # parallelGait(0,0,15,0,0,0)
    # time.sleep(3)
    # parallelGait(0,0,10,0,0,0)
    # time.sleep(3)
    init_pos = ReadAllPositions()
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    WaveGait(0,50,20,0,0,0,1)
    time.sleep(1)
    WriteAllPositions(init_pos)
    time.sleep(1)
    # WaveGait(0,50,20,0,0,0,2)
    # time.sleep(1)
    # WriteAllPositions(init_pos)
    # time.sleep(1)
    # WaveGait(0,50,20,0,0,0,2)
    # time.sleep(1)
    # WriteAllPositions(init_pos)
    # time.sleep(1)


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
