from image_processing import detect_chars, transform_collect_images
import numpy as np
import argparse
from port import main

argParser = argparse.ArgumentParser()
argParser.add_argument("port", help="which port will be connected to")
args=argParser.parse_args()

## Load HEX_BYTES and save as JPG image
main(args)

## Load the saved image and use its path for the detect_chars() command
# TODO

## Image processing and detecting individual characters
detect_chars('input/test4.jpg', 'output')

## Transform ROI images of characters to be of uniform size (resolution)
characters_dataset = transform_collect_images()
print("Char dataset shape: ", characters_dataset.shape)
print(type(characters_dataset))

## Save and store images in .npy dataset
np.save('../data/training/chars', characters_dataset)