import rospy
import time

from kinematics        import Kinematics
from dynamixel_library import *
from stand_up          import *
from math              import pi,cos,sin,atan2,acos,sqrt,pow
from Tactiles          import *

K = Kinematics()
def TripodGait(x,y,z,alpha,beta,gama,iteration_num):
    initial_pos = ReadAllPositions()
    init_pos = [int(i) for i in initial_pos]
    for i in range(0,iteration_num):
        my_list = K.DoIKine(0,0,z,alpha,beta,gama,0)
        ae = [int(i) for i in my_list]
        my_listi = K.DoIKine(-x,-y,0,alpha,beta,gama,0)
        aa = [int(i) for i in my_listi]
        reb_list = calc_Velocity(ae)
        reb_listi = calc_Velocity(aa)
        WriteTripodGaitVel(reb_list,0)
        WriteTripodGaitAcc(reb_list,0)
        WriteTripodGaitVel(reb_listi,1)
        WriteTripodGaitAcc(reb_listi,1)
        WriteTripodGait(ae,0)
        WriteTripodGait(aa,1)
        time.sleep(0.3)


        my_list2 = K.DoIKine(0, 0, -z,alpha,beta,gama,0)
        ae2 = [int(i) for i in my_list2]
        my_listi2 = K.DoIKine(0, 0, 0,alpha,beta,gama,0)
        aa2 = [int(i) for i in my_listi2]
        reb_list2 = calc_Velocity(ae2)
        reb_listi2 = calc_Velocity(aa2)
        WriteTripodGaitVel(reb_list2,0)
        WriteTripodGaitAcc(reb_list2,0)
        WriteTripodGaitVel(reb_listi2,1)
        WriteTripodGaitAcc(reb_listi2,1)
        WriteTripodGait(ae2,0)
        WriteTripodGait(aa2,1)
        time.sleep(0.3)


        my_list3 = K.DoIKine(0,0,0,alpha,beta,gama,0)
        ae3 = [int(i) for i in my_list3]
        my_listi3 = K.DoIKine(x,y,z,alpha,beta,gama,0)
        aa3 = [int(i) for i in my_listi3]
        reb_list3 = calc_Velocity(ae3)
        reb_listi3 = calc_Velocity(aa3)
        WriteTripodGaitVel(reb_list3,0)
        WriteTripodGaitAcc(reb_list3,0)
        WriteTripodGaitVel(reb_listi3,1)
        WriteTripodGaitAcc(reb_listi3,1)
        WriteTripodGait(ae3,0)
        WriteTripodGait(aa3,1)
        time.sleep(0.3)

        my_list4 = K.DoIKine(0,0,0,alpha,beta,gama,0)
        ae4 = [int(i) for i in my_list4]
        my_listi4 = K.DoIKine(0,0,-z,alpha,beta,gama,0)
        aa4 = [int(i) for i in my_listi4]
        reb_list4 = calc_Velocity(ae4)
        reb_listi4 = calc_Velocity(aa4)
        WriteTripodGaitVel(reb_list4,0)
        WriteTripodGaitAcc(reb_list4,0)
        WriteTripodGaitVel(reb_listi4,1)
        WriteTripodGaitAcc(reb_listi4,1)
        WriteTripodGait(ae4,0)
        WriteTripodGait(aa4,1)
        time.sleep(0.3)

        WriteAllPositions(init_pos)
        time.sleep(1)

