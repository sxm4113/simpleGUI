from torch import nn
import torch
from torchvision import models

class ClassificationModel(torch.nn.Module):
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

class InferenceClassification:
    def __init__(self, parameter_file):
        self.model = None
        self.parameter_file = parameter_file
        self.device = torch.device ("cuda") if torch.cuda.is_available() else torch.device("cpu")

    def initialize(self):
        base_model = models.vit_b_16(weights=models.ViT_B_16_Weights.DEFAULT)
        # PATH_old= r"C:\model\state_dict_model_10_7.pt"
        path = self.parameter_file
        feature_extractor = False
        self.model = ClassificationModel(base_model, feature_extractor).to(self.device)
        self.model.load_state_dict(torch.load(path, weights_only=True))
        self.model.eval() 
        
    def run_inference(self, image: torch.Tensor):
        outputs = self.model(image)
        _, preds = torch.max(outputs, 1)  # find prediction 
        return preds
        