#!/usr/bin/env python


import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

def tac_sub():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('sub_tactile', anonymous=True)

    rospy.Subscriber('tactile_1', String, callback)
    rospy.Subscriber('tactile_2', String, callback)
    rospy.Subscriber('tactile_3', String, callback)
    rospy.Subscriber('tactile_4', String, callback)
    rospy.Subscriber('tactile_5', String, callback)
    rospy.Subscriber('tactile_6', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    tac_sub()
