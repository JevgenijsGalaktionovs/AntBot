import time
import rospy

from math import pi,cos,sin,atan2,acos,sqrt,pow
from kinematics        import *
from dynamixel_library import *
from stupid_walk       import *

def gait_with_keypresses():

    stand_up()
    rot = int(input("How much do you want to rotate in degrees pr step?[max=45] "))
    rot_steps = rot*4096/360
    z = 20
    side = int(input("To the left or to the right?[0 for L/1 for R] "))
    print(side)
    while(1):
        servoPos = [(((x/2047.5)-1) * pi) for x in ReadAllPositions()]
        add_list = [rot_steps, 0,0,rot_steps, 0, 0,rot_steps, 0, 0,rot_steps, 0, 0,rot_steps, 0, 0,rot_steps, 0, 0]
        if side == 1:
            for x in range(0, 18)
             new_servo_pos = servoPos + add_list
             print(new_servo_pos)
        else:
             new_servo_pos = servoPos - add_list
             print(new_servo_pos)

        my_list = K.DoIKine(0,0,z)
        ae = [int(i) for i in my_list]
        reb_list = [20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100]
        WriteTripodProfVel(reb_list,1)
        WriteTripodProfAcc(reb_list,1)
        WriteTripodProfVel(reb_list,0)
        WriteTripodProfAcc(reb_list,0)
        WriteTripodGait(ae,1)
        time.sleep(1)
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        getch()


        my_list2 = K.DoIKine(x, y, 0)
        ae2 = [int(i) for i in my_list2]
        reb_list2 = [20, 100, 50, 20, 100, 50, 20, 100, 50, 20, 100, 50, 20, 100, 50, 20, 100, 50]
        WriteTripodProfVel(reb_list2,1)
        WriteTripodProfAcc(reb_list2,1)
        WriteTripodProfVel(reb_list2,0)
        WriteTripodProfAcc(reb_list2,0)
        WriteTripodGait(ae2,1)
        time.sleep(1)
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        getch()

        my_list3 = K.DoIKine(0,0,-z)
        ae3 = [int(i) for i in my_list3]
        reb_list3 = [20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100]
        WriteTripodProfVel(reb_list3,1)
        WriteTripodProfAcc(reb_list3,1)
        WriteTripodProfVel(reb_list3,0)
        WriteTripodProfAcc(reb_list3,0)
        WriteTripodGait(ae3,1)
        time.sleep(1)
        getch()

if __name__=='__main__':
    try:
        CheckStatus()           # Checks if all 18 servos are connected
        WritePWMLimit([500]*18) # Modify PWM Limit (torque must be off)
        K = Kinematics()        # Creates Kinematics class object "K"
        EnableTorqueAllServos() # Enable Torque, duuh


        gait_with_keypresses()  # tripod gait that expects keyboard press between steps
    except rospy.ROSInterruptException :
        portHandler.closePort()





