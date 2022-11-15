from flask import Flask
from flask_sockets import Sockets
import socket
import RPi.GPIO as GPIO
import time
import json
import serial

LED_PIN_1 = 11 # for led
LED_PIN_2 = 17 # for led

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)

def encrypted_string(s):
    es = []
    for i in range(len(s)):
        k = ord(s[i])
        k += 1
        es.append(chr(k))
    return str(''.join(es))

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

hostname = socket.gethostname()
IPAddr = get_ip()
print("IP Address: " + IPAddr)


app = Flask(__name__)
sockets = Sockets(app)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

@sockets.route('/lightsensor')
def echo_socket(ws):
    host='192.168.137.167' #raspi ip
    port = 4005
    server = ('172.23.64.134', 4000) #laptop ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))


    while True:
        message = ws.receive()
        light_data = json.loads(message)
        light_value = light_data.get("light")
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
        light = encrypted_string(str(light))
        s.sendto(repr(light).encode('utf-8'), server)

        print("light:",light_value)
        ws.send(message)

        if ser.in_waiting > 0:
            ph_value = ser.readline().decode('utf-8').rstrip()
            ph = {"ph":ph_value}
            ph = encrypted_string(str(ph))
            s.sendto(repr(ph).encode('utf-8'), server)
            print("pH:",ph_value)


    s.close()
    f.close()
    GPIO.cleanup()


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(
        ('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
