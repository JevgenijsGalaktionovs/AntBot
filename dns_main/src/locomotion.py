#!/usr/bin/env python2
import time
from math import radians

from service_router import readPos, positionN, \
    velocityAll, accelerationAll, positionAll, readFSR
from kinematics import Kinematics

from math_calc import vector_length


leg = {
    1: [1, 2, 3],     # IDs Leg 1
    2: [4, 5, 6],     # IDs Leg 2
    3: [7, 8, 9],     # IDs Leg 3
    4: [10, 11, 12],  # IDs Leg 4
    5: [13, 14, 15],  # IDs Leg 5
    6: [16, 17, 18]   # IDs Leg 6
}

ALL = [1, 2, 3, 4, 5, 6]  # Leg indexes
TG_1 = [1, 4, 5]  # Tripod Leg Group 1
TG_2 = [2, 3, 6]  # Tripod Leg Group 2


K = Kinematics()


# Locomotions, all work with current code as by 21.11.2019
def standUp():
    standup_pos = [2048, 2418, 824, 2048, 2418, 824,
                   2048, 2418, 824, 2048, 2418, 824,
                   2048, 2418, 824, 2048, 2418, 824]

    front_standup = list_combine(leg[1] + leg[2], standup_pos)
    rear_standup = list_combine(leg[5] + leg[6], standup_pos)
    middle_standup = list_combine(leg[3] + leg[4], standup_pos)
    positionN(front_standup)
    time.sleep(1)
    positionN(rear_standup)
    time.sleep(1)
    positionN(middle_standup)
    time.sleep(1)


def parallelGait(alpha, beta, gamma, dist_x, dist_y, dist_z):
    alpha_rad = radians(alpha)
    beta_rad = radians(beta)
    gamma_rad = radians(gamma)

    current_pos = readPos()
    next_pos = K.doIkineRotationEuler(current_pos, alpha_rad, beta_rad, gamma_rad, dist_x, dist_y, dist_z)

    #scaler = [20] * 18
    #velocityAll(scaler)
    #accelerationAll(scaler)

    positionAll(next_pos)
    time.sleep(0.35)


def yawRotation(alpha_deg):
    delay = 0.3
    alpha_rad = radians(alpha_deg)

    do_motion([0, 0, 20], leg_case=TG_2)
    time.sleep(delay)

    current_pos = readPos()
    next_pos = K.doIkineRotationEuler(current_pos, alpha_rad, 0, 0, 0, 0, 0)
    pos_list = list_combine(leg[1] + leg[4] + leg[5], next_pos)
    positionN(pos_list)
    time.sleep(delay)

    do_motion([0, 0, -20], leg_case=TG_2)
    time.sleep(delay)

    do_motion([0, 0, 20], leg_case=TG_1)
    time.sleep(delay)

    positionN([1, 2048, 10, 2048, 13, 2048])
    time.sleep(delay)

    final_pos = list_combine(leg[1] + leg[4] + leg[5], current_pos)
    positionN(final_pos)
    time.sleep(delay)


def rippleGait(x, y, z, iterations):
    init_pos = readPos()
    delay = 0.3

    move1 = [x, y, z]
    move2 = [-x / 2, -y / 2, 0]
    move3 = [0, 0, -z]

    for i in range(iterations):

        do_motion(move1, leg_case=[1, 4])
        do_motion(move2, leg_case=[2, 3, 5, 6])
        time.sleep(delay)
        do_motion(move3, leg_case=[1, 4])
        time.sleep(delay)

        do_motion(move1, leg_case=[3, 6])
        do_motion(move2, leg_case=[1, 2, 4, 5])
        time.sleep(delay)
        do_motion(move3, leg_case=[3, 6])
        time.sleep(delay)

        do_motion(move1, leg_case=[2, 5])
        do_motion(move2, leg_case=[1, 3, 4, 6])
        time.sleep(delay)
        do_motion(move3, leg_case=[2, 5])
        time.sleep(delay)

        positionAll(init_pos)
        time.sleep(delay)


