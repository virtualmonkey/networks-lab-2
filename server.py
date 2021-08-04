from bitarray import bitarray
from socket import *
from config import HOST, PORT
import pickle
import binascii

def decode(bitarray):
    return bitarray.tobytes().decode('utf-8')

def verify(payload, crc32):
    return binascii.crc32(payload) == crc32


def bin2str(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def Three1(array):
    data1 = array[0]
    data2 = array[1]
    data3 = array[2]
    temp= ""
    cont = 0

    for i in data1:
        if i == data2[cont]:
            temp += i 
        elif data2[cont] == data3[cont]:
            temp += data2[cont]
        else: 
            temp+= i
        cont += 1
    return temp


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print ("The server is ready to receive")
connection, addr = server_socket.accept()
strarr = []
errors =  0 
while True:
    message = connection.recv(1024)
    
    if not message:
        break
    
    message = pickle.loads(message)
    temp = message['payload'].to01()
    
    strarr.append(temp)
    
    #print(message['payload'])
    #decoded_message = decode(message['payload'])
    decoded_message = bin2str(temp)
    print("el mensaje entrante es: ",decoded_message)
    #print ("Message from client:", decoded_message)
    if( verify(message['payload'],message["crc32"]) != True):
        errors +=1

    if(len(strarr)%3==0):
        if(errors>0):
            corrected_str=Three1(strarr)
            corrected_message=bin2str(corrected_str)
            print("se encontró al menos un error, el mensaje corregido es: ",corrected_message)
            errors=0
        strarr = []
    #print ("No errors have been detected in the message" if verify(message['payload'], message["crc32"]) else "An error has been detected in the message")
    

connection.close()