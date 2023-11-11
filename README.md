# Project - EITP40 - Handwriting recognition

# Data Collection

In directory `/ImageProcessing`: Run [`script.py`](/ImageProcessing/script.py) which will detect characters from image by running [`image_processing.py`](/ImageProcessing/image_processing.py).

## Image Processing

Input is a `JPG/PNG` image, which is processed to detect individual characters/letters. The input image should be taken with evenly distributed light on the paper.

Perhaps need to optimize the image processing for the appropriate size of the text in the photo.

The processing can be improved by adjusting paramaters:

- kernel size
- dilation iterations

TODO:

- Filter to get rid of shadows?
- Transform all output images to the same resolution (padding)
- Remove red rectangles from output images

## Collect all images in dataset

Store all images in dataset [here](/ImageProcessing/output/data/) - output images should be converted into a dataformat like `.npy`

# Conda Environment

- `conda create --name <env-name>`
- `conda activate <env-name>`
- `kernel install --user --name=<env-name>`

## Packages

- `conda install -c conda-forge opencv` or `pip install opencv-python`