def RippleGait(x,y,z,alpha,beta,gama,iteration_num):
    initial_pos = ReadAllPositions()
    init_pos = [int(i) for i in initial_pos]
    for i in range(0,iteration_num):
        my_list1 = K.DoIKine(x,y,z,alpha,beta,gama,0)
        ae1 = [int(i) for i in my_list1]
        my_listi1 = K.DoIKine(-x/2,-y/2,0,alpha,beta,gama,0)
        aa1 = [int(i) for i in my_listi1]
        reb_list1 = calc_Velocity(ae1)
        reb_listi1 = calc_Velocity(aa1)
        WriteParallelVel(reb_list1,1)
        WriteParallelAcc(reb_list1,1)
        WriteParallelVel(reb_listi1,2)
        WriteParallelAcc(reb_listi1,2)
        WriteParallelVel(reb_listi1,3)
        WriteParallelAcc(reb_listi1,3)
        WriteParallelVel(reb_list1,4)
        WriteParallelAcc(reb_list1,4)
        WriteParallelVel(reb_listi1,5)
        WriteParallelAcc(reb_listi1,5)
        WriteParallelVel(reb_listi1,0)
        WriteParallelAcc(reb_listi1,0)
        WriteParallel(ae1,1)
        WriteParallel(aa1,2)
        WriteParallel(aa1,3)
        WriteParallel(ae1,4)
        WriteParallel(aa1,5)
        WriteParallel(aa1,0)
        time.sleep(1)
        my_list1 = K.DoIKine(0,0,-z,alpha,beta,gama,0)
        ae1 = [int(i) for i in my_list1]
        reb_list1 = calc_Velocity(ae1)
        WriteParallelVel(reb_list1,1)
        WriteParallelAcc(reb_list1,1)
        WriteParallelVel(reb_list1,4)
        WriteParallelAcc(reb_list1,4)
        WriteParallel(ae1,1)
        WriteParallel(ae1,4)
        time.sleep(1)
        print("1")

        my_list1 = K.DoIKine(x,y,z,alpha,beta,gama,0)
        ae1 = [int(i) for i in my_list1]
        my_listi1 = K.DoIKine(-x/2,-y/2,0,alpha,beta,gama,0)
        aa1 = [int(i) for i in my_listi1]
        reb_list1 = calc_Velocity(ae1)
        reb_listi1 = calc_Velocity(aa1)
        WriteParallelVel(reb_listi1,1)
        WriteParallelAcc(reb_listi1,1)
        WriteParallelVel(reb_listi1,2)
        WriteParallelAcc(reb_listi1,2)
        WriteParallelVel(reb_list1,3)
        WriteParallelAcc(reb_list1,3)
        WriteParallelVel(reb_listi1,4)
        WriteParallelAcc(reb_listi1,4)
        WriteParallelVel(reb_listi1,5)
        WriteParallelAcc(reb_listi1,5)
        WriteParallelVel(reb_list1,0)
        WriteParallelAcc(reb_list1,0)
        WriteParallel(aa1,1)
        WriteParallel(aa1,2)
        WriteParallel(ae1,3)
        WriteParallel(aa1,4)
        WriteParallel(aa1,5)
        WriteParallel(ae1,0)
        time.sleep(1)
        my_list1 = K.DoIKine(0,0,-z,alpha,beta,gama,0)
        ae1 = [int(i) for i in my_list1]
        reb_list1 = calc_Velocity(ae1)
        WriteParallelVel(reb_list1,3)
        WriteParallelAcc(reb_list1,3)
        WriteParallelVel(reb_list1,0)
        WriteParallelAcc(reb_list1,0)
        WriteParallel(ae1,3)
        WriteParallel(ae1,0)
        time.sleep(1)
        print("2")

        my_list1 = K.DoIKine(x,y,z,alpha,beta,gama,0)
        ae1 = [int(i) for i in my_list1]
        my_listi1 = K.DoIKine(-x/2,-y/2,0,alpha,beta,gama,0)
        aa1 = [int(i) for i in my_listi1]
        reb_list1 = calc_Velocity(ae1)
        reb_listi1 = calc_Velocity(aa1)
        WriteParallelVel(reb_listi1,1)
        WriteParallelAcc(reb_listi1,1)
        WriteParallelVel(reb_list1,2)
        WriteParallelAcc(reb_list1,2)
        WriteParallelVel(reb_listi1,3)
        WriteParallelAcc(reb_listi1,3)
        WriteParallelVel(reb_listi1,4)
        WriteParallelAcc(reb_listi1,4)
        WriteParallelVel(reb_list1,5)
        WriteParallelAcc(reb_list1,5)
        WriteParallelVel(reb_listi1,0)
        WriteParallelAcc(reb_listi1,0)
        WriteParallel(aa1,1)
        WriteParallel(ae1,2)
        WriteParallel(aa1,3)
        WriteParallel(aa1,4)
        WriteParallel(ae1,5)
        WriteParallel(aa1,0)
        time.sleep(1)
        my_list1 = K.DoIKine(0,0,-z,alpha,beta,gama,0)
        ae1 = [int(i) for i in my_list1]
        reb_list1 = calc_Velocity(ae1)
        WriteParallelVel(reb_list1,2)
        WriteParallelAcc(reb_list1,2)
        WriteParallelVel(reb_list1,5)
        WriteParallelAcc(reb_list1,5)
        WriteParallel(ae1,2)
        WriteParallel(ae1,5)
        time.sleep(1)
        print("3")
        WriteAllPositions(init_pos)
        time.sleep(1)




