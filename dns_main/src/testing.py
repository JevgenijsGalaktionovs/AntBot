#!/usr/bin/env python2
import time
from math import radians
from service_router import *
from locomotion     import *
#, positionN, \
#    velocityAll, accelerationAll, positionAll, readFSR
from kinematics import Kinematics

from math_calc import vector_length
K=Kinematics()


def standUpForStairs():
    standup_pos = [1948, 2048, 1296, 2148, 2048, 1296,
                   2048, 2048, 1296, 2048, 2048, 1296,
                   2148, 2048, 1296, 1948, 2048, 1296]

    front_standup = list_combine(leg[1] + leg[2], standup_pos)
    rear_standup = list_combine(leg[5] + leg[6], standup_pos)
    middle_standup = list_combine(leg[3] + leg[4], standup_pos)
    positionN(front_standup)
    time.sleep(1)
    positionN(rear_standup)
    time.sleep(1)
    positionN(middle_standup)
    time.sleep(1)

def initialDistance(distance):
    all_pos = readPos()
    ee_xyz, servopos = K.doFkine(all_pos)
    dist2FirstStep_1 = distance 
    dist2FirstStep_2 = distance
    dist2FirstStep_3 = distance + ee_xyz[1] - ee_xyz[7]
    dist2FirstStep_4 = distance + ee_xyz[1] - ee_xyz[10]
    dist2FirstStep_5 = distance + ee_xyz[1] - ee_xyz[13]
    dist2FirstStep_6 = distance + ee_xyz[1] - ee_xyz[16]
    dist2FirstStep = dist2FirstStep_1, dist2FirstStep_2, dist2FirstStep_3, dist2FirstStep_4, dist2FirstStep_5, dist2FirstStep_6
    print dist2FirstStep
    return dist2FirstStep

