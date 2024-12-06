from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def collections_inline_keyboards():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='📃 Mashhur', switch_inline_query_current_chat='#collection1')
    )
    builder.row(
        InlineKeyboardButton(text='📃 Yangi filmlar', switch_inline_query_current_chat='#collection2')
    )
    builder.row(
        InlineKeyboardButton(text='📃 Yangi seriallar', switch_inline_query_current_chat='#collection3')
    )
    builder.row(
        InlineKeyboardButton(text='🗂 Mening to\'plamlarim', callback_data='my_collections')
    )
    builder.row(
        InlineKeyboardButton(text='🔙 Ortga', callback_data='back_to_main')
    )
    return builder.as_markup()