def WaveGait(x,y,z,alpha,beta,gama,iteration_num):
    initial_pos = ReadAllPositions()
    init_pos = [int(i) for i in initial_pos]
    for i in range(0,iteration_num):
        my_list1 = K.DoIKine(x,y,z,alpha,beta,gama,1)
        ae1 = [int(i) for i in my_list1]
        my_listi1 = K.DoIKine(-x/5,-y/5,0,alpha,beta,gama,0)
        aa1 = [int(i) for i in my_listi1]
        reb_list1 = calc_Velocity(ae1)
        reb_listi1 = calc_Velocity(aa1)
        WriteParallelVel(reb_list1,1)
        WriteParallelAcc(reb_list1,1)
        WriteParallelVel(reb_listi1,2)
        WriteParallelAcc(reb_listi1,2)
        WriteParallelVel(reb_listi1,3)
        WriteParallelAcc(reb_listi1,3)
        WriteParallelVel(reb_listi1,4)
        WriteParallelAcc(reb_listi1,4)
        WriteParallelVel(reb_listi1,5)
        WriteParallelAcc(reb_listi1,5)
        WriteParallelVel(reb_listi1,0)
        WriteParallelAcc(reb_listi1,0)
        WriteParallel(ae1,1)
        WriteParallel(aa1,2)
        WriteParallel(aa1,3)
        WriteParallel(aa1,4)
        WriteParallel(aa1,5)
        WriteParallel(aa1,0)
        time.sleep(1)
        print("1")

        my_listj2 = K.DoIKine(0,0,-z,alpha,beta,gama,1)
        ee2 = [int(i) for i in my_listj2]
        reb_listj2 = calc_Velocity(ee2)
        WriteParallelVel(reb_listj2,1)
        WriteParallelAcc(reb_listj2,1)
        WriteParallel(ee2,1)
        time.sleep(1)

        my_list2 = K.DoIKine(x,y,z,alpha,beta,gama,3)
        ae2 = [int(i) for i in my_list2]
        my_listi2 = K.DoIKine(-x/5,-y/5,0,alpha,beta,gama,0)
        aa2 = [int(i) for i in my_listi2]
        reb_list2 = calc_Velocity(ae2)
        reb_listi2 = calc_Velocity(aa2)
        WriteParallelVel(reb_listi2,1)
        WriteParallelAcc(reb_listi2,1)
        WriteParallelVel(reb_list2,3)
        WriteParallelAcc(reb_list2,3)
        WriteParallelVel(reb_listi2,5)
        WriteParallelAcc(reb_listi2,5)
        WriteParallelVel(reb_listi2,2)
        WriteParallelAcc(reb_listi2,2)
        WriteParallelVel(reb_listi2,4)
        WriteParallelAcc(reb_listi2,4)
        WriteParallelVel(reb_listi2,0)
        WriteParallelAcc(reb_listi2,0)
        WriteParallel(aa2,1)
        WriteParallel(ae2,3)
        WriteParallel(aa2,5)
        WriteParallel(aa2,2)
        WriteParallel(aa2,4)
        WriteParallel(aa2,0)
        time.sleep(1)
        #getch()
        print("2")
        my_listj2 = K.DoIKine(0,0,-z,alpha,beta,gama,3)
        ee2 = [int(i) for i in my_listj2]
        reb_listj2 = calc_Velocity(ee2)
        WriteParallelVel(reb_listj2,3)
        WriteParallelAcc(reb_listj2,3)
        WriteParallel(ee2,3)
        time.sleep(1)

        my_list2 = K.DoIKine(x,y,z,alpha,beta,gama,5)
        ae2 = [int(i) for i in my_list2]
        my_listi2 = K.DoIKine(-x/5,-y/5,0,alpha,beta,gama,0)
        aa2 = [int(i) for i in my_listi2]
        reb_list2 = calc_Velocity(ae2)
        reb_listi2 = calc_Velocity(aa2)
        WriteParallelVel(reb_listi2,1)
        WriteParallelAcc(reb_listi2,1)
        WriteParallelVel(reb_listi2,3)
        WriteParallelAcc(reb_listi2,3)
        WriteParallelVel(reb_list2,5)
        WriteParallelAcc(reb_list2,5)
        WriteParallelVel(reb_listi2,2)
        WriteParallelAcc(reb_listi2,2)
        WriteParallelVel(reb_listi2,4)
        WriteParallelAcc(reb_listi2,4)
        WriteParallelVel(reb_listi2,0)
        WriteParallelAcc(reb_listi2,0)
        WriteParallel(aa2,1)
        WriteParallel(aa2,3)
        WriteParallel(ae2,5)
        WriteParallel(aa2,2)
        WriteParallel(aa2,4)
        WriteParallel(aa2,0)
        time.sleep(1)
        #getch()
        print("3")
        my_listj2 = K.DoIKine(0,0,-z,alpha,beta,gama,5)
        ee2 = [int(i) for i in my_listj2]
        reb_listj2 = calc_Velocity(ee2)
        WriteParallelVel(reb_listj2,5)
        WriteParallelAcc(reb_listj2,5)
        WriteParallel(ee2,5)
        time.sleep(1)

        my_list2 = K.DoIKine(x,y,z,alpha,beta,gama,2)
        ae2 = [int(i) for i in my_list2]
        my_listi2 = K.DoIKine(-x/5,-y/5,0,alpha,beta,gama,0)
        aa2 = [int(i) for i in my_listi2]
        reb_list2 = calc_Velocity(ae2)
        reb_listi2 = calc_Velocity(aa2)
        WriteParallelVel(reb_listi2,1)
        WriteParallelAcc(reb_listi2,1)
        WriteParallelVel(reb_listi2,3)
        WriteParallelAcc(reb_listi2,3)
        WriteParallelVel(reb_listi2,5)
        WriteParallelAcc(reb_listi2,5)
        WriteParallelVel(reb_list2,2)
        WriteParallelAcc(reb_list2,2)
        WriteParallelVel(reb_listi2,4)
        WriteParallelAcc(reb_listi2,4)
        WriteParallelVel(reb_listi2,0)
        WriteParallelAcc(reb_listi2,0)
        WriteParallel(aa2,1)
        WriteParallel(aa2,3)
        WriteParallel(aa2,5)
        WriteParallel(ae2,2)
        WriteParallel(aa2,4)
        WriteParallel(aa2,0)
        time.sleep(1)
        #getch()
        print("4")
        my_listj2 = K.DoIKine(0,0,-z,alpha,beta,gama,2)
        ee2 = [int(i) for i in my_listj2]
        reb_listj2 = calc_Velocity(ee2)
        WriteParallelVel(reb_listj2,2)
        WriteParallelAcc(reb_listj2,2)
        WriteParallel(ee2,2)
        time.sleep(1)



        my_list2 = K.DoIKine(x,y,z,alpha,beta,gama,4)
        ae2 = [int(i) for i in my_list2]
        my_listi2 = K.DoIKine(-x/5,-y/5,0,alpha,beta,gama,0)
        aa2 = [int(i) for i in my_listi2]
        reb_list2 = calc_Velocity(ae2)
        reb_listi2 = calc_Velocity(aa2)
        WriteParallelVel(reb_listi2,1)
        WriteParallelAcc(reb_listi2,1)
        WriteParallelVel(reb_listi2,3)
        WriteParallelAcc(reb_listi2,3)
        WriteParallelVel(reb_listi2,5)
        WriteParallelAcc(reb_listi2,5)
        WriteParallelVel(reb_listi2,2)
        WriteParallelAcc(reb_listi2,2)
        WriteParallelVel(reb_list2,4)
        WriteParallelAcc(reb_list2,4)
        WriteParallelVel(reb_listi2,0)
        WriteParallelAcc(reb_listi2,0)
        WriteParallel(aa2,1)
        WriteParallel(aa2,3)
        WriteParallel(aa2,5)
        WriteParallel(aa2,2)
        WriteParallel(ae2,4)
        WriteParallel(aa2,0)
        time.sleep(1)
        #getch()
        print("5")
        my_listj2 = K.DoIKine(0,0,-z,alpha,beta,gama,4)
        ee2 = [int(i) for i in my_listj2]
        reb_listj2 = calc_Velocity(ee2)
        WriteParallelVel(reb_listj2,4)
        WriteParallelAcc(reb_listj2,4)
        WriteParallel(ee2,4)
        time.sleep(1)


        my_list2 = K.DoIKine(x,y,z,alpha,beta,gama,6)
        ae2 = [int(i) for i in my_list2]
        my_listi2 = K.DoIKine(-x/5,-y/5,0,alpha,beta,gama,0)
        aa2 = [int(i) for i in my_listi2]
        reb_list2 = calc_Velocity(ae2)
        reb_listi2 = calc_Velocity(aa2)
        WriteParallelVel(reb_listi2,1)
        WriteParallelAcc(reb_listi2,1)
        WriteParallelVel(reb_listi2,3)
        WriteParallelAcc(reb_listi2,3)
        WriteParallelVel(reb_listi2,5)
        WriteParallelAcc(reb_listi2,5)
        WriteParallelVel(reb_listi2,2)
        WriteParallelAcc(reb_listi2,2)
        WriteParallelVel(reb_listi2,4)
        WriteParallelAcc(reb_listi2,4)
        WriteParallelVel(reb_list2,0)
        WriteParallelAcc(reb_list2,0)
        WriteParallel(aa2,1)
        WriteParallel(aa2,3)
        WriteParallel(aa2,5)
        WriteParallel(aa2,2)
        WriteParallel(aa2,4)
        WriteParallel(ae2,0)
        time.sleep(1)
        #getch()
        print("6")
        my_listj2 = K.DoIKine(0,0,-z,alpha,beta,gama,6)
        ee2 = [int(i) for i in my_listj2]
        reb_listj2 = calc_Velocity(ee2)
        WriteParallelVel(reb_listj2,0)
        WriteParallelAcc(reb_listj2,0)
        WriteParallel(ee2,0)
        time.sleep(1)


        WriteAllPositions(init_pos)
        time.sleep(1)

