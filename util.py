from kivy.graphics.texture import Texture

def create_texture(data):
    texture = Texture.create(size=(data.shape[1], data.shape[0]), colorfmt='luminance')
    texture.blit_buffer(data.tobytes(), colorfmt='luminance', bufferfmt='ubyte')
    texture.flip_vertical()
    return texture

def create_color_texture(data):
    texture = Texture.create(size=(data.shape[1], data.shape[0]), colorfmt='rgb')
    texture.blit_buffer(data.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
    texture.flip_vertical()
    return texture
