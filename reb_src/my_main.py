import rospy
import time

from kinematics        import Kinematics
from dynamixel_library import *
from stupid_walk       import *
from trajectory        import *

def gait_with_keypresses():
    stand_up()
    time.sleep(3)
    ee_xyz = [0,0,0]
    #ee_xyz_init = [0,0,0]
    for i in range(0,21):
        print(i)
        ee_xyz_init = ee_xyz
        x_init = ee_xyz_init[0]
        y_init = ee_xyz_init[1]
        z_init = ee_xyz_init[2]
        print("rounded_init :",ee_xyz_init)
        ee_xyz = T.calc_Parabola(0,60,40,i)
        rounded = [round(i,4) for i in ee_xyz]
        x = round(rounded[0] - x_init,4)
        y = round(rounded[1] - y_init,4)
        z = round(rounded[2] - z_init,4)
        print("rounded", [x,y,z])
        my_list = K.DoIKine(x,y,z)
        #print("ikine coordinates: ",my_list)
        ae = [int(i) for i in my_list]
        aa = calc_Velocity(ae)
        WriteProfVel(aa)
        WriteProfAcc(aa)
        #WriteTripodGait(ae,1)
        WriteTripodGait(ae,0)
        time.sleep(1)





if __name__=='__main__':
    try:
        CheckStatus()           # Checks if all 18 servos are connected
        WritePWMLimit([500]*18) # Modify PWM Limit (torque must be off)
        K = Kinematics()
        T = trajectoryPlanning()      # Creates Kinematics class object "K"
        EnableTorqueAllServos() # Enable Torque, duuh


        gait_with_keypresses()  # tripod gait that expects keyboard press between steps
    except rospy.ROSInterruptException :
        portHandler.closePort()
