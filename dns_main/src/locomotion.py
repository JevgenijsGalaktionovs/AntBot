#!/usr/bin/env python2
import time
from math import pi

from service_router import *
from kinematics     import Kinematics
from math_calc import *


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

leg = {
    1: [1, 2, 3],     # IDs Leg 1
    2: [4, 5, 6],     # IDs Leg 2
    3: [7, 8, 9],     # IDs Leg 3
    4: [10, 11, 12],  # IDs Leg 4
    5: [13, 14, 15],  # IDs Leg 5
    6: [16, 17, 18]   # IDs Leg 6
}

K = Kinematics()


# Gaits
def standUp():
    front_legs  = [1, 2, 3,  4, 5, 6]
    rear_legs   = [13, 14, 15,  16, 17, 18]
    middle_legs = [7, 8, 9,  10, 11, 12]
    standup_pos = [2048, 2218, 1024,   2048, 2218, 1024,
                   2048, 2218, 1024,   2048, 2218, 1024,
                   2048, 2218, 1024,   2048, 2218, 1024]
    #standup_pos =[1980, 2201, 953,   1972, 2030, 1082,
    #              2096, 2183, 1106,  2111, 2202, 952, 
    #              1941, 2204, 1028,  2003, 2183, 1107]
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
    #print("id_list",id_list)
    #print(value_list)
    sr_count = 0
    output = [0] * 2 * len(id_list)  # output size must be:  # of servos * 2 (ID + VALUE)
    for x in range(len(id_list)):
        #print(x)
        output[x + sr_count] = id_list[x]
        #print("output",output)
        output[x + sr_count + 1] = value_list[x]#id_list[x] - 1]
        sr_count += 1
    return output


def calc_scaler(thetas):
    return [i * 1 for i in thetas]


def do_motion(xyz_list, ID_list, orientation=None,leg = None):
    """Parameters: xyz_list: list of 3 integers with x,y,z changes to accomplish
                   ID_list:  list of servo IDs
                   orientaiton: list of 3 rotation integers in degrees. alpha,beta,gama
       Example call  : do_motion([0, 30, 20], [7, 8, 9])
       Example result: Position of servo ID7, ID8 and ID9 (Leg 3) will be
                       changed to reach end-tip x= +0, y= +30 and z= +20"""
    current_pos = readPos()
    if orientation:
        next_pos = K.doIkine(current_pos, xyz_list[0], xyz_list[1],
                             xyz_list[2], body_orient=orientation, leg= leg)
        #print("next pos", next_pos)
    else:
        next_pos = K.doIkine(current_pos, xyz_list[0], xyz_list[1],
                             xyz_list[2],leg = leg)

    scaler = calc_scaler(next_pos)
    vel_acc_value = list_combine(ID_list, scaler)
    velocityN(vel_acc_value)  # Setting same vel/acc = Trapezoid trajectory
    accelerationN(vel_acc_value)

    motion = list_combine(ID_list, next_pos)
    positionN(motion)
    return next_pos



def singleLeg(x, y, z, alpha, beta, gama, leg_case):
    orient= [alpha,beta,gama]
    ID_list = leg[leg_case]
    #print("ID_list=",ID_list)
    do_motion([x,y,z], ID_list, orientation = orient,leg = leg_case)


def calculate_motion(xyz_list, orientation=None):
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

    return next_pos


def continiousMotion(x, y, z, iterations):
	one_leg_calculation_up  = [x, y, z]
	one_leg_calculation_down  = [x, y, 0]
	one_push_leg_calculation = [0, 0 , 0]
	a=calculate_motion(one_leg_calculation_up, l1)
	b=calculate_motion(one_leg_calculation_down, l1)
	c=calculate_motion(one_push_leg_calculation, l1)
	
