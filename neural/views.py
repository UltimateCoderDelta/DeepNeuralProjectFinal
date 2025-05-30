from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from .models import BlogsOriginal, TabularModels, UserPostDocumentation
from .forms import UploadFileForm
import requests
import json
import pandas as pd
from .ai_models import generate_text
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
import rest_framework 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

#TO DO - Install rest framwork

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


#Working with class-based views here
class PostDocument(APIView):
    def post(self, request):
        response_data = {"user": "request"}
        return Response("POST TESTING")


@api_view(['POST', 'GET'])
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
          return Response({"error ": {str(e)}}, status=status.HTTP_400_BAD_REQUEST)
 



    
