#!/usr/bin/env python


import rospy
from std_msgs.msg import Int16

    # Function to write the published message from the IR
    # to log and terminal when new data is received.
def callback(msg):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', msg.data)

def kf_sub():
    # Create a node for the subscriber
    rospy.init_node('sub_kf', anonymous=True)

    # A subscriber for each of the topics managing all IRs
    rospy.Subscriber('kf_updated', Int16, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    kf_sub()
