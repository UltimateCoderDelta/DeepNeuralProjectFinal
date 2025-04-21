from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("predictive_models/", views.predictive_models, name="predictive_models"),
    path("chatbot/", views.anxio, name="chatbot"),
    path("pneumonia_form/", views.pneumonia_form, name="pneumonia_form"),
    path("deepneural_blog/", views.deepneural_blog, name="deepneural_blog"),
    path("deepneural_intro/", views.deepneural_blog_one, name="deepneural_intro"),
    path("tabular_models/", views.tabular_models, name="tabular_models"),
    path("tabular_models/breast_cancer_classifier/", views.breast_cancer_model_desc, name='breast_cancer_classifier'),
    path("tabular_models/heart_disease_classifier/", views.heart_disease_model_desc, name='heart_diseas_classifier'),
    path("tabular_models/diabetes_health_indicator/", views.diabetes_health_indicator, name="diabetes_health_indicator"),
]