from   dynamixel_library import *
import time



def stand_up():

    # First Tripod
    #Leg 1
	Write1Pos(1,2048)
	Write1Pos(2,2218)
	Write1Pos(3,1024)
	#time.sleep(1)
    #Leg 2
	Write1Pos(4,2048)
	Write1Pos(5,1878)
	Write1Pos(6,3048)
	time.sleep(0.5)

    #Leg 5
	Write1Pos(13,2048)
	Write1Pos(14,2218)
	Write1Pos(15,1024)
	#time.sleep(1)
    #Leg 6
	Write1Pos(16,2048)
	Write1Pos(17,1878)
	Write1Pos(18,3048)
	time.sleep(0.5)

    #Leg 3
	Write1Pos(7,2048)
	Write1Pos(8,2218)
	Write1Pos(9,1024)
	#time.sleep(1)

    # Leg 4
	Write1Pos(10,2048)
	Write1Pos(11,1878)
	Write1Pos(12,3048)
	time.sleep(1)

# Iteration 1 : Australopithecus
############################
def step1():
    # First Tripod
    #Leg 1
	Write1Pos(1,2145)
	Write1Pos(2,2659)
	Write1Pos(3,777)
    #Leg 4
	Write1Pos(10,1951)
	Write1Pos(11,1437)
	Write1Pos(12,3319)
    #Leg 5
	Write1Pos(13,2145)
	Write1Pos(14,2659)
	Write1Pos(15,777)

    # Second Tripod
    #Leg 2
	Write1Pos(4,2048)
	Write1Pos(5,1878)
	Write1Pos(6,3048)
    #Leg 3
	Write1Pos(7,2048)
	Write1Pos(8,2218)
	Write1Pos(9,1024)
    #Leg 6
	Write1Pos(16,2048)
	Write1Pos(17,1878)
	Write1Pos(18,3048)
def step2():
    # First Tripod
    #Leg 1
	Write1Pos(1,2237)
	Write1Pos(2,2208)
	Write1Pos(3,1069)
    #Leg 4
	Write1Pos(10,1859)
	Write1Pos(11,1888)
	Write1Pos(12,3027)
    #Leg 5
	Write1Pos(13,2237)
	Write1Pos(14,2208)
	Write1Pos(15,1069)

    # Second Tripod
    #Leg 2
	Write1Pos(4,2048)
	Write1Pos(5,1878)
	Write1Pos(6,3048)
    #Leg 3
	Write1Pos(7,2048)
	Write1Pos(8,2218)
	Write1Pos(9,1024)
    #Leg 6
	Write1Pos(16,2048)
	Write1Pos(17,1878)
	Write1Pos(18,3048)
def step3():
    # First Tripod
    #Leg 1
	Write1Pos(1,2237)
	Write1Pos(2,2208)
	Write1Pos(3,1069)
    #Leg 4
	Write1Pos(10,1859)
	Write1Pos(11,1888)
	Write1Pos(12,3027)
    #Leg 5
	Write1Pos(13,2237)
	Write1Pos(14,2208)
	Write1Pos(15,1069)

    # Second Tripod
    #Leg 2
	Write1Pos(4,1951)
	Write1Pos(5,1437)
	Write1Pos(6,3319)
    #Leg 3
	Write1Pos(7,2145)
	Write1Pos(8,2659)
	Write1Pos(9,777)
    #Leg 6
	Write1Pos(16,1951)
	Write1Pos(17,1437)
	Write1Pos(18,3319)
def step4():
    # First Tripod
    #Leg 1
	Write1Pos(1,2048)
	Write1Pos(2,2218)
	Write1Pos(3,1024)
    #Leg 4
	Write1Pos(10,2048)
	Write1Pos(11,1878)
	Write1Pos(12,3048)
    #Leg 5
	Write1Pos(13,2048)
	Write1Pos(14,2218)
	Write1Pos(15,1024)


    # Second Tripod
    #Leg 2
	Write1Pos(4,1951)
	Write1Pos(5,1437)
	Write1Pos(6,3319)
    #Leg 3
	Write1Pos(7,2145)
	Write1Pos(8,2659)
	Write1Pos(9,777)
    #Leg 6
	Write1Pos(16,1951)
	Write1Pos(17,1437)
	Write1Pos(18,3319)
def step5():
    # First Tripod
    #Leg 1
	Write1Pos(1,2048)
	Write1Pos(2,2218)
	Write1Pos(3,1024)
    #Leg 4
	Write1Pos(10,2048)
	Write1Pos(11,1878)
	Write1Pos(12,3048)
    #Leg 5
	Write1Pos(13,2048)
	Write1Pos(14,2218)
	Write1Pos(15,1024)


    # Second Tripod
    #Leg 2
	Write1Pos(4,1859)
	Write1Pos(5,1888)
	Write1Pos(6,3027)
    #Leg 3
	Write1Pos(7,2237)
	Write1Pos(8,2208)
	Write1Pos(9,1069)
    #Leg 6
	Write1Pos(16,1859)
	Write1Pos(17,1888)
	Write1Pos(18,3027)
def step6():
    # First Tripod
    #Leg 1
	Write1Pos(1,2145)
	Write1Pos(2,2659)
	Write1Pos(3,777)
    #Leg 4
	Write1Pos(10,1951)
	Write1Pos(11,1437)
	Write1Pos(12,3319)
    #Leg 5
	Write1Pos(13,2145)
	Write1Pos(14,2659)
	Write1Pos(15,777)


    # Second Tripod
    #Leg 2
	Write1Pos(4,1859)
	Write1Pos(5,1888)
	Write1Pos(6,3027)
    #Leg 3
	Write1Pos(7,2237)
	Write1Pos(8,2208)
	Write1Pos(9,1069)
    #Leg 6
	Write1Pos(16,1859)
	Write1Pos(17,1888)
	Write1Pos(18,3027)
