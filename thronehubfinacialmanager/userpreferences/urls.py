from . import views
from django.urls import path

# URL patterns for handling preferences related views

urlpatterns = [
    # Maps the root URL to the index view function from views.py, named 'preferences'
    path('', views.index, name="preferences"),
]
