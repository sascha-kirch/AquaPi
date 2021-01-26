import threading
import time as time
import RPi.GPIO as GPIO 
from AquaPiArduino import *
import mysql.connector
from datetime import datetime
import traceback
from uuid import getnode as get_mac
import subprocess
import socket

class AquaPiArduinoThread(threading.Thread):
	def __init__(self, setting):
		threading.Thread.__init__(self)
		self._setting = setting
		self._terminationRequest = False
		self._status = "Not Available"
		self.deamon = True
		self.start()
		self._arduino = None
		
	def run(self):
		self._terminationRequest = False
		while(not self._terminationRequest):
			self.RunAquaPiArduinoCycle()
			#delay sligthly longer as set by Interval_sec -> loop and if adds some execution time.
			for i in range(0, self._setting.Intervall_sec):
				if(self._terminationRequest):
					break
				else:
					time.sleep(1)
	
	def Terminate(self):
		self._terminationRequest = True

	def RunAquaPiArduinoCycle(self):
		self._arduino = AquaPiArduino(self._setting)
		arduinoCycleAcitveLedPin = 3
		
		#Setup GPIO. Indicates Active cycle of the Arduino
		GPIO.setup(arduinoCycleAcitveLedPin, GPIO.OUT)
		GPIO.output(arduinoCycleAcitveLedPin, GPIO.HIGH)
		
		self._arduino.Up()
		if(self._arduino.IsUp):
			try:
				self._arduino.RequestAlive()
				self._arduino.Start()
				self._arduino.SendConfig()
				self._arduino.UpdateSensorValues()
				sensorValuesDict = self._arduino.RequestSensorValues()
				self._arduino.ActUponSensorValues()
				self._status = self._arduino.RequestStatus()
				self._arduino.Stop()
				
				#Update DataBase
				if(self.ValidateSensorValueDict(sensorValuesDict)):
					self.UpdateDataBase(sensorValuesDict,self._status)
							
			except TransmissionFailedError:
				print(traceback.print_exc())
			except Exception:
				print(traceback.print_exc())
			finally:
				self._arduino.Down()
				GPIO.output(arduinoCycleAcitveLedPin, GPIO.LOW)

	def ValidateSensorValueDict(self,sensorValueDict:dict):
		if(('humidityPlant' in sensorValueDict) & ('humidityRoom' in sensorValueDict) & ('temperatureRoom' in sensorValueDict) & ('waterLevel' in sensorValueDict)):
			return True
		else:
			return False
			
	def UpdateDataBase(self,sensorValuesDict:dict, sensorStatus:str):
		#create database object
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="aquapi",
		  passwd="aquapi",
		  database="AquaPiDatabase"
		)
		
		mac = get_mac()
		macHex = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))

		#create cursor to send queries
		myCursor = mydb.cursor()

		#check if client is registered and register if not
		sql ='SELECT macAdress FROM Client WHERE macAdress = "' + macHex +'"'
		myCursor.execute(sql)
		
		#result retrieved from the cursor
		myResult = myCursor.fetchall()
		
		if(len(myResult) == 0):
			hostname = socket.gethostname()
			ipAdress = (subprocess.run(["hostname", "-I"], capture_output=True, encoding="ascii")).stdout.split(" ")[0]
			sql ='INSERT INTO Client (macAdress, ipAdress, hostName) VALUES(%s,%s,%s)'
			val = (macHex, str(ipAdress), str(hostname))
			myCursor.execute(sql, val)
			mydb.commit()
		
		timeStamp = datetime.now()
		
		#sql query for inserting a watering process
		if(sensorStatus=="WATERED"):
			sql = "INSERT INTO WateringProcess (wateringProcessId, timeStamp, clientMacAdressRefference) VALUES(NULL,%s,%s)"
			val = (timeStamp,macHex)
			myCursor.execute(sql, val)	
			mydb.commit()
			
		#sql querry to insert data into a table.
		sql = "INSERT INTO SensorMeasurement (sensorMeasurementId, plantHumidity, roomHumidity, roomTemperature, waterTankLevel, timeStamp, clientMacAdressRefference) VALUES(NULL,%s,%s,%s,%s,%s,%s)"
		val = (sensorValuesDict['humidityPlant'],sensorValuesDict['humidityRoom'],sensorValuesDict['temperatureRoom'],sensorValuesDict['waterLevel'],timeStamp,macHex)
		myCursor.execute(sql, val)
		mydb.commit()
		
	@property
	def Status(self):
		return self._status
