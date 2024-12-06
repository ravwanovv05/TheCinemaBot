from aiogram import types, Bot
from bot.api.users.telegram_users import TelegramUser
from bot.buttons.inline_buttons.main import mian_inline_keyboards
from bot.buttons.inline_buttons.movies.categories import categories_list_btn
from bot.buttons.reply_buttons.main import main_reply_keyboards
from utils.users.telegram_users import read_file, write_file


async def start(message: types.Message, bot: Bot):
    telegram_id = message.from_user.id
    users = read_file('users.json')
    users_id = []
    for user in users:
        users_id.append(user['telegram_id'])

    if telegram_id not in users_id:
        users.append(
            {
                'telegram_id': telegram_id,
            }
        )
        write_file('users.json', users)
        create_user = TelegramUser(
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            telegram_id=telegram_id
        ).create_telegram_user()
    else:
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await bot.delete_message(message.chat.id, message.message_id)

    await message.answer('/start', reply_markup=main_reply_keyboards())
    await message.answer(
        '🍿 Salom, kino ixlosmandlari! \n\n 🔍 Qidirish uchun quyidagi tugmalardan foydalaning.',
        reply_markup=mian_inline_keyboards()
    )


async def new(message: types.Message):
    user = TelegramUser().tg_user_details(message.from_user.id)
    if user['role'] in ('director', 'manager', 'admin'):
        await message.answer('what are you going to add?', reply_markup=categories_list_btn(1))

