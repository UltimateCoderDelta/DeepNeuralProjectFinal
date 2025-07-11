from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import BlogsOriginal, TabularModels, UserPostDocumentation, UserImagePost, UserImagePostPneumonia, UserPostSentiment,\
     ProductListCards, ChartFileUploaderData
from django.urls import reverse_lazy
from .forms import UploadFileForm,CustomUserCreationForm, UserDeletionConfirmation, ForgotPasswordForm, UserResetConfirmPassword,\
     ChangePasswordForm
import json
import pandas as pd
from ai_models import generate_text, skin_cancer_classifier, pneumonia_classifier, sentiment_classifier
import rest_framework 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.contrib.auth import logout, login, authenticate
import numpy as np
# Import the email modules we'll need
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def logout_form(request):
     logout(request)
     return redirect("home")

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

@login_required(login_url="login_form")
def health_chatbot_pagination(request):
    return render(request, "neural/chatbot.html") 

def handle_dataframe(df):
    features_list = [feature for feature in df.columns]
    return features_list


@login_required(login_url="login_form")
def deep_visual(request):
    """
    Function purpose: It obtains a Pandas dataframe,
    and hereafter manipulates the data according to the
    selected features for visualization
    """
    features_dict = {'error_one': '', 'error_two':''}
    if not ChartFileUploaderData.objects.exists(): #check if data exists, otherwise load charts with dummy data
           features_dict['data'] = json.dumps([" "])
           features_dict['label'] = json.dumps([20, 30, 40, 50, 30])
           return render(request, "neural/deep_visual.html", features_dict) 
    else:
        label = request.session.get('label', None) #feature name for labels
        data = request.session.get('data', None)

        # if ((data in dataset_features) or (label in dataset_features)):
        if ((label != '') and (data != '')):
            session_df = pd.DataFrame({label:ChartFileUploaderData.objects.values_list('data_label_numeric'),
                                        data:ChartFileUploaderData.objects.values_list('data_numeric')})
            data_num = [data[0] for data in session_df[data][:]]
            labels = [label[0] for label in session_df[label][:]]
            features_dict['data'] = json.dumps(data_num)
            features_dict['label'] = json.dumps(labels)
                            
        elif ((label != '') and (data == '')):
             session_df = pd.DataFrame({label:ChartFileUploaderData.objects.values_list('categorical_label')})
             value_counts = session_df[label].value_counts()
             print(value_counts)
             data = value_counts[:].to_numpy().tolist()
             labels = value_counts.index.tolist()  # Convert Index to list for JSON serialization
             features_dict['data'] = json.dumps(data)
             features_dict['label'] = json.dumps(labels)
        else:
            return redirect('file_uploader') 
        ChartFileUploaderData.objects.all().delete()
        return render(request, "neural/deep_visual.html", features_dict) 

def handle_uploaded_file(file=None):
    df = pd.read_csv(file)
    df.columns = df.columns.str.lower()
    #Check the size of the dataframe
    df_size = df.shape[0]
    print(f'Size:{df_size}')
    if df_size > 700:
       df = df[:round((0.30 * df_size))]
    print(df_size)
    return df
           
