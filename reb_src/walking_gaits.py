import rospy
import time

from kinematics        import Kinematics
from dynamixel_library import *
from stupid_walk       import *
from math              import pi,cos,sin,atan2,acos,sqrt,pow


#def gait_with_keypresses():

#class WalkingGaits(object):

K = Kinematics()
def TripodGait(x,y,z,iteration_num):
    initial_pos = ReadAllPositions()
    init_pos = [int(i) for i in initial_pos]
    for i in range(0,iteration_num):
        my_list = K.DoIKine(0,0,z,6)
        ae = [int(i) for i in my_list]
        my_listi = K.DoIKine(-x,-y,0,6)
        aa = [int(i) for i in my_listi]
        reb_list = calc_Velocity(ae)
        reb_listi = calc_Velocity(aa)
        WriteTripodGaitVel(reb_list,1)
        WriteTripodGaitAcc(reb_list,1)
        WriteTripodGaitVel(reb_listi,0)
        WriteTripodGaitAcc(reb_listi,0)
        WriteTripodGait(ae,1)
        WriteTripodGait(aa,0)
        time.sleep(0.3)
        #K.DoBothKinematicsAndPrint(0,0,0)
        #print ReadAllPositions()
        #getch()


        my_list2 = K.DoIKine(0, 0, -z,6)
        ae2 = [int(i) for i in my_list2]
        my_listi2 = K.DoIKine(0, 0, 0,6)
        aa2 = [int(i) for i in my_listi2]
        reb_list2 = calc_Velocity(ae2)
        reb_listi2 = calc_Velocity(aa2)
        WriteTripodGaitVel(reb_list2,1)
        WriteTripodGaitAcc(reb_list2,1)
        WriteTripodGaitVel(reb_listi2,0)
        WriteTripodGaitAcc(reb_listi2,0)
        WriteTripodGait(ae2,1)
        WriteTripodGait(aa2,0)
        time.sleep(0.3)
        # K.DoBothKinematicsAndPrint(0,0,0)
        # print ReadAllPositions()
        #getch()


        my_list3 = K.DoIKine(0,0,0,6)
        ae3 = [int(i) for i in my_list3]
        my_listi3 = K.DoIKine(x,y,z,6)
        aa3 = [int(i) for i in my_listi3]
        reb_list3 = calc_Velocity(ae3)
        reb_listi3 = calc_Velocity(aa3)
        WriteTripodGaitVel(reb_list3,1)
        WriteTripodGaitAcc(reb_list3,1)
        WriteTripodGaitVel(reb_listi3,0)
        WriteTripodGaitAcc(reb_listi3,0)
        WriteTripodGait(ae3,1)
        WriteTripodGait(aa3,0)
        time.sleep(0.3)
        #getch()


        my_list4 = K.DoIKine(0,0,0,6)
        ae4 = [int(i) for i in my_list4]
        my_listi4 = K.DoIKine(0,0,-z,6)
        aa4 = [int(i) for i in my_listi4]
        reb_list4 = calc_Velocity(ae4)
        reb_listi4 = calc_Velocity(aa4)
        WriteTripodGaitVel(reb_list4,1)
        WriteTripodGaitAcc(reb_list4,1)
        WriteTripodGaitVel(reb_listi4,0)
        WriteTripodGaitAcc(reb_listi4,0)
        WriteTripodGait(ae4,1)
        WriteTripodGait(aa4,0)
        time.sleep(0.3)
        #getch()

        WriteAllPositions(init_pos)
        time.sleep(1)
        # K.DoBothKinematicsAndPrint(0,0,0)
        # print ReadAllPositions()
        # time.sleep(1)

