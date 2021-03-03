from SunFounder_PiCar.picar import front_wheels, back_wheels 
from SunFounder_PiCar.picar.SunFounder_PCA9685 import Servo
from time import sleep
from threading import Thread
import RPi.GPIO as GPIO
from SunFounder_PiCar import picar

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
fw.turning_max = 45

def standby(LED_pin, button_pin):
    '''Run this command when everything is completely setup and you just want the robot to idle.'''
    picar.setup()
    GPIO.output(LED_pin, GPIO.HIGH)
    button_state = GPIO.input(button_pin)
    timer_thread = Thread(target = start_timer)
    print("DEBUG: AWAITING BUTTON PRESS")
    while (True):
        if (button_state == 1):
            print("DEBUG: BUTTON PRESS DETECTED, STARTING SILENCER")
            GPIO.output(LED_pin, GPIO.LOW)
            timer_thread.start()
            break
        else:
            sleep(0.01)

def forward(forward_speed = 75):
    print("DEBUG: FORWARD")
    bw.forward()
    bw.speed = forward_speed

def backward(backward_speed = 75):
    print("DEBUG: BACKWARD")
    bw.backward()
    bw.speed = backward_speed

def stop():
    print("DEBUG: STOPPING WHEELS")
    bw.stop()

def stop_all():
    print("DEBUG: RESETTING ALL MOTORS")
    bw.stop()
    fw.turn_straight()

def turn(direction, degree):
    '''This function is assuming that the servo works like a unit circle...'''
    if (direction == 'left'):
        print("DEBUG: TURNING LEFT BY " + degree + "DEGREES")
        degree = degree - (degree * 2)
        fw.turn(degree)
    elif (direction == 'right'):
        print("DEBUG: TURNING RIGHT BY " + degree + "DEGREES")
        fw.turn(degree)

def straighten():
    print("DEBUG: STRAIGHTENING WHEELS")
    fw.turn_straight()

def start_timer():
    global clock
    rt_clock = 0
    while (True):
        rt_clock = rt_clock + .01
        clock = round(rt_clock, 2)
        sleep(.01)

def obstacle_detection():
    while (True):
        #might not be needed...
