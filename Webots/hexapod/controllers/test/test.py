#import math
import time
from math import pi, cos, sin, atan2, acos, sqrt, pow, radians
from controller import Robot, Node, Motor, PositionSensor
#from locomotion import *
#from kinematics import Kinematics

SENSOR_SAMPLE_PERIOD = 100
all_positions = []
all_touches = []
positions = []



ALL  = [1, 2, 3,   4, 5, 6,   7, 8, 9,   10, 11, 12,   13, 14, 15,   16, 17, 18]
TG_1 = [1, 2, 3,  10, 11, 12,  13, 14, 15]  # Leg 1,4,5 servo IDs "Tripod Group 1"
TG_2 = [4, 5, 6,  7,  8,  9,   16, 17, 18]  # Leg 2,3,6 servo IDs "Tripod Group 2"
l1   = [1, 2, 3]     # Leg 1
l2   = [4, 5, 6]     # Leg 2
l3   = [7, 8, 9]     # Leg 3
l4   = [10, 11, 12]  # Leg 4
l5   = [13, 14, 15]  # Leg 5
l6   = [16, 17, 18]  # Leg 6

leg = {
    1: [1, 2, 3],     # IDs Leg 1
    2: [4, 5, 6],     # IDs Leg 2
    3: [7, 8, 9],     # IDs Leg 3
    4: [10, 11, 12],  # IDs Leg 4
    5: [13, 14, 15],  # IDs Leg 5
    6: [16, 17, 18]   # IDs Leg 6
}

class LegConsts(object):
    ''' Class object to store characteristics of each leg '''
    def __init__(self, x_off, y_off, z_off, ang_off, side, leg_nr):
        self.x_off     = x_off              # X offset from body origin to first servo (mm)
        self.y_off     = y_off              # Y offset from body origin to first servo (mm)
        self.z_off     = z_off              # Z offset from body origin to first servo (mm)
        self.ang_off   = ang_off            # Angular offset from body origin to first servo (mm)
        self.side      = side               # Left or Right-sided leg (servo angles inverted)
        self.f_ang_off = 20.00 * pi / 180   # Angular offset of Femur
        self.t_ang_off = -28.27 * pi / 180  # Angular offset of Tibia
        self.c_len     = 66.50              # Link length of Coxa  (mm)
        self.f_len     = 92.17              # Link length of Femur (mm)
        self.t_len     = 193.66             # Link length of Tibia (mm)
        self.leg_nr    = leg_nr             # Leg Number


