from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def mian_inline_keyboards():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="ℹ️ Video qo'llanma", callback_data='video_guide'),
        InlineKeyboardButton(text='⚙️ Sozlamalar', callback_data='settings')

    )
    builder.row(
        InlineKeyboardButton(text='🔍 Qidiruvni boshlash', switch_inline_query_current_chat='')
    )
    return builder.as_markup()
