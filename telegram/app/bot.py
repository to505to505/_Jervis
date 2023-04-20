from aiogram import Bot, Dispatcher
import os
import logging

from aiogram.contrib.fsm_storage.redis import RedisStorage2

import aioredis
import redis 

logging.basicConfig(level=logging.DEBUG)


#BOT_TOKEN = os.getenv("BOT_TOKEN")
#BOT_TOKEN = '6076696755:AAHWtI_46iKQG3NxYAfV65Zi4sXFWME3TmQ'

#test 
BOT_TOKEN = '6284620288:AAHYt9Xru76sPk20_rgnRvmk7poIzgth3Gk'

storage = RedisStorage2('jervis_redis', 6379, db=0)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)#, storage=storage)