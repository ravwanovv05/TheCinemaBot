import pytz
from datetime import datetime
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from bot.api.movies.categories import Category
from bot.buttons.inline_buttons.movies.filters import filters_inline_keyboards


async def filter_movie(message: types.Message):
    await message.answer(
        'Qidiruv filtri \n\n Filtrlarni tanlang va "🔍Filtr bo\'yicha qidirish" tugmasini bosing \n\n'
        '\n Tanlangan: \n➡️ Yil: hammasi '
        '\n➡️ Turi: hammasi \n➡️ Janr: hammasi \n➡️ Mamlakat: hammasi',
        reply_markup=filters_inline_keyboards()
    )


async def select_data(inline_query: types.InlineQuery, state: FSMContext, bot: Bot):
    query = inline_query.query
    data = await state.get_data()
    keys = list(data.keys())

    print(data)
    results = []

    if query == 'filter_from_year' or query == 'filter_to_year':
        current_year = datetime.now(pytz.timezone('Asia/Tashkent')).year
        for year in list(range(1975, current_year + 1)):
            if query == 'filter_from_year' and 'from_year' in keys and data['from_year'] == year:
                year = str(year) + '✅'
            if query == 'filter_to_year' and 'to_year' in keys and data['to_year'] == year:
                year = str(year) + '✅'

            results.append(
                InlineQueryResultArticle(
                    id=str(year),
                    title=str(year),
                    input_message_content=InputTextMessageContent(message_text=f"{query}_{year}")
                )
            )
    elif query == 'filter_type':
        categories = Category().categories()
        for category in categories:
            if 'type' in keys and int(data['type'].split('_')[-1]) == int(category['id']):
                title = category['name'] + '✅'
            else:
                title = category['name']
            results.append(
                InlineQueryResultArticle(
                    id=str(category['id']),
                    title=title,
                    input_message_content=InputTextMessageContent(
                        message_text=f"{query}_{category['name']}_{category['id']}"
                    )
                )
            )

    await bot.answer_inline_query(inline_query.id, results=results, cache_time=0, request_timeout=0)


async def selected_data(message: types.Message, state: FSMContext, bot: Bot):
    if message.text.startswith('filter_from_year'):
        await bot.delete_message(message.chat.id, message.message_id)
        await state.update_data(from_year=int(message.text.split('_')[-1]))

    elif message.text.startswith('filter_to_year'):
        await bot.delete_message(message.chat.id, message.message_id)
        await state.update_data(to_year=int(message.text.split('_')[-1]))

    elif message.text.startswith('filter_type'):
        await bot.delete_message(message.chat.id, message.message_id)
        await state.update_data(type=message.text)

    data = await state.get_data()
    keys = list(data.keys())

    from_year = f"{data['from_year']} dan" if 'from_year' in keys else 'hammasi'
    to_year = f"{data['to_year']} gacha" if 'to_year' in keys else ''
    type_ = f"{data['type']} dan" if 'type' in keys else 'hammasi'

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await message.answer(
        f'Qidiruv filtri \n\n Filtrlarni tanlang va "🔍Filtr bo\'yicha qidirish" tugmasini bosing \n\n'
        f'\n Tanlangan: \n'
        f'➡️ Yil: {from_year} {to_year}\n'
        f'➡️ Turi: {type_} \n'
        f'➡️ Janr: hammasi \n'
        f'➡️ Mamlakat: hammasi',
        reply_markup=filters_inline_keyboards()
    )

