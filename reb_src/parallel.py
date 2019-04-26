import time
import rospy
from kinematics        import *
from dynamixel_library import *
from stupid_walk       import *
from math              import pi,cos,sin,atan2,acos,sqrt,pow
#from control_interface import *




K = Kinematics()

def parallelGait(alpha_rad, beta_rad, gama_rad, dist_x, dist_y, dist_z):
    print("im here:")
    my_listx = K.DoIKineRotationEuler(alpha_rad, beta_rad, gama_rad)
    my_reb_valx = K.DoIKine(-dist_x, -dist_y, -dist_z,6)
    xx = [int(i) for i in my_listx]
    print(xx)
    ae_reb_valx = [int(i) for i in my_reb_valx]
    velocity_list = [10, 50, 50, 10, 50, 50, 10, 50, 50, 10, 50, 50, 10, 50, 50, 10, 50, 50]
    WriteTripodGaitVel(velocity_list,1)
    WriteTripodGaitAcc(velocity_list,1)
    WriteTripodGaitVel(velocity_list,0)
    WriteTripodGaitAcc(velocity_list,0)
    WriteAllPositions(xx)
    WriteAllPositions(ae_reb_valx)
    print("im here:")

    # getch()
    # my_list_rotx = K.DoIKine(x1, -y1, z1)
    # my_list1_rotx = K.DoIKine(x1, y1, -z1)
    # ae_rotx = [int(i) for i in my_list_rotx]
    # ae1_rotx = [int(i) for i in my_list1_rotx]
    # WriteTripodRotationx(ae_rotx,0)
    # WriteTripodRotationx(ae1_rotx,1)
    # K.DoBothKinematicsAndPrint(0,0,0)
    # print ReadAllPositions()
    # getch()
    # stand_up()
    # getch()
