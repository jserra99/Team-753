import wpilib
import time

VictorSP = wpilib.VictorSP

wheelOne = VictorSP(1)
wheelTwo = VictorSP(2)
wheelThree = VictorSP(3)
wheelFour = VictorSP(4)
print("Spinning Wheel 4")
wheelFour.set(1)
time.sleep(5)
print("Spinning Wheel 3")
wheelThree.set(1)
time.sleep(5)
print("Stopping All Wheels")
wheelFour.set(0)
wheelThree.set(0)
