#Load and operate saved ML models here
import os
import time
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img
from keras.preprocessing import image
import numpy as np



# Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("summarization", model="Falconsai/text_summarization")

# def generate_text(input_text, model=pipe, max_length=600, min_length=80, print_time_taken=False):
#   start = time.time()
#   output = model(input_text, max_length=max_length, min_length=min_length)
#   end = time.time()
#   print(f"Total Time Elapsed: {end - start:.2f}s")
#   return ("SUMMARY: \n" + output[0]['summary_text'])

def generate_text(text):
  return text

def get_skin_cancer_model():
    classifier_directory = os.path.join('ml_models', 'deepneural_Skin_Cancer_Detector.keras')
    #Load model
    if (classifier_directory):
       #If the file was found, load the model
       try:
          model = tf.keras.models.load_model(classifier_directory)
       except Exception:
          return "The model failed to load!"
       else:
         return model
   
def skin_cancer_classifier(user_image_path):
    if user_image_path:
      #  If user image is not empty, predict (load model when needed)
      model = get_skin_cancer_model()

      #Load the user image from path returned by user
      pneumonia_img = load_img(user_image_path, target_size=(224, 224))
      x = image.img_to_array(pneumonia_img)
      x = np.expand_dims(x, axis=0)

      #Predict outcome
      image_tensor = np.vstack([x])
      classes = model.predict(image_tensor)
      if (classes[0] > 0.5):
         return f"Scan ID of {user_image_path} is considered pneumonia \
          with a {(classes[0] * 100)} confidence rate "
      else:
         return f"Scan ID of {user_image_path} is considered non-pneumonia \
          with a {(classes[0] * 100)} confidence rate "
    else:
       raise Exception("No images detected, please reupload")

