import os
import cv2

from image_pyramid import Pyramid
from multiscale_morphology import Morphology
from simpleGUI_emum import ImageType 

class Image_collector:
    def __init__(self, filename):
        self.original = cv2.imread(filename,0)
        self.p = Pyramid(filename)
        self.m = Morphology(filename)
        self.images = {}

        self.results()
    
    def results(self):
        pyramid_image = self.p.run_algorithm()  
        morphology_image = self.m.run_algorithm()
        
        self.images={ImageType.ORIGINAL: self.original,
            ImageType.PYRAMID: pyramid_image , 
            ImageType.MORPHOLOGY: morphology_image}
    