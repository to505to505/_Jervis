import time
import aiohttp
import requests
import os
from pathlib import Path
import logging
import json

from uvicorn import Config, Server
from fastapi import FastAPI
import disnake
from disnake.ext import commands
from pydantic import BaseModel

from JervisRequests import *

class ImageGenerationRequest(BaseModel):
    prompt: str
    
class PushButtonRequest(BaseModel):
    method: str
    image_number: int
    messageid_sseed: str

app = FastAPI()

PARENT_PATH = Path(__file__).resolve(strict=True).parent
IMG_PATH = PARENT_PATH.joinpath("Users_pavelsedyh_Downloads_Andy_Gandy_defender_of_the_infinity_surreal_38aadc1c-702a-4ef1-b827-c3b1a87bd3c8.png")

logging.info(IMG_PATH)

url = 'https://discord.com/api/v9/channels/1095343240594595900/messages'
auth = {
  'authorization': os.getenv("AUTH_TOKEN")
  #'authorization': 'MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI'
}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate_image/")
async def generate_image(request: ImageGenerationRequest):
    data = request.json()
    data = json.loads(data)
    input_text = data.get("prompt")
    #logging.info(data, input_text)
    
    file = open(IMG_PATH, 'rb')
    files = {
        "file" : (#IMG_PATH,
                  file) # The picture that we want to send in binary
    }

    msg = {"content":f"{input_text}"}

    requests.post(url, headers=auth, data=msg, files=files)
    print(f"sent a /generate command with prompt: {input_text}")
    file.close()
    
    return {"result": "image is generating"}
