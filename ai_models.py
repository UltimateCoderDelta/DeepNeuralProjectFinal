#Load and operate saved ML models here
import os
import time
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img
from keras.preprocessing import image
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import django
from django.conf import settings
import pickle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deepsite.settings")

import django
django.setup()


# Use a pipeline as a high-level helper
from transformers import pipeline

# pipe = pipeline("summarization", model="Falconsai/text_summarization")

# def generate_text(input_text, model=pipe, max_length=600, min_length=55):
#   output = model(input_text, max_length=max_length, min_length=min_length)
#   return ("SUMMARY: \n" + output[0]['summary_text'])

def generate_text(text):
   return text

def get_skin_cancer_model():
    classifier_directory = os.path.join(settings.BASE_DIR, 'neural/ml_models', 'deepneural_Skin_Cancer_Detector.keras')
    #Load model
    if (classifier_directory):
       #If the file was found, load the model
       try:
          model = tf.keras.models.load_model(classifier_directory)
          return model
       except Exception:
          raise RuntimeError("The model failed to load!") 
       
def get_pneumonia_model():
    classifier_directory = os.path.join(settings.BASE_DIR, 'neural/ml_models', 'deepneural_pneumonia_detector_v1.keras')
    #Load model
    if (classifier_directory):
       #If the file was found, load the model
       try:
          model = tf.keras.models.load_model(classifier_directory)
          return model
       except Exception:
          raise RuntimeError("The model failed to load!") 

def load_sentiment_model():
    sentiment_model_path = os.path.join(settings.BASE_DIR, 'neural/ml_models', 'deepneural_sentiment_classifier_v2.keras')
    #Check if the path is correct
    if sentiment_model_path:
       #Load it
       try:
          model = tf.keras.models.load_model(sentiment_model_path)
          return model
       except Exception:
          raise RuntimeError("The model failed to load!") 

def load_sentiment_tokenizer():
    path_to_tokenizer = os.path.join(settings.BASE_DIR, 'neural/ml_models/tokenizers', 'sentiment_tokenizer.pkl')
    if path_to_tokenizer:
       return pickle.load(open(path_to_tokenizer, 'rb'))
    else:
       raise Exception("The path specified is invalid") 


def sentiment_classifier_labels():
    labels = ['Anxiety', 'Normal', 'Depression', 'Bipolar']
    label_index = dict()
    for index, status in enumerate(labels):
       if status not in label_index:
          label_index[status] = index
    
    return label_index

skin_cancer_model = get_skin_cancer_model()
pneumonia_model = get_pneumonia_model()
sentiment_model = load_sentiment_model()
sentiment_tokenizer = load_sentiment_tokenizer()
sentiment_labels = sentiment_classifier_labels()
   
def skin_cancer_classifier(user_image_path):
    if os.path.exists(user_image_path):
      print("Loaded...")
      #  If user image is not empty, predict (load model when needed)
      model = get_skin_cancer_model()

      #Load the user image from path returned by user
      skin_cancer_img = load_img(user_image_path, target_size=(224, 224))
      x = image.img_to_array(skin_cancer_img)
      x = np.expand_dims(x, axis=0)

      #Predict outcome
      image_tensor = np.vstack([x])
      classes = model.predict(image_tensor)
      if (classes[0] > 0.5):
         return (f"The following image scan is considered malignant \
          with a {(classes[0][0] * 100)}% confidence rate") 
      else:
         return (f"The following image scan is considered benign \
          with a {(classes[0][0] * 100)} confidence rate ")
    else:
       raise ValueError("No images detected or incorrect path, please reupload")
    
def pneumonia_classifier(user_image_path):
    if os.path.exists(user_image_path):
      #  If user image is not empty, predict (load model when needed)
      model = get_pneumonia_model()

      #Load the user image from path returned by user
      pneumonia_img = load_img(user_image_path, target_size=(28, 28), color_mode="grayscale")
      x = image.img_to_array(pneumonia_img)
      x = np.expand_dims(x, axis=0)

      #Predict outcome
      image_tensor = np.vstack([x])
      classes = model.predict(image_tensor)
      if (classes[0] > 0.5):
         return (f"The following image scan is considered Pneumonia \
          with a {(classes[0][0] * 100)}% confidence rate") 
      else:
         return (f"The following image scan is considered non-Pneumonia \
          with a {(classes[0][0] * 100)} confidence rate ")
    else:
       raise ValueError("No images detected, please reupload")
             
def sentiment_classifier(text):
   #Check if the text the user entered isn't empty
   if len(text) > 0:
      #Convert the text into an array
      text_list = [text]
      #Then load the model and tokenizer  
      maxlen = 200 
      model = load_sentiment_model()
      tokenizer = load_sentiment_tokenizer()
      labels = sentiment_classifier_labels()

      if (model and tokenizer and labels): #If the model, tokenizer, and labels are operational 
         #Then sequence the user input text
         sequenced_text = tokenizer.texts_to_sequences(text_list)
         #Pad the sequences for equal length
         sequenced_text = pad_sequences(sequenced_text, maxlen=maxlen, padding='post',
                                        truncating='post')
         #Perform the prediction
         prediction = model.predict(sequenced_text)

         #Gather the most likely sentiment
         prediction_index = np.argmax(prediction[0]) #Return the index of the prediction

         #Identify sentiment  
         index_label = {value: key for key, value in labels.items()}  
         prediction_result = index_label[prediction_index]
         return (f"The predicted label for the statement: \"{text}\" is considered {prediction_result}")
      else:
         raise Exception("One of the models failed to load")
   else:
      raise ValueError("The text for sentiment analysis must not be empty")
         
