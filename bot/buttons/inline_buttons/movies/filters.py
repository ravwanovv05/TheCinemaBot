from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def filters_inline_keyboards():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='➡️ Yil dan', switch_inline_query_current_chat='#filter_from_year')
    )
    builder.add(
        InlineKeyboardButton(text='️️️️️➡️ Yil gacha', switch_inline_query_current_chat='#filter_to_year')
    )
    builder.row(
        InlineKeyboardButton(text='➡️ Tur tanlash', switch_inline_query_current_chat='#filter_type')
    )
    builder.row(
        InlineKeyboardButton(text='➡️ Janr tanlash', switch_inline_query_current_chat='#filter_genre')
    )
    builder.row(
        InlineKeyboardButton(text='➡️ Mamlakat tanlash', switch_inline_query_current_chat='#filter_country')
    )
    builder.row(
        InlineKeyboardButton(text='🎲 Tasodifiy kino', switch_inline_query_current_chat='random_movie')
    )
    builder.row(
        InlineKeyboardButton(text='🔂 Tozalash', callback_data='clear_filter')
    )
    builder.row(
        InlineKeyboardButton(text='🔍 Qidiruv', callback_data='search')
    )
    builder.row(
        InlineKeyboardButton(text='🔍 Filtr bo\'yicha qidirish', switch_inline_query_current_chat='#filter')
    )
    return builder.as_markup()
