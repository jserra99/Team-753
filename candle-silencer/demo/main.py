''' The file which handles which script is executed and how that is done.'''
import jobot as jb
import RPi.GPIO as GPIO
import controllerdemo
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

        led_thread = Thread(target = choose_your_weapon.passiveLED)
        led_thread.start()
        jb.ready()
        print("Awaiting button press...")
        while (chosen == False):
            button_state = GPIO.input(startButton)
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
                sleep(0.01)
        if (choice == 'controller'):
            print("Starting the controller demo...")
            controllerdemo.mainloop()
            
        elif (choice == 'silencer'):
            print("Starting Silencer...")
            #silencer.main()
    

    def passiveLED():
        while (chosen == False):
            GPIO.output(redLED, GPIO.HIGH)
            sleep(1)
            GPIO.output(redLED, GPIO.LOW)
            sleep(1)
        GPIO.output(redLED, GPIO.LOW)

while True:
    choose_your_weapon.go()
