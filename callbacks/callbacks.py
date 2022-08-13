from dispatcher import dp
from aiogram import filters, types
import db
from localisation.localisation import locale
import re

async def show_menu(message:types.Message, reply_text=None, edit=False):
    buttons = [
        [{"text":locale.get(message.chat.id, "btn_show"), "callback_data":"show"}], 
        [{"text":locale.get(message.chat.id, "btn_create"), "callback_data":"create"}],
        [{"text":locale.get(message.chat.id, "language"), "callback_data":"lang"}]
    ]
    db.set_user_settings(message.chat.id, is_add_task=False)
    if not reply_text: reply_text=locale.get(message.chat.id, "menu")
    if edit:
        if message.text != reply_text:
            await message.edit_text(reply_text, reply_markup=types.InlineKeyboardMarkup(2, buttons))
    else:
        await message.answer(reply_text, reply_markup=types.InlineKeyboardMarkup(2, buttons))

# main menu if callback "back" 
@dp.callback_query_handler(filters.Text("back"))
async def back(query, reply_text=None):
    db.set_user_settings(query.message.chat.id, is_add_task=False)
    # edit text because callback query has inline buttons 
    await show_menu(query.message, reply_text, edit=True)

# show menu
@dp.callback_query_handler(filters.Text("show"))
async def show_task(query:types.CallbackQuery):
    tasks = db.get_task(query.message.chat.id)
    if tasks:
        # show task list by buttons + button "back"
        buttons = [[{"text":f"{t[1]}", "callback_data":f"delete {t[0]}"}] for t in tasks] + [[{"text":locale.get(query.message.chat.id, "back"), "callback_data":"back"}]]
        await query.message.edit_text(locale.get(query.message.chat.id, "menu_show"), 
                                reply_markup=types.InlineKeyboardMarkup(len(tasks), buttons))
    else:
        await query.answer(locale.get(query.message.chat.id, "no_task"))
        await show_menu(query.message, edit=True)

# create task
@dp.callback_query_handler(filters.Text("create"))
async def create_task(query:types.CallbackQuery):
    db.set_user_settings(query.message.chat.id, is_add_task=True)
    await query.message.edit_text(locale.get(query.message.chat.id, "menu_create"), 
                                    reply_markup=None)

# language callback
@dp.callback_query_handler(filters.Text("lang"))
async def lang(query:types.CallbackQuery):
    locale.set_for_user(query.message.chat.id)
    await show_menu(query.message, edit=True)

# callback_query_task
@dp.callback_query_handler(filters.Text)
async def callback_query_task(query:types.CallbackQuery):
    # delete task by task_id and user_id 
    # callback_query pattern "delete task_id"
    if re.match(r"delete \d+", query.data):
        task_id = int(query.data.replace("delete ", ""))
        db.remove_task(query.from_user.id, task_id)
        await show_task(query)