from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.api.movies.languages import Language


def languages_btn():
    languages = Language().list()
    builder = InlineKeyboardBuilder()

    for language in languages:
        builder.row(
            InlineKeyboardButton(
                text=language['name'], callback_data=f"{language['name']}_{language['id']}"
            )
        )

    return builder.as_markup()
