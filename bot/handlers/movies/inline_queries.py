import os
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.types import InlineQuery, InlineQueryResultVideo
from bot.api.movies.movies import Movie

load_dotenv()

CHANNEL_LINK = os.getenv('MOVIES_CHANNEL_LINK')

async def inline_forward_video(inline_query: InlineQuery, bot: Bot):
    query = inline_query.query

    if not query:
        movies = Movie().all_movies()
    else:
        movies = Movie().search_movies(query)
    

    results = []

    
    for movie in movies:
        results.append(
            InlineQueryResultVideo(
                id=str(movie['id']),
                video_url=f"https://t.me/{CHANNEL_LINK}/{movie['code']}",
                mime_type='video/mp4',
                title=movie['title'],
                description=movie['description'],
                thumbnail_url='https://t4.ftcdn.net/jpg/04/48/02/97/360_F_448029739_g5nVVSEtqpEWDSzZIu0BQLfN0LwtE9m9.jpg',
            )
        )

    await bot.answer_inline_query(inline_query_id=inline_query.id, results=results)
    