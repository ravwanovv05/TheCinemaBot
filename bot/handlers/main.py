from aiogram import types
from bot.api.users.telegram_users import TelegramUser
from bot.buttons.inline_buttons.inline_queries import search_inline
from bot.buttons.inline_buttons.movies.categories import categories_list_btn
from bot.buttons.reply_buttons.main import main_btn
from utils.users.telegram_users import read_file, write_file


async def start(message: types.Message):
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

    await message.answer(f"Xush kelibsiz {message.from_user.first_name}", reply_markup=main_btn())


async def new(message: types.Message):
    user = TelegramUser().tg_user_details(message.from_user.id)
    if user['role'] in ('director', 'manager', 'admin'):
        await message.answer('what are you going to add?', reply_markup=categories_list_btn(1))


async def search_movies(message: types.Message):
    await message.answer('Kerakli filmni topish uchun "Qidiruvni boshlash" tugmasini bosing va so\'rovingizni kiriting.', reply_markup=search_inline())
