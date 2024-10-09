import torch
from torch import nn
from torchvision import datasets,transforms,models
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision.io import read_image 
 
import cv2 
from PIL import Image

pretrained_model = models.vit_b_16(weights=models.ViT_B_16_Weights.DEFAULT)

DEVICE = torch.device ("cuda") if torch.cuda.is_available() else torch.device("cpu")
print (f"using Pytorch version: {torch.__version__}, Device: {DEVICE}")

# print(pretrained_model)

class MyTransferLearningModel(torch.nn.Module):

    def __init__(self, pretrained_model, feature_extractor):

        super().__init__()

        if (feature_extractor):
            for param in pretrained_model.parameters():
                param.require_grad = False

        # modify header
        pretrained_model.heads = torch.nn.Sequential(
            torch.nn.Linear(pretrained_model.heads[0].in_features, 128),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.5),
            torch.nn.Linear(128, 7) # 7 type of tomato leaves
        )

        self.model = pretrained_model

    def forward(self, data):

        logits = self.model(data)

        return logits

import os
from torchvision.io import read_image
 
PATH_old= "C:/Users/sangy/Documents/pythonCode/model/state_dict_model_10_7.pt"
base_model = models.vit_b_16(weights=models.ViT_B_16_Weights.DEFAULT)
feature_extractor = False
model_inference = MyTransferLearningModel(base_model, feature_extractor).to(DEVICE)
model_inference.load_state_dict(torch.load(PATH_old, weights_only=True))
model_inference.eval()
 
TRANSFORM = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

filename=r'C:\Users\sangy\Documents\images\tomato_leaf\test\images\IMG_0219_JPG.rf.c8d288f364390a28656a50ed7415713a.jpg'
img = cv2.imread(filename) 
image2=TRANSFORM(img).to(DEVICE).unsqueeze(dim=0)
  
outputs = model_inference(image2)
_, preds = torch.max(outputs, 1)  # find prediction
 
print('preds => ', preds)