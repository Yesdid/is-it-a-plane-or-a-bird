#import python imaging library. to open and manipulate image files
from PIL import Image

#import torch. framework that runs model
import torch 

#import feature extractor and image classification auto mode 
from transformers import AutoImageProcessor, AutoModelForImageClassification

#declare variables for extractor and model. downloads config files and neural network
processor = AutoImageProcessor.from_pretrained("chriamue/bird-species-classifier")
model = AutoModelForImageClassification.from_pretrained("chriamue/bird-species-classifier")

def analyze_image(img): 
    #open image
    image = Image.open(img) #ADD STUFF TO INTEGRATE IMAGE STUFF LATER

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

    #get raw model scores
    logits = outputs.logits

    #convert raw scores to probabilities
    probabilities = torch.nn.functional.softmax(logits, dim=-1)

    #get probabilities and indices for top 5
    top5 = torch.topk(probabilities, 5)

    # create dictionary
    top5_predictions = {}

    #add names and confidene to dictionary
    for confidence_score, class_index in zip(top5.values[0], top5.indices[0]):
        bird_name = model.config.id2label[class_index.item()]
        confidence_percent = confidence_score.item() * 100

        top5_predictions[bird_name] = confidence_percent

    #return predictions
    return top5_predictions
