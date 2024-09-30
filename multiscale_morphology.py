import os
import cv2
import numpy as np
from exceptions import ImageNotFound 

class Morphology:
    def __init__(self,image_filename):
        try:   
            if os.path.exists(image_filename) != True:
                raise ImageNotFound ("Error-Image not found")
            else:
                self.image = cv2.imread(image_filename,0)
        except ImageNotFound as e:
            print (e)
            exit(1) 

    def displayImage(self, input= None):
        if input is None:
            input = self.image
        cv2.imshow("window", input)
        cv2.waitKey(0)
    
    def saveImage (self, input = None):
        if input is None:
            input = self.image
        cv2.imwrite("output.jpg", input)

    def black_hat(self, k_size, input=None):
        if input is None:
            input = self.image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(k_size,k_size))
        output = cv2.morphologyEx(input, cv2.MORPH_BLACKHAT, kernel)
        
        return output
    
    def top_hat(self, k_size, input=None):
        if input is None:
            input = self.image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(k_size,k_size))
        output = cv2.morphologyEx(input, cv2.MORPH_TOPHAT, kernel)
        
        return output
    
    def run_algorithm(self):
        top_hat3 = self.top_hat(k_size=3)
        top_hat5 = self.top_hat(k_size=5)
        top_hat7 = self.top_hat(k_size=7) 

        black_hat3 = self.black_hat(k_size=3)
        black_hat5 = self.black_hat(k_size=5)
        black_hat7 = self.black_hat(k_size=7) 

        sum_top_hat = 0.9 * top_hat3 + 0.7 * top_hat5 + 0.5 * top_hat3          
        sum_black_hat = 0.9 * black_hat3 + 0.7 * black_hat5 + 0.5 * top_hat3  
        print ('run algorithm')
        final_image_floating =  self.image + sum_top_hat - sum_black_hat
        final_image = np.clip(final_image_floating, 0, 255)
        final_image = final_image.astype(np.uint8) 
        
        return final_image            