def rotationz(degrees):
    temp_stand_up = ReadAllPositions()
    alpha_rad = degrees*pi/180
    my_list = K.DoIKine(0,0,20,alpha,beta,gama,0)
    ae = [int(i) for i in my_list]
    WriteTripodGait(ae,0)
    time.sleep(0.5)
    my_listx = K.DoIKineRotationEuler(alpha_rad, 0, 0)
    xx = [int(i) for i in my_listx]
    WriteTripodGait(xx,1)
    time.sleep(1)
    my_list = K.DoIKine(0,0,-20,alpha,beta,gama,0)
    ae = [int(i) for i in my_list]
    WriteTripodGait(ae,0)
    time.sleep(1)
    my_list = K.DoIKine(0,0,20,alpha,beta,gama,0)
    ae = [int(i) for i in my_list]
    WriteTripodGait(ae,1)
    time.sleep(1)
    Write1Pos(1,2048)
    Write1Pos(10,2048)
    Write1Pos(13,2048)
    time.sleep(1)
    WriteTripodGait(temp_stand_up,1)


def rippleMirror(x,y,z,alpha,beta,gama,leg_case):
        ee_xyz = K.DoFKine()
        if leg_case == 1:
            my_list = K.DoIKine(x,y,z,alpha,beta,gama,1)
            ae = [int(i) for i in my_list]
            my_listi = K.DoIKine(-x,y,z,alpha,beta,gama,2)
            aa = [int(i) for i in my_listi]
            velocity_list = calc_Velocity(aa)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,1)
            WriteParallel(aa,2)
        elif leg_case == 2:
            my_list = K.DoIKine(x,y,z,alpha,beta,gama,3)
            ae = [int(i) for i in my_list]
            my_listi = K.DoIKine(-x,y,z,alpha,beta,gama,4)
            aa = [int(i) for i in my_listi]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,3)
            WriteParallel(aa,4)
        else:
            my_list = K.DoIKine(x,y,z, alpha,beta,gama,5)
            ae = [int(i) for i in my_list]
            my_listi = K.DoIKine(-x,y,z,alpha,beta,gama,6)
            aa = [int(i) for i in my_listi]
            velocity_list = calc_Velocity(aa)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,5)
            WriteParallel(aa,0)

