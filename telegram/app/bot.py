from aiogram import Bot, Dispatcher
import os
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode

import aioredis
import redis 

logging.basicConfig(level=logging.DEBUG)


BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN = 

#test 
#BOT_TOKEN = '6284620288:AAHYt9Xru76sPk20_rgnRvmk7poIzgth3Gk'

#storage = RedisStorage2(host=os.getenv("REDIS_HOST"), port=6379, db=0)
storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN)#, parse_mode=ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=storage)
