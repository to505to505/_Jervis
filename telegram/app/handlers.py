import logging
import aiohttp
import asyncio
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

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.auth.credentials import Credentials
from googleapiclient.http import MediaFileUpload

from back_functions import *
from bot import bot, dp

logging.basicConfig(level=logging.DEBUG)


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


### Handler of /start
async def send_start(message: types.Message, state: FSMContext):
    ''' Starting bot, sending user main menu buttons and sending his chat_id to django'''
    await state.set_state(MyConversation.non_generation)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Сгенерировать изображение")
    button2 = KeyboardButton("Мой профиль")
    button3 = KeyboardButton("Техническая поддержка")
    keyboard.row(button1, button2)
    keyboard.add(button3)
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'hello world)', reply_markup = keyboard)
    await send_id(chat_id)


### Handlers of Main Menu buttons
    
async def handle_generate(message: types.Message, state: FSMContext):
    '''' Starting generation by clicking on the button Сгенерировать изображение. Function gets prompt and sends prompts to Django'''
    await state.set_state(MyConversation.generation)
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Напишите prompt и по желанию прикрепите картинку-референс.')


async def handle_prompt(message: types.Message, state: FSMContext):
        ''''Handling prompt without a reference-photo'''
        chat_id = message.chat.id
        prompt = message.text
        tg_message_id = message.message_id
        await bot.send_message(chat_id, f'Изображение генерируется по запросу: \n{prompt}\n Пожалуйста, подождите!')
        await send_prompt(chat_id, prompt, tg_message_id)
        await state.set_state(MyConversation.non_generation)
        
    
async def handle_photo(message: types.Message, state: FSMContext):
    '''' Handling prompt with photo'''
    chat_id = message.chat.id
    tg_message_id = message.message_id
    
    if message.caption:
        caption = message.caption
        file_id = message.photo[-1].file_id
        
        # save image locally
        PHOTO_PATH = f"/reference/{chat_id}__{tg_message_id}_reference.jpg"
        PHOTO_NAME = f'{chat_id}__{tg_message_id}_r'
         
        file = await bot.download_file_by_id(file_id)
        with open(PHOTO_PATH, "wb") as f:
            f.write(file.read())
            
        await bot.send_message(chat_id, f'Изображение генерируется по картинке-референсу и по запросу: \n{caption}\n Пожалуйста, подождите!')
        
        # Load image on google drive
        file_metadata = {'name': PHOTO_NAME}
        media = MediaFileUpload(PHOTO_PATH, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')
        file = service.files().get(fileId=file_id, fields='webViewLink').execute()
        photo_link = file.get('webViewLink')
        
        prompt = ""
        prompt += photo_link
        prompt += f" {caption}"

        await send_prompt(chat_id, prompt, tg_message_id)
        await state.set_state(MyConversation.non_generation)
    else:
        await bot.send_message(chat_id, 'Вы обязательно должны прикрепить prompt в сообщении с картинкой-референсом! Попробуйте еще раз.')
        await state.set_state(MyConversation.non_generation)


async def handle_help(message: types.Message, state: FSMContext):
    ''' Handling Техническая Поддержка button'''
    await state.set_state(MyConversation.non_generation)
    chat_id = message.chat.id
    button1 = InlineKeyboardButton('Техническая поддержка', url = 'https://t.me/Kwazzart')
    button2 = InlineKeyboardButton('Сотрудничество и прочие вопросы', url = 'https://t.me/to505to505')
    keyboard = InlineKeyboardMarkup().row(button1, button2)
    await bot.send_message(chat_id, f'При обращении в поддержку, пожалуйста, сообщите свой id: {chat_id}', reply_markup=keyboard)


#Handlers of buttons like U1, U2 etc, 
async def button_gen_handler(callback_query: CallbackQuery, state: FSMContext):
    method = callback_query.data.get('method')
    image_number = callback_query.data.get('image_numb  er')
    tg_message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id

    message = await bot.get_message(chat_id=chat_id, message_id=tg_message_id)
    original_message_id = message.reply_to_message.message_id
    response = await push_button(chat_id, original_message_id, tg_message_id, method, image_number)
    return response





    

        
      