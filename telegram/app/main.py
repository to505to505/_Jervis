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



logging.basicConfig(level=logging.DEBUG)


dp.register_message_handler(send_start, commands=['start'])
dp.register_message_handler(handle_generate, Text(equals='Сгенерировать изображение'), state = MyConversation.non_generation)
dp.callback_query_handler(button_gen_handler)
dp.register_message_handler(handle_help, Text(equals='Техническая поддержка'))
dp.register_message_handler(handle_prompt, content_types=types.ContentTypes.TEXT, state=MyConversation.generation)
dp.register_message_handler(handle_photo, content_types=types.ContentTypes.PHOTO, state = MyConversation.generation)

if __name__ == '__main__':
    #try:
    executor.start_polling(dp, skip_updates=False)
    #finally:
      #  dp.storage.close()
      #  dp.storage.wait_closed()
        
        


