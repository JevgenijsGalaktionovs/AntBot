"""hexapod_controller controller."""

from controller import Robot, Node, Motor, PositionSensor

TIME_STEP = 64
POSITION_SENSOR_SAMPLE_PERIOD = 100


class Controller():

    def __init__(self):

        # Initialize the Webots Supervisor.
        self.robot = Robot()
        self.timeStep = int(4 * self.robot.getBasicTimeStep())
        self.keyboard = self.robot.getKeyboard()

        # Initialize the arm motors.
        self.servos = []
        self.position_sensors = []

        self.init_servos()
        self.init_positional_sensors()

    def init_servos(self):
                         # coxa,      femur,    tibia
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

    def init_positional_sensors(self):
                                    # coxa,     femur,    tibia
        for positionalsensorName in ('c1_pos', 'f1_pos', 't1_pos',   # LEG 1
                                     'c2_pos', 'f2_pos', 't2_pos',   # LEG 2
                                     'c3_pos', 'f3_pos', 't3_pos',   # LEG 3
                                     'c4_pos', 'f4_pos', 't4_pos',   # LEG 4
                                     'c5_pos', 'f5_pos', 't5_pos',   # LEG 5
                                     'c6_pos', 'f6_pos', 't6_pos',): # LEG 6
            positional_sensor = self.robot.getPositionSensor(positionalsensorName)
            positional_sensor.enable(POSITION_SENSOR_SAMPLE_PERIOD)
            self.position_sensors.append(positional_sensor)
            
    def run(self):
        positions = [1.5, 1.5, 2]
    
        while self.robot.step(self.timeStep) != 1:
            for servos, position in zip(self.servos, positions):
                servos.setPosition(position)
            
if __name__ == "__main__":
    controller = Controller()
    controller.run()
    print(controller)



