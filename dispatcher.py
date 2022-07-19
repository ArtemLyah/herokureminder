from aiogram import Bot, Dispatcher, executor
import logging
import config

logging.basicConfig(level=logging.ERROR)

bot = Bot(config.TOCKEN)
dp = Dispatcher(bot, executor.asyncio.get_event_loop())