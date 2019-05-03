#!/usr/bin/env python


import rospy
from std_msgs.msg import Int16

def callback(msg):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', msg.data)

def tac_sub():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('sub_tactile', anonymous=True)

    rospy.Subscriber('tactile_1', Int16, callback)
    rospy.Subscriber('tactile_2', Int16, callback)
    rospy.Subscriber('tactile_3', Int16, callback)
    rospy.Subscriber('tactile_4', Int16, callback)
    rospy.Subscriber('tactile_5', Int16, callback)
    rospy.Subscriber('tactile_6', Int16, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    tac_sub()
