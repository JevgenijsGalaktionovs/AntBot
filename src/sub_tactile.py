#!/usr/bin/env python


import rospy
from std_msgs.msg import Int16

    # Function to write the published message from the FSR
    # to log and terminal when new data is received.
def callback(msg):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', msg.data)

def tac_sub():
    # Create a node for the subscriber
    rospy.init_node('sub_tactile', anonymous=True)

    # A subscriber for each of the topics managing each FSR
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
