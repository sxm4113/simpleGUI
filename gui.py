from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Line, Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import cv2
import numpy as np

from image_collector import Image_collector
from simpleGUI_emum import ImageType

def create_texture(data):
    texture = Texture.create(size=(data.shape[1], data.shape[0]), colorfmt='luminance')
    texture.blit_buffer(data.tobytes(), colorfmt='luminance', bufferfmt='ubyte')
    texture.flip_vertical()
    return texture

class Imagelayout(Widget):
    def __init__(self, **kwargs):
        super(Imagelayout,self).__init__(**kwargs)
        init_image = create_texture(np.ones((600,500)))
        with self.canvas.before:
            self.rect = Rectangle(texture = init_image,
                size=init_image.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_image(self, img):
        self.clear_canvas()
        self.rect.texture = img

    def clear_canvas(self):
        self.canvas.clear()

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ButtonLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonLayout,self).__init__(**kwargs)
        self.spacing = 10

class Mainlayout(BoxLayout):
    def __init__(self,images, **kwargs):
        super(Mainlayout,self).__init__(**kwargs)
        self.spacing = 10
        self.images = images
        buttons =[]

        # Image layout
        self.image_layout = Imagelayout(size_hint=(1.0, 1.0) )
        self.image_layout.update_image(create_texture(self.images[ImageType.ORIGINAL]))

        # Button layout
        button_layout = ButtonLayout(size_hint=(None,None), orientation='vertical',
                    width = 160, height = 140, pos_hint={'x':0.8,'y':0.7})

        for k, _ in self.images.items():
            buttons.append(Button (text=k.name))

        for button in buttons:
            button.bind(on_press=self.on_button_press)
            button_layout.add_widget(button)

        self.add_widget(self.image_layout)
        self.add_widget(button_layout)

    def on_button_press(self, instance):
        if instance.text == ImageType.ORIGINAL.name:
            self.image_layout.update_image(create_texture(self.images[ImageType.ORIGINAL]))

        elif instance.text == ImageType.PYRAMID.name:
            self.image_layout.update_image(create_texture(self.images[ImageType.PYRAMID]))

        elif instance.text == ImageType.MORPHOLOGY.name:
            self.image_layout.update_image(create_texture(self.images[ImageType.MORPHOLOGY]))

class SimpleGUIApp(App):
    def __init__(self, filename, **kwargs):
        super(SimpleGUIApp,self).__init__(**kwargs)
        self._image_collector=Image_collector(filename)

    def build(self):
        mainPanel = Mainlayout(images=self._image_collector.images, orientation='horizontal')
        return mainPanel

if __name__=="__main__":
    SimpleGUIApp().run()
