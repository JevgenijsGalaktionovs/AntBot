The contents of this folder is a 6th semester project of group 664, called AntBot.
The project is a continuously on-going project that is expected to be continued in the following years.

At the moment, the project is in the middle of a major version upgrade.
"Old version" part of the code is based on the old method (Controlling Dynamixels from Raspberry Pi via Dynamixel SDK)
"New version" part of the code is based on the new method (Controlling Dynamixels/sensors through Arduino Mega via custom driver)

The project tree is as follows:

1. Matlab
	All Matlab files used for calculation and simulation

2. Old method
	All Python files necessary to execute Stairs and Ramp algorithms, used for Specific requirement 1 and 2

3. New method
	3.1 Arduino_part
		All C++ files. External libraries are also present in the folder 	~/Arduino_part/lib
	3.2 RPI_part
		All Python files necessary to execute path-planner and serial communication with Arduino.


LATEST VERSION OF THE CODE CAN BE OBTAINED IN THE FOLLOWING GitHub REPOSITORY:
https://github.com/JevgenijsGalaktionovs/AntBot
