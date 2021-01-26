import json

class AquaPiMessage():
	def __init__(self,messageType:str):
		self.mst = messageType
	
	def Serialize(self):#Can be called by child classes
		startDelimiter = "<"
		endDelimiter =">"
		message = str(startDelimiter + json.dumps(self.__dict__) + endDelimiter)
		return json.dumps(message)
		
class AquaPiMessage_Command(AquaPiMessage):
	def __init__(self,command:str):
		super().__init__("CMD")
		self.cmd = command
		#possible commands - Same Size and short for memory optimization at Arduino side!
		#STO - Stop AquaPi
		#RUN - Start Arduino
		#SSV - Send Sensor Values
		#WON - Watering On
		#WOF - Watering Off
		#ACT - Act Upon Sensor Values
		#STS - Send status
		#ALV - Request Alive Signal
		#USV - Update Sensor Values
		
class AquaPiMessage_Setting(AquaPiMessage):
	def __init__(self,setting:dict):
		super().__init__("STG")
		self.stg = setting
