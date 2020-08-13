from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/info - Посмотреть информацию о текущем сезоне',
        '/standings - Просмотреть турнирную таблицу',
        '/fixtures - Просмотреть расписание предстоящих туров',
        '/results - Посмотреть результаты прошедших матчей'
    ]
    await message.answer('\n'.join(text))
