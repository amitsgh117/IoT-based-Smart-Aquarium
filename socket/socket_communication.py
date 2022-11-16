import socket
import json

sensor_json = 'sensor_output.json' # json file containing light and pH values

# function for decrypting data
def decrypted_string(s):
    es = []
    for i in range(len(s)):
        k = ord(s[i]) # char to ascii
        k -= 1
        es.append(chr(k)) # ascii to char
    return str(''.join(es))

def Main():

    IP = '172.17.79.87' #enter laptop (client) ip
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((IP, port)) # socket connection
    
    print("Server Starting...")
    while True:
        data, addr = s.recvfrom(1024) # received data
        data = data.decode('utf-8') 
        print("Encrypted message:", data) 
        data = decrypted_string(data)[1:-1] # decrypting after transmission
        entry = eval(data) # converting string to object (json)
        
        with open(sensor_json, "r") as file:
            sensor_value = json.load(file) #load json file

        # object for pH value goes to 'pH_data' and object for light values goes to 'light_data' in the json
        if (not 'ph' in entry):
            sensor_value['light_data'].append(entry)
        else:
            sensor_value['pH_data'].append(entry)

        # updating json
        with open(sensor_json, "w") as file:
            json.dump(sensor_value, file)

        print("Message from: " + str(addr) + data)
        
    s.close() 

if __name__=='__main__':
    Main()