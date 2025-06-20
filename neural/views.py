from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import BlogsOriginal, TabularModels, UserPostDocumentation, UserImagePost, UserImagePostPneumonia, UserPostSentiment,\
     ProductListCards 
from django.urls import reverse
from .forms import UploadFileForm,CustomUserCreationForm
import json
import pandas as pd
from ai_models import generate_text, skin_cancer_classifier, pneumonia_classifier, sentiment_classifier
import rest_framework 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import login



# Create your views here.
def predictive_models(request):
    context = {
        "models": {

            "model_breast_desc": """
                
                        A breast cancer model designed for 
                        the prediction the prediction of early 
                        signs of breast cancer. The result is displayed
                        in a percentage of likelihood.

                        """,
                "model_pneumonia":

                    """
                    DeepNeural's Pneumonia predictor model is designed to act as an assistive tool
                    for doctors and nurses, providing a quicker diagnosis of the presence of Pneumonia
                    within a patient undergoing potential breathing difficulties. The model returns the result
                    in a terms of a percentage. 

                     """,

            "tumor_detector_desc":"""

                    An image cancer classifier model designed for 
                    the detection of tumors. The result is displayed
                    in a percentage of likelihood.

                     """
        }
    }

    return render(request,"neural/predictive_models.html", context)

def anxio(request):
    return render(request, "neural/anxio.html")

def home(request):
    return render(request, "neural/home.html")

def pneumonia_form(request):
    return render(request, "neural/pneumonia_form.html")

def deepneural_blog(request):
    all_blogs = BlogsOriginal.objects.all()
    context = {
        "blogs" : all_blogs
    }
    return render(request, "neural/deepneural_blog.html", context)

def deepneural_blog_one(request):
    return render(request, "neural/deepneural_intro.html")

def tabular_models(request):
    tabular_mls = TabularModels.objects.all()
    context = {
        "tabular_models": tabular_mls
    }
    return render(request, "neural/tabular_models.html", context)

def breast_cancer_model_desc(request):
    return render(request, "neural/breast_cancer_classifier.html")

def heart_disease_model_desc(request):
    return render(request, "neural/heart_disease_classifier.html")

def diabetes_health_indicator(request):
    return render(request, "neural/diabetes_health_indicator.html")

def health_chatbot_pagination(request):
    return render(request, "neural/chatbot.html") 

def handle_dataframe(df):
    features_list = [feature for feature in df.columns]
    return features_list

def deep_visual(request):
    """
    Function purpose: It obtains a Pandas dataframe,
    and hereafter manipulates the data according to the
    selected features for visualization
    """
    session_df = request.session.get('converted_csv', None)
    features_dict = {}
    if (session_df is None):
         features_dict['data'] = json.dumps([" "])
         features_dict['label'] = json.dumps([20, 30, 40, 50, 30])
    else:
        label = request.session.get('label', None) #feature name for labels
        data = request.session.get('data', None)
        session_df = pd.read_json(session_df) 
        #Create empty features dictionary
        # Initially check if label is not empty and data is empty
        if ((label != '') and (data == '')):
            # The user wants a frequency chart (default)
            data = session_df[label].value_counts()[:].to_numpy().tolist()
            labels = session_df[label].unique().tolist()
            features_dict['data'] = json.dumps(data)
            features_dict['label'] = json.dumps(labels)
        
        elif ((label != '') and (data != '')):
            # The user wants a quantitative chart (non-default and explicit)
            data = session_df[data][:].to_list()
            labels = session_df[label][:].to_list()
            features_dict['data'] = json.dumps(data)
            features_dict['label'] = json.dumps(labels)
     
    return render(request, "neural/deep_visual.html", features_dict)
    
#For the file upload
#Handle the uploaded file with pandas and do what must be done
def handle_uploaded_file(file=None):
    df = pd.read_csv(file)
    return df

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
           try:
              df = handle_uploaded_file(request.FILES['csv_file'])
           except Exception as e:
               HttpResponse(f'Error: {e}')
           else:
            request.session['data'] = form.cleaned_data['x_Axis_data'] #Gather the data feature name
            request.session['label'] = form.cleaned_data['label'] #Gather the label feature name
            
            request.session['converted_csv'] = df.to_json() #attempt without converting to JSON
            return HttpResponseRedirect("deep_visual")
    else:
        form = UploadFileForm()
    return render(request, "neural/file-uploader.html", {'form': form})


