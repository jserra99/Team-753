import wpilib
import math
import rev
from wpilib import controller as controller
from SwerveModule import SwerveModule

class DriveTrain:
	robotLength = 25.25
	robotWidth = 21
	diagonal = math.hypot(robotLength,robotWidth)
	
	def __init__(self, offsets):
		self.frontLeft = SwerveModule(7,8,0,offsets["Front Left"],"Front Left") #drive ID, turn ID, encoder ID, encoder offset
		self.frontRight = SwerveModule(1,2,2,offsets["Front Right"],"Front Right")
		self.rearLeft = SwerveModule(5,6,3,offsets["Rear Left"],"Rear Left")
		self.rearRight = SwerveModule(3,4,1,offsets["Rear Right"], "Rear Right")
		
	def move(self,x,y,z):
		'''wpilib.SmartDashboard.putNumber("x",x)
		wpilib.SmartDashboard.putNumber("y",y)
		wpilib.SmartDashboard.putNumber("z",z)'''
		
		a = y - z*self.robotLength/self.diagonal
		b = y + z*self.robotLength/self.diagonal
		c = x - z*self.robotWidth/self.diagonal
		d = x + z*self.robotWidth/self.diagonal
		
		frontLeftSpeed = math.hypot(b,d)
		frontRightSpeed = math.hypot(a,d) #used to be b and c
		rearLeftSpeed = math.hypot(b,c) #used to be a and d
		rearRightSpeed = math.hypot(a,c)
		
		frontLeftAngle = math.atan2(b,d)*180/math.pi #returns -180 to 180
		frontRightAngle = math.atan2(a,d)*180/math.pi #used to be b and c
		rearLeftAngle = math.atan2(b,c)*180/math.pi #used to be a and d
		rearRightAngle = math.atan2(a,c)*180/math.pi
		
		maxSpeed = max(frontLeftSpeed,frontRightSpeed,rearLeftSpeed,rearRightSpeed)
		if maxSpeed > 1:
			frontLeftSpeed /= maxSpeed
			frontRightSpeed /= maxSpeed
			rearLeftSpeed /= maxSpeed
			rearRightSpeed /= maxSpeed
		
		self.frontLeft.move(frontLeftSpeed,frontLeftAngle) #speed, angle
		self.frontRight.move(frontRightSpeed,frontRightAngle)
		self.rearLeft.move(rearLeftSpeed,rearLeftAngle)
		self.rearRight.move(rearRightSpeed,rearRightAngle)
		
	def stationary(self):
		self.frontLeft.stationary()
		self.frontRight.stationary()
		self.rearLeft.stationary()
		self.rearRight.stationary()
		
	def zeroEncoders(self):
		self.stopTurn()
		self.brake()
		
		fLAbsolute = []
		fRAbsolute = []
		rLAbsolute = []
		rRAbsolute = []
		for i in range(6):
			fLPosition = self.frontLeft.returnAbsolutes()
			fRPosition = self.frontRight.returnAbsolutes()
			rLPosition = self.rearLeft.returnAbsolutes()
			rRPosition = self.rearRight.returnAbsolutes()
			
			fLAbsolute.append(fLPosition)
			fRAbsolute.append(fRPosition)
			rLAbsolute.append(rLPosition)
			rRAbsolute.append(rRPosition)
		fLPosition = sum(fLAbsolute)/len(fLAbsolute)
		fRPosition = sum(fRAbsolute)/len(fRAbsolute)
		rLPosition = sum(rLAbsolute)/len(rLAbsolute)
		rRPosition = sum(rRAbsolute)/len(rRAbsolute)
		
		self.frontLeft.zeroEncoder(fLPosition)
		self.frontRight.zeroEncoder(fRPosition)
		self.rearLeft.zeroEncoder(rLPosition)
		self.rearRight.zeroEncoder(rRPosition)
		
	def coast(self):
		self.frontLeft.coast()
		self.frontRight.coast()
		self.rearLeft.coast()
		self.rearRight.coast()
		
	def brake(self):
		self.frontLeft.brake()
		self.frontRight.brake()
		self.rearLeft.brake()
		self.rearRight.brake()
		
	def stopTurn(self):
		self.frontLeft.stopTurn()
		self.frontRight.stopTurn()
		self.rearLeft.stopTurn()
		self.rearRight.stopTurn()
		
	def checkEncoders(self):
		self.frontLeft.checkEncoders()
		self.frontRight.checkEncoders()
		self.rearLeft.checkEncoders()
		self.rearRight.checkEncoders()

	def getEncoderVals(self):
		return self.frontLeft.encoderBoundedPosition(), self.frontRight.encoderBoundedPosition(), self.rearLeft.encoderBoundedPosition(), self.rearRight.encoderBoundedPosition()
		
	def averageWheelPosition(self):
		frontLeftX, frontLeftY = self.frontLeft.autoPosition()
		frontRightX, frontRightY = self.frontRight.autoPosition()
		rearLeftX, rearLeftY = self.rearLeft.autoPosition()
		rearRightX, rearRightY = self.rearRight.autoPosition()
		
		averageX = (abs(frontLeftX)+abs(frontRightX)+abs(rearLeftX)+abs(rearRightX))/4
		averageY = (abs(frontLeftY)+abs(frontRightY)+abs(rearLeftY)+abs(rearRightY))/4
		return(averageX,averageY)
		
	def frontLeftPosition(self):
		position = self.frontLeft.basicPosition()
		return(position)
		