from SunFounder_PiCar.picar import front_wheels, back_wheels 
from SunFounder_PiCar.picar.SunFounder_PCA9685 import Servo
from SunFounder_PiCar.picar import PCF8591
from time import sleep
import RPi.GPIO as GPIO
from SunFounder_PiCar import picar

ADC = PCF8591.PCF8591(0x48)
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
fw.turning_max = 45

def toggle_lock():
    lock = True
def pan(pan_angle):
    pan_angle = 90 + pan_angle
    pan_servo.write(pan_angle)

def tilt(tilt_angle):
    tilt_angle = 90 + tilt_angle
    tilt_servo.write(tilt_angle)

def ready():
    global lock
    lock = False
    picar.setup()
    bw.stop()
    fw.turn_straight()
    Servo.install()
    pan(0)

def forward(forward_speed = 35):
    bw.forward()
    bw.speed = forward_speed

def backward(backward_speed = 35):
    bw.backward()
    bw.speed = backward_speed

def stop():
    bw.stop()

def stop_all():
    bw.stop()
    fw.turn_straight()

def turn(direction, angle):
    '''This function is assuming that the servo works like a unit circle...'''
    if (direction == 'left'):
        fw.turn(angle)
        turn_action = str('l' + str(angle))
    elif (direction == 'right'):
        turn_action = str('r' + str(angle))
        nangle = 360 - angle
        fw.turn(nangle)

def straighten():
    fw.turn_straight()

def retrieve_distance():
    sleep(0.05)
    range1 = ADC.read(0)
    sleep(0.05)
    range2 = ADC.read(0)
    sleep(0.05)
    range3 = ADC.read(0)
    A0 = (range1 + range2 + range3) / 3
    return A0

def correct_path(action):
    if (action == 'far_right'):
        #Corrects the robot if it is too far from the right side wall
        turn('right', 10)
        forward()
        sleep(0.5)
        turn('left', 20)
        sleep(0.5)
        stop_all()
    elif (action == 'close_right'):
        #Corrects the robot if it is too close to the right side wall
        turn('left', 10)
        forward()
        sleep(0.5)
        turn('right', 20)
        sleep(0.25)
        stop_all()
    elif (action == 'close_straight'):
        #Corrects the robot if it is too close to the wall infront of it
        turn('right', 22.5)
        backward()
        sleep(0.5)
        stop_all()
        turn('left', 22.5)
        forward()
        sleep(0.5)
        stop_all()
    elif (action == 'close_straight_and_right'):
        #For if the robot is too close to both the front and right side wall, IE if it hits a corner.
        backward(backward_speed=50)
        sleep(1)
        stop_all()
        turn('left', 45)
        forward(forward_speed=50)
        sleep(2.5)
        stop_all()
    elif (action == 'far_right_close_front'):
        turn('right', 45)
        backward()
        sleep(0.5)
        stop_all()
        turn('left', 10)
        forward()
        sleep(0.25)
        stop_all()
