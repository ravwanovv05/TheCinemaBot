from aiogram import types, Bot
from bot.buttons.inline_buttons.main import mian_inline_keyboards
from bot.buttons.inline_buttons.movies.collections import collections_inline_keyboards
from bot.buttons.reply_buttons.main import main_reply_keyboards


async def collections_handler(message: types.Message, bot: Bot):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await message.answer(
        '🗂 Filmlar va seriallar to\'plami\n\n🍿 tomosha qilishdan zavqlaning! 🍿',
        reply_markup=collections_inline_keyboards()
    )


async def back_to_main_handler(query: types.CallbackQuery, bot: Bot):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.from_user.id, '/start', reply_markup=main_reply_keyboards())
    await bot.send_message(
        query.from_user.id,
        '🔍 Qidirish uchun quyidagi tugmalardan foydalaning.',
        reply_markup=mian_inline_keyboards()
    )

