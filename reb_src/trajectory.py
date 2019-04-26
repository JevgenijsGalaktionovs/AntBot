#!/usr/bin/env python

from   dynamixel_library import *
import rospy
from   kinematics        import *
from math import pi,cos,sin,atan2,acos,sqrt,pow
from stupid_walk import *



class trajectoryPlanning :
    vel = 2
    trajecrtory_list = []

    def calc_Parabola(self,x,y,z,i):
        delta_x = x
        delta_y = y
        delta_z = z
        a_0 = -(4*delta_z)/(pow(delta_y,2))
        a_1 = -a_0*delta_y
        #print("a1",a_1)
        x = round(delta_x,4)
        y = round(self.vel*i,4)
        z = round(a_0*(pow(y,2)) + a_1*y,4)
        print("z :",z)
        ee_xyz = [x, y, z]
        #print("Local current time :", a_0)
        print ("cordinates :",ee_xyz)
        return ee_xyz

            ########################################
