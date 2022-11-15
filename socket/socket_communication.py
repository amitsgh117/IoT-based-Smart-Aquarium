import socket
import json

sensor_json = 'sensor_output.json'

def decrypted_string(s):
    es = []
    for i in range(len(s)):
        k = ord(s[i])
        k -= 1
        es.append(chr(k))
    return str(''.join(es))

def Main():

    IP = '172.17.79.87' #laptop ip
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((IP, port))
    
    print("Server Starting . . . ")
    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')        
        print("Encrypted message:", data)
        data = decrypted_string(data)[1:-1]
        entry = eval(data)
        
        with open(sensor_json, "r") as file:
            sensor_value = json.load(file)

        if (not 'ph' in entry):
            sensor_value['light_data'].append(entry)
        else:
            sensor_value['pH_data'].append(entry)


        with open(sensor_json, "w") as file:
            json.dump(sensor_value, file)

        print("Message from: " + str(addr) + data)
        
    s.close() 

if __name__=='__main__':
    Main()