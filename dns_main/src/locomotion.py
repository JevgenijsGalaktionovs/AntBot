#!/usr/bin/env python2
import time
from math import pi

from service_router import *
from kinematics     import Kinematics
from parallel_forward import get_orietation


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
    print("id_list",id_list)
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
    print("ID_list=",ID_list)
    do_motion([x,y,z], ID_list, orientation = orient,leg = leg_case)


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

    #scaler = calc_scaler(next_pos)
    #vel_acc_value = list_combine(ID_list, scaler)
    #motion = list_combine(ID_list, next_pos)
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
		else:	
                	print("NotGood")

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
		else:
			print("NotGood")

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

def auto_calcTrajectory(x,y,z,leg_case):
    all_positions = readPos()
    ee_xyz, servoPos = K.doFkine(all_positions)
    ee_xyz = [ee_xyz[3*(leg_case-1)],ee_xyz[3*(leg_case-1)+1],ee_xyz[3*(leg_case-1)+2]]
    print("xyz",ee_xyz)
    while K.calc_ikine( x, y, z, ee_xyz,K.leg_list[leg_case-1], auto = 1) == -1:
        if leg_case % 2 == 1:
            x = x + 1
            print(x,y,z)
            time.sleep(0.2)
        elif leg_case % 2 == 0:
            x = x - 1
            print(x,y,z)
            time.sleep(0.2)

    return [x,y,z]

def singleLeg_stairs(x, y, z, alpha, beta, gama, leg_case):
    my_list= auto_calcTrajectory(x,y,z, leg_case)
    orient= [alpha,beta,gama]
    ID_list = [3*(leg_case-1)+1,3*(leg_case-1)+2,3*(leg_case-1)+3]
    all_positions = readPos()
    next_pos = K.doIkine(all_positions, my_list[0], my_list[1], my_list[2], body_orient=orient, leg=leg_case, auto=None)
    ae = [ID_list[0],next_pos[0],ID_list[1],next_pos[1],ID_list[2],next_pos[2]]
    #positionN(ae)
    return ae, my_list

def singleLeg_walk(x, y, z, alpha, beta, gama, leg_case):
    my_list= [x,y,z]
    orient= [alpha,beta,gama]
    ID_list = [3*(leg_case-1)+1,3*(leg_case-1)+2,3*(leg_case-1)+3]
    all_positions = readPos()
    next_pos = K.doIkine(all_positions, my_list[0], my_list[1], my_list[2], body_orient=orient, leg=leg_case, auto=None)
    ae = [ID_list[0],next_pos[0],ID_list[1],next_pos[1],ID_list[2],next_pos[2]]
    #positionN(ae)
    return ae
    

def tripodGait_stairs(lift, alpha, beta, gama, depth, riser):
    delay = 2
    gone_forward = 0
    step = depth/4
    print("step",step)
    ae = []
    front_legs = True
    middle_legs = False
    rare_legs = False
    while gone_forward < step:     #depth-step:
        if front_legs is True:
            ae_stored1, xyz_stored = singleLeg_stairs( 0, 0, riser + lift,alpha,beta,gama,1)
            ae.extend(ae_stored1)
            print("ae",ae)
        elif front_legs is not True:
            print("im not here")
            ae.extend(singleLeg_walk( 0, 0, lift,alpha,beta,gama,1))
        if middle_legs is True:
            ae_stored4, xyz_stored = singleLeg_stairs( 0, 0, riser + lift,alpha,beta,gama,4)
            ae.extend(ae_stored4)
            pint("leg4 lift up")
        elif middle_legs is not True:
            print("ae",ae)
            ae.extend(singleLeg_walk( 0, 0, lift,alpha,beta,gama,4))
        if rare_legs is True: 
            ae_stored5, xyz_stored = singleLeg_stairs( 0, 0, riser + lift,alpha,beta,gama,5)
            ae.extend(ae_stored5)
            pint("leg5 lift up")
        elif rare_legs is not True:
            ae.extend(singleLeg_walk( 0, 0, lift,alpha,beta,gama,5))
            print("ae",ae)
        ae.extend(singleLeg_walk( 0, -step, 0,alpha,beta,gama,2))
        ae.extend(singleLeg_walk( 0, -step, 0,alpha,beta,gama,3))
        ae.extend(singleLeg_walk( 0, -step, 0,alpha,beta,gama,6))
        positionN(ae)
        time.sleep(delay/2)

    ##########put down
        gone_forward = gone_forward + step
        print(gone_forward)
        front_legs = False
        


  