@api_view(['POST'])
def post_user_document(request):
    """
    This function will allow the user to post their
    data, which will be accessed by a seperate view
    """ 
    if request.method == "POST":
       #We expect a JSON object
       try:
          user_data = request.data.get("document")
          if not user_data:
            raise ValueError("The document provided is empty!")
         #Post the as JSON to the database
          user_document = UserPostDocumentation.objects.create(document={'user_document': user_data})
          user_document.save()
          return Response({"document": user_data}, status=status.HTTP_201_CREATED)
       except Exception as e:
         return Response({"Error: ", str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_user_summary(request):
    field_name = 'document'
    if request.method == "GET":
       #Then summarize the data and return it
       try:
         #Get the user data from the database instead
          user_data = UserPostDocumentation.objects.first() #returns JSON data
          field_object = UserPostDocumentation._meta.get_field(field_name)
          field_value = getattr(user_data, field_object.attname)
          # Convert the JSON data to a string
          user_document = field_value['user_document']
          if not user_document:
           raise ValueError("The document provided is empty!")    
        #   user_data = json.loads(json_str)      
          summarized_data = generate_text(user_document)
          #Delete all data from the database for the next request
          UserPostDocumentation.objects.all().delete()
          return Response({"summary": summarized_data}, status=status.HTTP_200_OK)
       except Exception as e:
          return Response({"error ": str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['POST'])
def post_user_image(request):
    """
    This function will allow the user to post their
    image files, which will be accessed by a seperate view
    """ 
    if request.method == "POST":
       #We expect a JSON object
       try:
          user_image = request.FILES.get("file")
          if not user_image:
            raise ValueError("The file provided is empty or incorrect!")
         #Post the as JSON to the IMAGE FILE database (TO DO)
          user_document = UserImagePost.objects.create(image=user_image, model_name="skin_class")
          user_document.save()
          return Response({"image": user_image.name}, status=status.HTTP_201_CREATED)
       except Exception as e:
         return Response({"Error: ", str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_classification(request):
    if request.method == "GET":
       #Then predict the image result
       try:
         #Get the user data from the database instead
          user_data = UserImagePost.objects.filter(model_name="skin_class").first() #returns JSON data
          image_path = user_data.image.path
        #   user_image = getattr(user_data, field_object.attname)
          # Convert the JSON data to a string
          if not image_path:
           raise ValueError("The image provided is not available!")    
        #   user_data = json.loads(json_str)      
          predicted_result = skin_cancer_classifier(image_path)
          UserImagePost.objects.all().delete()
          return Response({"prediction": predicted_result}, status=status.HTTP_200_OK)
       except Exception as e:
          return Response({"error ": str(e)}, status=status.HTTP_400_BAD_REQUEST)
       
@api_view(['POST'])
def post_user_image_pneumonia(request):
    """
    This function will allow the user to post their
    image files, which will be accessed by a seperate view
    """ 
    if request.method == "POST":
       #We expect a JSON object
       try:
          user_image = request.FILES.get("file")
          if not user_image:
            raise ValueError("The file provided is empty or incorrect!")
         #Post the as JSON to the IMAGE FILE database (TO DO)
          user_document = UserImagePostPneumonia.objects.create(image=user_image, model_name="pneumonia")
          user_document.save()
          return Response({"image": user_image.name}, status=status.HTTP_201_CREATED)
       except Exception as e:
         return Response({"Error: ", str(e)}, status=status.HTTP_400_BAD_REQUEST)
       

@api_view(['GET'])
def get_user_classification_pneumonia(request):
    if request.method == "GET":
       #Then predict the image result
       try:
         #Get the user data from the database instead
          user_data = UserImagePostPneumonia.objects.filter(model_name="pneumonia").first()
          image_path = user_data.image.path
        #   user_image = getattr(user_data, field_object.attname)
          # Convert the JSON data to a string
          if not image_path:
           raise ValueError("The image provided is not available!")    
        #   user_data = json.loads(json_str)      
          predicted_result = pneumonia_classifier(image_path)
          UserImagePostPneumonia.objects.all().delete()
          return Response({"prediction_pneumonia": predicted_result}, status=status.HTTP_200_OK)
       except Exception as e:
          return Response({"error ": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def  post_user_sentiment(request):
    """
    This function will allow the user to post their
    sentiment, which will be accessed by a seperate view
    """ 
    if request.method == "POST":
       #We expect a JSON object
       try:
          user_data = request.data.get("sentiment")
          if len(user_data) < 1:
            raise ValueError("The sentiment text provided is empty!")
         #Post the as JSON to the database
          user_document = UserPostSentiment.objects.create(sentiment={'user_statement': user_data})
          user_document.save()
          return Response({"statement": user_data}, status=status.HTTP_201_CREATED)
       except Exception as e:
         return Response({"Error: ", str(e)}, status=status.HTTP_400_BAD_REQUEST)
       
@api_view(['GET'])
def get_user_sentiment(request):
    field_name = 'sentiment'
    if request.method == "GET":
       #Then develop the sentiment for the text
       try:
         #Get the user data from the database instead
          user_data = UserPostSentiment.objects.first() #returns JSON data
          field_object = UserPostSentiment._meta.get_field(field_name)
          field_value = getattr(user_data, field_object.attname)
          # Convert the JSON data to a string
          user_sentiment = field_value['user_statement']
          if not user_sentiment:
           raise ValueError("The text provided is empty!")    
        #   user_data = json.loads(json_str)      
          sentiment_data = sentiment_classifier(user_sentiment) #Change the function
          #Delete all data from the database for the next request
          UserPostSentiment.objects.all().delete()
          return Response({"sentiment_prediction": sentiment_data}, status=status.HTTP_200_OK)
       except Exception as e:
          return Response({"error ": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Creating user accounts
def sign_up(request):
   if request.method == 'POST':
      #If the request is a post request, gather the json value from the request
      form = CustomUserCreationForm(request.POST)
      if form.is_valid(): #If the form is valid
        user = form.save()
        login(request, user)
        return redirect(reverse("home")) #Redirect the user to the welcome page 
   else:
      form = CustomUserCreationForm()
   return render(request, "neural/user_signup.html", {"form": form})

#User accounts page
def user_account(request):
   products = ProductListCards.objects.all()
   context = {
    "account_products": products,
    }
   return render(request, "neural/account_page.html", context)

def textual_models(request):
    return render(request, "neural/textual_models.html")


def vision_models(request):
   return render(request, "neural/vision_models.html")

def sentiment_analysis_model(request):
   return render(request, "neural/sentiment_analysis_model.html")

def pneumonia_predictor_model(request):
   return render(request, "neural/image_classification_models_pneumonia.html")

def skin_cancer_predictor_model(request):
   return render(request, "neural/image_classification_models_skin_cancer.html")