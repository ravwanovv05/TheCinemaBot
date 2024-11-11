from aiogram.fsm.state import  State, StatesGroup


class Advert(StatesGroup):
    post = State()