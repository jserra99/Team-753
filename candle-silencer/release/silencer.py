#importing necessary modules...
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
import jobot as jb

#Set up area
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

redLED = 20
startButton = 5
midDistanceSensor = 26
midThermalSensor = 6
preciseThermalSensor = 13
waterPump = 12
rightPhysicalSensor = 19

pull_up_down = GPIO.PUD_UP
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(startButton, GPIO.IN, pull_up_down)
GPIO.setup(midDistanceSensor, GPIO.IN, pull_up_down)
GPIO.setup(preciseThermalSensor, GPIO.IN, pull_up_down)
GPIO.setup(midThermalSensor, GPIO.IN, pull_up_down)
GPIO.setup(waterPump, GPIO.OUT)
GPIO.setup(rightPhysicalSensor, GPIO.IN, pull_up_down)

def check_sensors():
    global end
    end = False
    i = 0
    while (end == False):
        stuck = False
        state = GPIO.input(rightPhysicalSensor)
        front_state = GPIO.input(midDistanceSensor)
        button_state = GPIO.input(startButton)
        if (actually_kys == False):
            if (state == 0):
                i = 0
                pause = True
                print("Right press detected...")
                jb.stop_all()
                sleep(0.5)
                jb.correct_path('close_right')
                pause = False
            elif (front_state == 0):
                i = 0
                pause = True
                print("Front press detected...")
                jb.stop_all()
                sleep(0.5)
                jb.correct_path("close_straight_and_right")
                pause = False
            elif (button_state == 0):
                pause = True
                jb.stop_all()
                sensor_thread._stop()
                thermal_thread._stop()
                quit
            elif (i == 1500):
                pause = True
                jb.stop_all()
                i = 0
                print("Lord jesus help me god i am stuck...")
                jb.turn('right', 45)
                jb.forward(forward_speed=100)
                jb.sleep(1)
                jb.stop_all()
                jb.backward(backward_speed=50)
                sleep(1)
                jb.stop()
                jb.turn('left', 45)
                jb.forward()
                sleep(5)
                jb.stop_all()
                pause = False
            i += 1
            print(i)
        sleep(0.01)
sensor_thread = Thread(target= check_sensors)

def seek_candle(angle_found):
    if (angle_found >= 0 and angle_found <= 15):
        TTW = 0.5
    elif (angle_found >= 15 and angle_found <= 30):
        TTW = 1
    elif (angle_found >= 30 and angle_found <= 60):
        TTW = 2.75
    elif (angle_found >= 60 and angle_found <= 90):
        TTW = 4.75
    candle_found = True
    pause = True
    jb.pan(0)
    GPIO.output(redLED, GPIO.HIGH)
    for i in range (2):
        jb.stop_all()
        print("Candle has been found... Waiting.")
        sleep(1)
    jb.stop_all()
    jb.turn('right', 45)
    jb.backward(backward_speed= 35)
    sleep(TTW)
    jb.stop_all()
    GPIO.output(waterPump, GPIO.HIGH)
    jb.forward(forward_speed= 30)
    sleep(3)
    for i in range (10):
        jb.stop_all()
        sleep(1)
    print("Ladies and gentlemen we got em.")
    print("*Crowd Applaudes*")
    GPIO.output(redLED, GPIO.LOW)
    GPIO.output(waterPump, GPIO.LOW)

def thermals():
    while (end == False):
        found = False
        r = 0
        for i in range (90):
            angle = 90 - 1 * i
            jb.pan(angle)
            thermalGen = GPIO.input(midThermalSensor)
            thermalAccu = GPIO.input(preciseThermalSensor)
            if (thermalGen == 0):
                print("Candle found at: ", angle)
                found = True
                seek_candle(angle)

            sleep(0.025)
        if (found == False and pause == False):
            print("All Clear", r)
            jb.turn('right', 5)
            jb.forward(forward_speed= 65)
            i += 1
            sleep(1)
thermal_thread = Thread(target= thermals)
#Where the main logic loop is
def __main__():
    global candle_found
    global pause
    global actually_kys
    pause = False
    candle_found = False
    actually_kys = False
    sensor_thread.start()
    thermal_thread.start()
