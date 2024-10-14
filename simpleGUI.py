from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.screenmanager import ScreenManager, Screen
from threading import Thread
import queue
from kivy.uix.togglebutton import ToggleButton

from image_collector import Image_collector
from page_contrast_enhancement import ContrastEnhancementLayout
from page_classification import ClassificationLayout
from simpleGUI_emum import ProcessingType 

class FirstScreen(Screen):
    def __init__(self, images, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        
        mainPanel = ClassificationLayout(images)

        self.add_widget(mainPanel)
 
class SecondScreen(Screen):
    def __init__(self, images,**kwargs):
        super(SecondScreen, self).__init__(**kwargs)
 
        mainPanel = ContrastEnhancementLayout(orientation='horizontal')
        mainPanel.add_image(images)
   
        self.add_widget(mainPanel)

class PageButtonPanel(BoxLayout):
    def __init__(self, collector, **kwargs):
        super(PageButtonPanel, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.buttons=[]

        buttonlayout = BoxLayout(orientation='horizontal',size_hint=(1,None),height=40  )
        self.buttons.append(ToggleButton(text=ProcessingType.CONTRAST_ENHANCEMENT.name))
        self.buttons.append(ToggleButton(text=ProcessingType.CLASSIFICATION.name))
        
        for button in self.buttons:
            button.bind(on_press=self.switch_to_second)        
            buttonlayout.add_widget(button)

        layout.add_widget(buttonlayout)

        self.firstScreen = FirstScreen(name=ProcessingType.CLASSIFICATION.name,
                images=collector.images[ProcessingType.CLASSIFICATION])
        self.secondScreen = SecondScreen(name=ProcessingType.CONTRAST_ENHANCEMENT.name,
                images=collector.images[ProcessingType.CONTRAST_ENHANCEMENT])
        self.sm = ScreenManager()
        self.sm.add_widget(self.firstScreen)
        self.sm.add_widget(self.secondScreen)
         
        layout.add_widget(self.sm)
        self.add_widget(layout) 
         
    def switch_to_second(self, instance):
        for button in self.buttons:
            if button.text is instance.text:
                button.state = "down"
                self.sm.current = instance.text
            else:
                button.state = "normal"
 
class SimpleGUIApp(App):
    def __init__(self, **kwargs):
        super(SimpleGUIApp,self).__init__(**kwargs)

    def build(self):
        filename = r'images/original_image.jpg'
        self._image_collector=Image_collector(filename)
        collector = self._image_collector
        self.pg = PageButtonPanel(collector) 
 
        return self.pg

class SimpleGUI(SimpleGUIApp):
    def __init__(self,image_filename,**kwargs):
        super(SimpleGUI,self).__init__(**kwargs)

        self.filename = image_filename
        self.imageQueue = queue.Queue()
        self.threads=[]
        self.threads.append(Thread(target=self.startGUI))
        self.threads.append(Thread(target=self.print_))
        # self.threads.append(Thread(target=start_image_collector, args=(image_filename, self.imageQueue)))

  
    
    def startGUI(self):
        SimpleGUIApp().run()

    def print_(self):
        print ("thread func")
    def start_image_collector(self, filename, queue):
        _image_collector=Image_collector(filename)
        queue.put(_image_collector)

    def start(self): 
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        print ("wait")
        while True:
            print ("wait")
            pass    