class Kinematics(object):
    ''' Class object to compute various types of kinematics data for AntBot '''
    # Origin to coxa: x_off    y_off    z_off    ang_off  side     name
    leg1 = LegConsts(71.6,     120.96, -17,    - pi / 3, "right", "Leg 1")
    leg2 = LegConsts(-71.6,    120.96, -17, -2 * pi / 3, "left",  "Leg 2")
    leg3 = LegConsts(141.33,   0,      -17,      0,      "right", "Leg 3")
    leg4 = LegConsts(-141.33,  0,      -17,      pi,     "left",  "Leg 4")
    leg5 = LegConsts(71.6,    -120.96, -17,      pi / 3, "right", "Leg 5")
    leg6 = LegConsts(-71.6,   -120.96, -17,  2 * pi / 3, "left",  "Leg 6")
    leg_list = [leg1, leg2, leg3, leg4, leg5, leg6]

    ################
    # Public methods
    ################

    def doFkine(self, all_positions):
        ''' Function:  computes forward kinematics
            Parameter: all_positions: list with 18 values of servo positions in steps from ID1 to ID18
            Return:    ee_xyz: list of x,y,z coordinates for all 6 legs
                       servoPos: servo positions in radians
        '''
        servoPos = all_positions
        ee_xyz = []
        j = 0
        for i in range(0, 16, 3):
            ee_xyz.extend(self.calc_fkine(servoPos[i:i + 3],   self.leg_list[j]))
            j += 1
        return ee_xyz, servoPos

    def doIkine(self, all_positions, x, y, z, body_orient=None, leg=None):
        ''' Function:   computes inverse kinematics
            Parameters: all_positions: list with 18 values of servo positions in steps from ID1 to ID18;
                        x,y,z: desired change in x,y,z coordinates (same for all legs)
                        body_orient: list of 3 integers meaning alpha,beta,gamma rotation in degrees
                        leg: list with integers meaning leg numbers to compute inverse for them only
            Return:     list of 18 integers with servo steps
        '''
        ee_xyz, servoPos = self.doFkine(all_positions)
        thetas = []
        j = 0

        if isinstance(leg, int):
            leg = [leg]
        elif isinstance(leg, tuple):
            leg = list(leg)
        elif isinstance(body_orient, tuple):
            body_orient = list(body_orient)
        if body_orient:
            # Optional parameter. Compute inverse with body orientation
            body_orient = [radians(d) for d in body_orient]
            alpha_rad, beta_rad, gama_rad = body_orient[0], body_orient[1], body_orient[2]
            x = (cos(gama_rad) * sin(beta_rad) * z + sin(gama_rad) * sin(beta_rad) * y + x * cos(beta_rad)) \
                * cos(alpha_rad) - sin(alpha_rad) * (cos(gama_rad) * y - sin(gama_rad) * z)
            y = (cos(gama_rad) * sin(beta_rad) * z + sin(gama_rad) * sin(beta_rad) * y + x * cos(beta_rad)) \
                * sin(alpha_rad) + cos(alpha_rad) * (cos(gama_rad) * y - sin(gama_rad) * z)
            z = -sin(beta_rad) * x + cos(beta_rad) * sin(gama_rad) * y + cos(beta_rad) * cos(gama_rad) * z

        if leg:
            # Optional parameter. Compute inverse for a specific leg/s.

            for i in range(len(leg)):
                j = leg[i] - 1
                thetas.extend(self.calc_ikine(x, y, z, ee_xyz[3 * j:3 * j + 3], self.leg_list[j]))
        else:
            # Compute inverse for all legs if not leg specified.
            for i in range(0, 16, 3):
                thetas.extend(self.calc_ikine(x, y, z, ee_xyz[i:i + 3],   self.leg_list[j]))
                j += 1

        result = [int(each_theta) for each_theta in self.rad_to_step(thetas)]
        return result

    def doIkineRotationEuler(self, all_positions, alpha_rad, beta_rad, gama_rad, dist_x, dist_y, dist_z):
        ''' Function:   computes inverse kinematics and body rotation (Parallel kinematics)
            Parameters: all_positions: list with 18 values of servo positions in steps from ID1 to ID18;
                        alpha,beta,gama: desired degree change in x,y,z coordinates of robot's body
                        dist_x,dist_y,dist_z : desired translation along x,y,z of body
            Return:     list of 18 integers with servo steps
        '''
        final_eexyz, ee_xyz = self.calc_rot_matrix(all_positions, alpha_rad, beta_rad, gama_rad)
        thetas = []
        j = 0
        for i in range(0, 16, 3):
            thetas.extend(self.calc_ikine(final_eexyz[i] - dist_x, final_eexyz[i + 1] - dist_y, final_eexyz[i + 2] - dist_z, ee_xyz[i:i + 3], self.leg_list[j]))
            j += 1
        result = [int(each_theta) for each_theta in self.rad_to_step(thetas)]
        return result

    def printForward(self, all_positions):
        ''' Function:   Prints x,y,z coordinates of each leg
            Parameters: all_positions: list with 18 values of servo positions in steps from ID1 to ID18;
        '''
        ee_list, theta_list = self.doFkine(all_positions)
        RoundedCoords = ['%.4f' % elem for elem in ee_list]
        print ("")
        print ("X,Y,Z coordinates of Leg end-points: ")
        print ("       " + str(["X       ", " Y    ", "  Z   "]))
        print ("Leg 1: " + str(RoundedCoords[0:3]))
        print ("Leg 2: " + str(RoundedCoords[3:6]))
        print ("Leg 3: " + str(RoundedCoords[6:9]))
        print ("Leg 4: " + str(RoundedCoords[9:12]))
        print ("Leg 5: " + str(RoundedCoords[12:15]))
        print ("Leg 6: " + str(RoundedCoords[15:18]))
        print ("")

    def printInverse(self, theta_list):
        ''' Function:   Prints servo positions, in radians, needed to reach the position
            Parameters: theta_list: 18 servo positions in radians.
        '''
        RoundedThetas = ['%.4f' % elem for elem in theta_list]
        print ("")
        print ("Theta angles of each servo:")
        print ("       " + str(["Coxa    ", "Femur ", "Tibia"]))
        print ("Leg 1: " + str(RoundedThetas[0:3]))
        print ("Leg 2: " + str(RoundedThetas[3:6]))
        print ("Leg 3: " + str(RoundedThetas[6:9]))
        print ("Leg 4: " + str(RoundedThetas[9:12]))
        print ("Leg 5: " + str(RoundedThetas[12:15]))
        print ("Leg 6: " + str(RoundedThetas[15:18]))
        print ("")

    def printKinematics(self, all_positions, x, y, z):
        self.printForward(all_positions)
        self.printInverse(self.doIkine(all_positions, x, y, z))

    #################
    # Private methods
    #################

    def calc_fkine(self, servoPos, leg):
        theta1 = servoPos[0] - leg.ang_off
        #if leg.side == "right":
        theta2 = servoPos[1] + leg.f_ang_off
        theta3 = servoPos[2] + leg.t_ang_off
        ee_z   = leg.f_len * sin(theta2) + leg.t_len * sin(theta3 + theta2) + leg.z_off
        #elif leg.side == "left":
        #    theta2 = servoPos[1] - leg.f_ang_off
        #    theta3 = servoPos[2] - leg.t_ang_off
        #    ee_z   = -(leg.f_len * sin(theta2) + leg.t_len * sin(theta3 + theta2) - leg.z_off)
        ee_x   = leg.x_off + cos(theta1) * (leg.c_len + leg.f_len * cos(theta2) + leg.t_len * cos(theta3 + theta2))
        ee_y   = leg.y_off + sin(theta1) * (leg.c_len + leg.f_len * cos(theta2) + leg.t_len * cos(theta3 + theta2))
        return [ee_x, ee_y, ee_z]

    def calc_ikine(self, x, y, z, ee_xyz, leg):
        init_X   = ee_xyz[0]
        init_Y   = ee_xyz[1]
        init_Z   = ee_xyz[2]
        X        = init_X + (x) - leg.x_off
        Y        = init_Y + (y) - leg.y_off
        Z        = init_Z + (z) - leg.z_off
        theta1   = atan2(Y, X)   + leg.ang_off
        if theta1 < -pi:
            theta1 += 2 * pi
        if theta1 > pi:
            theta1 -= 2 * pi
        new_x    = cos(leg.ang_off) * X   - sin(leg.ang_off) * Y
        new_y    = sin(leg.ang_off) * X   + cos(leg.ang_off) * Y
        final_x  = cos(theta1) * new_x    + sin(theta1) * new_y - leg.c_len
        s        = sqrt(pow(final_x, 2)   + pow(Z, 2))
        try:
            t3_term = (-pow(s, 2) + pow(leg.f_len, 2) + pow(leg.t_len, 2)) / (2 * leg.f_len * leg.t_len)
            t3       = pi - acos(t3_term)
        except ValueError:
            print ("Cannot compute acos(", t3_term, ") for ", leg.leg_nr)
            if t3_term < 0:
                t3 = pi - acos(-0.99)
            else:
                t3 = pi - acos(0.99)
        #if leg.side == "right":  # ODD LEGS
        theta3 = -t3 - leg.t_ang_off
        theta2 = -(-atan2(Z, final_x) - atan2(leg.t_len * sin(t3), leg.f_len + leg.t_len * cos(t3)) + leg.f_ang_off)
        #elif leg.side == "left":  # EVEN LEGS
        #theta3 = t3 + leg.t_ang_off
        #theta2 = -(atan2(Z, final_x) + atan2(leg.t_len * sin(t3), leg.f_len + leg.t_len * cos(t3)) - leg.f_ang_off)
        return [theta1, theta2, theta3]

    def calc_rot_displacement(self, alpha_rad, beta_rad, gama_rad, ee_xyz):
        pre_x = ee_xyz[0]
        pre_y = ee_xyz[1]
        pre_z = ee_xyz[2]
        r_term1 = (cos(gama_rad) * sin(beta_rad) * pre_z + sin(gama_rad) * sin(beta_rad) * pre_y + pre_x * cos(beta_rad))
        r_term2 = (cos(gama_rad) * pre_y - sin(gama_rad) * pre_z)
        r_x = r_term1 * cos(alpha_rad) - r_term2 * sin(alpha_rad) - pre_x
        r_y = r_term1 * sin(alpha_rad) + r_term2 * cos(alpha_rad) - pre_y
        r_z = - sin(beta_rad) * pre_x + cos(beta_rad) * sin(gama_rad) * pre_y + cos(beta_rad) * cos(gama_rad) * pre_z - pre_z
        return [r_x, r_y, r_z]

    def calc_rot_matrix(self, all_positions, alpha_rad, beta_rad, gama_rad):
        ee_xyz, servoPos = self.doFkine(all_positions)
        rot_val_list = []
        for i in range(0, 16, 3):
            rot_val_list.extend(self.calc_rot_displacement(alpha_rad, beta_rad, gama_rad, ee_xyz[i:i + 3]))
        return rot_val_list, ee_xyz

    def rad_to_step(self, pos_rads):
        return [i / pi * 2048 + 2048 for i in pos_rads]

    def step_to_rad(self, pos_steps):
        return [(((x / 2047.5) - 1) * pi) for x in pos_steps]