def parallelGait(alpha, beta, gama, dist_x, dist_y, dist_z):
        alpha_rad = alpha*pi/180
        beta_rad = beta*pi/180
        gama_rad = gama*pi/180
        my_listx = K.DoIKineRotationEuler(alpha_rad, beta_rad, gama_rad)
        xx = [int(i) for i in my_listx]
        listx = [10, 50, 50, 10, 50, 50, 10, 50, 50, 10, 50, 50, 10, 50, 50, 10, 50, 50]
        WriteTripodGaitVel(listx,1)
        WriteTripodGaitAcc(listx,1)
        WriteTripodGaitVel(listx,0)
        WriteTripodGaitAcc(listx,0)
        WriteAllPositions(xx)
        time.sleep(2)
        my_valx = K.DoIKine(-dist_x, -dist_y, -dist_z,0,0,0,0)
        ae_valx = [int(i) for i in my_valx]
        WriteAllPositions(ae_valx)
def singleLeg(x,y,z,alpha,beta,gama,leg_case):
        ee_xyz = K.DoFKine()
        if leg_case == 1:
            my_list = K.DoIKine(x,y,z,alpha,beta,gama,1)
            ae = [int(i) for i in my_list]
            velocity_list =[127*60/639, 50, 194*50/639, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            acc_list =[127*500/639, 500, 194*500/639, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(acc_list,leg_case)
            WriteParallel(ae,1)
        elif leg_case == 2:
            my_list = K.DoIKine(-x,y,z,alpha,beta,gama,2)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,2)
        elif leg_case == 3:
            my_list = K.DoIKine(x,y,z,alpha,beta,gama,3)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,3)
        elif leg_case == 4:
            my_list = K.DoIKine(-x,y,z,alpha,beta,gama,4)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,4)
        elif leg_case == 5:
            my_list = K.DoIKine(x,y,z,alpha,beta,gama,5)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,5)
        else:
            my_list = K.DoIKine(-x,y,z,alpha,beta,gama,6)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,0)

def put_down(alpha,beta,gama,leg_case):
    j = int(leg_case-1)
    for x in range(40):
        tac = allTactiles()
        tac_oneleg = tac[j]
        if tac_oneleg == 0:
            ae = K.doIKine(0,0,-5,alpha,beta,gama,leg_case)
            steps = [int(i) for i in ae]
            Write1Pos(3*j+2,steps[3*j+1])
            Write1Pos(3*j+3,steps[3*j+2])
            time.sleep(0.3)
        else:
            return
