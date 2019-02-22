#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dynamixel_sdk import *                     # Uses Dynamixel SDK library

# Control table address. Same for MX-28(2.0), MX-64(2.0), MX-106(2.0)
ADDR_MX_ID                 = 7
ADDR_MX_BAUDRATE           = 8
ADDR_MX_PWM_LIMIT          = 36
ADDR_MX_CURRENT_LIMIT      = 38
ADDR_MX_VELOCITY_LIMIT     = 44
ADDR_MX_TORQUE_ENABLE      = 64                 # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 116
ADDR_MX_PRESENT_POSITION   = 132
ADDR_MX_GOAL_PWM           = 100
ADDR_MX_PRESENT_PWM        = 124
ADDR_MX_PRESENT_LOAD       = 126
ADDR_MX_PRESENT_VELOCITY   = 128
ADDR_MX_OPERATION_MODE     = 11
ADDR_MX_SECONDARY_ID       = 12



LEN_4BYTES                 = 4
LEN_2BYTES                 = 2
LEN_1BYTE                  = 1


PROTOCOL_VERSION           = 2.0               # See which protocol version is used in the Dynamixel

SECONDARY_ID               = 20
BROADCAST_ID               = 0xFE              # ID 254, reserved for broadcast ("send to all available ids")
BAUDRATE                   = 1000000           # Dynamixel default baudrate : 57600
DEVICENAME                 = '/dev/ttyUSB0'    # Check which port is being used on your controller

TORQUE_ENABLE              = 1                 # Value for enabling the torque
TORQUE_DISABLE             = 0                 # Value for disabling the torque

MAX_ONE_ROTATION_UNIT      = 4095
MAX_UINT16_VALUE           = 65536             # 65535+1 . That "1" is needed to correctly represent negative values.
MAX_UINT32_VALUE           = 4294967296        # 4294967295+1


portHandler   = PortHandler   (DEVICENAME)       # Get methods and members of PortHandlerLinux or PortHandlerWindows
packetHandler = PacketHandler (PROTOCOL_VERSION) # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
gbr           = GroupBulkRead (portHandler, packetHandler)
gbw           = GroupBulkWrite(portHandler, packetHandler)

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
            sys.stdin.flush()
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def CheckOpenPort(portHandler):
    # Open port
    if portHandler.openPort():
        print ("")
        print("Succeeded to open the port %s" % DEVICENAME)
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()
def SetPortBaudrate(BAUDRATE):
    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        pass
        print("Succeeded to set the baudrate %d" %BAUDRATE)
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()

CheckOpenPort(portHandler)
SetPortBaudrate(BAUDRATE)

def CheckStatus():
    count_dynamixels = 0
    id_dynamixels = list()
    dxl_data_list, dxl_comm_result = packetHandler.broadcastPing(portHandler)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    print("Detected Dynamixels :")
    for dxl_id in dxl_data_list:
        count_dynamixels +=1
        id_dynamixels.append(dxl_id)
    print(id_dynamixels)
    if count_dynamixels != 18:
        print "Not all servos are connected. Found %d out of 18 servos." %count_dynamixels
        print "Press any key to restart"
        getch()
        timeout = 6# one more
        for x in range (0,5):
            timeout -=1
            print "Restart in %d seconds..." %timeout
            time.sleep(1)
        return 0
    else:
        return 1
def ConnectToDynamixels():
    while 1:
        print "Attempting to connect"
        status = CheckStatus()
        if status:
            break
    print "Connection to Dynamixels has been established."




def ConvertTo4Bytes(data):
    data_write = [DXL_LOBYTE(DXL_LOWORD(data)), DXL_HIBYTE(DXL_LOWORD(data)),
                  DXL_LOBYTE(DXL_HIWORD(data)), DXL_HIBYTE(DXL_HIWORD(data))]
    return data_write # Allocate value into 4 byte array (Example: Goal Position must be 4 bytes long)
def ConvertTo2Bytes(data):
    data_2bytes = [DXL_LOBYTE(data), DXL_HIBYTE(data)]
    return data_2bytes # Allocate value into 2 byte array (Example: Goal PWM must be 4 bytes long)
