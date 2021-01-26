<img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/logo.png" width="200" />

# AquaPi
AquaPi is a plant watering project using a Raspberry Pi and an Arduino Uno. The Raspberry Pi is the master device. It processes the user's input via a XBox controller, it shows a menu on the LCD display, it manages the Arduino and its connected sensors and it hosts and updates a database and a web interface.

<img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/setup.PNG" width="600" />

## Hardware


### Electronics

The schemetic of the electronics is shown in the image bellow:
> <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/schematic.png" width="800" />

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

**Desktop view webinterface**:
> <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/webinterface_desktop.PNG" width="800" />

**Smartphone view webinterface**:
> <img src="https://github.com/SaKi1309/AquaPi/blob/main/imgs/webinterface_android.PNG" width="300" />
