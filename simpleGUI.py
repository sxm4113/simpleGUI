from kivy.app import App
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.screenmanager import ScreenManager, Screen
from threading import Thread
import queue
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config

from image_collector import ImageCollector
from page_contrast_enhancement import ContrastEnhancementLayout
from page_classification import ClassificationLayout
from simpleGUI_emum import ProcessingType 

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '650')

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        
        self.mainPanel = ClassificationLayout() 
        self.add_widget(self.mainPanel)
 
class SecondScreen(Screen):
    def __init__(self,**kwargs):
        super(SecondScreen, self).__init__(**kwargs)
 
        self.mainPanel = ContrastEnhancementLayout(orientation='horizontal') 
        self.add_widget(self.mainPanel)

class PageButtonPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(PageButtonPanel, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.buttons=[] 

        buttonlayout = BoxLayout(orientation='horizontal',size_hint=(1,None),height=40  )
        self.buttons.append(ToggleButton(text=ProcessingType.CONTRAST_ENHANCEMENT.name, state='down'))
        self.buttons.append(ToggleButton(text=ProcessingType.CLASSIFICATION.name))
        
        for button in self.buttons:
            button.bind(on_press=self.switch_to_second)        
            buttonlayout.add_widget(button)

        layout.add_widget(buttonlayout)

        self.firstScreen = FirstScreen(name=ProcessingType.CLASSIFICATION.name)
        self.secondScreen = SecondScreen(name=ProcessingType.CONTRAST_ENHANCEMENT.name) 

        self.sm = ScreenManager()
        self.sm.add_widget(self.firstScreen)
        self.sm.add_widget(self.secondScreen)
        self.sm.current = ProcessingType.CONTRAST_ENHANCEMENT.name
        
        layout.add_widget(self.sm)
        self.add_widget(layout) 
         
    def switch_to_second(self, instance):
        for button in self.buttons:
            if button.text is instance.text:
                button.state = "down"
                self.sm.current = instance.text
            else:
                button.state = "normal"
 
    def add_image(self, images):
        self.firstScreen.mainPanel.button_layout_panel.add_image(images[ProcessingType.CLASSIFICATION])
        self.secondScreen.mainPanel.button_layout_box.add_image(images[ProcessingType.CONTRAST_ENHANCEMENT])

class SimpleGUIApp(App):
    def __init__(self, **kwargs):
        super(SimpleGUIApp,self).__init__(**kwargs)

    def build(self):
 
        self.pg = PageButtonPanel() 
        return self.pg
  
def imageCollector(image_queue,input_info):  
    image_collector=ImageCollector(input_info)
    image_collector.classification_results()
    image_collector.contrast_enhancement_results()

    image_queue.put(image_collector.images) 
 
def app_run(app):
    try:
        app.run()
    except Exception as e:
        app.get_running_app().stop() 

class SimpleGUI():
    def __init__(self,input_info):
        self.app=SimpleGUIApp()
 
        self.imageQueue = queue.Queue()
        self.threads=[]
        self.threads.append(Thread(target=app_run, args=(self.app,)))
        self.threads.append(Thread(target=imageCollector, args=(self.imageQueue,input_info)))
   
    def start(self): 
        for thread in self.threads:
            thread.start()
                      
        while True: 
            if self.app.root is not None:
                contents = self.imageQueue.get()
                if contents is not None:         
                    imageset = contents 
                    self.app.root.add_image(imageset)
                    break
 
 
 