def moveForward(x, y, z, alpha, beta, gamma, distance):
    

    Forward =   [x, y, z]
    Up      =   [0, 0, z]
    Down    =   [x, y, 0]
    Push    =   [0, 0, 0]

    HalfForward =   [0.5*x, 0.5*y, z]
    HalfUp      =   [0, 0, z]
    HalfDown    =   [0.5*x, 0.5*y, 0]


    PushBackwards = calc_motion(Push)
    LiftUp        = calc_motion(Up)
    LiftDown      = calc_motion(Down)
    PutForward    = calc_motion(Forward)

  
    HalfLiftUp        = calc_motion(HalfUp)
    HalfLiftDown      = calc_motion(HalfDown)
    HalfPutForward    = calc_motion(HalfForward)

    
    while distance > 0.75 * stepSize:
        if distance > 1.5 * stepSize:
            pos = list()
            pos.extend(PushBackwards[0:6])
            pos.extend(LiftUp[6:12])
            pos.extend(LiftUp[12:18])
            pos.extend(PushBackwards[18:24])
            pos.extend(PushBackwards[24:30])
            pos.extend(LiftUp[30:36])
            positionN(pos)
            check_position_error(80, 50, pos)

            pos1 = list()
            pos1.extend(PushBackwards[0:6])
            pos1.extend(PutForward[6:12])
            pos1.extend(PutForward[12:18])
            pos1.extend(PushBackwards[18:24])
            pos1.extend(PushBackwards[24:30])
            pos1.extend(PutForward[30:36])
            positionN(pos1)
            check_position_error(80, 50, pos1)

            pos2 = list()
            pos2.extend(PushBackwards[0:6])
            pos2.extend(LiftDown[6:12])
            pos2.extend(LiftDown[12:18])
            pos2.extend(PushBackwards[18:24])
            pos2.extend(PushBackwards[24:30])
            pos2.extend(LiftDown[30:36])
            positionN(pos2)
            check_position_error(80, 50, pos2)

            pos3 = list()
            pos3.extend(LiftUp[0:6])
            pos3.extend(PushBackwards[6:12])
            pos3.extend(PushBackwards[12:18])
            pos3.extend(LiftUp[18:24])
            pos3.extend(LiftUp[24:30])
            pos3.extend(PushBackwards[30:36])
            positionN(pos3)
            check_position_error(80, 50, pos3)

            pos4 = list()
            pos4.extend(PushBackwards[0:6])
            pos4.extend(PushBackwards[6:12])
            pos4.extend(PushBackwards[12:18])
            pos4.extend(PushBackwards[18:24])
            pos4.extend(PushBackwards[24:30])
            pos4.extend(PushBackwards[30:36])
            positionN(pos4)
            check_position_error(80, 50, pos4)
            distance = distance -  stepSize
        else:
            pos = list()
            pos.extend(PushBackwards[0:6])
            pos.extend(HalfLiftUp[6:12])
            pos.extend(HalfLiftUp[12:18])
            pos.extend(PushBackwards[18:24])
            pos.extend(PushBackwards[24:30])
            pos.extend(HalfLiftUp[30:36])
            positionN(pos)
            check_position_error(80, 50, pos)

            pos1 = list()
            pos1.extend(PushBackwards[0:6])
            pos1.extend(HalfPutForward[6:12])
            pos1.extend(HalfPutForward[12:18])
            pos1.extend(PushBackwards[18:24])
            pos1.extend(PushBackwards[24:30])
            pos1.extend(HalfPutForward[30:36])
            positionN(pos1)
            check_position_error(80, 50, pos1)

            pos2 = list()
            pos2.extend(PushBackwards[0:6])
            pos2.extend(HalfLiftDown[6:12])
            pos2.extend(HalfLiftDown[12:18])
            pos2.extend(PushBackwards[18:24])
            pos2.extend(PushBackwards[24:30])
            pos2.extend(HalfLiftDown[30:36])
            positionN(pos2)
            check_position_error(80, 50, pos2)

            pos3 = list()
            pos3.extend(HalfLiftUp[0:6])
            pos3.extend(PushBackwards[6:12])
            pos3.extend(PushBackwards[12:18])
            pos3.extend(HalfLiftUp[18:24])
            pos3.extend(HalfLiftUp[24:30])
            pos3.extend(PushBackwards[30:36])
            positionN(pos3)
            check_position_error(80, 50, pos3)

            pos4 = list()
            pos4.extend(PushBackwards[0:6])
            pos4.extend(PushBackwards[6:12])
            pos4.extend(PushBackwards[12:18])
            pos4.extend(PushBackwards[18:24])
            pos4.extend(PushBackwards[24:30])
            pos4.extend(PushBackwards[30:36])
            positionN(pos4)
            check_position_error(80, 50, pos4)
            distance = distance -  (0.5 *stepSize)
    time.sleep(0.5)
    return distance   

