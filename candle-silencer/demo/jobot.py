from SunFounder_PiCar.picar import front_wheels, back_wheels 
from SunFounder_PiCar.picar.SunFounder_PCA9685 import Servo
from time import sleep
from threading import Thread
import RPi.GPIO as GPIO
from SunFounder_PiCar import picar
from silencer import record

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
fw.turning_max = 45

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

def turn(direction, angle):
    '''This function is assuming that the servo works like a unit circle...'''
    if (direction == 'left'):
        fw.turn(angle)
    elif (direction == 'right'):
        angle = 360 - angle
        fw.turn(angle)

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

def pan(pan_angle):
    pan_angle = 90 + pan_angle
    pan_servo.write(pan_angle)

def tilt(tilt_angle):
    tilt_angle = 90 + tilt_angle
    tilt_servo.write(tilt_angle)

def ready():
    picar.setup()
    stop_all()
    install_servos()
    pan(0)
    tilt(0)

def install_servos():
    Servo.install()

def retrieve_distance():
    distance = 255
    return distance

def correct_path(action):
    if (action == 'far_right'):
        #Corrects the robot if it is too far from the right side wall
        turn('right', 15)
        record('r15')
        forward()
        record('forward')
        sleep(1)
        turn('left', 30)
        record('l30')
        sleep(1)
        stop_all()
        record('stop')
        record('straighten')
    elif (action == 'close_right'):
        #Corrects the robot if it is too close to the right side wall
        pass
    elif (action == 'close_sraight'):
        #Corrects the robot if it is too close to the wall infront of it
        pass
    elif (action == 'close_left'):
        #On the very rare occurance that this happens it will correct the robot if it is too close to the left side wall
        pass

def revert(action_to_revert):
    ''' Essentially turns the action inputted into the exact opposite of that action. '''
    if (action_to_revert[0] == 'l'):
        returning_list = []
        turn_angle = int(action_to_revert[1] + action_to_revert[2])
        returning_list.append('right')
        returning_list.append(turn_angle)
    elif (action_to_revert[0] == 'r'):
        turn_angle = int(action_to_revert[1] + action_to_revert[2])
        returning_list.append('left')
        returning_list.append(turn_angle)
    elif (action_to_revert == 'forward'):
        returning_list.append('backward')
    elif (action_to_revert == 'backward'):
        returning_list.append('forward')
    elif (action_to_revert == 'stop'):
        returning_list.append('stop')
    return returning_list


def retrace(action_list, timer_list):
    ''' The backbone of returning to the starting location of the jobot. '''
    #action_list.reverse()
    #timer_list.reverse()
    indexer = 0
    for action in action_list:
        stop = False
        returned_list = revert(action)
        if (returned_list[0] == 'right'):
            turn('right', returned_list[1])
        elif (returned_list[0] == 'left'):
            turn('left', returned_list[1])
        elif (returned_list[0] == 'forward'):
            forward()
            stop = True
        elif (returned_list[0] == 'backward'):
            backward()
            stop = True
        elif (returned_list[0] == 'stop'):
            stop()
        elif (returned_list[0] == 'straighten'):
            straighten()
        if (returned_list[0] == 'stop'):
            pass
        elif (stop == True):
            sleep(int(timer_list[indexer]))
            stop()

        indexer += 1
        

