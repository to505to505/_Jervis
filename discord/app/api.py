import time
import requests
import logging

from fastapi import FastAPI
import disnake
from disnake.ext import commands
from uvicorn import Config, Server

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

app = FastAPI()

url = 'https://discord.com/api/v9/interactions'
auth = {
  'authorization': 'MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI'
}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate_image/")
async def generate_image(input_text):
    logging.info(f"sent a /generate_image command with prompt: {input_text}")
    msg = {"type":2,
    "application_id":"1032699319368814652",
    "guild_id":"1094995526769987704",
    "channel_id":"1095343240594595900",
    "session_id":"2e224721645708c191a4f38585994b53",
    "data":
    {"version":"1093695818164338708",
    "id":"1037145598782099518",
    "name":"generate",
    "type":1,
    "options":[{"type":3,
    "name":"description",
    "value":input_text}],
    }}
    requests.post(url, headers = auth, json = msg)
    logging.info(f"sent a /generate command with prompt: {input_text}")
    return {"result": "Your request is gotten"}
