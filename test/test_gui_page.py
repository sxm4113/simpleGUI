import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from page_contrast_enhancement import ContrastEnhancementLayout
from image_collector import Image_collector
from simpleGUI_emum import ProcessingType

class FirstScreen(Screen):
    def __init__(self, images, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
 
        l = Label(text="1st screen")
 
        self.add_widget(l)

    def switch_to_second(self, instance):
        self.manager.current = 'second'

class SecondScreen(Screen):
    def __init__(self, images, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        mainPanel = ContrastEnhancementLayout(orientation='horizontal')
        mainPanel.add_image(images)
   
        self.add_widget(mainPanel)
 

class PageButtonPanel(BoxLayout):
    def __init__(self, images, **kwargs):
        super(PageButtonPanel, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
                
        buttonlayout = BoxLayout(orientation='horizontal',size_hint=(1,None),height=40  )
        button1 = Button(text=ProcessingType.CONTRAST_ENHANCEMENT.name)
        button2 = Button(text=ProcessingType.CLASSIFICATION.name)
        
        button1.bind(on_press=self.switch_to_second)
        button2.bind(on_press=self.switch_to_second)
        
        buttonlayout.add_widget(button1)
        buttonlayout.add_widget(button2)

        layout.add_widget(buttonlayout)

        self.sm = ScreenManager()
        self.sm.add_widget(FirstScreen(name=ProcessingType.CONTRAST_ENHANCEMENT.name, images = images))
        self.sm.add_widget(SecondScreen(name=ProcessingType.CLASSIFICATION.name, images = images))
         
        layout.add_widget(self.sm)

        self.add_widget(layout) 
    def switch_to_second(self, instance): 
        if instance.text == ProcessingType.CONTRAST_ENHANCEMENT.name:
            self.sm.current = ProcessingType.CLASSIFICATION.name
        elif instance.text == ProcessingType.CLASSIFICATION.name:
            self.sm.current = ProcessingType.CONTRAST_ENHANCEMENT.name

class MyApp(App):
    def build(self):
        filename = r'images/original_image.jpg'
        self._image_collector=Image_collector(filename)
        images = self._image_collector.images
        pg=PageButtonPanel(images) 
        return pg

if __name__ == '__main__':
    MyApp().run()
