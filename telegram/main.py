import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message


logging.basicConfig(level=logging.INFO)

bot = Bot(token='6076696755:AAHWtI_46iKQG3NxYAfV65Zi4sXFWME3TmQ')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'hello world)', reply_markup = keyboard)




from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Define the keyboard
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton("Сгенерировать изображение")
button2 = KeyboardButton("Мой профиль")
button3 = KeyboardButton("Техническая поддержка")
keyboard.row(button1, button2)
keyboard.add(button3)

# Define the message handler function
@dp.message_handler(text=["Сгенерировать изображение", "Мой профиль", "Техническая поддержка"])
async def handle_keyboard(message: Message):
    chat_id = message.chat.id
    if message.text == "Сгенерировать изображение":
        await bot.send_message(chat_id, 'Напишите prompt и прие', reply_markup = keyboard)

        # Do something when Option 1 is selected  
    elif message.text == "Мой профиль":
        # Do something when Option 2 is selected
        pass
    elif message.text == "Техническая поддержка":
        # Do something when Option 3 is selected
        pass

@dp.message_handler(text="Сгенерировать изображение")
async def handle_option_one(message: types.Message):
    chat_id = message.chat.id
    # Send a message to request the image
    await bot.send_message(chat_id, 'Напишите prompt и прие')

    # Register a new handler to receive the image
    @dp.message_handler(content_types=types.ContentTypes.PHOTO)
    async def handle_image(message: Message):
    # Check if the message contains a caption
        if message.caption:
            caption = message.caption
        else:
            caption = "No caption provided"
    
    # Get the largest image from the list of photo sizes
    photo: PhotoSize = message.photo[-1]
    chat_id = message.chat.id
    
    # Download the image and save it to a file
    from aiogram.types import Message

# Assuming 'message' is the Message object received from the user
file_id = message.document.file_id  # or use message.photo.file_id for a photo
file = await bot.get_file(file_id)
filename = file.file_path.split("/")[-1]
await file.download(destination=f"./folder/{filename}")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

