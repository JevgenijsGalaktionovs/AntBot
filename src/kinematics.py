#!/usr/bin/env python
from math import pi,cos,sin,atan2,acos,sqrt,pow
from dynamixel_library import ReadAllPositions

class LegConsts(object):
    def __init__(self,x_off,y_off,z_off,ang_off,side):
        self.x_off     =  x_off           # X offset from body origin to first servo (mm)
        self.y_off     =  y_off           # Y offset from body origin to first servo (mm)
        self.z_off     =  z_off           # Z offset from body origin to first servo (mm)
        self.ang_off   =  ang_off         # Angular offset from body origin to first servo (mm)
        self.side      =  side            # Left or Right-sided leg (servo angles inverted)
        self.f_ang_off =  20.00 * pi/180  # Angular offset of Femur
        self.t_ang_off = -28.27 * pi/180  # Angular offset of Tibia
        self.c_len     =  66.50           # Link length of Coxa  (mm)
        self.f_len     =  92.17           # Link length of Femur (mm)
        self.t_len     =  193.66          # Link length of Tibia (mm)

class Kinematics(object):
    # Origin to coxa: x_off   y_off   z_off  ang_off  side
    leg1 = LegConsts( 71.6,   120.96, -17,   -pi/3, "right" )
    leg2 = LegConsts(-71.6,   120.96, -17, -2*pi/3, "left"  )
    leg3 = LegConsts( 141.33, 0,      -17,  0     , "right" )
    leg4 = LegConsts(-141.33, 0,      -17,    pi  , "left"  )
    leg5 = LegConsts( 71.6,  -120.96, -17,    pi/3, "right" )
    leg6 = LegConsts(-71.6,  -120.96, -17,  2*pi/3, "left"  )

    def calc_FKine(self, servoPos, leg):
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
        return [ee_x,ee_y,ee_z]

    def DoFKine(self):
        servoPos = [(((x/2047.5)-1) * pi) for x in ReadAllPositions()] # Converts each ReadPosition from steps to radians
        ee_xyz = []
        ee_xyz.extend(self.calc_FKine(servoPos[0:3],   self.leg1 ))
        ee_xyz.extend(self.calc_FKine(servoPos[3:6],   self.leg2 ))
        ee_xyz.extend(self.calc_FKine(servoPos[6:9],   self.leg3 ))
        ee_xyz.extend(self.calc_FKine(servoPos[9:12],  self.leg4 ))
        ee_xyz.extend(self.calc_FKine(servoPos[12:15], self.leg5 ))
        ee_xyz.extend(self.calc_FKine(servoPos[15:18], self.leg6 ))
        return ee_xyz

    def calc_IKine(self, x, y, z, ee_xyz, leg):
        print x,y,z
        init_X   = ee_xyz[0]
        init_Y   = ee_xyz[1]
        init_Z   = ee_xyz[2]
        X        = init_X + (x) - leg.x_off
        Y        = init_Y + (y) - leg.y_off
        Z        = init_Z - (z) - leg.z_off
        theta1   = atan2(Y,X)   + leg.ang_off
        if theta1 < -pi:
           theta1 += 2*pi
        if theta1 > pi:
           theta1 -= 2*pi
        new_x    = cos(leg.ang_off) * X   - sin(leg.ang_off) * Y
        new_y    = sin(leg.ang_off) * X   + cos(leg.ang_off) * Y
        final_x  = cos(theta1) * new_x    + sin(theta1) * new_y - leg.c_len
        s        = sqrt( pow(final_x,2)   + pow(Z,2) )
        t3       = pi - acos((-pow(s,2) + pow(leg.f_len,2) + pow(leg.t_len,2)) / (2 * leg.f_len * leg.t_len))
        if leg.side == "right" : # ODD LEGS
            theta3 = -t3 - leg.t_ang_off
            theta2 = -(-atan2(Z,final_x) - atan2(leg.t_len * sin(t3), leg.f_len + leg.t_len * cos(t3)) + leg.f_ang_off)
        elif leg.side == "left": # EVEN LEGS
            theta3 =  t3 + leg.t_ang_off
            theta2 = -( atan2(Z,final_x) + atan2(leg.t_len * sin(t3), leg.f_len + leg.t_len * cos(t3)) - leg.f_ang_off)
        return [theta1,theta2,theta3]

    def DoIKine(self, x, y, z):
        ee_xyz = self.DoFKine()
        thetas = []
        thetas.extend(self.calc_IKine(x, y, z, ee_xyz[0:3],   self.leg1 ))
        thetas.extend(self.calc_IKine(x, y, z, ee_xyz[3:6],   self.leg2 ))
        thetas.extend(self.calc_IKine(x, y, z, ee_xyz[6:9],   self.leg3 ))
        thetas.extend(self.calc_IKine(x, y, z, ee_xyz[9:12],  self.leg4 ))
        thetas.extend(self.calc_IKine(x, y, z, ee_xyz[12:15], self.leg5 ))
        thetas.extend(self.calc_IKine(x, y, z, ee_xyz[15:18], self.leg6 ))
        thetas = [x / pi * 2048 + 2048 for x in thetas] # Convert from pi to steps
        return thetas
        
    def PrintForward(self):
        coord_list = self.DoFKine()
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
    def PrintInverse(self, theta_list):
        RoundedThetas = [ '%.4f' % elem for elem in theta_list ]
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
    def DoBothKinematicsAndPrint(self, x,y,z):
        self.PrintForward()
        self.PrintInverse(self.DoIKine(x,y,z))
