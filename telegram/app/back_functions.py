from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import time
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.auth.credentials import Credentials

bot = Bot(token = '6076696755:AAHWtI_46iKQG3NxYAfV65Zi4sXFWME3TmQ')
dp = Dispatcher(bot)

cred_path = f'jervisreshost-65947324df56.json'
creds = service_account.Credentials.from_service_account_file(cred_path)

# Set up the Drive API client
service = build('drive', 'v3', credentials=creds)



async def send_id(chat_id):
    data = {"chat_id": chat_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://{os.getenv('HOST')}:8000/api/tg/create_chat/", data=data) as response:
            response_text = await response.text()
            print(response_text)
            
async def hello():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{os.getenv('HOST')}:8000/") as response:
            response_text = await response.text()
            return response_text

async def send_prompt(chat_id, prompt):
    data = {"chat_id": chat_id,
            "prompt":prompt}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://{os.getenv('HOST')}:8000/api/tg/send_prompt/", data=data) as response:
            response_text = await response.text()
            return(response_text)

async def push_button(chat_id, prompt, button):
    pass


async def download_photo(chat_id, mess_id, result):
    file_link = result
    file_id = file_link.split("/")[5]
    file = service.files().get(fileId=file_id).execute()
    download_url = file.get("exportLinks").get("image/jpeg")
    if download_url:
        response = requests.get(download_url)
        file_name = f"{chat_id}__{mess_id}.jpeg"
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        pass
    return file_name