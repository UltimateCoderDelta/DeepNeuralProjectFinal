from django import forms
import pandas as pd

from django.contrib.auth.forms import UserCreationForm

class UploadFileForm(forms.Form):
      label = forms.CharField(max_length=100)
      x_Axis_data = forms.CharField(max_length=100, required=False)
      csv_file = forms.FileField(required=True)

class UploadFileFormQuant(forms.Form):
      csv_file = forms.FileField()
      label = forms.CharField(max_length=100, required=True)
      x_Axis_data = forms.CharField(max_length=100, required=True)  
          
      
#Creating the user login form
class UserLoginForm(forms.Form):
      """
      The user creation form, designed to ensure the use can access
      crucial DeepNeural features, such as the visualization and chatbot
      features.
      """
      email_field = forms.CharField(max_length=20, required=True)
      password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class UserSignupForm(forms.Form):
      first_name = forms.CharField(max_length=20)
      last_name = forms.CharField(max_length=20)
      email = forms.EmailField(max_length=30)
      password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)