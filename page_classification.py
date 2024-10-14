from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label 
import torch
import numpy as np

from simpleGUI_emum import ProcessingType, Classification_Label, Model_enum
from util import create_color_texture, prepare_image_data
from image_collector import Image_collector
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
    def __init__(self, imagelayout, images,**kwargs):
        super(ThumnailImage,self).__init__(**kwargs)
        self.cols = 2
        self.spacing=10

        self.imagelayout = imagelayout
        self.buttons = {}
        self.clicked_button = None

        for k,v in images.items():
            btn_text = k
            self.buttons.update({btn_text:
                {"button":ToggleButton (text=btn_text),
                 "image":v['image']
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
                self.clicked_button = key
                value["button"].state = "down"
                self.imagelayout.rect.texture = create_color_texture(value["image"])
                self.imagelayout.result_label.text = ""

class ButtonLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonLayout,self).__init__(**kwargs)
        self.spacing = 10
        self.padding= 10

class ButtonLayoutBox(FloatLayout):
    def __init__(self, imagelayout, images, **kwargs):
        super(ButtonLayoutBox,self).__init__(**kwargs)

        self.images = images
        self.imagelayout = imagelayout
        buttons=[]
        with self.canvas.before:
            Color(0.4, 0.4, 0.4, 1)
            self.rect = Rectangle()
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.thumnail_image = ThumnailImage(self.imagelayout, images, size_hint=(None,None), width = 120, height = 150,
                           pos_hint={'x':0.1,'y':0.65})
        self.button_layout = ButtonLayout(size_hint=(None,None), orientation='vertical',
                    width = 150, height = 80*len(Model_enum), pos_hint={'x':0.01,'y':0.2})

        for k in Model_enum:
            buttons.append(Button (text=k.name))

        for button in buttons:
            button.bind(on_press=self.on_button_press)
            self.button_layout.add_widget(button)

        self.add_widget(self.thumnail_image)
        self.add_widget(self.button_layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_button_press(self, instance): 
        if instance.text == Model_enum.VisionTransformer.name: 
            clicked_key = self.thumnail_image.clicked_button
            self.imagelayout.result_label.text = self.images[clicked_key]['result']

class ClassificationLayout(BoxLayout):
    def __init__(self, images, **kwargs):
        super(ClassificationLayout, self).__init__(**kwargs)
        self.orientation='horizontal'
        DEVICE = torch.device ("cuda") if torch.cuda.is_available() else torch.device("cpu")

        classification = InferenceClassification()
        classification.initialize()
        for k,v in images.items():
            img=prepare_image_data(v['image'])
            image=img.to(DEVICE).unsqueeze(dim=0)
            outputs = classification.run_inference(image) 
            label=Classification_Label(outputs.item()).name
            v.update({'result':label})
              
        i = Imagelayout()

        b = ButtonLayoutBox(i, images , size_hint=(None,1),width=150)
        self.add_widget(i)
        self.add_widget(b)
