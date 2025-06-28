import os
import sys
import django
from django.test import TestCase
from django.test import Client
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deepsite.settings")

django.setup()


import ai_models
import unittest
from django.conf import settings
import os
from neural import views
from django.http import HttpRequest

#Check for empty input exception
class TestAIModelsMethods(unittest.TestCase):
      client = Client() #Initializing the client

      def test_sentiment_classifier_value_test(self):
         self.assertRaises(ValueError, ai_models.sentiment_classifier, "")

      def test_check_skin_cancer_model_path(self):
          self.assertRaises(ValueError, ai_models.skin_cancer_classifier, "A_random_path")

      def test_check_pneumonia_model(self):
          self.assertRaises(ValueError, ai_models.pneumonia_classifier, "random_path")

      def test_user_sentiment_post_request(self):
          response = self.client.post("/neural/chatbot_sentiment_post/", 
                                 {"sentiment": "I feel absolutely terrible"})
          status_code = response.status_code
          #This function tests the 201 status of the call
          self.assertEqual(status_code, 201)

      #Test user sentiment get request after a positive sentiment request
      def test_user_sentiment_get_request(self):
          response = self.client.get("/neural/chatbot_sentiment/")
          self.assertEqual(response.status_code, 200)

      #Test user sentiment with no input         
      def test_user_pneumonia_post_for_empty_image(self):
           response = self.client.post("/neural/classification_upload_pneumonia/", 
                                 {"file": ""})
           status_code = response.status_code
           self.assertEqual(status_code, 400)

      def test_classification_pneumonia_get_request(self):
          response = self.client.get("/neural/classification_result_pneumonia/")
          status_code = response.status_code
          self.assertEqual(status_code, 400)

      def test_user_pneumonia_post_for_valid_image(self):
          model_path = os.path.join(settings.BASE_DIR, 'neural/ml_models', 'deepneural_pneumonia_detector_v1.keras')
          image_path = os.path.join(settings.BASE_DIR, 'media/neural', 'media/Pneumonia.png')
          if not (os.path.exists(model_path) and os.path.exists(image_path)):
              self.skipTest("The following model/image does not exist")
          #Load the image with matplotlib
          with open(image_path, 'rb') as image:
                response = self.client.post("/neural/classification_upload_pneumonia/", 
                                 {"file": image})
                self.assertEqual(response.status_code, 201)

      #Make sure to add a valid get request test for the image model here as well

      def test_user_pneumonia_post_for_invalid_image(self):
          model_path = os.path.join(settings.BASE_DIR, 'neural/ml_models', 'deepneural_pneumonia_detector_v1.keras')
          image_path = os.path.join(settings.BASE_DIR, 'media/neural', 'false_path')
          if not os.path.exists(model_path):
              self.skipTest("The following model does not exist")
              response = self.client.post("/neural/classification_upload_pneumonia/", 
                                 {"file": image_path})
              self.assertEqual(response.status_code, 400)


    #Test user summarization request for passes and failures
      def test_post_user_document_request(self):
          response = self.client.post("/neural/chatbot_request/", 
                                      {"document": "testing my model summary request"})
          self.assertEqual(response.status_code, 201)
          
      def test_get_user_document_summary_request(self):
          response = self.client.get("/neural/chatbot_summary/")
          self.assertEqual(response.status_code, 200)

    #   Write a test to ensure a user's texts are greater than 30 characters

      def test_user_document_greater_than_thirty(self):
          pass
    #Test that  the database properly registers new users
      def test_user_is_found_database(self):
          pass
      


              

if __name__ == '__main__':
    unittest.main()
