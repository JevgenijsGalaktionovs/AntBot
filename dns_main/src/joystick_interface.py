#!/usr/bin/env python2
import rospy
from sensor_msgs.msg import Joy
from service_router import torque, reboot, readPwm, pwmAll
from locomotion import parallelGait, tripodGait, waveGait, rippleGait

PS3_BUTTON_SELECT = 0
PS3_BUTTON_STICK_LEFT = 1
PS3_BUTTON_STICK_RIGHT = 2
PS3_BUTTON_START = 3
PS3_BUTTON_CROSS_UP = 4
PS3_BUTTON_CROSS_RIGHT = 5
PS3_BUTTON_CROSS_DOWN = 6
PS3_BUTTON_CROSS_LEFT = 7
PS3_BUTTON_LEFT_BUMPER = 8
PS3_BUTTON_RIGHT_BUMPER = 9
PS3_BUTTON_LEFT_TRIGGER = 10
PS3_BUTTON_RIGHT_TRIGGER = 11
PS3_BUTTON_ACTION_TRIANGLE = 12
PS3_BUTTON_ACTION_CIRCLE = 13
PS3_BUTTON_ACTION_CROSS = 14
PS3_BUTTON_ACTION_SQUARE = 15
PS3_BUTTON_PAIRING = 16

PS3_AXIS_STICK_LEFT_LEFTWARDS = 0
PS3_AXIS_STICK_LEFT_UPWARDS = 1
PS3_LEFT_BUMBER = 2
PS3_AXIS_STICK_RIGHT_LEFTWARDS = 3
PS3_AXIS_STICK_RIGHT_UPWARDS = 4
PS3_RIGHT_BUMPER = 5


