import disnake
from disnake.ext import commands
import time
import requests


bot = commands.Bot(command_prefix='.', help_command=None, intents=disnake.Intents.all())
url = 'https://discord.com/api/v9/interactions'
auth = {
  'authorization': 'MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI'
}

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
