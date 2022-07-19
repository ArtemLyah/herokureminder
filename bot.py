from aiogram import executor
from dispatcher import dp
from events import get_alarm_tasks
import handlers

if __name__ == "__main__":
    dp.loop.create_task(get_alarm_tasks())
    executor.start_polling(dp, skip_updates=True)

