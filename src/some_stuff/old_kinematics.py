#!/usr/bin/env python
import math
from   dynamixel_library import ReadAllPositions

###################################################
#CONSTANTS, DON'T CHANGE UNLESS YOU KNOW WHAT TO DO

ang_offset_femur =  20.00 * math.pi/180   # CONSTANT FOR ALL LEGS
ang_offset_tibia = -28.27 * math.pi/180   # CONSTANT FOR ALL LEGS

len_coxa         =  66.50   # CONSTANT FOR ALL LEGS
len_femur        =  92.17   # CONSTANT FOR ALL LEGS
len_tibia        =  193.66  # CONSTANT FOR ALL LEGS

z_offset         = -14.90   # CONSTANT FOR ALL LEGS
l1_x_offset      =  60.827  # CONSTANT FOR LEG 1
l1_y_offset      =  131.38  # CONSTANT FOR LEG 1
l2_x_offset      = -60.827  # CONSTANT FOR LEG 2
l2_y_offset      =  131.38  # CONSTANT FOR LEG 2
l3_x_offset      =  109.38  # CONSTANT FOR LEG 3
l3_y_offset      =  0       # CONSTANT FOR LEG 3
l4_x_offset      = -109.38  # CONSTANT FOR LEG 4
l4_y_offset      =  0       # CONSTANT FOR LEG 4
l5_x_offset      =  60.827  # CONSTANT FOR LEG 5
l5_y_offset      = -131.38  # CONSTANT FOR LEG 5
l6_x_offset      = -60.827  # CONSTANT FOR LEG 6
l6_y_offset      = -131.38  # CONSTANT FOR LEG 6

##################################################
################INVERSE KINEMATICS################
##################################################
def calculate_X(init_X,x,which_leg):
    if   which_leg == 1:
        return init_X + (x) - l1_x_offset
    elif which_leg == 2:
        return init_X + (x) - l2_x_offset
    elif which_leg == 3:
        return init_X + (x) - l3_x_offset
    elif which_leg == 4:
        return init_X + (x) - l4_x_offset
    elif which_leg == 5:
        return init_X + (x) - l5_x_offset
    elif which_leg == 6:
        return init_X + (x) - l6_x_offset
    else:
        pass
def calculate_Y(init_Y,y,which_leg):
    if   which_leg == 1:
        return init_Y + (y) - l1_y_offset
    elif which_leg == 2:
        return init_Y + (y) - l2_y_offset
    elif which_leg == 3:
        return init_Y + (y) - l3_y_offset
    elif which_leg == 4:
        return init_Y + (y) - l4_y_offset
    elif which_leg == 5:
        return init_Y + (y) - l5_y_offset
    elif which_leg == 6:
        return init_Y + (y) - l6_y_offset
def calculate_Z(init_Z,z):
    return init_Z - (z) - z_offset

def calculate_theta1(X,Y,which_leg):
    if   which_leg == 1:
        return math.atan2(Y,X) - math.pi/4
    elif which_leg == 2:
        return math.atan2(Y,X) - (3*math.pi/4)
    elif which_leg == 3:
        return math.atan2(Y,X)
    elif which_leg == 4:
        return math.atan2(Y,X) - math.pi
    elif which_leg == 5:
        return math.atan2(Y,X) + (math.pi/4)
    elif which_leg == 6:
        return math.atan2(Y,X) + (3*math.pi/4)
    else:
        pass
def calculate_new_x(X,Y,which_leg):
    if   which_leg == 1:
        return (math.cos(-45*math.pi/180)   * X) - (math.sin(-45*math.pi/180)   * Y)
    elif which_leg == 2:
        return (math.cos(-3*45*math.pi/180) * X) - (math.sin(-3*45*math.pi/180) * Y)
    elif which_leg == 3:
        pass # No new_x in leg 3
    elif which_leg == 4:
        return (math.cos(-180*math.pi/180)  * X) - (math.sin(-180*math.pi/180)  * Y)
    elif which_leg == 5:
        return (math.cos(45*math.pi/180)    * X) - (math.sin(45*math.pi/180)    * Y)
    elif which_leg == 6:
        return (math.cos(3*45*math.pi/180)  * X) - (math.sin(3*45*math.pi/180)  * Y)
    else:
        pass
