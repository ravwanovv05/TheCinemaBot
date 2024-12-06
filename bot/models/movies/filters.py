from aiogram.filters.state import State, StatesGroup


class Filter(StatesGroup):
    from_year = State()
    to_year = State()
    genre_id = State()
    country_id = State()
