from   dynamixel_library import *
import time



def stand_up():
	initial_pos = [2048,2218,1024,
				   2048,1878,3048,
				   2048,2218,1024,
				   2048,1878,3048,
				   2048,2218,1024,
				   2048,1878,3048]
	WriteAllPositions(initial_pos)
def temp_stand_up():
	initial_pos = ReadAllPositions()
	WriteAllPositions(initial_pos)
