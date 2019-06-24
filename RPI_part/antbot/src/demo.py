#!/usr/bin/env python2
import time

from locomotion import *
from kinematics import Kinematics
from service_router import position1, torque, reboot, readPos

K = Kinematics()
toggle_torque = True


def demo_wavegait():
    waveGait(0, 40, 10, 5)


def demo_ripplegait():
    rippleGait(0, 40, 10, 5)


def demo_tripodgait_fast():
    tripodGait(0, 40, 15, 5)


#  Omnidirectional translation (Left analog stick)
def demo_tripodgait_forward():
    tripodGait(0, 20, 10, 1)
    time.sleep(1)


def demo_tripodgait_backward():
    tripodGait(0, -20, 10, 1)
    time.sleep(1)


def demo_tripodgait_left():
    tripodGait(-20, 0, 10, 1)
    time.sleep(1)


def demo_tripodgait_right():
    tripodGait(20, 0, 10, 1)
    time.sleep(1)


def demo_tripodgait_forward_left():
    tripodGait(-14, 14, 10, 1)
    time.sleep(1)


def demo_tripodgait_backward_right():
    tripodGait(14, -14, 10, 1)
    time.sleep(1)


def demo_tripodgait_forward_right():
    tripodGait(14, 14, 10, 1)
    time.sleep(1)


def demo_tripodgait_backward_left():
    tripodGait(-14, -14, 10, 1)
    time.sleep(1)


#  Omnidirectional translation (Left analog stick)
def demo_bodytilt_forward():
    parallelGait(0, 0, 3, 0, 0, 0)


def demo_bodytilt_backward():
    parallelGait(0, 0, -3, 0, 0, 0)


def demo_bodytilt_left():
    parallelGait(0, 3, 0, 0, 0, 0)


def demo_bodytilt_right():
    parallelGait(0, -3, 0, 0, 0, 0)


def demo_bodytilt_forward_left():
    parallelGait(0, 2, 2, 0, 0, 0)


def demo_bodytilt_backward_right():
    parallelGait(0, -2, -2, 0, 0, 0)


def demo_bodytilt_forward_right():
    parallelGait(0, -2, 2, 0, 0, 0)


def demo_bodytilt_backward_left():
    parallelGait(0, 2, -2, 0, 0, 0)


def demo_tripodgait_omnidirection():
    print("tripod gait omnidirectional")
    print ("Move Forward")
    tripodGait(0, 20, 10, 1)
    time.sleep(1)
    print ("Move Backward")
    tripodGait(0, -20, 10, 1)
    time.sleep(1)
    print ("Move Right")
    tripodGait(20, 0, 10, 1)
    time.sleep(1)
    print ("Move Left")
    tripodGait(-20, 0, 10, 1)
    time.sleep(1)
    print ("Move Diagonally forward/right")
    tripodGait(20, 20, 10, 1)
    time.sleep(1)
    print ("Move Diagonally backward/right")
    tripodGait(20, -20, 10, 1)
    time.sleep(1)
    print ("Move Diagonally forward/left")
    tripodGait(-20, 20, 10, 1)
    time.sleep(1)
    print ("Move Diagonally backward/left")
    tripodGait(-20, -20, 10, 1)


def demo_parallel_gait():
    parallelGait(10, 0, 0, 0, 0, 50)


def demo_body_rotation_CW():
    yawRotation(30)


def demo_body_rotation_CCW():
    yawRotation(-10)


def demo_tactile_stepdown():
    pos = K.doIkine([2048, 2218, 1024,  2048, 1878, 3048] * 3, 0, 0, 100, leg=1)
    position1(2, pos[1])
    position1(3, pos[2])
    time.sleep(1)
    stepDown(1)


def demo_standup():
    standUp()


def demo_translation_up():
    translationZ(-10)


def demo_translation_down():
    translationZ(10)


def demo_quit():
    quit()


def demo_reboot():
    reboot()
    global toggle_torque
    toggle_torque = True


def demo_torque():
    global toggle_torque
    if toggle_torque is True:
        torque(1)
    else:
        torque(0)

    toggle_torque = not(toggle_torque)


def demo_menu():
    while True:
        print ""
        print "AntBot motion demonstration:"
        print " Press 1 for Stand Up (funny one)"
        print " Press 2 for Ripple Gait"
        print " Press 3 for Wave Gait"
        print " Press 4 for Fast Tripod Gait"
        print " Press 5 for Omnidirectional Tripod Gait"
        print " Press 6 for Body Rotation"
        print " Press 7 for Tactile Stepdown"
        print " Press 8 for Torque"
        print " Press 9 for Reboot"
        print  " Press 10 for QUIT"
        print ""

        options = {1: demo_standup,
                   2: demo_ripplegait,
                   3: demo_wavegait,
                   4: demo_tripodgait_fast,
                   5: demo_tripodgait_omnidirection,
                   6: demo_body_rotation_CW,
                   7: demo_tactile_stepdown,
                   8: demo_torque,
                   9: demo_reboot,
                   10: demo_quit,
                   }

        choice = int(raw_input("Choose a number: "))
        options[choice]()


