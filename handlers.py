from datetime import datetime
from aiogram import filters, types
from dispatcher import dp
import re
import db

# main menu if callback query 
@dp.callback_query_handler(filters.Text("back"))
async def back(query, reply_text="Choose a button"):
    buttons = [
        [{"text":"Show tasks", "callback_data":"show"}], 
        [{"text":"Create a new task", "callback_data":"create"}]
    ]
    db.set_is_create_task(query.from_user.id, 0)
    # edit text because callback query has inline buttons 
    await query.message.edit_text(reply_text, reply_markup=types.InlineKeyboardMarkup(2, buttons))

# buttons "show task" and "create task" 
# show menu
@dp.callback_query_handler(filters.Text("show"))
async def show_task(query:types.CallbackQuery):
    tasks = db.get_task(query.from_user.id)
    if tasks:
        # show task list by buttons + button "back"
        buttons = [[{"text":f"{t[1]}", "callback_data":f"delete {t[0]}"}] for t in tasks] + [[{"text":"<< Back", "callback_data":"back"}]]
        await query.message.edit_text("There are your tasks\nPress on a taks to delete it", 
                                reply_markup=types.InlineKeyboardMarkup(len(tasks), buttons))
    else:
        await query.answer("You don't have tasks. Try to create one")
        await show_menu(query.message, edit=True)
# create task
@dp.callback_query_handler(filters.Text("create"))
async def create_task(query:types.CallbackQuery):
    db.set_is_create_task(query.from_user.id, 1)
    await query.message.delete_reply_markup()
    await query.message.edit_text("Create a new task 📝\nWrite your task and press Enter.\nIf you would like to switch on an alarm use the pattern alarm(HH:MM:SS) and if you would like you can write a date alarm(HH:MM:SS DD/MM/YYYY)")

# callback_query_task
@dp.callback_query_handler(filters.Text)
async def callback_query_task(query:types.CallbackQuery):
    # delete task by task_id and user_id 
    # callback_query pattern "delete task_id"
    if re.match(r"delete \d+", query.data):
        task_id = int(query.data.replace("delete ", ""))
        db.remove_task(query.from_user.id, task_id)
        await show_task(query)


@dp.message_handler(filters.Command(["start"]))
async def start(message:types.Message):
    db.add_user(message.from_user.id)
    await message.answer("Hello I am reminder 🗓.\nLet's create your tasks /menu")
# main menu
@dp.message_handler(filters.Command("menu"))
async def show_menu(message:types.Message, reply_text="Choose a button", edit=False):
    buttons = [
        [{"text":"Show tasks", "callback_data":"show"}], 
        [{"text":"Create a new task", "callback_data":"create"}]
    ]
    db.set_is_create_task(message.from_user.id, 0)
    if edit:
        if message.text != reply_text:
            await message.edit_text(reply_text, reply_markup=types.InlineKeyboardMarkup(2, buttons))
    else:
        await message.answer(reply_text, reply_markup=types.InlineKeyboardMarkup(2, buttons))
# processing text
@dp.message_handler(filters.Text)
async def other(message:types.Message):
    if db.get_is_create_task(message.from_user.id):
        text = message.text
        # process alarm function
        alarm_time = re.search(r"alarm\(.*\)", message.text)
        if alarm_time:
            alarm_time = alarm_time.group()[6:][:-1]
            text = re.sub(r"alarm\(.*\)", "", message.text)
        if db.get_task(message.from_user.id, text):
            await message.answer("You already have the task")
            await show_menu(message)
        else:
            db.create_task(message.from_user.id, text, alarm_time)
            await message.answer("Your task successfully added")
            await show_menu(message)