class JoystickPS3:

    button_inputs = 17 * [0]
    axes_inputs = 20 * [0]
    toggle_torque = False
    curr_goal_pwm = 0
    gait_type = 1
    gait = 0

    def __init__(self):
        self.gait = tripodGait
        self.ControllerNode()

    def callback(self, msg):
        self.button_inputs = msg.buttons
        self.axes_inputs = msg.axes

    def CreateEmptyMsgJoy(self):
        msg = Joy()
        msg.axes = [0.0] * 20
        msg.buttons = [0.0] * 17
        return msg

    def ButtonMapping(self):
        b = self.button_inputs
        a = self.axes_inputs

        if b[PS3_BUTTON_SELECT]:
            if self.toggle_torque is False:
                print("Torque on")
                torque(1)
                self.pub.publish(self.CreateEmptyMsgJoy())
            else:
                print("Torque off")
                torque(0)
                self.pub.publish(self.CreateEmptyMsgJoy())
            self.toggle_torque = not(self.toggle_torque)

        elif b[PS3_BUTTON_START]:
            print("Dynamixel Reboot")
            reboot()
            self.toggle_torque = False
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_PAIRING]:
            print("Program quit()")
            quit()

        elif b[PS3_BUTTON_ACTION_SQUARE]:
            print("Empty button, nothing happens.")
            # LEFT EMPTY. PUT YOUR COMMAND HERE
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_ACTION_CROSS]:
            print("Empty button, nothing happens.")
            # LEFT EMPTY. PUT YOUR COMMAND HERE
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_ACTION_CIRCLE]:
            print("Empty button, nothing happens.")
            # LEFT EMPTY. PUT YOUR COMMAND HERE
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_ACTION_TRIANGLE]:
            if self.gait_type == 3:
                self.gait_type = 1
            else:
                self.gait_type += 1

            print("Mode switched to: ")
            if self.gait_type == 1:
                self.gait = tripodGait
                print("Tripod Gait")
            elif self.gait_type == 2:
                self.gait = rippleGait
                print("Ripple Gait")
            else:
                self.gait = waveGait
                print("Wave Gait")
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_LEFT_TRIGGER]:
            print("Empty button, nothing happens.")
            # LEFT EMPTY. PUT YOUR COMMAND HERE
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_RIGHT_TRIGGER]:
            print("Empty button, nothing happens.")
            # LEFT EMPTY. PUT YOUR COMMAND HERE
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_LEFT_BUMPER]:
            print("Left Bumper pressed.")
            self.curr_goal_pwm = readPwm()[0]

            if self.curr_goal_pwm == 885:
                self.curr_goal_pwm -= 85
                torque(0)
                pwmAll([self.curr_goal_pwm] * 18)
                torque(1)
                print("PWM set to: ", self.curr_goal_pwm)

            elif self.curr_goal_pwm >= 300:
                self.curr_goal_pwm -= 100

                if self.curr_goal_pwm > 885:
                    self.curr_goal_pwm = 885  # set to max

                torque(0)
                pwmAll([self.curr_goal_pwm] * 18)
                torque(1)
                print("PWM set to: ", self.curr_goal_pwm)
            else:
                print("PWM is already MIN value: ", self.curr_goal_pwm)
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_RIGHT_BUMPER]:
            print("Right Bumper pressed.")
            self.curr_goal_pwm = readPwm()[0]
            if self.curr_goal_pwm <= 800:
                self.curr_goal_pwm += 100
                if self.curr_goal_pwm > 885:
                    self.curr_goal_pwm = 885  # set to max
                torque(0)
                pwmAll([self.curr_goal_pwm] * 18)
                torque(1)
                print("PWM set to: ", self.curr_goal_pwm)
            else:
                print("PWM is already MAX value: ", self.curr_goal_pwm)

            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_CROSS_RIGHT]:
            print("Empty button, nothing happens.")
            # LEFT EMPTY. PUT YOUR COMMAND HERE
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_CROSS_LEFT]:
            print("Empty button, nothing happens.")
            # LEFT EMPTY. PUT YOUR COMMAND HERE
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_CROSS_UP]:
            print("Empty button, nothing happens.")
            # LEFT EMPTY. PUT YOUR COMMAND HERE
            self.pub.publish(self.CreateEmptyMsgJoy())

        elif b[PS3_BUTTON_CROSS_DOWN]:
            print("Empty button, nothing happens.")
            # LEFT EMPTY. PUT YOUR COMMAND HERE
            self.pub.publish(self.CreateEmptyMsgJoy())

        #  Left Stick
        elif a[PS3_AXIS_STICK_LEFT_LEFTWARDS] or a[PS3_AXIS_STICK_LEFT_UPWARDS]:
            # Left
            if a[PS3_AXIS_STICK_LEFT_LEFTWARDS] > 0.2 and a[PS3_AXIS_STICK_LEFT_UPWARDS] < 0.38 and a[PS3_AXIS_STICK_LEFT_UPWARDS] > -0.38:
                print("Left motion")
                self.gait(-20, 0, 10, 1)
                self.pub.publish(self.CreateEmptyMsgJoy())

            # Right
            if a[PS3_AXIS_STICK_LEFT_LEFTWARDS] < -0.2 and a[PS3_AXIS_STICK_LEFT_UPWARDS] < 0.38 and a[PS3_AXIS_STICK_LEFT_UPWARDS] > -0.38:
                print("Right motion")
                self.gait(20, 0, 10, 1)
                self.pub.publish(self.CreateEmptyMsgJoy())

            # Up
            if a[PS3_AXIS_STICK_LEFT_UPWARDS] > 0.2 and a[PS3_AXIS_STICK_LEFT_LEFTWARDS] < 0.38 and a[PS3_AXIS_STICK_LEFT_LEFTWARDS] > -0.38:
                print("Forward motion")
                self.gait(0, 20, 10, 1)
                self.pub.publish(self.CreateEmptyMsgJoy())

            # Down
            if a[PS3_AXIS_STICK_LEFT_UPWARDS] < -0.2 and a[PS3_AXIS_STICK_LEFT_LEFTWARDS] < 0.38 and a[PS3_AXIS_STICK_LEFT_LEFTWARDS] > -0.38:
                print("Backward motion")
                self.gait(0, -20, 10, 1)
                self.pub.publish(self.CreateEmptyMsgJoy())

            # Top Left
            if a[PS3_AXIS_STICK_LEFT_LEFTWARDS] > 0.38 and a[PS3_AXIS_STICK_LEFT_UPWARDS] > 0.38:
                print("Forward-Left motion")
                self.gait(-14, 14, 10, 1)
                self.pub.publish(self.CreateEmptyMsgJoy())

            # Top Right
            if a[PS3_AXIS_STICK_LEFT_LEFTWARDS] < -0.38 and a[PS3_AXIS_STICK_LEFT_UPWARDS] > 0.38:
                print("Forward-Right motion")
                self.gait(14, 14, 10, 1)
                self.pub.publish(self.CreateEmptyMsgJoy())

            # Bottom Left
            if a[PS3_AXIS_STICK_LEFT_LEFTWARDS] > 0.38 and a[PS3_AXIS_STICK_LEFT_UPWARDS] < -0.38:
                print("Backward-Left motion")
                self.gait(-14, -14, 10, 1)
                self.pub.publish(self.CreateEmptyMsgJoy())
            # Bottom Right
            if a[PS3_AXIS_STICK_LEFT_LEFTWARDS] < -0.38 and a[PS3_AXIS_STICK_LEFT_UPWARDS] < -0.38:
                print("Backward-Right motion")
                self.gait(14, -14, 10, 1)
                self.pub.publish(self.CreateEmptyMsgJoy())

        # Right Stick
        elif a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] or a[PS3_AXIS_STICK_RIGHT_UPWARDS]:
            # Left
            if a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] > 0.2 and a[PS3_AXIS_STICK_RIGHT_UPWARDS] < 0.38 and a[PS3_AXIS_STICK_RIGHT_UPWARDS] > -0.38:
                print("Left tilt")
                parallelGait(0, 3, 0, 0, 0, 0)
                self.pub.publish(self.CreateEmptyMsgJoy())
            # Right
            if a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] < -0.2 and a[PS3_AXIS_STICK_RIGHT_UPWARDS] < 0.38 and a[PS3_AXIS_STICK_RIGHT_UPWARDS] > -0.38:
                print("Right tilt")
                parallelGait(0, -3, 0, 0, 0, 0)
                self.pub.publish(self.CreateEmptyMsgJoy())
            # Up
            if a[PS3_AXIS_STICK_RIGHT_UPWARDS] > 0.2 and a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] < 0.38 and a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] > -0.38:
                print("Forward tilt")
                parallelGait(0, 0, 3, 0, 0, 0)
                self.pub.publish(self.CreateEmptyMsgJoy())
            # Down
            if a[PS3_AXIS_STICK_RIGHT_UPWARDS] < -0.2 and a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] < 0.38 and a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] > -0.38:
                print("Backward tilt")
                parallelGait(0, 0, -3, 0, 0, 0)
                self.pub.publish(self.CreateEmptyMsgJoy())
            # Top Left
            if a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] > 0.38 and a[PS3_AXIS_STICK_RIGHT_UPWARDS] > 0.38:
                print("Forward-Left tilt")
                parallelGait(0, 2, 2, 0, 0, 0)
                self.pub.publish(self.CreateEmptyMsgJoy())
            # Top Right
            if a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] < -0.38 and a[PS3_AXIS_STICK_RIGHT_UPWARDS] > 0.38:
                print("Forward-Right tilt")
                parallelGait(0, -2, -2, 0, 0, 0)
                self.pub.publish(self.CreateEmptyMsgJoy())
            # Bottom Left
            if a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] > 0.38 and a[PS3_AXIS_STICK_RIGHT_UPWARDS] < -0.38:
                print("Backward-Left tilt")
                parallelGait(0, 2, -2, 0, 0, 0)
                self.pub.publish(self.CreateEmptyMsgJoy())
            # Bottom Right
            if a[PS3_AXIS_STICK_RIGHT_LEFTWARDS] < -0.38 and a[PS3_AXIS_STICK_RIGHT_UPWARDS] < -0.38:
                print("Backward-Right tilt")
                parallelGait(0, -2, 2, 0, 0, 0)
                self.pub.publish(self.CreateEmptyMsgJoy())

        rospy.sleep(0.01)

    def ControllerNode(self):
        rospy.init_node('JoystickPS3')
        while not rospy.is_shutdown():
            rospy.Subscriber('joy', Joy, self.callback, queue_size=3)
            self.pub = rospy.Publisher('joy', Joy, queue_size=1)
            self.ButtonMapping()


JoystickPS3()
