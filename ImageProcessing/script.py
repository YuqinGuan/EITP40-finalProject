from image_processing import detect_chars, transform_create_datasets
import numpy as np

## Load the saved image and use its path for the detect_chars() command
# TODO

## Image processing and detecting individual characters
## Each detected word will be stored as a dataset in data/test
detect_chars('input/chars1.png', 'output')
print("Characters detected")


## Transform ROI images of characters to be of uniform size (resolution)
## and then resized to (28,28)
## Create separate datasets for each word
word_datasets = transform_create_datasets()

for i, dataset in enumerate(word_datasets):
    print("Char dataset shape: ", dataset.shape)
    #print(type(dataset))

    ## Save and store images in .npy dataset
    dataset_path = '../data/test/word_' + str(i)
    np.save(dataset_path, dataset)