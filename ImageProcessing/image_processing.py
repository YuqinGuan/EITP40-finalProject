import cv2
from PIL import Image
import numpy as np
import os

## Configs
DEV_MODE = False
SHADOW = True
if SHADOW:
    # When using shadow filter
    kernel1 = (4,1)
    iter1 = 3
    kernel2 = (2,1)
    iter2 = 2
    th_low, th_high = 210, 255
else:
    # When shadow filter not applied
    kernel1 = (8,2)
    iter1 = 2
    kernel2 = (2,1)
    iter2 = 3
    th_low, th_high = 127, 255

def show_image(image, title):
    #resized_img = cv2.resize(image, size)
    cv2.imshow(title, image)

def save_image(image, filename):
    cv2.imwrite('output/processing/' + filename + '.jpg', image)

def clear_dir(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            os.remove(os.path.join(path, file))

def remove_shadows(image):
    rgb_planes = cv2.split(image)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((5,5), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    #result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)
    return result_norm

def process(image, kernel_size, iter):
    assert(np.shape(kernel_size) == (2,))
    # To grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Filter shadows or not
    if SHADOW:
        shadow_norm = remove_shadows(gray)
    else:
        shadow_norm = cv2.normalize(gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    
    #binary threshold
    _,thresh = cv2.threshold(shadow_norm, th_low, th_high, cv2.THRESH_BINARY_INV)
    
    #dilation
    kernel = np.ones(kernel_size, np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=iter)
    
    #find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return gray, shadow_norm, thresh, img_dilation, ctrs


def sub_roi(roi, index, char_path):
    _,_,_,_,ctrs = process(roi, (2,2), iter=iter2)
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    for i, ctr in enumerate(sorted_ctrs):
        x,y,w,h = cv2.boundingRect(ctr)
        area = cv2.contourArea(ctr)
        #print(f"Sub ROI {index+i}")
        if area > 200:
            sub_roi = roi[y:y+h, x:x+w]
            if DEV_MODE: cv2.rectangle(roi, (x,y), (x+w,y+h), (250,10,90), 2)
            name = char_path + '/subROI_' + str(index+i) + '.jpg'
            cv2.imwrite(name, sub_roi)            

def detect_chars(input_image_path, output_path):
    assert(isinstance(output_path, str))
    assert(isinstance(input_image_path, str))
    char_path = output_path + '/chars'
    clear_dir(char_path)
    
    image = cv2.imread(input_image_path)
    # Process input image
    gray, shadow_norm, thresh, img_dilation, ctrs = process(image, kernel1, iter=iter1)
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x,y,w,h = cv2.boundingRect(ctr)
        # Getting ROI
        roi = image[y:y+h, x:x+w]
        area = cv2.contourArea(ctr)
        # Avoid noise and small ROIs
        if area > 250:
            #print(f"{i}: area={area}, width={w}")
            if w > 65:
                # Process sub-ROI image
                sub_roi(roi, i, char_path)
            else:
                if DEV_MODE:
                    # Draw rectangles in image for ROIs
                    color = (90,0,255)
                    cv2.rectangle(image, (x,y), (x+w, y+h), color, 2)
                # Save ROI as image
                filename = char_path + '/ROI_' + str(i) + '.jpg'
                cv2.imwrite(filename, roi)

    if DEV_MODE:
        # show images
        # show_image(gray, "Grayscale")
        # show_image(thresh, "Binary")
        # show_image(img_dilation, "Dilation")
        show_image(shadow_norm, 'Shadow Norm')
        show_image(image, 'Result')
        cv2.waitKey(0)
    
    ## save images
    save_image(gray, 'Grayscale')
    save_image(shadow_norm, 'Shadow_filter')
    save_image(thresh, 'Binary_threshold')
    save_image(img_dilation, 'Dilation_with_kernel')
    save_image(image, 'Result')
    

def transform_images():
    # Iterate through all images in chars directory
    widths = []
    heights = []
    samples = 0
    for img in os.scandir('output/chars'):
        char_img = Image.open(img.path)
        # convert image to numpy array
        char_data = np.asarray(char_img)
        #print(char_data.shape[0:2], img.path)
        h,w,channels = char_data.shape[0:3]
        widths.append(w)
        heights.append(h)
        samples += 1

    # Largest height and width
    max_w = np.max(widths)
    max_h = np.max(heights)
    #print(max_w, max_h, channels)

    # Padding of images to all be of shape (max_w, max_h)
    new_w = max_w
    new_h = max_h

    # Initialize dataset to store all images represented as arrays
    char_dataset = np.zeros((samples, new_h, new_w, channels))
    i = 0
    for img in os.scandir('output/chars'):
        # Extract color of image in pixel (0,0)
        r,g,b = char_data[0,0,:]
        bg_color = (r,g,b)
        reshaped_char = np.full((new_h, new_w, channels), bg_color, dtype=np.uint8)
        char_data = cv2.imread(img.path)
        
        filename = img.path.split('/')[2]
        h, w, channels = char_data.shape
        x_c = (max_w - w) // 2
        y_c = (max_h - h) // 2

        # copy img image into center of result image
        reshaped_char[y_c:y_c+h, x_c:x_c+w] = char_data
        cv2.imwrite("output/reshaped_chars/" + filename, reshaped_char)
        #print("Reshaped image: ", reshaped_char.shape)
        char_dataset[i] = reshaped_char
        i += 1
    
    return char_dataset