def continiousTripodTactile(x, y, z, iterations):
    one_leg_calculation_up  = [x, y, z]
    one_leg_calculation_down  = [x, y, 0]
    one_push_leg_calculation = [0, 0 , 0]
    push_leg_calculation     = [-x,-y,0]
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

    leg1_1=a1[:3]
    leg2_1=c2[3:6]
    leg3_1=c3[6:9]
    leg4_1=a4[9:12]
    leg5_1=a5[12:15]
    leg6_1=c6[15:18]
    motion1 = leg1_1+leg2_1+leg3_1+leg4_1+leg5_1+leg6_1
    print(motion1)

    leg1_2_1=b1[:3]
    leg2_2_1=c2[3:6]
    leg3_2_1=c3[6:9]
    leg4_2_1=b4[9:12]
    leg5_2_1=b5[12:15]
    leg6_2_1=c6[15:18]
    motion2_1 = leg1_2_1+leg2_2_1+leg3_2_1+leg4_2_1+leg5_2_1+leg6_2_1
    print(motion2_1)

    leg1_2_2=b1[:3]
    leg2_2_2=a2[3:6]
    leg3_2_2=a3[6:9]
    leg4_2_2=b4[9:12]
    leg5_2_2=b5[12:15]
    leg6_2_2=a6[15:18]
    motion2_2 = leg1_2_2+leg2_2_2+leg3_2_2+leg4_2_2+leg5_2_2+leg6_2_2
    print(motion2_2)

    leg1_3=c1[:3]
    leg2_3=b2[3:6]
    leg3_3=b3[6:9]
    leg4_3=c4[9:12]
    leg5_3=c5[12:15]
    leg6_3=b6[15:18]
    motion3 = leg1_3+leg2_3+leg3_3+leg4_3+leg5_3+leg6_3
    print(motion3)
    itter=15

    for i in range(iterations):
        ##########################1-st Group upp, 2nd push
        a1=calculate_motion(one_leg_calculation_up, l1)
        a4=calculate_motion(one_leg_calculation_up, l4)
        a5=calculate_motion(one_leg_calculation_up, l5)
        c2=calculate_motion(push_leg_calculation, l2)
        c3=calculate_motion(push_leg_calculation, l3)
        c6=calculate_motion(push_leg_calculation, l6)
        leg1_1=a1[:3]
        leg2_1=c2[3:6]
        leg3_1=c3[6:9]
        leg4_1=a4[9:12]
        leg5_1=a5[12:15]
        leg6_1=c6[15:18]
        motion1 = leg1_1+leg2_1+leg3_1+leg4_1+leg5_1+leg6_1
        positionAll(motion1)
        ae=motion1[:18]
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
            absoluteError_leg2= sum([abs(x) for x in possition_error_leg1])/3
            absoluteError_leg3= sum([abs(x) for x in possition_error_leg3])/3
            absoluteError_leg6= sum([abs(x) for x in possition_error_leg4])/3
            absoluteError_stance = absoluteError_leg2+absoluteError_leg3+absoluteError_leg6
            absoluteError= absoluteError_stance+absoluteError_swing
            print(absoluteError)
            if absoluteError < 20:
                print(absoluteError, "1")
                break
