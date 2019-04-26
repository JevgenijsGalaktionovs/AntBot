#!/usr/bin/env python

# import rospy
# import time
#
# from kinematics        import Kinematics
# from dynamixel_library import *
# from stupid_walk       import *
# #import RPi.GPIO as GPIO
# import time
#
# #GPIO.setmode(GPIO.BCM)
# #GPIO.setup(4,GPIO.IN)
# DisableTorqueAllServos()
# WritePWMLimit([250]*18) # Modify PWM Limit (torque must be off)
# EnableTorqueAllServos()
# #for x in range (0, 18):
# # my_listVelcoxa =  [100,100,100,100]
# # my_listVelfemor = [100,100, 20,100]
# # my_listVeltibia = [100, 20,100, 20]
# # for x,y,z in zip (my_listVelcoxa,my_listVelfemor,my_listVeltibia):
# # 	writeProfVel(1,x)
# # 	writeProfAcc(1,x)
# # 	writeProfVel(2,y)
# # 	writeProfAcc(2,y)
# # 	writeProfVel(3,z)
# # 	writeProfAcc(3,z)
#
# #def sensor_data():
# ##initialise a previous input variable to 0 (Assume no pressure applied)
# #    	prev_input = 0
#  #       #take a reading
#  #       input = GPIO.input(4)
# #	a=1
#  #       #if the last reading was low and this one high, alert us
#   #      if ((not prev_input) and input):
#   #          print("Under Pressure")
# #    a=0
#  #       #update previous input
#   #      prev_input = input
#    #     #slight pause
# #	print(a)
#
# #	return a
#
#
# #servo1=[2054,2057,2064,2074,2085,2097,2108,2117,2124,2129,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130]
# #servo2=[2218,2238,2283,2335,2373,2377,2340,2279,2214,2163,2143,2108,2075,2041,2007,1973,1939,1905,1870,1836,1806,1764,1727,1690,1651,1610,1567,1522,1472,1417,1351,1260]
# #servo3=[1027,1017, 996, 979, 976, 996,1044,1106,1169,1219,1238,1265,1292,1320,1348,1378,1409,1440,1473,1507,1542,1580,1618,1660,1702,1750,1799,1854,1915,1986,2073,2200]
# #servo1=[2054,2054,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130]
# #servo2=[2218,2674,2143,2108,2075,2041,2007,1973,1939,1905,1870,1836,1806,1764,1727,1690,1651,1610,1567,1522,1472,1417,1351,1260]
# #servo3=[1027, 752,1238,1265,1292,1320,1348,1378,1409,1440,1473,1507,1542,1580,1618,1660,1702,1750,1799,1854,1915,1986,2073,2200]
# servo1=           [2054,2054,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130,2130]
# servo2=           [2218,2674,2488,2143,2108,2075,2041,2007,1973,1939,1905,1870,1836,1806,1764,1727,1690,1651,1610,1567,1522,1472,1417,1351,1260]
# servo3=           [1027, 752,1016,1239,1265,1292,1320,1348,1378,1409,1440,1473,1507,1542,1580,1618,1660,1702,1750,1799,1854,1915,1986,2073,2200]
# my_listVelcoxa =  [ 100, 100, 100, 100,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10]
# my_listVelfemor = [ 100, 100,  70, 100,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10]
# my_listVeltibia = [ 100,  60, 100,  60,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10]
# a = 0
# for x in range (0,25):
#   for x,y,z,x1,y1,z1 in zip(my_listVelcoxa,my_listVeltibia,my_listVelfemor,servo1,servo3,servo2):
# 	print("ok")
# #	a = sensor_data()
# 	if a == 0:
# 		time.sleep(2)
# 		writeProfVel(1,x)
# 		writeProfAcc(1,x)
# 		writeProfVel(3,y)
# 		writeProfAcc(3,y)
# 		writeProfVel(2,z)
# 		writeProfAcc(2,z)
# 		Write1Pos(1,x1)
# 		Write1Pos(3,y1)
# 		Write1Pos(2,z1)
# 		#print (x,y,z)
# 	else:
# 		print("not ok")
# 		b == 1
# 		break
#   if  b == 1:
# 	break
###########better one#####
import rospy
import time

