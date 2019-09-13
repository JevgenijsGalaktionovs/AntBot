#!/usr/bin/env python2
import time
from math import pi

from service_router import *
from kinematics     import Kinematics


######################################################
#  UNCOMMENT NEXT LINE IF THE PROGRAM IS ON RASPBERY PI
# from tactiles       import allTactiles


ALL  = [1, 2, 3,   4, 5, 6,   7, 8, 9,   10, 11, 12,   13, 14, 15,   16, 17, 18]
TG_1 = [1, 2, 3,  10, 11, 12,  13, 14, 15]  # Leg 1,4,5 servo IDs "Tripod Group 1"
TG_2 = [4, 5, 6,  7,  8,  9,   16, 17, 18]  # Leg 2,3,6 servo IDs "Tripod Group 2"
l1   = [1, 2, 3]     # Leg 1
l2   = [4, 5, 6]     # Leg 2
l3   = [7, 8, 9]     # Leg 3
l4   = [10, 11, 12]  # Leg 4
l5   = [13, 14, 15]  # Leg 5
l6   = [16, 17, 18]  # Leg 6

legs = {
    1 : [1, 2, 3],     # Leg 1
    2 : [4, 5, 6],     # Leg 2
    3 : [7, 8, 9],     # Leg 3
    4 : [10, 11, 12],  # Leg 4
    5 : [13, 14, 15],  # Leg 5
    6 : [16, 17, 18]   # Leg 6
}

K = Kinematics()


# Gaits
def standUp():
    front_legs  = [1, 2, 3,  4, 5, 6]
    rear_legs   = [13, 14, 15,  16, 17, 18]
    middle_legs = [7, 8, 9,  10, 11, 12]

    standup_pos = [2048, 2218, 1024,   2048, 1878, 3048,
                   2048, 2218, 1024,   2048, 1878, 3048,
                   2048, 2218, 1024,   2048, 1878, 3048]
    front_standup  = list_combine(front_legs, standup_pos)
    rear_standup   = list_combine(rear_legs, standup_pos)
    middle_standup = list_combine(middle_legs, standup_pos)
    positionN(front_standup)
    time.sleep(1)
    positionN(rear_standup)
    time.sleep(1)
    positionN(middle_standup)
    time.sleep(1)


def parallelGait(alpha, beta, gamma, dist_x, dist_y, dist_z):
    alpha_rad = alpha * pi / 180
    beta_rad  = beta  * pi / 180
    gamma_rad = gamma * pi / 180
    current_pos = readPos()
    next_pos = K.doIkineRotationEuler(current_pos, alpha_rad, beta_rad, gamma_rad, dist_x, dist_y, dist_z)
    scaler = [50] * 18
    velocityAll(scaler)
    accelerationAll(scaler)
    positionAll(next_pos)
    time.sleep(0.35)


def translationZ(distance):
    pos = [0, 0, distance]
    do_motion(pos, ALL)


def yawRotation(degrees):
    delay = 0.3
    alpha_rad   = degrees * pi / 180

    do_motion([0, 0, 20], TG_2)
    time.sleep(delay)

    current_pos = readPos()
    next_pos    = K.doIkineRotationEuler(current_pos, alpha_rad, 0, 0, 0, 0, 0)
    pos_list    = list_combine(TG_1, next_pos)
    positionN(pos_list)
    time.sleep(delay)

    do_motion([0, 0, -20], TG_2)
    time.sleep(delay)

    do_motion([0, 0, 20], TG_1)
    time.sleep(delay)

    positionN([1, 2048, 10, 2048, 13, 2048])
    time.sleep(delay)

    final_pos = list_combine(TG_1, current_pos)
    positionN(final_pos)
    time.sleep(delay)


def rippleGait(x, y, z, iterations):
    init_pos = readPos()
    delay = 0.3

    move1 = [x, y, z]
    move2 = [-x / 2, -y / 2, 0]
    move3 = [0, 0, -z]

    for i in range(iterations):

        do_motion(move1, l1 + l4)
        do_motion(move2, l2 + l3 + l5 + l6)
        time.sleep(delay)
        do_motion(move3, l1 + l4)
        time.sleep(delay)

        do_motion(move1, l3 + l6)
        do_motion(move2, l1 + l2 + l4 + l5)
        time.sleep(delay)
        do_motion(move3, l3 + l6)
        time.sleep(delay)

        do_motion(move1, l2 + l5)
        do_motion(move2, l1 + l3 + l4 + l6)
        time.sleep(delay)
        do_motion(move3, l2 + l5)
        time.sleep(delay)

        positionAll(init_pos)
        time.sleep(delay)


