import logging
import aiohttp
import os
from utils import *

logging.basicConfig(level=logging.INFO)

#BOT_TOKEN = '6076696755:AAHWtI_46iKQG3NxYAfV65Zi4sXFWME3TmQ'
BOT_TOKEN = os.getenv("BOT_TOKEN")

#HOST = "localhost"
HOST = os.getenv('DJANGO_HOST')


async def send_id(chat_id):
    data = {"chat_id": chat_id}
    response = await make_async_request_post(f"http://{HOST}:8000/api/tg/create_chat/", data=data)
    return response


async def send_prompt(chat_id, prompt, tg_message_id):
    data = {"chat_id": chat_id,
            "prompt": prompt,
            "tg_message_id": tg_message_id}
    response = await make_async_request_post(f"http://{HOST}:8000/api/tg/send_prompt/", data=data)
    return response


async def push_button(chat_id, tg_message_id, method, image_number):#, original_message_id):
    data = {"chat_id": chat_id,
            "tg_message_id": tg_message_id,
           # "original_message_id": original_message_id,
            "method": method,
            "image_number": image_number}   
    response = await make_async_request_post(f"http://{HOST}:8000/api/tg/push_button/", data=data)
    return response