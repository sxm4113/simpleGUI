from gui import SimpleGUIApp
from image_collector import Image_collector

class SimpleGUI:
    def __init__(self,image_filename):
        self.filename = image_filename

    def start(self):
        self._image_collector=Image_collector(self.filename)
        SimpleGUIApp(self._image_collector.images).run()