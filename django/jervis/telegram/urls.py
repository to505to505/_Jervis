from django.urls import path
from .views import *


urlpatterns = [
    path('', HelloWorldView.as_view(), name='hello_view'),
    path('api/tg/create_chat/', CreateTgChat.as_view(), name='create_chat'),
    path('api/tg/send_prompt/', SendPrompt.as_view(), name='send_prompt'),
    path('api/ds/load_image/', SaveImage.as_view(), name='save_image'),
    path('api/tg/push_button/', PushButton.as_view(), name='push_button'), 
]