import cv2
from PIL import Image
import numpy as np
import os
import shutil
from skimage import io, color

## Configs
DEV_MODE = False
SHADOW = True
MIN_AREA = 40 # 250 , make smaller 
MAX_AREA = 700
MIN_HEIGHT = 10 # to avoid thin horizontal lines
MAX_HEIGHT_SORTING = 40 # This matters when sorting the contours
SPACE_WIDTH = 20
if SHADOW:
    # When using shadow filter
    kernel1 = (6,1)
    iter1 = 1
    # kernel2 = (2,1)
    # iter2 = 2
    th_low, th_high = 210, 255
else:
    # When shadow filter not applied
    kernel1 = (8,2)
    iter1 = 2
    # kernel2 = (2,1)
    # iter2 = 3
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



def sort_contours(ctrs):
    # Sort contours in reading order
    # Calculate maximum rectangle height
    heights = []
    for ctr in ctrs:
        _,_,_,h = cv2.boundingRect(ctr)
        if h < MAX_HEIGHT_SORTING:
            heights.append(h)
    max_height = np.max(heights)

    ## Sort based on y offset
    sorted_ctrs_by_y = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[1])
    line_y = cv2.boundingRect(sorted_ctrs_by_y[0])[1] # First y
    line = 1
    by_line = []

    # Assign line number to each contour
    for ctr in sorted_ctrs_by_y:
        x,y,w,h = cv2.boundingRect(ctr)
        if y > line_y + max_height:
            line_y = y
            line += 1
        by_line.append((line, x,y,w,h))

    # This will now sort automatically by line then by x
    contours_sorted = [(x, y, w, h) for line, x, y, w, h in sorted(by_line)]
    return contours_sorted


def detect_chars(input_image_path, output_path):
    assert(isinstance(output_path, str))
    assert(isinstance(input_image_path, str))
    char_path = output_path + '/chars'
    

    shutil.rmtree(char_path)
    os.mkdir(char_path)
    #clear_dir(char_path)
    clear_dir('output/padded_chars')
    clear_dir('output/resized')
    clear_dir('../data/test')
    
    image = cv2.imread(input_image_path)
    # Process input image
    gray, shadow_norm, thresh, img_dilation, ctrs = process(image, kernel1, iter=iter1)
    sorted_ctrs = sort_contours(ctrs)
    
    k = 0 
    prev_x = 0
    word_i = -1

    for entry in sorted_ctrs: 
        x,y,w,h = entry
        # Getting ROI
        binary_roi = thresh[y:y+h,x:x+w]
        #roi = image[y:y+h,x:x+h]
        area = w*h
        # Avoid noise and small/large ROIs
        if area > MIN_AREA and area < MAX_AREA and h > MIN_HEIGHT:
            dx = np.abs(prev_x - x)
            prev_x = x
            #if k == 0: dx = 0
            if dx >= SPACE_WIDTH:
                ## Create separate folders for each word
                word_i += 1
                word_path = output_path + '/chars/word_' + str(word_i)
                #print(word_path)
                os.mkdir(word_path)

            #print(f"{k}: (x,y)={x,y}, dx={dx}")
            # Draw red rectangles on original image
            color = (90,0,255)
            cv2.rectangle(image, (x,y), (x+w, y+h), color, 1)
            # Save ROI as image, using the binary thresh image
            # filename = char_path + '/ROI_' + str(k) + '.jpg'
            filename = char_path + '/word_'+str(word_i)+'/ROI_'+str(k)+'.jpg'         
            cv2.imwrite(filename, binary_roi)
            k += 1

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


    
def create_dataset(samples, sorted_char_dir, max_w, max_h, index):
    char_dataset = np.zeros((samples, 28, 28))
    for i, img_number in enumerate(sorted_char_dir):
        # Padding image into uniform shape (new_h, new_w) by 
        padded_char = np.full((max_h, max_w), 0, dtype=np.uint8)
        char_data = cv2.imread('output/chars/word_'+str(index)+'/ROI_'+str(img_number)+'.jpg')
        gray_char = color.rgb2gray(char_data)*255

        filename = 'ROI_'+str(img_number)+'.jpg'
        h, w = gray_char.shape
        x_c = (max_w - w) // 2
        y_c = (max_h - h) // 2

        # Store padded image in padded_chars directory
        padded_char[y_c:y_c+h, x_c:x_c+w] = gray_char
        cv2.imwrite("output/padded_chars/" + filename, padded_char)

        # Now resize image to desired (28,28) shape
        image = Image.open('output/padded_chars/' + filename)
        resized = image.resize((28,28))
        resized.save("output/resized/" + filename)

        # char_dataset[i] = padded_char
        char_dataset[i] = resized
        
    return char_dataset


def transform_create_datasets():
    # Iterate through all images in chars directory
    widths = []
    heights = []
    # samples = 0
    char_directory = os.listdir('output/chars')
    sorted_char_dir = sorted([int(x.split('_')[1].split('.')[0]) for x in char_directory])
    
    samples_per_word = []
    chars_per_word = []

    for word_number in sorted_char_dir:
        samples = 0
        word_dir = os.listdir('output/chars/word_' + str(word_number))
        sorted_word_dir = sorted([int(x.split('_')[1].split('.')[0]) for x in word_dir])
        #print(sorted_word_dir)
        chars_per_word.append(sorted_word_dir)

        for img_number in sorted_word_dir:
            char_img = Image.open('output/chars/word_'+str(word_number)+'/ROI_'+str(img_number)+'.jpg')
            # Convert to numpy array
            char_data = np.asarray(char_img)
            h,w = char_data.shape[0:2]
            widths.append(w)
            heights.append(h)
            samples += 1

        samples_per_word.append(samples)

    max_w = np.max(widths)
    max_h = np.max(heights)

    # Create dataset for each sub-folder word_i
    datasets = []
    for i in range(0,len(sorted_char_dir)):
        print(f"====\nWord {i}: {chars_per_word[i]}")
        dset = create_dataset(samples_per_word[i], chars_per_word[i], max_w, max_h, index=i)
        datasets.append(dset)

    return datasets
    