# 	for i in range(iterations):
		
		positionN([1,a[0],2,a[1],3,a[2]])
		ae=a[:3]
		for x in range (10): 
			current_pos = readPos()
			x = current_pos[:3]
			possition_error=x[0]-ae[0],x[1]-ae[1],x[2]-ae[2]
			absoluteError= sum([abs(x) for x in possition_error])/3
			#print(possition_error)
			if absoluteError < 10:
				#print(absoluteError, "1")
				break
		else:	
                	print("NotGood")

		positionN([1,b[0],2,b[1],3,b[2]])
		ae=b[:3]
		for x in range (10): 
			current_pos = readPos()
			x = current_pos[:3]
			possition_error=x[0]-ae[0],x[1]-ae[1],x[2]-ae[2]
			absoluteError= sum([abs(x) for x in possition_error])/3
			#print(possition_error)
			if absoluteError < 10:
				#print(absoluteError,"2")
				break
		else:
			print("NotGood")

		positionN([1,c[0],2,c[1],3,c[2]])
		ae=c[:3]
		for x in range (10): 
			current_pos = readPos()
			x = current_pos[:3]
			possition_error=x[0]-ae[0],x[1]-ae[1],x[2]-ae[2]
			absoluteError= sum([abs(x) for x in possition_error])/3
			#print(possition_error)
			if absoluteError < 10:
				#print(absoluteError,"3")
				break
		else:
			print("NotGood")


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
		#print(abssss)
		ae=a1[:3]
		for x in range (10): 
			current_pos = readPos()
			x = current_pos[:3]
			possition_error=x[0]-ae[0],x[1]-ae[1],x[2]-ae[2]
			absoluteError= sum([abs(x) for x in possition_error])/3
			#print(possition_error)
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
			#print(possition_error)
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
			#print(possition_error)
			if absoluteError < 10:
				print(absoluteError,"3")
				break


def rippleMirror(x, y, z, alpha, beta, gama, leg_pair):
    if leg_pair < 4 and leg_pair > 0:
        legs = leg[2*(leg_pair-1)+1] + leg[2*(leg_pair-1)+2]
    #if leg_pair == 1:  # Front legs
    #    legs = leg[1] + leg[2]
    #elif leg_pair == 2:  # Middle legs
    #    legs = leg[3] + leg[4]
    #elif leg_pair == 3:  # Rear legs
    #    legs = leg[5] + leg[6]
    else:
        raise ValuSeError('leg_pair value must be 1,2 or 3. Your value:', leg_pair)

    do_motion([x, y, z], legs, orientation=[alpha, beta, gama])
    do_motion([-x, y, z], legs, orientation=[alpha, beta, gama])

def clear_view_stairs():
    delay = 0.2
    do_motion([0, 60, 30], l3+l4, leg=[3, 4])
    time.sleep(delay)
    do_motion([0, 0, -30], l3+l4, leg=[3, 4])
    time.sleep(delay)
    do_motion([0, 100, 0], l1, leg=[1])
    do_motion([0, -100, 0], l5, leg=[5])
def auto_calcTrajectory(x,y,z,leg_case):
    all_positions = readPos()
    ee_xyz, servoPos = K.doFkine(all_positions)
    #print("whole", ee_xyz)
    ee_xyz = [ee_xyz[3*(leg_case-1)],ee_xyz[3*(leg_case-1)+1],ee_xyz[3*(leg_case-1)+2]]
    leng = length(ee_xyz)
    #print("xyz",ee_xyz)
    while K.calc_ikine( x, y, z, ee_xyz,K.leg_list[leg_case-1], auto = 1) == -1:
        if leg_case % 2 == 1:
            if leng < 483:
                x = x + 1
            elif leng > 483:
                x = x - 1
        
        elif leg_case % 2 == 0:
            if leng < 483:
                x = x - 1
            elif leng > 483:
                x = x + 1
        #print(x,y,z)
    return [x,y,z]
 
def tripodGait_stairs(x, y, z):
    delay = 0.2

def singleLeg_stairs(x, y, z, alpha, beta, gama, leg_case):
    my_list= auto_calcTrajectory(x,y,z, leg_case)
    orient= [alpha,beta,gama]
    ID_list = [3*(leg_case-1)+1,3*(leg_case-1)+2,3*(leg_case-1)+3]
    all_positions = readPos()
    next_pos = K.doIkine(all_positions, my_list[0], my_list[1], my_list[2], body_orient=orient, leg=leg_case, auto=None)
    ae = [ID_list[0],next_pos[0],ID_list[1],next_pos[1],ID_list[2],next_pos[2]]
    print(next_pos)
    #positionN(ae)
    return ae, my_list