def WaveGait(x,y,z,iteration_num):
    initial_pos = ReadAllPositions()
    init_pos = [int(i) for i in initial_pos]
    for i in range(0,iteration_num):
        my_list1 = K.DoIKine(x,y,z,1)
        ae1 = [int(i) for i in my_list1]
        my_listi1 = K.DoIKine(-x/6,-y/6,0,6)
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
        time.sleep(0.3)
        #getch()
        print("1")

        my_list2 = K.DoIKine(x,y,z,3)
        ae2 = [int(i) for i in my_list2]
        my_listi2 = K.DoIKine(-x/6,-y/6,0,6)
        aa2 = [int(i) for i in my_listi2]
        my_listj2 = K.DoIKine(0,0,-z,1)
        ee2 = [int(i) for i in my_listj2]
        reb_list2 = calc_Velocity(ae2)
        reb_listi2 = calc_Velocity(aa2)
        reb_listj2 = calc_Velocity(ee2)
        WriteParallelVel(reb_listj2,1)
        WriteParallelAcc(reb_listj2,1)
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
        WriteParallel(ee2,1)
        WriteParallel(ae2,3)
        WriteParallel(aa2,5)
        WriteParallel(aa2,2)
        WriteParallel(aa2,4)
        WriteParallel(aa2,0)
        time.sleep(0.3)
        #getch()
        print("2")

        my_list3 = K.DoIKine(x,y,z,5)
        ae3 = [int(i) for i in my_list3]
        my_listi3 = K.DoIKine(-x/6,-y/6,0,6)
        aa3 = [int(i) for i in my_listi3]
        my_listj3 = K.DoIKine(0,0,-z,3)
        ee3 = [int(i) for i in my_listj3]
        reb_list3 = calc_Velocity(ae3)
        reb_listi3 = calc_Velocity(aa3)
        reb_listj3 = calc_Velocity(ee3)
        WriteParallelVel(reb_listi3,1)
        WriteParallelAcc(reb_listi3,1)
        WriteParallelVel(reb_listj3,3)
        WriteParallelAcc(reb_listj3,3)
        WriteParallelVel(reb_list3,5)
        WriteParallelAcc(reb_list3,5)
        WriteParallelVel(reb_listi3,2)
        WriteParallelAcc(reb_listi3,2)
        WriteParallelVel(reb_listi3,4)
        WriteParallelAcc(reb_listi3,4)
        WriteParallelVel(reb_listi3,0)
        WriteParallelAcc(reb_listi3,0)
        WriteParallel(aa3,1)
        WriteParallel(ee3,3)
        WriteParallel(ae3,5)
        WriteParallel(aa3,2)
        WriteParallel(aa3,4)
        WriteParallel(aa3,0)
        time.sleep(0.3)
        #getch()
        print("3")


        my_list4 = K.DoIKine(x,y,z,2)
        ae4 = [int(i) for i in my_list4]
        my_listi4 = K.DoIKine(-x/6,-y/6,0,6)
        aa4 = [int(i) for i in my_listi4]
        my_listj4 = K.DoIKine(0,0,-z,5)
        ee4 = [int(i) for i in my_listj4]
        reb_list4 = calc_Velocity(ae4)
        reb_listi4 = calc_Velocity(aa4)
        reb_listj4 = calc_Velocity(ee4)
        WriteParallelVel(reb_listi4,1)
        WriteParallelAcc(reb_listi4,1)
        WriteParallelVel(reb_listi4,3)
        WriteParallelAcc(reb_listi4,3)
        WriteParallelVel(reb_listj4,5)
        WriteParallelAcc(reb_listj4,5)
        WriteParallelVel(reb_list4,2)
        WriteParallelAcc(reb_list4,2)
        WriteParallelVel(reb_listi4,4)
        WriteParallelAcc(reb_listi4,4)
        WriteParallelVel(reb_listi4,0)
        WriteParallelAcc(reb_listi4,0)
        WriteParallel(aa4,1)
        WriteParallel(aa4,3)
        WriteParallel(ee4,5)
        WriteParallel(ae4,2)
        WriteParallel(aa4,4)
        WriteParallel(aa4,0)
        time.sleep(0.3)
        #getch()
        print("4")


        my_list5 = K.DoIKine(x,y,z,4)
        ae5 = [int(i) for i in my_list5]
        my_listi5 = K.DoIKine(-x/6,-y/6,0,6)
        aa5 = [int(i) for i in my_listi5]
        my_listi5 = K.DoIKine(-x/6,-y/6,0,6)
        aa5 = [int(i) for i in my_listi5]
        my_listj5 = K.DoIKine(0,0,-z,2)
        ee5 = [int(i) for i in my_listj5]
        reb_list5 = calc_Velocity(ae5)
        reb_listi5 = calc_Velocity(aa5)
        reb_listj5 = calc_Velocity(ee5)
        WriteParallelVel(reb_listi5,1)
        WriteParallelAcc(reb_listi5,1)
        WriteParallelVel(reb_listi5,3)
        WriteParallelAcc(reb_listi5,3)
        WriteParallelVel(reb_listi5,5)
        WriteParallelAcc(reb_listi5,5)
        WriteParallelVel(reb_listj5,2)
        WriteParallelAcc(reb_listj5,2)
        WriteParallelVel(reb_list5,4)
        WriteParallelAcc(reb_list5,4)
        WriteParallelVel(reb_listi5,0)
        WriteParallelAcc(reb_listi5,0)
        WriteParallel(aa5,1)
        WriteParallel(aa5,3)
        WriteParallel(aa5,5)
        WriteParallel(ee5,2)
        WriteParallel(ae5,4)
        WriteParallel(aa5,0)
        time.sleep(0.3)
        #getch()
        print("5")


        my_list = K.DoIKine(x,y,z,0)
        ae = [int(i) for i in my_list]
        my_listi = K.DoIKine(-x/6,-y/6,0,6)
        aa = [int(i) for i in my_listi]
        my_listi = K.DoIKine(-x/6,-y/6,0,6)
        aa = [int(i) for i in my_listi]
        my_listj = K.DoIKine(0,0,-z,4)
        ee = [int(i) for i in my_listj]
        reb_list = calc_Velocity(ae)
        reb_listi = calc_Velocity(aa)
        reb_listj = calc_Velocity(ee)
        WriteParallelVel(reb_listi,1)
        WriteParallelAcc(reb_listi,1)
        WriteParallelVel(reb_listi,3)
        WriteParallelAcc(reb_listi,3)
        WriteParallelVel(reb_listi,5)
        WriteParallelAcc(reb_listi,5)
        WriteParallelVel(reb_listi,2)
        WriteParallelAcc(reb_listi,2)
        WriteParallelVel(reb_listj,4)
        WriteParallelAcc(reb_listj,4)
        WriteParallelVel(reb_list,0)
        WriteParallelAcc(reb_list,0)
        WriteParallel(aa,1)
        WriteParallel(aa,3)
        WriteParallel(aa,5)
        WriteParallel(aa,2)
        WriteParallel(ee,4)
        WriteParallel(ae,0)
        time.sleep(0.3)
        #getch()
        print("6")

        WriteAllPositions(init_pos)
        time.sleep(0.3)
