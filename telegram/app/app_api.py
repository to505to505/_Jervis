import json
import io
import aiohttp
import logging
import time
import aiohttp
import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery

from fastapi import FastAPI, Request
from pydantic import BaseModel

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient import http
from google.oauth2 import service_account
from google.auth.credentials import Credentials

from bot import bot, dp 
from utils import *


#getting acess to google api
SERVICE_ACCOUNT_FILE = f'jervisreshost-65947324df56.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
service = build('drive', 'v3', credentials=credentials)


#creating fastapi
app = FastAPI()


#pydantic request forms
class ImageRequest(BaseModel):
    tg_message_id: int
    chat_id: int
    prompt: str
    image_url: str


async def download_photo(chat_id, tg_message_id, image_url):
    ''' Function for downloading photo with google url'''
    file_link = image_url
    file_id = file_link.split("/")[5]
    try:
        request = service.files().get_media(fileId=file_id)
        with open(f'temp_storage/{chat_id}__{tg_message_id}__.jpg', 'wb') as f:
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


async def make_buttons():
    ''''Creating buttons as U1, U2, etc,'''
    button1 = InlineKeyboardButton(text="U1", callback_data="Upscaled:1")
    button2 = InlineKeyboardButton(text="U2", callback_data="Upscaled:2")
    button3 = InlineKeyboardButton(text="U3", callback_data="Upscaled:3")
    button4 = InlineKeyboardButton(text="U4", callback_data="Upscaled:4")
    button5 = InlineKeyboardButton(text="V1", callback_data="Variations:1")
    button6 = InlineKeyboardButton(text="V2", callback_data="Variations:2")
    button7 = InlineKeyboardButton(text="V3", callback_data="Variations:3")
    button8 = InlineKeyboardButton(text="V4", callback_data="Variations:4")
    button9 = InlineKeyboardButton(text="Reroll", callback_data="Reroll:0")

    keyboard = InlineKeyboardMarkup()
    keyboard.row(button1, button2, button3, button4, button9)
    keyboard.row(button5, button6, button7, button8)
    return keyboard



@app.get('/', tags = ['ROOT'])
async def root() -> dict:
    ''' Test '''
    return {'Ping': 'Pong'}  


@app.post('/load_image/')
async def handle_post(request: ImageRequest):
    '''
    Getting image_url that volodya posted from load_image, downloading it and sending to user. Deleting after.
    '''
    
    data = request.json()
    data = json.loads(data)
    
    chat_id = data['chat_id']
    tg_message_id = data['tg_message_id']
    image_url = data['image_url']
    prompt = data['prompt']
    
    await download_photo(chat_id, tg_message_id, image_url)
    reply_text = "This is your photo!"
    photo_path = f'temp_storage/{chat_id}__{tg_message_id}__.jpg' 
     
    with open(photo_path, 'rb') as f:
        photo_bytes = f.read()
        
    keyboard = await make_buttons()
    await bot.send_photo(chat_id = chat_id, photo = photo_bytes, caption=reply_text, reply_to_message_id= tg_message_id, reply_markup = keyboard)
    os.remove(photo_path)
    
    return {"message": "Data received and processed successfully"}



