# !/usr/bin/env python2
from math import pi, cos, sin, atan2, acos, sqrt, pow, radians


class LegConsts(object):
    ''' Class object to store characteristics of each leg '''
    def __init__(self, x_off, y_off, z_off, ang_off, side, leg_nr):
        self.x_off     = x_off              # X offset from body origin to first servo (mm)
        self.y_off     = y_off              # Y offset from body origin to first servo (mm)
        self.z_off     = z_off              # Z offset from body origin to first servo (mm)
        self.ang_off   = ang_off            # Angular offset from body origin to first servo (mm)
        self.side      = side               # Left or Right-sided leg (servo angles inverted)
        self.f_ang_off = 20.00 * pi / 180   # Angular offset of Femur
        self.t_ang_off = -32.264 * pi / 180  # Angular offset of Tibia
        self.c_len     = 66.50              # Link length of Coxa  (mm)
        self.f_len     = 92.17              # Link length of Femur (mm)
        self.t_len     = 194.00             # Link length of Tibia (mm)
        self.leg_nr    = leg_nr             # Leg Number


class Kinematics(object):
    ''' Class object to compute various types of kinematics data for AntBot '''
    # Origin to coxa: x_off    y_off    z_off    ang_off  side     name
    leg1 = LegConsts(71.6,     120.96, -14.9,    - pi / 3, "right", "Leg 1")
    leg2 = LegConsts(-71.6,    120.96, -14.9, -2 * pi / 3, "left",  "Leg 2")
    leg3 = LegConsts(141.33,   0,      -14.9,      0,      "right", "Leg 3")
    leg4 = LegConsts(-141.33,  0,      -14.9,      pi,     "left",  "Leg 4")
    leg5 = LegConsts(71.6,    -120.96, -14.9,      pi / 3, "right", "Leg 5")
    leg6 = LegConsts(-71.6,   -120.96, -14.9,  2 * pi / 3, "left",  "Leg 6")
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
        servoPos = self.step_to_rad(all_positions)
        ee_xyz = []
        j = 0
        for i in xrange(0, 16, 3):
            ee_xyz.extend(self.calc_fkine(servoPos[i:i + 3],   self.leg_list[j]))
            j += 1
        return ee_xyz, servoPos

    def doIkine(self, all_positions, x, y, z, body_orient=None, leg=None, auto=None):
        print("1.leg is:",leg )
        leg = leg
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
            print("2.leg is:",leg )
            for i in range(len(leg)):
                print("3.leg is:",leg )
                print("i :",i , leg[i] )
                j = leg[i] - 1
                print(j)
                thetas.extend(self.calc_ikine(x, y, z, ee_xyz[3 * j:3 * j + 3], self.leg_list[j]))
        else:
            # Compute inverse for all legs if not leg specified.
            for i in xrange(0, 16, 3):
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
        for i in xrange(0, 16, 3):
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
        print ""
        print "X,Y,Z coordinates of Leg end-points: "
        print "       " + str(["X       ", " Y    ", "  Z   "])
        print "Leg 1: " + str(RoundedCoords[0:3])
        print "Leg 2: " + str(RoundedCoords[3:6])
        print "Leg 3: " + str(RoundedCoords[6:9])
        print "Leg 4: " + str(RoundedCoords[9:12])
        print "Leg 5: " + str(RoundedCoords[12:15])
        print "Leg 6: " + str(RoundedCoords[15:18])
        print ""

    def printInverse(self, theta_list):
        ''' Function:   Prints servo positions, in radians, needed to reach the position
            Parameters: theta_list: 18 servo positions in radians.
        '''
        RoundedThetas = ['%.4f' % elem for elem in theta_list]
        print ""
        print "Theta angles of each servo:"
        print "       " + str(["Coxa    ", "Femur ", "Tibia"])
        print "Leg 1: " + str(RoundedThetas[0:3])
        print "Leg 2: " + str(RoundedThetas[3:6])
        print "Leg 3: " + str(RoundedThetas[6:9])
        print "Leg 4: " + str(RoundedThetas[9:12])
        print "Leg 5: " + str(RoundedThetas[12:15])
        print "Leg 6: " + str(RoundedThetas[15:18])
        print ""

    def printKinematics(self, all_positions, x, y, z):
        self.printForward(all_positions)
        self.printInverse(self.doIkine(all_positions, x, y, z))

    #################
    # Private methods
    #################

    def calc_fkine(self, servoPos, leg):
        theta1 = servoPos[0] - leg.ang_off
        if leg.side == "right":
            theta2 = servoPos[1] + leg.f_ang_off
            theta3 = servoPos[2] + leg.t_ang_off
            ee_z   = leg.f_len * sin(theta2) + leg.t_len * sin(theta3 + theta2) + leg.z_off
        elif leg.side == "left":
            theta2 = servoPos[1] - leg.f_ang_off
            theta3 = servoPos[2] - leg.t_ang_off
            ee_z   = -(leg.f_len * sin(theta2) + leg.t_len * sin(theta3 + theta2) - leg.z_off)
        ee_x   = leg.x_off + cos(theta1) * (leg.c_len + leg.f_len * cos(theta2) + leg.t_len * cos(theta3 + theta2))
        ee_y   = leg.y_off + sin(theta1) * (leg.c_len + leg.f_len * cos(theta2) + leg.t_len * cos(theta3 + theta2))
        return [ee_x, ee_y, ee_z]

    def calc_ikine(self, x, y, z, ee_xyz, leg, auto=None):
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
            print "Cannot compute acos(", t3_term, ") for ", leg.leg_nr
            if auto is None:
                print("something went wrong")
                if t3_term < 0:
                    t3 = pi - acos(-0.99)
                else:
                    t3 = pi - acos(0.99)
            else:
                print("im here dont worry")
            return -1


        if leg.side == "right":  # ODD LEGS
            theta3 = -t3 - leg.t_ang_off
            theta2 = -(-atan2(Z, final_x) - atan2(leg.t_len * sin(t3), leg.f_len + leg.t_len * cos(t3)) + leg.f_ang_off)
        elif leg.side == "left":  # EVEN LEGS
            theta3 = t3 + leg.t_ang_off
            theta2 = -(atan2(Z, final_x) + atan2(leg.t_len * sin(t3), leg.f_len + leg.t_len * cos(t3)) - leg.f_ang_off)

        #if theta2 > 1.9877574030405747 or theta2 < -1.9877574030405747 :
        #    if theta3 < -2.3575370511554175 or theta3 > 2.3575370511554175 :
        #        return -1
        #
        #else:
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
        for i in xrange(0, 16, 3):
            rot_val_list.extend(self.calc_rot_displacement(alpha_rad, beta_rad, gama_rad, ee_xyz[i:i + 3]))
        return rot_val_list, ee_xyz

    def rad_to_step(self, pos_rads):
        return [i / pi * 2048 + 2048 for i in pos_rads]

    def step_to_rad(self, pos_steps):
        return [(((x / 2047.5) - 1) * pi) for x in pos_steps]
