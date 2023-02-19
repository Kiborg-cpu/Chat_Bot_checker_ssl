import logging

from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from aiogram.types import ParseMode
from link_filter import Link_filter
from qr_code import translate_qr_code
from site_checker import Check_site

API_TOKEN = '5618279321:AAHp0qAld0EjJCqmVkdqL2rCG9HibaAjKDY'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.filters_factory.bind(Link_filter)
url_check = Check_site()


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.answer("Привет!✋")
    await message.answer("Я checker_link_bot!")
    await message.answer("Я могу проверить безопасный ли сайт, который ты хочешь посетить.🛠🛠🛠")
    await message.answer("Кинь ссылку или QR_code на сайт, если хочешь в этом убедиться.🧐🧐🧐")


@dp.message_handler(Link_filter())
async def message_info_link(message: types.Message):
    await message.reply('сейчас проверим...')
    await message.answer(check_site(message.text))


@dp.message_handler(content_types=['photo'])
async def message_info_qr_code_link(message: types.Message):
    file_photo = message.photo[-1].file_id
    idfile = await bot.get_file(file_photo)
    dowloaded_file_photo = await bot.download_file(idfile.file_path)
    link = translate_qr_code(dowloaded_file_photo)
    await message.answer(link)
    await message.answer(check_site(link), parse_mode=ParseMode.HTML)


def check_site(link):
    text = 'Этот сайт:\n'
    if url_check.is_valid(link):
        if url_check.get_ssl_cert(link):
            text += '✅ИМЕЕТ SSL СЕРТИФИКАТ' + '\n'
        else:
            text += '❌ОТСУТСТВУЕТ SSL СЕРТИФИКАТ\n'
        if url_check.check_redirect(link):
            text += '✅Нет переадресации на другую страницу'
        else:
            if len(url_check.r.history) > 1:
                text += '❌Есть переадресация на другие страницы:\n'
                for i, response in enumerate(url_check.r.history, 1):
                    text += f'{i}. {response.url}\n'
            else:
                text += '❌Есть переадресация на другую страницу:\n'
                text += url_check.r.history
        return text
    else:
        return 'Ошибка, возможно вы написали не правильно ссылку, повторите запрос'


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
