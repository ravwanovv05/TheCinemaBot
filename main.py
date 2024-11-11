import os
import sys
import asyncio
import logging
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from bot.api.movies.movies import Movie
from bot.handlers.adverts.advertising import advert, send_post_for_all_users
from bot.handlers.main import start, new
from bot.handlers.movies.add_movies import get_title_of_movie, get_description_of_movie, get_year_of_movie, \
    get_series_of_movie, get_code_of_movie, get_language_of_movie, get_country_of_movie
from bot.handlers.movies.categories import sub_categories
from bot.handlers.movies.movies import get_movie_by_code
from bot.models.advertising import Advert
from bot.models.movies.movies import MovieModel

load_dotenv()


token = os.getenv('TOKEN')

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(token=token)
    dp = Dispatcher(bot=bot)

    dp.message.register(start, Command(commands='start'))

    dp.message.register(advert, Command(commands='advert'))
    dp.message.register(send_post_for_all_users, Advert.post)

    dp.message.register(new, Command(commands='new'))
    dp.message.register(get_title_of_movie, MovieModel.title)
    dp.message.register(get_description_of_movie, MovieModel.description)
    dp.message.register(get_year_of_movie, MovieModel.year)
    dp.message.register(get_series_of_movie, MovieModel.series)
    dp.callback_query.register(get_country_of_movie, MovieModel.country_id)
    dp.callback_query.register(get_language_of_movie, MovieModel.language_id)
    dp.message.register(get_code_of_movie, MovieModel.code)

    dp.message.register(get_movie_by_code)

    dp.callback_query.register(sub_categories, lambda query: query.data.startswith(('category', 'subcategory', 'backtocategory')))


    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
