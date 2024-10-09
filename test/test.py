from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.core.image import Image

class ImageButton(Button):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        with self.canvas.before:
            self.texture = Image('images/image2.jpg').texture
            self.rect = Rectangle(texture=self.texture, pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class TestApp(App):
    def build(self):
        return ImageButton(size_hint=(.3, .3), pos_hint={'center_x': 0.5, 'center_y': 0.5})

if __name__ == '__main__':
    TestApp().run()
