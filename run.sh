#!/usr/bin/env bash

cd ImageProcessing

# Save taken image with device camera
#python3 port.py /dev/cu.usbmodem1421101
python3 port.py /dev/ttyACM0

# Run script to detect characters and create dataset
python3 script.py