#!/usr/bin/env python2
import rospy

from dns.srv import *


# Wrappers (for user convenience)

def positionN(ID_n_pos_list):
    return pos_N_request(ID_n_pos_list)


def velocityN(ID_n_vel_list):
    return vel_N_request(ID_n_vel_list)


def accelerationN(ID_n_acc_list):
    return acc_N_request(ID_n_acc_list)


def pwmN(ID_n_pwm_list):
    return pwm_N_request(ID_n_pwm_list)


def position1(ID, Pos):
    return pos_1_request([ID, Pos])


def accelerationAll(acc_list):
    return acc_all_request(acc_list)


def velocityAll(vel_list):
    return vel_all_request(vel_list)


def pwmAll(pwm_list):
    return pwm_all_request(pwm_list)


def positionAll(pos_list):
    return pos_all_request(pos_list)


def torque(bool_value):
    return tor_request(bool_value)


def reboot():
    return rst_request(1)


def readIR():
    tmp_IR = read_IR_request()
    IR_front = tmp_IR[0]
    IR_right = tmp_IR[1]
    IR_left  = tmp_IR[2]
    return IR_front, IR_right, IR_left


def readPos():
    return read_pos_all_request(1)


def readPwm():
    return read_pwn_all_request(1)


# Requests

def read_pos_all_request(command):
    rospy.wait_for_service('read_all_pos')
    try:
        read_all_pos = rospy.ServiceProxy('read_all_pos', pos_key)
        response = read_all_pos(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def read_pwn_all_request(command):
    rospy.wait_for_service('read_all_pwm')
    try:
        read_all_pwm = rospy.ServiceProxy('read_all_pwm', pos_key)
        response = read_all_pwm(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def read_IR_request():
    rospy.wait_for_service('read_IR')
    try:
        read_IR = rospy.ServiceProxy('read_IR', pos_key)
        response = read_IR()
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def acc_all_request(command):
    rospy.wait_for_service('write_acc_all')
    try:
        write_acc_all = rospy.ServiceProxy('write_acc_all', list_key)
        response = write_acc_all(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def pwm_all_request(command):
    rospy.wait_for_service('write_pwm_all')
    try:
        write_pwm_all = rospy.ServiceProxy('write_pwm_all', list_key)
        response = write_pwm_all(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def vel_all_request(command):
    rospy.wait_for_service('write_vel_all')
    try:
        write_vel_all = rospy.ServiceProxy('write_vel_all', list_key)
        response = write_vel_all(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def pos_1_request(command):
    rospy.wait_for_service('write_pos_1')
    try:
        write_pos_1 = rospy.ServiceProxy('write_pos_1', list_key)
        response = write_pos_1(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def pos_all_request(command):
    rospy.wait_for_service('write_pos_all')
    try:
        write_pos_all = rospy.ServiceProxy('write_pos_all', list_key)
        response = write_pos_all(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def tor_request(command):
    rospy.wait_for_service('write_tor_all')
    try:
        write_tor_all = rospy.ServiceProxy('write_tor_all', bool_key)
        response = write_tor_all(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def rst_request(command):
    rospy.wait_for_service('write_rst_all')
    try:
        write_rst_all = rospy.ServiceProxy('write_rst_all', bool_key)
        response = write_rst_all()
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def pos_N_request(command):
    rospy.wait_for_service('write_pos_N')
    try:
        write_pos_N = rospy.ServiceProxy('write_pos_N', list_key)
        response = write_pos_N(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def vel_N_request(command):
    rospy.wait_for_service('write_vel_N')
    try:
        write_vel_N = rospy.ServiceProxy('write_vel_N', list_key)
        response = write_vel_N(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def acc_N_request(command):
    rospy.wait_for_service('write_acc_N')
    try:
        write_acc_N = rospy.ServiceProxy('write_acc_N', list_key)
        response = write_acc_N(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def pwm_N_request(command):
    rospy.wait_for_service('write_pwm_N')
    try:
        write_pwm_N = rospy.ServiceProxy('write_pwm_N', list_key)
        response = write_pwm_N(command)
        return response.reply
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e
