from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


def main_reply_keyboards():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text='🔍 Qidiruv'), KeyboardButton(text='🗂 To\'plamlar')
    )
    builder.row(
        KeyboardButton(text='🌪️ Filtr'), KeyboardButton(text='⚙️ Sozlamalar')
    )
    return builder.as_markup(resize_keyboard=True)
