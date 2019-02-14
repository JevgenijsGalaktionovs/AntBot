
File explanation:



  /src folder:

  main.py              : Checks the status (ping) of Dynamixel servos and initializes the class from Antbot.py (MAIN LOOP)
  control_interface.py : A Python Class with joystick button mapping. Runs the "Controller" node.
  dynamixel_library.py : Library of functions to communicate and manage Dynamixel servos.
  kinematics.py        : Library of functions to calculate inverse and forward kinematics.
  ------------------------------------------------------------------------------------------------------------------------------------

  antbot.bash          : Sourcing setup files and linking the device (slave) to the master. Has to be run on RPI or included into bash.rc file.
  Currently set up for Lars PC, can't be used.

  Kinematics           : Not updated on new robot mechanical design
  Joystick             : Using stupid sleeps. Might be a problem for the system smooth performance?