###########################################################################################################################

def standUp():
    #front_legs  = [1, 2, 3,  4, 5, 6]
    #rear_legs   = [13, 14, 15,  16, 17, 18]
    #middle_legs = [7, 8, 9,  10, 11, 12]
    #standup_pos = [2048, -2218, 1024,   
    #               2048, -1878, 3048,
    #               2048, -2218, 1024,   
    #               2048, -1878, 3048,
    #               2048, -2218, 1024,   
    #               2048, -1878, 3048]  
    standup_pos = [0.00, -0.26, 1.07,    
                   0.00, -0.26, 1.07,   
                   0.00, -0.26, 1.07,    
                   0.00, -0.26, 1.07,
                   0.00, -0.26, 1.07,
                   0.00, -0.26, 1.07]
    #front_standup  = list_combine(front_legs, standup_pos)
    #rear_standup   = list_combine(rear_legs, standup_pos)
    #middle_standup = list_combine(middle_legs, standup_pos)
    #positions = K.step_to_rad(standup_pos)
    positions = standup_pos
    C.positionN(positions) # was front_standup in non-simulation
    #time.sleep(1)
    #C.positionN(rear_standup)
    #time.sleep(1)
    #C.positionN(_middle_standup)
    #time.sleep(1)


def parallelGait(alpha, beta, gamma, dist_x, dist_y, dist_z):
    alpha_rad = alpha * pi / 180
    beta_rad  = beta  * pi / 180
    gamma_rad = gamma * pi / 180
    current_pos = C.readPos()
    next_pos = K.doIkineRotationEuler(current_pos, alpha_rad, beta_rad, gamma_rad, dist_x, dist_y, dist_z)
    #scaler = [50] * 18
    #velocityAll(scaler)
    #accelerationAll(scaler)
    next_pos = K.step_to_rad(next_pos)
    print(next_pos)
    C.positionN(next_pos)
    #time.sleep(0.35)