def BulkWrite(ADDR_MX, DATA_LEN, list_18_values): # Takes ~0.003sec to read

    value_byte_array = list()

    if   DATA_LEN == 1:
        for x in range(0,len(list_18_values)):
            value_byte_array.append([list_18_values[x]])
    elif DATA_LEN == 2:
        for x in range(0,len(list_18_values)):
            value_byte_array.append(ConvertTo2Bytes(list_18_values[x]))
    elif DATA_LEN == 4:
        for x in range(0,len(list_18_values)):
            value_byte_array.append(ConvertTo4Bytes(list_18_values[x]))

    for ID in range (1,19):
        dxl_addparam_result = gbw.addParam(ID, ADDR_MX, DATA_LEN, value_byte_array[ID-1])
        if dxl_addparam_result != True:
            print("[ID:%03d] groupBulkRead addparam failed" % ID)
            quit()

    dxl_comm_result = gbw.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    gbw.clearParam()
def BulkRead(ADDR_MX,DATA_LEN): # Takes ~0.023sec to read

    data = list()
    for ID in range (1,19):
        dxl_addparam_result = gbr.addParam(ID, ADDR_MX, DATA_LEN)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupBulkRead addparam failed" % ID)
            quit()

    dxl_comm_result = gbr.txRxPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    for ID in range (1,19):
        dxl_getdata_result = gbr.isAvailable(ID, ADDR_MX, DATA_LEN)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % ID)
            quit()
        data.append(gbr.getData(ID, ADDR_MX, DATA_LEN))

    gbr.clearParam()
    return data


######################################
#######  All servo commands  #########
######################################
def EnableTorqueAllServos():
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, BROADCAST_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("All Torques enabled")
def DisableTorqueAllServos():
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, BROADCAST_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("All Torques disabled")
def PingAllServos():
    dxl_data_list, dxl_comm_result = packetHandler.broadcastPing(portHandler)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
def RebootAllServos():
    dxl_comm_result, dxl_error = packetHandler.reboot(portHandler,BROADCAST_ID)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("All Servos rebooted")
def ReadAllPositions():
    return BulkRead(ADDR_MX_PRESENT_POSITION, LEN_4BYTES)
def ReadAllPWM():
    all_pwm = BulkRead(ADDR_MX_PRESENT_PWM, LEN_2BYTES)
    for x in range(0,len(all_pwm)):
        if all_pwm[x] > (MAX_UINT16_VALUE*0.8): # dirty hack. we read 2 bytes = uint32 ;It has values from 0 to 65535
            all_pwm[x] -= MAX_UINT16_VALUE
    return all_pwm
def ReadAllPWMlimits():
    print BulkRead(ADDR_MX_PWM_LIMIT, LEN_2BYTES)
def ReadAllVelocitylimits():
    print BulkRead(ADDR_MX_VELOCITY_LIMIT, LEN_4BYTES)
def ReadAllCurrents():
        all_currents = BulkRead(ADDR_MX_PRESENT_LOAD, LEN_2BYTES)
        for x in range(0,len(all_currents)):
            if all_currents[x] > (MAX_UINT16_VALUE*0.8): # dirty hack. we read 2 bytes = uint32 ;It has values from 0 to 65535
                all_currents[x] -= MAX_UINT16_VALUE
        print all_currents


def ReadAllVelocity():
    all_velocities =  BulkRead(ADDR_MX_PRESENT_VELOCITY, LEN_4BYTES)
    for x in range(0,len(all_velocities)):
        if all_velocities[x] > (MAX_UINT32_VALUE*0.8): # dirty hack. we read 2 bytes = uint32 ;It has values from 0 to 65535
            all_velocities[x] -= MAX_UINT32_VALUE
    print all_velocities
def WriteAllPWM(PWM18VALUES_LIST):
    BulkWrite(ADDR_MX_GOAL_PWM, LEN_2BYTES, PWM18VALUES_LIST)
def ReadAllOperationModes():
    return BulkRead(ADDR_MX_OPERATION_MODE, LEN_1BYTE)
def WriteAllOperationModes():
    print "Please choose the mode (all servos at once): "
    print "Type 3 for Position Contro Mode"
    print "Type 16 for PWM Control Mode"
    servo_mode = int(raw_input())
    options = [3,16]
    if servo_mode not in options:
        print "Wrong number, quitting..."
        return
    mode_list = [servo_mode]*18
    BulkWrite(ADDR_MX_OPERATION_MODE, LEN_1BYTE,mode_list)
    print ReadAllOperationModes()
