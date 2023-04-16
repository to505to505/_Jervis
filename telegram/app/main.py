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

logging.basicConfig(level=logging.INFO)

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
            print(response_text)

async def push_button(chat_id, propmpt, button):
    pass

async def send_result(chat_id, prompt, result):
    with open('photo.jpg', 'rb') as photo:
        await bot.send_photo(chat_id, photo=InputFile(photo))
        
    button1 = InlineKeyboardButton(text="U1", callback_data="U1")
    button2 = InlineKeyboardButton(text="U2", callback_data="U2")
    button3 = InlineKeyboardButton(text="U3", callback_data="U3")
    button4 = InlineKeyboardButton(text="U4", callback_data="U4")
    button5 = InlineKeyboardButton(text="V1", callback_data="V1")
    button6 = InlineKeyboardButton(text="V2", callback_data="V2")
    button7 = InlineKeyboardButton(text="V3", callback_data="V3")
    button8 = InlineKeyboardButton(text="V4", callback_data="V4")
    button9 = InlineKeyboardButton(text="Reroll", callback_data="Reroll")

    keyboard1 = InlineKeyboardMarkup()
    keyboard1.row(button1, button2, button3, button4, button9)
    keyboard1.row(button5, button6, button7, button8)

bot = Bot(token=os.getenv("APP_TOKEN"))
dp = Dispatcher(bot)
    
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'hello world)', reply_markup = keyboard)
    await send_id(chat_id)
    
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    chat_id = message.chat.id
    server_response = await hello()
    await bot.send_message(chat_id, server_response, reply_markup = keyboard)
    
@dp.message_handler(commands=['test'])
async def send_help(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Test 200 kind of, OK", reply_markup = keyboard)

# Define the keyboard
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton("Сгенерировать изображение")
button2 = KeyboardButton("Мой профиль")
button3 = KeyboardButton("Техническая поддержка")
keyboard.row(button1, button2)
keyboard.add(button3)

@dp.message_handler(text="Сгенерировать изображение")
async def handle_generate(message: types.Message):

    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Напишите prompt и по желанию прикрепите картинку-референс.')

    #только промпт
    @dp.message_handler(content_types=types.ContentTypes.TEXT)
    async def handle_prompt(message: types.Message):
        prompt = message.text
        await bot.send_message(chat_id, f'Изображение генерируется по запросу: \n{prompt}\n Пожалуйста, подождите!')
        result = await send_prompt(chat_id, prompt)
    
        send_result(chat_id, prompt, result)

        @dp.message_handler(text="U1")
        async def handle_U1(message: types.Message):
            pass

    #промпт + референс
    @dp.message_handler(content_types=types.ContentTypes.PHOTO)
    async def handle_photo(message: types.Message):
        if message.caption:
            caption = message.caption
        else:
            await bot.send_message(chat_id, 'Вы обязательно должны прикрепить prompt в сообщении с картинкой-референсом! Попробуйте еще раз.')

        file_id = message.photo[-1].file_id
        file = await bot.download_file_by_id(file_id)
        with open("photo.jpg", "wb") as f:
            f.write(file.read())
        await bot.send_message(chat_id, f'Изображение генерируется по картинке-референсу и по запросу: \n{prompt}\n Пожалуйста, подождите!')
        result = send_prompt_photo(chat_id, caption, file)
        send_result(chat_id, caption, result)


# dp.register_message_handler(handle_photo, Text(equals="Option 1"), content_types=types.ContentTypes.PHOTO)
#dp.register_message_handler(start_handler, commands=['start'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

