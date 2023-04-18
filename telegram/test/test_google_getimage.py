


import json
import io
import aiohttp
import asyncio
from pydantic import BaseModel

from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google.auth.credentials import Credentials
from googleapiclient.discovery import HttpError
from googleapiclient.discovery import build
from googleapiclient import http


SERVICE_ACCOUNT_FILE = f'/Users/dmitrysakharov/Documents/_Jervis/discord/app/jervisreshost-d276f897f4c0.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
service = build('drive', 'v3', credentials=credentials)

#pydantic request forms
class ImageRequest(BaseModel):
    tg_message_id: int
    chat_id: int
    prompt: str
    image_url: str


async def download_photo(chat_id, mess_id, image_url):
    file_link = image_url
    file_id = file_link.split("/")[5]
    try:
        request = service.files().get_media(fileId=file_id)
        with open('file.jpg', 'wb') as f:
            downloader = http.MediaIoBaseDownload(f, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f'Download {int(status.progress() * 100)}.')
    except HttpError as error:
        if error.resp.status == 404:
            print(f'File with ID "{file_id}" does not exist.')
        else:
            raise error



async def main():
    await download_photo(11, 22, 'https://drive.google.com/file/d/1l5uYZWiUl9wJfs2O1j4VTmjfPoMYHDH8/view')

asyncio.run(main())
    
