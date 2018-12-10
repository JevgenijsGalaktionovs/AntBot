#!/usr/bin/env python

import RPi.GPIO as GPIO
import time






class CameraNeck:

    FREQUENCY_RATE   = 100    # frequency = 100 Hz
    START_POS_PAN    = 14.0   # initial duty cycle = 14% for 90 degrees angle
    START_POS_TILT   = 19.0   # initial duty cycle = 19% for 140 degrees angle
    MAX_PAN 	     = 23.0
    MIN_PAN          = 5.0
    MAX_TILT         = 20.0
    MIN_TILT 	     = 7.0
    def __init__(self):

        self.pan_gpio_pin       = 18
        self.tilt_gpio_pin      = 19

        self.current_pan_angle  = self.START_POS_PAN
        self.current_tilt_angle = self.START_POS_TILT


        GPIO.setmode(GPIO.BCM) # use GPIO pin numbering, not physical pin numbering
	GPIO.setwarnings(False)
        GPIO.setup(self.tilt_gpio_pin, GPIO.OUT)
        GPIO.setup(self.pan_gpio_pin,  GPIO.OUT)
        GPIO.setup(self.tilt_gpio_pin, GPIO.OUT)

        self.pan_pwmObject  = GPIO.PWM(self.pan_gpio_pin,  self.FREQUENCY_RATE)
        self.tilt_pwmObject = GPIO.PWM(self.tilt_gpio_pin, self.FREQUENCY_RATE)

        self.NeckStartPos()


    def NeckStartPos(self):
        self.current_pan_angle  = self.START_POS_PAN
        self.current_tilt_angle = self.START_POS_TILT
        self.pan_pwmObject.start(self.current_pan_angle)
        self.tilt_pwmObject.start(self.current_tilt_angle)
        time.sleep(0.5)			        # short delay before PWM shut off
        self.pan_pwmObject.start(0)		# Turn PWM off to prevent shake
        self.tilt_pwmObject.start(0)


    def PanLeft(self, pwm): # 1PWM = 10 degrees
      	pwm = -(pwm)
        value = self.ValueGenerator(self.current_pan_angle, self.MAX_PAN, self.MIN_PAN, pwm)
	self.current_pan_angle = value

        self.pan_pwmObject.ChangeDutyCycle(value)
        time.sleep(0.5)
        self.pan_pwmObject.ChangeDutyCycle(0.0)


    def ValueGenerator(self,servo_angle,MAX,MIN, pwm):

        new_servo_angle =  servo_angle + pwm
        print new_servo_angle, servo_angle, pwm
        if new_servo_angle > MAX:
            print 'Max reached. PAN PWM is set to %d!' % MAX
 	    return float(MAX)
        elif new_servo_angle < MIN:
            print 'Min reached. PAN PWM is set to %d!' % MIN
            return float(MIN)
        else:
            return float(new_servo_angle)

    def PanRight(self,pwm):
	value = self.ValueGenerator(self.current_pan_angle, self.MAX_PAN, self.MIN_PAN, pwm)
	self.current_pan_angle = value

        self.pan_pwmObject.ChangeDutyCycle(value)
        time.sleep(0.5)
        self.pan_pwmObject.ChangeDutyCycle(0.0)


    def TiltDown(self,pwm):
	value = self.ValueGenerator(self.current_tilt_angle, self.MAX_TILT, self.MIN_TILT, pwm)
	self.current_tilt_angle = value

        self.tilt_pwmObject.ChangeDutyCycle(value)
        time.sleep(0.5)
        self.tilt_pwmObject.ChangeDutyCycle(0.0)

    def TiltUp(self,pwm):
	pwm = -(pwm)
	value = self.ValueGenerator(self.current_tilt_angle, self.MAX_TILT, self.MIN_TILT, pwm)
	self.current_tilt_angle = value

        self.tilt_pwmObject.ChangeDutyCycle(value)
        time.sleep(0.5)
        self.tilt_pwmObject.ChangeDutyCycle(0.0)
