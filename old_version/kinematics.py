
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
        return ee_xyz,servoPos

    def calc_IKine(self, x, y, z, ee_xyz, leg):
        init_X   = ee_xyz[0]
        init_Y   = ee_xyz[1]
        init_Z   = ee_xyz[2]
        X        = init_X + (x) - leg.x_off
        Y        = init_Y + (y) - leg.y_off
        Z        = init_Z + (z) - leg.z_off
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
        if t3 :
            if leg.side == "right": # ODD LEGS
                theta3 = -t3 - leg.t_ang_off
                theta2 = -(-atan2(Z,final_x) - atan2(leg.t_len * sin(t3), leg.f_len + leg.t_len * cos(t3)) + leg.f_ang_off)
            elif leg.side == "left": # EVEN LEGS
                theta3 =  t3 + leg.t_ang_off
                theta2 = -( atan2(Z,final_x) + atan2(leg.t_len * sin(t3), leg.f_len + leg.t_len * cos(t3)) - leg.f_ang_off)
            return [theta1,theta2,theta3]
        else :
            t3 =  acos((pow(s,2) - pow(leg.f_len,2) - pow(leg.t_len,2)) / (2 * leg.f_len * leg.t_len))
            print("t3 doesnt exists")
            if leg.side == "right": # ODD LEGS
                theta3 = -t3 - leg.t_ang_off
                theta2 = -(-atan2(Z,final_x) - atan2(leg.t_len * sin(t3), leg.f_len + leg.t_len * cos(t3)) + leg.f_ang_off)
            elif leg.side == "left": # EVEN LEGS
                theta3 =  t3 + leg.t_ang_off
                theta2 = -( atan2(Z,final_x) + atan2(leg.t_len * sin(t3), leg.f_len + leg.t_len * cos(t3)) - leg.f_ang_off)
            return [theta1,theta2,theta3]

    def DoIKine(self, x, y, z,alpha,beta,gama, switcher):
        alpha_rad = alpha*pi/180
        beta_rad = beta*pi/180
        gama_rad = gama*pi/180
        r_x = (cos(gama_rad)*sin(beta_rad)*z+ sin(gama_rad)*sin(beta_rad)*y+x*cos(beta_rad))*cos(alpha_rad)-sin(alpha_rad)*(cos(gama_rad)*y-sin(gama_rad)*z)
        r_y = (cos(gama_rad)*sin(beta_rad)*z + sin(gama_rad)*sin(beta_rad)*y+x*cos(beta_rad))*sin(alpha_rad)+cos(alpha_rad)*(cos(gama_rad)*y-sin(gama_rad)*z)
        r_z = -sin(beta_rad)*x+cos(beta_rad)*sin(gama_rad)*y+cos(beta_rad)*cos(gama_rad)*z
        ee_xyz,servoPos = self.DoFKine()
        thetas = []
        if switcher == 0:
            thetas.extend(self.calc_IKine(r_x, r_y, r_z, ee_xyz[0:3],   self.leg1 ))
            thetas.extend(self.calc_IKine(r_x, r_y, r_z, ee_xyz[3:6],   self.leg2 ))
            thetas.extend(self.calc_IKine(r_x, r_y, r_z, ee_xyz[6:9],   self.leg3 ))
            thetas.extend(self.calc_IKine(r_x, r_y, r_z, ee_xyz[9:12],  self.leg4 ))
            thetas.extend(self.calc_IKine(r_x, r_y, r_z, ee_xyz[12:15], self.leg5 ))
            thetas.extend(self.calc_IKine(r_x, r_y, r_z, ee_xyz[15:18], self.leg6 ))

        elif switcher == 1:
            thetas.extend(self.calc_IKine(x, y, z, ee_xyz[0:3],   self.leg1 ))
            thetas.extend(servoPos[3:6])
            thetas.extend(servoPos[6:9])
            thetas.extend(servoPos[9:12])
            thetas.extend(servoPos[12:15])
            thetas.extend(servoPos[15:18])

        elif switcher == 2:
            thetas.extend(servoPos[0:3])
            thetas.extend(self.calc_IKine(x, y, z, ee_xyz[3:6],   self.leg2 ))
            thetas.extend(servoPos[6:9])
            thetas.extend(servoPos[9:12])
            thetas.extend(servoPos[12:15])
            thetas.extend(servoPos[15:18])
        elif switcher == 3:
            thetas.extend(servoPos[0:3])
            thetas.extend(servoPos[3:6])
            thetas.extend(self.calc_IKine(x, y, z, ee_xyz[6:9],   self.leg3 ))
            thetas.extend(servoPos[9:12])
            thetas.extend(servoPos[12:15])
            thetas.extend(servoPos[15:18])
        elif switcher == 4:
            thetas.extend(servoPos[0:3])
            thetas.extend(servoPos[3:6])
            thetas.extend(servoPos[6:9])
            thetas.extend(self.calc_IKine(x, y, z, ee_xyz[9:12],   self.leg4 ))
            thetas.extend(servoPos[12:15])
            thetas.extend(servoPos[15:18])
        elif switcher == 5:
            thetas.extend(servoPos[0:3])
            thetas.extend(servoPos[3:6])
            thetas.extend(servoPos[6:9])
            thetas.extend(servoPos[9:12])
            thetas.extend(self.calc_IKine(x, y, z, ee_xyz[12:15],   self.leg5 ))
            thetas.extend(servoPos[15:18])
        elif switcher == 6:
            thetas.extend(servoPos[0:3])
            thetas.extend(servoPos[3:6])
            thetas.extend(servoPos[6:9])
            thetas.extend(servoPos[9:12])
            thetas.extend(servoPos[12:15])
            thetas.extend(self.calc_IKine(x, y, z, ee_xyz[15:18],   self.leg6 ))


        thetas = [x / pi * 2048 + 2048 for x in thetas] # Convert from pi to steps
        return thetas


    def PrintForward(self,t):
        coord_list,servo_pos = self.DoFKine()
        RoundedCoords = coord_list
        # pos = ReadAllPositions()
        # print(RoundedCoords[0],RoundedCoords[1],RoundedCoords[2],pos[0],pos[1],pos[2],t)
        print ""
        print "X,Y,Z coordinates of Leg end-points: "
        print "       " +  str(["X       ", " Y    ", "  Z   "])
        print "Leg 1: " +  str(RoundedCoords[0:3])
        print "Leg 2: " +  str(RoundedCoords[3:6])
        print "Leg 3: " +  str(RoundedCoords[6:9])
        print "Leg 4: " +  str(RoundedCoords[9:12])
        print "Leg 5: " +  str(RoundedCoords[12:15])
        print "Leg 6: " +  str(RoundedCoords[15:18])
        # print ""
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
        self.PrintInverse(self.DoIKine(x,y,z,alpha,beta,gama,switcher))
    # def calc_Velocity(thetas)
    #     if thetas[2]> thetas[3]





