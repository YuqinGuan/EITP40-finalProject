import cv2
import numpy as np
import os

def show_image(image, title):
    #resized_img = cv2.resize(image, size)
    cv2.imshow(title, image)

def save_image(image, filename):
    cv2.imwrite('output/processing/' + filename + '.jpg', image)

def clear_dir(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            os.remove(os.path.join(path, file))

def process(image, kernel_size, iter):
    assert(np.shape(kernel_size) == (2,))
    #im = cv2.resize(image,None,fx=4, fy=4, interpolation = cv2.INTER_CUBIC)
    # To grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    norm_img = cv2.normalize(gray,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    #binary
    _,thresh = cv2.threshold(norm_img,127,255,cv2.THRESH_BINARY_INV)
    
    #dilation
    kernel = np.ones(kernel_size, np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=iter)
    
    #find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return gray, norm_img, thresh, img_dilation, ctrs


def sub_roi(roi, index, char_path):
    gray, norm_img, thresh, img_dilation, ctrs = process(roi, (1,5), iter=1)
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    for i, ctr in enumerate(sorted_ctrs):
        x,y,w,h = cv2.boundingRect(ctr)
        area = cv2.contourArea(ctr)
        print(f"Sub ROI {index+i}")
        if area > 200:
            sub_roi = roi[y:y+h, x:x+w]
            cv2.rectangle(roi, (x,y), (x+w,y+h), (250,10,90), 2)
            name = char_path + '/subROI_' + str(index+i) + '.jpg'
            cv2.imwrite(name, sub_roi)            

def detect_chars(input_image_path, output_path):
    assert(isinstance(output_path, str))
    assert(isinstance(input_image_path, str))
    
    char_path = output_path + '/chars'
    clear_dir(char_path)
    
    # Desired image size
    size = (1920,1080)
    image = cv2.imread(input_image_path)
    # Process input image
    gray, norm_img, thresh, img_dilation, ctrs = process(image, (8,2), iter=2)
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x,y,w,h = cv2.boundingRect(ctr)
        # Getting ROI
        roi = image[y:y+h, x:x+w]
        area = cv2.contourArea(ctr)
        # Avoid noise and small ROIs
        if area > 250:
            print(f"{i}: area={area}, width={w}")
            if w > 65:
                # Process sub-ROI image
                #cv2.imshow('roi_{}'.format(i), roi)
                sub_roi(roi, i, char_path)
                
            else:
                # Draw rectangles in image for ROIs
                color = (90,0,255)
                #w = int(np.round(w*0.8))
                cv2.rectangle(image, (x,y), (x+w, y+h), color, 2)
                # Save ROI as image
                filename = char_path + '/ROI_' + str(i) + '.jpg'
                cv2.imwrite(filename, roi)

    ## show images
    # show_image(gray, "Grayscale", size)
    # show_image(blur, 'Blur')
    # show_image(thresh, "Binary", size)
    # show_image(img_dilation, "Dilation", size)
    show_image(image, 'Result')
    
    ## save images
    save_image(gray, 'Grayscale')
    save_image(norm_img, 'Norm')
    save_image(thresh, 'Binary')
    save_image(img_dilation, 'Dilation_with_kernel')
    save_image(image, 'Result')
    
    cv2.waitKey(0)


def transform_images():
    print("TODO")