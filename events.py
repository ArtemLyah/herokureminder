from dispatcher import bot
import asyncio
from db import db_tasks

async def get_alarm_tasks():
    while True:
        await asyncio.sleep(5)
        tasks = db_tasks.get_alarm_tasks()
        if tasks:
            for t in tasks:
                user_id = t[0]
                text = t[1]
                await bot.send_message(user_id, text)
                db_tasks.remove_date_from_task(user_id, text)