#!/usr/bin/env python2
import rospy

from path_planning import pathPlanning

if __name__ == '__main__':
    try:
        pathPlanning()
    except rospy.ROSInterruptException:
        SystemExit
