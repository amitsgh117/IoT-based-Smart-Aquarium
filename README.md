# IoT based Smart Aquarium

## Link to the repository: 
https://github.com/amitsgh117/IoT-based-Smart-Aquarium

## Hardware Requirements

* Raspberry Pi 3
* Arduino
* Relay
* pH Sensor
* Mobile Phone for LDR Sensor using [Phone Pi+](https://play.google.com/store/apps/details?id=com.phonepiplus&hl=en_US&gl=US&pli=1) app
* Solenoid Valve
* 2 LEDs
* Breadboard
* Wires

## Hardware Connections

### Arduino and pH sensor connection
Connect wires between the following pins:
| Arduino | pH Sensor Board |
| ------ | ------ |
| 5V | V+ |
| GND | G |
| A0 | Po |

Then connect the pH sensor electrode with pH Sensor Board.
![ph measure](https://user-images.githubusercontent.com/85020065/202157699-350878e4-31dd-4e6b-adcf-a19785f20dda.jpg)


### Arduino, Relay and Solenoid Valve connection

Connect wires between the following pins:
| Arduino | Relay Module |
| ------ | ------ |
| 3.3V | VCC |
| GND | GND |
| D12 pin | IN1 input |

Then connect one wire of Solenoid valve with the battery's +ve terminal, it's other wire to the relay and battery's -ve terminal to the relay. 

![solenoid connection](https://user-images.githubusercontent.com/85020065/202157884-b09fbd82-7d9d-4eb0-9976-80eec685df01.jpg)


### Raspberry Pi and LED connection
Connect wires between the following:
| Raspberry Pi | LED |
| ------ | ------ |
| GPIO 17 & GND | LED 1 |
| GPIO 11 & GND | LED 2 |

![led OFF](https://user-images.githubusercontent.com/85020065/202157969-8d6ee4b3-8786-477e-af2a-0595884312b7.jpg)

## Project Structure and Code description

* ```/Raspberry Pi code copy/requirements.txt```: Contains all the dependencies required for Raspberry Pi
* ```/Raspberry Pi code copy/sensor.py```: Receives real-time Light Sensor values from PhonePi+ app and pH values from Arduino, controls the LEDs, sends sensor data to Client through Socket, encrypts data before transmission
* ```/arduino code/ph/ph.ino```: Collects real-time pH values and sends it to the Raspberry Pi, controls the relay which turns ON/OFF the solenoid valve for water flow
* ```/socket/socket_communication.py```: Receives real=time sensor data from Raspberry Pi, decrypts the data and sends it to sensor_output.json
* ```/socket/sensor_output.json```: JSON containing light and pH values
* ```/backend/package.json```: Contains all the dependencies required for backend
* ```/backend/server.js```: API to fetch data from sensor_output.json
* ```/front end/package.json```: Contains all the dependencies required for frontend
* ```/front end/src/app/```: Contains files to integrate the API and display live data on a button click on a webpage

## STEPS TO RUN:

1) Connect the Arduino (with all pH sensor and relay connection) to the PC using the USB cable. RUN and UPLOAD the ```/arduino code/ph/ph.ino``` in the Arduino IDE. Make sure that it is printing the pH values in the Serial Monitor every 2 seconds. Remove the USB and connect it to the Raspberry Pi.
2) Connect the Raspberry Pi (with all LED connections) to the PC using Type B cable. Connect it to WiFi (The board used in this Project connects to a WiFi network with {Name: Rpi, Password:00000000}). Open the Raspberry Pi terminal and log in. (Log in credentials of our board: {Username: pi, Password: iotians}).
3) Duplicate the files ```/Raspberry Pi code copy/requirements.txt``` and ```/Raspberry Pi code copy/sensor.py``` in any directory. (In our board, just navinate to ```/Desktop/Group8``` directory where files already exists).
4) Install all the dependencies using: 
```sh
pip install -r requirements.txt
```
5) In the ```sensor.py``` enter Raspberry Pi IP and PC IP addresses in the variables _server_ and _client_ respectively.
6) Now in PC, in the ```/socket/socket_communication.py``` enter PC IP address in the variable _IP_ and run this file making it ready to receive data from Raspberry Pi. (Make sure running it from the correct directory).
```sh
python3 socket_communication.py
```
7) In the Raspberry Pi, run the ```sensor.py```. Now it waits for the Light Sensor in the PhonePi+ app to turn ON before printing and transmitting sensors data.
```sh
python3 sensor.py
```
8) Connect the mobile phone to the same network with which Raspberry Pi is connected. (In our case, WiFi network with {Name: Rpi, Password:00000000}). In the PhonePi+ app, enter the Raspberry Pi IP address, set frequency corresponding to LightSensor as 2000 and turn ON the LightSensor.

This will start streaming sensors data on Raspberry Pi as well as sending it to the PC through socket communication. In the PC, this data is received and gets recorded in ```/socket/sensor_output.json``` file in real-time.

9) Now to view this data on the webpage, first start the backend by installing dependencies and running ```/backend/server.js``` (Make sure doing it from the correct directory):
```sh
npm install
node server.js
```
10) Now start the frontend by navigating to the ```/front end/``` directory, installing all dependencies and running:
```sh
npm install
npm start
```
11) Once its comeplete, open the browser, go to http://localhost:4200/ and click the button "_Check Values_". This will display the light and the pH values.
