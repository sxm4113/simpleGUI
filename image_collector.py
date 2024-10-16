import os
import cv2
import torch

from image_pyramid import Pyramid
from multiscale_morphology import Morphology
from simpleGUI_emum import ImageType, ProcessingType, Classification_Label
from model_classification import InferenceClassification
from util import prepare_image_data 

class ImageCollector:
    def __init__(self, input_info):
        self.images = {}
        self.input_info = input_info

        self.p = Pyramid(self.input_info['image_file'])
        self.m = Morphology(self.input_info['image_file'])
        
        original = cv2.imread(self.input_info['image_file'],0)        
        self.images.update({ProcessingType.CONTRAST_ENHANCEMENT:{ImageType.ORIGINAL:original}})
        self.images[ProcessingType.CLASSIFICATION]={}

        image_folder = os.path.join(os.path.dirname(__file__),self.input_info['image_folder'])
        imagefile_list = os.listdir(image_folder)

        for idx, image in enumerate(imagefile_list):
            self.images[ProcessingType.CLASSIFICATION].update(
            {str(idx):{'image':cv2.imread(os.path.join(image_folder, image))}})
  
    def contrast_enhancement_results(self):
        pyramid_image = self.p.run_algorithm()
        morphology_image = self.m.run_algorithm()

        self.images[ProcessingType.CONTRAST_ENHANCEMENT].update({
                ImageType.PYRAMID: pyramid_image ,
                ImageType.MORPHOLOGY: morphology_image
                })

    def classification_results(self):
        DEVICE = torch.device ("cuda") if torch.cuda.is_available() else torch.device("cpu")

        classification = InferenceClassification(self.input_info['parameter_file'])
        classification.initialize()

        imageset = self.images[ProcessingType.CLASSIFICATION]

        for k,v in imageset.items():
            img=prepare_image_data(v["image"])
            image=img.to(DEVICE).unsqueeze(dim=0)
            outputs = classification.run_inference(image) 
            label=Classification_Label(outputs.item()).name
            v.update({"result":label})