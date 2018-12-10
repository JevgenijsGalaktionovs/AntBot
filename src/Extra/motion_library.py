#!/usr/bin/env python
import os
from dynamixel_library import *


#Function to hold program and wait for any key input in the terminal
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
#----------------------------------------------------------------------

def isclose(a, b, rel_tol, abs_tol): # Comparing two numbers with tolerances.
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def ReachPosition(servo_id,PWM_value): # Work-in-progress function. Put servo into desired position using pwm.
    desired_pos = float(raw_input("Desired position:"))
    pos_rads = ReadPosition(servo_id)
    WritePWM(servo_id,PWM_value)
    while (isclose(desired_pos,pos_rads,0.05,0) != True):
        pos_rads = ReadPosition(servo_id)
        # print "Current position: " + str(pos_rads)
        # print "Goal    position: " + str(desired_pos)
        # Radvel        = ((ReadVelocity(16)*0.229*(2.0*math.pi))/60.0)
        # print "Velocity: %f" % Radvel
        if isclose(desired_pos,pos_rads,0.05,0): #function arguments: number1, number2, relative tolerance, absolute tolerance)
            WritePWM(servo_id,0)
            print "Position reached %f" % pos_rads
            break
