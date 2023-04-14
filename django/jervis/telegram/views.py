from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from serializers import *

# Create your views here.

class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})