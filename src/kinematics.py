#!/usr/bin/env python
from math import pi,cos,sin,atan2,acos,sqrt,pow
from dynamixel_library import ReadAllPositions
pi = 3.1415926535
###################################################
#CONSTANTS, DON'T CHANGE UNLESS YOU KNOW WHAT TO DO
femur_ang_off =  20.00 * pi/180 #  20    degrees
tibia_ang_off = -28.27 * pi/180 # -28.27 degrees

len_coxa         =  66.50     # Link length of Coxa
len_femur        =  92.17     # Link length of Femur
len_tibia        =  193.66    # Link length of Tibia

z_offset         = -17      # CONSTANT FOR ALL LEGS
l1_x_offset      =  71.6    # CONSTANT FOR LEG 1
l1_y_offset      =  120.96  # CONSTANT FOR LEG 1
l2_x_offset      = -71.6    # CONSTANT FOR LEG 2
l2_y_offset      =  120.96  # CONSTANT FOR LEG 2
l3_x_offset      =  141.33  # CONSTANT FOR LEG 3
l3_y_offset      =  0       # CONSTANT FOR LEG 3
l4_x_offset      = -141.33  # CONSTANT FOR LEG 4
l4_y_offset      =  0       # CONSTANT FOR LEG 4
l5_x_offset      =  71.6    # CONSTANT FOR LEG 5
l5_y_offset      = -120.96  # CONSTANT FOR LEG 5
l6_x_offset      = -71.6    # CONSTANT FOR LEG 6
l6_y_offset      = -120.96  # CONSTANT FOR LEG 6

# Angular offsets from robot body origin to the first servo.
l1_ang_off       =   -pi/3 # Leg 1
l2_ang_off       = -2*pi/3 # Leg 2
l3_ang_off       =  0      # Leg 3
l4_ang_off       =    pi   # Leg 4
l5_ang_off       =    pi/3 # Leg 5
l6_ang_off       =  2*pi/3 # Leg 6

################FORWARD KINEMATICS################
def calc_Fkine(x_offset,y_offset,l_ang_off,servoPos,leg_side):
    theta1 = servoPos[0] - l_ang_off
    if leg_side == "odd" : # ODD LEGS
        theta2 = servoPos[1] + femur_ang_off
        theta3 = servoPos[2] + tibia_ang_off
        ee_z   = len_femur*sin(theta2) + len_tibia*sin(theta3+theta2) + z_offset
    elif leg_side == "even":
        theta2 = servoPos[1] - femur_ang_off
        theta3 = servoPos[2] - tibia_ang_off
        ee_z   = -(len_femur*sin(theta2) + len_tibia*sin(theta3+theta2) - z_offset)
    ee_x   = x_offset + cos(theta1)*(len_coxa + len_femur*cos(theta2) + len_tibia*cos(theta3+theta2))
    ee_y   = y_offset + sin(theta1)*(len_coxa + len_femur*cos(theta2) + len_tibia*cos(theta3+theta2))
    return [ee_x,ee_y,ee_z]
def Forward_kinematics(): #INPUT: An array with 18 servo thetas in RADIANS
    servoPos = [(((x/2047.5)-1) * pi) for x in ReadAllPositions()] # Converts each ReadPosition from steps to radians
    endpoint_xyz = []
    endpoint_xyz.extend(calc_Fkine(l1_x_offset,l1_y_offset, l1_ang_off, servoPos[0:3],   "odd" ))
    endpoint_xyz.extend(calc_Fkine(l2_x_offset,l2_y_offset, l2_ang_off, servoPos[3:6],   "even"))
    endpoint_xyz.extend(calc_Fkine(l3_x_offset,l3_y_offset, l3_ang_off, servoPos[6:9],   "odd" ))
    endpoint_xyz.extend(calc_Fkine(l4_x_offset,l4_y_offset, l4_ang_off, servoPos[9:12],  "even"))
    endpoint_xyz.extend(calc_Fkine(l5_x_offset,l5_y_offset, l5_ang_off, servoPos[12:15], "odd" ))
    endpoint_xyz.extend(calc_Fkine(l6_x_offset,l6_y_offset, l6_ang_off, servoPos[15:18], "even"))
    return endpoint_xyz #OUTPUT: 6 sets of x,y,z coordinates for each leg end-tip

