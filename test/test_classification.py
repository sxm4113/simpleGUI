import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import numpy as np 

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.label import Label 
import torch
from simpleGUI_emum import ProcessingType, Classification_Label, Model_enum
from util import create_color_texture, prepare_image_data 
from model_classification import InferenceClassification

class Imagelayout(FloatLayout):
    def __init__(self, **kwargs):
        super(Imagelayout,self).__init__(**kwargs)
        self.padding=10
        self.result_label = Label(text="",pos_hint={'x_center':0. ,'y':-0.4 }, font_size = '30dp')
        init_image = create_color_texture(np.zeros((1024,1280)))
        with self.canvas.before:
            self.rect = Rectangle(texture = init_image, size=init_image.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect) 
        self.add_widget(self.result_label)
    def update_image(self, img):
       self.canvas.clear()
       self.rect.texture = img

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ThumnailImage(GridLayout):
    def __init__(self, imagelayout,**kwargs):
        super(ThumnailImage,self).__init__(**kwargs)
        self.cols = 2
        self.spacing=10

        self.imagelayout = imagelayout
        self.images=None
        self.buttons = []
        self.clicked_button = None

        for i in range(4):
            btn_text = str(i)
            self.buttons.append(ToggleButton (text=btn_text))

        for button in self.buttons:
            button.bind(on_press=self.on_button_press)
            button.disabled = True
            self.add_widget(button)

    def add_image (self, images):
        self.images = images
        for button in self.buttons: 
            button.disabled = False

    def on_button_press(self, instance):
        for button in self.buttons:
            if button.text is not instance.text:
                button.state = "normal"
            else:
                self.clicked_button = instance.text
                button.state = "down"
                self.imagelayout.rect.texture = create_color_texture(self.images[instance.text]['image'])
                self.imagelayout.result_label.text = ""

class ButtonLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonLayout,self).__init__(**kwargs)
        self.spacing = 10
        self.padding= 10

class inputlabel(Widget):
    def __init__(self, **kwargs):
        super(inputlabel,self).__init__(**kwargs)
        input_label= Label(text="Input Image")
        btn = Button(text='aa')
        self.add_widget(btn)

class ButtonLayoutPanel(FloatLayout):
    def __init__(self, imagelayout, **kwargs):
        super(ButtonLayoutPanel,self).__init__(**kwargs)

        self.images = None
        self.imagelayout = imagelayout
        self.buttons=[]
        with self.canvas.before:
            Color(0.4, 0.4, 0.4, 1)
            self.rect = Rectangle()
        self.bind(pos=self.update_rect, size=self.update_rect)

        input_label = Label(text="Input Image", size_hint=(None,None), width = 100, height = 20,
                                             pos_hint={'x':0.2,'y':0.9})
        

        self.thumnail_image = ThumnailImage(self.imagelayout, size_hint=(None,None), width = 120, height = 150,
                           pos_hint={'x':0.1,'y':0.65})
        self.button_layout = ButtonLayout(size_hint=(None,None), orientation='vertical',
                    width = 150, height = 80*len(Model_enum), pos_hint={'x':0.01,'y':0.2})

        for k in Model_enum:
            self.buttons.append(Button (text=k.name))

        for button in self.buttons:
            button.bind(on_press=self.on_button_press)
            button.disabled=True
            self.button_layout.add_widget(button)
        
        self.add_widget(input_label)
        self.add_widget(self.thumnail_image)
        self.add_widget(self.button_layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def add_image (self, images):
        self.images = images 
        self.thumnail_image.add_image(images)
        for button in self.buttons: 
            button.disabled=False 

    def on_button_press(self, instance): 
        if instance.text == Model_enum.VisionTransformer.name: 
            clicked_key = self.thumnail_image.clicked_button
            self.imagelayout.result_label.text = self.images[clicked_key]['result']

class ClassificationLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ClassificationLayout, self).__init__(**kwargs)
        self.orientation='horizontal'
        self.DEVICE = torch.device ("cuda") if torch.cuda.is_available() else torch.device("cpu")

        self.classification = InferenceClassification()
        self.classification.initialize()


        self.image_layout = Imagelayout()
        self.button_layout_panel = ButtonLayoutPanel(self.image_layout , size_hint=(None,1),width=150)
          
        self.add_widget(self.image_layout)
        self.add_widget(self.button_layout_panel)

class MyApp(App):
    def build(self):
             
        mainlayout = ClassificationLayout()
        return mainlayout

if __name__ == '__main__':

    MyApp().run()
 
