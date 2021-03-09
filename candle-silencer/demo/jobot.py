from SunFounder_PiCar.picar import front_wheels, back_wheels 
from SunFounder_PiCar.picar.SunFounder_PCA9685 import Servo
from time import sleep
from threading import Thread
import RPi.GPIO as GPIO
from SunFounder_PiCar import picar

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
fw.turning_max = 45
over = False

def pan(pan_angle):
    pan_angle = 90 + pan_angle
    pan_servo.write(pan_angle)

def tilt(tilt_angle):
    tilt_angle = 90 + tilt_angle
    tilt_servo.write(tilt_angle)

def ready():
    picar.setup()
    bw.stop()
    fw.turn_straight()
    Servo.install()
    pan(0)
    tilt(0)

from silencer import record

def forward(forward_speed = 75):
    print("DEBUG: FORWARD")
    bw.forward()
    bw.speed = forward_speed
    if (over == False):
        record('forward')

def backward(backward_speed = 75):
    print("DEBUG: BACKWARD")
    bw.backward()
    bw.speed = backward_speed
    if (over == False):
        record('backward')

def stop():
    print("DEBUG: STOPPING WHEELS")
    bw.stop()
    if (over == False):
        record('stop')

def stop_all():
    print("DEBUG: RESETTING ALL MOTORS")
    bw.stop()
    fw.turn_straight()
    if (over == False):
        record('stop')
        record('straighten')

def turn(direction, angle):
    '''This function is assuming that the servo works like a unit circle...'''
    if (direction == 'left'):
        fw.turn(angle)
        print("DEBUG: TURNING LEFT BY " + str(angle) + " DEGREES")
        turn_action = str('l' + str(angle))
    elif (direction == 'right'):
        turn_action = str('r' + str(angle))
        nangle = 360 - angle
        fw.turn(nangle)
        print("DEBUG: TURNING RIGHT BY " + str(angle) + " DEGREES")
    if (over == False):
        record(turn_action)

def straighten():
    print("DEBUG: STRAIGHTENING WHEELS")
    fw.turn_straight()
    if (over == False):
        record('straighten')

def start_timer():
    global clock
    rt_clock = 0
    while (True):
        rt_clock = rt_clock + .01
        clock = round(rt_clock, 2)
        sleep(.01)

def retrieve_distance():
    distance = 255
    return distance

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
        sleep(0.5)
        stop_all()
    elif (action == 'close_straight'):
        #Corrects the robot if it is too close to the wall infront of it
        turn('right', 22.5)
        backward()
        sleep(0.5)
        stop_all()
        turn('left', 22.5)
        forward()
        sleep(0.5
        stop_all()
    elif (action == 'close_left'):
        #On the very rare occurance that this happens it will correct the robot if it is too close to the left side wall
        pass

def revert(action_to_revert):
    ''' Essentially turns the action inputted into the exact opposite of that action. '''
    returning_list = []
    if (action_to_revert[0] == 'l'):
        turn_angle = int(action_to_revert[1] + action_to_revert[2])
        #returning_list.append('right')
        returning_list.append('left')
        returning_list.append(turn_angle)
    elif (action_to_revert[0] == 'r'):
        turn_angle = int(action_to_revert[1] + action_to_revert[2])
        #returning_list.append('left')
        returning_list.append('right')
        returning_list.append(turn_angle)
    elif (action_to_revert == 'forward'):
        returning_list.append('backward')
    elif (action_to_revert == 'backward'):
        returning_list.append('forward')
    elif (action_to_revert == 'stop'):
        returning_list.append('stop')
    elif (action_to_revert == 'straighten'):
        returning_list.append('straighten')
    return returning_list


def retrace(action_list, timer_list):
    ''' The backbone of returning to the starting location of the jobot. '''
    global over
    indexer = 0
    print(timer_list)
    over = True
    total_reversed_actions = []
    for action in action_list:
        plz_stop = False
        ignore = False
        returned_list = revert(action)
        total_reversed_actions.append(returned_list[0])
        print('TTW: ', timer_list[indexer])
        sleep(int(timer_list[indexer]))
        if (not returned_list):
            break
        if (returned_list[0] == 'right'):
            turn('right', returned_list[1])
            ignore = True
        elif (returned_list[0] == 'left'):
            turn('left', returned_list[1])
            ignore = True
        elif (returned_list[0] == 'forward'):
            forward()
            plz_stop = True
        elif (returned_list[0] == 'backward'):
            backward()
            plz_stop = True
        elif (returned_list[0] == 'stop'):
            stop()
        elif (returned_list[0] == 'straighten'):
            straighten()
            ignore = True
        if (returned_list[0] == 'stop'):
            ignore = True
            pass
        '''if (ignore == False):
            sleep(int(timer_list[indexer]))
            print('TTW: ', timer_list[indexer])
        else:
            print("Not waiting lol have fun with this statement joe!")'''
        indexer += 1
    print(total_reversed_actions)
    stop_all()