def demo_robot_dance():

    t = 0.1
    d = 30
    standUp()
    time.sleep(1)
    initial_pos = readPos()
    positionAll(initial_pos)
    time.sleep(30 * t)

    ############################

    # parallelGait(-15,0,0,0,0,0)
    # time.sleep(10 * t)
    # # parallelGait(15,0,0,0,0,0)
    # # time.sleep(t)
    # positionAll(initial_pos)
    # time.sleep(10 * t)
    # parallelGait(15,0,0,0,0,0)
    # time.sleep(t)
    # # parallelGait(-15,0,0,0,0,0)
    # # time.sleep(t)
    # positionAll(initial_pos)
    # time.sleep(10 * t)
    # parallelGait(0,10,0,0,0,0)
    # time.sleep(t)
    # # parallelGait(0,-10,0,0,0,0)
    # # time.sleep(t)
    # positionAll(initial_pos)
    # time.sleep(10 * t)
    # parallelGait(0,-10,0,0,0,0)
    # time.sleep(t)
    # # parallelGait(0,10,0,0,0,0)
    # # time.sleep(t)
    # positionAll(initial_pos)
    # time.sleep(10 * t)
    # parallelGait(0,0,10,0,0,0)
    # time.sleep(10 * t)
    # # parallelGait(0,0,-10,0,0,0)
    # positionAll(initial_pos)
    # time.sleep(10 * t)
    # parallelGait(0,0,-10,0,0,0)
    # time.sleep(t)
    # parallelGait(0,0,10,0,0,0)

    ############################

    parallelGait(0, -5, 0, 0, 0, 0)  # rot(0,-y)
    time.sleep(t)
    parallelGait(0, 0, -5, 0, 0, 0)  # rot(-x,-y)

    for n in range(2):
        parallelGait(0, 5, 0, 0, 0, 0)  # rot(-x,0) & rot(-x,y)
        time.sleep(t)
    for n in range(2):
        parallelGait(0, 0, 5, 0, 0, 0)  # rot(0,y) & rot(x,y)
        time.sleep(t)
    for n in range(2):
        parallelGait(0, -5, 0, 0, 0, 0)  # rot(x,0) & rot(x,-y)
        time.sleep(t)
    for n in range(2):
        parallelGait(0, 0, -5, 0, 0, 0)  # rot(0,-y) & rot(-x,-y)
        time.sleep(t)

    positionAll(initial_pos)
    time.sleep(30 * t)
    parallelGait(0, 0, 0, 0, 0, 50)
    time.sleep(20 * t)
    pos_up = readPos()
    parallelGait(0, 0, 0, 0, 0, 50)
    time.sleep(10 * t)
    positionAll(pos_up)
    time.sleep(10 * t)
    parallelGait(0, 0, 0, d, 0, 0)
    time.sleep(5 * t)
    parallelGait(0, 0, 0, 0, d, 0)
    time.sleep(5 * t)
    for i in range(2):
        parallelGait(0, 0, 0, -d, 0, 0)
        time.sleep(5 * t)
    for i in range(2):
        parallelGait(0, 0, 0, 0, -d, 0)
        time.sleep(5 * t)
    for i in range(2):
        parallelGait(0, 0, 0, d, 0, 0)
        time.sleep(5 * t)
    for i in range(2):
        parallelGait(0, 0, 0, 0, d, 0)
        time.sleep(5 * t)
    positionAll(pos_up)
    time.sleep(10 * t)
    positionAll(initial_pos)
    time.sleep(10 * t)
    parallelGait(0, 0, 0, 0, 0, -50)
    time.sleep(20 * t)
    positionAll(initial_pos)
    time.sleep(20 * t)
    parallelGait(15, 0, 0, 0, 0, 0)
    time.sleep(10 * t)
    positionAll(initial_pos)
    time.sleep(10 * t)
    parallelGait(-15, 0, 0, 0, 0, 0)
    time.sleep(10 * t)
    positionAll(initial_pos)
    time.sleep(10 * t)
    parallelGait(20, 0, 0, 0, 0, 50)
    time.sleep(10 * t)
    positionAll(initial_pos)
    time.sleep(10 * t)
    parallelGait(0, 10, 0, 0, 50, 0)
    time.sleep(20 * t)
    parallelGait(0, -20, 0, 0, -100, 0)
    time.sleep(20 * t)
    parallelGait(0, 20, 0, 0, 0, 0)
    time.sleep(20 * t)
    parallelGait(0, -20, 0, 100, 0, 0)
    time.sleep(20 * t)
    positionAll(initial_pos)
    time.sleep(10 * t)
