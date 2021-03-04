#This particular script is only compatible with a raspberry pi or versions of linux that support evdev.
#This one is made for an xbox one controller, however this method can be applied to practically anything.

#Importing dependencies.
from evdev import InputDevice, categorize, ecodes
from time import sleep
import jobot as jb
import RPi.GPIO as GPIO

#Setting the crucial gamepad and printing it out.
gamepad = InputDevice('/dev/input/event0')
print(gamepad)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
redLED = 20
startButton = 16
pull_up_down = GPIO.PUD_UP
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(startButton, GPIO.IN)
#The numbers are the code value for that given button.
#Mapping the numbers to rememberable buttons will help for later on.

#A, B, X, and Y buttons.
aBtn = 304
bBtn = 305
xBtn = 307
yBtn = 308

#The bumpers
LBmper = 310
RBmper = 311

#The utility buttons in the middle of the controller.
MenuBtn = 315
WindowBtn = 314
XboxBtn = 316

#The D-pad mappings which can only have one given button down at a time.
HorizontalDp = 16
VerticalDp = 17

#The two triggers.
RightT = 5
LeftT = 2

#The input from when you "click" in a stick.
LeftStickClick = 317
RightStickClick = 318

#The Left and Right stick axis.
Ls_X = 0
Ls_Y = 1
Rs_X = 3
Rs_Y = 4

#The mainloop responsible for handling events when a given button is pressed
jb.stop_all()
#jb.standby(redLED, startButton)
for event in gamepad.read_loop():
    value = event.value
    code = event.code
    if (code == aBtn):
        if (value == 1):
            GPIO.output(redLED, GPIO.HIGH)
            print("The A button is pressed")
        if (value == 0):
            GPIO.output(redLED, GPIO.LOW)
            print("The A button was released")
    if (code == bBtn):
        if (value == 1):
            print("The B button is pressed")
        if (value == 0):
            print("The B button was released")
    if (code == xBtn):
        if (value == 1):
            print("The X button is pressed")
        if (value == 0):
            print("The X button was released")
    if (code == yBtn):
        if (value == 1):
            print("The Y button is pressed")
        if (value == 0):
            print("The Y button was released")
    if (code == LBmper):
        if (value == 1):
            print("The left bumper is pressed")
        if (value == 0):
            print("The left bumper was released")
    if (code == RBmper):
        if (value == 1):
            print("The right bumper is pressed")
        if (value == 0):
            print("The right bumper was released")
    if (code == MenuBtn):
        if (value == 1):
            print("The menu button is pressed")
        if (value == 0):
            print("The menu button was released")
    if (code == WindowBtn):
        if (value == 1):
            print("The window button is pressed")
        if (value == 0):
            print("The window button was released")
    if (code == HorizontalDp):
        if (value == 1):
            jb.turn('right')
            print("Right on D-pad is pressed.")
        if (value == -1):
            jb.turn('left')
            print("Left on D-pad is pressed.")
        if (value == 0):
            jb.straighten()
            print("The horizontal D-pad was released.")
    if (code == VerticalDp):
        if (value == 1):
            print("Down on D-pad was pressed.")
        if (value == -1):
            print("Up on D-pad was pressed.")
        if (value == 0):
            print("The vertical D-pad was released.")
    #The section for the triggers, the max input value is 1023 the deadzone i would reccomend is 100 which is an equivalent to 10%.
    if (code == RightT):
        if (value >= 250):
            jb.forward(25)
            print("Right Trigger is 25% depressed.")
        if (value >= 750):
            jb.forward(75)
            print("Right Trigger is 75% depressed.")
        if (value == 1023):
            jb.forward(100)
            print("Right Trigger is fully depressed.")
        else:
            jb.stop()
            print("Right Trigger is no longer depressed.")
    if (code == LeftT):
        if (value >= 250):
            jb.backward(25)
            print("Left Trigger is 25% depressed.")
        if (value >= 750):
            jb.backward(75)
            print("Left Trigger is 75% depressed.")
        if (value == 1023):
            jb.backward(100)
            print("Left Trigger is fully depressed.")
        else:
            jb.stop()
            print("Left Trigger is no longer depressed.")
    if (code == LeftStickClick):
        if (value == 1):
            print("Left Stick was clicked inward.")
        if (value == 0):
            print("Left Stick click was released.")
    if (code == RightStickClick):
        if (value == 1):
            print("Right Stick was clicked inward.")
        if (value == 0):
            print("Right Stick click was released.")
    if (code == Ls_X and value != 0):
        if (value <= -10000):
            jb.turn('left')
            print("Left Stick left.")
        elif (value >= 10000):
            jb.turn('right')
            print("Left Stick right.")
        else:
            jb.straighten()

    if (code == Ls_Y):
        if (value <= -10000):
            print("Left Stick up.")
        if (value >= 10000):
            print("Left Stick down.")
    if (code == Rs_Y):
        if (value <= -10000):
            print("Right Stick up.")
        if (value >= 10000):
            print("Right Stick down.")
    if (code == Rs_X):
        if (value <= -10000):
            print("Right Stick left.")
        if (value >= 10000):
            print("Right Stick right.")
    if (code == XboxBtn):
        if (value == 1):
            print("The xbox button was pressed.")
        else:
            print("The xbox button was released.")
