from django.db import models

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