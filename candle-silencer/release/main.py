''' The file which handles which script is executed and how that is done.'''
import jobot as jb
import RPi.GPIO as GPIO
import controllerdemo
import silencer
from time import sleep
from threading import Thread

class choose_your_weapon():
    def go():
        global chosen
        global redLED
        chosen = False
        redLED = 20
        startButton = 5
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(redLED, GPIO.OUT)
        GPIO.setup(startButton, GPIO.IN, GPIO.PUD_UP)
        jb.ready()
        print("Awaiting button press...")
        i = 0
        while (chosen == False):
            button_state = GPIO.input(startButton)
            if (i == 50):
                GPIO.output(redLED, GPIO.HIGH)
            elif (i == 100):
                GPIO.output(redLED, GPIO.LOW)
                i = 0
            if (button_state == 0):
                print("Initial Press")
                sleep(3)
                button_state = GPIO.input(startButton)
                if (button_state == 0):
                    print("2nd press")
                    choice = 'controller'
                    chosen = True
                else:
                    print("No 2nd press")
                    choice = 'silencer'
                    chosen = True
            else:
                i += 1
                sleep(0.01)
        GPIO.output(redLED, GPIO.LOW)
        if (choice == 'controller'):
            print("Starting the controller demo...")
            controllerdemo.mainloop()
            
        elif (choice == 'silencer'):
            print("Starting Silencer...")
            silencer.__main__()
            
            #silencer.main()

choose_your_weapon.go()
jb.stop_all()
