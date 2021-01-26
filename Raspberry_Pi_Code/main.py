import time as time
import xbox
import subprocess
import json
import traceback
import RPi.GPIO as GPIO 
from AquaPiSetting import *
from AquaPiDisplay import *
from pathlib import Path
from AquaPiArduinoThread import AquaPiArduinoThread

#Internal Settings & constants
version = 1.0
SETTING_FILE = Path("/etc/AquaPi/setting.txt")
standardSetting = AquaPiSetting("Planty","Wet","Medium",300)
setting = None

arduinoActive = False
aquaPiArduinoThread = None

def LoadSettings():
    global setting
    #check if setting file is available and load it, if not create and load.
    try:
        if (SETTING_FILE.is_file()):
            fileContent=""
            with open(SETTING_FILE,'rt') as f:
                fileContent = f.read()
            setting = AquaPiSetting(**json.loads(fileContent))
        else:
            raise FileNotFoundError
    # Chatch exception if the file is not found or if the file is corrupted and can not be loaded by json.loads()
    except:
        subprocess.run(["sudo","mkdir", SETTING_FILE.parent])
        subprocess.run(["sudo","touch", SETTING_FILE])
        subprocess.run(["sudo","chown", "pi:pi",SETTING_FILE])
        with open(SETTING_FILE,'wt') as f:
            f.write(standardSetting.Serialize())
        setting = standardSetting    

def EvaluateStateResponse(response:str):
    global aquaPiArduinoThread
    global setting
    global SETTING_FILE
    if(response == ""):
        pass 
    elif(response == "start"):
        aquaPiArduinoThread = AquaPiArduinoThread(setting)
    elif(response == "stop"):
        aquaPiDisplay.on_event('termination_requested')
        aquaPiArduinoThread.Terminate()
        aquaPiArduinoThread.join()
        aquaPiDisplay.on_event('termination_finalized')
    elif(response.startswith("update")):
        responseArray = response.split(":")

        if(responseArray[1] == '_intervall_sec'):
            setting.Intervall_sec = int(responseArray[2])
        elif(responseArray[1] == '_motorOnTimeString'):
            setting.MotorOnTimeString = str(responseArray[2])
        elif(responseArray[1] == '_plantHumidityString'):
            setting.PlantHumidityString = str(responseArray[2])
        elif(responseArray[1] == '_plantName'):
            setting.PlantName = str(responseArray[2])

        with open(SETTING_FILE,'wt') as f:
            f.write(setting.Serialize())
    elif(response == "reboot"):
        time.sleep(3)
        subprocess.run(["sudo", "reboot", "now"])
    

def run():
    while not joystick.leftThumbstick():
        #Move Cursor Up / Down
        if ((joystick.leftY() > 0.5) | joystick.dpadUp()):
            aquaPiDisplay.on_event('up')
            EvaluateStateResponse(aquaPiDisplay.State.Response)
            while((joystick.leftY() > 0.5) | joystick.dpadUp()): #used for debouncing!
                pass
        elif ((joystick.leftY() < -0.5) | joystick.dpadDown()):
            aquaPiDisplay.on_event('down')
            EvaluateStateResponse(aquaPiDisplay.State.Response)
            while((joystick.leftY() < -0.5) | joystick.dpadDown()): #used for debouncing!
                pass
    
        #Move Cursor left / right
        elif ((joystick.leftX() > 0.5) | joystick.dpadRight()):
            aquaPiDisplay.on_event('right')
            EvaluateStateResponse(aquaPiDisplay.State.Response)
            while((joystick.leftX() > 0.5) | joystick.dpadRight()): #used for debouncing!
                pass
        elif ((joystick.leftX() < -0.5) | joystick.dpadLeft()):
            aquaPiDisplay.on_event('left')
            EvaluateStateResponse(aquaPiDisplay.State.Response)
            while((joystick.leftX() < -0.5) | joystick.dpadLeft()): #used for debouncing!
                pass
        
        #Right Joystic Up/down -> for fast change
        elif ((joystick.rightY() > 0.5) ):
            while((joystick.rightY() > 0.5) ): #used for debouncing!
                aquaPiDisplay.on_event('up_fast')
                time.sleep(0.1)
        elif ((joystick.rightY() < -0.5) ):
            while((joystick.rightY() < -0.5) ): #used for debouncing!
                aquaPiDisplay.on_event('down_fast')
                time.sleep(0.1)
        
        #A-Button pressed
        elif(joystick.A()):
            aquaPiDisplay.on_event('button_A_pressed')
            while(joystick.A()): #used for debouncing!
                pass
            EvaluateStateResponse(aquaPiDisplay.State.Response)
                
        #B-Button pressed
        elif(joystick.B()):
            aquaPiDisplay.on_event('button_B_pressed')
            while(joystick.B()): #used for debouncing!
                pass
            EvaluateStateResponse(aquaPiDisplay.State.Response)
        
        #Back-Button pressed -> Restart
        elif(joystick.Back()):
            start = time.time()
            while(joystick.Back()): #used for debouncing!
                pass
            end = time.time()
            if((end-start) > 3):
                aquaPiDisplay.on_event('reboot_requested')
                EvaluateStateResponse(aquaPiDisplay.State.Response)
        
        #RB-Button pressed -> show Ip Address
        elif(joystick.rightBumper()):
            aquaPiDisplay.on_event('rigth_bumper_pressed')
            EvaluateStateResponse(aquaPiDisplay.State.Response)
            while(joystick.rightBumper()): #used for debouncing!
                pass
            aquaPiDisplay.on_event('rigth_bumper_released')
            EvaluateStateResponse(aquaPiDisplay.State.Response)


# Load Settings
LoadSettings()

#Initialize Display
aquaPiDisplay = AquaPiDisplay(version,setting)

#Instantiate the controller
joystick = xbox.Joystick()

#Runs the Menu
run()