def translationZ(distance):
    pos = [0, 0, distance]
    do_motion(pos, ALL)


def yawRotation(degrees):
    delay = 0.3
    alpha_rad   = degrees * pi / 180

    do_motion([0, 0, 20], TG_2)
    #time.sleep(delay)

    current_pos = C.readPos()
    next_pos    = K.doIkineRotationEuler(current_pos, alpha_rad, 0, 0, 0, 0, 0)
    #pos_list    = list_combine(TG_1, next_pos)
    positions = next_pos
    C.positionN(positions)
    #time.sleep(delay)

    do_motion([0, 0, -20], TG_2)
    #time.sleep(delay)

    do_motion([0, 0, 20], TG_1)
    #time.sleep(delay)
    
    positions = C.readPos()
    positions[0]  = K.step_to_rad(2048)
    positions[9]  = K.step_to_rad(2048)
    positions[12] = K.step_to_rad(2048)
    C.positionN(positions) # Converted to radians, old was [1, 2048, 10, 2048, 13, 2048] steps
    #time.sleep(delay)

    #final_pos = list_combine(TG_1, current_pos)
    positions = current_pos
    C.positionN(positions)
    #time.sleep(delay)


def rippleGait(x, y, z, iterations):
    init_pos = C.readPos()
    delay = 0.3

    move1 = [x, y, z]
    move2 = [-x / 2, -y / 2, 0]
    move3 = [0, 0, -z]

    for i in range(iterations):

        do_motion(move1, l1 + l4)
        do_motion(move2, l2 + l3 + l5 + l6)
        #time.sleep(delay)
        do_motion(move3, l1 + l4)
        #time.sleep(delay)

        do_motion(move1, l3 + l6)
        do_motion(move2, l1 + l2 + l4 + l5)
        #time.sleep(delay)
        do_motion(move3, l3 + l6)
        #time.sleep(delay)

        do_motion(move1, l2 + l5)
        do_motion(move2, l1 + l3 + l4 + l6)
        #time.sleep(delay)
        do_motion(move3, l2 + l5)
        #time.sleep(delay)

        C.positionN(init_pos) # was positionAll(init_pos) for non-simulation
        #time.sleep(delay)


