#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16

def callback_leg1_coxa(data):
    a = data.data
def callback_leg1_femur(data):
    b = data.data
def callback_leg1_tibia(data):
    c = data.data

def slave():

    rospy.init_node('Slave')

    rospy.Subscriber("Hexapod_servos/Leg_1/Coxa", UInt16, callback_leg1_coxa)
    rospy.Subscriber("Hexapod_servos/Leg_1/Femur", UInt16, callback_leg1_femur)
    rospy.Subscriber("Hexapod_servos/Leg_1/Tibia", UInt16, callback_leg1_tibia)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    slave()
