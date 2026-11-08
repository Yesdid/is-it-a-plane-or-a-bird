#import python imaging library. to open and manipulate image files
from PIL import Image

#import torch. framework that runs model
import torch 

#import feature extractor and image classification auto mode 
from transformers import AutoImageProcessor, AutoModelForImageClassification

#declare variables for extractor and model. downloads config files and neural network
processor = AutoImageProcessor.from_pretrained("chriamue/bird-species-classifier")
model = AutoModelForImageClassification.from_pretrained("chriamue/bird-species-classifier")

#open image
image = Image.open("images/bird1.jpeg") #ADD STUFF TO INTEGRATE IMAGE STUFF LATER

#convert image to model input
inputs = processor(images=image, return_tensors="pt")

#run model without gradient tracking
with torch.no_grad():
    #get image tensor
    pixel_values = inputs["pixel_values"]

    #feed image tensor to model and run inference
    outputs = model(pixel_values=pixel_values)

    #get raw prediction scores
    logits = outputs.logits

#find highest % score to determine which bird
#get raw model scores
logits = outputs.logits

#find index of largest score
predicted_class_tensor = logits.argmax(-1)

#convert tensor to int
predicted_class = predicted_class_tensor.item()

#print converted number as name of bird for top match
print("Top match: ")
print(model.config.id2label[predicted_class])

#print top 5 highest matches
print("\nTop 5 highest matches:")

#convert raw scores to probabilities
probabilities = torch.nn.functional.softmax(logits, dim=-1)

#get probabilities and indices for top 5 
top5 = torch.topk(probabilities, 5)

#print matches
for confidence_score, class_index in zip(top5.values[0], top5.indices[0]):

    bird_name = model.config.id2label[class_index.item()]
    confidence_percent = confidence_score.item() * 100

    print(f"{bird_name}: {confidence_percent:.2f}%")