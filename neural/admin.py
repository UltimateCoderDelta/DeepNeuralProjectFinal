from django.contrib import admin

# Register your models here.
from .models import BlogsOriginal, MLModels

admin.site.register(BlogsOriginal)
admin.site.register(MLModels)
