#!/usr/bin/python3
import serial
from matplotlib import pyplot as plt
import numpy as np
import struct
import io
import base64
from matplotlib import cm
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
    print("Converting")
    raw_bytes = np.array(imageList).astype(np.uint16) #dtype="i2")
    print(len(raw_bytes))
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

    image = np.reshape(image,(240,320,3)) # QVGA resolution
    #pic = Image.fromarray(np.uint8(cm.gist_earth(image)))
    #pic.save("input/fig.jpg")
    # Show the image
    print("image done")
    im=Image.fromarray((image).astype(np.uint8))
    im.save("input/your_file.png")
    

def main():
    #print(args.port)
    #ser = serial.Serial(args.port, 9600)
    print("Init")
    ser = serial.Serial("COM6", 9600)
    ser.flushInput()
    ser.flushOutput()
    while True:  
        cc=str(ser.readline())
        print("data received")
        #f = open("file.txt", "w")
        HEXADECIMAL_BYTES=cc[2:][:-5] # take away header and only keep the raw data
        stringlist=HEXADECIMAL_BYTES.split(",")
        print("stringlist length is : {}".format(len(stringlist)))
        #convert to hexdecimal list 
        hex_list=[]
        for x in stringlist:
            hex_int = int(x, 16)
            hex_list.append(hex_int)
        #print(type(hex_list[0]))
        #f.writelines(cc)
        #f.write("\n")
        #f.close()
        ser.flushInput()
        ser.flushOutput()
        # translate hex_list to image
        convertToImage(hex_list)


if __name__ == "__main__":
    #argParser = argparse.ArgumentParser()
    #argParser.add_argument("port", help="which port will be connected to")
    #args=argParser.parse_args()
    main()
