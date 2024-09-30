import os
import cv2
import numpy as np
import copy
from scipy.ndimage import minimum_filter, maximum_filter

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

        output = np.zeros_like(self.image,np.float32)

        min_filtered = minimum_filter(rolp, size=(3,3), mode='constant')
        max_filtered = maximum_filter(rolp, size=(3,3), mode='constant'
                                      )
        min_mask = rolp < 1.0
        output = np.where(min_mask, min_filtered, self.image)

        max_mask = rolp > 1.0
        output = np.where(max_mask, max_filtered, self.image)

        output = output * 3.0 * rolp
        return output

    def run_algorithm(self):
        downsized_image = self.downsample(self.image)
        down_conv_filtered = self.conv_filter(downsized_image)
        up_sampled = self.upsample(down_conv_filtered)
        up_conv_filtered = self.conv_filter(up_sampled)
        lowpass_ratio = self.rolp(up_conv_filtered)
        final_image = self.adjust(lowpass_ratio)

        return final_image.astype(np.uint8)
