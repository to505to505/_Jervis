import logging
import aiohttp
import asyncio
import os
import requests
import time

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Filter
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
from aiogram.utils import markdown

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.auth.credentials import Credentials
from googleapiclient.http import MediaFileUpload

import boto3

from back_functions import *
from bot import bot, dp, BOT_TOKEN

logging.basicConfig(level=logging.DEBUG)

# Set up AWS credentials and region
aws_access_key_id = 'AKIAQME5MYJPO377UW6W'
aws_secret_access_key = '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'
region_name = 'eu-north-1'
output = 'json'
bucket_name = 'jervis-reference'

# Create an S3 client (configuration)
s3 = boto3.client('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name=region_name
                  )

#google set up
SERVICE_ACCOUNT_FILE = f'jervisreshost-65947324df56.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
service = build('drive', 'v3', credentials=credentials)

#defining callback_data variable just to use it more easily
callback_data = CallbackData('method', 'image_number', 'tag')

class MyConversation(StatesGroup):
    '''' Defining class to track states of users'''
    generation = State()
    non_generation = State()

class SkipHandlerFilter(Filter):
    def __init__(self, skip_text: dict):
        self.skip_text = skip_text  

    async def check(self, message):
        for i in self.skip_text:
            if i==message.text:
                return False
        return True

### Handler of /start
async def send_start(message: types.Message, state: FSMContext):
    ''' Starting bot, sending user main menu buttons and sending his chat_id to django'''
    logging.info(f'Received start command from {message.from_user.id}')
    await MyConversation.non_generation.set()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Сгенерировать изображение")
    button2 = KeyboardButton("Мой профиль")
    button3 = KeyboardButton("Техническая поддержка")
    keyboard.row(button1, button2)
    keyboard.add(button3)
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'hello world', reply_markup = keyboard)
    await send_id(chat_id)


### Handlers of Main Menu buttons
    
async def handle_generate(message: types.Message, state: FSMContext):
    '''' Starting generation by clicking on the button Сгенерировать изображение. Function gets prompt and sends prompts to Django'''
    logging.info(f'Received generation command from {message.from_user.id}')
    await MyConversation.generation.set()
    logging.info(f'Received generation command2 from {message.from_user.id}')
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Напишите prompt и по желанию прикрепите картинку-референс.')


async def handle_prompt(message: types.Message, state: FSMContext):
        ''''Handling prompt without a reference-photo'''
        chat_id = message.chat.id
        prompt = message.text
        tg_message_id = message.message_id
        await bot.send_message(chat_id, f'Изображение генерируется по запросу: \n{prompt}\n Пожалуйста, подождите!')
        await send_prompt(chat_id, prompt, tg_message_id)
        await MyConversation.non_generation.set()
        

def upload_s3(photo_name, upload_path):
    object_key = photo_name
    with open(upload_path, "rb") as f:
        s3.upload_fileobj(f, bucket_name, object_key)
    
async def handle_photo(message: types.Message, state: FSMContext):
    '''' Handling prompt with photo'''
    chat_id = message.chat.id
    tg_message_id = message.message_id
    

    if message.caption:
        caption = message.caption
        file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        PHOTO_PATH = f"./reference/{chat_id}__{tg_message_id}_reference.jpeg"
        with open(PHOTO_PATH, 'wb') as new_file:
            new_file.write(downloaded_file.getvalue())
        logging.info(f'{downloaded_file.getvalue()}')
        logging.info(f'OK')
        # save image locally
        
        PHOTO_NAME = f'{chat_id}__{tg_message_id}_r.jpeg'
         
    
            
        await bot.send_message(chat_id, f'Изображение генерируется по картинке-референсу и по запросу: \n{caption}\n Пожалуйста, подождите!')
        
        # Load image on s3
        upload_s3(PHOTO_NAME, PHOTO_PATH)
        photo_link = f'https://jervis-reference.s3.eu-north-1.amazonaws.com/{PHOTO_NAME}'
        prompt = ""
        prompt += photo_link
        prompt += f" {caption}"
        logging.info(f'{photo_link}')
        await send_prompt(chat_id, prompt, tg_message_id)
        await state.set_state(MyConversation.non_generation)
        os.remove(PHOTO_PATH)
    else:
        await bot.send_message(chat_id, 'Вы обязательно должны прикрепить prompt в сообщении с картинкой-референсом! Попробуйте еще раз.')
        await state.set_state(MyConversation.non_generation)


async def handle_help(message: types.Message, state: FSMContext):
    ''' Handling Техническая Поддержка button'''
    #await state.set_state(MyConversation.non_generation)
    chat_id = message.chat.id
    button1 = InlineKeyboardButton('Техническая поддержка', url = 'https://t.me/Kwazzart')
    button2 = InlineKeyboardButton('Сотрудничество и прочие вопросы', url = 'https://t.me/jervis_collaboration')
    keyboard = InlineKeyboardMarkup().row(button1, button2)
    chat_id_str = markdown.bold(f'{chat_id}')
    await bot.send_message(chat_id, f'При обращении в поддержку, пожалуйста, сообщите свой ID: {chat_id_str}', reply_markup=keyboard)


#Handlers of buttons like U1, U2 etc, 
async def button_gen_handler(callback_query: CallbackQuery, state: FSMContext):
    logging.info(f'Buttons started')
    message = callback_query.message

    callback_text = callback_query.data
    method, image_number = callback_text.split(':')
    tg_message_id = message.message_id
    chat_id = callback_query.message.chat.id
    original_message_id = message.reply_to_message.message_id
    text_to_send = ''
    if method == 'upsample':
        text_to_send = f'Повышаем качество изображения под номером {image_number}!'
    elif method == 'variation':
        text_to_send = f'Генерируем похожие изображения для изображения под номером {image_number}!'
    else:
        text_to_send = 'Сейчас перегенирируем изображения по тому же запросу!'

    await bot.send_message(chat_id, text_to_send)

    response = await push_button(chat_id, tg_message_id, original_message_id, method, image_number)
    return response
    

        






    

        
      