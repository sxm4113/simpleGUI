import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout

from gui import create_texture
from simpleGUI_emum import ImageType
from image_collector import Image_collector

class ThumnailImage(GridLayout):
    def __init__(self, **kwargs):
        super(ThumnailImage,self).__init__(**kwargs)
        self.cols = 2
        buttons=[Button (text=str(i+10)) for i in range(4)]
        for button in buttons:
            self.add_widget(button)

class ButtonLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonLayout,self).__init__(**kwargs)
        self.spacing = 10
        self.padding= 10

class ButtonLayoutBox(FloatLayout):
    def __init__(self, **kwargs):
        super(ButtonLayoutBox,self).__init__(**kwargs)
        # self.orientation='vertical'
        buttons=[]
        with self.canvas.before:
            Color(0.4, 0.4, 0.4, 1)
            self.rect = Rectangle()
        self.bind(pos=self.update_rect, size=self.update_rect)

        ti = ThumnailImage(size_hint=(None,None), width = 100, height = 200,
                           pos_hint={'x':0.2,'y':0.7})
        button_layout = ButtonLayout(size_hint=(None,None), orientation='vertical',
                    width = 100, height = 100, pos_hint={'x':0.2,'y':0.3})

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
        if instance.text == ImageType.ORIGINAL.name:
            self.image_layout.update_image(create_texture(self.image_layout.images[ImageType.ORIGINAL]))

        elif instance.text == ImageType.PYRAMID.name:
            self.image_layout.update_image(create_texture(self.image_layout.images[ImageType.PYRAMID]))

        elif instance.text == ImageType.MORPHOLOGY.name:
            self.image_layout.update_image(create_texture(self.image_layout.images[ImageType.MORPHOLOGY]))


class MainLayout(BoxLayout):
    def __init__(self, images, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation='horizontal'
        i = Button(text='image panel')
        b = ButtonLayoutBox(size_hint=(None,1),width=150)

        self.add_widget(i)
        self.add_widget(b)

class MyApp(App):
    def build(self):
        filename = r'images/original_image.jpg'
        self._image_collector=Image_collector(filename)
        images = self._image_collector.images
        mainlayout = MainLayout(images)
        return mainlayout
if __name__ == '__main__':
    MyApp().run()
