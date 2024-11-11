from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from bot.api.movies.categories import Category
from bot.buttons.inline_buttons.movies.categories import categories_by_parent_btn, categories_list_btn
from bot.models.movies.movies import MovieModel


async def sub_categories(query: types.CallbackQuery, state: FSMContext, bot: Bot):
    if query.data == 'backtocategory':
        await bot.edit_message_text('what are you going to add?', chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=categories_list_btn(1))

    elif query.data.startswith('categoryprev'):
        page = int(query.data.split('_')[-1]) - 1
        await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=categories_list_btn(page))

    elif query.data.startswith('categorynext'):
        page = int(query.data.split('_')[-1]) + 1
        await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=categories_list_btn(page))

    elif query.data.startswith('subcategoryprev'):
        page = int(query.data.split('_')[-1]) - 1
        parent_id = int(query.data.split('_')[1])
        await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=categories_by_parent_btn(parent_id, page))

    elif query.data.startswith('subcategorynext'):
        page = int(query.data.split('_')[-1]) + 1
        parent_id = int(query.data.split('_')[1])
        await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=categories_by_parent_btn(parent_id, page))

    else:
        category_id = int(query.data.split('_')[-1])
        category = Category().categories_by_parent(category_id)

        if len(category) == 0:
            await state.update_data(category_id=category_id)
            await state.set_state(MovieModel.title)
            await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
            await bot.send_message(query.from_user.id, 'title:')

        else:
            category_name = query.data.split('_')[1]
            await bot.edit_message_text(
                chat_id=query.from_user.id, message_id=query.message.message_id,
                text=category_name, reply_markup=categories_by_parent_btn(parent_id=category_id)
            )