def singleLeg_walk(x, y, z, alpha, beta, gama, leg_case):
    my_list= [x,y,z]
    orient= [alpha,beta,gama]
    ID_list = [3*(leg_case-1)+1,3*(leg_case-1)+2,3*(leg_case-1)+3]
    all_positions = readPos()
    next_pos = K.doIkine(all_positions, my_list[0], my_list[1], my_list[2], body_orient=orient, leg=leg_case, auto=None)
    ae = [ID_list[0],next_pos[0],ID_list[1],next_pos[1],ID_list[2],next_pos[2]]
    print(next_pos)
    #positionN(ae)
    return ae
    
def half_step(x,step,z,alpha,beta,gama):
    aa = []
    aa.extend(singleLeg_walk( 0,-step,0,alpha,beta,gama,1))
    aa.extend(singleLeg_walk( 0,0,z,alpha,beta,gama,2))
    aa.extend(singleLeg_walk( 0,0,z,alpha,beta,gama,3))
    aa.extend(singleLeg_walk( 0,-step,0,alpha,beta,gama,4))
    aa.extend(singleLeg_walk( 0,-step,0,alpha,beta,gama,5))
    aa.extend(singleLeg_walk( 0,0,z,alpha,beta,gama,6))
    positionN(aa)
    checking_for_errors(80,50,aa)
    aa = []
    aa.extend(singleLeg_walk( 0,0,0,alpha,beta,gama,1))
    aa.extend(singleLeg_walk( 0,0,-z,alpha,beta,gama,2))
    aa.extend(singleLeg_walk( 0,0,-z,alpha,beta,gama,3))
    aa.extend(singleLeg_walk( 0,0,0,alpha,beta,gama,4))
    aa.extend(singleLeg_walk( 0,0,0,alpha,beta,gama,5))
    aa.extend(singleLeg_walk( 0,0,-z,alpha,beta,gama,6))
    positionN(aa)
    checking_for_errors(80,50,aa)
    checkContact()

