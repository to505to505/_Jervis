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

from handlers import send_welcome, handle_generate, button_gen_handler, handle_help

logging.basicConfig(level=logging.INFO)

#bot info
#BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN = '6076696755:AAHWtI_46iKQG3NxYAfV65Zi4sXFWME3TmQ'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
    

dp.register_message_handler(send_welcome, commands=['start'])
dp.register_message_handler(handle_generate, Text(equals='Сгенерировать изображение'))
dp.callback_query_handler(button_gen_handler, filters=lambda c: c.data['tag'] == 'regen')
dp.register_message_handler(handle_help, Text(equals='Техническая поддержка'))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

