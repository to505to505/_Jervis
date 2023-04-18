import json

import aiohttp

from fastapi import FastAPI, Request
from pydantic import BaseModel

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.auth.credentials import Credentials

#pydantic request forms
class ImageRequest(BaseModel):
    tg_message_id: int
    chat_id: int
    prompt: str
    image_url: str


async def download_photo(chat_id, mess_id, image_url):
    file_link = image_url
    file_id = file_link.split("/")[5]
    file = service.files().get(fileId=file_id).execute()
    download_url = file.get("exportLinks").get("image/jpeg")
    if download_url:
        response = make_async_request_post(download_url)
        file_name = f"{chat_id}__{mess_id}.jpeg"
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        pass
    return file_name

async def make_async_request_post(url: str, data: dict):
    '''
    Make async http request
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.text()

SERVICE_ACCOUNT_FILE = f'../jervisreshost-65947324df56.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
service = build('drive', 'v3', credentials=credentials)

app = FastAPI()

@app.get('/', tags = ['ROOT'])
async def root() -> dict:
    return {'Ping': 'Pong'}  


@app.post('/load_image/')
async def handle_post(request: ImageRequest):
    data = request.json()
    data = json.loads(data)
    print(data)
    
    # Send action request to tg bot
    
    
    return {"message": "Data received and processed successfully"}



