
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

tac_1_pin = 5
tac_2_pin = 6
tac_3_pin = 13
tac_4_pin = 19
tac_5_pin = 26
tac_6_pin = 21


def rc_time(sensor):
    count = 0
    GPIO.setup(sensor, GPIO.OUT)
    GPIO.output(sensor, GPIO.LOW)
    time.sleep(0.01)
    GPIO.setup(sensor, GPIO.IN)
    while (GPIO.input(sensor) == GPIO.LOW):
        count += 1
        if count > 2000:
            count = 0
            GPIO.setup(sensor, GPIO.OUT)
            GPIO.output(sensor, GPIO.HIGH)
    return count


def tactile1():
    tac_1_input = rc_time(tac_1_pin)
    if (tac_1_input > 20):
        # print("1", tac_1_input)
        tac_1 = 1
        return tac_1
    else:
        tac_1 = 0
        return tac_1


def tactile2():
    tac_2_input = rc_time(tac_2_pin)
    if (tac_2_input > 20):
        # print("2", tac_2_input)
        tac_2 = 1
        return tac_2
    else:
        tac_2 = 0
        return tac_2


def tactile3():
    tac_3_input = rc_time(tac_3_pin)
    if (tac_3_input > 20):
        # print("1", tac_3_input)
        tac_3 = 1
        return tac_3
    else:
        tac_3 = 0
        return tac_3


def tactile4():
    tac_4_input = rc_time(tac_4_pin)
    if (tac_4_input > 20):
        # print("4", tac_4_input)
        tac_4 = 1
        return tac_4
    else:
        tac_4 = 0
        return tac_4


def tactile5():
    tac_5_input = rc_time(tac_5_pin)
    if (tac_5_input > 20):
        # print("5", tac_5_input)
        tac_5 = 1
        return tac_5
    else:
        tac_5 = 0
        return tac_5


def tactile6():
    tac_6_input = rc_time(tac_6_pin)
    if (tac_6_input > 20):
        # print("6", tac_6_input)
        tac_6 = 1
        return tac_6
    else:
        tac_6 = 0
        return tac_6


def allTactiles():
    a = tactile1()
    b = tactile2()
    c = tactile3()
    d = tactile4()
    e = tactile5()
    f = tactile6()
    return [a, b, c, d, e, f]
