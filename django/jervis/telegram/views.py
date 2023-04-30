import aiohttp
import asyncio
import requests
import pickle
import logging
import os
import json
import secrets
import string

from django.shortcuts import render
from django.http import QueryDict, HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .models import *
from .serializers import *
from .utils import *
from jervis.tasks import *


# Create your views here.
ALPHABET = string.ascii_letters + string.digits
random_string = ''.join(secrets.choice(ALPHABET) for i in range(50))

#TG_HOST = "localhost"
TG_SOCKET = f"{os.getenv('TG_HOST')}:81" 

#DS_HOST = "localhost"
DS_SOCKET = f"{os.getenv('DISCORD_HOST')}:80"
    
    
class CreateTgChat(APIView):
    '''
    Create new object in Chat model
    '''
    def post(self, request, format=None):
        chat_id = request.data.get("chat_id")
        try:
            chat = Chat.objects.get(chat_id=chat_id)
            return Response("User is already created", status=status.HTTP_409_CONFLICT)
        except Chat.DoesNotExist:
            serializer = ChatSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class SendPrompt(APIView):
    '''
    Send and generate prompt
    '''
    def post(self, request, format=None):
        chat_id = request.data.get("chat_id")
        prompt = request.data.get("prompt")
        tg_message_id = request.data.get("tg_message_id")
        chat = Chat.objects.get(chat_id=chat_id)
        
        if chat.generation_amount == 0:
            return Response(data="User has no generation tokens!", status=status.HTTP_402_PAYMENT_REQUIRED)

        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chat=chat, tg_message_id=tg_message_id)
            
            if chat.status == "paid":
                generate_paid_image.delay(prompt, DS_SOCKET)
            elif chat.status == "free":
                generate_free_image.delay(prompt, DS_SOCKET)
            
            return Response(data={"message": "Image generation task has been added to the queue."}, status=status.HTTP_202_ACCEPTED)
        return Response(data={"erros":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
 
    
class PushButton(APIView):
    '''
    Push button under midjourney image
    '''
    def post(self, request, format=None):
        origin_message_id = request.data.get("original_message_id")
        tg_message_id = request.data.get("tg_message_id")
        chat_id = request.data.get("chat_id")
        method = request.data.get("method")
        image_number = request.data.get("image_number")
        
        chat = Chat.objects.get(chat_id=chat_id)
        
        if chat.generation_amount == 0:
            return Response(data="User has no generation tokens!", status=status.HTTP_402_PAYMENT_REQUIRED)
        
        origin_image = Image.objects.get(tg_message_id = origin_message_id)
        messageid_sseed = origin_image.mesageid_sseed
        origin_prompt = origin_image.prompt.split(":::")[0]
        
        new_data = QueryDict('', mutable=True)
        new_data.update(request.data)
        new_data["prompt"] = f"{origin_prompt}"# {method}"
        
        serializer = ImageSerializer(data=new_data)
        if serializer.is_valid():
            serializer.save(chat=chat)
            
            if chat.status == "paid":
                push_paid_button.delay(method, image_number, messageid_sseed, DS_SOCKET)
            elif chat.status == "free":
                push_free_button.delay(method, image_number, messageid_sseed, DS_SOCKET)
                
            return Response(data={"message": "Image push button task has been added to the queue."}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

class SaveImage(APIView):
    '''
    Load and save generated image url from discord
    '''
    def put(self, request, format=None):
        prompt = request.data.get("prompt") 
        image_url = request.data.get("image_url")
        mesageid_sseed = request.data.get("mesageid_sseed")
        
        image = Image.objects.filter(prompt=prompt).latest('id')
        
        tg_message_id = image.tg_message_id
        chat = image.chat
        chat_id = chat.chat_id
        
        chat_data = QueryDict('', mutable=True)
        chat_data["generation_amount"] = chat.generation_amount - 1
        chat_serializer = ChatSerializer(chat, chat_data)
        if chat_serializer.is_valid():
            chat_serializer.save()
        else:
            return JsonResponse(chat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        if chat.status == "paid":
            response = send_data_to_telegram_paid.delay(image_url, tg_message_id, chat_id, prompt, TG_SOCKET)
        elif chat.status == "free":
            response = send_data_to_telegram_free.delay(image_url, tg_message_id, chat_id, prompt, TG_SOCKET)
        
        new_data = QueryDict('', mutable=True)
        new_data.update(request.data)
        new_data["is_ended"] = True
        new_data["prompt"] = prompt + ":::" + random_string
        
        serializer = ImageSerializer(image, new_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data={"response":response}, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# utils views
class GetTgChatInfo(APIView):
    '''
    Just test function. If you get a response, then the API is working
    '''
    def get(self, request):
        chat_id = request.data.get("chat_id")
        chat = Chat.objects.get(chat_id=chat_id)
        
        data = {"generations_amount": chat.generation_amount,
                "status": chat.status}
        
        return Response(data=data, status=status.HTTP_200_OK)
        
        

        