def waveGait(x, y, z, iterations):
    init_pos = C.readPos()
    delay = 0.1

    one_leg_motion_up  = [x, y, z]
    one_leg_motion_down  = [0, 0, -z]
    five_leg_motion = [-x / 6, -y / 6, 0]
    for i in range(iterations):

        do_motion(one_leg_motion_up, l1)
        do_motion(five_leg_motion, l2 + l3 + l4 + l5 + l6)
        #time.sleep(delay)

        do_motion(one_leg_motion_down, l1)
        do_motion(one_leg_motion_up, l3)
        do_motion(five_leg_motion, l2 + l4 + l5 + l6)
        #time.sleep(delay)

        do_motion(one_leg_motion_down, l3)
        do_motion(one_leg_motion_up, l5)
        do_motion(five_leg_motion, l1 + l2 + l4 + l6)
        #time.sleep(delay)

        do_motion(one_leg_motion_down, l5)
        do_motion(one_leg_motion_up, l2)
        do_motion(five_leg_motion, l1 + l3 + l4 + l6)
        #time.sleep(delay)

        do_motion(one_leg_motion_down, l2)
        do_motion(one_leg_motion_up, l4)
        do_motion(five_leg_motion, l1 + l3 + l5 + l6)
        #time.sleep(delay)

        do_motion(one_leg_motion_down, l4)
        do_motion(one_leg_motion_up, l6)
        do_motion(five_leg_motion, l1 + l2 + l3 + l5)
        #time.sleep(delay)

        C.positionN(init_pos) #was positionAll(init_pos) for non-simulation
        #time.sleep(delay)


