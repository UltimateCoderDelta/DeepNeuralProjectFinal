from django.contrib import admin

# Register your models here.
from .models import BlogsOriginal, MLModels, TabularModels, ModelDecriptions

admin.site.register(BlogsOriginal)
admin.site.register(MLModels)
admin.site.register(TabularModels)
admin.site.register(ModelDecriptions)
