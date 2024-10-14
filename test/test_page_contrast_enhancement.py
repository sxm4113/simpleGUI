from page_contrast_enhancement import ContrastEnhancementLayout
from simpleGUI_emum import ImageType, ProcessingType
from image_collector import Image_collector
from kivy.app import App

class MyApp(App):
    def build(self):
        cel = ContrastEnhancementLayout()
        
        filename = r'images/original_image.jpg'
        collector=Image_collector(filename) 
        cel.add_image(collector.images[ProcessingType.CONTRAST_ENHANCEMENT])
  
        return cel

if __name__ == '__main__':
    MyApp().run()
