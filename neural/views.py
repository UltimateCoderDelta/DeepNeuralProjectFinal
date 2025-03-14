from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from .models import BlogsOriginal
# Create your views here.
def predictive_models(request):
    context = {
        "models": {

            "model_breast_desc": """
                
                        A breast cancer model designed for 
                        the prediction the prediction of early 
                        signs of breast cancer. The result is displayed
                        in a percentage of likelihood.

                        """,
                "model_pneumonia":

                    """
                    DeepNeural's Pneumonia predictor model is designed to act as an assistive tool
                    for doctors and nurses, providing a quicker diagnosis of the presence of Pneumonia
                    within a patient undergoing potential breathing difficulties. The model returns the result
                    in a terms of a percentage. 

                     """,

            "tumor_detector_desc":"""

                    An image cancer classifier model designed for 
                    the detection of tumors. The result is displayed
                    in a percentage of likelihood.

                     """
        }
    }

    return render(request,"neural/predictive_models.html", context)

def anxio(request):
    return render(request, "neural/anxio.html")

def home(request):
    return render(request, "neural/home.html")

def pneumonia_form(request):
    return render(request, "neural/pneumonia_form.html")

def deepneural_blog(request):
    all_blogs = BlogsOriginal.objects.all()
    context = {
        "blogs" : all_blogs
    }
    return render(request, "neural/deepneural_blog.html", context)

def deepneural_blog_one(request):
    return render(request, "neural/deepneural_intro.html")