import logging

from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor


API_TOKEN = '5618279321:AAHp0qAld0EjJCqmVkdqL2rCG9HibaAjKDY'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Привет!")
    await message.answer("Я checker_link_bot!")
    await message.answer("Я могу проверить безопасный ли сайт, который ты хочешь посетить.")
    await message.answer("Кинь ссылку на сайт, если хочешь в этом убедиться")


@dp.message_handler()
async def my_message_handler(message: types.Message):
    await message.reply('сейчас проверим')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
