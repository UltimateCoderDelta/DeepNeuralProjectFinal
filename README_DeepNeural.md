
# DeepNeural Project Installation Guide

==========================================================
Summary: DeepNeural was build with the Django framework, and therefore to ensure a proper duplication 
of the following project is possible, it is recommended to follow the steps below for local development:

- <i class="fas fa-check"></i> Create a virtual environment 
  `
    python -m venv .venv 
  `
- Install the necessary packages: 

  1. TensorFlow
  2. django-cors-headers
  3. Keras
  4. HuggingFace Transformers
  5. Django
  6. django-rest-framework

All of these libraries and framworks can be properly installed as follows in the terminal

---
 TensorFlow:

  `pip install tensorflow`

django-cors-headers:

`pip install django-cors-headers`

Keras

`pip install keras`

Hugging Face Transformers

`pip install transformers`

Django

`pip install django`

django-rest-framework

`pip install django-rest-framework`


---

# Running the Django Application

=================================================================

Upon having completed the above installation processes, it is now 
officially time to check whether django is officially installed. First, navigate the project directory - in this case *DeepNeuralFinal*. Then proceed with running migrations to ensure all database objects are correctly stored. Follow the code instructions below.

```

cd DeepNeuralFinal

python manage.py makemigrations

python manage.py migrate

```
Now, it is time to initiate the local server:

 `python manage.py runserver`

 > **Note:** if the page fails to load or provides an error, append */neural* to the original path.

 And that's it! The site should run perfectly well :joy: 
