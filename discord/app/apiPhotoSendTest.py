from fastapi import FastAPI
import disnake
from disnake.ext import commands
import time
import requests
from uvicorn import Config, Server

app = FastAPI()

url = 'https://discord.com/api/v9/channels/1095343240594595900/messages'
auth = {
  'authorization': 'MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI'
}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/current_prompt/")
async def current_prompt(input_text):
    files = {
        "file" : ("/Users/pavelsedyh/Downloads/Andy_Gandy_defender_of_the_infinity_surreal_38aadc1c-702a-4ef1-b827-c3b1a87bd3c8.png",
                  open("/Users/pavelsedyh/Downloads/Andy_Gandy_defender_of_the_infinity_surreal_38aadc1c-702a-4ef1-b827-c3b1a87bd3c8.png", 'rb')) # The picture that we want to send in binary
    }

    msg = {"content":f"{input_text}"}

    requests.post(url, headers = auth, data = msg, files=files)
    print(f"sent a /generate command with prompt: {input_text}")