def rotationz(degrees):
    temp_stand_up = ReadAllPositions()
    alpha_rad = degrees*pi/180
    my_list = K.DoIKine(0,0,20,6)
    ae = [int(i) for i in my_list]
    WriteTripodGait(ae,0)
    time.sleep(0.5)
    my_listx = K.DoIKineRotationEuler(alpha_rad, 0, 0)
    xx = [int(i) for i in my_listx]
    WriteTripodGait(xx,1)
    time.sleep(1)
    my_list = K.DoIKine(0,0,-20,6)
    ae = [int(i) for i in my_list]
    WriteTripodGait(ae,0)
    time.sleep(1)
    my_list = K.DoIKine(0,0,20,6)
    ae = [int(i) for i in my_list]
    WriteTripodGait(ae,1)
    time.sleep(1)
    Write1Pos(1,2048)
    Write1Pos(10,2048)
    Write1Pos(13,2048)
    time.sleep(1)
    WriteTripodGait(temp_stand_up,1)



def rippleStairs(x,y,z,leg_case):
        my_list = K.DoIKine(x,y,z,6)
        ae = [int(i) for i in my_list]
        velocity_list = calc_Velocity(ae)
        WriteRippleVel(velocity_list,leg_case)
        WriteRippleAcc(velocity_list,legcase)
        WriteRippleGait(ae,leg_case)
        time.sleep(1)

