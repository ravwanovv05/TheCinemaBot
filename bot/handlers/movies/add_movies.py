import os
from dotenv import load_dotenv
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from bot.api.movies.movies import Movie
from bot.buttons.inline_buttons.movies.countries import countries_btn
from bot.buttons.inline_buttons.movies.genres import genres_btn
from bot.buttons.inline_buttons.movies.languages import languages_btn
from bot.models.movies.movies import MovieModel

load_dotenv()


async def get_title_of_movie(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(title=message.text)
    await state.set_state(MovieModel.year)
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer('year:')


async def get_year_of_movie(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(year=message.text)
    await state.set_state(MovieModel.part)
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer('part:')


async def get_series_of_movie(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(part=message.text)
    await state.set_state(MovieModel.country_id)
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer('country:', reply_markup=countries_btn(page=1))


async def get_country_of_movie(query: types.CallbackQuery, state: FSMContext, bot: Bot):
    if query.data.startswith('countryprev'):
        page = int(query.data.split('_')[-1]) - 1
        await state.set_state(MovieModel.country_id)
        await bot.edit_message_text(
            'country:', chat_id=query.from_user.id, message_id=query.message.message_id,
            reply_markup=countries_btn(page=page)
        )
    elif query.data.startswith('countrynext'):
        page = int(query.data.split('_')[-1]) + 1
        await state.set_state(MovieModel.country_id)
        await bot.edit_message_text(
            'country:', chat_id=query.from_user.id, message_id=query.message.message_id,
            reply_markup=countries_btn(page=page)
        )
    else:
        await state.update_data(country_id=query.data.split()[-1])
        await state.set_state(MovieModel.genre_id)
        await bot.edit_message_text(
            'genre:', chat_id=query.from_user.id, message_id=query.message.message_id,
            reply_markup=genres_btn(page=1)
        )


async def get_genre_of_movie(query: types.CallbackQuery, bot: Bot, state: FSMContext):
    if query.data.startswith('genreprev'):
        page = int(query.data.split('_')[-1]) - 1
        await state.set_state(MovieModel.genre_id)
        await bot.edit_message_text(
            'genre:', chat_id=query.from_user.id, message_id=query.message.message_id,
            reply_markup=genres_btn(page=page)
        )
    elif query.data.startswith('genrenext'):
        page = int(query.data.split('_')[-1]) + 1
        await state.set_state(MovieModel.genre_id)
        await bot.edit_message_text(
            'genre:', chat_id=query.from_user.id, message_id=query.message.message_id,
            reply_markup=genres_btn(page=page)
        )
    else:
        await state.update_data(genre_id=query.data)
        await state.set_state(MovieModel.language_id)
        await bot.edit_message_text(
            'language: ', chat_id=query.from_user.id, message_id=query.message.message_id,
            reply_markup=languages_btn()
        )


async def get_language_of_movie(query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(language_id=query.data)
    await state.set_state(MovieModel.code)
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text='send movie:')


async def get_code_of_movie(message: types.Message, state: FSMContext, bot: Bot):
    channel_id = int(os.getenv('MOVIES_CHANNEL_ID'))
    try:
        movie = await bot.send_video(channel_id, message.video.file_id)
        await state.update_data(code=movie.message_id)
        data = await state.get_data()
        add_movie = Movie(
            title=data['title'],
            year=data['year'],
            part=data['part'],
            code=data['code'],
            genre_id=int(data['genre_id'].split('_')[-1]),
            country_id=int(data['country_id'].split('_')[-1]),
            language_id=int(data['language_id'].split('_')[-1]),
            category_id=int(data['category_id'])
        ).save()
        await state.clear()
        await bot.delete_message(message.from_user.id, message.message_id - 1)
        await bot.delete_message(message.from_user.id, message.message_id)
        await message.answer('Successfully added movie!')
    except Exception as e:
        await message.answer(str(e))

