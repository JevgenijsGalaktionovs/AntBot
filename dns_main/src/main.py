#!/usr/bin/env python2
import rospy

from service_router import getAllStairsInfo, getStairsDepth, getStairsHeight, \
    getStairsDistZ, getStairsDistX


if __name__ == '__main__':
    try:
        # Testing new functions. Don't use all together.
        # If you just need all numbers use getAllStairsInfo() (RECOMMENDED)
        # Order: [depth, height, dist_z_to_1step, dist_x_to_1step]
        print getAllStairsInfo()
        print getStairsDepth()
        print getStairsHeight()
        print getStairsDistZ()
        print getStairsDistX()
    except rospy.ROSInterruptException:
        SystemExit
