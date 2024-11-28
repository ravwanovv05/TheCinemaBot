from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from bot.api.users.telegram_users import TelegramUser
from bot.models.advertising import Advert


async def advert(message: types.Message, state: FSMContext):
    await state.set_state(Advert.post)
    await message.answer('send post')

async def send_post_for_all_users(message: types.Message, state: FSMContext, bot: Bot):
    users = TelegramUser().list()
    count = 0

    for user in users:
        try:
            await bot.copy_message(chat_id=user['telegram_id'], from_chat_id=message.from_user.id, message_id=message.message_id)
            update_user = TelegramUser().update(user['id'], {'active': True})
            count += 1
        except Exception as e:
            update_user = TelegramUser().update(user['id'], {'active': False})
            print(str(e))
    await state.clear()
    await message.answer(f"Successfully post has been sent to {count} users")
