#!/usr/bin/env python


import time
import rospy
import RPi.GPIO as GPIO
from std_msgs.msg import Int16

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
    time.sleep(0.01)
    GPIO.setup(sensor, GPIO.IN)
    while (GPIO.input(sensor) == GPIO.LOW):
        count += 1
        if count > 3000:
            count = 0
            GPIO.setup(sensor, GPIO.OUT)
            GPIO.output(sensor, GPIO.HIGH)
    return count

def tac_pub():
    tac_1_pub = rospy.Publisher('tactile_1', Int16, queue_size=10)
    tac_2_pub = rospy.Publisher('tactile_2', Int16, queue_size=10)
    tac_3_pub = rospy.Publisher('tactile_3', Int16, queue_size=10)
    tac_4_pub = rospy.Publisher('tactile_4', Int16, queue_size=10)
    tac_5_pub = rospy.Publisher('tactile_5', Int16, queue_size=10)
    tac_6_pub = rospy.Publisher('tactile_6', Int16, queue_size=10)
    rospy.init_node('pub_tactile', anonymous=True)
    rate = rospy.Rate(10)                         # 10 hz
    while not rospy.is_shutdown():                # when no ctrl+c is called in terminal.

        tac_1_input = rc_time (tac_1_pin)         # take a reading from sensor
        if True: #(tac_1_input > 20):             # is the reading low enough to be pressure
            rospy.loginfo(tac_1_input)            # prints the message to screen, log and rosout
            tac_1_pub.publish(tac_1_input)        # send the string to the publishe

        tac_2_input = rc_time (tac_2_pin)
        if True: #(tac_2_input > 20):
            rospy.loginfo(tac_2_input)
            tac_2_pub.publish(tac_2_input)
        rate.sleep()

        tac_3_input = rc_time (tac_3_pin)
        if True: #(tac_3_input > 20):
            rospy.loginfo(tac_3_input)
            tac_3_pub.publish(tac_3_input)
        rate.sleep()

        tac_4_input = rc_time (tac_4_pin)
        if True: #(tac_4_input > 20):
            rospy.loginfo(tac_4_input)
            tac_4_pub.publish(tac_4_input)
        rate.sleep()

        tac_5_input = rc_time (tac_5_pin)
        if True: #(tac_5_input > 20):
            rospy.loginfo(tac_5_input)
            tac_5_pub.publish(tac_5_input)
        rate.sleep()

        tac_6_input = rc_time (tac_6_pin)
        if True: #(tac_6_input > 20):
            rospy.loginfo(tac_6_input)
            tac_6_pub.publish(tac_6_input)
        rate.sleep()

if __name__ == '__main__':
    try:
        tac_pub()
    except rospy.ROSInterruptException:
        pass
