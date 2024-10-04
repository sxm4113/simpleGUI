from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import cv2
import numpy as np

from simpleGUI_emum import ImageType

def create_texture(data):
    texture = Texture.create(size=(data.shape[1], data.shape[0]), colorfmt='luminance')
    texture.blit_buffer(data.tobytes(), colorfmt='luminance', bufferfmt='ubyte')
    texture.flip_vertical()
    return texture

class Imagelayout(Widget):
    def __init__(self, images, **kwargs):
        super(Imagelayout,self).__init__(**kwargs)
        self.images = images
        self.padding=10

        init_image = create_texture(np.ones((600,500)))
        with self.canvas.before:
            self.rect = Rectangle(texture = init_image, size=init_image.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.rect.texture = create_texture(self.images[ImageType.ORIGINAL])

    def update_image(self, img):
       self.canvas.clear()
       self.rect.texture = img

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        # self.border.rectangle = (self.x, self.y, self.width, self.height)

class ButtonLayoutBox(BoxLayout):
    def __init__(self, image_layout, **kwargs):
        super(ButtonLayoutBox,self).__init__(**kwargs)
        buttons=[]
        self.image_layout= image_layout

        with self.canvas.before:
            Color(0.4, 0.4, 0.4, 1)
            self.rect = Rectangle()
        self.bind(pos=self.update_rect, size=self.update_rect)

        button_layout = ButtonLayout(size_hint=(None,None), orientation='vertical',
                    width = 150, height = 200, pos_hint={'x':0.8,'y':0.6})

        for k, _ in self.image_layout.images.items():
            buttons.append(Button (text=k.name))

        for button in buttons:
            button.bind(on_press=self.on_button_press)
            button_layout.add_widget(button)

        self.add_widget(button_layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_button_press(self, instance):
        if instance.text == ImageType.ORIGINAL.name:
            self.image_layout.update_image(create_texture(self.image_layout.images[ImageType.ORIGINAL]))

        elif instance.text == ImageType.PYRAMID.name:
            self.image_layout.update_image(create_texture(self.image_layout.images[ImageType.PYRAMID]))

        elif instance.text == ImageType.MORPHOLOGY.name:
            self.image_layout.update_image(create_texture(self.image_layout.images[ImageType.MORPHOLOGY]))

class ButtonLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonLayout,self).__init__(**kwargs)
        self.spacing = 10
        self.padding= 10

class Mainlayout(BoxLayout):
    def __init__(self,images, **kwargs):
        super(Mainlayout,self).__init__(**kwargs)

        # Image layout
        image_layoutBox=Imagelayout(images)

        # Button layout
        button_layout_box = ButtonLayoutBox(image_layoutBox, size_hint=(None,1),width=150)

        self.add_widget(image_layoutBox)
        self.add_widget(button_layout_box)



class SimpleGUIApp(App):
    def __init__(self, images, **kwargs):
        super(SimpleGUIApp,self).__init__(**kwargs)
        self.images = images

    def build(self):
        mainPanel = Mainlayout(images=self.images, orientation='horizontal')
        return mainPanel

if __name__=="__main__":
    SimpleGUIApp().run()
