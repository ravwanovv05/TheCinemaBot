import os
import pytz
from datetime import datetime
from dotenv import load_dotenv
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultVideo
from bot.api.movies.categories import Category
from bot.api.movies.countries import Country
from bot.api.movies.genres import Genre
from bot.api.movies.movies import Movie
from bot.buttons.inline_buttons.movies.filters import filters_inline_keyboards
from utils.movies.movies import write_details_of_movie

load_dotenv()

CHANNEL_LINK = os.getenv('MOVIES_CHANNEL_LINK')
MOVIES_CHANNEL_ID = os.getenv('MOVIES_CHANNEL_ID')


async def filter_movie(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    keys = list(data.keys())
    from_year = f"{data['from_year']} dan" if 'from_year' in keys else 'hammasi'
    to_year = f"{data['to_year']} gacha" if 'to_year' in keys else ''
    type_ = f"{data['type'].split('_')[-2]}" if 'type' in keys else 'hammasi'
    genre = f"{data['genre'].split('_')[-2]}" if 'genre' in keys else 'hammasi'
    country = f"{data['country'].split('_')[-2]}" if 'country' in keys else 'hammasi'

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await message.answer(
        f'Qidiruv filtri \n\n Filtrlarni tanlang va "🔍 Filtr bo\'yicha qidirish" tugmasini bosing \n\n'
        f'\n Tanlangan: \n'
        f'➡️ Yil: {from_year} {to_year}\n'
        f'➡️ Turi: {type_} \n'
        f'➡️ Janr: {genre} \n'
        f'➡️ Mamlakat: {country}',
        reply_markup=filters_inline_keyboards()
    )


async def select_data(inline_query: types.InlineQuery, state: FSMContext, bot: Bot):
    query = inline_query.query
    data = await state.get_data()
    keys = list(data.keys())

    print(data)
    results = []

    if query == '#filter_from_year' or query == '#filter_to_year':
        current_year = datetime.now(pytz.timezone('Asia/Tashkent')).year
        for year in list(range(current_year, 1975 - 1, -1)):
            if query == 'filter_from_year' and 'from_year' in keys and data['from_year'] == year:
                year = str(year) + '✅'
            if query == 'filter_to_year' and 'to_year' in keys and data['to_year'] == year:
                year = str(year) + '✅'

            results.append(
                InlineQueryResultArticle(
                    id=str(year),
                    title=str(year),
                    input_message_content=InputTextMessageContent(message_text=f"{query}_{year}")
                )
            )
    elif query == '#filter_type':
        categories = Category().categories()
        for category in categories:
            if 'type' in keys and int(data['type'].split('_')[-1]) == category['id']:
                title = category['name'] + '✅'
            else:
                title = category['name']
            results.append(
                InlineQueryResultArticle(
                    id=str(category['id']),
                    title=title,
                    input_message_content=InputTextMessageContent(
                        message_text=f"{query}_{category['name']}_{category['id']}"
                    )
                )
            )
    elif query == '#filter_genre':
        genres = Genre().genres_list()
        for genre in genres:
            if 'genre' in keys and int(data['genre'].split('_')[-1]) == genre['id']:
                title = genre['name'] + '✅'
            else:
                title = genre['name']
            results.append(
                InlineQueryResultArticle(
                    id=str(genre['id']),
                    title=title,
                    input_message_content=InputTextMessageContent(
                        message_text=f"{query}_{genre['name']}_{genre['id']}"
                    )
                )
            )
    elif query == '#filter_country':
        countries = Country().list()
        for country in countries:
            if 'country' in keys and int(data['country'].split('_')[-1]) == country['id']:
                title = country['name'] + '✅'
            else:
                title = country['name']
            results.append(
                InlineQueryResultArticle(
                    id=str(country['id']),
                    title=title,
                    input_message_content=InputTextMessageContent(
                        message_text=f"{query}_{country['name']}_{country['id']}"
                    )
                )
            )
    elif query == '#filter':
        movies = Movie().movie_filter(
            genre_id=int(data['genre'].split('_')[-1]) if 'genre' in keys else None,
            country_id=int(data['country'].split('_')[-1]) if 'country' in keys else None,
            from_year=data['from_year'] if 'from_year' in keys else None,
            to_year=data['to_year'] if 'to_year' in keys else None,
            category_id=int(data['type'].split('_')[-1]) if 'type' in keys else None
        )
        if movies:
            thumbnail_url = 'https://www.creativefabrica.com/wp-content/uploads/2018/11/Movie-logo-by-meisuseno-3-580x446.jpg'
            for movie in movies:
                results.append(
                    InlineQueryResultVideo(
                        id=str(movie['id']),
                        video_url=f"https://t.me/{CHANNEL_LINK}/{movie['code']}",
                        mime_type='video/mp4',
                        title=f"{movie['title']} {movie['part'] if movie['part'] > 1 else ''}",
                        description=write_details_of_movie(
                            category_id=movie['category_id'],
                            year=movie['year'],
                            country_id=movie['country_id'],
                            genre_id=movie['genre_id']
                        ),
                        thumbnail_url=thumbnail_url,
                        video_width=900,
                        video_height=900,
                        input_message_content=InputTextMessageContent(
                            message_text=f"filter_movie_{Category().details(movie['category_id'])['name']}_{movie['code']}"
                        )
                    )
                )

    await bot.answer_inline_query(inline_query.id, results=results, cache_time=0, request_timeout=0)


async def selected_data(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    keys = list(data.keys())
    if message.text:
        if message.text.startswith('filter_from_year'):
            if 'to_year' in keys and int(message.text.split('_')[-1]) > int(data['to_year']):
                from_year = int(data['to_year'])
            else:
                from_year = int(message.text.split('_')[-1])
            await bot.delete_message(message.chat.id, message.message_id)
            await state.update_data(from_year=from_year)

        elif message.text.startswith('filter_to_year'):
            if 'from_year' in keys and int(message.text.split('_')[-1]) < data['from_year']:
                to_year = data['from_year']
            else:
                to_year = int(message.text.split('_')[-1])
            await bot.delete_message(message.chat.id, message.message_id)
            await state.update_data(to_year=to_year)

        elif message.text.startswith('filter_type'):
            type_ = message.text.split('_')[-2] + '_' + message.text.split('_')[-1]
            await bot.delete_message(message.chat.id, message.message_id)
            await state.update_data(type=type_)

        elif message.text.startswith('filter_genre'):
            genre = message.text.split('_')[-2] + '_' + message.text.split('_')[-1]
            await bot.delete_message(message.from_user.id, message.message_id)
            await state.update_data(genre=genre)

        elif message.text.startswith('filter_country'):
            country = message.text.split('_')[-2] + '_' + message.text.split('_')[-1]
            await bot.delete_message(message.from_user.id, message.message_id)
            await state.update_data(country=country)

        elif message.text.startswith('filter_movie'):
            code = int(message.text.split('_')[-1])
            await bot.delete_message(message.from_user.id, message.message_id - 1)
            await bot.delete_message(message.from_user.id, message.message_id)
            if message.text.split('_')[-2] in ('Serial', 'Anime serial', 'Multserial'):
                pass
            else:
                await bot.copy_message(message.from_user.id, MOVIES_CHANNEL_ID, code)

        if not message.text.startswith('filter_movie'):
            new_data = await state.get_data()
            new_keys = list(new_data.keys())
            from_year = f"{new_data['from_year']} dan" if 'from_year' in new_keys else 'hammasi'
            to_year = f"{new_data['to_year']} gacha" if 'to_year' in new_keys else ''
            type_ = f"{new_data['type'].split('_')[-2]}" if 'type' in new_keys else 'hammasi'
            genre = f"{new_data['genre'].split('_')[-2]}" if 'genre' in new_keys else 'hammasi'
            country = f"{new_data['country'].split('_')[-2]}" if 'country' in new_keys else 'hammasi'

            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
            await message.answer(
                f'Qidiruv filtri \n\n Filtrlarni tanlang va "🔍 Filtr bo\'yicha qidirish" tugmasini bosing \n\n'
                f'\n Tanlangan: \n'
                f'➡️ Yil: {from_year} {to_year}\n'
                f'➡️ Turi: {type_} \n'
                f'➡️ Janr: {genre} \n'
                f'➡️ Mamlakat: {country}',
                reply_markup=filters_inline_keyboards()
            )
    elif message.video:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)


async def clear_filter(query: types.CallbackQuery, state: FSMContext, bot: Bot):
    try:
        await bot.edit_message_text(
            'Qidiruv filtri \n\n Filtrlarni tanlang va "🔍 Filtr bo\'yicha qidirish" tugmasini bosing \n\n'
            '\n Tanlangan: \n➡️ Yil: hammasi '
            '\n➡️ Turi: hammasi \n➡️ Janr: hammasi \n➡️ Mamlakat: hammasi',
            chat_id=query.from_user.id, message_id=query.message.message_id,
            reply_markup=filters_inline_keyboards(),
        )
        await query.answer('✅ Filtr tozalandi')
        await state.clear()
    except Exception as e:
        print(str(e))

