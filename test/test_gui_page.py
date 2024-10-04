import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from gui import Mainlayout
from image_collector import Image_collector

class Topbutton(BoxLayout):
    def __init__(self, **kwargs):
        super(Topbutton, self).__init__(**kwargs)
        buttonlayout = BoxLayout(orientation='horizontal')

        button1 = Button(text="Go to First Screen", size_hint=(0.5,None))
        button2 = Button(text="Go to Second Screen", size_hint=(0.5,None))
        buttonlayout.add_widget(button1)
        buttonlayout.add_widget(button2)
        self.add_widget(buttonlayout)
                        #, size_hint=(None,0.1), width = 400)

class FirstScreen(Screen):
    def __init__(self, images, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        b = Topbutton(size_hint=(1.0,0.1))
        button = Button(text="Go to Second Screen")
        button.bind(on_press=self.switch_to_second)
        m = Mainlayout(images)
        layout.add_widget(b)
        layout.add_widget(m)
        self.add_widget(layout)

    def switch_to_second(self, instance):
        self.manager.current = 'second'

class SecondScreen(Screen):
    def __init__(self, images, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        b = Topbutton(size_hint=(1.0,0.1))
        button1 = Button(text="Go to First Screen")
        button1.bind(on_press=self.switch_to_first)
        m = Mainlayout(images)
        layout.add_widget(b)
        layout.add_widget(m)

        self.add_widget(layout)

    def switch_to_first(self, instance):
        self.manager.current = 'first'

class MyApp(App):
    def build(self):
        filename = r'images/original_image.jpg'
        self._image_collector=Image_collector(filename)
        images = self._image_collector.images

        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first', images = images))
        sm.add_widget(SecondScreen(name='second', images = images))
        return sm

if __name__ == '__main__':
    MyApp().run()