def tripodGait(x, y, z, iterations):

    start_pos = tripodGait_start(x, y, z)
    tripodGait_full(x, y, z, iterations, start_pos=start_pos)
    tripodGait_finish(x, y, z)


def tripodGait_start(x, y, z):
    delay = 0.2

    TG1_m1 = [-x, -y,  0]  # Tripod Group 1 : Motion 1

    TG2_m1 = [x,  y,  z]   # Tripod Group 2 : Motion 1
    TG2_m2 = [0,  0, -z]   # Tripod Group 2 : Motion 2

    # Motion 1
    do_motion(TG2_m1, TG_2)
    do_motion(TG1_m1, TG_1)
    #time.sleep(delay)
    # Motion 2
    do_motion(TG2_m2, TG_2)
    #time.sleep(delay)
    start_pos = C.readPos()
    return start_pos


def tripodGait_full(x, y, z, iterations, start_pos=None):
    delay = 0.2

    # init_pos = [2048, 2218, 1024,   2048, 1878, 3048,
    #             2048, 2218, 1024,   2048, 1878, 3048,
    #             2048, 2218, 1024,   2048, 1878, 3048]
    if start_pos:
        init_pos = start_pos
    else:                                                  # old values in steps
        init_pos = [2002, 2218, 957, 2012, 1918, 2971, 2127, 2200, 1027, 2123, 1887, 3048, 2011, 2188, 1097, 2003, 1872, 3120]
        #init_pos = [-0.06981317,  0.26160759, -1.67321454, # 2002, 2218, 957,
        #            -0.05446961, -0.19869902,  1.41697719, # 2012, 1918, 2971,
        #             0.12198125,  0.23398919, -1.56580967, # 2127, 2200, 1027,
        #             0.11584383, -0.24626403,  1.53512256, # 2123, 1887, 3048,
        #            -0.05600397,  0.21557693, -1.45840479, # 2011, 2188, 1097,
        #            -0.06827881, -0.26927937,  1.64559615] # 2003, 1872, 3120]
    for i in range(iterations):

        TG1_m1 = [2 * x,  2 * y,  z]   # Tripod Group 1 : Motion 1
        TG1_m2 = [0,  0, -z]           # Tripod Group 1 : Motion 2
        TG1_m3 = [-2 * x, -2 * y,  0]  # Tripod Group 1 : Motion 3

        TG2_m1 = [-2 * x, -2 * y,  0]  # Tripod Group 2 : Motion 1
        TG2_m3 = [2 * x, 2 * y,  z]    # Tripod Group 2 : Motion 3
        TG2_m4 = [0,  0, -z]           # Tripod Group 1 : Motion 4

        # Motion 1
        do_motion(TG1_m1, TG_1)
        #time.sleep(0.05)
        do_motion(TG2_m1, TG_2)
        #time.sleep(delay)

        # Motion 2
        do_motion(TG1_m2, TG_1)
        #time.sleep(delay)

        # Motion 3
        do_motion(TG2_m3, TG_2)
        #time.sleep(0.05)
        do_motion(TG1_m3, TG_1)
        #time.sleep(delay)

        # Motion 4
        do_motion(TG2_m4, TG_2)
        #time.sleep(delay)

        # Motion 5
        #positions = K.step_to_rad(init_pos)
        C.positionN(init_pos)
        #time.sleep(delay)


def tripodGait_finish(x, y, z):
    delay = 0.15

    TG1_m1 = [0,  0,  z]   # Tripod Group 1 : Motion 1
    TG1_m2 = [x,  y,  0]   # Tripod Group 1 : Motion 2
    TG1_m3 = [0,  0, -z]   # Tripod Group 1 : Motion 3

    TG2_m4 = [0,  0,  z]   # Tripod Group 2 : Motion 4
    TG2_m5 = [-x, -y,  0]  # Tripod Group 2 : Motion 5
    TG2_m6 = [0,  0, -z]   # Tripod Group 2 : Motion 6
    # Motion 1
    do_motion(TG1_m1, TG_1)
    #time.sleep(delay)

    # Motion 2
    do_motion(TG1_m2, TG_1)
    #time.sleep(delay)

    # Motion 3
    do_motion(TG1_m3, TG_1)
    #time.sleep(delay)

    # Motion 4
    do_motion(TG2_m4, TG_2)
    #time.sleep(delay)

    # Motion 5
    do_motion(TG2_m5, TG_2)
    #time.sleep(delay)

    # Motion 6
    do_motion(TG2_m6, TG_2)
    #time.sleep(delay)


