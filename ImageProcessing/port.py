import serial
from matplotlib import pyplot as plt
import numpy as np
import struct
import io
import base64
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import urllib.request
import io
import binascii
import sys, getopt
import argparse



def convertToImage(imageList):
    
    # Reformat the bytes into an image
    raw_bytes = np.array(imageList, dtype="i2")
    #print(len(raw_bytes))
    image = np.zeros((len(raw_bytes),3), dtype=int)

    # Loop through all of the pixels and form the image
    for i in range(len(raw_bytes)):
        #Read 16-bit pixel
        pixel = struct.unpack('>h', raw_bytes[i])[0]

        #Convert RGB565 to RGB 24-bit
        r = ((pixel >> 11) & 0x1f) << 3
        g = ((pixel >> 5) & 0x3f) << 2
        b = ((pixel >> 0) & 0x1f) << 3
        image[i] = [r,g,b]

    image = np.reshape(image,(144, 176,3)) #QCIF resolution

    # Show the image
    plt.imshow(image)
    plt.show()
    plt.savefig('output/figure.jpg')
    




def main():
    #print(args.port)
    ser = serial.Serial("/dev/ttyACM0", 9600)
    ser.flushInput()
    ser.flushOutput()
    while True:
        
        
        cc=str(ser.readline())
        #print("String: \n {}\n".format(cc))
        f = open("file.txt", "w")
        HEXADECIMAL_BYTES=cc[2:][:-5]
        
        #print("HEX: \n {}\n".format(cc))
        #print("HEX length {}".format(len(HEXADECIMAL_BYTES)))
        
        stringlist=HEXADECIMAL_BYTES.split(",")
        print("stringlist length is : {}".format(len(stringlist)))
        hex_list=[]
        for x in stringlist:
            hex_int = int(x, 16)
            hex_list.append(hex_int)
        #print(type(hex_list[0]))
        #f.writelines(HEXADECIMAL_BYTES)
        #f.write("\n")
        #f.close()
        ser.flushInput()
        ser.flushOutput()
        
        convertToImage(hex_list)


if __name__ == "__main__":
    #argParser = argparse.ArgumentParser()
    #argParser.add_argument("port", help="which port will be connected to")
    #args=argParser.parse_args()
    main()
