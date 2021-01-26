# my_states.py
import time as time
from menuState import MenuState
import string
import subprocess
import psutil

# Start of our states
class StartUp(MenuState):
    def __init__(self, lcd, version):
        super().__init__(lcd)
        self.showStartUpScreen(3, version)
    
    """Show Logo and wait""" 
    def showStartUpScreen(self,interval, version):
		
        self._lcd.clear()
        self._lcd.home()
        self._lcd.message("     AquaPi\n")
        self._lcd.message("   Version " + str(version) + "\n")
        time.sleep(interval)
        self._lcd.clear()
        self._lcd.home()
        self._lcd.message("   Created by\n")
        self._lcd.message("  Sascha Kirch\n")
        time.sleep(interval)
        self.showIpAdress()
        time.sleep(interval) 
        
    def on_event(self, event):
        if (event == 'start_menu'):
            return Main(self._lcd)
        return self
        
class Main(MenuState):
    
    def __init__(self, lcd):
        super().__init__(lcd)
        if(MenuState.running):
            self._menuEntries[0] = "Stop"
        else:
            self._menuEntries[0] = "Start"
        self._menuEntries[1] = "Setting"
        self._menuEntries[2] = "Help"
        self._menuEntries[3] = "Status"
        self.showMenu_4x4()
    
    def showTerminationRequest(self):
        self._lcd.clear()
        self._lcd.home()
        self._lcd.message("Request received\n")
        self._lcd.message("terminating...\n") 
            
    def on_event(self, event):
        self._response = ""
        
        if (event == 'up'):
            self.setCursor(MenuState.cursor[0],0)
        elif (event == 'down'):
            self.setCursor(MenuState.cursor[0],1)
        elif (event == 'right'):
            self.setCursor(7, MenuState.cursor[1])
        elif (event == 'left'):
            self.setCursor(0, MenuState.cursor[1])
        elif (event == 'rigth_bumper_pressed'):
            self.showIpAdress()
        elif (event == 'rigth_bumper_released'):
            self.showMenu_4x4()
        elif (event == 'termination_requested'):
            self.showTerminationRequest()
        elif (event == 'termination_finalized'):
            self.showMenu_4x4()
        elif (event == 'reboot_requested'):
            self.showRebootMessage()
            self._response = "reboot"
        elif (event == 'button_A_pressed'):
            if(MenuState.cursor == [0, 0]):
                if(not MenuState.running):
                    self._response = "start"
                    self._menuEntries[0] = "Stop"
                    MenuState.running = True
                    self.showMenu_4x4()
                else:
                    self._response = "stop"
                    self._menuEntries[0] = "Start"
                    MenuState.running = False
                    self.showMenu_4x4()
            elif(MenuState.cursor == [0, 1]):
                return Help(self._lcd) 
            elif(MenuState.cursor == [7, 0]):
                MenuState.cursor = [0,0]
                return Setting(self._lcd) 
            elif(MenuState.cursor == [7, 1]):
                return Status(self._lcd) 

        return self


class Setting(MenuState):
    
    def __init__(self, lcd):
        super().__init__(lcd)
        self._menuEntries[0] = "Plant"
        self._menuEntries[1] = "Humidity"
        self._menuEntries[2] = "Cycle"
        self._menuEntries[3] = "Motor"
        self.showMenu_4x4()
        
    def on_event(self, event):
        self._response = ""
        
        if (event == 'up'):
            self.setCursor(MenuState.cursor[0],0)
        elif (event == 'down'):
            self.setCursor(MenuState.cursor[0],1)
        elif (event == 'right'):
            self.setCursor(7, MenuState.cursor[1])
        elif (event == 'left'):
            self.setCursor(0, MenuState.cursor[1])
        elif (event == 'rigth_bumper_pressed'):
            self.showIpAdress()
        elif (event == 'rigth_bumper_released'):
            self.showMenu_4x4()
        elif (event == 'reboot_requested'):
            self.showRebootMessage()
            self._response = "reboot"
        elif (event == 'button_A_pressed'):
            if(MenuState.cursor == [0, 0]):
                 return ChangeSettingPlant(self._lcd)   
            elif(MenuState.cursor == [0, 1]):
                return ChangeSettingCycle(self._lcd)
            elif(MenuState.cursor == [7, 0]):
                return ChangeSettingHumidity(self._lcd) 
            elif(MenuState.cursor == [7, 1]):
                return ChangeSettingMotor(self._lcd)
        elif (event == 'button_B_pressed'):
            MenuState.cursor = [7,0] #set to setting position. looks better.
            return Main(self._lcd)
        return self

