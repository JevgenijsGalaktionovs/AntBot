#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16
from antbot.msg import UInt16_list
from dynamixel_library import *

def callback_leg1_coxa(data):
    a = data.data
def callback_leg1_femur(data):
    b = data.data
    print b
    Write1Pos(17,b)
def callback_leg1_tibia(data):
    c = data.data
    Write1Pos(18,c)

def slave():

    rospy.init_node('Slave')
    all_pos = rospy.Publisher("Hexapod_servos/Positions_all", UInt16_list, queue_size=1)
    rospy.Subscriber("Hexapod_servos/Leg_1/Coxa", UInt16, callback_leg1_coxa)
    rospy.Subscriber("Hexapod_servos/Leg_1/Femur", UInt16, callback_leg1_femur)
    rospy.Subscriber("Hexapod_servos/Leg_1/Tibia", UInt16, callback_leg1_tibia)
    # spin() simply keeps python from exiting until this node is stopped

    rate = rospy.Rate(2) # 10hz
    while not rospy.is_shutdown():
        all_servo_positions = ReadAllPositions()
        all_pos.publish(all_servo_positions)
        rate.sleep()

if __name__ == '__main__':
    slave()
