#from ImageProcessing.image_processing import detect_chars
#from collection_class import DataCollection
from image_processing import detect_chars, transform_images
from data_collection import store_data

## Image processing and detecting individual characters
detect_chars('input/test4.jpg', 'output')

## Transform ROI images of characters to be of uniform size (resolution)
transform_images()

## Collect and store images in dataset
store_data()

## If it is better to use a class, then go with
# dc = DataCollection('data/input/images/test.jpg', 'data/output/images')
# dc.detect_chars()

