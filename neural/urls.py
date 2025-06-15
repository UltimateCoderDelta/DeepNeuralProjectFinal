from django.urls import include, path
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from neural.forms import UserLoginForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.home, name="home"),
    path("predictive_models/", views.predictive_models, name="predictive_models"),
    path("chatbot/", views.health_chatbot_pagination, name="chatbot"),
    path("pneumonia_form/", views.pneumonia_form, name="pneumonia_form"),
    path("deepneural_blog/", views.deepneural_blog, name="deepneural_blog"),
    path("deepneural_intro/", views.deepneural_blog_one, name="deepneural_intro"),
    path("tabular_models/", views.tabular_models, name="tabular_models"),
    path("tabular_models/breast_cancer_classifier/", views.breast_cancer_model_desc, name='breast_cancer_classifier'),
    path("tabular_models/heart_disease_classifier/", views.heart_disease_model_desc, name='heart_diseas_classifier'),
    path("tabular_models/diabetes_health_indicator/", views.diabetes_health_indicator, name="diabetes_health_indicator"),
    path("file_uploader/", views.upload_file, name="file_uploader"),
    path("file_uploader/deep_visual/", views.deep_visual, name="deep_visual"),
    path("chatbot_request/", views.post_user_document),
    path("chatbot_summary/", views.get_user_summary),
    path("chatbot_sentiment_post/", views.post_user_sentiment),
    path("chatbot_sentiment/", views.get_user_sentiment),
    path("classification_upload/", views.post_user_image),
    path("classification_result/", views.get_user_classification),
    path("classification_upload_pneumonia/", views.post_user_image_pneumonia),
    path("classification_result_pneumonia/", views.get_user_classification_pneumonia),
    path("sign_up/", views.sign_up, name='sign_up'),
    path("user_account/", views.user_account, name="user_account"),
    path("textual_models/", views.textual_models, name="textual_models"),
    path("vision_models/", views.vision_models, name="vision_models"),
    path("sentiment_analysis_model", views.sentiment_analysis_model, name="sentiment_analysis"),
    path("vision_models/pneumonia_predictor_model/", views.pneumonia_predictor_model, name="pneumonia_predictor_model"),
    path("vision_models/skin_cancer_predictor_model/", views.skin_cancer_predictor_model, name="skin_cancer_predictor_model"),


]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)