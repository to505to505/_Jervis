from django.urls import path
from asgiref.sync import async_to_sync
from django.views.decorators.csrf import csrf_exempt
from .views import *


urlpatterns = [
    path('api/tg/create_chat/', CreateTgChat.as_view(), name='create_chat'),
    path('api/tg/send_prompt/', SendPrompt.as_view(), name='send_prompt'),
    path('api/tg/push_button/', PushButton.as_view(), name='push_button'), 
    path('api/ds/load_image/', SaveImage.as_view(), name='save_image'),
    path('api/tg/get_chat_info', GetTgChatInfo.as_view(), name='get_chat_info'),
]