from aiogram import executor
from dispatcher import dp
from callbacks import handlers, callbacks

if __name__ == "__main__":
    print("OK")
    executor.start_polling(dp)

