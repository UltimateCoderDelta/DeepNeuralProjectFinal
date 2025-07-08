from django.db import models
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from django.urls import reverse

# Create your models here.
class BlogsOriginal(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    template_name = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        data = {
            'Title': self.title,
            'Description': self.description,
            'Date Published': self.date,
            'Template Name' : self.template_name,
        }
        return str(data)


class MLModels(models.Model):
    model_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class TabularModels(models.Model):
    model_name = models.CharField(max_length=100)
    model_description = models.CharField(max_length=200)
    template_name = models.CharField(max_length=200)

    def __str__(self):
        data = {
            'Name': self.model_name,
            'Description': self.model_description,
            'Template name': self.template_name,
        }
        return str(data)
    

class ModelDecriptions(models.Model):
     model_id = models.CharField(max_length=100, primary_key=True, default='')
     model_description = models.CharField(max_length=150)
     developed_by = models.CharField(max_length=200)
     uses = models.CharField(max_length=300, blank=True)
     bias_and_risks = models.CharField(max_length=300, blank=True)
     recommendations = models.CharField(max_length=500, blank=True)
     metrics = models.CharField(max_length=200, blank=True)
     results = models.DecimalField(max_digits=3, decimal_places=2, blank=True)

     def __str__(self):
        data = {
            'Developed_by': self.developed_by,
            'Description': self.model_description,
            'Uses': self.uses,
            'Bias': self.bias_and_risks,
            'Recommendations': self.recommendations,
            'Metrics': self.metrics,
            'Results':self.results,
        }
        return str(data)
     
class UserPostDocumentation(models.Model):
    document = models.JSONField()

    def __str__(self):
        return str(self.document)

    def returnJson(self):
        return str(self.document)

class UserPostSentiment(models.Model):
    sentiment = models.JSONField()

    def __str__(self):
        return str(self.sentiment)

    def returnJson(self):
        return str(self.sentiment)
    
class UserImagePost(models.Model):
    image = models.ImageField(upload_to='neural/media')
    model_name = models.CharField(max_length=100)
    def __str__(self):
        return self.model_name
    
class UserImagePostPneumonia(models.Model):
    image = models.ImageField(upload_to='neural/mediaSec')
    model_name = models.CharField(max_length=100)
    def __str__(self):
        return self.model_name

class UserList(models.Model):
      #Creating the user creation fields
      first_name = models.CharField(max_length=20)
      last_name = models.CharField(max_length=20)
      email = models.EmailField(max_length=30, primary_key=True)
      password = models.CharField(max_length=20)
      last_login = models.DateTimeField(blank=True, null=True)
      
      error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
      def __str__(self):
          return f'User account: {self.email} has been created'
      
#Create the 
class UserListForm(ModelForm):
      class Meta:
          model = UserList
          fields = ["first_name", "last_name", "email", "password"]


class ProductListCards(models.Model):
      product_name = models.CharField(max_length=30)
      product_descr = models.CharField(max_length=200)
      href_name = models.CharField(max_length=30)

      data = {
            'product_name': product_name,
            'product_descr': product_descr,
            'href_name': href_name
      }
      def __str__(self):
         return str(self.data)

  
class ChartFileUploaderData(models.Model):
      categorical_label = models.CharField(max_length=50, null=True, blank=True)
      data_label_numeric = models.FloatField(null=True, blank=True)
      data_numeric = models.FloatField(null=True, blank=True)
      
      def __str__(self):
          return str({'catogeorical_data': self.categorical_label,
                      'data_label': self.data_label_numeric,
                      'data_numeric': self.data_numeric})