def WriteAllPositions(POS18VALUES_LIST):
    BulkWrite(ADDR_MX_GOAL_POSITION, LEN_4BYTES, POS18VALUES_LIST)


######################################
#######  Commands for 1 servo  #######
######################################
def Read1PWM(servo_id):
    dxl_present_pwm, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, servo_id, ADDR_MX_PRESENT_PWM)
    if dxl_present_pwm > (MAX_UINT16_VALUE*0.8): # dirty hack. we read 2 bytes = uint32 ;It has values from 0 to 65535
        dxl_present_pwm -= MAX_UINT16_VALUE
        return dxl_present_pwm
    else:
        return dxl_present_pwm
def Read1Load(servo_id):
    dxl_present_load, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, servo_id, ADDR_MX_PRESENT_LOAD)
    if dxl_present_load > (MAX_UINT16_VALUE*0.8): # dirty hack. we read 2 bytes = uint32 ;It has values from 0 to 65535
        dxl_present_load -= MAX_UINT16_VALUE
        return dxl_present_load
    else:
        return dxl_present_load
def Read1Position(servo_id):
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, servo_id, ADDR_MX_PRESENT_POSITION)
    if abs(dxl_present_position) > MAX_ONE_ROTATION_UNIT:
        new_present_position = dxl_present_position % MAX_ONE_ROTATION_UNIT
        return new_present_position
    else:
        return dxl_present_position
def Read1Velocity(servo_id):
    dxl_present_velocity, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, servo_id, ADDR_MX_PRESENT_VELOCITY)
    if dxl_present_velocity > (MAX_UINT32_VALUE*0.8):  # dirty hack. we read 4 bytes = uint32 ;It has values from 0 to 4294967295
        dxl_present_velocity -= MAX_UINT32_VALUE
        return dxl_present_velocity
    else:
        return dxl_present_velocity
def Change1ID():
    old_id = int(raw_input("Which servo ID? (old): "))
    new_id = int(raw_input("Change to (new)      : "))
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, old_id, ADDR_MX_ID, new_id) # Values from -885 to +885
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    print Read1ID(new_id)
def Read1ID(servo_id):
    dxl_id, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, servo_id, ADDR_MX_ID)
    return dxl_id
def Write1PWM(servo_id,pwm_value):
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, servo_id, ADDR_MX_GOAL_PWM, pwm_value) # Values from -885 to +885
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
def Write1Pos(servo_id,val_pos):
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, servo_id, ADDR_MX_GOAL_POSITION,val_pos) # 16 - PWM Control Mode
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
def Read1LimitPWM(servo_id):
    dxl_limit_pwm, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, servo_id, ADDR_MX_PWM_LIMIT)
    print dxl_limit_pwm
def Read1LimitCurrent(servo_id):
    dxl_limit_current, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, servo_id, ADDR_MX_CURRENT_LIMIT)
    print dxl_limit_current
def Read1OperatingMode(servo_id):
    dxl_operation_mode, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, servo_id, ADDR_MX_OPERATION_MODE)
    print dxl_operation_mode
def Change1OperationMode(servo_id):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, servo_id, ADDR_MX_OPERATION_MODE, 3) # 16 - PWM Control Mode
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
def Set1SecondaryID(servo_id):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, servo_id, ADDR_MX_SECONDARY_ID, SECONDARY_ID) # 16 - PWM Control Mode
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
def Read1SecondaryID(servo_id):
    dxl_secondary_id, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, servo_id, ADDR_MX_SECONDARY_ID)
    print dxl_secondary_id
def ChangeBaudrate(servo_id):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, servo_id, ADDR_MX_BAUDRATE, 3) # 16 - PWM Control Mode
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
def read1byte(servo_id,addr):
        data, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, servo_id, addr)
        print data
def read4byte(servo_id,addr):
        data, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, servo_id, addr)
        print data
def write4byte(servo_id,addr,value):
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, servo_id, addr,value) # 16 - PWM Control Mode
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

def isclose(a, b, rel_tol, abs_tol): # Comparing two numbers with tolerances.
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def WritePWMLimit(servo_id, pwm_limit):
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, servo_id, ADDR_MX_PWM_LIMIT, pwm_limit) # Values from -885 to +885
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

def Write1VelocitLimit(servo_id,velocity_limt):
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, servo_id, ADDR_MX_VELOCITY_LIMIT,velocity_limt) # 16 - PWM Control Mode
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
