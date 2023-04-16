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


from back_functions import send_id, hello
from back_functions import send_prompt, download_photo

#bot = Bot(token = '6076696755:AAHWtI_46iKQG3NxYAfV65Zi4sXFWME3TmQ')
bot = Bot(token = os.getenv("APP_TOKEN"))
dp = Dispatcher(bot)


callback_data = CallbackData("button", "action")

class MyConversation(StatesGroup):
    state1 = State()
    state2 = State()



# async def send_with_buttons(message: Message):
#     markup = InlineKeyboardMarkup()
#     markup.row(
#         InlineKeyboardButton("Button 1", callback_data=callback_data.new(action="action1")),
#         InlineKeyboardButton("Button 2", callback_data=callback_data.new(action="action2")),
#     )
#     await message.answer("Choose an action:", reply_markup=markup)

# Define a function to handle button clicks
async def button_gen_handler(callback_query: CallbackQuery, state: FSMContext):
    action = callback_query.data.get("action")
    if action == "action1":
        await state.set_state(MyConversation.state1)
        result = push_button(chat_id, prompt, button)
    elif action == "action2":
        await callback_query.answer("You clicked button 2")
        await state.set_state(MyConversation.state2)

# Add handlers to the dispatcher
#dp.register_message_handler(send_with_buttons, Command("start"))
#dp.register_callback_query_handler(button_handler, callback_data.filter(action=["action1", "action2"]))










async def button_clicked_callback_handler(query: CallbackQuery):
    # Get the callback data from the query
    callback_data = query.data
    # Do something with the callback data
    await query.answer(text=f"You clicked the button with callback data '{callback_data}'!")



#@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Сгенерировать изображение")
    button2 = KeyboardButton("Мой профиль")
    button3 = KeyboardButton("Техническая поддержка")
    keyboard.row(button1, button2)
    keyboard.add(button3)
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'hello world)', reply_markup = keyboard)
    await send_id(chat_id)
    
#@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    chat_id = message.chat.id
    server_response = await hello()
    await bot.send_message(chat_id, server_response, reply_markup = keyboard)
    
#@dp.message_handler(commands=['test'])
async def send_help(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Test 200 kind of, OK", reply_markup = keyboard)


#@dp.message_handler(text="Сгенерировать изображение")
async def handle_generate(message: types.Message):

    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Напишите prompt и по желанию прикрепите картинку-референс.')

    #только промпт
    @dp.message_handler(content_types=types.ContentTypes.TEXT)
    async def handle_prompt(message: types.Message):
        prompt = message.text
        mess_id = message.id
        await bot.send_message(chat_id, f'Изображение генерируется по запросу: \n{prompt}\n Пожалуйста, подождите!')
        result = await send_prompt(chat_id, prompt, mess_id)
        photo_path = await download_photo(chat_id, mess_id, result)
        caption = 'Держи фото!'
        with open(photo_path, 'rb') as photo_file:
            await bot.send_photo(chat_id=chat_id, photo=photo_file, caption=caption)



    #промпт + референс
    @dp.message_handler(content_types=types.ContentTypes.PHOTO)
    async def handle_photo(message: types.Message):
        if message.caption:
            caption = message.caption
        else:
            await bot.send_message(chat_id, 'Вы обязательно должны прикрепить prompt в сообщении с картинкой-референсом! Попробуйте еще раз.')
            return

        file_id = message.photo[-1].file_id
        file = await bot.download_file_by_id(file_id)
        with open("photo.jpg", "wb") as f:
            f.write(file.read())
        await bot.send_message(chat_id, f'Изображение генерируется по картинке-референсу и по запросу: \n{caption}\n Пожалуйста, подождите!')
   #     result = send_prompt_photo(chat_id, caption, file)
 #       send_result(chat_id, caption, result)



# async def handle_callback_query(callback_query: CallbackQuery):
#     handle_callback_query(callback_query: CallbackQuery)



# button1 = InlineKeyboardButton(text="U1", callback_data="U1")
# button2 = InlineKeyboardButton(text="U2", callback_data="U2")
# button3 = InlineKeyboardButton(text="U3", callback_data="U3")
# button4 = InlineKeyboardButton(text="U4", callback_data="U4")
# button5 = InlineKeyboardButton(text="V1", callback_data="V1")
# button6 = InlineKeyboardButton(text="V2", callback_data="V2")
# button7 = InlineKeyboardButton(text="V3", callback_data="V3")
# button8 = InlineKeyboardButton(text="V4", callback_data="V4")
# button9 = InlineKeyboardButton(text="Reroll", callback_data="Reroll")

# keyboard1 = InlineKeyboardMarkup()
# keyboard1.row(button1, button2, button3, button4, button9)
# keyboard1.row(button5, button6, button7, button8)
# await bot.send_message(chat_id, reply_markup = keyboard)



async def handle_help(message: types.Message):
    chat_id = message.chat.id
    button1 = InlineKeyboardButton('Техническая поддержка', url = 'https://t.me/Kwazzart')
    button2 = InlineKeyboardButton('Сотрудничество и прочие вопросы', url = 'https://t.me/to505to505')
    button3 = InlineKeyboardButton('FAQ', callback_data=callback_data.new(action="faq"))
    keyboard = InlineKeyboardMarkup().row(button1, button2)
    keyboard.add(button3)
    await bot.send_message(chat_id, f'При обращении в поддержк, пожалуйста, сообщите свой id: {chat_id}')




    #Хорошие кнопки 

    # async def button_gen_handler(callback_query: CallbackQuery, state: FSMContext):
        #     action = callback_query.data.get("action")
        #     if action == "action1":
        #         await state.set_state(MyConversation.state1)
        #         result = push_button(chat_id, prompt, button)
        #     elif action == "action2":
        #         await callback_query.answer("You clicked button 2")
        #         await state.set_state(MyConversation.state2)