class ChangeSetting(MenuState):
    def __init__(self, lcd):
        super().__init__(lcd)
        self._lcd.clear()
        self._lcd.home()
        
    def UpdateScreen(self, messageString:str):
        self._lcd.set_cursor(0,1)
        self._lcd.message(" "*16)
        self._lcd.set_cursor(0,1)
        self._lcd.message(" " + messageString)
        
class ChangeSettingCycle(ChangeSetting):
    def __init__(self, lcd):
        super().__init__(lcd)
        self._value = MenuState.setting.Intervall_sec
        self._lcd.message("Cycle Time [sec]:\n")
        self._lcd.message(" " + str(self._value))      
        
    def on_event(self, event):
        self._response = ""
        if (event == 'up'):
            self._value = min( self._value + 1, 999)
            self.UpdateScreen(str(self._value))
        elif (event == 'down'):
            self._value = max( self._value - 1, 0)
            self.UpdateScreen(str(self._value))
        elif (event == 'up_fast'):
            self._value = min( self._value + 10, 999)
            self.UpdateScreen(str(self._value))
        elif (event == 'down_fast'):
            self._value = max( self._value - 10, 0)
            self.UpdateScreen(str(self._value))    
        elif (event == 'button_A_pressed'):
            self._response = "update:" + "_intervall_sec:" + str(self._value)
            self.UpdateScreen(str(self._value) + "->Set<-")
        elif (event == 'button_B_pressed'):
            return Setting(self._lcd)
        elif (event == 'reboot_requested'):
            self.showRebootMessage()
            self._response = "reboot"
        return self
        
class ChangeSettingMotor(ChangeSetting):
    def __init__(self, lcd):
        super().__init__(lcd)
        self._values = ["Short","Medium","Long"]
        self._index = self._values.index(MenuState.setting.MotorOnTimeString)
        self._lcd.message("Motor On Time:\n")
        self._lcd.message(" " + self._values[self._index])
        
    def on_event(self, event):
        self._response = ""
        if (event == 'up'):
            self._index = min( self._index + 1, len(self._values) - 1)
            self.UpdateScreen(str(self._values[self._index]))
        elif (event == 'down'):
            self._index = max( self._index - 1, 0)
            self.UpdateScreen(str(self._values[self._index]))
        elif (event == 'button_A_pressed'):
            self._response = "update:" + "_motorOnTimeString:" + str(self._values[self._index])
            self.UpdateScreen(str(self._values[self._index]) + "->Set<-")
        elif (event == 'button_B_pressed'):
            return Setting(self._lcd)
        elif (event == 'reboot_requested'):
            self.showRebootMessage()
            self._response = "reboot"
        return self
        
class ChangeSettingHumidity(ChangeSetting):
    def __init__(self, lcd):
        super().__init__(lcd)
        self._values = ["Dry","Medium","Wet"]
        self._index = self._values.index(MenuState.setting.PlantHumidityString)
        self._lcd.message("Plant Humidity:\n")
        self._lcd.message(" " + self._values[self._index])
        
    def on_event(self, event):
        self._response = ""
        if (event == 'up'):
            self._index = min( self._index + 1, len(self._values) - 1)
            self.UpdateScreen(str(self._values[self._index]))
        elif (event == 'down'):
            self._index = max( self._index - 1, 0)
            self.UpdateScreen(str(self._values[self._index]))    
        elif (event == 'button_A_pressed'):
            self._response = "update:" + "_plantHumidityString:" + str(self._values[self._index])
            self.UpdateScreen(str(self._values[self._index]) + "->Set<-")
        elif (event == 'button_B_pressed'):
            return Setting(self._lcd)
        elif (event == 'reboot_requested'):
            self.showRebootMessage()
            self._response = "reboot"
        return self
        
