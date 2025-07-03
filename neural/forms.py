from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UploadFileForm(forms.Form):
      label = forms.CharField(max_length=100)
      x_Axis_data = forms.CharField(max_length=100, required=False)
      csv_file = forms.FileField(required=True)

class UploadFileFormQuant(forms.Form):
      csv_file = forms.FileField()
      label = forms.CharField(max_length=100, required=True)
      x_Axis_data = forms.CharField(max_length=100, required=True)  
          
      
#Creating the user login form
class UserLoginForm(AuthenticationForm):
      """
      The user creation form, designed to ensure the use can access
      crucial DeepNeural features, such as the visualization and chatbot
      features.
      """
      def __init__(self, *args, **kwargs):
           super(UserLoginForm, self).__init__(*args, **kwargs)
           self.fields['username'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Username',
           })
           self.fields['password'].widget.attrs.update({
             'class': 'form-control',
             'placeholder': 'Password'
           })
      # username = forms.CharField(max_length=20, required=True, widget=TextInput(attrs={'placeholder': 'Username'}))
      # password = forms.CharField(max_length=20, widget=PasswordInput(attrs={'placeholder': 'Password'}))


class UserSignupForm(forms.Form):
      first_name = forms.CharField(max_length=20)
      last_name = forms.CharField(max_length=20)
      email = forms.EmailField(max_length=30)
      password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class UserDeletionConfirmation(forms.Form):
      confirm_deletion = forms.CharField(max_length=20)

      def __str__(self):
           return self.confirm_deletion
      
class ForgotPasswordForm(forms.Form):
      email = forms.EmailField(max_length=50)

      def __str__(self):
          return self.confirm_deletion

