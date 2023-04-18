import logging
import time
import aiohttp
import os
import aiohttp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputFile
from aiogram.utils import executor
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.auth.credentials import Credentials

async def make_async_request_post(url: str, data: dict):
    '''
    Make async http request
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.text()

BOT_TOKEN = '6076696755:AAHWtI_46iKQG3NxYAfV65Zi4sXFWME3TmQ'
#BOT_TOKEN = os.getenv("BOT_TOKEN")

HOST = "localhost"
#HOST = os.getenv('HOST')

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher(bot)


async def send_id(chat_id):
    data = {"chat_id": chat_id}
    await make_async_request_post(f"http://{HOST}:8000/api/tg/create_chat/", data=data)


async def send_prompt(chat_id, prompt, tg_message_id):
    data = {"chat_id": chat_id,
            "prompt": prompt,
            "mess_id": tg_message_id}
    await make_async_request_post(f"http://{HOST}:8000/api/tg/send_prompt/", data=data)


async def push_button(chat_id, original_message_id, tg_message_id, method, image_number):
    data = {"chat_id": chat_id,
            "tg_message_id": tg_message_id,
            "original_message_id": original_message_id,
            "Method": method,
            "image_number": image_number}   
    await make_async_request_post(f"http://{HOST}:8000/api/tg/push_button/", data=data) 