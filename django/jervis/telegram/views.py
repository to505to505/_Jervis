import aiohttp
import requests
import logging
import os
import json

from django.shortcuts import render
from django.http import QueryDict
from django.http import HttpRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .models import *
from .serializers import *

# Create your views here.

TG_HOST = "localhost"
#TG_HOST = os.getenv("TG_HOST")

DS_HOST = "localhost"
#DS_HOST = os.getenv("DISCORD_HOST")

class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})
    
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
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        
        data = {"chat_id": chat_id,
                "prompt":prompt,
                "tg_message_id":tg_message_id}
    
        print(data)
        
        requests.post(f"http://{DS_HOST}:80/generate_image/", json=data)

        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chat=chat)
            return Response("Image has sent!")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SaveImage(APIView):
    '''
    Load and save generated image url from discord
    '''
    def put(self, request, format=None):
        prompt = request.data.get("prompt")
        image_url = request.data.get("image_url")
        
        image = Image.objects.get(prompt = prompt)
        
        tg_message_id = image.tg_message_id
        chat = image.chat
        chat_id = chat.chat_id
        
        new_data = QueryDict('', mutable=True)
        new_data.update(request.data)
        new_data["is_ended"] = True
        
        serializer = ImageSerializer(image, new_data)
        if serializer.is_valid():
            chat.generation_amount -= 1
            data_for_tg = {"image_url": image_url,
                           "tg_message_id": tg_message_id,
                           "chat_id": chat_id}
            
            print(data_for_tg)
            serializer.save()
            requests.post(f"http://{TG_HOST}:81/load_image/", json=data_for_tg)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PushButton(APIView):
    '''
    Push button under midjourney image
    '''
    def post(self, request, format=None):
        tg_message_id = request.data.get("tg_message_id")
        chat_id = request.data.get("chat_id")
        