def walkUp(distanceToStair, x, stepSize, threshold, riser, alpha, beta, gamma):
    orientation = [alpha,beta,gamma]

                
    Forward =   [x, stepSize, threshold]
    Up      =   [0, 0, threshold]
    Down    =   [x, stepSize, 0]
    Push    =   [0, 0, 0]

    UpForward       =   [x, stepSize, threshold+riser]
    StepUp          =   [0, 0, threshold+riser]
    StepDownFirst   =  [x, stepSize, threshold/2+riser]
    StepDownSecond  =  [x, 0, threshold/2+riser]

    PushBackwards = calc_motion(Push,orientation)
    LiftUp        = calc_motion(Up,orientation)
    LiftDown      = calc_motion(Down,orientation)
    PutForward    = calc_motion(Forward,orientation)

  
    StepUpForward        = calc_motion(UpForward,orientation)
    StepUpUp             = calc_motion(StepUp,orientation)
    StepDownDownFirst    = calc_motion(StepDownFirst,orientation)
    StepDownDownSecond   = calc_motion(StepDownSecond,orientation)

    pos = []

  
    ##Lift_Up_First_Leg
    for i in range(len(distanceToStair)):
        if i == 0 :
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            else:
                pos.extend(LiftUp[i*6 : i*6+6]) 
        elif i == 3:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            else:
                pos.extend(LiftUp[i*6 : i*6+6])
        elif i == 4:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            else:
                pos.extend(LiftUp[i*6 : i*6+6])  
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(PushBackwards[i*6 : i*6+6])
            else:
                pos.extend(PushBackwards[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Put_Forward_First_Leg
    for i in range(len(distanceToStair)):
        if i == 0:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpForward[i*6 : i*6+6])
            else:
                pos.extend(PutForward[i*6 : i*6+6]) 
        elif i == 3:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpForward[i*6 : i*6+6])
            else:
                pos.extend(PutForward[i*6 : i*6+6]) 
        elif i == 4:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpForward[i*6 : i*6+6])
            else:
                pos.extend(PutForward[i*6 : i*6+6]) 
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(PushBackwards[i*6 : i*6+6])
            else:
                pos.extend(PushBackwards[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Step_Down_First_leg
    for i in range(len(distanceToStair)):
        if i == 0:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownFirst[i*6 : i*6+6])
            else:
                pos.extend(LiftDown[i*6 : i*6+6]) 
        elif i == 3:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownFirst[i*6 : i*6+6])
            else:
                pos.extend(LiftDown[i*6 : i*6+6]) 
        elif i == 4:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownFirst[i*6 : i*6+6])
            else:
                pos.extend(LiftDown[i*6 : i*6+6]) 
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(PushBackwards[i*6 : i*6+6])
            else:
                pos.extend(PushBackwards[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    checkContactWithoutControlSystem()
    #########################################################################################################
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    UpPushBackwards     = [0, -stepSize, 0]
    StepUpPushBackwards = calc_motion(UpPushBackwards)
    ##Lift_Up_Second_Leg
    for i in range(len(distanceToStair)):
        if i == 1:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            else:
                pos.extend(LiftUp[i*6 : i*6+6])
        elif i == 2:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            else:
                pos.extend(LiftUp[i*6 : i*6+6])
        elif i == 5:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            
            else:
                pos.extend(LiftUp[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6]) 

    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Put_Forward_Second_Leg
    for i in range(len(distanceToStair)):
        if i == 1:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            else:
                pos.extend(LiftUp[i*6 : i*6+6])
        elif i == 2:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            else:
                pos.extend(LiftUp[i*6 : i*6+6])
        elif i == 5:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            else:
                pos.extend(LiftUp[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpPushBackwards[i*6 : i*6+6])
            else:
                pos.extend(StepUpPushBackwards[i*6 : i*6+6]) 

    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Step_Down_Second_leg
    for i in range(len(distanceToStair)):
        if i ==1:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownSecond[i*6 : i*6+6])
            else:
                pos.extend(PushBackwards[i*6 : i*6+6])
        elif i ==2:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownSecond[i*6 : i*6+6])
            else:
                pos.extend(PushBackwards[i*6 : i*6+6])
        elif i ==5:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownSecond[i*6 : i*6+6])
            else:
                pos.extend(PushBackwards[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpPushBackwards[i*6 : i*6+6])
            else:
                pos.extend(StepUpPushBackwards[i*6 : i*6+6]) 
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    checkContactWithoutControlSystem()
    distanceToStair = [i - stepSize for i in distanceToStair]

def updateDistance(distanceToStair, stepSize):
    distanceToStair = [i - stepSize for i in distanceToStair]
    for i in range(len(distanceToStair)):
        if distanceToStair[i] < 0:
            distanceToStair[i] = distanceToStair[i] + thread
    print distanceToStair
    return distanceToStair

def rotateAndTranslate(riser,climbed_stairs_front, climbed_stairs_rear):
    gamma, beta = K.get_orientation([1, 5, 6])
    parallelGait(0, -beta, -gamma, 0, 0, 0)
    time.sleep(2)
    a = K.calc_translationStairs(riser,climbed_stairs_front, climbed_stairs_rear)
    parallelGait(0, 0, 0, 0, a[1], a[0])
    time.sleep(2)
    return beta , gamma


def moveForwardOnStair(x, y, z, alpha, beta, gamma, distance):
    initialDistance = distance
    orientation = [alpha, beta, gamma]    

    Forward =   [x, y, z]
    Up      =   [0, 0, z]
    Down    =   [x, y, 0]
    Push    =   [0, 0, 0]

    HalfForward =   [0.5*x, 0.5*y, z]
    HalfUp      =   [0, 0, z]
    HalfDown    =   [0.5*x, 0.5*y, 0]


    PushBackwards = calc_motion(Push, orientation)
    LiftUp        = calc_motion(Up, orientation)
    LiftDown      = calc_motion(Down, orientation)
    PutForward    = calc_motion(Forward, orientation)

  
    HalfLiftUp        = calc_motion(HalfUp, orientation)
    HalfLiftDown      = calc_motion(HalfDown, orientation)
    HalfPutForward    = calc_motion(HalfForward, orientation)

    print (distance)

    while distance > 0.75 * stepSize:
        if distance > 1.5 * stepSize:
            pos = list()
            pos.extend(PushBackwards[0:6])
            pos.extend(LiftUp[6:12])
            pos.extend(LiftUp[12:18])
            pos.extend(PushBackwards[18:24])
            pos.extend(PushBackwards[24:30])
            pos.extend(LiftUp[30:36])
            positionN(pos)
            check_position_error(80, 50, pos)

            pos1 = list()
            pos1.extend(PushBackwards[0:6])
            pos1.extend(PutForward[6:12])
            pos1.extend(PutForward[12:18])
            pos1.extend(PushBackwards[18:24])
            pos1.extend(PushBackwards[24:30])
            pos1.extend(PutForward[30:36])
            positionN(pos1)
            check_position_error(80, 50, pos1)

            pos2 = list()
            pos2.extend(PushBackwards[0:6])
            pos2.extend(LiftDown[6:12])
            pos2.extend(LiftDown[12:18])
            pos2.extend(PushBackwards[18:24])
            pos2.extend(PushBackwards[24:30])
            pos2.extend(LiftDown[30:36])
            positionN(pos2)
            check_position_error(80, 50, pos2)

            pos3 = list()
            pos3.extend(LiftUp[0:6])
            pos3.extend(PushBackwards[6:12])
            pos3.extend(PushBackwards[12:18])
            pos3.extend(LiftUp[18:24])
            pos3.extend(LiftUp[24:30])
            pos3.extend(PushBackwards[30:36])
            positionN(pos3)
            check_position_error(80, 50, pos3)

            pos4 = list()
            pos4.extend(PushBackwards[0:6])
            pos4.extend(PushBackwards[6:12])
            pos4.extend(PushBackwards[12:18])
            pos4.extend(PushBackwards[18:24])
            pos4.extend(PushBackwards[24:30])
            pos4.extend(PushBackwards[30:36])
            positionN(pos4)
            check_position_error(80, 50, pos4)
            distance = distance -  stepSize
        else:
            pos = list()
            pos.extend(PushBackwards[0:6])
            pos.extend(HalfLiftUp[6:12])
            pos.extend(HalfLiftUp[12:18])
            pos.extend(PushBackwards[18:24])
            pos.extend(PushBackwards[24:30])
            pos.extend(HalfLiftUp[30:36])
            positionN(pos)
            check_position_error(80, 50, pos)

            pos1 = list()
            pos1.extend(PushBackwards[0:6])
            pos1.extend(HalfPutForward[6:12])
            pos1.extend(HalfPutForward[12:18])
            pos1.extend(PushBackwards[18:24])
            pos1.extend(PushBackwards[24:30])
            pos1.extend(HalfPutForward[30:36])
            positionN(pos1)
            check_position_error(80, 50, pos1)

            pos2 = list()
            pos2.extend(PushBackwards[0:6])
            pos2.extend(HalfLiftDown[6:12])
            pos2.extend(HalfLiftDown[12:18])
            pos2.extend(PushBackwards[18:24])
            pos2.extend(PushBackwards[24:30])
            pos2.extend(HalfLiftDown[30:36])
            positionN(pos2)
            check_position_error(80, 50, pos2)

            pos3 = list()
            pos3.extend(HalfLiftUp[0:6])
            pos3.extend(PushBackwards[6:12])
            pos3.extend(PushBackwards[12:18])
            pos3.extend(HalfLiftUp[18:24])
            pos3.extend(HalfLiftUp[24:30])
            pos3.extend(PushBackwards[30:36])
            positionN(pos3)
            check_position_error(80, 50, pos3)

            pos4 = list()
            pos4.extend(PushBackwards[0:6])
            pos4.extend(PushBackwards[6:12])
            pos4.extend(PushBackwards[12:18])
            pos4.extend(PushBackwards[18:24])
            pos4.extend(PushBackwards[24:30])
            pos4.extend(PushBackwards[30:36])
            positionN(pos4)
            check_position_error(80, 50, pos4)
            distance = distance -  (0.5 *stepSize)
    time.sleep(0.5)
    return distance

def walkUpAllLegs(distanceToStair, x, stepSize, threshold, riser, alpha, beta, gamma):
    orientation = [alpha,beta,gamma]

                
    Forward =   [x, stepSize, threshold]
    Up      =   [0, 0, threshold]
    Down    =   [x, stepSize, 0]
    Push    =   [0, 0, 0]

    UpForward       =   [x, stepSize, threshold+riser]
    StepUp          =   [0, 0, threshold+riser]
    StepDownFirst   =  [x, stepSize, threshold/2+riser]
    StepDownSecond  =  [x, 0, threshold/2+riser]

    PushBackwards = calc_motion(Push,orientation)
    LiftUp        = calc_motion(Up,orientation)
    LiftDown      = calc_motion(Down,orientation)
    PutForward    = calc_motion(Forward,orientation)

  
    StepUpForward        = calc_motion(UpForward,orientation)
    StepUpUp             = calc_motion(StepUp,orientation)
    StepDownDownFirst    = calc_motion(StepDownFirst,orientation)
    StepDownDownSecond   = calc_motion(StepDownSecond,orientation)

    pos = []

  
    ##Lift_Up_First_Leg
    for i in range(len(distanceToStair)):
        if i == 4:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(PushBackwards[i*6 : i*6+6])
            else:
                pos.extend(PushBackwards[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Put_Forward_First_Leg
    for i in range(len(distanceToStair)):
        if i == 4:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpForward[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(PushBackwards[i*6 : i*6+6])
            else:
                pos.extend(PushBackwards[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Step_Down_First_leg
    for i in range(len(distanceToStair)):
        if i == 4:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownFirst[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(PushBackwards[i*6 : i*6+6])
            else:
                pos.extend(PushBackwards[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    checkContactWithoutControlSystem()
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    #########################################################################################################
    ##Lift_Up_Second_Leg
    for i in range(len(distanceToStair)):
        if i == 5:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6]) 
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Put_Forward_Second_Leg
    for i in range(len(distanceToStair)):
        if i == 5:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpForward[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6]) 

    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Step_Down_Second_leg
    for i in range(len(distanceToStair)):
        if i ==5:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownFirst[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6]) 
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    checkContactWithoutControlSystem()
    distanceToStair = [i - stepSize for i in distanceToStair]
    parallelGait(0,0,0,0,0,riser/2)
    time.sleep(2)
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    Forward =   [x, stepSize, threshold]
    Up      =   [0, 0, threshold]
    Down    =   [x, stepSize, 0]
    Push    =   [0, 0, 0]

    UpForward       =   [x, stepSize, threshold+riser]
    StepUp          =   [0, 0, threshold+riser]
    StepDownFirst   =  [x, stepSize, threshold/2+riser]
    StepDownSecond  =  [x, 0, threshold/2+riser]

    PushBackwards = calc_motion(Push,orientation)
    LiftUp        = calc_motion(Up,orientation)
    LiftDown      = calc_motion(Down,orientation)
    PutForward    = calc_motion(Forward,orientation)

  
    StepUpForward        = calc_motion(UpForward,orientation)
    StepUpUp             = calc_motion(StepUp,orientation)
    StepDownDownFirst    = calc_motion(StepDownFirst,orientation)
    StepDownDownSecond   = calc_motion(StepDownSecond,orientation)
    ###########################################################################
    ##Lift_Up_First_Leg
    for i in range(len(distanceToStair)):
        if i == 2:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Put_Forward_First_Leg
    for i in range(len(distanceToStair)):
        if i == 2:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpForward[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Step_Down_First_leg
    for i in range(len(distanceToStair)):
        if i == 2:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownFirst[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    checkContactWithoutControlSystem()
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    #########################################################################################################
    ##Lift_Up_Second_Leg
    for i in range(len(distanceToStair)):
        if i == 3:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6]) 
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Put_Forward_Second_Leg
    for i in range(len(distanceToStair)):
        if i == 3:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpForward[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6]) 
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Step_Down_Second_leg
    for i in range(len(distanceToStair)):
        if i ==3:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownFirst[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6]) 
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    checkContactWithoutControlSystem()
    distanceToStair = [i - stepSize for i in distanceToStair]
    parallelGait(0,0,0,0,0,riser/2)
    time.sleep(2)
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    Forward =   [x, stepSize, threshold]
    Up      =   [0, 0, threshold]
    Down    =   [x, stepSize, 0]
    Push    =   [0, 0, 0]

    UpForward       =   [x, stepSize, threshold+riser]
    StepUp          =   [0, 0, threshold+riser]
    StepDownFirst   =  [x, stepSize, threshold/2+riser]
    StepDownSecond  =  [x, 0, threshold/2+riser]

    PushBackwards = calc_motion(Push,orientation)
    LiftUp        = calc_motion(Up,orientation)
    LiftDown      = calc_motion(Down,orientation)
    PutForward    = calc_motion(Forward,orientation)

  
    StepUpForward        = calc_motion(UpForward,orientation)
    StepUpUp             = calc_motion(StepUp,orientation)
    StepDownDownFirst    = calc_motion(StepDownFirst,orientation)
    StepDownDownSecond   = calc_motion(StepDownSecond,orientation)
        ###########################################################################
        ##Lift_Up_First_Leg
    for i in range(len(distanceToStair)):
        if i == 0:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Put_Forward_First_Leg
    for i in range(len(distanceToStair)):
        if i == 0:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpForward[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Step_Down_First_leg
    for i in range(len(distanceToStair)):
        if i == 0:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownFirst[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6])
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    checkContactWithoutControlSystem()
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    #########################################################################################################
    ##Lift_Up_Second_Leg
    for i in range(len(distanceToStair)):
        if i == 1:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6]) 
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Put_Forward_Second_Leg
    for i in range(len(distanceToStair)):
        if i == 1:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpForward[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6]) 

    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    ##Step_Down_Second_leg
    for i in range(len(distanceToStair)):
        if i ==1:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownFirst[i*6 : i*6+6])
        else:
            if distanceToStair[i] < stepSize:
                pos.extend(UpUpNothing[i*6 : i*6+6])
            else:
                pos.extend(UpUpNothing[i*6 : i*6+6]) 
    positionN(pos)
    check_position_error(80, 50, pos)
    pos = []
    checkContactWithoutControlSystem()
    distanceToStair = [i - stepSize for i in distanceToStair]