#def stepDown(leg_case):
#    j = int(leg_case - 1)
#    for x in range(40):
#        tac = allTactiles()
#        tac_oneleg = tac[j]
#        if tac_oneleg == 0:
#            init_pos = C.readPos()
#            steps = K.doIkine(init_pos, 0, 0, -5, leg=leg_case)
#            position1(3 * j + 2, steps[3 * j + 1])
#            position1(3 * j + 3, steps[3 * j + 2])
#            time.sleep(0.3)
#        else:
#            return


def list_combine(id_list, value_list):
    ''' Parameters: id_list: list of servo IDs (any order, any number of IDs from 1 to 18)
                    value_list: list of 18 values.
        Return:     list of format: [ID_1, Value_1, ... , ID_n, Value_n]
    '''
    sr_count = 0
    output = [0] * 2 * len(id_list)  # output size must be:  # of servos * 2 (ID + VALUE)
    for x in range(len(id_list)):
        output[x + sr_count] = id_list[x]
        output[x + sr_count + 1] = value_list[id_list[x] - 1]
        sr_count += 1
    return output


def calc_scaler(thetas):
    return [i * 1 for i in thetas]


def do_motion(xyz_list, ID_list, orientation=None):
    """Parameters: xyz_list: list of 3 integers with x,y,z changes to accomplish
                   ID_list:  list of servo IDs
                   orientaiton: list of 3 rotation integers in degrees. alpha,beta,gama
       Example call  : do_motion([0, 30, 20], [7, 8, 9])
       Example result: Position of servo ID7, ID8 and ID9 (Leg 3) will be
                       changed to reach end-tip x= +0, y= +30 and z= +20"""
    current_pos = C.readPos()
    #print(current_pos)
    if orientation:
        next_pos = K.doIkine(current_pos, xyz_list[0], xyz_list[1],
                             xyz_list[2], body_orient=orientation)
    else:
        next_pos = K.doIkine(current_pos, xyz_list[0], xyz_list[1],
                             xyz_list[2])

    #scaler = calc_scaler(next_pos)
    #vel_acc_value = list_combine(ID_list, scaler)
    #velocityN(vel_acc_value)  # Setting same vel/acc = Trapezoid trajectory
    #accelerationN(vel_acc_value)

    #motion = list_combine(ID_list, next_pos)
    #print(motion) # just for debugging
    
    
    positions = K.step_to_rad(next_pos)
    #print(positions) # just for debugging
    C.positionN(positions)


def singleLeg(x, y, z, alpha, beta, gama, leg_case):
    ID_list = leg[leg_case]
    do_motion([x, y, z], ID_list, orientation=[alpha, beta, gama])


def rippleMirror(x, y, z, alpha, beta, gama, leg_pair):
    if leg_pair == 1:  # Front legs
        legs = leg[1] + leg[2]
    elif leg_pair == 2:  # Middle legs
        legs = leg[3] + leg[4]
    elif leg_pair == 3:  # Rear legs
        legs = leg[5] + leg[6]
    else:
        raise ValueError('leg_pair value must be 1,2 or 3. Your value:', leg_pair)

    do_motion([x, y, z], legs, orientation=[alpha, beta, gama])
    do_motion([-x, y, z], legs, orientation=[alpha, beta, gama])


###########################################################################################################################


