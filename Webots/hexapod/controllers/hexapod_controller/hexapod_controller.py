"""hexapod_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
TIME_STEP = 64
robot = Robot()

servos = []
servosNames = ['coxa1', 'femur1', 'tibia1',
               'coxa2', 'femur2', 'tibia2',
               'coxa3', 'femur3', 'tibia3',
               'coxa4', 'femur4', 'tibia4',
               'coxa5', 'femur5', 'tibia5',
               'coxa6', 'femur6', 'tibia6',]
for i in range(18):
    servos.append(robot.getMotor(servosNames[i]))
    servos[i].setPosition(float('inf'))
    servos[i].setVelocity(0.0)

# get the time step of the current world.
#timestep = int(robot.getBasicTimeStep())

MAX_SPEED = 6.28

servos[2].setVelocity(0.1 * MAX_SPEED)
servos[5].setVelocity(0.1 * MAX_SPEED)
servos[8].setVelocity(0.1 * MAX_SPEED)
servos[11].setVelocity(0.1 * MAX_SPEED)
servos[14].setVelocity(0.1 * MAX_SPEED)
servos[17].setVelocity(0.1 * MAX_SPEED)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