def tripodGait_stairs(stairs, distance, depth, riser):
    ee_xyz, servopos = K.doFkine(readPos())
    gama, beta = K.get_orientation([1,5,6])
    print ("gama,beta",gama,beta)
    delay = 2
    alpha = 0
    step = 45
    ae = []
    ae1 = []
    lift = 20
    y_off = 120.96
    #leg1_liftedUp = False
    #leg2_liftedUp = False
    #leg3_liftedUp = False
    #leg4_liftedUp = False
    #leg5_liftedUp = False
    #leg6_liftedUp = False
    #front = False
    #middle = False
    #rear = False
    dist2NextLevel_1 = distance
    dist2NextLevel_2 = distance
    dist2NextLevel_3 = distance + y_off - ee_xyz[7]
    dist2NextLevel_4 = distance + y_off - ee_xyz[10]
    dist2NextLevel_5 = distance + y_off - ee_xyz[13]
    dist2NextLevel_6 = distance + y_off - ee_xyz[16]
    print("dist2NextLevel",dist2NextLevel_1,dist2NextLevel_2,dist2NextLevel_3,dist2NextLevel_4,dist2NextLevel_5,dist2NextLevel_6)
    half_step(0,step,lift,alpha,beta,gama)
    dist2NextLevel_2 = distance - step
    dist2NextLevel_3 = dist2NextLevel_3 - step
    dist2NextLevel_6 = dist2NextLevel_6 - step

    print("dist2NextLevel",dist2NextLevel_2,dist2NextLevel_3,dist2NextLevel_6)
    #time.sleep(30)

    while stairs is True: 
        if dist2NextLevel_1 < 2*step:
            ae_stored1, xyz_stored1 = singleLeg_stairs( 0, 0, riser + lift, alpha, beta, gama,1)
            ae.extend(ae_stored1)
            print("leg1", xyz_stored1)
        elif dist2NextLevel_1 > 2*step:
            xyz_stored1 = [0]*3
            ae.extend(singleLeg_walk( 0, 0, lift, alpha, beta, gama,1))
        ae.extend(singleLeg_walk( 0, -step, 0,alpha,beta,gama,2))
        ae.extend(singleLeg_walk( 0, -step, 0,alpha,beta,gama,3))
        if dist2NextLevel_4 < 2*step:
            ae_stored4, xyz_stored4 = singleLeg_stairs( 0, 0, riser + lift,alpha,beta,gama,4)
            ae.extend(ae_stored4)
            print("leg4", xyz_stored4)
        elif dist2NextLevel_4 > 2*step:
            xyz_stored4 = [0]*3
            ae.extend(singleLeg_walk( 0, 0, lift,alpha,beta,gama,4))
        if dist2NextLevel_5 < 2*step:
            ae_stored5, xyz_stored5 = singleLeg_stairs( 0, 0, riser + lift,alpha,beta,gama,5)
            ae.extend(ae_stored5)
            print("leg5", xyz_stored5)
        elif dist2NextLevel_5 > 2*step:
            xyz_stored5 = [0]*3
            ae.extend(singleLeg_walk( 0, 0, lift, alpha,beta,gama,5))
        ae.extend(singleLeg_walk( 0, -step, 0,alpha,beta,gama,6))
        ee_xyz, servopos = K.doFkine(readPos())
        z1 = ee_xyz[2]
        z4 = ee_xyz[11]
        z5 = ee_xyz[14]
        my_list = K.doFkine(ae)
        positionN(ae)
        checking_for_errors(80,50,ae)

        time.sleep(2)
    ###########put forward ae1
        ae1.extend(singleLeg_walk( -xyz_stored1[0], 2*step, 0, alpha, beta, gama,1))
        ae1.extend(singleLeg_walk( 0, -step, 0, alpha , beta, gama,2))
        ae1.extend(singleLeg_walk( 0, -step, 0, alpha , beta, gama,3))
        ae1.extend(singleLeg_walk( -xyz_stored4[0], 2*step, 0, alpha , beta, gama,4))
        ae1.extend(singleLeg_walk( -xyz_stored5[0], 2*step, 0, alpha , beta, gama,5))
        ae1.extend(singleLeg_walk( 0, -step, 0, alpha, beta, gama,6))
        positionN(ae1)
        checking_for_errors(80,50,ae1)
        checkContact()
    ##########put down
        #checkContact()
        checkContact()
        time.sleep(2)
        ee_xyz, servopos = K.doFkine(readPos())
        z1_new = ee_xyz[2]
        z4_new = ee_xyz[11]
        z5_new = ee_xyz[14]
        dist2NextLevel_1 = dist2NextLevel_1 - 2*step
        if z1_new - z1 > riser/2:    #the leg is lifted up
            if dist2NextLevel_1 > 0:
                dist2NextLevel_1 = depth - 5
                
            else:
                dist2NextLevel_1 = depth + dist2NextLevel_1
        else:
            if dist2NextLevel_1 < 0:
                dist2NextLevel_1 = 10

        dist2NextLevel_4 = dist2NextLevel_4 - 2*step 
        if z4_new - z4 > riser/2:    #the leg is lifted up
            if dist2NextLevel_4 > 0:
                dist2NextLevel_4 = depth - 5
                
            else:
                dist2NextLevel_4 = depth + dist2NextLevel_4
        else:
            if dist2NextLevel_4 < 0:
                dist2NextLevel_4 = 10
        
        dist2NextLevel_5 = dist2NextLevel_5 - 2*step
        if z5_new - z5 > riser/2:    #the leg is lifted up
            if dist2NextLevel_5 > 0:
                dist2NextLevel_5 = depth - 5
                
            else:
                dist2NextLevel_5 = depth + dist2NextLevel_5
        else:
            if dist2NextLevel_5 < 0:
                dist2NextLevel_5 = 10


        
        print("dist",dist2NextLevel_1,dist2NextLevel_2,dist2NextLevel_3,dist2NextLevel_4,dist2NextLevel_5,dist2NextLevel_6)
        time.sleep(2)
    ##########seconed group lift up and push
        ae = []
        ae1 = []
        ae.extend(singleLeg_walk( 0, -step, 0,alpha,beta,gama,1))
        if dist2NextLevel_2 < 2*step:
            ae_stored2, xyz_stored2 = singleLeg_stairs( 0, 0, riser + lift, alpha, beta, gama,2)
            ae.extend(ae_stored2)
            print("leg2", xyz_stored2)
        elif dist2NextLevel_2 > 2*step:
            xyz_stored2 = [0]*3
            ae.extend(singleLeg_walk( 0, 0, lift,alpha,beta,gama,2))

        if dist2NextLevel_3 < 2*step:
            ae_stored3, xyz_stored3 = singleLeg_stairs( 0, 0, riser + lift,alpha,beta,gama,3)
            ae.extend(ae_stored3)
            print("leg3", xyz_stored3)
        elif dist2NextLevel_3 > 2*step:
            xyz_stored3 = [0]*3
            ae.extend(singleLeg_walk( 0, 0, lift, alpha,beta,gama,3))
        ae.extend(singleLeg_walk( 0, -step, 0,alpha,beta,gama,4))
        ae.extend(singleLeg_walk( 0, -step, 0,alpha,beta,gama,5))
        if dist2NextLevel_6 < 2*step:
            ae_stored6, xyz_stored6 = singleLeg_stairs( 0, 0, riser + lift,alpha,beta,gama,6)
            ae.extend(ae_stored6)
            print("leg6", xyz_stored6)
        elif dist2NextLevel_6 > 2*step:
            xyz_stored6 = [0]*3
            ae.extend(singleLeg_walk( 0, 0, lift,alpha,beta,gama,6))
        ee_xyz, servopos = K.doFkine(readPos())
        z2 = ee_xyz[5]
        z3 = ee_xyz[8]
        z6 = ee_xyz[17]
        positionN(ae)
        checking_for_errors(80,50,ae)
    ###########put forward ae1
        ae1.extend(singleLeg_walk( 0, -step, 0, alpha , beta, gama,1))
        ae1.extend(singleLeg_walk( -xyz_stored2[0], 2*step, 0, alpha, beta, gama,2))
        ae1.extend(singleLeg_walk( -xyz_stored3[0], 2*step, 0, alpha , beta, gama,3))
        ae1.extend(singleLeg_walk( 0, -step, 0, alpha , beta, gama,4))
        ae1.extend(singleLeg_walk( 0, -step, 0, alpha , beta, gama,5))
        ae1.extend(singleLeg_walk( -xyz_stored6[0], 2*step, 0, alpha , beta, gama,6))
        positionN(ae1)
        checking_for_errors(80,50,ae1)
        checkContact()
    ##########put down
        checkContact()
        #checkContact()
        ee_xyz = []
        ee_xyz, servopos = K.doFkine(readPos())
        z2_new = ee_xyz[5]
        z3_new = ee_xyz[8]
        z6_new = ee_xyz[17]
        dist2NextLevel_2 = dist2NextLevel_2 - 2*step
        if z2_new - z2 > riser/2:    #the leg is lifted up
            if dist2NextLevel_2 > 0:
                dist2NextLevel_2 = depth - 5
                
            else:
                dist2NextLevel_2 = depth + dist2NextLevel_2
        else:
            if dist2NextLevel_2 < 0:
                dist2NextLevel_2 = 10

        dist2NextLevel_3 = dist2NextLevel_3 - 2*step
        if z3_new - z3 > riser/2:    #the leg is lifted up
            if dist2NextLevel_3 > 0:
                dist2NextLevel_3 = depth - 3
                
            else:
                dist2NextLevel_3 = depth + dist2NextLevel_3
        else:
            if dist2NextLevel_3 < 0:
                dist2NextLevel_3 = 10
        
        dist2NextLevel_6 = dist2NextLevel_6 - 2*step
        if z6_new - z6 > riser/2:    #the leg is lifted up
            if dist2NextLevel_6 > 0:
                dist2NextLevel_6 = depth - 5
                
            else:
                dist2NextLevel_6 = depth + dist2NextLevel_6
        else:
            if dist2NextLevel_6 < 0:
                dist2NextLevel_6 = 10

        print("dist",dist2NextLevel_1,dist2NextLevel_2,dist2NextLevel_3,dist2NextLevel_4,dist2NextLevel_5,dist2NextLevel_6)
        ee_xyz = []
        ee_xyz, servopos = K.doFkine(readPos())
        z1 = ee_xyz[2]
        z2 = ee_xyz[5]
        z5 = ee_xyz[14]
        z6 = ee_xyz[17]
        z_front = abs(z1 - z2)
        z_rear = abs(z5 - z6)
        if (z_front<15) and (z_rear<15):
            gama,beta = K.get_orientation([1,5,6])
            time.sleep(1)
            parallelGait(0,-beta,-gama,0,0,0)
            time.sleep(1)
            a = K.calc_translationStairs(riser)
            time.sleep(1)
            parallelGait(0,0,0,0, a[1], a[0])

