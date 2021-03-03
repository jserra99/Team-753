#importing necessary modules...
import Rpi.GPIO as GPIO
from time import sleep
import jobot as jb

#Set up area
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

redLED = 20
startButton = 16
leftDistanceSensor = 12
midDistanceSensor = 26
rightDistanceSensor = 19 
leftThermalSensor = 13
midThermalSensor = 6
rightThermalSensor = 5

pull_up_down = GPIO.PUD_UP
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(startButton, GPIO.IN, pull_up_down)
GPIO.setup(leftDistanceSensor, GPIO.IN, pull_up_down)
GPIO.setup(midDistanceSensor, GPIO.IN, pull_up_down)
GPIO.setup(rightDistanceSensor, GPIO.IN, pull_up_down)
GPIO.setup(leftThermalSensor, GPIO.IN, pull_up_down)
GPIO.setup(midThermalSensor, GPIO.IN, pull_up_down)
GPIO.setup(rightThermalSensor, GPIO.IN, pull_up_down)

picar.setup()
#Run this after everything is set up
jb.standby(redLED, startButton)
candle_found = False
just_reset = False
leftDistance = GPIO.input(leftDistanceSensor)
midDistance = GPIO.input(midDistanceSensor)
rightDistance = GPIO.input(rightDistanceSensor)
leftThermal = GPIO.input(leftThermalSensor)
midThermal = GPIO.input(midThermalSensor)
rightThermal = GPIO.input(rightThermalSensor)
stopButton = GPIO.input(startButton)
#Where the main logic loop is
def __main__():
    while (candle_found == False):
        if (leftDistance or midDistance or rightDistance or leftThermal or midThermal or rightThermal == 0):
            if (leftThermal or midThermal or rightThermal == 0):
                if (leftThermal == 0):
                    #
                elif (rightThermal == 0):
                    #
                else:
                    #
            else:
                if (leftDistance == 0):
                    #Back away from the left wall
                    jb.stop()
                    jb.turn('left', 45)
                    jb.backward()
                    sleep(1)
                    jb.stop_all()
                    just_reset = True
                elif (rightDistance == 0):
                    #Back away from the right wall
                    jb.stop()
                    jb.turn('right', 45)
                    jb.backward()
                    sleep(1)
                    jb.stop_all()
                    just_reset = True
                else:
                    #Back up and turn left?
                    jb.stop()
                    jb.turn('right', 45)
                    jb.backward()
                    sleep(1)
                    jb.stop_all()
                    just_reset = True
        elif (stopButton == 0):
            break
        else:
            #Pathfinding algorithm
            if (just_reset == True):
                jb.forward()
                sleep(0.5)
                jb.turn('right', 30)
                just_reset = False
            else:
                jb.turn('right', 30)
                jb.forward()

        sleep(0.01)
    jb.standby(redLED, startButton)  
    __main__()
