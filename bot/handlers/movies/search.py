import os
from aiogram import Bot
from aiogram.types import InlineQuery, InlineQueryResultVideo, InputTextMessageContent
from dotenv import load_dotenv

from bot.api.movies.genres import Genre
from bot.api.movies.movies import Movie

load_dotenv()

CHANNEL_LINK = os.getenv('MOVIES_CHANNEL_LINK')


async def search_movies(inline_query: InlineQuery, bot: Bot):
    query = inline_query.query

    if not query:
        movies = Movie().all_movies()
    else:
        movies = Movie().search_movies(query)

    results = []
    thumbnail_url = 'https://www.creativefabrica.com/wp-content/uploads/2018/11/Movie-logo-by-meisuseno-3-580x446.jpg'
    for movie in movies:
        results.append(
            InlineQueryResultVideo(
                id=str(movie['id']),
                video_url=f"https://t.me/{CHANNEL_LINK}/{movie['code']}",
                mime_type='video/mp4',
                title=f"{movie['title']} {movie['part'] if movie['part'] > 1 else ''}",
                description=f"{Genre().details(movie['genre_id'])['name']} | {movie['year']}",
                thumbnail_url=thumbnail_url,
                input_message_content=InputTextMessageContent(message_text=f"search_{movie['code']}")
            )
        )

    await bot.answer_inline_query(inline_query_id=inline_query.id, results=results, cache_time=0, request_timeout=0)
    