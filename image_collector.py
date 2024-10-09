import os
import cv2

from image_pyramid import Pyramid
from multiscale_morphology import Morphology
from simpleGUI_emum import ImageType, ProcessingType

class Image_collector:
    def __init__(self, filename):
        self.original = cv2.imread(filename,0)
        self.p = Pyramid(filename)
        self.m = Morphology(filename)
        self.images = {ProcessingType.CONTRAST_ENHANCEMENT:None,
                       ProcessingType.CLASSIFICATION:None}

        self.contrast_enhancement_results()
        self.classification_results()

    def contrast_enhancement_results(self):
        pyramid_image = self.p.run_algorithm()
        morphology_image = self.m.run_algorithm()

        self.images[ProcessingType.CONTRAST_ENHANCEMENT]={
                ImageType.ORIGINAL: self.original,
                ImageType.PYRAMID: pyramid_image ,
                ImageType.MORPHOLOGY: morphology_image
                }

    def classification_results(self):
        image_folder = os.path.join(os.path.dirname(__file__), r'images\classification')
        images = os.listdir(image_folder)


        self.images[ProcessingType.CLASSIFICATION]={
                "input_image":[cv2.imread(os.path.join(image_folder, image)) for image in images]
            }
