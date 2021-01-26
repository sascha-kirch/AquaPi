import RPi.GPIO as GPIO 
import Adafruit_CharLCD as LCD
import time as time
from AquaPiMenuStates import *

class AquaPiDisplay():
	def __init__(self, version, setting):
		# Raspberry Pi pin setup (GPIO Numbers!!!)
		lcd_rs = 23
		lcd_en = 24
		lcd_d4 = 25
		lcd_d5 = 8
		lcd_d6 = 7
		lcd_d7 = 1
		lcd_backlight = 2	

		# Define LCD column and row size for 16x2 LCD.
		lcd_columns = 16
		lcd_rows = 2
		
		#Initiate GPIO
		GPIO.setwarnings(False)

		#initiate LCD
		self._lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
		self._lcd.blink(False)
		self._lcd.show_cursor(False)
		
		#AquaPi Settings
		self._setting = setting
		MenuState.setting = setting
		
		# Start with a default state.
		self._state = StartUp(self._lcd, version)
		
		#start the main menu
		self._state = self._state.on_event('start_menu')
		
	def on_event(self, event):
        # The next state will be the result of the on_event function.
		self._state = self._state.on_event(event)
	
	#Getter Attributes
	@property
	def Lcd(self):
		return self._lcd
		
	@property
	def State(self):
		return self._state
		
	@property
	def Setting(self):
		return self._setting
	
	#Setter Attributes
	@Setting.setter
	def Setting(self,value):
		self._setting = value
		MenuState.setting = value

