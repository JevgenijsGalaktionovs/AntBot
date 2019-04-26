#!/usr/bin/env python
import time

from kinematics        import *
from dynamixel_library import *
from stupid_walk       import *

# DisableTorqueAllServos()
# time.sleep(1)
# EnableTorqueAllServos()
# #stand_up()
# time.sleep(1)

writeProfVel(1,200)
writeProfAcc(1,50)
writeProfVel(2,200)
writeProfAcc(2,50)
writeProfVel(3,200)
writeProfAcc(3,50)
writeProfVel(4,200)
writeProfAcc(4,50)
writeProfVel(5,200)
writeProfAcc(5,50)
writeProfVel(6,200)
writeProfAcc(6,50)
#standing Position
Write1Pos(1,2048)
Write1Pos(2,2048)
Write1Pos(3,1251)
Write1Pos(4,2048)
Write1Pos(5,1874)
Write1Pos(6,2844)
time.sleep(3)
self.PrintForward()
#midpoint
# Write1Pos(1,2136)
# Write1Pos(2,2634)
# Write1Pos(3,1074)
# Write1Pos(4,2165)
# Write1Pos(5,2191)
# Write1Pos(6,2663)
# #end point
# time.sleep(0.5)
# Write1Pos(1,2184)
# Write1Pos(2,2307)
# Write1Pos(3,1351)
# Write1Pos(4,2403)
# Write1Pos(5,2064)
# Write1Pos(6,2837)

time.sleep(1)
    # print(vel_MX28[index], vel_MX106[index], vel_MX64[index])
