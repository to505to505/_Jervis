import time
import requests
import logging
import os

from fastapi import FastAPI
import disnake
from disnake.ext import commands
from uvicorn import Config, Server
from JervisRequests import *
from pydantic import BaseModel
import json

class ImageGenerationRequest(BaseModel):
    prompt: str

class PushButtonRequest(BaseModel):
    method: str
    image_number: int
    messageid_sseed: str

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate_image/")
async def generate_image(request: ImageGenerationRequest):
    data = request.json()
    data = json.loads(data)
    input_text = data.get("prompt")
    
    logging.info(f"sent a /generate_image command with prompt: {input_text}")

    get_image(input_text)

    logging.info(f"sent a /generate command with prompt: {input_text}")

    return {"result": "Your request is gotten"}
