#!/usr/bin/env python2
import serial
import sys
import glob
import rospy
import json

from antbot.srv import bool_key, bool_keyResponse, list_key, \
    list_keyResponse, pos_key,  pos_keyResponse


class ArduinoCommunication:
    '''Serial interface that communicates with Arduino via JSON strings over serial port'''
    baudrate = 1000000
    ser = 0  # Placeholder for Serial Port object.

    def __init__(self):
        self.ser = self.openSerialPort(self.baudrate)
        if self.ser.isOpen():
            self.ser.flushInput()
            self.ser.flushOutput()
        else:
            print "Cannot open Serial Port "
        self.serialNode()

    def serialNode(self):
        rospy.init_node('ArduinoCommunication')

        rospy.Service('write_tor_all', bool_key, self.tor_srv)
        rospy.Service('write_rst_all', bool_key, self.rst_srv)
        rospy.Service('write_pos_1',   list_key, self.pos_1_srv)
        rospy.Service('write_pos_all', list_key, self.pos_all_srv)
        rospy.Service('write_vel_all', list_key, self.vel_all_srv)
        rospy.Service('write_acc_all', list_key, self.acc_all_srv)
        rospy.Service('write_pwm_all', list_key, self.pwm_all_srv)
        rospy.Service('write_pos_N',   list_key, self.pos_N_srv)
        rospy.Service('write_vel_N',   list_key, self.vel_N_srv)
        rospy.Service('write_acc_N',   list_key, self.acc_N_srv)
        rospy.Service('write_pwm_N',   list_key, self.pwm_N_srv)
        rospy.Service('read_all_pos',  pos_key,  self.read_pos_all_srv)
        rospy.Service('read_all_pwm',  pos_key,  self.read_pwm_all_srv)
        rospy.Service('read_IR_filt',  pos_key,  self.read_IR_filt_srv)
        rospy.Service('read_FSR_filt', pos_key,  self.read_FSR_filt_srv)

        rate = rospy.Rate(100)  # 100hz
        while not rospy.is_shutdown():
            rate.sleep()

    def serialPorts(self):
        """ Function: lists serial port names
            Raise:  EnvironmentError: On unsupported or unknown platforms
            Return: A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def openSerialPort(self, baudrate):
        port = self.serialPorts()
        print "Available ports: ", port, " Connecting to: ", port[0]
        ser  = serial.Serial(port[0], baudrate)
        return ser

    def sendSerial(self, data_package):
        tmp_msg = json.dumps(data_package)
        msg = tmp_msg + '\n'
        self.ser.write(msg)

    # Services
    def tor_srv(self, req):
        data_to_send = dict(torque=req.command)
        self.sendSerial(data_to_send)
        return bool_keyResponse("Torque changed")

    def rst_srv(self, req):
        data_to_send = dict(reboot=req.command)
        self.sendSerial(data_to_send)
        return bool_keyResponse("Dynamixels Rebooted")

    def pos_1_srv(self, req):
        data_to_send = dict(pos_1=req.command)
        self.sendSerial(data_to_send)
        reply = "ID " + str(req.command[0]) + " >> Position " + str(req.command[1])
        return list_keyResponse(reply)

    def pos_all_srv(self, req):
        data_to_send = dict(pos_all=req.command)
        self.sendSerial(data_to_send)
        return list_keyResponse("All Positions changed")

    def pwm_all_srv(self, req):
        data_to_send = dict(pwm_all=req.command)
        self.sendSerial(data_to_send)
        return list_keyResponse("All PWM Limits changed")

    def acc_all_srv(self, req):
        data_to_send = dict(aprof_all=req.command)
        self.sendSerial(data_to_send)
        return list_keyResponse("All Acceleration profiles changed")

    def vel_all_srv(self, req):
        data_to_send = dict(vprof_all=req.command)
        self.sendSerial(data_to_send)
        return list_keyResponse("All Velocity profiles changed")

    def vel_N_srv(self, req):
        data_to_send = dict(vprof_n=req.command)
        self.sendSerial(data_to_send)
        return list_keyResponse("Some Velocity profiles changed")

    def pos_N_srv(self, req):
        data_to_send = dict(pos_n=req.command)
        self.sendSerial(data_to_send)
        return list_keyResponse("Some Positions changed")

    def pwm_N_srv(self, req):
        data_to_send = dict(pwm_n=req.command)
        self.sendSerial(data_to_send)
        return list_keyResponse("Some PWM Limits changed")

    def acc_N_srv(self, req):
        data_to_send = dict(aprof_n=req.command)
        self.sendSerial(data_to_send)
        return list_keyResponse("Some Acceleration profiles changed")

    def read_pos_all_srv(self, req):
        data_to_send = dict(read_pos_all=req.command)
        self.sendSerial(data_to_send)
        while True:
            # time.sleep(0.01)
            while self.ser.inWaiting() > 0:
                in_data = self.ser.readline()
                try:  # Take only non-corrupted JSON messages
                    sr_pos  = json.loads(in_data).get('sr_pos')
                    if sr_pos is not None:
                        return pos_keyResponse(sr_pos)
                except ValueError:
                    pass  # do nothing, not a valid json

    def read_pwm_all_srv(self, req):
        data_to_send = dict(read_pwm_all=req.command)
        self.sendSerial(data_to_send)
        while True:
            # time.sleep(0.01)
            while self.ser.inWaiting() > 0:
                in_data = self.ser.readline()
                try:  # Take only non-corrupted JSON messages
                    sr_pwm  = json.loads(in_data).get('sr_pwm')
                    if sr_pwm is not None:
                        return pos_keyResponse(sr_pwm)
                except ValueError:
                    pass  # do nothing, not a valid json

    def read_IR_filt_srv(self, req):
        data_to_send = dict(read_IR_filt=req.command)
        self.sendSerial(data_to_send)
        while True:
            # time.sleep(0.01)
            while self.ser.inWaiting() > 0:
                in_data = self.ser.readline()

                try:  # Take only non-corrupted JSON messages
                    IR_read  = json.loads(in_data).get('IR_dist')
                    if IR_read is not None:
                        return pos_keyResponse(IR_read)
                except ValueError:
                    pass  # do nothing, not a valid json

    def read_FSR_filt_srv(self, req):
        data_to_send = dict(read_FSR_filt=req.command)
        self.sendSerial(data_to_send)
        while True:
            # time.sleep(0.01)
            while self.ser.inWaiting() > 0:
                in_data = self.ser.readline()

                try:  # Take only non-corrupted JSON messages
                    FSR_read  = json.loads(in_data).get('FSR_pres')
                    if FSR_read is not None:
                        return pos_keyResponse(FSR_read)
                except ValueError:
                    pass  # do nothing, not a valid json


ArduinoCommunication()
