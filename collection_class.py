import cv2
import os
import numpy as np

class DataCollection:
    def __init__(self, input_image_path, store_path):
        self.input_image_path = input_image_path
        self.store_path = store_path

    def show_image(self, image, title, size):
        resized_img = cv2.resize(image, size)
        cv2.imshow(title, resized_img)

    def save_image(self, image, filename):
        cv2.imwrite(self.store_path + '/processing/' + filename + '.jpg', image)

    def clear_dir(self, path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                os.remove(os.path.join(path, file))

    def detect_chars(self):
        assert(isinstance(self.store_path, str))
        assert(isinstance(self.input_image_path, str))

        char_path = os.path.join(self.store_path, 'chars')
        self.clear_dir(char_path)
            
        # Desired image size
        size = (960,540)
        image = cv2.imread(self.input_image_path)

        # To grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #binary
        ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
        
        #dilation
        kernel = np.ones((5,5), np.uint8)
        img_dilation = cv2.dilate(thresh, kernel, iterations=1)
        
        #find contours
        # im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])


        for i, ctr in enumerate(sorted_ctrs):
            # Get bounding box
            x,y,w,h = cv2.boundingRect(ctr)
            # Getting ROI
            roi = image[y:y+h, x:x+w]
            area = cv2.contourArea(ctr)
            # Avoid noise and small ROIs
            if area > 100:
                # Draw rectangles in image for ROIs
                cv2.rectangle(image, (x,y), (x+w, y+h), (90,0,255), 2)
                # Save ROI as image
                filename = self.store_path + '/chars/ROI_' + str(i) + '.jpg'
                cv2.imwrite(filename, roi)


        ## show images
        self.show_image(gray, "Grayscale", size)
        self.show_image(thresh, "Binary", size)
        self.show_image(img_dilation, "Dilation", size)
        self.show_image(image, 'Result', size)
        ## save images
        self.save_image(gray, 'Grayscale')
        self.save_image(thresh, 'Binary')
        self.save_image(img_dilation, 'Dilation_with_kernel')
        self.save_image(image, 'Result')
        cv2.waitKey(0)