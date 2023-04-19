import time
import requests
import os
import logging
import asyncio
from pathlib import Path

import disnake
from disnake.ext import commands

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build

from JervisRequests import get_image, send_image

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = "MTA5NTI4MjA5MzAyMzU2NzkxMg.GfSL-S.LB2-z5EuCwVC1T-veV2KzO26m3sqSKdUxbQ3e4"
#BOT_TOKEN = os.getenv("APP_TOKEN")

AUTH_TOKEN = 'MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI'
#AUTH_TOKEN = os.getenv("AUTH_TOKEN")

HOST = "localhost"
#HOST = os.getenv("HOST")

#pathes
PICTURE_PATH = ''
MAIN_FOLDER_PATH = Path(__file__).resolve(strict=True).parent

#config for service account of google drive_service
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = MAIN_FOLDER_PATH.joinpath('jervisreshost-d276f897f4c0.json')
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

#config for discord bot
bot = commands.Bot(command_prefix='.', help_command=None, intents=disnake.Intents.all())
url = 'https://discord.com/api/v9/interactions'
auth = {
  #'authorization': os.getenv("AUTH_TOKEN"),
  'authorization': AUTH_TOKEN,
}

def parce_get_prompt(url):
    #''.join(url.split('/')[6].split('_')[:-1])
    return url[url.find("_")+1:url.rfind("_")].replace("_", " ")

def parce_get_sseed(url):
    return url.split("_")[-1]

#bot async functions
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
        await asyncio.sleep(1)
        logging.info(message.attachments)

        if message.attachments:
            # Getting file name from discord
            attachment = message.attachments[0]
            filename = attachment.url.split("_")[-1]

            FILE_PATH = PICTURE_PATH + filename

            # Save image locally
            await attachment.save(FILE_PATH)
            file_ds_url = attachment.url
            await message.channel.send(f"Image: {file_ds_url}")
            logging.info('saved')

            # Connecting to google drive and load image
            creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            drive_service = build('drive', 'v3', credentials=creds)
            file_metadata = {'name': filename, 'parents': ['1Av1_QNovnSEvQAnED5OAvZO2TJMFowlP']}
            media = MediaFileUpload(FILE_PATH, resumable=True)
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            # Getting link on google drive
            file_id = file.get('id')
            file_drive_url = f'https://drive.google.com/file/d/{file_id}'

            messageid_sseed = f"{message.id}_{parce_get_sseed(file_drive_url)}"

            await send_image(messageid_sseed, file_drive_url, message.content)

            logging.info(file_drive_url)
            logging.info(FILE_PATH)
            logging.info(f"File ID: {file_id}")

            # Удаляем локальную картинку
            os.remove(FILE_PATH)

        else:
            logging.warning("There are no attachment...")

bot.run(BOT_TOKEN)
