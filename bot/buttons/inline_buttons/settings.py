from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def settings_btn():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="👨‍💼 Qo'llab quvvatlash")
    )

    return builder.as_markup()
