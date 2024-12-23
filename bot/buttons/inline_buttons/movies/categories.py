from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.api.movies.categories import Category


def categories_list_btn(page: int = 1):
    categories = Category().categories()
    start_index = (page - 1) * 10
    end_index = min(start_index + 10, len(categories))
    builder = InlineKeyboardBuilder()

    c = 0
    for i in range(start_index, end_index):
        button = InlineKeyboardButton(
            text=categories[i]['name'], callback_data=f"category_{categories[i]['name']}_{categories[i]['id']}"
        )
        c += 1
        if c % 2 != 0:
            builder.row(button)
        else:
            builder.add(button)

    if start_index >= 1 and end_index < len(categories):
        builder.row(
            InlineKeyboardButton(
                text='⬅️', callback_data=f"categoryprev_{page}"
            ),
            InlineKeyboardButton(
                text='➡️', callback_data=f"categorynext_{page}"
            )
        )
        return builder.as_markup()

    if start_index >= 1:
        builder.row(
            InlineKeyboardButton(
                text='⬅️', callback_data=f"categoryprev_{page}"
            )
        )

    if end_index < len(categories):
        builder.row(
            InlineKeyboardButton(
                text='➡️', callback_data=f"categorynext_{page}"
            )
        )

    return builder.as_markup()


