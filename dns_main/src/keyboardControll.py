#!/usr/bin/env python
import time
from math import radians
from service_router import *
from locomotion     import *
from math import asin, pi, atan2
#, positionN, \
#    velocityAll, accelerationAll, positionAll, readFSR
from kinematics import Kinematics
# from math_calc import vector_length

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


def Stand_up(): 
    torque(0)
    pwm_list = [800]*18         #Setting PWM to "high" max is 885
    pwmAll(pwm_list)
    scaler_acc = [20] * 18      #Setting Acceleration to "low"
    scaler_vel = [20] * 18      #Setting Velocity to "low"
    velocityAll(scaler_vel)
    accelerationAll(scaler_acc)
    torque(1)
    standup_pos = [2048, 2048, 1296, 2048, 2048, 1296,
                   2048, 2048, 1296, 2048, 2048, 1296,
                   2048, 2048, 1296, 2048, 2048, 1296]

    front_standup = list_combine(leg[1] + leg[2], standup_pos)
    rear_standup = list_combine(leg[5] + leg[6], standup_pos)
    middle_standup = list_combine(leg[3] + leg[4], standup_pos)
    positionN(front_standup)
    time.sleep(1)
    positionN(rear_standup)
    time.sleep(1)
    positionN(middle_standup)
    time.sleep(1)


def move(PushBackwards, LiftUp, LiftDown, PutForward):

    pos = list()
    pos.extend(LiftUp[6:12])
    pos.extend(LiftUp[12:18])
    pos.extend(LiftUp[30:36])
    positionN(pos)
    leg_case = [2,3,6]
    check_position_error_legs(20, 60, pos, leg_case)

    pos1 = list()
    pos1.extend(PutForward[6:12])
    pos1.extend(PutForward[12:18])
    pos1.extend(PutForward[30:36])
    positionN(pos1)
    leg_case = [2,3,6]
    check_position_error_legs(20, 60, pos1, leg_case)

    pos2 = list()
    pos2.extend(LiftDown[6:12])
    pos2.extend(LiftDown[12:18])
    pos2.extend(LiftDown[30:36])
    positionN(pos2)
    leg_case = [2,3,6]
    check_position_error_legs(20, 60, pos2, leg_case)

    pos3 = list()
    pos3.extend(LiftUp[0:6])
    pos3.extend(PushBackwards[6:12])
    pos3.extend(PushBackwards[12:18])
    pos3.extend(LiftUp[18:24])
    pos3.extend(LiftUp[24:30])
    pos3.extend(PushBackwards[30:36])
    positionN(pos3)
    check_position_error(40, 80, pos3)

    pos4 = list()
    pos4.extend(PushBackwards[0:6])
    pos4.extend(PushBackwards[18:24])
    pos4.extend(PushBackwards[24:30])
    positionN(pos4)
    leg_case = [1,4,5]
    check_position_error_legs(20, 60, pos4, leg_case)


def TactileCheck(LiftUp):
    pos5 = list()
    pos5.extend(LiftUp[0:6])
    positionN(pos5)
    leg_case = [1]
    check_position_error_legs(20, 20, pos5, leg_case)
    checkContactWithoutControlSystem()


def ChangeVelocity(x):
    torque(0)
    scaler_acc = [20+x] * 18      #Setting Acceleration to "low"
    scaler_vel = [20+x] * 18      #Setting Velocity to "low"
    velocityAll(scaler_vel)
    accelerationAll(scaler_acc)
    torque(1)
    print("Acc is", scaler_acc[0])
    standup_pos = [2048, 2048, 1296, 2048, 2048, 1296,
                   2048, 2048, 1296, 2048, 2048, 1296,
                   2048, 2048, 1296, 2048, 2048, 1296]
    positionAll(standup_pos)
    time.sleep(0.10)
    return x


def Demo():
    stairs = True
    x = 20
    PushF, LiftF, DownF, ForwardF, LiftBW, DownBW, ForwardBW, LiftLE, DownLE, ForwardLE, LiftRI, DownRI, ForwardRI = CalculationMotions()
    while stairs is True: 
        KeyboardControll() 
        getch = _Getch()
        print ("Please enter something: ")
        choice = getch()
        if  choice == "i":
            print("Increase speed")
            x += 10
            x = ChangeVelocity(x)
        elif choice == "k":
            print("Decrease speed")
            x -=10
            x = ChangeVelocity(x)
        elif choice == "w":
            move(PushF, LiftF,DownF,ForwardF)
            print("Move Forward")
        elif choice == "a":
            print("Move Left")
            move(PushF, LiftLE, DownLE,ForwardLE)
        elif choice == "s": 
            print("Move backwards")
            move(PushF, LiftBW, DownBW, ForwardBW)
        elif choice == "d":
            print("Move right")
            move(PushF, LiftRI, DownRI, ForwardRI)
        elif choice == "t":
            print("Rotate Clockwise")
            yawRotation(10)
        elif choice == "y":
            print("Rotate CounterClockwise")
            yawRotation(-10)
        elif choice == "v":
            print("Dance")
            DanceStar()
        elif choice == "b":
            print("Tactile")
            TactileCheck(LiftF)
        elif choice == "c":
            print("CameraDemo")
            CameraDemo()
        else:
            print("")
            print("   	 Enter number from 0 to 4!")
            print("   	 You entered: %s" % choice)
            print("   	 Try again in 3 seconds.")
            time.sleep(3)


