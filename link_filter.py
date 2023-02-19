from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
import re


class Link_filter(BoundFilter):
    async def check(self, message: types.Message):
        return 'http' in message.text
