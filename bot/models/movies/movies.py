from aiogram.filters.state import State, StatesGroup


class MovieModel(StatesGroup):
    category_id = State()
    title = State()
    description = State()
    year = State()
    series = State()
    country_id = State()
    language_id = State()
    code = State()
    file_id = State()