def waveGait(x, y, z, iterations):
    init_pos = readPos()
    delay = 0.1

    one_leg_motion_up = [x, y, z]
    one_leg_motion_down = [0, 0, -z]
    five_leg_motion = [-x / 6, -y / 6, 0]
    for i in range(iterations):

        do_motion(one_leg_motion_up, leg_case=1)
        do_motion(five_leg_motion, leg_case=[2, 3, 4, 5, 6])
        time.sleep(delay)

        do_motion(one_leg_motion_down, leg_case=1)
        do_motion(one_leg_motion_up, leg_case=3)
        do_motion(five_leg_motion, leg_case=[2, 3, 4, 5, 6])
        time.sleep(delay)

        do_motion(one_leg_motion_down, leg_case=3)
        do_motion(one_leg_motion_up, leg_case=5)
        do_motion(five_leg_motion, leg_case=[1, 2, 4, 6])
        time.sleep(delay)

        do_motion(one_leg_motion_down, leg_case=5)
        do_motion(one_leg_motion_up, leg_case=2)
        do_motion(five_leg_motion, leg_case=[1, 3, 4, 6])
        time.sleep(delay)

        do_motion(one_leg_motion_down, leg_case=2)
        do_motion(one_leg_motion_up, leg_case=4)
        do_motion(five_leg_motion, leg_case=[1, 3, 5, 6])
        time.sleep(delay)

        do_motion(one_leg_motion_down, leg_case=4)
        do_motion(one_leg_motion_up, leg_case=6)
        do_motion(five_leg_motion, leg_case=[1, 2, 3, 5])
        time.sleep(delay)

        positionAll(init_pos)
        time.sleep(delay)


def tripodGait(x, y, z, iterations):

    start_pos = tripodGait_start(x, y, z)
    tripodGait_full(x, y, z, iterations, start_pos=start_pos)
    tripodGait_finish(x, y, z)


def tripodGait_start(x, y, z):
    delay = 0.2

    TG1_m1 = [-x, -y, 0]  # Tripod Group 1 : Motion 1

    TG2_m1 = [x, y, z]   # Tripod Group 2 : Motion 1
    TG2_m2 = [0, 0, -z]   # Tripod Group 2 : Motion 2

    # Motion 1
    do_motion(TG2_m1, leg_case=TG_2)
    do_motion(TG1_m1, leg_case=TG_1)
    time.sleep(delay)
    # Motion 2
    do_motion(TG2_m2, leg_case=TG_2)
    time.sleep(delay)
    current_pos = readPos()
    return current_pos


def tripodGait_full(x, y, z, iterations, start_pos=None):
    delay = 0.2

    if start_pos:
        init_pos = start_pos
    else:
        init_pos = [2002, 2218, 957, 2012, 1918, 2971, 2127, 2200, 1027, 2123, 1887, 3048, 2011, 2188, 1097, 2003, 1872, 3120]
    for i in range(iterations):

        TG1_m1 = [2 * x, 2 * y, z]   # Tripod Group 1 : Motion 1
        TG1_m2 = [0, 0, -z]           # Tripod Group 1 : Motion 2
        TG1_m3 = [-2 * x, -2 * y, 0]  # Tripod Group 1 : Motion 3

        TG2_m1 = [-2 * x, -2 * y, 0]  # Tripod Group 2 : Motion 1
        TG2_m3 = [2 * x, 2 * y, z]    # Tripod Group 2 : Motion 3
        TG2_m4 = [0, 0, -z]           # Tripod Group 1 : Motion 4

        # Motion 1
        do_motion(TG1_m1, leg_case=TG_1)
        time.sleep(0.05)
        do_motion(TG2_m1, leg_case=TG_2)
        time.sleep(delay)

        # Motion 2
        do_motion(TG1_m2, leg_case=TG_1)
        time.sleep(delay)

        # Motion 3
        do_motion(TG2_m3, leg_case=TG_2)
        time.sleep(0.05)
        do_motion(TG1_m3, leg_case=TG_1)
        time.sleep(delay)

        # Motion 4
        do_motion(TG2_m4, leg_case=TG_2)
        time.sleep(delay)

        # Motion 5
        positionAll(init_pos)
        time.sleep(delay)


