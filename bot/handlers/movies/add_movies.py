import os
from dotenv import load_dotenv
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from bot.api.movies.movies import Movie
from bot.buttons.inline_buttons.movies.countries import countries_btn
from bot.buttons.inline_buttons.movies.languages import languages_btn
from bot.models.movies.movies import MovieModel
from utils.movies.movies import write_details_of_movie

load_dotenv()

async def get_title_of_movie(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(MovieModel.description)
    await message.answer('description:')


async def get_description_of_movie(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(MovieModel.year)
    await message.answer('year:')


async def get_year_of_movie(message: types.Message, state: FSMContext):
    await state.update_data(year=message.text)
    await state.set_state(MovieModel.series)
    await message.answer('series:')

async def get_series_of_movie(message: types.Message, state: FSMContext):
    await state.update_data(series=message.text)
    await state.set_state(MovieModel.country_id)
    await message.answer('country:', reply_markup=countries_btn(page=1))

async def get_country_of_movie(query: types.CallbackQuery, state: FSMContext, bot: Bot):
    if query.data.startswith('countryprev'):
        page = int(query.data.split('_')[-1]) - 1
        await state.set_state(MovieModel.country_id)
        await bot.edit_message_text('country:', chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=countries_btn(page=page))
    elif query.data.startswith('countrynext'):
        page = int(query.data.split('_')[-1]) + 1
        await state.set_state(MovieModel.country_id)
        await bot.edit_message_text('country:', chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=countries_btn(page=page))
    else:
        await state.update_data(country_id=query.data)
        await state.set_state(MovieModel.language_id)
        await bot.edit_message_text('language: ', chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=languages_btn())


async def get_language_of_movie(query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(language_id=query.data)
    await state.set_state(MovieModel.code)
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await bot.send_message(chat_id=query.from_user.id, text='send movie:')

async def get_code_of_movie(message: types.Message, state: FSMContext, bot: Bot):
    channel_id = int(os.getenv('MOVIES_CHANNEL_ID'))
    data = await state.get_data()
    movie = await bot.copy_message(
        channel_id, message.from_user.id, message.message_id,
        caption=write_details_of_movie(data)
    )
    await state.update_data(code=movie.message_id)
    data = await state.get_data()
    add_movie = Movie(
        title=data['title'],
        description=data['description'],
        year=data['year'],
        series=data['series'],
        code=data['code'],
        country_id=int(data['country_id'].split('_')[-1]),
        language_id=int(data['language_id'].split('_')[-1]),
        category_id=int(data['category_id'])
    ).save()
    await state.clear()
    await message.answer('Successfully added movie!')
