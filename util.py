from kivy.graphics.texture import Texture
from PIL import Image
from torchvision import transforms
import numpy as np

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

def prepare_image_data(image:np.array):
 
    TRANSFORM = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor()
    ])
    img = TRANSFORM(image) 
    
    return img
 
# img = cv2.imread(filename)
# image2=TRANSFORM(img).to(DEVICE).unsqueeze(dim=0)