def calculate_new_y(X,Y,which_leg):
    if   which_leg == 1:
        return (math.sin(-45*math.pi/180) * X)   + (math.cos(-45*math.pi/180)   * Y)
    elif which_leg == 2:
        return (math.sin(-3*45*math.pi/180) * X) + (math.cos(-3*45*math.pi/180) * Y)
    elif which_leg == 3:
        pass # No new_x in leg 3
    elif which_leg == 4:
        return (math.sin(-180*math.pi/180) * X)  + (math.cos(-180*math.pi/180)  * Y)
    elif which_leg == 5:
        return (math.sin(45*math.pi/180) * X)    + (math.cos(45*math.pi/180)    * Y)
    elif which_leg == 6:
        return (math.sin(3*45*math.pi/180) * X)  + (math.cos(3*45*math.pi/180)  * Y)
    else:
        pass
def calculate_final_x(theta1,new_x,new_y,which_leg):
    if   which_leg == 1:
        return (math.cos(theta1) * new_x) - (math.sin(-theta1) * new_y) - len_coxa
    elif which_leg == 2:
        return (math.cos(theta1) * new_x)  + (math.sin(theta1) * new_y)  - len_coxa
    elif which_leg == 3:
        return (math.cos(-theta1) * new_x) - (math.sin(-theta1) * new_y) - len_coxa # some spookie magic happened here. X> new_x ; Y>new_y
    elif which_leg == 4:
        return (math.cos(theta1) * new_x)  + (math.sin(theta1) * new_y)  - len_coxa
    elif which_leg == 5:
        return (math.cos(theta1) * new_x)  + (math.sin(theta1) * new_y)  - len_coxa
    elif which_leg == 6:
        return (math.cos(theta1) * new_x)  + (math.sin(theta1) * new_y)  - len_coxa
    else:
        pass
def calculate_s(final_x,Z):
    return math.sqrt(math.pow(final_x,2) + math.pow(Z,2))
def calculate_t3(s):
    return math.pi - math.acos((-math.pow(s,2) + math.pow(len_femur,2) + math.pow(len_tibia,2)) / (2*len_femur*len_tibia))
    # return math.acos((math.pow(s,2) - math.pow(len_femur,2) - math.pow(len_tibia,2)) / (2*len_femur*len_tibia))
def calculate_theta3(t3,leg_case):

    if leg_case == 1:
        # ODD LEGS
        return t3 + ang_offset_tibia
    else:
        # EVEN LEGS
        return -t3 - ang_offset_tibia
def calculate_theta2(Z,final_x,t3,leg_case):
    # LEG 3 HAS DIFFERENT FORMULA! IMPORTANT!
    # Therefore, we are using another formula if calculated theta2 is on LEG 3
    if leg_case == 1:
        return   math.atan2(Z,final_x) + math.atan2(len_tibia * math.sin(t3), len_femur + len_tibia * math.cos(t3))  - ang_offset_femur
    else:
        return (-math.atan2(Z,final_x) - math.atan2(len_tibia * math.sin(t3), len_femur + len_tibia * math.cos(t3))) + ang_offset_femur

def Ikine_leg1(x,y,z,endtip_xyz):
    init_X   = endtip_xyz[0]
    init_Y   = endtip_xyz[1]
    init_Z   = endtip_xyz[2]
    X        = calculate_X(init_X,x,1)
    Y        = calculate_Y(init_Y,y,1)
    Z        = calculate_Z(init_Z,z)
    theta1   = calculate_theta1(X,Y,1)
    new_x    = calculate_new_x(X,Y,1)   # DIFFERS in all legs
    new_y    = calculate_new_y(X,Y,1)
    final_x  = calculate_final_x(theta1,new_x,new_y,1)
    s        = calculate_s(final_x,Z)
    t3       = calculate_t3(s)
    theta3   = calculate_theta3(t3,1)
    theta2   = calculate_theta2(Z,final_x,t3,0)
    # print(theta1*180/math.pi) # Theta 1 in degrees
    # print(theta2*180/math.pi) # Theta 2 in degrees
    # print(theta3*180/math.pi) # Theta 3 in degrees
    return [theta1,theta2,theta3]
def Ikine_leg2(x,y,z,endtip_xyz):
    init_X  = endtip_xyz[3]
    init_Y  = endtip_xyz[4]
    init_Z  = endtip_xyz[5]
    X       = calculate_X(init_X,x,2)
    Y       = calculate_Y(init_Y,y,2)
    Z       = calculate_Z(init_Z,z)
    theta1  = calculate_theta1(X,Y,2)
    new_x   = calculate_new_x(X,Y,2)
    new_y   = calculate_new_y(X,Y,2)
    final_x = calculate_final_x(theta1,new_x,new_y,2)
    s       = calculate_s(final_x,Z)
    t3      = calculate_t3(s)
    theta3  = calculate_theta3(t3,0)
    theta2  = calculate_theta2(Z,final_x,t3,1)
    return [theta1,theta2,theta3]
