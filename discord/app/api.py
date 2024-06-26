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
from pydantic import BaseModel
import json

class ImageGenerationRequest(BaseModel):
    prompt: str

class PushButtonRequest(BaseModel):
    method: str
    image_number: int
    messageid_sseed: str

app = FastAPI()

# PARENT_PATH = Path(__file__).resolve(strict=True).parent
# IMG_PATH = PARENT_PATH.joinpath("Users_pavelsedyh_Downloads_Andy_Gandy_defender_of_the_infinity_surreal_38aadc1c-702a-4ef1-b827-c3b1a87bd3c8.png")

#logging.info(IMG_PATH)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate_image/")
async def generate_image(request: ImageGenerationRequest):
    data = request.json()
    data = json.loads(data)
    input_text = data.get("prompt")
    #logging.info(data, input_text)
    await get_image(input_text)
    logging.info(f"sent a /imagine command with prompt: {input_text}")
    print(f"sent a /generate command with prompt: {input_text}")
    return {"result": "image is generating"}

@app.post("/push_button/")
async def push_button(request: PushButtonRequest):
    data = request.json()
    data = json.loads(data)
    method = data.get("method")
    image_number = data.get("image_number")
    messageid_sseed = data.get("messageid_sseed")

    await push_button_request(method, image_number, messageid_sseed)
    logging.info(f"pushed a button {image_number} with messageid_sseed {messageid_sseed} for {method}")
    print(f"pushed a button {image_number} with messageid_sseed {messageid_sseed} for {method}")
    return {"result": f"image is {method}"}
