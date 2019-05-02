#!/usr/bin/env python


import rospy
import RPi.GPIO as GPIO
import time
from std_msgs.msg import String

# determine board pin numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# pin for sensor
tac_1_pin = 5
tac_2_pin = 6
tac_3_pin = 13
tac_4_pin = 19
tac_5_pin = 26
tac_6_pin = 21

# record pressure duration
def rc_time (sensor):
    count = 0
    GPIO.setup(sensor, GPIO.OUT)
    GPIO.output(sensor, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(sensor, GPIO.IN)
    while (GPIO.input(sensor) == GPIO.LOW):
        count += 1
    return count

def tac_pub():
    pub_tac_1 = rospy.Publisher('tactile_1', String, queue_size=10)
    pub_tac_2 = rospy.Publisher('tactile_2', String, queue_size=10)
    pub_tac_3 = rospy.Publisher('tactile_3', String, queue_size=10)
    pub_tac_4 = rospy.Publisher('tactile_4', String, queue_size=10)
    pub_tac_5 = rospy.Publisher('tactile_5', String, queue_size=10)
    pub_tac_6 = rospy.Publisher('tactile_6', String, queue_size=10)
    rospy.init_node('pub_tactile', anonymous=True)
    rate = rospy.Rate(5) # 5 hz
    while not rospy.is_shutdown():
        tac_1_input = rc_time (tac_1_pin)    # take a reading from sensor
        if (tac_1_input < 2000):                # is the reading low enough to be pressure
            tac_1_str = "Leg 1: Ground Contact: {}" .format(tac_1_input)   # format the string to pass to the topic
            rospy.loginfo(tac_1_str)            # prints the message to screen, log and rosout
            pub_tac_1.publish(tac_1_str)        # send the string to the publishe

        tac_2_input = rc_time (tac_2_pin)
        if (tac_2_input < 2000):
            tac_2_str = "Leg 2: Ground Contact: {}" .format(tac_2_input)
            rospy.loginfo(tac_2_str)
            pub_tac_2.publish(tac_2_str)
        rate.sleep()

        tac_3_input = rc_time (tac_3_pin)
        if (tac_3_input < 2000):
            tac_3_str = "Leg 3: Ground Contact: {}" .format(tac_3_input)
            rospy.loginfo(tac_3_str)
            pub_tac_3.publish(tac_3_str)
        rate.sleep()

        tac_4_input = rc_time (tac_4_pin)
        if (tac_4_input < 2000):
            tac_4_str = "Leg 4: Ground Contact: {}" .format(tac_4_input)
            rospy.loginfo(tac_4_str)
            pub_tac_4.publish(tac_4_str)
        rate.sleep()

        tac_5_input = rc_time (tac_5_pin)
        if (tac_5_input < 2000):
            tac_5_str = "Leg 5: Ground Contact: {}" .format(tac_5_input)
            rospy.loginfo(tac_5_str)
            pub_tac_5.publish(tac_5_str)
        rate.sleep()

        tac_6_input = rc_time (tac_6_pin)
        if (tac_6_input < 2000):
            tac_6_str = "Leg 6: Ground Contact: {}" .format(tac_6_input)
            rospy.loginfo(tac_6_str)
            pub_6_tac.publish(tac_6_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        tac_pub()
    except rospy.ROSInterruptException:
        pass
