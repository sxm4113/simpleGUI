import os
import cv2
import numpy as np

from exceptions import ImageNotFound 

class Pyramid:
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
            cv2.imshow("window", self.image)
            cv2.waitKey(0)

    def downsample(self, input_image):
        return cv2.resize(input_image,None,fx=0.5, fy=0.5,
                                 interpolation=cv2.INTER_LINEAR)
    
    def upsample(self, input_image):
        return cv2.resize(input_image,None,fx=2.0, fy=2.0,
                                 interpolation=cv2.INTER_LINEAR)
    
    def conv_filter(self, input_image):

        kernel1 = np.array(
            [[1.0 / 256, 4.0 / 256, 6.0 / 256, 4.0 / 256, 1.0 / 256],
        [4.0 / 256, 16.0 / 256, 24.0 / 256, 16.0 / 256, 4.0 / 256],
        [6.0 / 256, 24.0 / 256, 36.0 / 256, 24.0 / 256, 6.0 / 256],
        [4.0 / 256, 16.0 / 256, 24.0 / 256, 16.0 / 256, 4.0 / 256],
        [1.0 / 256, 4.0 / 256, 6.0 / 256, 4.0 / 256, 1.0 / 256]]) 

        filtered_image = cv2.filter2D(src=input_image.astype(np.float32), ddepth=-1, kernel=kernel1)
        return filtered_image
    
    def rolp(self,lowpass_image):
        output =cv2.divide(self.image.astype(np.float32), 4.0*lowpass_image.astype(np.float32))
        return output
    
    def adjust(self, rolp):
        height, width = self.image.shape[:2]
      
        output = np.zeros_like(self.image,np.float32)
        ##remove loop
        for i in range (0,height):
            for j in range (0,width):
                if (i > 1 and i < height - 1 and j > 1 and j < width):
                    
                    if rolp[i,j] < 1:
                        CE_EXP = np.min(self.image[i-1:i+1, j-1:j+1])
                    else:
                        CE_EXP = np.max(self.image[i-1:i+1, j-1:j+1])
                else: 
                    CE_EXP = self.image[i,j]
                final_value = CE_EXP * 3.0 * rolp[i,j]
                output[i,j] = final_value
        return output
    
    def run_algorithm(self):
        downsized_image = self.downsample(self.image)
        down_conv_filtered = self.conv_filter(downsized_image)
        up_sampled = self.upsample(down_conv_filtered)
        up_conv_filtered = self.conv_filter(up_sampled)
        lowpass_ratio = self.rolp(up_conv_filtered)
        final_image = self.adjust(lowpass_ratio) 
 
        return final_image.astype(np.uint8)


        