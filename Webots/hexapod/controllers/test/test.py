from controller import Robot


robot = Robot()
timeStep = int(4 * robot.getBasicTimeStep())
keyboard = robot.getKeyboard()

# Define lists for servo and sensor values
servos = []
ps = []
    
    
# Initialise servos and sensors
             # coxa,     femur,    tibia
servosName = ['c1_ser', 'f1_ser', 't1_ser',   # LEG 1
              'c2_ser', 'f2_ser', 't2_ser',   # LEG 2
              'c3_ser', 'f3_ser', 't3_ser',   # LEG 3
              'c4_ser', 'f4_ser', 't4_ser',   # LEG 4
              'c5_ser', 'f5_ser', 't5_ser',   # LEG 5
              'c6_ser', 'f6_ser', 't6_ser',]  # LEG 6
for name in servosName:
    servos.append(robot.getMotor(name))
   
            
         # coxa,     femur,    tibia
psName = ['c1_pos', 'f1_pos', 't1_pos',   # LEG 1
          'c2_pos', 'f2_pos', 't2_pos',   # LEG 2
          'c3_pos', 'f3_pos', 't3_pos',   # LEG 3
          'c4_pos', 'f4_pos', 't4_pos',   # LEG 4
          'c5_pos', 'f5_pos', 't5_pos',   # LEG 5
          'c6_pos', 'f6_pos', 't6_pos',]  # LEG 6
for i in range(18):
    ps.append(robot.getPositionSensor(psName[i]))
    ps[i].enable(timeStep)

  
# Read positions for all servos before motion
#psValues = []
#value = []
#while robot.step(timeStep) != -1:
#    for i in range(18):
#        value = ps[i].getValue()
#        psValues.append(value)
#    break
#print(psValues)


# Set positions for each servo to stand
positions = [0.1, 1.0, 2, 0.1, 1.0, 2, 0.1, 1.0, 2, 0.1, 1.0, 2, 0.1, 1.0, 2, 0.1, 1.0, 2]
while robot.step(timeStep) != 1:
    for servo, position in zip(servos, positions):
        servo.setPosition(position)
    break

            
# Read positions for all servos after motion
psValues = []
value = []
while robot.step(timeStep) != 1:
    for i in range(18):
        value = ps[i].getValue()
        psValues.append(value)
    break
print(psValues)