import wpilib
import time

VictorSP = wpilib.VictorSP

wheelOne = VictorSP(1)
wheelTwo = VictorSP(2)
wheelThree = VictorSP(3)
wheelFour = VictorSP(4)

wheelFour.set(1)
time.sleep(5)
wheelThree.set(1)
time.sleep(5)
wheelFour.set(0)
wheelThree.set(0)