def checkContact():
    stepping_down_calculation = [0,0,-5]
    desired_Position = calculate_motion(stepping_down_calculation)
    for x in range (20):
        fsr = readFSR()
        leg_trigger=[True]*6
        print ("fsr",fsr)
        for x in range (6): 
            if fsr[x] < 100:
                print ("leg_",x+1 ,"is not activated")
                leg_trigger[x]=False
        print (leg_trigger) 
        for x in range (6):
                if leg_trigger[x] == False:
                    j = x
                    positionN([3*j+1,desired_Position[3*j],3*j+2,desired_Position[3*j+1],3*j+3,desired_Position[3*j+2]])
                if False in leg_trigger:
                    print ("All legs are not in contact")
                else:	
                    break
        time.sleep(0.5)
        current_Position = readPos()
        desired_Position=wannabeControlSystem(desired_Position,current_Position,0,0,-5)

def wannabeControlSystem(current_Position, desired_Position, x,y,z):
    newPoss      = []
    NewWhereIAm  = [0]*18
    NewWhereToGo = [0]*18
    WhereToGo = K.doFkine(desired_Position)[:1]
    WhereIAm  = K.doFkine(current_Position)[:1]
    for i in range (18):
        NewWhereToGo[i] = WhereToGo[0][i] 
        NewWhereIAm[i]  = WhereIAm[0][i]
    Error = [i - j for i, j in zip(NewWhereToGo, NewWhereIAm)]
    ee_xyz_error = [i * 0.9 for i in Error]
    ee_xyz = [i - j for i, j in zip(NewWhereIAm,ee_xyz_error)]
    print(NewWhereIAm)
    print(ee_xyz_error)
    j = 0
    for i in xrange(0, 16, 3):
        newPoss.extend(K.calc_ikine(x, y, z, ee_xyz[i:i + 3], K.leg_list[j]))
        j += 1
    result = [int(next_poss) for next_poss in K.rad_to_step(newPoss)]
    print("Newposs",result)
    return result

