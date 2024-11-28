from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


def main_btn():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text='Kod'), KeyboardButton(text='Qidirish 🔍')
    )
    return builder.as_markup(resize_keyboard=True)
