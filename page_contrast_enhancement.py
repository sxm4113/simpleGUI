from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture  
import numpy as np

from simpleGUI_emum import ImageType
from image_collector import Image_collector
from util import create_texture
 
class Imagelayout(Widget):
    def __init__(self, **kwargs):
        super(Imagelayout,self).__init__(**kwargs)
        self.padding=10

        init_image = create_texture(np.zeros((1024,1280)))
        with self.canvas.before:
            self.rect = Rectangle(texture = init_image, size=init_image.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect) 

    def update_image(self, img):
       self.canvas.clear()
       self.rect.texture = img

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size 

class ButtonLayoutBox(BoxLayout):
    def __init__(self, image_layout, **kwargs):
        super(ButtonLayoutBox,self).__init__(**kwargs)
        self.buttons=[]
        self.images = {it:None for it in ImageType}
        self.image_layout= image_layout

        with self.canvas.before:
            Color(0.4, 0.4, 0.4, 1)
            self.rect = Rectangle()
        self.bind(pos=self.update_rect, size=self.update_rect)

        button_layout = ButtonLayout(size_hint=(None,None), orientation='vertical',
                    width = 150, height = 200, pos_hint={'x':0.8,'y':0.6})

        for i in ImageType:
            self.buttons.append(ToggleButton (text=i.name))

        for button in self.buttons:
            button.bind(on_press=self.on_button_press)
            button_layout.add_widget(button)

        self.add_widget(button_layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_button_press(self, instance):
        for button in self.buttons:
            if button.text != instance.text:
                button.state = "normal"
            else: 
                button.state = "down"
                self.image_layout.update_image(create_texture(self.images[ImageType[button.text]]))
 
class ButtonLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonLayout,self).__init__(**kwargs)
        self.spacing = 10
        self.padding= 10
 
class ContrastEnhancementLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ContrastEnhancementLayout,self).__init__(**kwargs)
        # Image layout
        image_layoutBox=Imagelayout() 
        # Button layout
        self.button_layout_box = ButtonLayoutBox(image_layoutBox, 
                                            size_hint=(None,1),width=150)
 
        self.add_widget(image_layoutBox) 
        self.add_widget(self.button_layout_box)

    def add_image(self, images):

        self.button_layout_box.images = images
 
if __name__=="__main__":
    SimpleGUIApp().run()
