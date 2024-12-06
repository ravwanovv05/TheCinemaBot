from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.api.movies.genres import Genre


def genres_btn(page: int = 1):
    genres = Genre().genres_list()
    start_index = (page - 1) * 10
    end_index = min(start_index + 10, len(genres))
    builder = InlineKeyboardBuilder()

    c = 0
    for i in range(start_index, end_index):
        button = InlineKeyboardButton(
            text=genres[i]['name'], callback_data=f"genre_{genres[i]['id']}"
        )
        c += 1
        if c % 2 != 0:
            builder.row(button)
        else:
            builder.add(button)

    if start_index >= 1 and end_index < len(genres):
        builder.row(
            InlineKeyboardButton(
                text='⬅️', callback_data=f"genreprev_{page}"
            ),
            InlineKeyboardButton(
                text='➡️', callback_data=f"genrenext_{page}"
            )
        )
        return builder.as_markup()

    if start_index >= 1:
        builder.row(
            InlineKeyboardButton(
                text='⬅️', callback_data=f"genreprev_{page}"
            )
        )

    if end_index < len(genres):
        builder.row(
            InlineKeyboardButton(
                text='➡️', callback_data=f"genrenext_{page}"
            )
        )

    return builder.as_markup()
