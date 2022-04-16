<img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/aquapi_logo.png" width="200" />

# AquaPi
AquaPi is a plant watering project using a Raspberry Pi and an Arduino Uno. The Raspberry Pi is the master device. It processes the user's input via a XBox controller, it shows a menu on the LCD display, it manages the Arduino and its connected sensors and it hosts and updates a database and a web interface. The arduino controlls the sensors and the actuators and communicates via USB with the RaspberryPi

<img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/aquapi_setup.PNG" width="600" />

## Hardware

### Electronics

The schemetic of the electronics is shown in the image bellow:
> <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/schematic.png" width="800" />

The table below shows an image of the components used for this project.
Component | Details | Image Model
------------ | ------------- | -------------
Temperature and Humidity Sensor | DHT11, 16bit |  <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/temperatur.PNG" width="150" /> 
Water level sensor | Capacitive sensor |  <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/waterlevel.PNG" width="150" /> 
Soil moisture sensor |  Capacitive sensor  | <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/moisture.PNG" width="150" /> 
Water pump |  3V and 5V, 100 liters per hour  | <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/waterpump.PNG" width="150" />
Relay |  -  | <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/relay.PNG" width="150" />
Display |  HD44780 1602 LCD Module  | <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/display.PNG" width="150" />


### Mechanics

Some of the mechanical components are crafted using CO2 laser cutter and 3D printer. The models are designed in Tinkercad and the links are provided in the table bellow:

Component | Crafted with |Tinkercad Link | Image Model
------------ | ------------- | ------------- | -------------
Cover Plate | CO2 Laser cutter| https://www.tinkercad.com/things/ephjkj1Kwn3 | <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/coverplate.png" width="250" /> 
Water tank | 3D Printer | https://www.tinkercad.com/things/as097kxnf2B | <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/watertank.PNG" width="250" /> 
Hose holder | 3D Printer | https://www.tinkercad.com/things/him38nNyUkI | <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/hoseholder.PNG" width="250" /> 
Display Frame | 3D Printer | https://www.tinkercad.com/things/j6xcOHT7CJA | <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/display_frame.PNG" width="250" />

## Software


## Database and Webinterface

A database is used to store information gathered by the sensors, to register one or more AquaPi setups and to store when the plant was watered.
The following tools are used:

Component | Used Tool / Package | Installation commadn
------------ | ------------- | -------------
Webserver | Apache2 | ``` sudo apt install apache2 -y ```
PHP| php 7.3 | ``` sudo apt install php7.3 php7.3-mbstring php7.3-mysql php7.3-curl php7.3-gd php7.3-zip -y ```
Database | MariaDB 10 | ``` sudo apt-get install mariadb-client mariadb-server ```
Database Management | PHPMyAdmin | ``` sudo apt-get install phpmyadmin ```

A webinterface is provided, to retrive the content of the database and to provide help. The design is responsive and can be used on the smartphone as well (only workes on Android, due to the API used for graphical representation)

**Desktop view AquaPi webinterface**:
> <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/webinterface_desktop.PNG" width="800" />

**Smartphone view AquaPi webinterface**:
> <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/webinterface_android.PNG" width="300" />


# Repo Stats
![](https://komarev.com/ghpvc/?username=saschakirchaquapi&color=yellow) since 16.04.2022
