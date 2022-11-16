from flask import Flask
from flask_sockets import Sockets
import socket
import RPi.GPIO as GPIO
import time
import json
import serial

LED_PIN_1 = 11 # raspberry pi pin no for led
LED_PIN_2 = 17 # raspberry pi pin no for led

# setup for led
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)

# function for encrypting data
def encrypted_string(s):
    es = []
    for i in range(len(s)):
        k = ord(s[i]) # char to ascii
        k += 1
        es.append(chr(k)) # ascii to char
    return str(''.join(es))


app = Flask(__name__)
sockets = Sockets(app)

# serial communication for data transfer from arduino to raspberry pi
# arduino must be connected to raspberry pi for ttyACM0 to appear
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # ttyACM0 represents arduino
ser.reset_input_buffer()

@sockets.route('/lightsensor') # for streaming light sensor data through PhonePi+ mobile app
def echo_socket(ws):
    server='192.168.137.167' # enter raspberry pi (server) ip
    port = 4005
    client = ('172.23.64.134', 4000) # enter laptop (client) ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((server,port)) # socket connection


    while True:
        message = ws.receive() # receiving light data from app
        light_data = json.loads(message)
        light_value = light_data.get("light")

        # handling non ideal lighting conditions by turning ON and OFF LEDs
        if(light_value>40):
            GPIO.output(LED_PIN_1,GPIO.LOW)
            GPIO.output(LED_PIN_2,GPIO.LOW)
        elif(light_value<20 and light_value>=10):
            GPIO.output(LED_PIN_1,GPIO.HIGH)
            GPIO.output(LED_PIN_2,GPIO.LOW)
        elif(light_value<10):
            GPIO.output(LED_PIN_1,GPIO.HIGH)
            GPIO.output(LED_PIN_2,GPIO.HIGH)

        light = {"light":light_value} 
        light = encrypted_string(str(light)) # encrypting before transmission
        s.sendto(repr(light).encode('utf-8'), client) # sending to client

        print("light:",light_value)
        ws.send(message)

        # receiving pH value from arduino and sending to client after encryption
        if ser.in_waiting > 0:
            ph_value = ser.readline().decode('utf-8').rstrip()
            ph = {"ph":ph_value}
            ph = encrypted_string(str(ph))
            s.sendto(repr(ph).encode('utf-8'), client)
            print("pH:",ph_value)


    s.close()
    f.close()
    GPIO.cleanup()


@app.route('/')
def hello():
    return 'Hello World!'

# connection with the PhonePi+ mobile app
if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(
        ('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
