#from ImageProcessing.image_processing import detect_chars
#from collection_class import DataCollection
from image_processing import detect_chars, transform_images
import numpy as np

## Image processing and detecting individual characters
detect_chars('input/test4.jpg', 'output')

## Transform ROI images of characters to be of uniform size (resolution)
characters_dataset = transform_images()
print("Char dataset shape: ", characters_dataset.shape)
print(type(characters_dataset))

## Save and store images in .npy dataset
# np.save('output/data/chars', characters_dataset)
np.save('../data/chars', characters_dataset)


## If it is better to use a class, then go with
# dc = DataCollection('data/input/images/test.jpg', 'data/output/images')
# dc.detect_chars()

