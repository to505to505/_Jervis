import disnake
from disnake.ext import commands
import time
import requests
import os
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build

#pathes
PICTURE_PATH = ''


#config for service account of google drive_service
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'jervisreshost-d276f897f4c0.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

#config for discord bot
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
        #time.sleep(10)
        await message.channel.send(f"image: {message.attachments[0].url}")
        #dsurl = message.attachments[0].url
        filename = message.attachments[0].url.split('_')[-1]
        await message.attachments[0].save(PICTURE_PATH + filename)
        print('saved')
        FILE_PATH = PICTURE_PATH + filename
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        drive_service = build('drive', 'v3', credentials=creds)
        file_metadata = {'name': filename, 'parents': ['1-6d1bVS_vi7-zWUyZKoyO7WPsujWSmSV']}
        media = MediaFileUpload(FILE_PATH, resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"File ID: {file.get('id')}")

bot.run("MTA5NTI4MjA5MzAyMzU2NzkxMg.GfSL-S.LB2-z5EuCwVC1T-veV2KzO26m3sqSKdUxbQ3e4")