def tripodGait_finish(x, y, z):
    delay = 0.15

    TG1_m1 = [0, 0, z]   # Tripod Group 1 : Motion 1
    TG1_m2 = [x, y, 0]   # Tripod Group 1 : Motion 2
    TG1_m3 = [0, 0, -z]   # Tripod Group 1 : Motion 3

    TG2_m4 = [0, 0, z]   # Tripod Group 2 : Motion 4
    TG2_m5 = [-x, -y, 0]   # Tripod Group 2 : Motion 5
    TG2_m6 = [0, 0, -z]   # Tripod Group 2 : Motion 6
    # Motion 1
    do_motion(TG1_m1, leg_case=TG_1)
    time.sleep(delay)

    # Motion 2
    do_motion(TG1_m2, leg_case=TG_1)
    time.sleep(delay)

    # Motion 3
    do_motion(TG1_m3, leg_case=TG_1)
    time.sleep(delay)

    # Motion 4
    do_motion(TG2_m4, leg_case=TG_2)
    time.sleep(delay)

    # Motion 5
    do_motion(TG2_m5, leg_case=TG_2)
    time.sleep(delay)

    # Motion 6
    do_motion(TG2_m6, leg_case=TG_2)
    time.sleep(delay)


def clear_view_stairs():
    delay = 2
    motion1 = [0, 60, 30]
    motion2 = [0, 0, -30]
    motion3 = [50, -80, 20]
    motion4 = [-50, -80, 20]
    motion5 = [0, 0, -15]

    do_motion(motion1, leg_case=[3, 4])
    time.sleep(delay)

    do_motion(motion2, leg_case=[3, 4])
    time.sleep(delay)

    do_motion(motion3, leg_case=1)
    do_motion(motion4, leg_case=2)
    time.sleep(delay)
    do_motion(motion5, leg_case=[1, 2])
    time.sleep(delay)
# Gaits end --------------------------------------------


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


def list_combine_notfull(id_list, value_list):
    ''' Parameters: id_list: list of servo IDs (any order, any number of IDs from 1 to 18)
                    value_list: list of n servo IDs (have to be in order by legs).
        Return:     list of format: [ID_1, Value_1, ... , ID_n, Value_n]
    '''
    sr_count = 0
    output = [0] * 2 * len(id_list)  # output size must be:  # of servos * 2 (ID + VALUE)
    for x in range(len(id_list)):
        output[x + sr_count] = id_list[x]
        output[x + sr_count + 1] = value_list[x]
        sr_count += 1
    return output


def auto_calcTrajectory(x, y, z, leg_case):
    current_pos = readPos()
    ee_xyz, servoPos = K.doFkine(current_pos)
    ee_xyz = [ee_xyz[3 * (leg_case - 1)],
              ee_xyz[3 * (leg_case - 1) + 1],
              ee_xyz[3 * (leg_case - 1) + 2]]
    leng = vector_length(ee_xyz)

    while K.calc_ikine(x, y, z, ee_xyz, K.leg_list[leg_case - 1], auto=1) == -1:
        if leg_case % 2 == 1:
            #if leng >= 483:
            x += 1
        #else:
        #        x -= 1
        elif leg_case % 2 == 0:
         #   if leng <= 483:
            x = x - 1
            #else:
            #    x = x + 1
    return x, y, z


def calc_motion(xyz, orientation=None, leg_case=None):

    ID_list = list()
    if leg_case is None:
        leg_case = [1, 2, 3, 4, 5, 6]  # If nothing passed to function, compute for ALL legs
    elif isinstance(leg_case, int):
        leg_case = [leg_case]
    elif isinstance(leg, tuple):
        leg_case = list(leg_case)

    for x in range((len(leg_case))):
        ID_list += leg[leg_case[x]]

    current_pos = readPos()
    next_pos = K.doIkine(current_pos, xyz[0], xyz[1], xyz[2], body_orient=orientation, leg=leg_case)

    if leg_case:
        motion = list_combine_notfull(ID_list, next_pos)
    else:
        motion = list_combine(ID_list, next_pos)
    return motion


