''' Throughout my journey of learning to program the robot 'Joe', I will be doing my best to thoroughly document and comment
everything so that it is easy for others to understand. '''

# Created by Joe on 3/16/21
# For documentation please visit: 
# https://docs.wpilib.org/en/stable/ 
# https://robotpy.readthedocs.io/projects/wpilib/en/stable/index.html
# https://github.com/Team-753/2020RobotCode
# https://github.com/jserra99/Team-753

# Importing necessary modules
import json # To parse through the config.json file
import wpilib # Duh...
from wpilib import controller # To recieve and intepret user input from various devices
from networktables import NetworkTables # Not completely sure on what this does quite yet but I know that its important...

class myRobot(wpilib.TimedRobot): # The main robot class which controls everything, this is a key aspect of OOP
    def robotInit(self): # The first function that is called when it's parent class is called
        pass
