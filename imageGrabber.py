import json
import time
import requests
import logging
import os

from fastapi import FastAPI
import disnake
from disnake.ext import commands
from uvicorn import Config, Server

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build

CHAT_ID = "1095343240594595900"
PICTURE_PATH = "/Users/pavelsedyh/Desktop/pictures/"
#MAIN_FOLDER_PATH = Path(__file__).resolve(strict=True).parent

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/Users/pavelsedyh/Desktop/_Jervis/discord/app/jervisreshost-d276f897f4c0.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

def drive_upload(image):
    # Getting file name from discord
    #attachment = image
    #filename = image['url'].split("_")[-1]
    filename = image.split("_")[-1]

    FILE_PATH = PICTURE_PATH + filename

    # Save image locally
    response = requests.get(image)
    if response.status_code:
        fp = open(FILE_PATH, 'wb')
        fp.write(response.content)
        file_metadata = {'name': filename, 'parents': ['1Av1_QNovnSEvQAnED5OAvZO2TJMFowlP']}
        media = MediaFileUpload(FILE_PATH, resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id')
        file_id = file.execute().get('id')
        file_drive_url = f'https://drive.google.com/file/d/{file_id}'
        fp.close()
        os.remove(FILE_PATH)
    #attachment.save(FILE_PATH)
    #file_ds_url = image
    #logging.info('saved')

    # Connecting to google drive and load image


    # Getting link on google drive

def retrive_messages(chat_id):
    url = f'https://discord.com/api/v9/channels/{chat_id}/messages?limit=50'
    auth = {
        #'authorization': os.getenv("AUTH_TOKEN")
        'authorization': "MTA5NjExMjQxMzE0Njg5NDQzNw.GIdgNV.D-jvRjQVbSdyul3Ak19DhLnjDD2sD-6FEN8Sp0"
    }
    r = requests.get(url, headers=auth)
    jsn = json.loads(r.text)
    print(type(jsn))
    for value in jsn:
        if value["attachments"]:
            drive_upload(value["attachments"][0]['url'])
            print(value["attachments"][0]['url'], '\n')


retrive_messages(CHAT_ID)