torque(0)
pwm_list = [800]*18
pwmAll(pwm_list)
scaler_acc = [20] * 18
scaler_vel = [30] * 18
velocityAll(scaler_vel)
accelerationAll(scaler_acc)
torque(1)
standUpForStairs()
time.sleep(1)
threshold = 50
stepSize = 50
riser = 150
thread = 260
error = 30


## Move forward to the first step on the stair. 700 = mm. Assuming the robot is placed at this distance 
#distanceToStair = initialDistance(moveForward(0, stepSize, threshold, 0, 0, 0, 700))
distanceToStair = 25.0, 25.0, 376.80185049724594, 376.02627441364115, 723.417427577023, 722.8063562905638

## Puts both front legs on the first step
#parallelGait(0,0,0,0,0,100)
#time.sleep(3)
#beta, gamma = rotateAndTranslate(riser, 1, 0)
#walkUp(distanceToStair,0, stepSize*2, threshold, riser, 0,0,0)
#newdistance = updateDistance(distanceToStair, stepSize*2)
#distance = min(newdistance) 
#print(distance)

## Move forward on stairs
#distance = moveForwardOnStair(0, stepSize, threshold, 0, -beta, 0, distance)
#print("this is the evaluated distance", distance)


## Walking up next stair 
#walkUp(distanceToStair,0, stepSize*2, threshold, riser, 0,-beta,0)
#beta, gamma = rotateAndTranslate(riser, 2, 0)
#parallelGait(0,beta,0,0,0,50)
#time.sleep(3)
#newdistance = updateDistance(distanceToStair, stepSize*2)
#print("new_Distance", newdistance)
#distance = min(newdistance) 
#print(distance)