class ChangeSettingPlant(ChangeSetting):
    def __init__(self, lcd):
        super().__init__(lcd)
        self._asciiString = " " + string.ascii_letters
        self._index = 1
        self._value = MenuState.setting.PlantName
        self._lcd.message("Plant Name:\n")
        self._lcd.message(" " + self._value)
        self._lcd.set_cursor(1,1)
        self._lcd.blink(True)   
        
    def __del__(self):
        self._lcd.blink(False)
        
    def on_event(self, event):
        self._response = ""
        if (event == 'up'):
            if(self._index > len(self._value)):
                letterIndex = 0
            else:
                letterIndex = self._asciiString.index(self._value[self._index-1])
            letterIndex = min(letterIndex + 1, len(self._asciiString) - 1)
            self._value = self._value[:self._index-1] + self._asciiString[letterIndex] + self._value[self._index:]
            self.UpdateScreen(self._value)
            self._lcd.set_cursor(self._index,1) #when writing, curser is moved -> set back
        elif (event == 'down'):
            if(self._index > len(self._value)):
                letterIndex = 0
            else:
                letterIndex = self._asciiString.index(self._value[self._index-1])
            letterIndex = max(letterIndex - 1, 0)
            self._value = self._value[:self._index-1] + self._asciiString[letterIndex] + self._value[self._index:]
            self.UpdateScreen(self._value)
            self._lcd.set_cursor(self._index,1) #when writing, curser is moved -> set back 
        elif (event == 'up_fast'):
            if(self._index > len(self._value)):
                letterIndex = 0
            else:
                letterIndex = self._asciiString.index(self._value[self._index-1])
            letterIndex = min(letterIndex + 5, len(self._asciiString) - 1)
            self._value = self._value[:self._index-1] + self._asciiString[letterIndex] + self._value[self._index:]
            self.UpdateScreen(self._value)
            self._lcd.set_cursor(self._index,1) #when writing, curser is moved -> set back
        elif (event == 'down_fast'):
            if(self._index > len(self._value)):
                letterIndex = 0
            else:
                letterIndex = self._asciiString.index(self._value[self._index-1])
            letterIndex = max(letterIndex - 5, 0)
            self._value = self._value[:self._index-1] + self._asciiString[letterIndex] + self._value[self._index:]
            self.UpdateScreen(self._value)
            self._lcd.set_cursor(self._index,1) #when writing, curser is moved -> set back 
        elif (event == 'left'):
            self._index = max( self._index - 1, 1)
            self._lcd.set_cursor(self._index,1)
        elif (event == 'right'):
            self._index = min( self._index + 1, 8)
            self._lcd.set_cursor(self._index,1)
        elif (event == 'button_A_pressed'):
            self._response = "update:" + "_plantName:" + str(self._value.strip())
            self.UpdateScreen(str(self._value.strip()) + "->Set<-")
        elif (event == 'button_B_pressed'):
            return Setting(self._lcd)
        elif (event == 'reboot_requested'):
            self.showRebootMessage()
            self._response = "reboot"
        return self
        
class Help(MenuState):
    def __init__(self, lcd):
        super().__init__(lcd)
        self.showHelp()
    
    def showHelp(self):
        self._lcd.clear()
        self._lcd.home()
        self._lcd.message("For help visit:\n")
        self._lcd.message("<IP>/Help.php")
        
    def on_event(self, event):
        self._response = ""
        if event == 'button_B_pressed':
            MenuState.cursor = [0,1] #set to setting position. looks better.
            return Main(self._lcd)
        elif (event == 'rigth_bumper_pressed'):
            self.showIpAdress()
        elif (event == 'rigth_bumper_released'):
            self.showHelp()
        elif (event == 'reboot_requested'):
            self.showRebootMessage()
            self._response = "reboot"
        return self
                
class Status(MenuState):
    def __init__(self, lcd):
        super().__init__(lcd)
        self.prepareStatus()
        self.showStatus_4x4()
        
    def prepareStatus(self):
        cpuUsage = 0
        cpuTemp = 0
        networkStatus = "NOK"
        arduinoStatus = "NOK"
        
        # check if Arduino is connected
        try:
            lsusb = subprocess.Popen(('lsusb'), stdout=subprocess.PIPE)
            subprocess.check_output(('grep', 'Arduino'), stdin=lsusb.stdout)
            lsusb.wait()
            arduinoStatus = "OK"
        except:
            #No Arduino at USB found USB 
            pass
        
        #get temperature    
        try:
            cpuTemp = ((subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, encoding="ascii")).stdout.split("=")[1]).split(".")[0]
        except:
            pass
        
        #ping router to check if connected to network
        try:
            ping = subprocess.Popen(('ping', '192.168.0.1','-c','1'), stdout=subprocess.PIPE)
            subprocess.check_output(('grep', '0% packet loss'), stdin=ping.stdout)
            ping.wait()
            networkStatus = "OK"
        except:
            pass

        cpuUsage = int(psutil.cpu_percent(interval=1))
                
        self._menuEntries[0] = "cpu%:" + str(cpuUsage)
        self._menuEntries[1] = "NET:" + str(networkStatus)
        self._menuEntries[2] = "cpuT:" + str(cpuTemp)
        self._menuEntries[3] = "UNO:" + str(arduinoStatus)
        
    def on_event(self, event):
        if event == 'button_B_pressed':
            return Main(self._lcd)
        elif (event == 'rigth_bumper_pressed'):
            self.showIpAdress()
        elif (event == 'rigth_bumper_released'):
            self.showStatus_4x4()
        elif (event == 'reboot_requested'):
            self.showRebootMessage()
            self._response = "reboot"
        return self
