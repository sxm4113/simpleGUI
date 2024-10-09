import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import numpy as np
import cv2

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

from simpleGUI_emum import ImageType, ProcessingType
from util import create_texture, create_color_texture
from image_collector import Image_collector

class Imagelayout(Widget):
    def __init__(self, images, **kwargs):
        super(Imagelayout,self).__init__(**kwargs)
        self.padding=10

        init_image = create_color_texture(np.ones((600,500)))
        with self.canvas.before:
            self.rect = Rectangle(texture = init_image, size=init_image.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.rect.texture = create_color_texture(images[0])

    def update_image(self, img):
       self.canvas.clear()
       self.rect.texture = img

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ThumnailImage(GridLayout):
    def __init__(self, imagelayout, images,**kwargs):
        super(ThumnailImage,self).__init__(**kwargs)
        self.cols = 2
        self.spacing=10

        self.imagelayout = imagelayout
        self.buttons = {}

        for i,image in enumerate(images):
            btn_text = f"img:{str(i)}"
            self.buttons.update({btn_text:
                {"button":ToggleButton (text=btn_text),
                 "image":image
                 }
            })
        for _, value in self.buttons.items():
            value["button"].bind(on_press=self.on_button_press)
            self.add_widget(value["button"])

    def on_button_press(self, instance):
        for key, value in self.buttons.items():
            if key is not instance.text:
                value["button"].state = "normal"
            else:
                value["button"].state = "down"
                self.imagelayout.rect.texture = create_color_texture(value["image"])

class ButtonLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonLayout,self).__init__(**kwargs)
        self.spacing = 10
        self.padding= 10

class ButtonLayoutBox(FloatLayout):
    def __init__(self, imagelayout, images, **kwargs):
        super(ButtonLayoutBox,self).__init__(**kwargs)

        buttons=[]
        with self.canvas.before:
            Color(0.4, 0.4, 0.4, 1)
            self.rect = Rectangle()
        self.bind(pos=self.update_rect, size=self.update_rect)

        ti = ThumnailImage(imagelayout, images, size_hint=(None,None), width = 120, height = 150,
                           pos_hint={'x':0.1,'y':0.75})
        button_layout = ButtonLayout(size_hint=(None,None), orientation='vertical',
                    width = 120, height = 200, pos_hint={'x':0.1,'y':0.2})

        for k in range(3):
            buttons.append(Button (text=str(k)))

        for button in buttons:
            button.bind(on_press=self.on_button_press)
            button_layout.add_widget(button)

        self.add_widget(ti)
        self.add_widget(button_layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_button_press(self, instance):
        if instance.text == '1':
            self.image_layout.update_image(create_texture(self.image_layout.images[ImageType.ORIGINAL]))

        elif instance.text == ImageType.PYRAMID.name:
            self.image_layout.update_image(create_texture(self.image_layout.images[ImageType.PYRAMID]))

        elif instance.text == ImageType.MORPHOLOGY.name:
            self.image_layout.update_image(create_texture(self.image_layout.images[ImageType.MORPHOLOGY]))


class MainLayout(BoxLayout):
    def __init__(self, images, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation='horizontal'

        i = Imagelayout(images["input_image"])

        b = ButtonLayoutBox(i, images["input_image"], size_hint=(None,1),width=150)
        self.add_widget(i)
        self.add_widget(b)

class MyApp(App):
    def build(self):
        filename = r'images/original_image.jpg'
        self._image_collector=Image_collector(filename)
        mainlayout = MainLayout(self._image_collector.images[ProcessingType.CLASSIFICATION])
        return mainlayout
if __name__ == '__main__':

    MyApp().run()
