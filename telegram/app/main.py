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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

from handlers import send_welcome

logging.basicConfig(level=logging.INFO)





bot = Bot(token=os.getenv("APP_TOKEN"))
dp = Dispatcher(bot)
    

# dp.register_message_handler(handle_photo, Text(equals="Option 1"), content_types=types.ContentTypes.PHOTO)
dp.register_message_handler(send_welcome, commands=['start'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

