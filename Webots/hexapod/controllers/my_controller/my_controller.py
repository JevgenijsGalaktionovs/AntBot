"""hexapod_controller controller."""

from controller import Robot, Node, Motor, PositionSensor
from locomotion import *
from kinematics import Kinematics


TIME_STEP = 64
POSITION_SENSOR_SAMPLE_PERIOD = 100

servosName = []
servos = []
psName = []
ps = []
psValues = []
    

def init_servos():
                          # coxa,     femur,    tibia
    for servosName in ('c1_ser', 'f1_ser', 't1_ser',   # LEG 1
                       'c2_ser', 'f2_ser', 't2_ser',   # LEG 2
                       'c3_ser', 'f3_ser', 't3_ser',   # LEG 3
                       'c4_ser', 'f4_ser', 't4_ser',   # LEG 4
                       'c5_ser', 'f5_ser', 't5_ser',   # LEG 5
                       'c6_ser', 'f6_ser', 't6_ser',): # LEG 6
        servo = robot.getMotor(servosName)
        servos.append(servo)
            
            
def init_positional_sensors():
    psName = ['c1_pos', 'f1_pos', 't1_pos',   # LEG 1
              'c2_pos', 'f2_pos', 't2_pos',   # LEG 2
              'c3_pos', 'f3_pos', 't3_pos',   # LEG 3
              'c4_pos', 'f4_pos', 't4_pos',   # LEG 4
              'c5_pos', 'f5_pos', 't5_pos',   # LEG 5
              'c6_pos', 'f6_pos', 't6_pos',]  # LEG 6
    for i in range(18):
        ps.append(robot.getPositionSensor(psName[i]))
        ps[i].enable(POSITION_SENSOR_SAMPLE_PERIOD)    

    
robot = Robot()
timeStep = int(4 * robot.getBasicTimeStep())
keyboard = robot.getKeyboard()
init_servos()
init_positional_sensors()

            
def run():
    positions = [1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2]
    
    while robot.step(timeStep) != 1:
        for servo, position in zip(servos, positions):
            servo.setPosition(position)
        break
            
                
def read():
    for i in range(18):   
        psValues.append(ps[i].getValue())
    return  psValues
      
           
if __name__ == "__main__":
    
    AE = read()
    print(AE)
    run()
    AE = read()
    print(AE)
    
    
    # tripodGait(0, 20, 10, 1)
    #print(controller)