def Ikine_leg3(x,y,z,endtip_xyz):
    init_X  = endtip_xyz[6]
    init_Y  = endtip_xyz[7]
    init_Z  = endtip_xyz[8]
    X       = calculate_X(init_X,x,3)
    Y       = calculate_Y(init_Y,y,3)
    Z       = calculate_Z(init_Z,z)
    theta1  = calculate_theta1(X,Y,3)
    final_x = calculate_final_x(theta1,X,Y,3) # Aha... new_x>X ; new_y>Y
    s       = calculate_s(final_x,Z)
    t3      = calculate_t3(s)
    theta3  = calculate_theta3(t3,1)
    theta2  = calculate_theta2(Z,final_x,t3,0)
    return [theta1,theta2,theta3]
def Ikine_leg4(x,y,z,endtip_xyz):
    init_X  = endtip_xyz[9]
    init_Y  = endtip_xyz[10]
    init_Z  = endtip_xyz[11]
    X       = calculate_X(init_X,x,4)
    Y       = calculate_Y(init_Y,y,4)
    Z       = calculate_Z(init_Z,z)
    theta1  = calculate_theta1(X,Y,4)
    new_x   = calculate_new_x(X,Y,4)
    new_y   = calculate_new_y(X,Y,4)
    final_x = calculate_final_x(theta1,new_x,new_y,4)
    s       = calculate_s(final_x,Z)
    t3      = calculate_t3(s)
    theta3  = calculate_theta3(t3,0)
    theta2  = calculate_theta2(Z,final_x,t3,1)

    if theta1 < -math.pi:
       theta1 += 2*math.pi
    return [theta1,theta2,theta3]
def Ikine_leg5(x,y,z,endtip_xyz):
    init_X  = endtip_xyz[12]
    init_Y  = endtip_xyz[13]
    init_Z  = endtip_xyz[14]
    X       = calculate_X(init_X,x,5)
    Y       = calculate_Y(init_Y,y,5)
    Z       = calculate_Z(init_Z,z)
    theta1  = calculate_theta1(X,Y,5)
    new_x   = calculate_new_x(X,Y,5)
    new_y   = calculate_new_y(X,Y,5)
    final_x = calculate_final_x(theta1,new_x,new_y,5)
    s       = calculate_s(final_x,Z)
    t3      = calculate_t3(s)
    theta3  = calculate_theta3(t3,1)
    theta2  = calculate_theta2(Z,final_x,t3,0)
    return [theta1,theta2,theta3]
def Ikine_leg6(x,y,z,endtip_xyz):
    init_X  = endtip_xyz[15]
    init_Y  = endtip_xyz[16]
    init_Z  = endtip_xyz[17]
    X       = calculate_X(init_X,x,6)
    Y       = calculate_Y(init_Y,y,6)
    Z       = calculate_Z(init_Z,z)
    theta1  = calculate_theta1(X,Y,6)
    new_x   = calculate_new_x(X,Y,6)
    new_y   = calculate_new_y(X,Y,6)
    final_x = calculate_final_x(theta1,new_x,new_y,6)
    s       = calculate_s(final_x,Z)
    t3      = calculate_t3(s)
    theta3  = calculate_theta3(t3,0)
    theta2  = calculate_theta2(Z,final_x,t3,1)
    return [theta1,theta2,theta3]
def Inverse_kinematics(x,y,z): #INPUT:  x/y/z increments of the robot body (coords)
    endtip_xyz = Forward_kinematics()
    servo_array = []
    servo_array.extend(Ikine_leg1(x,y,z,endtip_xyz))
    servo_array.extend(Ikine_leg2(x,y,z,endtip_xyz))
    servo_array.extend(Ikine_leg3(x,y,z,endtip_xyz))
    servo_array.extend(Ikine_leg4(x,y,z,endtip_xyz))
    servo_array.extend(Ikine_leg5(x,y,z,endtip_xyz))
    servo_array.extend(Ikine_leg6(x,y,z,endtip_xyz))
    return servo_array #OUTPUT: 18 servo thetas to accomplish this motion (rads)

##################################################
################FORWARD KINEMATICS################
##################################################
def calculate_ee_x(x_offset,theta1,theta2,theta3):
    return x_offset + math.cos(theta1)*(len_coxa + len_femur*math.cos(theta2) + len_tibia*math.cos(theta3+theta2))