def do_motion(xyz, orientation=None, leg_case=None):
    """x, y, z: 3 integers with x,y,z changes to accomplish
       orientaiton: list of 3 integers in degrees. alpha, beta, gamma
       leg_nr: list (can be one) of leg indexes"""
    motion = calc_motion(xyz, orientation=orientation, leg_case=leg_case)
    positionN(motion)
    return motion


def singleLeg_stairs(x, y, z, alpha, beta, gamma, leg_case):
    x, y, z = auto_calcTrajectory(x, y, z, leg_case)
    motion = calc_motion([x, y, z], orientation=[alpha, beta, gamma], leg_case=leg_case)
    return motion, [x, y, z]


def half_step(x, y, z, alpha, beta, gamma):

    move1 = [0, -y, 0]
    move2 = [0, 0, z]
    move3 = [0, 0, -z]
    move4 = [0, 0, 0]
    pos = list()
    pos.extend(calc_motion(move1, orientation=[alpha, beta, gamma], leg_case=1))
    pos.extend(calc_motion(move2, orientation=[alpha, beta, gamma], leg_case=2))
    pos.extend(calc_motion(move2, orientation=[alpha, beta, gamma], leg_case=3))
    pos.extend(calc_motion(move1, orientation=[alpha, beta, gamma], leg_case=4))
    pos.extend(calc_motion(move1, orientation=[alpha, beta, gamma], leg_case=5))
    pos.extend(calc_motion(move2, orientation=[alpha, beta, gamma], leg_case=6))
    positionN(pos)
    check_position_error(80, 50, pos)

    pos2 = list()
    pos2.extend(calc_motion(move4, orientation=[alpha, beta, gamma], leg_case=1))
    pos2.extend(calc_motion(move3, orientation=[alpha, beta, gamma], leg_case=2))
    pos2.extend(calc_motion(move3, orientation=[alpha, beta, gamma], leg_case=3))
    pos2.extend(calc_motion(move4, orientation=[alpha, beta, gamma], leg_case=4))
    pos2.extend(calc_motion(move4, orientation=[alpha, beta, gamma], leg_case=5))
    pos2.extend(calc_motion(move3, orientation=[alpha, beta, gamma], leg_case=6))
    positionN(pos2)
    check_position_error(80, 50, pos2)
    checkContact()


def checkContact():
    [x, y, z] = [0, 0, -5]
    current_pos = readPos()
    goal_pos = K.doIkine(current_pos, x, y, z)

    for j in range(40):  # 20 equals to total 10cm distance that leg will go down.
        fsr = readFSR()
        print fsr
        for x in range(6):
            if fsr[x] == 0:
                positionN([3 * x + 1, goal_pos[3 * x],
                           3 * x + 2, goal_pos[3 * x + 1],
                           3 * x + 3, goal_pos[3 * x + 2]])
        time.sleep(0.2)
        if all(sensor == 1 for sensor in fsr) is True:
            break
        else:
            leg_list = list()
            for leg in range(len(fsr)):
                if fsr[leg] == 0:
                    leg_list.append(leg)
        goal_pos = ControlSystem(goal_pos, 0, 0, -5, leg_list)


def ControlSystem(goal_pos, x, y, z, leg_list):
    gain_x = 1  # 1.2
    gain_y = -0.8  # -0.8
    gain_z = 3  # 3
    current_pos = readPos()
    curr_ee_xyz = K.doFkine(current_pos)[0]
    goal_ee_xyz = K.doFkine(goal_pos)[0]
    err_ee_xyz = [i - j for i, j in zip(goal_ee_xyz, curr_ee_xyz)]

    for i in range(6):
        err_ee_xyz[3 * i] = err_ee_xyz[3 * i] * gain_x
        err_ee_xyz[3 * i + 1] = err_ee_xyz[3 * i + 1] * gain_y
        err_ee_xyz[3 * i + 2] = err_ee_xyz[3 * i + 2] * gain_z
    ee_xyz = [i - j for i, j in zip(goal_ee_xyz, err_ee_xyz)]

    new_pos = []
    for leg in range(6):  # To list through numbers 1,2,3,4,5,6
        if leg in leg_list:
            new_pos.extend(K.rad_to_step(K.calc_ikine(x, y, z, ee_xyz[3 * leg:3 * leg + 3], K.leg_list[leg])))
        else:
            new_pos.append(current_pos[3 * leg])
            new_pos.append(current_pos[3 * leg + 1])
            new_pos.append(current_pos[3 * leg + 2])

    result = [int(next_pos) for next_pos in new_pos]
    return result