class Controller():

    jointNames = [
       # coxa,  femur, tibia
        'c1',  'f1',  't1',  # LEG 1
        'c2',  'f2',  't2',  # LEG 2
        'c3',  'f3',  't3',  # LEG 3
        'c4',  'f4',  't4',  # LEG 4
        'c5',  'f5',  't5',  # LEG 5
        'c6',  'f6',  't6']  # LEG 6

    touchNames = [
        'f1',  'f2',  'f3',
        'f4',  'f5',  'f6']

    def __init__(self):
        # Initialize the Webots Supervisor.
        self.robot = Robot()
        self.timeStep = int(4 * self.robot.getBasicTimeStep())
        self.keyboard = self.robot.getKeyboard()

        # Define list for motors and position sensors
        self.motors = []
        self.position_sensors = []
        self.touch_sensors = []
        # Initialise the motors and position sensors (could be moved into __init__ into a single for-loop)
        self.init_motors()
        self.init_positional_sensors()
        self.init_touching_sensors()

    def init_motors(self):
        for name in Controller.jointNames:
            motor = self.robot.getMotor(name + '_motor')
            # motor.setPosition(float('inf'))
            # motor.setVelocity(0)
            self.motors.append(motor)

    def init_positional_sensors(self):
        for name in Controller.jointNames:
            positional_sensor = self.robot.getPositionSensor(name + '_position_sensor')
            positional_sensor.enable(SENSOR_SAMPLE_PERIOD)
            self.position_sensors.append(positional_sensor)

    def init_touching_sensors(self):
        for name in Controller.jointNames[1::3]:
            touching_sensor = self.robot.getTouchSensor(name + '_touch_sensor')
            touching_sensor.enable(SENSOR_SAMPLE_PERIOD)
            self.touch_sensors.append(touching_sensor)

    # Test initialiser before I got the other version working.
    #def init_touching_sensors(self):
    #    for name in Controller.touchNames:
    #        touching_sensor = self.robot.getTouchSensor(name + '_touch_sensor')
    #        touching_sensor.enable(SENSOR_SAMPLE_PERIOD)
    #        self.touch_sensors.append(touching_sensor)

    def positionN(self, positions):
        #if ID_list:
        #    while self.robot.step(self.timeStep != 1:
        #        for i in ID_list
        #        
        #else:
        while self.robot.step(self.timeStep) != 1:
            for motor, position in zip(self.motors, positions):
                motor.setPosition(position)
            C.reachedPos(positions)
            break

    def readPos(self):
        all_positions = []
        valuePos = []
        while self.robot.step(self.timeStep) != 1:
            for i in range(len(self.jointNames)):
                valuePos = self.position_sensors[i].getValue()
                all_positions.append(valuePos)
            #print(all_positions)   # just for debugging
            return all_positions

    def readTouch(self):
        all_touches = []
        valueTouch = []
        while self.robot.step(self.timeStep) != 1:
            for i in range(len(self.jointNames[1::3])):
                valueTouch = self.touch_sensors[i].getValue()
                all_touches.append(valueTouch)
            #print(all_touches)   # just for debugging
            return all_touches

    def reachedPos(self, positions):
        all_positions = []
        while all_positions != positions:
            #self.robot.step(1)
            #all_positions = C.readPos() #old version without rounding to nearest 2nd decimal
            all_positions = [round(x, 2) for x in C.readPos()]
            positions = [round(y, 2) for y in positions]
            #print(all_positions)   # just for debugging
            #print(positions)       # just for debugging

    def walk(self):
        standUp()
        #tripodGait(0, 20, 10, 1)
        #waveGait(0, 20, 10, 1)
        #translationZ(50)
        #parallelGait(50, 0, 0, 0, 0, 0)
        


if __name__ == "__main__":
    C = Controller()
    K = Kinematics()
    
    #positions = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    #C.positionN(positions)
    #positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #C.positionN(positions)
    
    # Function for measuring contact
    #C.readTouch()
    id = [1, 2, 3]
    new = [x - 1 for x in id] 
    print(new)
    C.walk()
    
    print(C)