def calculate_ee_y(y_offset,theta1,theta2,theta3):
    return y_offset + math.sin(theta1)*(len_coxa + len_femur*math.cos(theta2) + len_tibia*math.cos(theta3+theta2))
def calculate_ee_z(z_offset,theta2,theta3):
    return z_offset + len_femur*math.sin(theta2) + len_tibia*math.sin(theta3+theta2)

def Fkine_leg1(servoPos):
    theta1 = servoPos[0] + (math.pi/4)
    theta2 = servoPos[1] + ang_offset_femur
    theta3 = servoPos[2] + ang_offset_tibia
    ee_x   = calculate_ee_x(l1_x_offset,theta1,theta2,theta3)
    ee_y   = calculate_ee_y(l1_y_offset,theta1,theta2,theta3)
    ee_z   = calculate_ee_z(z_offset,theta2,theta3)
    return [ee_x,ee_y,ee_z]
def Fkine_leg2(servoPos):
    theta1 = servoPos[3] + (0.75*math.pi)
    theta2 = servoPos[4] + ang_offset_femur
    theta3 = servoPos[5] + ang_offset_tibia
    ee_x   = calculate_ee_x(l2_x_offset,theta1,theta2,theta3)
    ee_y   = calculate_ee_y(l2_y_offset,theta1,theta2,theta3)
    ee_z   = calculate_ee_z(z_offset,theta2,theta3)
    return [ee_x,ee_y,-ee_z]
def Fkine_leg3(servoPos):
    theta1 = servoPos[6]
    theta2 = servoPos[7] + ang_offset_femur
    theta3 = servoPos[8] + ang_offset_tibia
    ee_x   = calculate_ee_x(l3_x_offset,theta1,theta2,theta3)
    ee_y   = calculate_ee_y(l3_y_offset,theta1,theta2,theta3)
    ee_z   = calculate_ee_z(z_offset,theta2,theta3)
    return [ee_x,ee_y,ee_z]
def Fkine_leg4(servoPos):
    theta1 = servoPos[9]  + (math.pi)
    theta2 = servoPos[10] + ang_offset_femur
    theta3 = servoPos[11] + ang_offset_tibia
    ee_x   = calculate_ee_x(l4_x_offset,theta1,theta2,theta3)
    ee_y   = calculate_ee_y(l4_y_offset,theta1,theta2,theta3)
    ee_z   = calculate_ee_z(z_offset,theta2,theta3)
    return [ee_x,ee_y,-ee_z]
def Fkine_leg5(servoPos):
    theta1 = servoPos[12] - (math.pi/4)
    theta2 = servoPos[13] + ang_offset_femur
    theta3 = servoPos[14] + ang_offset_tibia
    ee_x   = calculate_ee_x(l5_x_offset,theta1,theta2,theta3)
    ee_y   = calculate_ee_y(l5_y_offset,theta1,theta2,theta3)
    ee_z   = calculate_ee_z(z_offset,theta2,theta3)
    return [ee_x,ee_y,ee_z]
def Fkine_leg6(servoPos):
    theta1 = servoPos[15] - (0.75*math.pi)
    theta2 = servoPos[16] + ang_offset_femur
    theta3 = servoPos[17] + ang_offset_tibia
    ee_x   = calculate_ee_x(l6_x_offset,theta1,theta2,theta3)
    ee_y   = calculate_ee_y(l6_y_offset,theta1,theta2,theta3)
    ee_z   = calculate_ee_z(z_offset,theta2,theta3)
    return [ee_x,ee_y,-ee_z]
def Forward_kinematics(): #INPUT: An array with 18 servo thetas in RADIANS
    servoPos = [(((x/2047.5)-1)*math.pi) for x in ReadAllPositions()] # Converts each ReadPosition from steps to radians
    endpoint_xyz = []
    endpoint_xyz.extend(Fkine_leg1(servoPos))
    endpoint_xyz.extend(Fkine_leg2(servoPos))
    endpoint_xyz.extend(Fkine_leg3(servoPos))
    endpoint_xyz.extend(Fkine_leg4(servoPos))
    endpoint_xyz.extend(Fkine_leg5(servoPos))
    endpoint_xyz.extend(Fkine_leg6(servoPos))
    return endpoint_xyz #OUTPUT: 6 sets of x,y,z coordinates for each leg end-tip

##################################################
################ADDITIONAL STUFF##################
##################################################
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
def DoBothKinematicsAndPrint(x,y,z):
    PrintInverse(Inverse_kinematics(x,y,z))
    PrintForward()