# def stand_up():
# 	initial_pos = [2048,2218,1024,
# 			2048,1878,3048,
# 			2048,2218,1024,
# 			2048,1878,3048,
# 			2048,2218,1024,
# 			2048,1878,3048]
# 	WriteAllPositions(initial_pos)
#
# for x in range (0, 8):
#     writeProfVel(1,50)
#     writeProfAcc(1,20)
#     writeProfVel(2,100)
#     writeProfAcc(2,20)
#     writeProfVel(3,100)
#     writeProfAcc(3,20)
#     writeProfVel(4,50)
#     writeProfAcc(4,20)
#     writeProfVel(5,100)
#     writeProfAcc(5,20)
#     writeProfVel(6,100)
#     writeProfAcc(6,20)
#     writeProfVel(7,50)
#     writeProfAcc(7,20)
#     writeProfVel(8,100)
#     writeProfAcc(8,20)
#     writeProfVel(9,100)
#     writeProfAcc(9,20)
#     writeProfVel(10,50)
#     writeProfAcc(10,20)
#     writeProfVel(11,100)
#     writeProfAcc(11,20)
#     writeProfVel(12,100)
#     writeProfAcc(12,20)
#     writeProfVel(13,50)
#     writeProfAcc(13,20)
#     writeProfVel(14,100)
#     writeProfAcc(14,20)
#     writeProfVel(15,100)
#     writeProfAcc(15,20)
#     writeProfVel(16,50)
#     writeProfAcc(16,20)
#     writeProfVel(17,100)
#     writeProfAcc(17,20)
#     writeProfVel(18,100)
#     writeProfAcc(18,20)
#     #stand up
#     # leg 1
#     Write1Pos(1,2048)
#     Write1Pos(2,2218)
#     Write1Pos(3,1024)
#     # leg 2
#     Write1Pos(4,2048)
#     Write1Pos(5,1878)
#     Write1Pos(6,3048)
#     # leg 3
#     Write1Pos(7,2048)
#     Write1Pos(8,2218)
#     Write1Pos(9,1024)
#     time.sleep(0.5)
#     # leg 4
#     Write1Pos(10,2048)
#     Write1Pos(11,1878)
#     Write1Pos(12,3048)
#     # leg 5
#     Write1Pos(13,2048)
#     Write1Pos(14,2218)
#     Write1Pos(15,1024)
#     # leg 6
#     Write1Pos(16,2048)
#     Write1Pos(17,1878)
#     Write1Pos(18,3048)
#     time.sleep(0.5)
#
#
#     # #rotate body 45 degress
#     # # leg 1
#     # Write1Pos(1,2560)
#     # Write1Pos(2,2218)
#     # Write1Pos(3,1024)
#     # # leg 4
#     # Write1Pos(10,2560)
#     # Write1Pos(11,1878)
#     # Write1Pos(12,3048)
#     # # leg 5
#     # Write1Pos(13,2560)
#     # Write1Pos(14,2218)
#     # Write1Pos(15,1024)
#     # #leg 2
#     # Write1Pos(4,2560)
#     # Write1Pos(5,1878)
#     # Write1Pos(6,3048)
#     # #leg 3
#     # Write1Pos(7,2560)
#     # Write1Pos(8,2218)
#     # Write1Pos(9,1024)
#     # #leg 6
#     # Write1Pos(16,2560)
#     # Write1Pos(17,1878)
#     # Write1Pos(18,3048)
#     # time.sleep(1)
#     # #rotate body -45 degress
#     # # leg 1
#     # Write1Pos(1,2048)
#     # Write1Pos(2,2218)
#     # Write1Pos(3,1024)
#     # # leg 4
#     # Write1Pos(10,2048)
#     # Write1Pos(11,1878)
#     # Write1Pos(12,3048)
#     # # leg 5
#     # Write1Pos(13,2048)
#     # Write1Pos(14,2218)
#     # Write1Pos(15,1024)
#     # #leg 2
#     # Write1Pos(4,2048)
#     # Write1Pos(5,1878)
#     # Write1Pos(6,3048)
#     # #leg 3
#     # Write1Pos(7,2048)
#     # Write1Pos(8,2218)
#     # Write1Pos(9,1024)
#     # #leg 6
#     # Write1Pos(16,2048)
#     # Write1Pos(17,1878)
#     # Write1Pos(18,3048)
#     # time.sleep(1)
#     # #rotate body 45 degress
#     # # leg 1
#     # Write1Pos(1,1536)
#     # Write1Pos(2,2218)
#     # Write1Pos(3,1024)
#     # # leg 4
#     # Write1Pos(10,1536)
#     # Write1Pos(11,1878)
#     # Write1Pos(12,3048)
#     # # leg 5
#     # Write1Pos(13,1536)
#     # Write1Pos(14,2218)
#     # Write1Pos(15,1024)
#     # #leg 2
#     # Write1Pos(4,1536)
#     # Write1Pos(5,1878)
#     # Write1Pos(6,3048)
#     # #leg 3
#     # Write1Pos(7,1536)
#     # Write1Pos(8,2218)
#     # Write1Pos(9,1024)
#     # #leg 6
#     # Write1Pos(16,1536)
#     # Write1Pos(17,1878)
#     # Write1Pos(18,3048)
#     # time.sleep(1)
#     # #rotate body -45 degress
#     # # leg 1
#     # Write1Pos(1,2048)
#     # Write1Pos(2,2218)
#     # Write1Pos(3,1024)
#     # # leg 4
#     # Write1Pos(10,2048)
#     # Write1Pos(11,1878)
#     # Write1Pos(12,3048)
#     # # leg 5
#     # Write1Pos(13,2048)
#     # Write1Pos(14,2218)
#     # Write1Pos(15,1024)
#     # #leg 2
#     # Write1Pos(4,2048)
#     # Write1Pos(5,1878)
#     # Write1Pos(6,3048)
#     # #leg 3
#     # Write1Pos(7,2048)
#     # Write1Pos(8,2218)
#     # Write1Pos(9,1024)
#     # #leg 6
#     # Write1Pos(16,2048)
#     # Write1Pos(17,1878)
#     # Write1Pos(18,3048)
#     # time.sleep(1)
#
#
#     #legs up and midle
#     # leg 1
#     Write1Pos(1,2304)
#     Write1Pos(2,2418)
#     Write1Pos(3,1124)
#     # leg 4
#     Write1Pos(10,2304)
#     Write1Pos(11,1678)
#     Write1Pos(12,3148)
#     # leg 5
#     Write1Pos(13,2304)
#     Write1Pos(14,2418)
#     Write1Pos(15,1124)
#     time.sleep(0.5)
#
#     #legs down rotated 45 degrees
#     # leg 1
#     Write1Pos(1,2560)
#     Write1Pos(2,2218)
#     Write1Pos(3,1024)
#     # leg 4
#     Write1Pos(10,2560)
#     Write1Pos(11,1878)
#     Write1Pos(12,3048)
#     # leg 5
#     Write1Pos(13,2560)
#     Write1Pos(14,2218)
#     Write1Pos(15,1024)
#     time.sleep(0.5)
#     #other legs up in the air
#     #leg 2
#     Write1Pos(4,2048)
#     Write1Pos(5,1678)
#     Write1Pos(6,3148)
#     #leg 3
#     Write1Pos(7,2048)
#     Write1Pos(8,2418)
#     Write1Pos(9,1124)
#     #leg 6
#     Write1Pos(16,2048)
#     Write1Pos(17,1678)
#     Write1Pos(18,3148)
#     time.sleep(0.5)
#     #rotate body 45 degress
#     # leg 1
#     Write1Pos(1,2048)
#     Write1Pos(2,2218)
#     Write1Pos(3,1024)
#     # leg 4
#     Write1Pos(10,2048)
#     Write1Pos(11,1878)
#     Write1Pos(12,3048)
#     # leg 5
#     Write1Pos(13,2048)
#     Write1Pos(14,2218)
#     Write1Pos(15,1024)
#     time.sleep(0.5)
#     #other legs down on the ground
#     #leg 2
#     Write1Pos(4,2048)
#     Write1Pos(5,1878)
#     Write1Pos(6,3048)
#     #leg 3
#     Write1Pos(7,2048)
#     Write1Pos(8,2218)
#     Write1Pos(9,1024)
#     #leg 6
#     Write1Pos(16,2048)
#     Write1Pos(17,1878)
#     Write1Pos(18,3048)
#     time.sleep(0.5)