def check_position_error(iter, allowed_error, desired_pos):
    err_pos = [0] * 18
    des_pos = list((desired_pos[i + 1] for i in xrange(0, len(desired_pos), 2)))

    for x in range(iter):
        cur_pos = readPos()
        abs_err_pos = 0
        for i in range(len(des_pos)):
            err_pos[i] = abs(cur_pos[i] - des_pos[i])
        for j in range(6):
            abs_err_pos += (err_pos[j * 3] + err_pos[(j * 3) + 1] + err_pos[(j * 3) + 2]) / 3
        if abs_err_pos < allowed_error:
            print("Accepted Absolute Error: ", abs_err_pos)
            break


def tripodGait_stairs(stairs, distance, depth, riser):
    all_pos = readPos()
    ee_xyz, servopos = K.doFkine(all_pos)
    gamma, beta = K.get_orientation([1, 5, 6])
    print ("gamma, beta", gamma, beta)
    alpha = 0
    step = 50
    ae = []
    ae1 = []
    lift = 20
    climbed_stairs_front = 0
    climbed_stairs_rear = 0
    leg1_lifted_up = False
    leg2_lifted_up = False
    leg3_lifted_up = False
    leg4_lifted_up = False
    leg5_lifted_up = False
    leg6_lifted_up = False
    dist2NextLevel_1 = distance
    dist2NextLevel_2 = distance
    dist2NextLevel_3 = distance + ee_xyz[1] - ee_xyz[7]
    dist2NextLevel_4 = distance + ee_xyz[1] - ee_xyz[10]
    dist2NextLevel_5 = distance + ee_xyz[1] - ee_xyz[13]
    dist2NextLevel_6 = distance + ee_xyz[1] - ee_xyz[16]
    print("dist2NextLevel", dist2NextLevel_1, dist2NextLevel_2, dist2NextLevel_3,
    dist2NextLevel_4, dist2NextLevel_5, dist2NextLevel_6)
    half_step(0, step, lift, alpha, beta, gamma)
    dist2NextLevel_2 = dist2NextLevel_2 - step
    dist2NextLevel_3 = dist2NextLevel_3 - step
    dist2NextLevel_6 = dist2NextLevel_6 - step

    print("dist2NextLevel", dist2NextLevel_1,dist2NextLevel_2, dist2NextLevel_3,dist2NextLevel_4,dist2NextLevel_5, dist2NextLevel_6)

    while stairs is True:
        ae = []
        ae1 = []
        if dist2NextLevel_1 < 2 * step:
            ae_stored1, xyz_stored1 = singleLeg_stairs(0, 0, riser + lift, alpha, beta, gamma, 1)
            ae.extend(ae_stored1)
            print("leg1", xyz_stored1)
        elif dist2NextLevel_1 > 2 * step:
            xyz_stored1 = [0] * 3
            ae.extend(calc_motion([0, 0, lift], orientation=[alpha, beta, gamma], leg_case=1))
        ae.extend(calc_motion([0, -step, 0], orientation=[alpha, beta, gamma], leg_case=2))
        ae.extend(calc_motion([0, -step, 0], orientation=[alpha, beta, gamma], leg_case=3))
        if dist2NextLevel_4 < 2 * step:
            ae_stored4, xyz_stored4 = singleLeg_stairs(0, 0, riser + lift, alpha, beta, gamma, 4)
            ae.extend(ae_stored4)
            print("leg4", xyz_stored4)
        elif dist2NextLevel_4 > 2 * step:
            xyz_stored4 = [0] * 3
            ae.extend(calc_motion([0, 0, lift], orientation=[alpha, beta, gamma], leg_case=4))
        if dist2NextLevel_5 < 2 * step:
            ae_stored5, xyz_stored5 = singleLeg_stairs(0, 0, riser + lift, alpha, beta, gamma, 5)
            ae.extend(ae_stored5)
            print("leg5", xyz_stored5)
        elif dist2NextLevel_5 > 2 * step:
            xyz_stored5 = [0] * 3
            ae.extend(calc_motion([0, 0, lift], orientation=[alpha, beta, gamma], leg_case=5))
        ae.extend(calc_motion([0, -step, 0], orientation=[alpha, beta, gamma], leg_case=6))
        ee_xyz, servopos = K.doFkine(readPos())
        z1 = ee_xyz[2]
        z4 = ee_xyz[11]
        z5 = ee_xyz[14]
        positionN(ae)
        print ("ae",ae)
        check_position_error(80, 30, ae)
    
        # put forward ae1

        ae1.extend(calc_motion([-xyz_stored1[0], step, 0], orientation=[alpha, beta, gamma], leg_case=1))
        ae1.extend(calc_motion([0, 0, 0], orientation=[alpha, beta, gamma], leg_case=2))
        ae1.extend(calc_motion([0, 0, 0], orientation=[alpha, beta, gamma], leg_case=3))
        ae1.extend(calc_motion([-xyz_stored4[0],  step, 0], orientation=[alpha, beta, gamma], leg_case=4))
        ae1.extend(calc_motion([-xyz_stored5[0],  step, 0], orientation=[alpha, beta, gamma], leg_case=5))
        ae1.extend(calc_motion([0, 0, 0], orientation=[alpha, beta, gamma], leg_case=6))
        positionN(ae1)
        check_position_error(80, 50, ae1)
        checkContact()
        checkContact()
        ee_xyz, servopos = K.doFkine(readPos())
        z1_new = ee_xyz[2]
        z4_new = ee_xyz[11]
        z5_new = ee_xyz[14]
        dist2NextLevel_1 = dist2NextLevel_1 - 2 * step
        if z1_new - z1 > riser / 2:  # the leg is lifted up
            leg1_lifted_up = True
            if dist2NextLevel_1 > 0:
                dist2NextLevel_1 = depth - 5
            else:
                dist2NextLevel_1 = depth + dist2NextLevel_1
        else:
            if dist2NextLevel_1 < 0:
                dist2NextLevel_1 = 10

        dist2NextLevel_4 = dist2NextLevel_4 - 2 * step
        if z4_new - z4 > riser / 2:  # the leg is lifted up
            leg4_lifted_up = True
            if dist2NextLevel_4 > 0:
                dist2NextLevel_4 = depth - 5
            else:
                dist2NextLevel_4 = depth + dist2NextLevel_4
        else:
            if dist2NextLevel_4 < 0:
                dist2NextLevel_4 = 10
        dist2NextLevel_5 = dist2NextLevel_5 - 2 * step
        if z5_new - z5 > riser / 2:  # the leg is lifted up
            leg5_lifted_up = True
            if dist2NextLevel_5 > 0:
                dist2NextLevel_5 = depth - 5
            else:
                dist2NextLevel_5 = depth + dist2NextLevel_5
        else:
            if dist2NextLevel_5 < 0:
                dist2NextLevel_5 = 10

        print("dist", dist2NextLevel_1, dist2NextLevel_2, dist2NextLevel_3, dist2NextLevel_4, dist2NextLevel_5, dist2NextLevel_6)
    ########
        ee_xyz = []
        ee_xyz, servopos = K.doFkine(readPos())
        z1 = ee_xyz[2]
        z2 = ee_xyz[5]
        z3 = ee_xyz[8]
        z4 = ee_xyz[12]
        z5 = ee_xyz[14]
        z6 = ee_xyz[17]
        z_front = abs(z1 - z2)
        z_rear = abs(z5 - z6)
        if (leg1_lifted_up is True) and (leg2_lifted_up is True):
            climbed_stairs_front += 1
            leg1_lifted_up = False
            leg2_lifted_up = False
        if (leg5_lifted_up is True) and (leg6_lifted_up is True):
            climbed_stairs_rear += 1
            leg5_lifted_up = False
            leg6_lifted_up = False
        if (z_front < 15) and (z_rear < 15):
            gamma, beta = K.get_orientation([1, 5, 6])
            parallelGait(0, -beta, -gamma, 0, 0, 0)
            time.sleep(1)
            a = K.calc_translationStairs(riser,climbed_stairs_front, climbed_stairs_rear)
            parallelGait(0, 0, 0, 0, a[1], a[0])
            time.sleep(1)
    ########
    # seconed group lift up and push
        ae = []
        ae1 = []
        ae.extend(calc_motion([0, -step, 0], orientation=[alpha, beta, gamma], leg_case=1))
        if dist2NextLevel_2 < 2 * step:
            ae_stored2, xyz_stored2 = singleLeg_stairs(0, 0, riser + lift, alpha, beta, gamma, 2)
            ae.extend(ae_stored2)
            print("leg2", xyz_stored2)
        elif dist2NextLevel_2 > 2 * step:
            xyz_stored2 = [0] * 3
            ae.extend(calc_motion([0, 0, lift], orientation=[alpha, beta, gamma], leg_case=2))

        if dist2NextLevel_3 < 2 * step:
            ae_stored3, xyz_stored3 = singleLeg_stairs(0, 0, riser + lift, alpha, beta, gamma, 3)
            ae.extend(ae_stored3)
            print("leg3", xyz_stored3)
        elif dist2NextLevel_3 > 2 * step:
            xyz_stored3 = [0] * 3
            ae.extend(calc_motion([0, 0, lift], orientation=[alpha, beta, gamma], leg_case=3))
        ae.extend(calc_motion([0, -step, 0], orientation=[alpha, beta, gamma], leg_case=4))
        ae.extend(calc_motion([0, -step, 0], orientation=[alpha, beta, gamma], leg_case=5))
        if dist2NextLevel_6 < 2 * step:
            ae_stored6, xyz_stored6 = singleLeg_stairs(0, 0, riser + lift, alpha, beta, gamma, 6)
            ae.extend(ae_stored6)
            print("leg6", xyz_stored6)
        elif dist2NextLevel_6 > 2 * step:
            xyz_stored6 = [0] * 3
            ae.extend(calc_motion([0, 0, lift], orientation=[alpha, beta, gamma], leg_case=6))
        ee_xyz, servopos = K.doFkine(readPos())
        z2 = ee_xyz[5]
        z3 = ee_xyz[8]
        z6 = ee_xyz[17]
        positionN(ae)
        check_position_error(80, 30, ae)
    # put forward ae1
        ae1.extend(calc_motion([0, 0, 0], orientation=[alpha, beta, gamma], leg_case=1))
        ae1.extend(calc_motion([-xyz_stored2[0], step, 0], orientation=[alpha, beta, gamma], leg_case=2))
        ae1.extend(calc_motion([-xyz_stored3[0], step, 0], orientation=[alpha, beta, gamma], leg_case=3))
        ae1.extend(calc_motion([0, 0, 0], orientation=[alpha, beta, gamma], leg_case=4))
        ae1.extend(calc_motion([0, 0, 0], orientation=[alpha, beta, gamma], leg_case=5))
        ae1.extend(calc_motion([-xyz_stored6[0], step, 0], orientation=[alpha, beta, gamma], leg_case=6))
        positionN(ae1)
        check_position_error(80, 30, ae1)
        checkContact()
        checkContact()
    # put down
        checkContact()
        checkContact()
        ee_xyz = []
        ee_xyz, servopos = K.doFkine(readPos())
        z2_new = ee_xyz[5]
        z3_new = ee_xyz[8]
        z6_new = ee_xyz[17]
        dist2NextLevel_2 = dist2NextLevel_2 - 2 * step
        if z2_new - z2 > riser / 2:  # the leg is lifted up
            leg2_lifted_up = True
            if dist2NextLevel_2 > 0:
                dist2NextLevel_2 = depth - 5
            else:
                dist2NextLevel_2 = depth + dist2NextLevel_2
        else:
            if dist2NextLevel_2 < 0:
                dist2NextLevel_2 = 10

        dist2NextLevel_3 = dist2NextLevel_3 - 2 * step
        if z3_new - z3 > riser / 2:  # the leg is lifted up
            leg3_lifted_up = True
            if dist2NextLevel_3 > 0:
                dist2NextLevel_3 = depth - 3
            else:
                dist2NextLevel_3 = depth + dist2NextLevel_3
        else:
            if dist2NextLevel_3 < 0:
                dist2NextLevel_3 = 10

        dist2NextLevel_6 = dist2NextLevel_6 - 2 * step
        if z6_new - z6 > riser / 2:  # the leg is lifted up
            leg6_lifted_up = True
            if dist2NextLevel_6 > 0:
                dist2NextLevel_6 = depth - 5
            else:
                dist2NextLevel_6 = depth + dist2NextLevel_6
        else:
            if dist2NextLevel_6 < 0:
                dist2NextLevel_6 = 10

        print("dist", dist2NextLevel_1, dist2NextLevel_2, dist2NextLevel_3, dist2NextLevel_4, dist2NextLevel_5, dist2NextLevel_6)
        ee_xyz = []
        ee_xyz, servopos = K.doFkine(readPos())
        z1 = ee_xyz[2]
        z2 = ee_xyz[5]
        z3 = ee_xyz[8]
        z4 = ee_xyz[12]
        z5 = ee_xyz[14]
        z6 = ee_xyz[17]
        z_front = abs(z1 - z2)
        z_rear = abs(z5 - z6)
        if (leg1_lifted_up is True) and (leg2_lifted_up is True):
            climbed_stairs_front += 1
            leg1_lifted_up = False
            leg2_lifted_up = False
        if (leg1_lifted_up is True) and (leg2_lifted_up is True):
            climbed_stairs_rear += 1
            leg5_lifted_up = False
            leg6_lifted_up = False
        if (z_front < 30) and (z_rear < 30):
            gamma, beta = K.get_orientation([1, 5, 6])
            time.sleep(2)
            parallelGait(0, -beta, -gamma, 0, 0, 0)
            time.sleep(2)
            a = K.calc_translationStairs(riser,climbed_stairs_front, climbed_stairs_rear)
            time.sleep(2)
            parallelGait(0, 0, 0, 0, a[1], a[0])
            time.sleep(2)