##########################parallel kinematics ############################



    def calc_rotCordinates(self, alpha_rad, beta_rad, gama_rad, my_list_eeCor):
        pre_x = my_list_eeCor[0]
        pre_y = my_list_eeCor[1]
        pre_z = my_list_eeCor[2]
        r_x = (cos(gama_rad)*sin(beta_rad)*pre_z + sin(gama_rad)*sin(beta_rad)*pre_y+pre_x*cos(beta_rad))*cos(alpha_rad)-sin(alpha_rad)*(cos(gama_rad)*pre_y-sin(gama_rad)*pre_z)-pre_x
        r_y = (cos(gama_rad)*sin(beta_rad)*pre_z + sin(gama_rad)*sin(beta_rad)*pre_y+pre_x*cos(beta_rad))*sin(alpha_rad)+cos(alpha_rad)*(cos(gama_rad)*pre_y-sin(gama_rad)*pre_z)-pre_y
        r_z = -sin(beta_rad)*pre_x+cos(beta_rad)*sin(gama_rad)*pre_y+cos(beta_rad)*cos(gama_rad)*pre_z-pre_z
        rot_val = [r_x, r_y, r_z]
        #print("rot_val", rot_val)
        return rot_val




    def calc_RotationMatrix(self, alpha_rad, beta_rad, gama_rad):
        ee_xyz,servoPos = self.DoFKine()
        rot_val_list = []
        rot_val_list.extend(self.calc_rotCordinates( alpha_rad, beta_rad, gama_rad, ee_xyz[0:3]))
        rot_val_list.extend(self.calc_rotCordinates( alpha_rad, beta_rad, gama_rad, ee_xyz[3:6]))
        rot_val_list.extend(self.calc_rotCordinates( alpha_rad, beta_rad, gama_rad, ee_xyz[6:9]))
        rot_val_list.extend(self.calc_rotCordinates( alpha_rad, beta_rad, gama_rad, ee_xyz[9:12]))
        rot_val_list.extend(self.calc_rotCordinates( alpha_rad, beta_rad, gama_rad, ee_xyz[12:15]))
        rot_val_list.extend(self.calc_rotCordinates( alpha_rad, beta_rad, gama_rad, ee_xyz[15:18]))
        return rot_val_list




    def DoIKineRotationEuler(self, alpha_rad, beta_rad, gama_rad):
        ee_xyz,servoPos = self.DoFKine()
        final_eexyz = self.calc_RotationMatrix(alpha_rad, beta_rad, gama_rad)
        thetas = []
        thetas.extend(self.calc_IKine(final_eexyz[0], final_eexyz[1], final_eexyz[2], ee_xyz[0:3],   self.leg1 ))
        thetas.extend(self.calc_IKine(final_eexyz[3], final_eexyz[4], final_eexyz[5], ee_xyz[3:6],   self.leg2 ))
        thetas.extend(self.calc_IKine(final_eexyz[6], final_eexyz[7], final_eexyz[8], ee_xyz[6:9],   self.leg3 ))
        thetas.extend(self.calc_IKine(final_eexyz[9], final_eexyz[10], final_eexyz[11], ee_xyz[9:12],   self.leg4 ))
        thetas.extend(self.calc_IKine(final_eexyz[12], final_eexyz[13], final_eexyz[14], ee_xyz[12:15],   self.leg5 ))
        thetas.extend(self.calc_IKine(final_eexyz[15], final_eexyz[16], final_eexyz[17], ee_xyz[15:18],   self.leg6 ))
        thetas = [x / pi * 2048 + 2048 for x in thetas] # Convert from pi to steps
        return thetas