def waveGait(x, y, z, iterations):
    init_pos = readPos()
    delay = 0.1

    one_leg_motion_up  = [x, y, z]
    one_leg_motion_down  = [0, 0, -z]
    five_leg_motion = [-x / 6, -y / 6, 0]
    for i in range(iterations):

        do_motion(one_leg_motion_up, l1)
        do_motion(five_leg_motion, l2 + l3 + l4 + l5 + l6)
        time.sleep(delay)

        do_motion(one_leg_motion_down, l1)
        do_motion(one_leg_motion_up, l3)
        do_motion(five_leg_motion, l2 + l4 + l5 + l6)
        time.sleep(delay)

        do_motion(one_leg_motion_down, l3)
        do_motion(one_leg_motion_up, l5)
        do_motion(five_leg_motion, l1 + l2 + l4 + l6)
        time.sleep(delay)

        do_motion(one_leg_motion_down, l5)
        do_motion(one_leg_motion_up, l2)
        do_motion(five_leg_motion, l1 + l3 + l4 + l6)
        time.sleep(delay)

        do_motion(one_leg_motion_down, l2)
        do_motion(one_leg_motion_up, l4)
        do_motion(five_leg_motion, l1 + l3 + l5 + l6)
        time.sleep(delay)

        do_motion(one_leg_motion_down, l4)
        do_motion(one_leg_motion_up, l6)
        do_motion(five_leg_motion, l1 + l2 + l3 + l5)
        time.sleep(delay)

        positionAll(init_pos)
        time.sleep(delay)


def tripodGait(x, y, z, iterations):

    start_pos = tripodGait_start(x, y, z)
    tripodGait_full(x, y, z, iterations, start_pos=start_pos)
    tripodGait_finish(x, y, z)


def tripodGait_start(x, y, z):
    delay = 0.2

    TG1_m1 = [-x, -y,  0]  # Tripod Group 1 : Motion 1

    TG2_m1 = [x,  y,  z]   # Tripod Group 2 : Motion 1
    TG2_m2 = [0,  0, -z]   # Tripod Group 2 : Motion 2

    # Motion 1
    do_motion(TG2_m1, TG_2)
    do_motion(TG1_m1, TG_1)
    time.sleep(delay)
    # Motion 2
    do_motion(TG2_m2, TG_2)
    time.sleep(delay)
    start_pos = readPos()
    return start_pos


def tripodGait_full(x, y, z, iterations, start_pos=None):
    delay = 0.2

    # init_pos = [2048, 2218, 1024,   2048, 1878, 3048,
    #             2048, 2218, 1024,   2048, 1878, 3048,
    #             2048, 2218, 1024,   2048, 1878, 3048]
    if start_pos:
        init_pos = start_pos
    else:
        init_pos = [2002, 2218, 957, 2012, 1918, 2971, 2127, 2200, 1027, 2123, 1887, 3048, 2011, 2188, 1097, 2003, 1872, 3120]
    for i in range(iterations):

        TG1_m1 = [2 * x,  2 * y,  z]   # Tripod Group 1 : Motion 1
        TG1_m2 = [0,  0, -z]           # Tripod Group 1 : Motion 2
        TG1_m3 = [-2 * x, -2 * y,  0]  # Tripod Group 1 : Motion 3

        TG2_m1 = [-2 * x, -2 * y,  0]  # Tripod Group 2 : Motion 1
        TG2_m3 = [2 * x, 2 * y,  z]    # Tripod Group 2 : Motion 3
        TG2_m4 = [0,  0, -z]           # Tripod Group 1 : Motion 4

        # Motion 1
        do_motion(TG1_m1, TG_1)
        time.sleep(0.05)
        do_motion(TG2_m1, TG_2)
        time.sleep(delay)

        # Motion 2
        do_motion(TG1_m2, TG_1)
        time.sleep(delay)

        # Motion 3
        do_motion(TG2_m3, TG_2)
        time.sleep(0.05)
        do_motion(TG1_m3, TG_1)
        time.sleep(delay)

        # Motion 4
        do_motion(TG2_m4, TG_2)
        time.sleep(delay)

        # Motion 5
        positionAll(init_pos)
        time.sleep(delay)


