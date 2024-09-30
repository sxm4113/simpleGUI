import os
import cv2

from image_pyramid import Pyramid
from multiscale_morphology import Morphology
from simpleGUI_emum import ImageType 

class Image_collector:
    def __init__(self):
        image_file = os.path.join(os.path.dirname(__file__), 'images', 'original_image.jpg')
        image_data = cv2.imread(image_file,0)
        self.original = cv2.resize(image_data, (960, 768), interpolation = cv2.INTER_LINEAR)
        self.p = Pyramid(image_file)
        self.m = Morphology(image_file)
        self.images = {}

        self.results()
    
    def results(self):
        pyramid_image = self.p.run_algorithm()  
        morphology_image = self.m.run_algorithm()
        
        pyramid_image = cv2.resize(pyramid_image, (960, 768), interpolation = cv2.INTER_LINEAR)
        morphology_image = cv2.resize(morphology_image, (960, 768), interpolation = cv2.INTER_LINEAR)
        self.images={ImageType.ORIGINAL: self.original,
            ImageType.PYRAMID: pyramid_image , 
            ImageType.MORPHOLOGY: morphology_image}
    