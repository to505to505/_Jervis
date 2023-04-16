import aiohttp
import logging

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
    async def post(self, request, format=None):
        chat_id = request.data.get("chat_id")
        prompt = request.data.get("prompt")
        tg_message_id = request.data.get("tg_message_id")
        
        chat = Chat.objects.get(chat_id=chat_id)
        
        if chat.generation_amount == 0:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        
        data = {"chat_id": chat_id,
                "prompt":prompt}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post("http://localhost:8080/generate_image", data=data) as response:
                    response_data = await response.json()
                    
                    image_url = response_data["image_url"]
                    messageid_sseed = response_data["messageid_sseed"]
                    
                    logging.info(image_url)
                    chat.generation_amount -= 1
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
                
        chat.generation_amount -= 1
        
        new_dict = QueryDict('', mutable=True)
        new_dict.update(request.data)
        new_dict["image_url"] = image_url
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"image_url": image_url}
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
