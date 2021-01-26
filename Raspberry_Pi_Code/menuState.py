import subprocess

class MenuState(object):
    # Class Variable, shared among all instances
    cursor = [0,0]
    setting = None
    running = False

    def __init__(self, lcd):
        self._lcd = lcd
        self._menuEntries = ["","","",""]
        self._response = ""

    def __del__(self):
        pass

    def on_event(self, event):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__
    
    def showIpAdress(self):
        self._lcd.clear()
        self._lcd.home()
        self._lcd.message("Local IP Adress:\n")
        self._lcd.message((subprocess.run(["hostname", "-I"], capture_output=True, encoding="ascii")).stdout.split(" ")[0])
	
    def showRebootMessage(self):
        self._lcd.clear()
        self._lcd.home()
        self._lcd.message("     Reboot\n")
        self._lcd.message("     AquaPi\n")
    
    def setCursor(self,col, row):
        #clear current cursor
        self._lcd.set_cursor(MenuState.cursor[0],MenuState.cursor[1])
        self._lcd.message(" ")
        
        #set cursor
        self._lcd.set_cursor(col,row)
        self._lcd.message(">")
		
        #update class properties
        MenuState.cursor[0] = col
        MenuState.cursor[1] = row
    
    def showMenu_4x4(self, showCurser = True):
        self._lcd.clear()
        self._lcd.home()
        self._lcd.set_cursor(1,0)
        self._lcd.message(self._menuEntries[0])
        self._lcd.set_cursor(8,0)
        self._lcd.message(self._menuEntries[1])
        self._lcd.set_cursor(1,1)
        self._lcd.message(self._menuEntries[2])
        self._lcd.set_cursor(8,1)
        self._lcd.message(self._menuEntries[3])
        if(showCurser):
            self.setCursor(MenuState.cursor[0], MenuState.cursor[1])
            
    def showStatus_4x4(self):
        self._lcd.clear()
        self._lcd.home()
        self._lcd.set_cursor(0,0)
        self._lcd.message(self._menuEntries[0])
        self._lcd.set_cursor(9,0)
        self._lcd.message(self._menuEntries[1])
        self._lcd.set_cursor(0,1)
        self._lcd.message(self._menuEntries[2])
        self._lcd.set_cursor(9,1)
        self._lcd.message(self._menuEntries[3])
    
    #Getter Attributes
    @property
    def Response(self):
        return self._response
