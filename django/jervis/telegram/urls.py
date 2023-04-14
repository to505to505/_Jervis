from django.urls import path
from .views import *


urlpatterns = [
    path('', HelloWorldView.as_view(), name='hello_view'),
]