################INVERSE KINEMATICS################
def calc_Ikine(x, y, z, endtip_xyz, l_ang_off, l_x_offset, l_y_offset, leg_side):
    init_X   = endtip_xyz[0]
    init_Y   = endtip_xyz[1]
    init_Z   = endtip_xyz[2]
    X        = init_X + (x) - l_x_offset
    Y        = init_Y + (y) - l_y_offset
    Z        = init_Z - (z) - z_offset
    theta1   = atan2(Y,X) + l_ang_off
    if theta1 < -pi:
       theta1 += 2*pi
    if theta1 > pi:
       theta1 -= 2*pi
    new_x    = cos(l_ang_off) * X   - sin(l_ang_off) * Y
    new_y    = sin(l_ang_off) * X   + cos(l_ang_off) * Y
    final_x  = cos(theta1) * new_x  + sin(theta1)    * new_y  - len_coxa
    s        = sqrt( pow(final_x,2) + pow(Z,2) )
    t3       = pi - acos((-pow(s,2) + pow(len_femur,2) + pow(len_tibia,2)) / (2*len_femur*len_tibia))
    if leg_side == "odd" : # ODD LEGS
        theta3 = -t3 - tibia_ang_off
        theta2 = -(-atan2(Z,final_x) - atan2(len_tibia * sin(t3), len_femur + len_tibia * cos(t3)) + femur_ang_off)
    elif leg_side == "even": # EVEN LEGS
        theta3 =  t3 + tibia_ang_off
        theta2 = -( atan2(Z,final_x) + atan2(len_tibia * sin(t3), len_femur + len_tibia * cos(t3)) - femur_ang_off)
    return [theta1,theta2,theta3]
def Inverse_kinematics(x,y,z):
    endtip_xyz = Forward_kinematics()
    servo_array = []
    servo_array.extend(calc_Ikine(x, y, z, endtip_xyz[0:3],   l1_ang_off, l1_x_offset, l1_y_offset, "odd" ))
    servo_array.extend(calc_Ikine(x, y, z, endtip_xyz[3:6],   l2_ang_off, l2_x_offset, l2_y_offset, "even"))
    servo_array.extend(calc_Ikine(x, y, z, endtip_xyz[6:9],   l3_ang_off, l3_x_offset, l3_y_offset, "odd" ))
    servo_array.extend(calc_Ikine(x, y, z, endtip_xyz[9:12],  l4_ang_off, l4_x_offset, l4_y_offset, "even"))
    servo_array.extend(calc_Ikine(x, y, z, endtip_xyz[12:15], l5_ang_off, l5_x_offset, l5_y_offset, "odd" ))
    servo_array.extend(calc_Ikine(x, y, z, endtip_xyz[15:18], l6_ang_off, l6_x_offset, l6_y_offset, "even"))
    servo_array = [x / pi * 2048 + 2048 for x in servo_array]
    return servo_array #OUTPUT: 18 servo STEPS to accomplish this motion (rads)

#####################PRINTS#######################
def PrintForward():
    coord_list = Forward_kinematics()
    RoundedCoords = [ '%.4f' % elem for elem in coord_list ]
    print ""
    print "X,Y,Z coordinates of Leg end-points: "
    print "       " +  str(["X       ", " Y    ", "  Z   "])
    print "Leg 1: " +  str(RoundedCoords[0:3])
    print "Leg 2: " +  str(RoundedCoords[3:6])
    print "Leg 3: " +  str(RoundedCoords[6:9])
    print "Leg 4: " +  str(RoundedCoords[9:12])
    print "Leg 5: " +  str(RoundedCoords[12:15])
    print "Leg 6: " +  str(RoundedCoords[15:18])
    print ""
def PrintInverse(theta_list):
    thetas = theta_list
    RoundedThetas = [ '%.4f' % elem for elem in thetas ]
    print ""
    print "Theta angles of each servo:"
    print "       " +  str(["Coxa    ","Femur ", "Tibia"])
    print "Leg 1: " +  str(RoundedThetas[0:3])
    print "Leg 2: " +  str(RoundedThetas[3:6])
    print "Leg 3: " +  str(RoundedThetas[6:9])
    print "Leg 4: " +  str(RoundedThetas[9:12])
    print "Leg 5: " +  str(RoundedThetas[12:15])
    print "Leg 6: " +  str(RoundedThetas[15:18])
    print ""
def DoBothKinematicsAndPrint_new(x,y,z):
    PrintForward()
    PrintInverse(Inverse_kinematics(x,y,z))