from kinematics        import Kinematics
from dynamixel_library import *
from stupid_walk       import *

def gait_with_keypresses():

    stand_up()
    y = int(input("How much do you want to move forward in mm pr step? "))
    z = 40#height
    x = int(input("How much do you want to move sideways in mm pr step? "))
    increment = 5
    while(1):
        my_list = K.DoIKine(0,0,z)
        ae = [int(i) for i in my_list]
        my_listi = K.DoIKine(0,0,-z/2)
        aa = [int(i) for i in my_listi]
        reb_list = [20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100]
        WriteTripodProfVel(reb_list,1)
        WriteTripodProfAcc(reb_list,1)
        WriteTripodProfVel(reb_list,0)
        WriteTripodProfAcc(reb_list,0)
        WriteTripodGait(ae,1)
        WriteTripodGait(aa,0)
        time.sleep(1)
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        getch()


        my_list2 = K.DoIKine(x, y, 0)
        ae2 = [int(i) for i in my_list2]
        my_listi2 = K.DoIKine(-x, -y, 0)
        aa2 = [int(i) for i in my_listi2]
        reb_list2 = [20, 100, 50, 20, 100, 50, 20, 100, 50, 20, 100, 50, 20, 100, 50, 20, 100, 50]
        WriteTripodProfVel(reb_list2,1)
        WriteTripodProfAcc(reb_list2,1)
        WriteTripodProfVel(reb_list2,0)
        WriteTripodProfAcc(reb_list2,0)
        WriteTripodGait(ae2,1)
        WriteTripodGait(aa2,0)
        time.sleep(1)
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        getch()

        my_list3 = K.DoIKine(0,0,-z)
        ae3 = [int(i) for i in my_list3]
        my_listi3 = K.DoIKine(0,0,z/2)
        aa3 = [int(i) for i in my_listi3]
        reb_list3 = [20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100, 20, 50, 100]
        WriteTripodProfVel(reb_list3,1)
        WriteTripodProfAcc(reb_list3,1)
        WriteTripodProfVel(reb_list3,0)
        WriteTripodProfAcc(reb_list3,0)
        WriteTripodGait(ae3,1)
        WriteTripodGait(aa3,0)
        time.sleep(1)
        getch()
        # K.DoBothKinematicsAndPrint(0,0,0)
        # print ReadAllPositions()
        # getch()
        # my_list4 = K.DoIKine(x,y,-z/2)
        # ae4 = [int(i) for i in my_list4]
        # WriteTripodGait(ae4,0)
        # time.sleep(1)
        # K.DoBothKinematicsAndPrint(0,0,0)
        # print ReadAllPositions()
        # getch()
        for x in range(0, 15):
            my_list4 = K.DoIKine(0,0,-increment)
            ae4 = [int(i) for i in my_list4]
            reb_list4 = [20, 100, 100, 20, 100, 100, 20, 100, 100, 20, 100, 100, 20, 100, 100, 20, 100, 100]
            WriteTripodProfVel(reb_list4,1)
            WriteTripodProfAcc(reb_list4,1)
            WriteTripodGait(ae4,1)
            time.sleep(0.5)

        stand_up()
        K.DoBothKinematicsAndPrint(0,0,0)
        print ReadAllPositions()
        time.sleep(1)

if __name__=='__main__':
    try:
        CheckStatus()           # Checks if all 18 servos are connected
        WritePWMLimit([250]*18) # Modify PWM Limit (torque must be off)
        K = Kinematics()        # Creates Kinematics class object "K"
        EnableTorqueAllServos() # Enable Torque, duuh


        gait_with_keypresses()  # tripod gait that expects keyboard press between steps
    except rospy.ROSInterruptException :
        portHandler.closePort()