def checking_for_errors(itter, allowed_error, desired_pos):
    ae = desired_pos[1],desired_pos[3],desired_pos[5],desired_pos[7],desired_pos[9],desired_pos[11],desired_pos[13],desired_pos[15],desired_pos[17],desired_pos[19],desired_pos[21],desired_pos[23],desired_pos[25],desired_pos[27],desired_pos[29],desired_pos[31],desired_pos[33],desired_pos[35]
    for x in range (itter): 
        current_pos = readPos()
        pos = current_pos[:18]
        possition_error_leg1=pos[0]-ae[0],pos[1]-ae[1],pos[2]-ae[2]
        possition_error_leg4=pos[9]-ae[9],pos[10]-ae[10],pos[11]-ae[11]
        possition_error_leg5=pos[12]-ae[12],pos[13]-ae[13],pos[14]-ae[14]
        absoluteError_leg1= sum([abs(x) for x in possition_error_leg1])/3
        absoluteError_leg4= sum([abs(x) for x in possition_error_leg4])/3
        absoluteError_leg5= sum([abs(x) for x in possition_error_leg5])/3
        absoluteError_swing = absoluteError_leg1+absoluteError_leg4+absoluteError_leg5
        possition_error_leg2=pos[3]-ae[3],pos[4]-ae[4],pos[5]-ae[5]
        possition_error_leg3=pos[6]-ae[6],pos[7]-ae[7],pos[8]-ae[8]
        possition_error_leg6=pos[15]-ae[15],pos[16]-ae[16],pos[17]-ae[17]
        absoluteError_leg2= sum([abs(x) for x in possition_error_leg2])/3
        absoluteError_leg3= sum([abs(x) for x in possition_error_leg3])/3
        absoluteError_leg6= sum([abs(x) for x in possition_error_leg4])/3
        absoluteError_stance = absoluteError_leg2+absoluteError_leg3+absoluteError_leg6
        absoluteError= absoluteError_stance+absoluteError_swing
        print(absoluteError)
        if absoluteError < allowed_error:
            print(absoluteError, "1")
            break