def tripodGait_finish(x, y, z):
    delay = 0.15

    TG1_m1 = [0,  0,  z]   # Tripod Group 1 : Motion 1
    TG1_m2 = [x,  y,  0]   # Tripod Group 1 : Motion 2
    TG1_m3 = [0,  0, -z]   # Tripod Group 1 : Motion 3

    TG2_m4 = [0,  0,  z]   # Tripod Group 2 : Motion 4
    TG2_m5 = [-x, -y,  0]   # Tripod Group 2 : Motion 5
    TG2_m6 = [0,  0, -z]   # Tripod Group 2 : Motion 6
    # Motion 1
    do_motion(TG1_m1, TG_1)
    time.sleep(delay)

    # Motion 2
    do_motion(TG1_m2, TG_1)
    time.sleep(delay)

    # Motion 3
    do_motion(TG1_m3, TG_1)
    time.sleep(delay)

    # Motion 4
    do_motion(TG2_m4, TG_2)
    time.sleep(delay)

    # Motion 5
    do_motion(TG2_m5, TG_2)
    time.sleep(delay)

    # Motion 6
    do_motion(TG2_m6, TG_2)
    time.sleep(delay)


def stepDown(leg_case):
    j = int(leg_case - 1)
    for x in range(40):
        tac = allTactiles()
        tac_oneleg = tac[j]
        if tac_oneleg == 0:
            init_pos = readPos()
            steps = K.doIkine(init_pos, 0, 0, -5, leg=leg_case)
            position1(3 * j + 2, steps[3 * j + 1])
            position1(3 * j + 3, steps[3 * j + 2])
            time.sleep(0.3)
        else:
            return


def list_combine(id_list, value_list):
    ''' Parameters: id_list: list of servo IDs (any order, any number of IDs from 1 to 18)
                    value_list: list of 18 values.
        Return:     list of format: [ID_1, Value_1, ... , ID_n, Value_n]
    '''
    sr_count = 0
    output = [0] * 2 * len(id_list)  # output size must be:  # of servos * 2 (ID + VALUE)
    for x in range(len(id_list)):
        output[x + sr_count] = id_list[x]
        output[x + sr_count + 1] = value_list[id_list[x] - 1]
        sr_count += 1
    return output


def calc_scaler(thetas):
    return [i * 1 for i in thetas]


def do_motion(xyz_list, ID_list, orientation=None):
    """Parameters: xyz_list: list of 3 integers with x,y,z changes to accomplish
                   ID_list:  list of servo IDs
       Example call  : do_motion([0, 30, 20], [7, 8, 9])
       Example result: Position of servo ID7, ID8 and ID9 (Leg 3) will be
                       changed to reach end-tip x= +0, y= +30 and z= +20 position."""
    current_pos = readPos()
    if orientation:
        next_pos    = K.doIkine(current_pos, xyz_list[0], xyz_list[1], xyz_list[2], body_orient=orientation)
    else:
        next_pos    = K.doIkine(current_pos, xyz_list[0], xyz_list[1], xyz_list[2])

    scaler = calc_scaler(next_pos)
    vel_acc_value = list_combine(ID_list, scaler)
    velocityN(vel_acc_value)  # Setting same value for velocity and acceleration is a valid method for Dynamixels
    accelerationN(vel_acc_value)

    motion = list_combine(ID_list, next_pos)
    positionN(motion)
    return next_pos



def singleLeg(x, y, z, alpha, beta, gama, leg_case):
    ID_list = legs[leg_case]
    do_motion([x, y, z], ID_list, orientation=[alpha, beta, gama])



def calculate_motion(xyz_list, ID_list, orientation=None):
    """Parameters: xyz_list: list of 3 integers with x,y,z changes to accomplish
                   ID_list:  list of servo IDs
       Example call  : do_motion([0, 30, 20], [7, 8, 9])
       Example result: Position of servo ID7, ID8 and ID9 (Leg 3) will be
                       changed to reach end-tip x= +0, y= +30 and z= +20 position."""
    current_pos = readPos()
    if orientation:
        next_pos    = K.doIkine(current_pos, xyz_list[0], xyz_list[1], xyz_list[2], body_orient=orientation)
    else:
        next_pos    = K.doIkine(current_pos, xyz_list[0], xyz_list[1], xyz_list[2])

    scaler = calc_scaler(next_pos)
    vel_acc_value = list_combine(ID_list, scaler)
    motion = list_combine(ID_list, next_pos)
    return next_pos


