import time
import requests
import logging
import os

from fastapi import FastAPI
import disnake
from disnake.ext import commands
from uvicorn import Config, Server
from JervisRequests import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

app = FastAPI()

url = 'https://discord.com/api/v9/interactions'
auth = {
  'authorization': os.getenv("AUTH_TOKEN")
}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate_image/")
async def generate_image(input_text):
    logging.info(f"sent a /generate_image command with prompt: {input_text}")

    get_image(input_text)

    logging.info(f"sent a /generate command with prompt: {input_text}")

    return {"result": "Your request is gotten"}
