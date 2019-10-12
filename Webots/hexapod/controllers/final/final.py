import math
from controller import Supervisor, Node, Motor, PositionSensor

POSITION_SENSOR_SAMPLE_PERIOD = 100

class Controller():

    def __init__(self):

        # Initialize the Webots Supervisor.
        self.supervisor = Supervisor()
        self.timeStep = int(4 * self.supervisor.getBasicTimeStep())
        self.keyboard = self.supervisor.getKeyboard()

        # Initialize the arm motors.
        self.motors = []
        self.position_sensors = []

        self.init_motors()
        self.init_positional_sensors()

    def init_motors(self):
        for motorName in ('c1_ser', 'f1_ser', 't1_ser',   # LEG 1
                          'c2_ser', 'f2_ser', 't2_ser',   # LEG 2
                          'c3_ser', 'f3_ser', 't3_ser',   # LEG 3
                          'c4_ser', 'f4_ser', 't4_ser',   # LEG 4
                          'c5_ser', 'f5_ser', 't5_ser',   # LEG 5
                          'c6_ser', 'f6_ser', 't6_ser',): # LEG 6
            motor = self.supervisor.getMotor(motorName)
            # motor.setPosition(float('inf'))
            # motor.setVelocity(0)
            self.motors.append(motor)

    def init_positional_sensors(self):
        for positional_sensor_name in (
                'c1_pos', 'f1_pos', 't1_pos',   # LEG 1
                'c2_pos', 'f2_pos', 't2_pos',   # LEG 2
                'c3_pos', 'f3_pos', 't3_pos',   # LEG 3
                'c4_pos', 'f4_pos', 't4_pos',   # LEG 4
                'c5_pos', 'f5_pos', 't5_pos',   # LEG 5
                'c6_pos', 'f6_pos', 't6_pos',): # LEG 6
            positional_sensor = self.supervisor.getPositionSensor(positional_sensor_name)
            positional_sensor.enable(POSITION_SENSOR_SAMPLE_PERIOD)
            self.position_sensors.append(positional_sensor)

    def run(self):
        value = []
        psValue = []

        while self.supervisor.step(self.timeStep) != 1:
            for motor, position in zip(self.motors, positions):
                motor.setPosition(position)
            break
                
    def read(self):
        value = []
        psValue = []

        while self.supervisor.step(self.timeStep) != 1:    
            for i in range(18):
                value = self.position_sensors[i].getValue()
                psValue.append(value)
            print(psValue)
            psValue = []


if __name__ == "__main__":
    controller = Controller()
    positions = [1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2, 1.0, 1.0, 2]
    controller.run()
    controller.read()
    print(controller)