def CalculationMotions():
    Forward      =   [0, 50, 40]
    Up           =   [0, 0, 40]
    Down         =   [0, 50, 0]
    Push         =   [0, 0, 0]

    PushF        = calc_motion(Push)
    LiftF        = calc_motion(Up)
    DownF        = calc_motion(Down)
    ForwardF     = calc_motion(Forward)

    ForwardB     =   [0, -50, 40]
    UpB          =   [0, 0, 40]
    DownB        =   [0, -50, 0]

    LiftBW       = calc_motion(UpB)
    DownBW       = calc_motion(DownB)
    ForwardBW    = calc_motion(ForwardB)

    ForwardL     =   [-50, 0, 40]
    UpL          =   [0, 0, 40]
    DownL        =   [-50, 0, 0]

    LiftLE       = calc_motion(UpL)
    DownLE       = calc_motion(DownL)
    ForwardLE    = calc_motion(ForwardL)

    ForwardR     =   [50, 0, 40]
    UpR          =   [0, 0, 40]
    DownR        =   [50, 0, 0]

    LiftRI       = calc_motion(UpR)
    DownRI       = calc_motion(DownR)
    ForwardRI    = calc_motion(ForwardR)
    return PushF, LiftF, DownF, ForwardF, LiftBW, DownBW, ForwardBW, LiftLE, DownLE, ForwardLE, LiftRI, DownRI, ForwardRI
 

def KeyboardControll(): 
    
    print("	 _________________________________________________ ")
    print("	|               Keyboard Control:                   |")
    print("	|                  For Movement:                    |")
    print("	|                                                   |")
    print("	|                       w                           |")
    print("	|                   a   s   d                       |")
    print("	|                                                   |")
    print("	|               Increse/decrease speed              |")
    print("	|                                                   |")
    print("	|                       i/k                         |")
    print("	|                                                   |")
    print("	|        Rotate clockwise/counterclockwise          |")
    print("	|                                                   |")
    print("	|                       t/y                         |")
    print("	|                                                   |")
    print("	|                   Dance(v)                        |")
    print("	|    				CameraDemo(c)                   |")
    print("	|    		         Tactile(b)                     |")
    print("	|    				                                |")
    print("	|_________________________________________________|")


def parallelGaitCalc(alpha, beta, gamma, dist_x, dist_y, dist_z):
    alpha_rad = radians(alpha)
    beta_rad = radians(beta)
    gamma_rad = radians(gamma)

    current_pos = readPos()
    next_pos = K.doIkineRotationEuler(current_pos, alpha_rad, beta_rad, gamma_rad, dist_x, dist_y, dist_z)
    return next_pos

def CameraDemo():
    clear_view_stairs()
    time.sleep(1)
    stair_dimensions=getAllStairsInfo()
    print(stair_dimensions)
    Stand_up()

def DanceStar():
    
    t = 0.5
    ##Belly Dance
    A1=parallelGaitCalc(0, 5, 0, 0, 0, 0)
    A2=parallelGaitCalc(0, 10, 0, 0, 0, 0)
    A3=parallelGaitCalc(0, 10, 5, 0, 0, 0) 
    A4=parallelGaitCalc(0, 10, 10, 0, 0, 0) 
    A5=parallelGaitCalc(0, 5, 10, 0, 0, 0)  
    A6=parallelGaitCalc(0, 0, 10, 0, 0, 0)  
    A7=parallelGaitCalc(0, 0, 5, 0, 0, 0)  
    A8=parallelGaitCalc(0, 0, 0, 0, 0, 0)
    U0=parallelGaitCalc(0, 0, 0, 0, 0, 0)  

    U1=parallelGaitCalc(0, 0, 0, 0, 0, 50)  
    U2=parallelGaitCalc(0, 0, 0, 0, 0, 100)  

    L1=parallelGaitCalc(0, 0, 0, -30, 0, 100)
    L1=parallelGaitCalc(0, 0, 0, -60, 0, 100)
    L2=parallelGaitCalc(0, 0, 0, -60, -30, 100)
    L3=parallelGaitCalc(0, 0, 0, -60, -60, 100)
    L4=parallelGaitCalc(0, 0, 0, -30, -60, 100)
    L5=parallelGaitCalc(0, 0, 0, 0, -60, 100)
    L6=parallelGaitCalc(0, 0, 0, 0, -30, 100)


    R1= parallelGaitCalc(-15, 0, 0, 0, 0, 0)
    R2= parallelGaitCalc(15, 0, 0, 0, 0, 0)
    R3= parallelGaitCalc(0, 0, 0, 0, 0, 100)
    R4= parallelGaitCalc(20, 0, 0, 0, 0, 0)



    positionAll(A1)
    time.sleep(t)
    positionAll(A2)
    time.sleep(t)
    positionAll(A3)
    time.sleep(t)
    positionAll(A4)
    time.sleep(t)
    positionAll(A5)
    time.sleep(t)
    positionAll(A6)
    time.sleep(t)
    positionAll(A7)
    time.sleep(t)
    positionAll(A8)
    time.sleep(t)
    positionAll(U1)
    time.sleep(2*t)
    positionAll(U2)
    time.sleep(2*t)
    positionAll(L1)
    time.sleep(2*t)
    positionAll(L2)
    time.sleep(2*t)
    positionAll(L3)
    time.sleep(2*t)
    positionAll(L4)
    time.sleep(2*t)
    positionAll(L5)
    time.sleep(2*t)
    positionAll(L6)
    time.sleep(2*t)
    positionAll(U2)
    time.sleep(2*t)
    positionAll(U1)
    time.sleep(2*t)
    positionAll(U0)
    time.sleep(2*t)
    positionAll(R1)
    time.sleep(4*t)
    positionAll(R2)
    time.sleep(4*t)
    positionAll(R3)
    time.sleep(4*t)
    positionAll(R4)
    time.sleep(4*t)
    positionAll(U0)


Stand_up()
Demo()