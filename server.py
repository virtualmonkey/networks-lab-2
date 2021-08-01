from socket import *
from config import HOST, PORT
import pickle
import binascii

def decode(bitarray):
    return bitarray.tobytes().decode('utf-8')

def verify(payload, crc32):
    return binascii.crc32(payload) == crc32


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print ("The server is ready to receive")
connection, addr = server_socket.accept()

while True:
    message = connection.recv(1024)

    if not message:
        break
    
    message = pickle.loads(message)
    decoded_message = decode(message['payload'])
    print ("Message from client:", decoded_message)

    print ("No errors have been detected in the message" if verify(message['payload'], message["crc32"]) else "An error has been detected in the message")


connection.close()