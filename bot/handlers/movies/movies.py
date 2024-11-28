import os
from dotenv import load_dotenv
from aiogram import types, Bot
from bot.api.movies.movies import Movie
from bot.buttons.inline_buttons.inline_queries import search_inline

load_dotenv()

async def get_movies(message: types.Message, bot: Bot):
    if message.text == 'Qidirish 🔍':
        await message.answer('Kerakli filmni topish uchun "Qidiruvni boshlash" tugmasini bosing va so\'rovingizni kiriting.', reply_markup=search_inline())
    else:
        pass