def rippleMirror(x,y,z,leg_case):
        ee_xyz = K.DoFKine()
        if leg_case == 1:
            my_list = K.DoIKine(x,y,z,1)
            ae = [int(i) for i in my_list]
            my_listi = K.DoIKine(-x,y,z,2)
            aa = [int(i) for i in my_listi]
            velocity_list = calc_Velocity(aa)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,1)
            WriteParallel(aa,2)
        elif leg_case == 2:
            my_list = K.DoIKine(x,y,z,3)
            ae = [int(i) for i in my_list]
            my_listi = K.DoIKine(-x,y,z,4)
            aa = [int(i) for i in my_listi]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,3)
            WriteParallel(aa,4)
        else:
            my_list = K.DoIKine(x,y,z, 5)
            ae = [int(i) for i in my_list]
            my_listi = K.DoIKine(-x,y,z,0)
            aa = [int(i) for i in my_listi]
            velocity_list = calc_Velocity(aa)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,5)
            WriteParallel(aa,0)

def parallelGait(alpha_rad, beta_rad, gama_rad, dist_x, dist_y, dist_z):
        #print("im here:")
        my_listx = K.DoIKineRotationEuler(alpha_rad, beta_rad, gama_rad)
        my_reb_valx = K.DoIKine(-dist_x, -dist_y, -dist_z,6)
        xx = [int(i) for i in my_listx]
        ae_reb_valx = [int(i) for i in my_reb_valx]
        reb_listx = [10, 50, 50, 10, 50, 50, 10, 50, 50, 10, 50, 50, 10, 50, 50, 10, 50, 50]
        WriteTripodGaitVel(reb_listx,1)
        WriteTripodGaitAcc(reb_listx,1)
        WriteTripodGaitVel(reb_listx,0)
        WriteTripodGaitAcc(reb_listx,0)
        WriteAllPositions(xx)
        time.sleep(1)
        WriteAllPositions(ae_reb_valx)
        #print("im here:")
def singleLeg(x,y,z,leg_case):
        ee_xyz = K.DoFKine()
        if leg_case == 1:
            my_list = K.DoIKine(x,y,z,1)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,1)
        elif leg_case == 2:
            my_list = K.DoIKine(-x,y,z,2)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,2)
        elif leg_case == 3:
            my_list = K.DoIKine(x,y,z,3)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,3)
        elif leg_case == 4:
            my_list = K.DoIKine(-x,y,z,4)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,4)
        elif leg_case == 5:
            my_list = K.DoIKine(x,y,z,5)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,5)
        else:
            my_list = K.DoIKine(x,y,z,0)
            ae = [int(i) for i in my_list]
            velocity_list = calc_Velocity(ae)
            WriteRippleVel(velocity_list,leg_case)
            WriteRippleAcc(velocity_list,leg_case)
            WriteParallel(ae,0)
