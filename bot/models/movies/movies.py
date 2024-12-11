from aiogram.filters.state import State, StatesGroup


class MovieModel(StatesGroup):
    category_id = State()
    title = State()
    year = State()
    part = State()
    country_id = State()
    genre_id = State()
    language_id = State()
    code = State()
    file_id = State()
