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

# def stand_up():
# 	initial_pos = [2048,2218,1024,
# 			2048,1878,3048,
# 			2048,2218,1024,
# 			2048,1878,3048,
# 			2048,2218,1024,
# 			2048,1878,3048]
# 	WriteAllPositions(initial_pos)

for x in range (0, 8):
    writeProfVel(1,50)
    writeProfAcc(1,20)
    writeProfVel(2,100)
    writeProfAcc(2,20)
    writeProfVel(3,100)
    writeProfAcc(3,20)
    writeProfVel(4,50)
    writeProfAcc(4,20)
    writeProfVel(5,100)
    writeProfAcc(5,20)
    writeProfVel(6,100)
    writeProfAcc(6,20)
    writeProfVel(7,50)
    writeProfAcc(7,20)
    writeProfVel(8,100)
    writeProfAcc(8,20)
    writeProfVel(9,100)
    writeProfAcc(9,20)
    writeProfVel(10,50)
    writeProfAcc(10,20)
    writeProfVel(11,100)
    writeProfAcc(11,20)
    writeProfVel(12,100)
    writeProfAcc(12,20)
    writeProfVel(13,50)
    writeProfAcc(13,20)
    writeProfVel(14,100)
    writeProfAcc(14,20)
    writeProfVel(15,100)
    writeProfAcc(15,20)
    writeProfVel(16,50)
    writeProfAcc(16,20)
    writeProfVel(17,100)
    writeProfAcc(17,20)
    writeProfVel(18,100)
    writeProfAcc(18,20)
    #stand up
    # leg 1
    Write1Pos(1,2048)
    Write1Pos(2,2218)
    Write1Pos(3,1024)
    # leg 2
    Write1Pos(4,2048)
    Write1Pos(5,1878)
    Write1Pos(6,3048)
    # leg 3
    Write1Pos(7,2048)
    Write1Pos(8,2218)
    Write1Pos(9,1024)
    time.sleep(0.5)
    # leg 4
    Write1Pos(10,2048)
    Write1Pos(11,1878)
    Write1Pos(12,3048)
    # leg 5
    Write1Pos(13,2048)
    Write1Pos(14,2218)
    Write1Pos(15,1024)
    # leg 6
    Write1Pos(16,2048)
    Write1Pos(17,1878)
    Write1Pos(18,3048)
    time.sleep(0.5)


    #rotate body 45 degress
    # leg 1
    Write1Pos(1,2560)
    Write1Pos(2,2218)
    Write1Pos(3,1024)
    # leg 4
    Write1Pos(10,2560)
    Write1Pos(11,1878)
    Write1Pos(12,3048)
    # leg 5
    Write1Pos(13,2560)
    Write1Pos(14,2218)
    Write1Pos(15,1024)
    #leg 2
    Write1Pos(4,2560)
    Write1Pos(5,1878)
    Write1Pos(6,3048)
    #leg 3
    Write1Pos(7,2560)
    Write1Pos(8,2218)
    Write1Pos(9,1024)
    #leg 6
    Write1Pos(16,2560)
    Write1Pos(17,1878)
    Write1Pos(18,3048)
    time.sleep(1)
    #rotate body -45 degress
    # leg 1
    Write1Pos(1,2048)
    Write1Pos(2,2218)
    Write1Pos(3,1024)
    # leg 4
    Write1Pos(10,2048)
    Write1Pos(11,1878)
    Write1Pos(12,3048)
    # leg 5
    Write1Pos(13,2048)
    Write1Pos(14,2218)
    Write1Pos(15,1024)
    #leg 2
    Write1Pos(4,2048)
    Write1Pos(5,1878)
    Write1Pos(6,3048)
    #leg 3
    Write1Pos(7,2048)
    Write1Pos(8,2218)
    Write1Pos(9,1024)
    #leg 6
    Write1Pos(16,2048)
    Write1Pos(17,1878)
    Write1Pos(18,3048)
    time.sleep(1)
    #rotate body 45 degress
    # leg 1
    Write1Pos(1,1536)
    Write1Pos(2,2218)
    Write1Pos(3,1024)
    # leg 4
    Write1Pos(10,1536)
    Write1Pos(11,1878)
    Write1Pos(12,3048)
    # leg 5
    Write1Pos(13,1536)
    Write1Pos(14,2218)
    Write1Pos(15,1024)
    #leg 2
    Write1Pos(4,1536)
    Write1Pos(5,1878)
    Write1Pos(6,3048)
    #leg 3
    Write1Pos(7,1536)
    Write1Pos(8,2218)
    Write1Pos(9,1024)
    #leg 6
    Write1Pos(16,1536)
    Write1Pos(17,1878)
    Write1Pos(18,3048)
    time.sleep(1)
    #rotate body -45 degress
    # leg 1
    Write1Pos(1,2048)
    Write1Pos(2,2218)
    Write1Pos(3,1024)
    # leg 4
    Write1Pos(10,2048)
    Write1Pos(11,1878)
    Write1Pos(12,3048)
    # leg 5
    Write1Pos(13,2048)
    Write1Pos(14,2218)
    Write1Pos(15,1024)
    #leg 2
    Write1Pos(4,2048)
    Write1Pos(5,1878)
    Write1Pos(6,3048)
    #leg 3
    Write1Pos(7,2048)
    Write1Pos(8,2218)
    Write1Pos(9,1024)
    #leg 6
    Write1Pos(16,2048)
    Write1Pos(17,1878)
    Write1Pos(18,3048)
    time.sleep(1)


    # #legs up and midle
    # # leg 1
    # Write1Pos(1,2304)
    # Write1Pos(2,2418)
    # Write1Pos(3,1124)
    # # leg 4
    # Write1Pos(10,2304)
    # Write1Pos(11,1678)
    # Write1Pos(12,3148)
    # # leg 5
    # Write1Pos(13,2304)
    # Write1Pos(14,2418)
    # Write1Pos(15,1124)
    # time.sleep(0.5)
    #
    # #legs down rotated 45 degrees
    # # leg 1
    # Write1Pos(1,2560)
    # Write1Pos(2,2218)
    # Write1Pos(3,1024)
    # # leg 4
    # Write1Pos(10,2560)
    # Write1Pos(11,1878)
    # Write1Pos(12,3048)
    # # leg 5
    # Write1Pos(13,2560)
    # Write1Pos(14,2218)
    # Write1Pos(15,1024)
    # time.sleep(0.5)
    # #other legs up in the air
    # #leg 2
    # Write1Pos(4,2048)
    # Write1Pos(5,1678)
    # Write1Pos(6,3148)
    # #leg 3
    # Write1Pos(7,2048)
    # Write1Pos(8,2418)
    # Write1Pos(9,1124)
    # #leg 6
    # Write1Pos(16,2048)
    # Write1Pos(17,1678)
    # Write1Pos(18,3148)
    # time.sleep(0.5)
    # #rotate body 45 degress
    # # leg 1
    # Write1Pos(1,2048)
    # Write1Pos(2,2218)
    # Write1Pos(3,1024)
    # # leg 4
    # Write1Pos(10,2048)
    # Write1Pos(11,1878)
    # Write1Pos(12,3048)
    # # leg 5
    # Write1Pos(13,2048)
    # Write1Pos(14,2218)
    # Write1Pos(15,1024)
    # time.sleep(0.5)
    # #other legs down on the ground
    # #leg 2
    # Write1Pos(4,2048)
    # Write1Pos(5,1878)
    # Write1Pos(6,3048)
    # #leg 3
    # Write1Pos(7,2048)
    # Write1Pos(8,2218)
    # Write1Pos(9,1024)
    # #leg 6
    # Write1Pos(16,2048)
    # Write1Pos(17,1878)
    # Write1Pos(18,3048)
    # time.sleep(0.5)
    #
    #
