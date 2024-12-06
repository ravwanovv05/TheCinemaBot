from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from bot.buttons.inline_buttons.movies.categories import categories_list_btn
from bot.models.movies.movies import MovieModel


async def sub_categories(query: types.CallbackQuery, state: FSMContext, bot: Bot):
    if query.data == 'backtocategory':
        await bot.edit_message_text(
            'what are you going to add?', chat_id=query.from_user.id, message_id=query.message.message_id,
            reply_markup=categories_list_btn(1)
        )

    elif query.data.startswith('categoryprev'):
        page = int(query.data.split('_')[-1]) - 1
        await bot.edit_message_reply_markup(
            chat_id=query.from_user.id, message_id=query.message.message_id,
            reply_markup=categories_list_btn(page)
        )

    elif query.data.startswith('categorynext'):
        page = int(query.data.split('_')[-1]) + 1
        await bot.edit_message_reply_markup(
            chat_id=query.from_user.id, message_id=query.message.message_id,
            reply_markup=categories_list_btn(page)
        )

    else:
        category_id = int(query.data.split('_')[-1])

        await state.update_data(category_id=category_id)
        await state.set_state(MovieModel.title)
        await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        await bot.send_message(query.from_user.id, 'title:')

