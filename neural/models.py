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