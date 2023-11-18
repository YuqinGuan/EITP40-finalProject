# Project - EITP40 - Handwriting recognition

# Data Collection

We created a [Conda environment](#conda-environment) for this project.
To run this, make sure you have the Python [packages](#packages) installed.

In directory `/ImageProcessing`: Run [`script.py`](/ImageProcessing/script.py) which will detect characters from image by running [`image_processing.py`](/ImageProcessing/image_processing.py).

## Image Processing

Input is a `JPG/PNG` image, which is processed to detect individual characters/letters.

At the top of the file [`image_processing.py`](/ImageProcessing/image_processing.py) you can configure if you want to apply the shadow filter or not and change the parameters kernel size and dilation iterations.

The detected characters are stored in [`ImageProcessing/output/chars`](/ImageProcessing/output/) as JPG files. Then all images are transformed (reshaped) into the same resolution.

## Collect all images as dataset

After all images of the detected characters are reshaped into the same resolution and stored in [`ImageProcessing/output/reshaped_chars`](/ImageProcessing/output/reshaped_chars/), the numpy array is saved as a `.npy` file together with the EMNIST `.mat` dataset that we found online in [`data/training`](/data/training/).

One can load and plot a random character by running the notebook [`plot_char.ipynb`](/ImageProcessing/plot_char.ipynb).

## Store image taken by OV7675 Camera

TODO

# Conda Environment

- `conda create --name <env-name>`
- `conda activate <env-name>`
- `kernel install --user --name=<env-name>`

## Packages

- `conda install -c conda-forge opencv` or `pip install opencv-python`
- `pip install Pillow`
- `pip install scipy`
- `pip install scikit-image`
