import aiohttp
import requests
import pickle
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

async def make_async_request(url: str, data: dict):
    '''
    Make async http request
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.text()


class HelloWorldView(APIView):
    '''
    Just test function. If you get a response, then the API is working
    '''
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
            return Response(data="User has no generation tokens!", status=status.HTTP_402_PAYMENT_REQUIRED)

        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chat=chat, tg_message_id=tg_message_id)
            data = {"prompt":prompt,}
            
            # await make_async_request(f"http://{DS_HOST}:80/generate_image/", data=data)
            requests.post(f"http://{DS_HOST}:80/generate_image/", json=data)
            
            return Response("Image has sent and sabed in database!")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
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
        messageid_sseed = origin_image.messageid_sseed
        origin_prompt = origin_image.prompt
        
        new_data = QueryDict('', mutable=True)
        new_data.update(request.data)
        new_data["prompt"] = f"{origin_prompt} {method}"
        
        serializer = ImageSerializer(data=new_data)
        if serializer.is_valid():
            data = {"method":method,
                    "image_number":image_number,
                    "messageid_sseed":messageid_sseed}
            
            # await make_async_request(f"http://{DS_HOST}:80/push_button/", data=data)
            requests.post(f"http://{DS_HOST}:80/push_button/", json=data)
            
            serializer.save(chat=chat)
            return Response("Image has sent and sabed in database!", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SaveImage(APIView):
    '''
    Load and save generated image url from discord
    '''
    def put(self, request, format=None):
        prompt = request.data.get("prompt") 
        image_url = request.data.get("image_url")
        mesageid_sseed = request.data.get("mesageid_sseed")
        
        print(prompt, image_url, mesageid_sseed)
        
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
                           "chat_id": chat_id,
                           "prompt": prompt}
            
            # await make_async_request(f"http://{TG_HOST}:81/load_image/", data=data_for_tg)
            requests.post(f"http://{DS_HOST}:80/push_button/", json=data_for_tg)
            
            image.prompt += ":jervis_token_notcopy_ifsomeonegetitoutappwillcpllapse_43"
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
