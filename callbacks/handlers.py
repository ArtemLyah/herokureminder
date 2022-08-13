from aiogram import filters, types
from dispatcher import dp
import db
from localisation.localisation import locale

@dp.message_handler(filters.Command(["start"]))
async def start(message:types.Message):
    db.add_user(message.chat.id)
    await message.answer(locale.get(message.chat.id, "start"))

# main menu
@dp.message_handler(filters.Command("menu"))
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

# processing text
@dp.message_handler(filters.Text)
async def other(message:types.Message):
    if db.get_from_user_settings(message.chat.id, ["is_add_task"]):
        if db.get_task(message.chat.id, message.text):
            await message.answer(locale.get(message.chat.id, "have_task"), reply=True)
            await show_menu(message)
        else:
            db.create_task(message.chat.id, message.text)
            await message.answer(locale.get(message.chat.id, "task_added"), reply=True)
            await show_menu(message)
