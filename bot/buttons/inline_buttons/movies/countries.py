from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.api.movies.countries import Country


def countries_btn(page: int = 1):
    countries = Country().list()
    start_index = (page - 1) * 10
    end_index = min(start_index + 10, len(countries))

    builder = InlineKeyboardBuilder()

    c = 0
    for i in range(start_index, end_index):
        button = InlineKeyboardButton(
            text=countries[i]['name'], callback_data=f"{countries[i]['name']}_{countries[i]['id']}"
        )
        c += 1
        if c % 2 != 0:
            builder.row(button)
        else:
            builder.add(button)

    if start_index >= 1 and end_index < len(countries):
        builder.row(
            InlineKeyboardButton(
                text='⬅️', callback_data=f"countryprev_{page}"
            ),
            InlineKeyboardButton(
                text='➡️', callback_data=f"countrynext_{page}"
            )
        )
        return builder.as_markup()

    if start_index >= 1:
        builder.row(
            InlineKeyboardButton(
                text='⬅️', callback_data=f"countryprev_{page}"
            )
        )

    if end_index < len(countries):
        builder.row(
            InlineKeyboardButton(
                text='➡️', callback_data=f"countrynext_{page}"
            )
        )

    return builder.as_markup()
