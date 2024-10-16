from image_collector import ImageCollector
from simpleGUI_emum import ImageType, ProcessingType

filename = r'images/original_image.jpg'
imagescollector = ImageCollector(filename=filename)
CEimages = imagescollector.images[ProcessingType.CONTRAST_ENHANCEMENT]
for k, v in CEimages:
    print (k.name)    
imagescollector.contrast_enhancement_results()
imagescollector.classification_results()
print (type(images))