#distanceToStair = 185.0, 185.0, 27.4003589943, 27, 627.7887313219506, 632.1407038810671
#walkUp(distanceToStair,0, stepSize*2, threshold, riser,0,-beta,0)
#beta = rotateAndTranslate(riser, 2, 0)
#distance = 80
#moveForwardOnStair(0, stepSize, threshold, 0, beta, 0, distance)
#parallelGait(0,beta,0,0,0,50)
#time.sleep(3)
#distanceToStair = 25.0, 25.0, 127.4003589943, 127, 627.7887313219506, 632.1407038810671
#walkUp(distanceToStair,0, stepSize*2, threshold, riser,0,beta,0)
#beta = rotateAndTranslate(riser, 2, 0)


#####Testing new stuff
parallelGait(0,0,0,0,0,riser/2)
time.sleep(2)
distanceToStair = 25.0, 25.0, 305.0, 305.0, 629.9592456137348, 629.7755305462598
walkUp(distanceToStair,0, stepSize*2, threshold, riser, 0,0,0)
newdistance = updateDistance(distanceToStair, stepSize*2)
print("new_Distance", newdistance)
distance = min(newdistance) 
print(distance)
distance = moveForwardOnStair(0, stepSize, threshold, 0, 0, 0, distance)
print distance
parallelGait(0,0,0,0,0,riser/2+20)
time.sleep(2)
distanceToStair = 25.0, 25.0, 25.0, 25.0, 629.9592456137348, 629.7755305462598
walkUp(distanceToStair,0, stepSize*2, threshold, riser, 0,0,0)
#parallelGait(0,0,-20,0,0,0)
#time.sleep(2)
#parallelGait(0,0,0,0,0,50)
time.sleep(2)
newdistance = updateDistance(distanceToStair, stepSize*2)
print("new_Distance", newdistance)
distance = min(newdistance) 
print(distance)
distance = moveForwardOnStair(0, stepSize, threshold, 0, 10, 0, distance)
print distance
#parallelGait(0,0,0,0,0,50)
#time.sleep(2)
distanceToStair = 25.0, 25.0, 25.0, 25.0, 25.9592456137348, 25.7755305462598
walkUpAllLegs(distanceToStair,0, stepSize*2, threshold, riser, 0,0,0)
parallelGait(0,0,0,0,100,30)
time.sleep(2)
newdistance = updateDistance(distanceToStair, stepSize*2)
print("new_Distance", newdistance)
distance = min(newdistance) 
print(distance)
distance = moveForwardOnStair(0, stepSize, threshold, 0, 10, 0, distance)
print distance
#parallelGait(0,0,0,0,0,50)
#time.sleep(2)
distanceToStair = 25.0, 25.0, 25.0, 25.0, 25.9592456137348, 25.7755305462598
walkUpAllLegs(distanceToStair,0, stepSize*2, threshold, riser, 0,0,0)
parallelGait(0,0,0,0,100,0)
time.sleep(2)
newdistance = updateDistance(distanceToStair, stepSize*2)
print("new_Distance", newdistance)
distance = min(newdistance) 
print(distance)
distance = moveForwardOnStair(0, stepSize, threshold, 0, 10, 0, distance)
print distance
#parallelGait(0,0,0,0,0,50)
#time.sleep(2)
distanceToStair = 25.0, 25.0, 25.0, 25.0, 25.9592456137348, 25.7755305462598
walkUpAllLegs(distanceToStair,0, stepSize*2, threshold, riser, 0,0,0)
parallelGait(0,0,0,0,100,0)
time.sleep(2)


