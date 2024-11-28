from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def search_inline():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Qidirish", switch_inline_query_current_chat=''
        )
    )
    return builder.as_markup()

