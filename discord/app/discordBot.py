import time
import requests
import os
import logging
import asyncio
import aiohttp
from pathlib import Path
import re
import boto3

import disnake
from disnake.ext import commands

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build

from JervisRequests import get_image, send_image


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

aws_access_key_id = 
aws_secret_access_key = 
region_name = 'eu-north-1'
output = 'json'
bucket_name = 'jervis'

# Create an S3 client (configuration)
s3 = boto3.client('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name=region_name
                  )

def upload_s3(upload_path):
    object_key = upload_path.split("/")[-1]
    with open(upload_path, "rb") as f:
        s3.upload_fileobj(f, bucket_name, object_key)

#BOT_TOKEN = "MTA5NTI4MjA5MzAyMzU2NzkxMg.GfSL-S.LB2-z5EuCwVC1T-veV2KzO26m3sqSKdUxbQ3e4"
BOT_TOKEN = os.getenv("APP_TOKEN")

#HOST = "localhost"
HOST = os.getenv("DJANGO_HOST")

#pathes
PICTURE_PATH = '/data/shared_folder1/'
MAIN_FOLDER_PATH = Path(__file__).resolve(strict=True).parent

#config for service account of google drive_service
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = MAIN_FOLDER_PATH.joinpath('jervisreshost-d276f897f4c0.json')
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)
#config for discord bot
bot = commands.Bot(command_prefix='.', help_command=None, intents=disnake.Intents.all())
url = 'https://discord.com/api/v9/interactions'


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

        #logging.info(message.attachments)
        await asyncio.sleep(1)
        #logging.info(message.attachments)

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
            upload_s3(FILE_PATH)
            file_drive_url = f'https://jervis.s3.eu-north-1.amazonaws.com/results/{filename}'
            # Connecting to google drive and load image
            # file_metadata = {'name': filename, 'parents': ['1Av1_QNovnSEvQAnED5OAvZO2TJMFowlP']}
            # media = MediaFileUpload(FILE_PATH, resumable=True)

            ### file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            # file = await asyncio.to_thread(
            # drive_service.files().create,
            # body=file_metadata,
            # media_body=media,
            # fields='id'
            # )

            # # Getting link on google drive
            # file_id = file.execute().get('id')
            # file_drive_url = f'https://drive.google.com/file/d/{file_id}'

            messageid_sseed = f"{message.id}_{parce_get_sseed(file_ds_url)}"
            prompt = message.content.split("**")[1]
            if prompt.find("<https://s.mj.run/") != -1:
                pattern = r"<https://s\.mj\.run/.*?> "
                link = (re.findall(pattern, prompt))[0][:-1]
                link = link.strip("<>")
                response = requests.get(link, allow_redirects=True)
                prompt = f'{response.url} ' + re.sub(pattern, "", prompt)

            file_path = "/data/shared_folder1/eee.txt"

            with open(file_path, 'w') as file:
                file.write("This is an example content.")
            
            #delete
            
            
            logging.info(f"sent soon")
            await send_image(messageid_sseed, file_drive_url, prompt, DS_HOST=HOST)

            #logging.info(file_drive_url)
            #logging.info(FILE_PATH)
            #logging.info(f"File ID: {file_id}")

            # Удаляем локальную картинку
            # os.remove(FILE_PATH)

        else:
            logging.warning("There are no attachment...")


bot.run(BOT_TOKEN)