def checkContactWithoutControlSystem():


    for j in range(30):  # 20 equals to total 10cm distance that leg will go down.
        fsr = readFSR()
        print fsr
        [x, y, z] = [0, 0, -5]
        current_pos = readPos()
        goal_pos = K.doIkine(current_pos, x, y, z)
        ee_xyz = K.doFkine(goal_pos)[0]
        new_pos = []
        if all(sensor == 1 for sensor in fsr) is True:
            break
        else:
            leg_list = list()
            for leg in range(len(fsr)):
                if fsr[leg] == 0:
                    leg_list.append(leg)
        for x in range(6):
            if fsr[x] == 0:
                positionN([3 * x + 1, goal_pos[3 * x],
                           3 * x + 2, goal_pos[3 * x + 1],
                           3 * x + 3, goal_pos[3 * x + 2]])
        time.sleep(0.2)
        if leg in leg_list:
            new_pos.extend(K.rad_to_step(K.calc_ikine(x, y, z, ee_xyz[3 * leg:3 * leg + 3], K.leg_list[leg])))
        else:
            new_pos.append(current_pos[3 * leg])
            new_pos.append(current_pos[3 * leg + 1])
            new_pos.append(current_pos[3 * leg + 2])
        goal_pos = [int(next_pos) for next_pos in new_pos]


def check_position_error_legs(iter, allowed_error, desired_pos, leg_case):    
    err_pos = [0] * len(leg_case)*3
    des_pos = list((desired_pos[i + 1] for i in xrange(0, len(desired_pos), 2)))
    for x in range(iter):
        pos = readPos()
        cur_pos = []
        for i in range (len(leg_case)):
            cur_pos.extend(pos[(leg_case[i]-1)*3 : (leg_case[i]-1)*3+3])
        abs_err_pos = 0
        for i in range(len(des_pos)):
            err_pos[i] = abs(cur_pos[i] - des_pos[i])
        for j in range(len(leg_case)):
            abs_err_pos += (err_pos[j * 3] + err_pos[(j * 3) + 1] + err_pos[(j * 3) + 2]) / 3
        if abs_err_pos < allowed_error:
            break

