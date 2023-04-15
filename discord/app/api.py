from fastapi import FastAPI
import disnake
from disnake.ext import commands
import time
import requests
from uvicorn import Config, Server

app = FastAPI()

url = 'https://discord.com/api/v9/interactions'
auth = {
  'authorization': 'MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI'
}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/current_prompt/")
async def current_prompt(input_text):
    print(f"sent a /generate command with prompt: {input_text}")
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
    print(f"sent a /generate command with prompt: {input_text}")
