#importing necessary modules...
import RPi.GPIO as GPIO
from time import sleep
import jobot as jb
from threading import Thread

#Set up area
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

redLED = 20
startButton = 5
midDistanceSensor = 26
midThermalSensor = 6
waterPump = 12

pull_up_down = GPIO.PUD_UP
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(startButton, GPIO.IN, pull_up_down)
GPIO.setup(midDistanceSensor, GPIO.IN, pull_up_down)
GPIO.setup(midThermalSensor, GPIO.IN, pull_up_down)
GPIO.setup(waterPump, GPIO.OUT)

#Run this after everything is set up
jb.ready()
candle_found = False
just_reset = False
previous_pan = 0
max_distance_threshold = 200
min_distance_threshold = 100
timer_thread = Thread(target = start_timer)
timed_list = []
action_list = []

def start_timer():
        global clock
        global rt_clock
        rt_clock = 0
        while (True):
            rt_clock = rt_clock + .01
            clock = round(rt_clock, 2)
            sleep(.01)

def rotate_check():
    IR_Distance_Data = []
    IR_Thermal_Data = []
    jb.stop_all()
    for i in range (3):
        angle = 90 - 90 * i
        jb.pan(angle)
        IR_Distance_Data.append(jb.retrieve_distance())
        IR_Thermal_Data.append(GPIO.input(midThermalSensor))
        sleep(0.25)
    Frontal_Distance = GPIO.input(midDistanceSensor)
    print("IR Distance: ", IR_Distance_Data)
    print("Thermal Data: ", IR_Thermal_Data)
    print(Frontal_Distance)
    return IR_Distance_Data, IR_Thermal_Data, Frontal_Distance

def record(action):
    action_list.append(action)
    timed_list.append(int(clock))
    rt_clock = 0

#Where the main logic loop is
def __main__():
    timer_thread.start()
    while (candle_found == False):
        obstructions = False
        distances, thermal, front_distance = rotate_check()
        rt_clock = 0
        if (0 in thermal):
            obstructions = True
            if (thermal[0] == 0):
                print("Candle is on the left.")
                candle_found = True
                pass
            elif (thermal[1] == 0):
                print("Candle is infront.")
                candle_found = True
                pass
            else:
                print("Candle is on the right")
                candle_found = True
                pass
        for distance in distances:
            if (distance >= max_distance_threshold and distances.index(distance) == 2):
                print("Jobot is too far from the right side wall!")
                jb.correct_path('far_right')
                obstructions = True
                break
            elif (distance <= min_distance_threshold):
                if (distances.index(distance) == 2):
                    print("Jobot is too close to the right side wall!")
                    jb.correct_path('close_right')
                    obstructions = True
                    break
                elif (distances.index(distance) == 1):
                    print("Jobot is too close to the front side wall!")
                    jb.correct_path('close_straight')
                    obstructions = True
                    break
                else:
                    print("Jobot is too close to the left side wall!")
                    jb.correct_path('close_left')
                    obstructions = True
                    break
        if (obstructions == False):
            ''' If all the sensors detect nothing wrong then this will run. '''
            jb.turn('right', 10)
            record('r10')
            jb.forward()
            record('forward')
            sleep(1)
            jb.turn('left', 20)
            record('l20')
            sleep(1)
            jb.stop_all()
            record('stop')
            record('straighten')
    jb.retrace(action_list, timed_list)
