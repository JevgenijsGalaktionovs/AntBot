"""hexapod_controller controller."""

from controller import Robot, Node, Motor, PositionSensor
from locomotion import *
from kinematics import Kinematics

TIME_STEP = 64
POSITION_SENSOR_SAMPLE_PERIOD = 100


class Controller():

    def __init__(self):

        # Initialise the Webots Supervisor.
        self.robot = Robot()
        self.timeStep = int(4 * self.robot.getBasicTimeStep())
        self.keyboard = self.robot.getKeyboard()

        # Initialise the leg servos.
        self.servos = []
        self.position_sensors = []
        # Initialise the servo position sensors
        self.init_servos()
        self.init_position_sensors()

    def init_servos(self):
                          # coxa,     femur,    tibia
        for servosName in ('c1_ser', 'f1_ser', 't1_ser',   # LEG 1
                           'c2_ser', 'f2_ser', 't2_ser',   # LEG 2
                           'c3_ser', 'f3_ser', 't3_ser',   # LEG 3
                           'c4_ser', 'f4_ser', 't4_ser',   # LEG 4
                           'c5_ser', 'f5_ser', 't5_ser',   # LEG 5
                           'c6_ser', 'f6_ser', 't6_ser',): # LEG 6
            servos = self.robot.getMotor(servosName)
            # servos.setPosition(float('inf'))
            # servos.setVelocity(0)
            self.servos.append(servos)

    def init_position_sensors(self):
                                    # coxa,     femur,    tibia
        for positionsensorName in ('c1_pos', 'f1_pos', 't1_pos',   # LEG 1
                                   'c2_pos', 'f2_pos', 't2_pos',   # LEG 2
                                   'c3_pos', 'f3_pos', 't3_pos',   # LEG 3
                                   'c4_pos', 'f4_pos', 't4_pos',   # LEG 4
                                   'c5_pos', 'f5_pos', 't5_pos',   # LEG 5
                                   'c6_pos', 'f6_pos', 't6_pos',): # LEG 6
            position_sensor = self.robot.getPositionSensor(positionsensorName)
            position_sensor.enable(POSITION_SENSOR_SAMPLE_PERIOD)
            self.position_sensors.append(position_sensor)
        for i in range(len(positionsensorName)):
            a = self.position_sensors[i].getValue()
        return  a
            
    def run(self):
        positions = [1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2]
    
        while self.robot.step(self.timeStep) != 1:
            for servos, position in zip(self.servos, positions):
                servos.setPosition(position)
            break
                
#    def read(self):
#        while self.robot.step(self.timeStep) != 1:
#            for position_sensor in zip(self.position_sensors):
#                position_sensor = self.robot.getPositionSensor(positionsensorName)
#        return  position_sensor
            
if __name__ == "__main__":
    controller = Controller()
    controller.run()
    AE = controller.init_position_sensors()
    print(AE)
    
    
    # tripodGait(0, 20, 10, 1)
    print(controller)



