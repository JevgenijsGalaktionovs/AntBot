#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16
import random
from antbot.msg import UInt16_list
#from dynamixel_library import *

def imitatingKinematics():
	srv_pos = [0]*3
	for x in range(0,3):
		srv_pos[x] = random.randint(2050,3050)
	return srv_pos

def callback_all_pos(data):
    all_positions = data.data
    print all_positions

def master():
    rospy.init_node('Master')
    rospy.Subscriber("Hexapod_servos/Positions_all", UInt16_list, callback_all_pos)
    l1_coxa  = rospy.Publisher('Hexapod_servos/Leg_1/Coxa' , UInt16, queue_size=1)
    l1_femur = rospy.Publisher('Hexapod_servos/Leg_1/Femur', UInt16, queue_size=1)
    l1_tibia = rospy.Publisher('Hexapod_servos/Leg_1/Tibia', UInt16, queue_size=1)

    rate = rospy.Rate(2) # 10hz
    while not rospy.is_shutdown():
        servo_steps = imitatingKinematics()
        l1_coxa. publish(servo_steps[0])
        l1_femur.publish(servo_steps[1])
        l1_tibia.publish(servo_steps[2])
        rate.sleep()

if __name__ == '__main__':
    try:
	master()
    except rospy.ROSInterruptException:
        pass
