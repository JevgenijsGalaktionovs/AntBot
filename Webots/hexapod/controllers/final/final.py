import math
from controller import Supervisor, Node, Motor, PositionSensor
from locomotion import *
from kinematics import Kinematics

POSITION_SENSOR_SAMPLE_PERIOD = 100

class Controller():

    jointNames = [
       # coxa,  femur, tibia
        'c1',  'f1',  't1',  # LEG 1
        'c2',  'f2',  't2',  # LEG 2
        'c3',  'f3',  't3',  # LEG 3
        'c4',  'f4',  't4',  # LEG 4
        'c5',  'f5',  't5',  # LEG 5
        'c6',  'f6',  't6']  # LEG 6

    def __init__(self):
        # Initialize the Webots Supervisor.
        self.supervisor = Supervisor()
        self.timeStep = int(4 * self.supervisor.getBasicTimeStep())
        self.keyboard = self.supervisor.getKeyboard()

        # Define list for motors and position sensors
        self.motors = []
        self.position_sensors = []
        # Initialise the motors and position sensors (could be moved into __init__ into a single for-loop)
        self.init_motors()
        self.init_positional_sensors()

    def init_motors(self):
        for name in Controller.jointNames:
            motor = self.supervisor.getMotor(name + '_motor')
            # motor.setPosition(float('inf'))
            # motor.setVelocity(0)
            self.motors.append(motor)

    def init_positional_sensors(self):
        for name in Controller.jointNames:
            positional_sensor = self.supervisor.getPositionSensor(name + '_position_sensor')
            positional_sensor.enable(POSITION_SENSOR_SAMPLE_PERIOD)
            self.position_sensors.append(positional_sensor)

    def positionN(self):
        while self.supervisor.step(self.timeStep) != 1:
            for motor, position in zip(self.motors, positions):
                motor.setPosition(position)
            break

    def readPos(self):
        value = []
        all_positions = []

        while self.supervisor.step(self.timeStep) != 1:
            for i in range(len(self.jointNames)):
                value = self.position_sensors[i].getValue()
                all_positions.append(value)
            print(psValue)
            if psValue == positions:
                all_positions = []
                return
            all_positions = []


if __name__ == "__main__":
    controller = Controller()
    #positions = [0.1, 1.0, 2, 0.1, 1.0, 2, 0.1, 1.0, 2, 0.1, 1.0, 2, 0.1, 1.0, 2, 0.1, 1.0, 2]
    #controller.positionN()
    #controller.readPos()
    #positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #controller.positionN()
    #controller.readPos()

    tripodGait(0, 20, 10, 1)
    print(controller)
