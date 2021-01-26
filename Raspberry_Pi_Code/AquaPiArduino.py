import RPi.GPIO as GPIO 
from AquaPiMessage import *
import traceback
import serial
import time as time
import json
import re

class AquaPiArduinoException(Exception):
	pass

class  TransmissionFailedError(AquaPiArduinoException):
	pass
	
class AquaPiArduino():

	def __init__(self, setting):
		self._isUp = False
		self._configured = False
		self._setting = setting
		self._arduinoEnablePin = 27
		self._retransmissionLimit = 3
		self._pattern = r'^[<].*[>]$'
		GPIO.setup(self._arduinoEnablePin, GPIO.OUT)
		GPIO.output(self._arduinoEnablePin, GPIO.LOW)
		
		# Initialize Serial Interface
		self._ser = serial.Serial('/dev/ttyACM0',9600,timeout = 7)
	
	def __del__(self):
		# Ensure serial connection is closed
		if(self._ser.is_open):
			self._ser.close()
			
		# Ensure enable pin is low
		self.Down()
		
	@property
	def IsUp(self):
		return self._isUp
		
	def Up(self):
		GPIO.output(self._arduinoEnablePin, GPIO.HIGH)
		time.sleep(3) #später noch durch einen Pin kennzeichnen!!
		self._isUp = True

	def Down(self):
		GPIO.output(self._arduinoEnablePin, GPIO.LOW)
		self._isUp = False
	
	def Start(self):
		return self.CommandMessageDelegate(AquaPiMessage_Command,"RUN")
	
	def Stop(self):
		return self.CommandMessageDelegate(AquaPiMessage_Command,"STO")
	
	def RequestAlive(self):
		return self.CommandMessageDelegate(AquaPiMessage_Command,"ALV")
	
	def UpdateSensorValues(self):
		return self.CommandMessageDelegate(AquaPiMessage_Command,"USV")
		
	def ActivateWatering(self):
		return self.CommandMessageDelegate(AquaPiMessage_Command,"WON")
		
	def ActUponSensorValues(self):
		return self.CommandMessageDelegate(AquaPiMessage_Command,"ACT")
		
	def DeactivateWatering(self):
		return self.CommandMessageDelegate(AquaPiMessage_Command,"WOF")
		
	def SendConfig(self):
		return self.CommandMessageDelegate(AquaPiMessage_Setting,self._setting.ReturnArduinoSetting())
	
	def RequestSensorValues(self):
		return self.RequestMessageDelegate(AquaPiMessage_Command,"SSV",'val')
		
	def RequestStatus(self):
		return self.RequestMessageDelegate(AquaPiMessage_Command,"STS",'sid')
	
	def RequestMessageDelegate(self, messageFunc, arg:str, requestedParameter:str):
		ack = 0
		requestedValue = None
		if(self._ser.is_open):
			try:
				for attempt in range(0,self._retransmissionLimit):
					if(attempt >0):
						self._ser.reset_output_buffer()
						time.sleep(1)
						self._ser.reset_input_buffer()
						time.sleep(1)
					self._ser.write(bytes(messageFunc(arg).Serialize(),"ascii"))
					line = self._ser.readline().decode('ascii').rstrip()
					matchedMessage = re.search(self._pattern,line)
					if(matchedMessage):
						message = line[matchedMessage.start()+1:matchedMessage.end()-1]
						decodedMessage = json.loads(message)
						if("ack" in decodedMessage):
							ack = decodedMessage['ack']
						else:
							continue
						if(ack == "1"):
							line = self._ser.readline().decode('ascii').rstrip()
							statusMessage = re.search(self._pattern,line)
							if(statusMessage):
								message = line[statusMessage.start()+1:statusMessage.end()-1]
								decodedMessage = json.loads(message)
								if(requestedParameter in decodedMessage):
									requestedValue = decodedMessage[requestedParameter]
								else:
									continue
								return requestedValue
							else:
								continue	
						else:
							continue		
					else:
							continue	
				raise TransmissionFailedError("No Acknoledge after 3 attempts.")
			except TransmissionFailedError:
				print(traceback.print_exc())
				raise
			except Exception:
				print(traceback.print_exc())
				raise
			
	def CommandMessageDelegate(self, messageFunc, arg:str):
		ack = 0
		if(self._ser.is_open):
			try:
				for attempt in range(0,self._retransmissionLimit):
					if(attempt > 0):
						self._ser.reset_output_buffer()
						time.sleep(1)
						self._ser.reset_input_buffer()
						time.sleep(1)
					self._ser.write(bytes(messageFunc(arg).Serialize(),"ascii"))
					line = self._ser.readline().decode('ascii').rstrip()
					matchedMessage = re.search(self._pattern,line)
					if(matchedMessage):
						message = line[matchedMessage.start()+1:matchedMessage.end()-1]
						decodedMessage = json.loads(message)
						if("ack" in decodedMessage):
							ack = decodedMessage['ack']
						else:
							continue
						if(ack == "1"):
							return True
						else:
							continue
				raise TransmissionFailedError("No Acknoledge after 3 attempts.")
			except TransmissionFailedError:
				print(traceback.print_exc())
				raise
			except Exception:
				print(traceback.print_exc())
				raise
