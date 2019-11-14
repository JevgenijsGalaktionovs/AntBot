#!/usr/bin/env python2
import rospy

from service_router import getStairs

if __name__ == '__main__':
    try:
        print getStairs()
    except rospy.ROSInterruptException:
        SystemExit
