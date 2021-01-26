import json
from dataclasses import dataclass

class AquaPiSetting():
	#evtl Später ändern zum Dictionary!
	
	def __init__(self,_plantName:str,_plantHumidityString:str,_motorOnTimeString:str,_intervall_sec:int):
		self._plantName = _plantName
		self._plantHumidityString = _plantHumidityString
		self._motorOnTimeString = _motorOnTimeString
		self._intervall_sec = _intervall_sec
		
	def UpdateSetting(self,_plantName:str,_plantHumidityString:str,_motorOnTimeString:str,_intervall_sec:int):
		self._plantName = _plantName
		self._plantHumidityString = _plantHumidityString
		self._motorOnTimeString = _motorOnTimeString
		self._intervall_sec = _intervall_sec
	
	#Used for saving and loading the settings to and from a file
	def Serialize(self):
		return json.dumps(self.__dict__)
		
	#used for the transmission of the settings to the arduino	
	def ReturnArduinoSetting(self):
		return {"ph":AquaPiLookUpTable.GetAnalogHumidityByKey(self._plantHumidityString),"mt":AquaPiLookUpTable.GetMotorOnTimeByKey(self._motorOnTimeString)}
	
	# Getter Methods for private variables. No Setter implemented. Has to be done using updateSetting()	
	@property
	def PlantName(self):
		return self._plantName
	
	@property
	def PlantHumidityString(self):
		return self._plantHumidityString
	
	@property
	def PlantHumidityAnalog(self):
		return AquaPiLookUpTable.GetAnalogHumidityByKey(self._plantHumidityString)
	
	@property
	def MotorOnTimeString(self):
		return self._motorOnTimeString
	
	@property
	def MotorOnTime_ms(self):
		return AquaPiLookUpTable.GetMotorOnTimeByKey(self._motorOnTimeString)
	
	@property
	def Intervall_sec(self):
		return self._intervall_sec
	
	@Intervall_sec.setter
	def Intervall_sec(self, value):
		self._intervall_sec = value
		
	@MotorOnTimeString.setter
	def MotorOnTimeString(self, value):
		self._motorOnTimeString = value
		
	@PlantHumidityString.setter
	def PlantHumidityString(self, value):
		self._plantHumidityString = value
		
	@PlantName.setter
	def PlantName(self, value):
		self._plantName = value

#with dataclass, no property can be changed.
@dataclass(frozen=True)		
class AquaPiLookUpTable():
	
	@staticmethod
	def GetAnalogHumidityByKey(key):
		humiditySensorPlant = {"Wet":300,"Medium":350,"Dry":400}
		#else bedingung noch checken
		if key in humiditySensorPlant:
			return humiditySensorPlant[key]
	
	@staticmethod
	def GetAnalogWaterLevelByKey(key):
		waterLevelTank={"Full":320,"Medium":150,"Empty":20}
		#else bedingung noch checken
		if key in waterLevelTank:
			return waterLevelTank[key]
	
	@staticmethod
	def GetMotorOnTimeByKey(key):
		motorOnTime_ms ={"Long":4000,"Medium":2500,"Short":1000}
		#else bedingung noch checken
		if key in motorOnTime_ms:
			return motorOnTime_ms[key]