def continiousMotion(x, y, z, iterations):
	one_leg_calculation_up  = [x, y, z]
	one_leg_calculation_down  = [x, y, 0]
	one_push_leg_calculation = [0, 0 , 0]
	a=calculate_motion(one_leg_calculation_up, l1)
	b=calculate_motion(one_leg_calculation_down, l1)
	c=calculate_motion(one_push_leg_calculation, l1)
	
	for i in range(iterations):
		
		positionN([1,a[0],2,a[1],3,a[2]])
		ae=a[:3]
		for x in range (10): 
			current_pos = readPos()
			x = current_pos[:3]
			possition_error=x[0]-ae[0],x[1]-ae[1],x[2]-ae[2]
			absoluteError= sum([abs(x) for x in possition_error])/3
			print(possition_error)
			if absoluteError < 10:
				print(absoluteError, "1")
				break
				
		positionN([1,b[0],2,b[1],3,b[2]])
		ae=b[:3]
		for x in range (10): 
			current_pos = readPos()
			x = current_pos[:3]
			possition_error=x[0]-ae[0],x[1]-ae[1],x[2]-ae[2]
			absoluteError= sum([abs(x) for x in possition_error])/3
			print(possition_error)
			if absoluteError < 10:
				print(absoluteError,"2")
				break
				
		positionN([1,c[0],2,c[1],3,c[2]])
		ae=c[:3]
		for x in range (10): 
			current_pos = readPos()
			x = current_pos[:3]
			possition_error=x[0]-ae[0],x[1]-ae[1],x[2]-ae[2]
			absoluteError= sum([abs(x) for x in possition_error])/3
			print(possition_error)
			if absoluteError < 10:
				print(absoluteError,"3")
				break


def continiousTripod(x, y, z, iterations):
	one_leg_calculation_up  = [x, y, z]
	one_leg_calculation_down  = [x, y, 0]
	one_push_leg_calculation = [0, 0 , 0]

	#######Group 1
	a1=calculate_motion(one_leg_calculation_up, l1)
	b1=calculate_motion(one_leg_calculation_down, l1)
	c1=calculate_motion(one_push_leg_calculation, l1)
	
	a4=calculate_motion(one_leg_calculation_up, l4)
	b4=calculate_motion(one_leg_calculation_down, l4)
	c4=calculate_motion(one_push_leg_calculation, l4)
	
	a5=calculate_motion(one_leg_calculation_up, l5)
	b5=calculate_motion(one_leg_calculation_down, l5)
	c5=calculate_motion(one_push_leg_calculation, l5)
	#####Group 2
	a2=calculate_motion(one_leg_calculation_up, l2)
	b2=calculate_motion(one_leg_calculation_down, l2)
	c2=calculate_motion(one_push_leg_calculation, l2)
	
	a3=calculate_motion(one_leg_calculation_up, l3)
	b3=calculate_motion(one_leg_calculation_down, l3)
	c3=calculate_motion(one_push_leg_calculation, l3)
		
	a6=calculate_motion(one_leg_calculation_up, l6)
	b6=calculate_motion(one_leg_calculation_down, l6)
	c6=calculate_motion(one_push_leg_calculation, l6)
	

	for i in range(iterations):
		
		abssss=positionN([1,a1[0],2,a1[1],3,a1[2],4,c2[3],5,c2[4],6,c2[5],7,c3[6],8,c3[7],9,c3[8],10,a4[9],11,a4[10],12,a4[11],13,a5[12],14,a5[13],15,a5[14],16,c6[15],17,c6[16],18,c6[17]])
		print(abssss)
		ae=a1[:3]
		for x in range (10): 
			current_pos = readPos()
			x = current_pos[:3]
			possition_error=x[0]-ae[0],x[1]-ae[1],x[2]-ae[2]
			absoluteError= sum([abs(x) for x in possition_error])/3
			print(possition_error)
			if absoluteError < 10:
				print(absoluteError, "1")
				break
				
		positionN([1,b1[0],2,b1[1],3,b1[2],4,a2[3],5,a2[4],6,a2[5],7,a3[6],8,a3[7],9,a3[8],10,b4[9],11,b4[10],12,b4[11],13,b5[12],14,b5[13],15,b5[14],16,a6[15],17,a6[16],18,a6[17]])
		ae=b1[:3]
		for x in range (10): 
			current_pos = readPos()
			x = current_pos[:3]
			possition_error=x[0]-ae[0],x[1]-ae[1],x[2]-ae[2]
			absoluteError= sum([abs(x) for x in possition_error])/3
			print(possition_error)
			if absoluteError < 10:
				print(absoluteError,"2")
				break
				
		positionN([1,c1[0],2,c1[1],3,c1[2],4,b2[3],5,b2[4],6,b2[5],7,b3[6],8,b3[7],9,b3[8],10,c4[9],11,c4[10],12,c4[11],13,c5[12],14,c5[13],15,c5[14],16,c6[15],17,c6[16],18,c6[17]])
		ae=c1[:3]
		for x in range (10): 
			current_pos = readPos()
			x = current_pos[:3]
			possition_error=x[0]-ae[0],x[1]-ae[1],x[2]-ae[2]
			absoluteError= sum([abs(x) for x in possition_error])/3
			print(possition_error)
			if absoluteError < 10:
				print(absoluteError,"3")
				break

standUp()
time.sleep(1)
continiousTripod(0,45,20,20)
