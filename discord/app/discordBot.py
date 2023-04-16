import time
import requests
import os
import logging
import asyncio

import disnake
from disnake.ext import commands
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

#pathes
PICTURE_PATH = ''
MAIN_FOLDER_PATH = 'E:/_Jervis/discord/app/'


#config for service account of google drive_service
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = MAIN_FOLDER_PATH + 'jervisreshost-d276f897f4c0.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

#config for discord bot
bot = commands.Bot(command_prefix='.', help_command=None, intents=disnake.Intents.all())
url = 'https://discord.com/api/v9/interactions'
auth = {
  'authorization': 'MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI'
}

#bot async funcrions
@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")

@bot.event
async def on_message(message):
    if message.author.name != "MidjourneyTshirt":
        logging.info("msg: " + str(message))
        logging.info("type: " + str(message.type))
        logging.info("content: " + str(message.content))
        logging.info("embeds: " + str(message.embeds))
        
        logging.info(message.attachments)
        await asyncio.sleep(30)
        logging.info(message.attachments)
        
        if message.attachments:
            attachments = await message.embeds
            attachment = attachments[0]
            filename = attachment.url.split("_")[-1]
            
            await attachment.save(PICTURE_PATH + filename)
            await message.channel.send(f"Image: {attachment.url}")
        
            logging.info('saved')
            
            FILE_PATH = PICTURE_PATH + filename
            
            creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            drive_service = build('drive', 'v3', credentials=creds)
            file_metadata = {'name': filename, 'parents': ['1-6d1bVS_vi7-zWUyZKoyO7WPsujWSmSV']}
            media = MediaFileUpload(FILE_PATH, resumable=True)
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
            logging.info(f"File ID: {file.get('id')}")
            
        else:
            logging.warning("There are no attachment...")

bot.run("MTA5NTI4MjA5MzAyMzU2NzkxMg.GfSL-S.LB2-z5EuCwVC1T-veV2KzO26m3sqSKdUxbQ3e4")
