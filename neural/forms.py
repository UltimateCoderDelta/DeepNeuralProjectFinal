from django import forms
import pandas as pd

class UploadFileForm(forms.Form):
      label = forms.CharField(max_length=100)
      x_Axis_data = forms.CharField(max_length=100, required=False)
      csv_file = forms.FileField(required=True)

class UploadFileFormQuant(forms.Form):
      csv_file = forms.FileField()
      label = forms.CharField(max_length=100, required=True)
      x_Axis_data = forms.CharField(max_length=100, required=True)  
          
      


