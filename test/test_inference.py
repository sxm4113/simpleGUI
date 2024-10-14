import torch
import cv2
import util

from model_classification import ClassificationModel ,InferenceClassification

DEVICE = torch.device ("cuda") if torch.cuda.is_available() else torch.device("cpu")
print (f"using Pytorch version: {torch.__version__}, Device: {DEVICE}")

# print(pretrained_model)

  
filename=r'C:\Users\sangy\Documents\git_folder\simpleGUI\images\classification\images\IMG_0219.jpg'
img = cv2.imread(filename)
img=util.prepare_image_data(img)
image2=img.to(DEVICE).unsqueeze(dim=0)
# outputs = model_inference(image2)
# _, preds = torch.max(outputs, 1)  # find prediction

classification = InferenceClassification()
classification.initialize()
classification.run_inference(image2)

# outputs = model_inference(image2)
# _, preds = torch.max(outputs, 1)  # find prediction

# print('preds => ', preds)
