import torch
from torch import nn
from torchvision import datasets,transforms,models
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import  models

import os


# pretrained_model = models.vit_b_16(weights=models.ViT_B_16_Weights.DEFAULT)
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

# feature_extractor = False  # True for Feature Extractor,  False for Fine Tuning

# model = MyTransferLearningModel(pretrained_model, feature_extractor).to(DEVICE)

# loss_function = torch.nn.CrossEntropyLoss()

# optimizer = torch.optim.Adam(model.parameters(), lr = 1e-6)

TEST_DATA_ROOT_DIR = 'images/classification/'
check_label_directory = os.path.join(TEST_DATA_ROOT_DIR, 'labels')
check_image_directory = os.path.join(TEST_DATA_ROOT_DIR, 'images')

labels = os.listdir(check_label_directory)
print (len(labels))
