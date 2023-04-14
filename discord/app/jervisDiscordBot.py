import disnake
from disnake.ext import commands
import time
import requests
from fastapi import FastAPI

import nest_asyncio
nest_asyncio.apply()

app = FastAPI()

bot = commands.Bot(command_prefix='.', help_command=None, intents=disnake.Intents.all())
url = 'https://discord.com/api/v9/interactions'
auth = {
  'authorization': 'MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI'
}

@app.get("/")
async def root():
    return {"message": "Hello World"}

#@app.post("current_prompt")
#async def current_prompt(input_text):
#    msg = {"type":2,
#    "application_id":"1032699319368814652",
#    "guild_id":"1094995526769987704",
#    "channel_id":"1095343240594595900",
#    "session_id":"2e224721645708c191a4f38585994b53",
#    "data":
#    {"version":"1093695818164338708",
#    "id":"1037145598782099518",
#    "name":"generate",
#    "type":1,
#    "options":[{"type":3,
#    "name":"description",
#    "value":input_text}],
#    }}
#    requests.post(url, headers = auth, json = msg)
#    print(f"sent a /generate command with prompt: {input_text}")

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")

@bot.event
async def on_message(message):
    if message.author.name != "MidjourneyTshirt":
        print("msg: " + str(message))
        print("type: " + str(message.type))
        print("content: " + str(message.content))
        print("embeds: " + str(message.embeds))
        time.sleep(10)
        await message.channel.send(f"type: {message.type}")
        if len(message.embeds) >= 1:
            await message.channel.send(f"image: {message.embeds[0].image.proxy_url}")
            await message.channel.send(f"image: {message.embeds[0].fields[0].value}")
            await message.channel.send(f"image: {message.embeds[0].fields}")
        #requests.post("localhost:8080/image_response", message.embeds[0].image.proxy_url)

bot.run("MTA5NTI4MjA5MzAyMzU2NzkxMg.GfSL-S.LB2-z5EuCwVC1T-veV2KzO26m3sqSKdUxbQ3e4")
