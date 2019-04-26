import time
import rospy

from kinematics        import *
from dynamixel_library import *
from stupid_walk       import *
from math import pi,cos,sin,atan2,acos,sqrt,pow




def gait_with_keypresses():

    stand_up()
    getch()
    alpha = int(input("How much do you want to rotate around y axis? "))
    alpha_rad = alpha*pi/180
    s = 141.33*alpha_rad
    print(s)
    z = s*cos(alpha_rad)
    x = s*sin(alpha_rad)
    y = 0
    beta = int(input("How much do you want to rotate around x axis? "))
    beta_rad = beta*pi/180
    j =  120.96*beta_rad
    z1 = j*cos(beta_rad)
    y1 = j*sin(beta_rad)
    x1 = 0


    while(1):

        my_list_roty = K.DoIKine(-x, y, z)
        my_list1_roty = K.DoIKine(x, y, -z)
        ae_roty = [int(i) for i in my_list_roty]
        ae1_roty = [int(i) for i in my_list1_roty]
        reb_list = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        WriteTripodProfVel(reb_list,1)
        WriteTripodProfAcc(reb_list,1)
        WriteTripodProfVel(reb_list,0)
        WriteTripodProfAcc(reb_list,0)
        WriteTripodRotationy(ae_roty,0)
        WriteTripodRotationy(ae1_roty,1)
        time.sleep(1)
        getch()
        my_list_rotx = K.DoIKine(x1, -y1, z1)
        my_list1_rotx = K.DoIKine(x1, y1, -z1)
        ae_rotx = [int(i) for i in my_list_rotx]
        ae1_rotx = [int(i) for i in my_list1_rotx]
        WriteTripodRotationx(ae_rotx,0)
        WriteTripodRotationx(ae1_rotx,1)
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        getch()
        stand_up()
        getch()


if __name__=='__main__':
    try:
        CheckStatus()           # Checks if all 18 servos are connected
        WritePWMLimit([250]*18) # Modify PWM Limit (torque must be off)
        K = Kinematics()        # Creates Kinematics class object "K"
        EnableTorqueAllServos() # Enable Torque, duuh


        gait_with_keypresses()  # tripod gait that expects keyboard press between steps
    except rospy.ROSInterruptException :
        portHandler.closePort()
