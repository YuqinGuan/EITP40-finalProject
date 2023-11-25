# Project - EITP40 - Handwriting recognition

# Data Collection

We created a [Conda environment](#conda-environment) for this project.
To run this, make sure you have the Python [packages](#packages) installed.

In directory `/ImageProcessing`: Run [`script.py`](/ImageProcessing/script.py) which will detect characters from image by running [`image_processing.py`](/ImageProcessing/image_processing.py).

## Image Processing

Input is a `JPG/PNG` image, which is processed to detect individual characters/letters.

At the top of the file [`image_processing.py`](/ImageProcessing/image_processing.py) you can configure if you want to apply the shadow filter (`SHADOW` variable) or not and change parameters. Also you can set `DEV_MODE` as `True` or `False`. Setting it to `True` will open some of the images in the processing steps and sopen the resulting image of detected characters marked in red rectangles.

The detected characters are stored in [`ImageProcessing/output/chars`](/ImageProcessing/output/) as JPG files. Then all images are transformed (reshaped by padding) into the same resolution.

## Collect all images as dataset

After all images of the detected characters are padded into a uniform resolution and stored in [`ImageProcessing/output/padded_chars`](/ImageProcessing/output/padded_chars/), they are resized into the desired shape `(28,28)` and stored in [`ImageProcessing/output/resized/`](/ImageProcessing/output/resized/).
The numpy array of shape `(n_samples,28,28)` corresponding to all images is saved as a `.npy` file together with the EMNIST `.mat` dataset that we found online in [`data/training`](/data/training/).
The resizing is necessary as it drastically decreases the siz of the `.npy` file.

One can load and plot a random character by running the notebook [`pre_training.ipynb`](/pre_training.ipynb). Both for our own dataset and the EMNIST dataset. EMNIST dataset downloaded [here](https://www.nist.gov/itl/products-and-services/emnist-dataset).

## Store image taken by OV7675 Camera

Run port.py by python port.py ##port number

Philip's port: `/dev/cu.usbmodem1441101`

# Bash script

Run bash script `run.sh` to start the "pipeline".

To make the file executable:

- Appended this line at the top of the file `#!/usr/bin/env bash` (Mac OS)
- Change file permissions `chmod +x run.sh`

# Conda Environment

- `conda create --name <env-name>`
- `conda activate <env-name>`
- `kernel install --user --name=<env-name>`

## Packages

- `conda install -c conda-forge opencv` or `pip install opencv-python`
- `pip install Pillow`
- `pip install scipy`
- `pip install scikit-image`
- `pip install pyserial`
