import os
import sys
import asyncio
import logging
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers.advertisement.advertising import advert, send_post_for_all_users
from bot.handlers.main import start, new
from bot.handlers.movies.add_movies import (
    get_title_of_movie, get_description_of_movie, get_year_of_movie,
    get_series_of_movie, get_code_of_movie, get_language_of_movie, get_country_of_movie, get_genre_of_movie
)
from bot.handlers.movies.categories import sub_categories
from bot.handlers.movies.collections import collections_handler, back_to_main_handler
from bot.handlers.movies.filters import filter_movie, select_data, selected_data
from bot.models.advertising import Advert
from bot.models.movies.filters import Filter
from bot.models.movies.movies import MovieModel
from bot.handlers.movies.search import inline_forward_video

load_dotenv()

token = os.getenv('TOKEN')


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(token=token)
    dp = Dispatcher(bot=bot)

    dp.message.register(start, Command(commands='start'))
    # dp.inline_query.register(inline_forward_video)

    dp.message.register(advert, Command(commands='advert'))
    dp.message.register(send_post_for_all_users, Advert.post)

    # add movie
    dp.message.register(new, Command(commands='new'))
    dp.message.register(get_title_of_movie, MovieModel.title)
    dp.message.register(get_description_of_movie, MovieModel.description)
    dp.message.register(get_year_of_movie, MovieModel.year)
    dp.message.register(get_series_of_movie, MovieModel.series)
    dp.callback_query.register(get_country_of_movie, MovieModel.country_id)
    dp.callback_query.register(get_genre_of_movie, MovieModel.genre_id)
    dp.callback_query.register(get_language_of_movie, MovieModel.language_id)
    dp.message.register(get_code_of_movie, MovieModel.code)

    dp.callback_query.register(sub_categories, lambda query: query.data.startswith(('category', 'subcategory', 'backtocategory')))

    dp.message.register(collections_handler, lambda message: message.text == '🗂 To\'plamlar')

    dp.message.register(filter_movie, lambda message: message.text == '🌪️ Filtr')
    dp.inline_query.register(select_data)
    dp.message.register(selected_data)

    dp.callback_query.register(back_to_main_handler, lambda query: query.data == 'back_to_main')

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