@login_required(login_url="login_form")
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
           try:
              #Check for a valid csv_conversion process
              df = handle_uploaded_file(request.FILES['csv_file'])
           except Exception as e:
              return HttpResponse(f'Error: {e}')
           else:
            data = form.cleaned_data['x_Axis_data'].lower() #get the label names
            label = form.cleaned_data['label'].lower() 
            request.session['data'] = data
            request.session['label'] = label
            request.session['dataset_features'] = list(df.columns)  # Convert to list for JSON serialization
            #Store the data in the database if the # of rows are accurate to the task (frequency or numerical charts)
            if (data != '' and label != ''): #means the user wants a numeric chart
                if (((data in df.columns) and (label in df.columns))):
                    condition_one = (df[data].shape[0] > 0) and (df[label].shape[0] > 0)
                    condition_two = (((df[data].dtype == np.float64) or (df[data].dtype == np.int64)) and ((df[label].dtype == np.int64) or \
                                    (df[label].dtype == np.float64)))
                    if (condition_one and condition_two): # if both label and data features have data
                        for i in range(df[data].shape[0]):
                            ChartFileUploaderData.objects.create(
                                data_label_numeric=df[label][i],
                                data_numeric=df[data][i],
                                categorical_label=None
                            )
                    return HttpResponseRedirect("deep_visual")
                else:
                   return redirect('file_uploader')
            elif (data == '' and label != ''): # the user wants a frequency chart
                if (label in df.columns):
                    if ((df[label].shape[0] > 0) and (df[label].dtype == object)):
                        for i in range(df[label].shape[0]):
                            ChartFileUploaderData.objects.create(
                                categorical_label=df[label][i],
                                data_label_numeric=None,
                                data_numeric=None
                            )
                    return HttpResponseRedirect("deep_visual")
                else:
                  return redirect('file_uploader')
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
         #Store the summary in the database instead
          try:
            summary = generate_text(user_data)
          except Exception as e:
             return Response({"Error: ", str(e)}, status=status.HTTP_400_BAD_REQUEST)
          else:
            user_document = UserPostDocumentation.objects.create(document={'user_document': summary})
            user_document.save()
          return Response({"document": summary}, status=status.HTTP_201_CREATED)
       except Exception as e:
         return Response({"Error: ", str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_summary(request):
    field_name = 'document'
    if request.method == "GET":
       #Then summarize the data and return it
       try:
         #Get the user data from the database instead
          user_data = UserPostDocumentation.objects.last() #returns JSON data
          field_object = UserPostDocumentation._meta.get_field(field_name)
          field_value = getattr(user_data, field_object.attname)
          # Convert the JSON data to a string
          user_document = field_value['user_document']
          if not user_document:
           raise ValueError("The document provided is empty!")    
          UserPostDocumentation.objects.all().delete()
          return Response({"summary": user_document}, status=status.HTTP_200_OK)
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
          user_data = UserImagePost.objects.filter(model_name="skin_class").last() #returns JSON data
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
          user_data = UserImagePostPneumonia.objects.filter(model_name="pneumonia").last()
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
          user_document = UserPostSentiment.objects.create(sentiment={'user_statement': user_data}) #Might add it to a dict instead
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
          user_data = UserPostSentiment.objects.last() #returns JSON data
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

@login_required
def login_form(request):
    return render(request, "/registration/login.html")
    
# Creating user accounts
def sign_up(request):
   if request.method == 'POST':
      #If the request is a post request, gather the json value from the request
      form = CustomUserCreationForm(request.POST)
      if form.is_valid(): #If the form is valid
         username = request.POST["username"]
         password = request.POST["password1"]
         form.save()
         user = authenticate(request, username=username, password=password)
         if user is not None:
            login(request, user)
         else:
            form = CustomUserCreationForm(initial={"username":"", "email":"", "password1":"", "password2":""})
         return redirect(reverse_lazy("user_account")) #Redirect the user to the welcome page 
   else:
      form = CustomUserCreationForm(initial={"username":"", "email":"", "password1":"", "password2":""})
      #TO DO: Tell the user immediately what the requirements for an username, and if said username is already taken
   return render(request, "neural/user_signup.html", {"form": form})

#User accounts page
@login_required(login_url="login_form")
def user_account(request):
   products = ProductListCards.objects.all()
   context = {
    "account_products": products,
    }
   return render(request, "neural/account_page.html", context)

@login_required(login_url="login_form")
def user_account_privacy(request):
   return render(request, "neural/account_privacy.html")

@login_required(login_url="login_form")
def user_delete_account(request):
    #After a confirmation form, delete user
    if request.method == 'POST':
        form = UserDeletionConfirmation(request.POST)
        if form.is_valid():
           try:
              confirmation = form.cleaned_data["confirm_deletion"].strip()
           except Exception as e:
               HttpResponse(f'Error: {e}')
           else:
             if confirmation == "delete_account":
              #If the value is delete_account, delete the user account associated with the current user
              request.user.delete()
              return redirect("home")        
    else:
        form = UserDeletionConfirmation()
    return render(request, "neural/deletion_confirmation.html", {'form': form})


@login_required(login_url="login_form")
def user_account_settings(request):
    current_user = request.user
    user_current = {
       "username":current_user.username,
    #    "name": current_user.full_name,
       "last_login":current_user.last_login,
       "date_joined": current_user.date_joined,
       "email": current_user.email,
       "id": current_user.id,
    }

    return render(request, "neural/account_settings.html", user_current)

@login_required(login_url="login_form")
def user_account_security(request):
    current_user = request.user
    user_current = {
       "email": current_user.email,
       "id": current_user.id,
    }
    return render(request, "neural/account_security.html", user_current)

def textual_models(request):
    return render(request, "neural/textual_models.html")

def email_sent(request):
   return render(request, "registration/email_sent.html")


def vision_models(request):
   return render(request, "neural/vision_models.html")

def sentiment_analysis_model(request):
   return render(request, "neural/sentiment_analysis_model.html")

def pneumonia_predictor_model(request):
   return render(request, "neural/image_classification_models_pneumonia.html")

def skin_cancer_predictor_model(request):
   return render(request, "neural/image_classification_models_skin_cancer.html")
      
# @login_required(login_url="login_form")
def password_reset(request):
    #After a confirmation form, delete user
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
           try:
              user_email = form.cleaned_data["email"]
              if user_email == "":
                 raise ValueError("Email is empty!")
              print(user_email)
           except Exception as e:
               return HttpResponse(f'Error: {e}')
           else:
             with open('./neural/templates/email/email_content.txt') as mail:
                content = mail.read()
             send_mail(
                "DeepNeural Password Change Request",
                content,
                "deepneuralgeneral@gmail.com",
                [user_email],
                fail_silently=False,
             )
            #Redirect to login page
        return redirect("email_confirm")        
    else:
        form = ForgotPasswordForm()
    return render(request, "registration/password_reset_form.html", {'form': form})

@login_required(login_url='login_form')
def password_change_form(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
            #If form is valid, check that the passwords match
                user = request.user
                old_password = form.cleaned_data['old_password'].strip()
                password1 = form.cleaned_data['password1'].strip()
                password2 = form.cleaned_data['password2'].strip()
                #Check if the email address is in the database, and if so, save this user
            except Exception as e:
                return HttpResponse(f'Error: {e}')
            else:
                #Check that the passwords match
                if user is not None: #if the user exists
                    #Check if the old password matches what is in the Users DB
                    if user.check_password(old_password):
                    #If it matches proceed with the other password checkups
                        if password1 == password2:
                            #Then proceed to change the user password
                            user.set_password(password1)
                            print(f"Changing password for: {user.username} (id={user.id})")
                            user.save()
                            return redirect('password_change_done') #TO DO CREATE VIEW
                        #if invalid, stay on the form
                        else:
                            return redirect('password_change_form') 
                                     
    else:
      form = ChangePasswordForm()
    return render(request, "registration/password_change_form.html", {'form': form})

@login_required(login_url="login_form")
def password_change_done(request):
   return render(request, "registration/password_change_done.html")

def password_reset_confirm(request):
   if request.method == "POST":
      form = UserResetConfirmPassword(request.POST)
      if form.is_valid():
        try:
         #If form is valid, check that the passwords match
            password1 = form.cleaned_data['password1'].strip()
            password2 = form.cleaned_data['password2'].strip()
            username = form.cleaned_data['username'].strip()
            print(username)
            #Check if the email address is in the database, and if so, save this user
        except Exception as e:
            return HttpResponse(f'Error: {e}')
        else:
         #Check that the passwords match
         if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username) #collect the user by username
            if password1 == password2:
                #Then proceed to change the user password
                user.set_password(password1)
                print(f"Changing password for: {user.username} (id={user.id})")
                user.save()
                return redirect('login_form')
            #if invalid, stay on the form
            else:
               return redirect('password_reset_confirm')
            #If successful, try redirect to log
   else:
      form = UserResetConfirmPassword()
   return render(request, "registration/password_reset_confirm.html", {'form': form})

#User settings update class-based views
class UpdateUsername(UpdateView):
   model = User
   fields = ["username"]
   template_name = 'neural/username_update_form.html'
   success_url = reverse_lazy('user_account')

class UpdateEmail(UpdateView):
   model = User
   fields = ["email"]
   template_name = 'neural/email_update_form.html'
   success_url = reverse_lazy('user_account')