##########################1-st Group down
        
        c2=calculate_motion(one_push_leg_calculation, l2)
        c3=calculate_motion(one_push_leg_calculation, l3)
        c6=calculate_motion(one_push_leg_calculation, l6)
        leg2_2_1=c2[3:6]
        leg3_2_1=c3[6:9]
        leg6_2_1=c6[15:18]
        motion2_1 = leg1_2_1+leg2_2_1+leg3_2_1+leg4_2_1+leg5_2_1+leg6_2_1
        positionAll(motion2_1)
        ae=motion2_1[:18]
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
            absoluteError_leg2= sum([abs(x) for x in possition_error_leg1])/3
            absoluteError_leg3= sum([abs(x) for x in possition_error_leg3])/3
            absoluteError_leg6= sum([abs(x) for x in possition_error_leg4])/3
            absoluteError_stance = absoluteError_leg2+absoluteError_leg3+absoluteError_leg6
            absoluteError= absoluteError_stance+absoluteError_swing
            print(absoluteError)
            fsr = readFSR()
            fsr_leg1=fsr[0]
            fsr_leg4=fsr[3]
            fsr_leg5=fsr[4]
            if absoluteError < 20:
                print(absoluteError, "1")
                break
            if fsr_leg1 > 100:
                leg=1
                j=int(leg-1)
                current_pos_leg1 = readPos()
                pos_1 = current_pos_leg1[:18]
                positionN([3*j+1,pos_1[3*j],3*j+2,pos_1[3*j+1],3*j+3,pos_1[3*j+2]])
            if fsr_leg4 > 100:
                leg=4
                j=int(leg-1)
                current_pos_leg4 = readPos()
                pos_4 = current_pos_leg4[:18]
                positionN([3*j+1,pos_4[3*j],3*j+2,pos_4[3*j+1],3*j+3,pos_4[3*j+2]])
            if fsr_leg5 > 100:
                leg=5
                j=int(leg-1)
                current_pos_leg5 = readPos()
                pos_5 = current_pos_leg5[:18]
                positionN([3*j+1,pos_5[3*j],3*j+2,pos_5[3*j+1],3*j+3,pos_5[3*j+2]])
            elif fsr_leg1 > 100 and fsr_leg4 > 100 and fsr_leg5 > 100:
                break  
	checkContact()	
        a2=calculate_motion(one_leg_calculation_up, l2)
        a3=calculate_motion(one_leg_calculation_up, l3)
        a6=calculate_motion(one_leg_calculation_up, l6)
        c1=calculate_motion(one_push_leg_calculation, l1)
        c4=calculate_motion(one_push_leg_calculation, l4)
        c5=calculate_motion(one_push_leg_calculation, l5)
        leg1_2_2=c1[:3] 
        leg2_2_2=a2[3:6]
        leg3_2_2=a3[6:9]
        leg4_2_2=c4[9:12]
        leg5_2_2=c5[12:15]
        leg6_2_2=a6[15:18]
        motion2_2 = leg1_2_2+leg2_2_2+leg3_2_2+leg4_2_2+leg5_2_2+leg6_2_2
        print(motion2_2)
        positionAll(motion2_2)
        ae=motion2_2[:18]
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
            absoluteError_leg2= sum([abs(x) for x in possition_error_leg1])/3
            absoluteError_leg3= sum([abs(x) for x in possition_error_leg3])/3
            absoluteError_leg6= sum([abs(x) for x in possition_error_leg4])/3
            absoluteError_stance = absoluteError_leg2+absoluteError_leg3+absoluteError_leg6
            absoluteError= absoluteError_stance+absoluteError_swing
            print(absoluteError)
            if absoluteError < 20:
                print(absoluteError, "1")
                break
        c1=calculate_motion(push_leg_calculation, l1)
        c4=calculate_motion(push_leg_calculation, l4)
        c5=calculate_motion(push_leg_calculation, l5)
        leg1_3=c1[:3]
        leg4_3=c4[9:12]
        leg5_3=c5[12:15]
        motion3 = leg1_3+leg2_3+leg3_3+leg4_3+leg5_3+leg6_3
        positionAll(motion3)
        ae=motion3[:18]
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
            absoluteError_leg2= sum([abs(x) for x in possition_error_leg1])/3
            absoluteError_leg3= sum([abs(x) for x in possition_error_leg3])/3
            absoluteError_leg6= sum([abs(x) for x in possition_error_leg4])/3
            absoluteError_stance = absoluteError_leg2+absoluteError_leg3+absoluteError_leg6
            absoluteError= absoluteError_stance+absoluteError_swing
            print(absoluteError)
            fsr = readFSR()
            fsr_leg2=fsr[1]
            fsr_leg3=fsr[2]
            fsr_leg6=fsr[5]
            if absoluteError < 20:
                print(absoluteError, "1")
                break
            if fsr_leg2 > 100:
                leg=2
                j=int(leg-1)
                current_pos_leg2 = readPos()
                pos_2 = current_pos_leg2[:18]
                positionN([3*j+1,pos_2[3*j],3*j+2,pos_2[3*j+1],3*j+3,pos_2[3*j+2]])
            if fsr_leg3 > 100:
                leg=3
                j=int(leg-1)
                current_pos_leg3 = readPos()
                pos_3 = current_pos_leg3[:18]
                positionN([3*j+1,pos_3[3*j],3*j+2,pos_3[3*j+1],3*j+3,pos_3[3*j+2]])
            if fsr_leg6 > 100:
                leg=6
                j=int(leg-1)
                current_pos_leg6 = readPos()
                pos_6 = current_pos_leg6[:18]
                positionN([3*j+1,pos_6[3*j],3*j+2,pos_6[3*j+1],3*j+3,pos_6[3*j+2]])
            elif fsr_leg2 > 100 and fsr_leg3 > 100 and fsr_leg6 > 100:
                break 
	checkContact()	
	orientation=get_orietation()
	parallelGait(0, -orientation[1], -orientation[0], 0, 0, 0)
	time.sleep(2)
def checkContact():
	for x in range (20):
		fsr = readFSR()
		leg_trigger=[True]*6
		print fsr
		for x in range (6): 
			if fsr[x] < 100:
				print ("leg_",x+1 ,"is not activated")
				leg_trigger[x]=False
		print leg_trigger 
		for x in range (6):
			stepping_down_calculation = [0,0,-5]
	    		downCalc=calculate_motion(stepping_down_calculation,l1)
			if leg_trigger[x] == False:
				j = x
		        	positionN([3*j+1,downCalc[3*j],3*j+2,downCalc[3*j+1],3*j+3,downCalc[3*j+2]])
		if False in leg_trigger:
			print "All legs are not in contact"
		else:	
			break
torque(0)
pwm_list = [800]*18
pwmAll(pwm_list)
scaler_acc = [20] * 18
scaler_vel = [50] * 18
velocityAll(scaler_vel)
accelerationAll(scaler_acc)
torque(1)
standUp()
time.sleep(1)
continiousTripodTactile(0, 30, 20, 20)
checkContact()	

#velocityAll(scaler_vel)
#accelerationAll(scaler_acc)
#torque(1)
#standUp()
#velocityAll(scaler_vel)
#accelerationAll(scaler_acc)
#time.sleep(1)
#translationZ(-50)
#time.sleep(1)
#velocityAll(scaler_vel)
#accelerationAll(scaler_acc)
#continiousTripodTactile(0, 10, 10, 20)