def oneStep(iteration_num):
        for i in range(0,iteration_num):
            time.sleep(1)
            singleLeg(0,0,20,1)
            time.sleep(1)
            singleLeg(10,40,0,1)
            time.sleep(1)
            singleLeg(0,0,-20,1)
            time.sleep(1)
            singleLeg(0,0,20,2)
            time.sleep(1)
            singleLeg(10,40,0,2)
            time.sleep(1)
            singleLeg(0,0,-20,2)
            time.sleep(1)
            singleLeg(0,0,20,5)
            time.sleep(1)
            singleLeg(-10,50,0,5)
            time.sleep(1)
            singleLeg(0,0,-20,5)
            time.sleep(1)
            singleLeg(0,0,20,0)
            time.sleep(1)
            singleLeg(10,50,0,0)
            time.sleep(1)
            singleLeg(0,0,-20,0)
            time.sleep(1)

            TripodGait(0,20,20,6)
            time.sleep(1)

            parallelGait(0,0,0,0,0,30)
            time.sleep(1)
            singleLeg(0,0,20,5)
            time.sleep(1)
            singleLeg(-50,50,0,5)
            time.sleep(1)
            singleLeg(0,0,-20,5)
            time.sleep(1)
            singleLeg(0,0,20,0)
            time.sleep(1)
            singleLeg(50,50,0,0)
            time.sleep(1)
            singleLeg(0,0,-20,0)
            time.sleep(1)

            parallelGait(0,0,0,0,20,0)
            time.sleep(1)
            parallelGait(0,0,0,0,30,0)
            time.sleep(1)
            rippleMirror(50,0,100,1)
            time.sleep(1)
            rippleMirror(50,0,100,1)
            time.sleep(1)
            Write1Pos(1,2048)
            Write1Pos(4,2048)
            time.sleep(0.5)
            rippleMirror(0,0,-65,1)
            time.sleep(1)
            position_staris_4legs = ReadAllPositions()
            positions_int = [int(i) for i in position_staris_4legs]
            print("positions :",positions_int )
            ae_position2 = [2039, 2800, 1115, 2050, 1352, 2892, 2178, 2333, 873, 1874, 1701, 3163, 2148, 1244, 1817, 2065, 2846, 2314]
            WriteAllPositions(ae_position2)
            #rippleMirror(0,0,-65,1)
            time.sleep(1)
            Write1Pos(16,2048)
            time.sleep(0.5)
            parallelGait(0,0,0,0,0,15)
            time.sleep(1)

            rippleMirror(0,0,20,2)
            time.sleep(1)
            rippleMirror(-50,100,0,2)
            time.sleep(1)
            rippleMirror(0,0,-20,2)
            time.sleep(1)
            singleLeg(100,50,165,5)
            time.sleep(1)
            Write1Pos(13,2948)
            time.sleep(1)
            singleLeg(0,0,-30,5)
            time.sleep(1)
            # parallelGait(0,0,0,0,20,0)
            # time.sleep(1)
            rippleMirror(0,0,20,2)
            time.sleep(1)
            rippleMirror(0,-110,0,2)
            time.sleep(1)
            rippleMirror(0,0,-20,2)
            time.sleep(1)
            singleLeg(-100,50,165,0)
            time.sleep(1)
            Write1Pos(16,1148)
            time.sleep(1)
            singleLeg(0,0,-30,0)
            time.sleep(1)
            rippleMirror(0,0,20,2)
            time.sleep(1)
            rippleMirror(0,110,0,2)
            time.sleep(1)
            rippleMirror(0,0,-20,2)
            time.sleep(1)
            parallelGait(0,0,0,0,0,50)
            time.sleep(2)
            parallelGait(0,0,0,0,20,0)
            time.sleep(2)
            parallelGait(0,0,0,0,20,0)
            time.sleep(2)
            parallelGait(0,0,0,0,20,0)
            time.sleep(2)
            parallelGait(0,0,0,0,20,0)
            time.sleep(2)
            parallelGait(0,0,0,0,0,50)
            time.sleep(5)
            TripodGait(0,20,20,2)
            rippleMirror(50,0,100,2)
            time.sleep(1)
            rippleMirror(20,0,65,2)
            time.sleep(1)
            ################################################################3333
            # My_position_2leg = [1858, 2561, 805, 2229, 1539, 3249, 2167, 1525, 1558, 1917, 2528, 2543, 2298, 1528, 1681, 1825, 2545, 2507]
            # WriteParallel(My_position_2leg,3)
            # WriteParallel(My_position_2leg,4)
            ############################################################3
            # Write1Pos(7,2648)
            # Write1Pos(10,1448)
            # time.sleep(1)
            # rippleMirror(0,0,-35,2)
            # time.sleep(1)
            # # TripodGait(0,20,20,7)
            # # time.sleep(1)
            # parallelGait(0,0,0,0,20,0)
            # time.sleep(2)
            # parallelGait(0,0,0,0,20,0)
            # time.sleep(2)
            # parallelGait(0,0,0,0,20,0)
            # time.sleep(2)
            # positions_int = [1652, 2693, 678, 2411, 1431, 3404, 2384, 2582, 808, 1718, 1555, 3217, 2144, 1484, 1778, 1982, 2734, 2187]
            # reb_list = calc_Velocity(positions_int)
            # ae = K.DoIKine(0,0,10,6)
            # ae_int = [int(i) for i in ae]
            # WriteTripodGaitVel(reb_list,1)
            # WriteTripodGaitAcc(reb_list,1)
            # WriteTripodGaitVel(reb_list,0)
            # WriteTripodGaitAcc(reb_list,0)
            # WriteTripodGait(ae_int,0)
            # time.sleep(1)
            # WriteTripodGait(positions_int,0)
            # time.sleep(1)
            # WriteTripodGait(ae_int,1)
            # time.sleep(1)
            # WriteTripodGait(positions_int,1)