def step7():
    # First Tripod
    #Leg 1
	Write1Pos(1,2145)
	Write1Pos(2,2659)
	Write1Pos(3,777)
    #Leg 4
	Write1Pos(10,1951)
	Write1Pos(11,1437)
	Write1Pos(12,3319)
    #Leg 5
	Write1Pos(13,2145)
	Write1Pos(14,2659)
	Write1Pos(15,777)


    # Second Tripod
    #Leg 2
	Write1Pos(4,2048)
	Write1Pos(5,1878)
	Write1Pos(6,3048)
    #Leg 3
	Write1Pos(7,2048)
	Write1Pos(8,2218)
	Write1Pos(9,1024)
    #Leg 6
	Write1Pos(16,2048)
	Write1Pos(17,1878)
	Write1Pos(18,3048)
def step8():
    # First Tripod
    #Leg 1
	Write1Pos(1,2237)
	Write1Pos(2,2208)
	Write1Pos(3,1069)
    #Leg 4
	Write1Pos(10,1859)
	Write1Pos(11,1888)
	Write1Pos(12,3027)
    #Leg 5
	Write1Pos(13,2237)
	Write1Pos(14,2208)
	Write1Pos(15,1069)


    # Second Tripod
    #Leg 2
	Write1Pos(4,2048)
	Write1Pos(5,1878)
	Write1Pos(6,3048)
    #Leg 3
	Write1Pos(7,2048)
	Write1Pos(8,2218)
	Write1Pos(9,1024)
    #Leg 6
	Write1Pos(16,2048)
	Write1Pos(17,1878)
	Write1Pos(18,3048)
def WALK1():
	stand_up()
	time.sleep(0.1)
	step1()
	time.sleep(0.1)
	step2()
	time.sleep(0.1)
	while 1:
	# for x in range (1,10):
		step3()
		time.sleep(0.1)
		step4()
		time.sleep(0.1)
		step5()
		time.sleep(0.1)
		step6()
		time.sleep(0.1)
		step7()
		time.sleep(0.1)
		step8()
		time.sleep(0.1)

def Inverse_kinemat_gait1(x,y,z):
    endtip_xyz = Forward_kinematics()
    servo_array = []
    servo_array.extend(CalculateInverseLeg1(x,y,z,endtip_xyz))
    #servo_array.extend(CalculateInverseLeg2(x,y,z,endtip_xyz))
    #servo_array.extend(CalculateInverseLeg3(x,y,z,endtip_xyz))
    servo_array.extend(CalculateInverseLeg4(x,y,z,endtip_xyz))
    servo_array.extend(CalculateInverseLeg5(x,y,z,endtip_xyz))
    #servo_array.extend(CalculateInverseLeg6(x,y,z,endtip_xyz))

    b=[float(i) for i in servo_array]
    servo1 = int(b[0])
    servo2 =int(b[1])
    servo3 = int(b[2])
    servo10 = int(b[3])
    servo11 =int(b[4])
    servo12 = int(b[5])
    servo13 = int(b[6])
    servo14 =int(b[7])
    servo15 = int(b[8])
    if servo10 > 4096:
	servo10 = servo10-4096
    print(servo10)

    Write1Pos(1,servo1)
    Write1Pos(2,servo2)
    Write1Pos(3,servo3)
    Write1Pos(10,servo10)
    Write1Pos(11,servo11)
    Write1Pos(12,servo12)
    Write1Pos(13,servo13)
    Write1Pos(14,servo14)
    Write1Pos(15,servo15)

    return servo_array #OUTPUT: 18 servo thetas to accomplish this motion (rads)
def Inverse_kinemat_gait2(x,y,z):
    endtip_xyz = Forward_kinematics()
    servo_array = []
    #servo_array.extend(CalculateInverseLeg1(x,y,z,endtip_xyz))
    servo_array.extend(CalculateInverseLeg2(x,y,z,endtip_xyz))
    servo_array.extend(CalculateInverseLeg3(x,y,z,endtip_xyz))
    #servo_array.extend(CalculateInverseLeg4(x,y,z,endtip_xyz))
    #servo_array.extend(CalculateInverseLeg5(x,y,z,endtip_xyz))
    servo_array.extend(CalculateInverseLeg6(x,y,z,endtip_xyz))
    b=[float(i) for i in servo_array]
    servo4 = int(b[0])
    servo5 =int(b[1])
    servo6 = int(b[2])
    servo7 = int(b[3])
    servo8 =int(b[4])
    servo9 = int(b[5])
    servo16 = int(b[6])
    servo17 =int(b[7])
    servo18 = int(b[8])

    Write1Pos(4,servo4)
    Write1Pos(5,servo5)
    Write1Pos(6,servo6)
    Write1Pos(7,servo7)
    Write1Pos(8,servo8)
    Write1Pos(9,servo9)
    Write1Pos(16,servo16)
    Write1Pos(17,servo17)
    Write1Pos(18,servo18)

    return servo_array #OUTPUT: 18 servo thetas to accomplish this motion (rads)
############################

# Iteration 2 : Homo habilis
############################
def WALK2():
	#WALK()
	y = int(input("How much do you want to move forward in mm pr step? "))
	z=50#hight
	x = int(input("How much do you want to move sideways in mm pr step? "))
	while(1):
		Inverse_kinemat_gait1(x/2,y/2,z)
		Inverse_kinemat_gait1(x,y,-z)
		Inverse_kinemat_gait2(x/2,y/2,z)
		Inverse_kinemat_gait2(x,y,-z)
		stand_up()
############################
