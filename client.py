# str to Binary ASCII conversion from https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa?answertab=votes#tab-top
# add_noise method extracted from https://stackoverflow.com/questions/52918476/creating-a-function-that-changes-values-in-a-list-based-on-probability

from bitarray import bitarray
from socket import *
import binascii
from config import HOST, PORT
import random
import pickle


def convert_to_bits(text):
    bits = bin(int(binascii.hexlify(text.encode('utf-8', 'surrogatepass')), 16))[2:]
    bits = bits.zfill(8 * ((len(bits) + 7) // 8))
    return bitarray(bits)

def add_noise(bits):
    probability = 1/len(bits)
    altered_bitarray = bitarray()

    for bit in bits:
        if (random.random() <= probability):
            altered_bitarray.append(int(not bit))
        else:
            altered_bitarray.append(bit)
    return altered_bitarray

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((HOST,PORT))

while True:
    message = input("Message: ")
    converted_bitarray = convert_to_bits(message)
    print(converted_bitarray)
    crc32 =  binascii.crc32(converted_bitarray)
    print("crc32", crc32)
    noisy_bitarray = add_noise(converted_bitarray)
    clientSocket.send(pickle.dumps({'payload': noisy_bitarray, 'crc32': crc32}))

clientSocket.close()