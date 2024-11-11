import os
from dotenv import load_dotenv
from aiogram import types, Bot
from bot.api.movies.movies import Movie

load_dotenv()

async def get_movie_by_code(message: types.Message, bot: Bot):
    if message.text.isnumeric():
        movie = Movie().movie_by_code(int(message.text))
        if len(movie) == 0:
            await message.answer('Noto\'g\'ri code!!!')
        else:
            channel_id = int(os.getenv('MOVIES_CHANNEL_ID'))
            await bot.copy_message(message.from_user.id, channel_id, int(message.text))
    else:
        await message.answer('Noto\'g\'ri code!!!')

