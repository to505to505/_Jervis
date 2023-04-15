import requests

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
            chat_id = Chat.objects.get(chat_id=chat_id)
        except Chat.DoesNotExist: 
            serializer = ChatSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
