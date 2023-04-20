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

from handlers import *
from bot import bot, dp

logging.basicConfig(level=logging.INFO)

dp.register_message_handler(send_start, commands=['start'])
dp.register_message_handler(handle_generate, Text(equals='Сгенерировать изображение'))
dp.callback_query_handler(button_gen_handler)
dp.register_message_handler(handle_help, Text(equals='Техническая поддержка'))
dp.register_message_handler(handle_prompt, content_types=types.ContentTypes.TEXT)
#@dp.message_handler(content_types=types.ContentTypes.PHOTO)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

