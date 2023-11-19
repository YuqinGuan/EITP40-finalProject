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

width=144
height=176

def convertToImage(HEXADECIMAL_BYTES):
     
     # Reformat the bytes into an image
     raw_bytes = np.array(HEXADECIMAL_BYTES, dtype="i2")
     print(raw_bytes)
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

def v2(HEXADECIMAL_BYTES):
     return Image.frombytes("L", (width, height), HEXADECIMAL_BYTES, decoder_name="xbm")


def v3(HEXADECIMAL_BYTES):
   
    img = Image.frombuffer('L', (242,266), HEXADECIMAL_BYTES, 'raw', 'L', 0, 1)
    return img


def mapToArray(HEXADECIMAL_BYTES):
    b = bytearray()
    b.extend(map(ord, HEXADECIMAL_BYTES))
    return b

def main():
    
    ser = serial.Serial("COM4", 9600)
    
    while True:
        ser.flushInput()
        ser.flushOutput()
        cc=str(ser.readline())
        print("String: \n {}\n".format(cc))
        HEXADECIMAL_BYTES=cc[2:][:-5]
        print("HEX: \n {}\n".format(cc))
        print("HEX length {}".format(len(HEXADECIMAL_BYTES)))
        imageArray= mapToArray( HEXADECIMAL_BYTES)
        convertToImage(imageArray)
    #cc=str(ser.readline())
    #print("String: \n {}\n".format(cc))
    #print("String length :{}".format(len(cc)))
    #HEXADECIMAL_BYTES=cc[2:][:-5]
    #print('\n')
    #print("HEX: \n {}\n".format(cc))
    #print("HEX length {}".format(len(HEXADECIMAL_BYTES)))
    ##img = v2(HEXADECIMAL_BYTES)
    #b = bytearray()
    #b.extend(map(ord, HEXADECIMAL_BYTES))
    #np.reshape(b,(width,height))
    #img=v3(b)
    #imageArray= mapToArray( HEXADECIMAL_BYTES)
    #print(len(imageArray))
    #print("imageArray: {}".format(imageArray))
    #convertToImage(imageArray)
    #r_data = binascii.unhexlify(HEXADECIMAL_BYTES)
    #stream = io.BytesIO(r_data)
    #img = Image.open(stream)
    #HEXADECIMAL_BYTES= cc.encode('utf-8')
    #img = Image.frombytes("RGB", (width, height), HEXADECIMAL_BYTES)
     #draw = ImageDraw.Draw(img)
     
     
     
     #img.save('D:\\1.jpg')
     #convertToImage(HEXADECIMAL_BYTES)

if __name__ == "__main__":
    main()